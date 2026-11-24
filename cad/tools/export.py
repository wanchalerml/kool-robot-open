"""Export ชิ้นงาน build123d → cad/out/<name>.step + .3mf + รูปพรีวิว .png 3 มุม

รูปพรีวิวใช้ตัวเรนเดอร์ z-buffer ที่เขียนเองด้วย numpy + Pillow (ไม่ต้องมี OpenGL/VTK
จึงรันบนเซิร์ฟเวอร์ได้) · มุมกล้องแบบ orthographic: iso / top / front
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from build123d import Compound, Mesher, Shape, export_step

OUT_DIR = Path(__file__).resolve().parent.parent / "out"

# มุมกล้อง: (ชื่อ, ทิศจากวัตถุไปกล้อง, ทิศขึ้นของจอ)
VIEWS = [
    ("iso", (1.0, -1.3, 1.1), (0, 0, 1)),
    ("top", (0.0, 0.0, 1.0), (0, 1, 0)),
    ("front", (0.0, -1.0, 0.35), (0, 0, 1)),
]
PALETTE = [(70, 140, 220), (235, 150, 60), (90, 180, 110), (200, 90, 160)]


# ---------------------------------------------------------------- export


def export_part(name: str, parts: dict[str, Shape], out_dir: Path = OUT_DIR,
                tol: float = 0.01) -> list[Path]:
    """parts = {ชื่อชิ้น: shape} วางตำแหน่งไว้แล้ว (ทุกชิ้นวางบนพื้น z=0)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []

    step = out_dir / f"{name}.step"
    comp = Compound(children=[_labeled(s, k) for k, s in parts.items()], label=name)
    export_step(comp, str(step))
    files.append(step)

    m3 = out_dir / f"{name}.3mf"
    mesher = Mesher()
    for k, s in parts.items():
        mesher.add_shape(s, linear_deflection=tol, angular_deflection=0.1, part_number=k)
    mesher.write(str(m3))
    files.append(m3)

    meshes = [(_mesh(s, tol * 2), PALETTE[i % len(PALETTE)]) for i, s in enumerate(parts.values())]
    imgs = []
    for vname, d, up in VIEWS:
        img = render(meshes, d, up)
        _caption(img, f"{name} · {vname}")
        p = out_dir / f"{name}_{vname}.png"
        img.save(p)
        files.append(p)
        imgs.append(img)

    # แผ่นรวม 3 มุมในรูปเดียว (ไว้แนบรายงาน)
    w, h = imgs[0].size
    sheet = Image.new("RGB", (w * 3, h), (255, 255, 255))
    for i, im in enumerate(imgs):
        sheet.paste(im, (i * w, 0))
    p = out_dir / f"{name}_preview.png"
    sheet.save(p)
    files.append(p)
    return files


def _labeled(s: Shape, label: str) -> Shape:
    s.label = label
    return s


def _mesh(s: Shape, tol: float):
    v, t = s.tessellate(tol, 0.2)
    return np.array([[p.X, p.Y, p.Z] for p in v], float), np.array(t, int)


# ---------------------------------------------------------------- renderer


def render(meshes, view_dir, up, size=(800, 600), ss=2, margin=0.08) -> Image.Image:
    d = np.asarray(view_dir, float); d /= np.linalg.norm(d)
    r = np.cross(up, d); r /= np.linalg.norm(r)
    u = np.cross(d, r)
    W, H = size[0] * ss, size[1] * ss

    allv = np.vstack([v for (v, _), _ in meshes])
    sx, sy = allv @ r, allv @ u
    span = max((sx.max() - sx.min()) / (1 - 2 * margin) / W,
               (sy.max() - sy.min()) / (1 - 2 * margin) / H)
    cx, cy = (sx.max() + sx.min()) / 2, (sy.max() + sy.min()) / 2

    zbuf = np.full((H, W), -np.inf)
    col = np.zeros((H, W, 3))
    nbuf = np.zeros((H, W, 3))
    light = d * 0.55 + u * 0.55 + r * 0.35; light /= np.linalg.norm(light)

    for (v, tris), rgb in meshes:
        px = (v @ r - cx) / span + W / 2
        py = H / 2 - (v @ u - cy) / span
        pz = v @ d
        a, b, c = v[tris[:, 0]], v[tris[:, 1]], v[tris[:, 2]]
        n = np.cross(b - a, c - a)
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        n[(n @ d) < 0] *= -1                      # สองหน้า: หันหาแสงเสมอ
        shade = 0.35 + 0.65 * np.clip(n @ light, 0, 1)
        base = np.asarray(rgb, float) / 255
        for i, (i0, i1, i2) in enumerate(tris):
            _raster(px[[i0, i1, i2]], py[[i0, i1, i2]], pz[[i0, i1, i2]],
                    base * shade[i], n[i], zbuf, col, nbuf)

    # เส้นขอบ: ความลึกหรือทิศผิวเปลี่ยนแรง
    hit = np.isfinite(zbuf)
    zf = np.where(hit, zbuf, (zbuf[hit].min() if hit.any() else 0) - 1e3)
    edge = np.zeros_like(hit)
    # ความลึกใช้ผลต่างอันดับสอง (ผิวเรียบเอียงแค่ไหนก็ = 0) · ทิศผิวใช้ dot ของ normal
    thr = 3 * span
    e = np.abs(zf[2:] - 2 * zf[1:-1] + zf[:-2]) > thr
    edge[1:-1] |= e
    e = np.abs(zf[:, 2:] - 2 * zf[:, 1:-1] + zf[:, :-2]) > thr
    edge[:, 1:-1] |= e
    e = (np.sum(nbuf[1:] * nbuf[:-1], axis=2) < 0.85) & hit[1:] & hit[:-1]
    edge[1:] |= e
    e = (np.sum(nbuf[:, 1:] * nbuf[:, :-1], axis=2) < 0.85) & hit[:, 1:] & hit[:, :-1]
    edge[:, 1:] |= e
    img = np.ones((H, W, 3)) * 0.97
    img[hit] = col[hit]
    img[edge] = img[edge] * 0.25
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    return out.resize(size, Image.LANCZOS)


def _raster(x, y, z, rgb, n, zbuf, col, nbuf):
    H, W = zbuf.shape
    x0, x1 = max(int(np.floor(x.min())), 0), min(int(np.ceil(x.max())), W - 1)
    y0, y1 = max(int(np.floor(y.min())), 0), min(int(np.ceil(y.max())), H - 1)
    if x0 > x1 or y0 > y1:
        return
    den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
    if abs(den) < 1e-12:
        return
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
    w0 = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / den
    w1 = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / den
    w2 = 1 - w0 - w1
    m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not m.any():
        return
    zz = w0 * z[0] + w1 * z[1] + w2 * z[2]
    sub = zbuf[y0:y1 + 1, x0:x1 + 1]
    m &= zz > sub
    sub[m] = zz[m]
    col[y0:y1 + 1, x0:x1 + 1][m] = rgb
    nbuf[y0:y1 + 1, x0:x1 + 1][m] = n


def _caption(img: Image.Image, text: str):
    dr = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans.ttf", 18)
    except OSError:
        f = ImageFont.load_default()
    dr.text((12, 10), text, fill=(60, 60, 60), font=f)

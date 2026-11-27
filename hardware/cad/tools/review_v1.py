"""ตรวจทานชิ้นพิมพ์ V1 ก่อนพิมพ์จริง (27 พ.ย. 2569 v12)
อ่าน pieces.json (จาก slice_v1/pieces.py) → ต่อชิ้น: ปิดผิว (watertight) · จำนวนก้อน · ลงเตียง 256 (หลังหมุนจาก jobs.json)
· ความหนาผนัง (ยิงรังสีเข้าเนื้อจากจุดสุ่มบนผิว: เปอร์เซ็นไทล์ 2 / 10) → cad/out/show_v1_review.json
เกณฑ์ผนัง: เปลือก PLA ≥ 1.6 (4 เส้น 0.4) · ชิ้นโครง ≥ 2.0 · TPU ≥ 1.2 · ต่ำกว่าเกณฑ์ = ดูจุดนั้นเอง (ขอบบาง/ครีบ อาจตั้งใจ)
"""
import json, os, sys
import numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "out")
W = os.environ.get("SLICE_WORK", "/tmp/slice_v1")
N = int(os.environ.get("REVIEW_N", "1500"))
rng = np.random.default_rng(7)
P = json.load(open(os.path.join(W, "pieces.json")))
jobs = json.load(open(os.path.join(W, "jobs.json"))) if os.path.exists(os.path.join(W, "jobs.json")) else []
fit = {}
for j in jobs:
    fit.setdefault(j["file"], []).append(j.get("ext"))


def walls(m):
    pts, fi = trimesh.sample.sample_surface(m, N, seed=7)
    nrm = m.face_normals[fi]
    org = pts - nrm * 0.02
    try:
        loc, ir, it = m.ray.intersects_location(org, -nrm, multiple_hits=False)
    except Exception:
        return None
    d = np.full(len(org), np.nan)
    d[ir] = np.linalg.norm(loc - org[ir], axis=1)
    d = d[np.isfinite(d)]
    return d


res = []
for p in P:
    f = p["file"]
    m = trimesh.load(os.path.join(OUT, f))
    d = walls(m)
    th = 1.2 if p["mat"] == "TPU" else (1.6 if p["prof"].startswith("pla") or p["prof"] == "pc_face" else 2.0)
    r = dict(file=f, mat=p["mat"], n=p["n"], group=p["group"], watertight=bool(m.is_watertight),
             bodies=int(m.body_count), vol_cm3=round(float(m.volume) / 1000, 1),
             ext=[round(float(x), 1) for x in m.extents], thr=th)
    if d is not None and len(d):
        r.update(p2=round(float(np.percentile(d, 2)), 2), p10=round(float(np.percentile(d, 10)), 2),
                 thin_pct=round(float((d < th).mean() * 100), 1))
    res.append(r)
    print(f, r.get("p2"), r.get("thin_pct"), r["watertight"], flush=True)
json.dump(res, open(os.path.join(OUT, "show_v1_review.json"), "w"), ensure_ascii=False, indent=0)
print(len(res), "pieces")

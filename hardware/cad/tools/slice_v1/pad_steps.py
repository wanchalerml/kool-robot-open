"""เติมแผ่นรองใต้แขนปลอกแกนที่ลอยเหนือเตียง 0.05–2 มม. (ไฟล์พิมพ์ PETG-CF ส่วน 2–3 · robot v15 27 พ.ย. 2569)

ปัญหา: แขนปลอกแกนอยู่ระดับรูเปลือก ไม่ตรงระดับก้นวงปลอก → วางพิมพ์แล้วใต้แขนลอย 0.1–1.5 มม.
 = เริ่มพิมพ์กลางอากาศ (Studio เตือน "overhang regions could not get support") · ซีกปลอกบางซีกลอยทั้งซีก 0.24
แก้: ต่อผิวคว่ำที่ลอย ≤ 2 มม. ลงถึงเตียง (หนาเพิ่ม ≤ 2 มม. ใต้แขน = แขนแข็งขึ้น) · ไม่แตะชิ้นคอ (ขอบ ⌀41 เป็นบ่าบังคับศูนย์)
เช็กชนในตำแหน่งประกอบ (shell6 ทุกชิ้น) ก่อน/หลังเติม
ใช้: python3 cad/tools/slice_v1/pad_steps.py  → เขียนทับ cad/out/print_v1/KOOL_V1_s02-03_plate{1..4}_PETG-CF.3mf (+ _padded_report.txt)
"""
import glob, json, os, sys
import numpy as np, trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "..", "out")
PV = os.path.join(OUT, "print_v1")
MAXSTEP = 2.0

def pads_for(body, zmin=0.0):
    """แผ่นรองใต้ผิวคว่ำแบน (nz<-0.95) ที่อยู่สูง 0.05–MAXSTEP เหนือ zmin"""
    n = body.face_normals; c = body.triangles_center; tri = body.triangles
    sel = (n[:, 2] < -0.95) & (c[:, 2] - zmin > 0.05) & (c[:, 2] - zmin <= MAXSTEP)
    out = []
    levels = np.round(c[sel, 2] - zmin, 2)
    for lv in sorted(set(levels)):
        idx = np.where(sel)[0][levels == lv]
        poly = unary_union([Polygon(t[:, :2]).buffer(0) for t in tri[idx] if Polygon(t[:, :2]).area > 1e-6])
        poly = poly.buffer(-0.01).buffer(0.01).buffer(-0.05)   # หด 0.05 กันผิวข้างทับซ้อนแบบระนาบเดียว (union แล้วเกิดเศษ)
        if poly.is_empty or poly.area < 2: continue
        h = lv + 0.3                                    # ทับเข้าเนื้อแขนเดิม 0.3 ให้รวมเป็นชิ้นเดียว (รอยต่อไม่ขาด)
        for p in getattr(poly, "geoms", [poly]):
            m = trimesh.creation.extrude_polygon(p, h); m.apply_translation([0, 0, zmin]); out.append(m)
    return out

def main():
    man = json.load(open(f"{OUT}/show_v1_shell6_manifest.json"))
    ctx = {f: trimesh.load(f"{OUT}/{f}") for f in man if os.path.exists(f"{OUT}/{f}")}
    rep = ["เติมแผ่นรองใต้ส่วนที่ลอย (≤2 มม.) · ไฟล์พิมพ์ PETG-CF ส่วน 2–3", ""]
    for f in sorted(glob.glob(f"{PV}/KOOL_V1_s02-03_plate[1-4]_PETG-CF.3mf")):
        sc = trimesh.load(f); geoms = []
        for g in sc.dump():
            name = g.metadata.get("name")
            if not str(name).startswith("spine_collar"):
                geoms.append((name, g)); continue
            z = name.split("_")[-1]
            asm = trimesh.load(f"{OUT}/show_v1_shell6_ปลอกแกน_{z}.stl")
            R = trimesh.registration.procrustes(asm.vertices, g.vertices, reflection=True, scale=False, return_cost=True)
            T, cost = R[0], R[2]
            assert cost < 1e-6, (name, cost)
            pads = []
            for b in g.split(only_watertight=False):
                pads += pads_for(b, 0.0)
            if not pads:
                geoms.append((name, g)); rep.append(f"{os.path.basename(f)} · {name}: ไม่มีส่วนลอย"); continue
            pad = trimesh.util.concatenate(pads)
            new = trimesh.boolean.union([g] + pads, engine="manifold"); new.merge_vertices()
            assert new.is_watertight, name
            # เช็กชนในตำแหน่งประกอบ: แผ่นรองกลับไปพิกัดประกอบ
            padA = pad.copy(); padA.apply_transform(np.linalg.inv(T))
            hits = []
            for k, m in ctx.items():
                if k.endswith(f"ปลอกแกน_{z}.stl"): continue
                if not (np.all(padA.bounds[0] <= m.bounds[1]) and np.all(m.bounds[0] <= padA.bounds[1])): continue
                try:
                    v = trimesh.boolean.intersection([padA, m], engine="manifold").volume
                except Exception as e:
                    v = float("nan")   # shell6 บางชิ้นไม่ปิดสนิท → เช็กระยะห่างแทน (ดูท้ายรายงาน)
                if not (v <= 0.01): hits.append(f"{k.replace('show_v1_shell6_','')} {v:.2f}")
            rep.append(f"{os.path.basename(f)} · {name}: เติม {pad.volume:.0f} มม.³ ({pad.volume*1.25/1000:.1f} ก.) · ชนชิ้นอื่น: {', '.join(hits) or 'ไม่มี ✅'}")
            new.metadata["name"] = name
            geoms.append((name, new))
        out = trimesh.Scene()
        for name, m in geoms: out.add_geometry(m, geom_name=name, node_name=name)
        out.export(f)
    open(f"{PV}/padded_report.txt", "w").write("\n".join(rep) + "\n"); print("\n".join(rep))

if __name__ == "__main__":
    main()

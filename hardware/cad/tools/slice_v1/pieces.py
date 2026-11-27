"""V1 print-piece list (colour option ข, 27 พ.ย. 07:22) -> pieces.json"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "..", "out"); W = os.environ.get("SLICE_WORK", "/tmp/slice_v1"); os.makedirs(W, exist_ok=True)
man = json.load(open(f"{OUT}/show_v1_shell6_manifest.json"))
P = []
def add(f, mat, n, prof, group):
    P.append(dict(file=f, mat=mat, n=n, prof=prof, group=group))
BLACK_PLA_SHELL = ("เอว_", "สะโพก_", "มือขวา", "ปุ่มสะโพก", "ปุ่มเข่า")
for f, i in man.items():
    if i.get("bought") or "ตัวแทน" in f: continue
    n = 2 if i.get("mirror") else 1
    k = f.replace("show_v1_shell6_", "")
    m = i["mat"]
    if m == "PLA ขาว":
        mat = "PLA ดำ" if k.startswith(BLACK_PLA_SHELL) else "PLA ขาว"   # ข: เชิงกราน + มือ = ดำ
        add(f, mat, n, "pla_shell", "เปลือก")
    elif m == "PLA ดำ":
        add(f, "PLA ดำ", n, "pla_shell", "เปลือก")
    elif m.startswith("PETG-CF ดำ"):
        add(f, "PETG-CF", n, "petgcf_joint", "ปุ่มข้อแขน")
    elif m == "PETG-CF":
        light = k.startswith(("ถาด_", "ถ้วย", "กรอบไมค์", "กรงแบต"))
        add(f, "PETG-CF", n, "petgcf_light" if light else "petgcf_struct", "โครง")
    elif m == "PAHT-CF":
        add(f, "PAHT-CF", n, "pahtcf_beam" if k.startswith("ปลั๊ก") else "pahtcf_struct", "โครง")
    elif m.startswith("TPU"):
        add(f, "TPU", n, "tpu", "ยาง")
    else:
        raise SystemExit(f"? {f} {m}")
# หัว v4
add("show_v1_head4_เปลือกขาว_หน้า.stl", "PLA ขาว", 1, "pla_shell", "เปลือก")
add("show_v1_head4_เปลือกขาว_หลัง.stl", "PLA ขาว", 1, "pla_shell", "เปลือก")
add("show_v1_head4_หน้ากากใน.stl", "PLA ดำ", 1, "pla_shell", "เปลือก")
add("show_v1_head4_ฝาหน้า_ตัวแทน.stl", "PC Clear Black", 1, "pc_face", "หน้า")
# คอ = ดำ ตามแบบ ข แต่เป็นข้อฝืด M8 (แรงหนีบ ~319 N) → PETG-CF ดำ (PLA ไหลตัวใต้ M8)
add("show_v1_frame_upper_คอบน_โครงหัว.stl", "PETG-CF", 1, "petgcf_struct", "คอ")
add("show_v1_frame_upper_ฐานคอ.stl", "PETG-CF", 1, "petgcf_struct", "คอ")
# เท้า ×2
FOOT = {"คานนอก": ("PAHT-CF", "pahtcf_beam"), "คานใน": ("PAHT-CF", "pahtcf_beam"),
        "บล็อกข้อเท้า": ("PAHT-CF", "pahtcf_beam"), "ซ็อกเก็ตขา": ("PAHT-CF", "pahtcf_beam"),
        "ดรัมข้อเท้า_หน้า": ("PLA ดำ", "pla_shell"), "ดรัมข้อเท้า_หลัง": ("PLA ดำ", "pla_shell"),
        "ฝาปุ่มข้อเท้า": ("PETG-CF", "petgcf_light"), "ฝาปลายเพลานอก": ("PETG-CF", "petgcf_light"),
        "รางสายใน": ("PETG-CF", "petgcf_light"), "ที่ยึด_ToF_หน้า": ("PETG-CF", "petgcf_light"),
        "ที่ยึด_ToF_หลัง": ("PETG-CF", "petgcf_light"),
        "ปลอกกันฝุ่นล่าง_TPU": ("TPU", "tpu"), "ปลอกกันฝุ่นบน_TPU": ("TPU", "tpu"), "หัวกันยุบ_TPU": ("TPU", "tpu"), "หมุดหยุด_M5_ปลอกTPU": ("TPU", "tpu")}
for k, (mat, prof) in FOOT.items():
    add(f"show_v1_foot1_{k}.stl", mat, 2, prof, "เท้า")
add("show_v1_foot1_TEST_คานทดสอบแขวน_PAHT-CF.stl", "PAHT-CF", 1, "pahtcf_beam", "ทดสอบ")
# จิ๊กเจาะ (เครื่องมือ · PLA สีไหนก็ได้ · 27 พ.ย. v12 ทำเองไม่พึ่งร้านตัดเลเซอร์/กลึง)
for f in sorted(os.listdir(OUT)):
    if f.startswith("show_v1_pelvis_") and f.endswith("_PLA.stl"):
        add(f, "PLA (จิ๊ก)", 1, "pla_black", "จิ๊ก")
# กล่องจออก
for k in ("กรอบหน้า", "ฝาหลัง", "บานพับอก", "แผ่นรองใน"):
    add(f"show_v1_chest_tilt_{k}.stl", "PETG-CF", 1, "petgcf_light", "จอ")
for k in ("ยางกันชน_ก้ม_TPU",):
    add(f"show_v1_chest_tilt_{k}.stl", "TPU", 2, "tpu", "จอ")
for p in P:
    assert os.path.exists(f"{OUT}/{p['file']}"), p["file"]
json.dump(P, open(os.path.join(W, "pieces.json"), "w"), ensure_ascii=False, indent=0)
print(len(P), "files", sum(p["n"] for p in P), "pieces")

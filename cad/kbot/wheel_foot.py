"""เท้าล้อ K-Bot (ร่าง v0 · KOOL 24 พ.ย. 2569 · #robot-wheel-feet) — พิมพ์ X2D
แนวคิด: เท้าละ 2 ล้อ หน้า-หลัง + เบรก · กางขาด้วย hip roll ตอนหยุด
ชิ้น:
  1) truck  — ตัวรถเท้า: แผ่นล่าง + ส้อมล้อ 2 คู่ (ล้อ PU ⌀80 กว้าง 30 · เพลา ⌀8 + ลูกปืน 608) · ฐานล้อ WB มม.
              ล้อหน้า = ขับด้วย RobStride 00 (ยึดข้างส้อม · ลาย 4 รู ร่าง ต้องเช็กกับ STEP ของ RS00)
              รูสลักเบรก (solenoid สปริงดันล็อก ไฟดับ = ล็อก) ทั้ง 2 ล้อ
  2) pivot  — ข้อพับข้าง (passive roll ±12°) ระหว่างข้อเท้า K-Bot กับ truck: เพราะ K-Bot ข้อเท้ามีแกนเดียว
              กางขา 10° แล้วเท้าจะเอียง 10° → pivot ทำให้ล้อทั้ง 2 วางแบนกับพื้น · มีบัมเปอร์ TPU คืนศูนย์
  3) brake_disc — จานรูสลักติดดุมล้อ (8 รู ⌀6.5 ที่รัศมี 28)
⚠️ หน้าแปลนยึดข้อเท้า K-Bot = ตำแหน่งชั่วคราว (4×M4 สี่เหลี่ยม 40) — แก้หลังได้ STEP จริง
ใช้: python3 cad/kbot/wheel_foot.py → cad/out/kbot_wheel_foot_*.{stl,step} + _preview.png"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from build123d import *
import params as P
OUT = os.path.join(os.path.dirname(__file__), "..", "out"); os.makedirs(OUT, exist_ok=True)
WB = 230.0        # ระยะล้อหน้า-หลัง (ทั้งชิ้นยาว ~WB+90 ต้อง ≤ 256 → แบ่ง 2 ท่อนถ้ายาวเกิน)
WD, WW = 80.0, 30.0   # ล้อ PU
AX = 8.0          # เพลา
BRG = 22.0        # ลูกปืน 608 นอก ⌀22 หนา 7
T = 6.0           # ความหนาแผ่น/ส้อม (ชิ้นรับแรง)
GAP = 2.0         # ช่องข้างล้อ
FORK_IN = WW + 2 * GAP            # ระยะในส้อม
W = FORK_IN + 2 * T               # ความกว้าง truck
H_AX = WD / 2 + 4.0               # เพลาสูงจากพื้น (ล้อแตะพื้น · แผ่นลอย 4 มม.)
L = WB + WD * 0.5 + 2 * T         # ความยาวแผ่นล่าง
def truck():
    base = Box(L, W, T, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, H_AX + 6)))
    parts = base
    for x in (-WB / 2, WB / 2):
        for y in (-(FORK_IN / 2 + T / 2), FORK_IN / 2 + T / 2):
            plate = Box(WD * 0.75, T, H_AX + 6 - (H_AX - 14), align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, H_AX - 14)))
            parts += plate
        # รูเพลา + บ่าลูกปืน (แนวนอน → เผื่อ HORIZONTAL_HOLE_EXTRA)
        parts -= Cylinder(AX / 2 + (P.FIT_LOOSE + P.HORIZONTAL_HOLE_EXTRA) / 2, W + 2, rotation=(90, 0, 0)).moved(Location((x, 0, H_AX)))
        for y in (-(FORK_IN / 2 + T), FORK_IN / 2 + T):
            parts -= Cylinder(BRG / 2 + P.FIT_PRESS / 2, 7.2 * 2, rotation=(90, 0, 0)).moved(Location((x, y, H_AX)))
        # รูสลักเบรก ⌀6.5 ผ่านส้อมด้าน +y ที่รัศมี 28 เหนือเพลา
        parts -= Cylinder(3.25 + P.FIT_SLIDE, W + 2, rotation=(90, 0, 0)).moved(Location((x, 0, H_AX + 28)))
        # ช่องล้อในแผ่นล่าง
        parts -= Box(WD * 0.5, FORK_IN, T * 3).moved(Location((x, 0, H_AX + 6)))
    # รูยึด RS00 ข้างส้อมหน้า (+x, +y) — ร่าง: 4×M3 บนวง ⌀40 รอบเพลา
    for ang in (45, 135, 225, 315):
        import math
        parts -= Cylinder(1.7, 20, rotation=(90, 0, 0)).moved(Location((WB / 2 + 20 * math.cos(math.radians(ang)), W / 2, H_AX + 20 * math.sin(math.radians(ang)))))
    # บ่ารับ pivot กลางแผ่น (หูยึดแกน roll ตามแนว x)
    for x in (-28, 28):
        ear = Box(10, W, 26, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0, H_AX + 6 + T)))
        parts += ear
    parts -= Cylinder(4.0 + (P.FIT_SLIDE + P.HORIZONTAL_HOLE_EXTRA) / 2, 80, rotation=(0, 90, 0)).moved(Location((0, 0, H_AX + 6 + T + 16)))
    return parts
def pivot():
    # บล็อกข้อเท้า: ห้อยระหว่างหูทั้งสอง หมุนรอบแกน x ±12° · บนเป็นหน้าแปลนยึดข้อเท้า K-Bot (ชั่วคราว)
    blk = Box(44, W - 4, 30, align=(Align.CENTER, Align.CENTER, Align.MIN))
    blk -= Cylinder(4.0 + P.FIT_SLIDE / 2, 60, rotation=(0, 90, 0)).moved(Location((0, 0, 10)))
    fl = Box(56, 56, T, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, 30)))
    blk += fl
    for x in (-20, 20):
        for y in (-20, 20):
            blk -= Cylinder(2.2, 40).moved(Location((x, y, 30)))
    # ช่องบัมเปอร์ TPU 2 ข้าง (คืนศูนย์ + หยุดที่ ±12°)
    for y in (-(W - 4) / 2 + 4, (W - 4) / 2 - 4):
        blk -= Box(30, 6, 6).moved(Location((0, y, 1)))
    return blk
def brake_disc():
    import math
    dsk = Cylinder(34, 4) - Cylinder(AX / 2 + P.FIT_SLIDE / 2, 10)
    for k in range(8):
        a = 2 * math.pi * k / 8
        dsk -= Cylinder(3.25 + P.FIT_LOOSE / 2, 10).moved(Location((28 * math.cos(a), 28 * math.sin(a), 0)))
    for k in range(4):
        a = 2 * math.pi * k / 4 + math.pi / 4
        dsk -= Cylinder(1.7, 10).moved(Location((16 * math.cos(a), 16 * math.sin(a), 0)))
    return dsk
parts = {"truck": truck(), "pivot": pivot(), "brake_disc": brake_disc()}
rep = []
for n, p in parts.items():
    bb = p.bounding_box(); v = p.volume
    export_stl(p, os.path.join(OUT, f"kbot_wheel_foot_{n}.stl")); export_step(p, os.path.join(OUT, f"kbot_wheel_foot_{n}.step"))
    import math as _m
    xy = sorted((bb.size.X, bb.size.Y)); fits = bb.size.Z <= 256 and (xy[1] <= 256 or (xy[1] + xy[0]) / _m.sqrt(2) <= 256)
    rep.append(f"{n}: {bb.size.X:.0f}×{bb.size.Y:.0f}×{bb.size.Z:.0f} มม. · ~{v * 1.24e-3 * 0.45:.0f} ก. (PLA infill ~45%) · {('พอดีเตียง X2D' if max(bb.size.X, bb.size.Y) <= 256 else 'พิมพ์แนวทแยงบนเตียง') if fits else '⚠️ เกินเตียง'}")
open(os.path.join(OUT, "kbot_wheel_foot_report.txt"), "w").write("\n".join(rep) + "\n"); print("\n".join(rep))

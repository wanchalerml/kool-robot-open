"""เท้าล้อ v1.1 ทรงแคบ + ซ็อกเก็ตเอียง (KOOL 24 พ.ย. 2569 23:xx · ต่อจาก wheel_foot_v1.py)

v1.1 ต่างจาก v1:
  - โจทย์: ขาทรง A แต่เอียงน้อยกว่า 9° → TILT = 4° (sim/kbot/wheel_foot_tilt.py: ทุกมุม 0–9° ผ่าน ≥18° → มุมเลือกตามหน้าตา)
  - ข้อเท้าเลื่อนออกตามมุม: y = 105 + 496·tan(4°) = 140 · กลไกเท้าทั้งชุดเลื่อนตาม (DY) · ล้อขับ ±253
  - แบตย้ายเข้าต้นขาแล้ว → ตัดแบตออกจากแผ่นบน · แผ่นบนแคบลง (ขอบใน = ครึ่งหน้าแปลนซ็อกเก็ต)
  - ซ็อกเก็ต: หน้าแปลนเรียบกับแผ่นบน · กระบอกรับท่อเอียง TILT เข้าหาลำตัว

เดิม (v1): เท้าล้อ หุ่นโชว์ v1 (KOOL 24 พ.ย. 2569) — แผ่นอะลูมิเนียมตัด DXF + ชิ้นซื้อ · เท้าขวา (เท้าซ้าย = กลับด้าน)

แกน: x = หน้า · y = ออกนอกตัว (0 = กลางตัวหุ่น) · z = ขึ้น · พื้น z = 0 · หน่วย มม.

สเปก (24 พ.ย. 20:50 · ตามข้อ 10 ใน docs/show-v1):
  - ล้อขับ ZLTECH ZLLG50-ASM200 V1.0 เพลาเดี่ยว ⌀130 · ติดนอกเท้า · ศูนย์ล้อ y = ±220 (±22 ซม.)
  - ฐานล้อ 320 = เพลาล้อขับ (x +160) ถึงจุดแตะพื้นล้อหมุนตาม ⌀100 ตอนแย่สุด (ถอยหลัง) · แกนหมุนอยู่ x −198
    (ถ้าวัด 320 ถึงแกนหมุน ตอนถอยหลังจุดแตะพื้นขยับมาหน้า 38 → มุมล้มหลังเหลือ 14.8° ไม่ผ่าน ≥15°)
  - สปริงแม่พิมพ์ 2 ชุด/เท้า: เพลานำ ⌀10 บน SHF10 + ลูกปืนสไลด์ LMF10UU + สปริง ISO 10243 เขียว ⌀20×64 (19.6 N/มม.)
    → แผ่นบน (ขา+แบต) ขยับได้แค่ขึ้น-ลง · แผ่นล่าง (ล้อ+ล้อหมุนตาม) รับพื้น · ยาง PU 90A = ตัวหยุด
  - สลักล็อก: โซลินอยด์ 12V สปริงดัน ×2/เท้า (ไฟดับ/จอด = สลักเสียบ แข็งเหมือนไม่มีโช้ค · สั่งเดิน = ดึงออก)
  - หน้าแปลนถอดเร็ว: ซ็อกเก็ตงานกลึง (ยึดถาวรกับท่อขา ⌀25) หน้าแปลน 90×90 → แผ่นบน ด้วย M6 ×4 + หมุดนำ ⌀6 ×2
    + ปลั๊ก XT60 + GX16 6 ขา (ห้อยผ่านรูยาง) → ถอดเปลี่ยนชุดเท้าได้ ~10 นาที

แบบล้อ: docs/show-v1/ref/zllg50asm200_v1_drawing.png (ร้าน aifitlab · ZLLG50ASM200_V1.0-Drawing.pdf)
ชิ้นที่ขนาด "ประมาณ" ต้องเทียบของจริงก่อนส่งตัด → ดูหัวข้อ VERIFY ในรายงาน

ใช้: python3 cad/show_v1/wheel_foot_v1_1.py
ออก: cad/out/show_v1_1_wheel_foot.{step,3mf} + _iso/_top/_front/_preview.png
     cad/out/show_v1_1_wheel_foot_{lower,upper}_{R,L}.dxf + _dropout.dxf (ตัดเลเซอร์/CNC)
     cad/out/show_v1_1_wheel_foot_socket.step (งานกลึง) · show_v1_1_wheel_foot_report.txt
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from build123d import *  # noqa: E402
from tools.export import OUT_DIR, export_part  # noqa: E402

# ------------------------------------------------------------------ ตำแหน่งหลัก
TILT = float(os.environ.get("TILT", "4.0"))   # องศา · ขาทรง A (บนเอียงเข้าลำตัว)
HIP_Y, HIP_Z, ANK_Z = 105.0, 705.0, 209.0      # sim/kbot/frame_fit.py (จุดข้อต่อภาพ Gemini รอบ 3)
ANK_Y = HIP_Y + (HIP_Z - ANK_Z) * math.tan(math.radians(TILT))
DY = ANK_Y - 107.0                              # เลื่อนกลไกเท้าทั้งชุดจากตำแหน่ง v1 (ข้อเท้า 107)
TRACK = 220.0 + DY       # ศูนย์กลางหน้ายางล้อขับ (y) · v1 = 220
WB = 320.0               # ฐานล้อขั้นต่ำ = เพลาล้อขับ ↔ จุดแตะพื้นล้อหมุนตาม "แย่สุด" (ตอนถอยหลัง ล้อหมุนตามหันมาหน้า)
CAST_TRAIL = 38.0        # ระยะเยื้องแกนหมุนล้อหมุนตาม ⌀100 (ประมาณ)
AX_X = 160.0
CAST_X = AX_X - WB - CAST_TRAIL   # แกนหมุน −198 → จุดแตะพื้น −160 (ถอย) ถึง −236 (เดินหน้า)
CAST_Y = 160.0 + DY           # ล้อหมุนตามอยู่ใต้แผ่นล่าง (ยื่นนอกได้น้อยกว่าล้อขับเพราะต้องอยู่ใต้แผ่น)
LEG = (0.0, ANK_Y)       # หัวซ็อกเก็ต (x, y)

# ------------------------------------------------------------------ ล้อขับ ZLLG50-ASM200 V1.0 (จากแบบผู้ผลิต)
HUB_D = 130.0            # ⌀130 ±2
TIRE_W = 38.0            # หน้ายาง 38 ±1
HUB_BODY = 64.0          # 94.5 − 30.5 (ตัวดุม รวมฝานอก 13.6)
HUB_CAP = 13.6           # ฝานอกยื่นจากขอบยาง
SHAFT_L = 30.5           # เพลายื่นจากหน้าดุม
SHOULDER = 2.5           # บ่าเพลา
SHAFT_FLAT = 10.0        # ด้านแบนเพลา 10 (0/−0.1) · เกลียว M14×1.5
AX_Z = HUB_D / 2         # เพลาสูงจากพื้น = รัศมียาง
# ระยะจากศูนย์ยางถึงหน้าดุมด้านเพลา = 64 − (13.6 + 19) = 31.4
HUB_FACE_Y = TRACK - (HUB_BODY - HUB_CAP - TIRE_W / 2)    # หน้าดุมด้านเพลา (ด้านใน)
DROP_T = 8.0             # แผ่นหางปลา (dropout) อะลูมิเนียม 8 มม.
DROP_Y1 = HUB_FACE_Y - SHOULDER                              # ผิวนอกแผ่น (ชนบ่าเพลา)
DROP_Y0 = DROP_Y1 - DROP_T

# ------------------------------------------------------------------ ล้อหมุนตาม (⌀100 มีล็อก · ขนาดประมาณ → วัดของจริง)
CAST_H = 128.0           # ความสูงติดตั้ง (พื้น → ใต้แผ่นยึด)
CAST_WD = 100.0
CAST_OFF = CAST_TRAIL
CAST_PLATE = (100.0, 85.0)
CAST_HOLES = (80.0, 60.0)

# ------------------------------------------------------------------ แผ่น
LP_T, UP_T = 5.0, 6.0    # แผ่นล่าง 5 มม. · แผ่นบน 6 มม. (รับโมเมนต์จากขาที่อยู่ด้านใน)
LP_Z = CAST_H            # ใต้แผ่นล่าง = หน้ายึดล้อหมุนตาม
SHF_H = 10.0             # ฐานยึดเพลา SHF10 (สูงหน้าแปลน ~10 · ประมาณ)
SPRING_D, SPRING_L0, SPRING_K = 20.0, 64.0, 19.6   # ISO 10243 เขียว ⌀20 (รู ⌀10) ยาว 64 · N/มม.
SPRING_PRE = 1.0         # อัดล่วงหน้าด้วยปลอกล็อกเพลา (ยกหุ่นขึ้น ปลอกยังนั่งบนลูกปืน)
SPRING_SAG = 3.0         # ยุบตอนยืนนิ่งจากท่ายืดสุด (หุ่น 25–30 กก. ≈ 2.9–3.1 มม. · เช็กในรายงาน)
BUMP_TRAVEL = 9.0        # ยุบเพิ่มจากท่านิ่งจนชนยาง PU (รวมใช้งาน 12 มม. ตามข้อ 10)
GAP_STATIC = SPRING_L0 - SPRING_PRE - SPRING_SAG           # ระยะสปริงตอนนิ่ง
UP_Z = LP_Z + LP_T + SHF_H + GAP_STATIC                    # ใต้แผ่นบน (ท่านิ่ง)
POSTS = [(150.0, 112.0 + DY), (-165.0, 80.0 + DY)]                  # เพลานำ 2 ชุด: หน้า = แนวเพลาล้อขับ · หลัง = แนวล้อหมุนตาม
LMF = dict(D=19.0, L=29.0, FD=40.0, FT=6.0, PCD=29.0, H=4.5)   # LMF10UU
SHF = dict(FD=43.0, PCD=32.0, H=5.5)                           # SHF10 (ประมาณ)
BUMPER = (-20.0, 150.0 + DY)  # ยางกันกระแทก M6 (ชนเมื่อสปริงยุบเพิ่ม BUMP_TRAVEL)
LOCKS = (60.0, -110.0)   # โซลินอยด์ล็อก 2 ตัว (x) ที่ขอบนอก · สลักแนวแกน y
LOCK_TAB_Y = 196.0 + DY       # ผิวในของขาตั้งฉากล่าง (ฉาก 50×50×4)
SOL = (30.0, 20.0, 20.0) # ตัวโซลินอยด์ (x, y, z) ประมาณ · สลัก ⌀6 ช่วงชัก 10
BATT = dict(x0=-210.0, x1=-35.0, y0=118.0, y1=193.0, h=95.0)   # LiFePO4 24V 10Ah (ประมาณ 175×75×95)

# ------------------------------------------------------------------ ซ็อกเก็ตขา (งานกลึง 6061)
TUBE_D = 25.0
SOCK = dict(F=90.0, FT=8.0, BD=40.0, BH=60.0, BORE=25.2, BOLT_SQ=70.0, BOLT=6.6, DOWEL=6.0,
            PIN_Z=40.0, PIN_D=6.6)   # PIN = น็อต M6 ทะลุยึดท่อถาวร
GROMMET = (65.0, 112.0 + DY)   # รูยางร้อยปลั๊ก XT60 + GX16 บนแผ่นบน

ALU = 2.70e-6  # กก./มม.³


def poly(pts):
    with BuildSketch() as s:
        Polygon(*pts, align=None)
    return s.sketch


def holes(sk, pts_d):
    for (x, y), d in pts_d:
        sk = sk - Pos(x, y) * Circle(d / 2)
    return sk


def pcd(cx, cy, r, n, d, a0=45.0):
    return [((cx + r * math.cos(math.radians(a0 + 360 * k / n)), cy + r * math.sin(math.radians(a0 + 360 * k / n))), d)
            for k in range(n)]


# ---------------------------------------------------------------- แผ่นล่าง (5 มม.)
LP_OUT = [(-250, ANK_Y - 50), (212, ANK_Y - 50), (212, DROP_Y0 - 2), (100, DROP_Y0 - 2), (100, 210 + DY), (-250, 210 + DY)]
ANGLES_X = (118.0, 200.0)        # ฉาก 40×40×4 ยาว 30 ยึดแผ่นหางปลา (ศูนย์กลาง x)
ANG_IN = 40.0                    # ขาแนวนอนของฉาก (ยื่นเข้าใน)


def lower_sketch():
    sk = poly(LP_OUT)
    h = []
    for px, py in POSTS:                                  # SHF10 4×M5 (SHF จับเพลาด้วยสกรูของมันเอง)
        h += pcd(px, py, SHF["PCD"] / 2, 4, SHF["H"])
    cx0, cy0 = CAST_X, CAST_Y                             # ล้อหมุนตาม 4×M8
    h += [((cx0 + sx * CAST_HOLES[0] / 2, cy0 + sy * CAST_HOLES[1] / 2), 8.6) for sx in (-1, 1) for sy in (-1, 1)]
    for ax in ANGLES_X:                                   # ฉากยึด dropout: 2×M5 ต่อฉาก
        h += [((ax - 8, DROP_Y0 - 22), 5.5), ((ax + 8, DROP_Y0 - 22), 5.5)]
    for lx in LOCKS:                                      # ฉากรับสลัก 50×50×4: 2×M5
        h += [((lx - 12, LOCK_TAB_Y - 25), 5.5), ((lx + 12, LOCK_TAB_Y - 25), 5.5)]
    h += [(BUMPER, 6.6), ((90.0, 150.0 + DY), 22.0)]           # ยาง PU · รูร้อยสายล้อ
    return holes(sk, h)


# ---------------------------------------------------------------- แผ่นบน (6 มม.)
UP_OUT = [(-195, ANK_Y - 46), (175, ANK_Y - 46), (175, 205 + DY), (-195, 205 + DY)]   # v1.1: ไม่มีแบต → สั้นลง/ขอบในชิดหน้าแปลน


def upper_sketch():
    sk = poly(UP_OUT)
    lx, ly = LEG
    b = SOCK["BOLT_SQ"] / 2
    h = [((lx + sx * b, ly + sy * b), SOCK["BOLT"]) for sx in (-1, 1) for sy in (-1, 1)]   # 4×M6
    h += [((lx, ly + b), SOCK["DOWEL"]), ((lx, ly - b), SOCK["DOWEL"])]                     # หมุดนำ ⌀6 (รีมเมอร์)
    for px, py in POSTS:                                  # LMF10UU: รูเพลา + 4×M4
        h += [((px, py), 12.0)] + pcd(px, py, LMF["PCD"] / 2, 4, LMF["H"])
    for lx2 in LOCKS:                                     # ฉากแขวนโซลินอยด์ 40×40×4: 2×M5
        h += [((lx2 - 12, LOCK_TAB_Y - 25), 5.5), ((lx2 + 12, LOCK_TAB_Y - 25), 5.5)]
    h += [(GROMMET, 22.0)]
    return holes(sk, h)


# ---------------------------------------------------------------- แผ่นหางปลา (8 มม. · ระนาบ x-z)
DROP_Z0, DROP_Z1 = 35.0, LP_Z + LP_T + 40.0


def dropout_sketch():
    """ร่างในระนาบ (x, z) · ร่องเปิดล่าง กว้าง 10.2 รับด้านแบนเพลา (กันหมุน) · ปลายร่อง = ศูนย์เพลา"""
    sk = poly([(100, DROP_Z0), (218, DROP_Z0), (218, DROP_Z1), (100, DROP_Z1)])
    slot = poly([(AX_X - 5.1, DROP_Z0 - 1), (AX_X + 5.1, DROP_Z0 - 1), (AX_X + 5.1, AX_Z), (AX_X - 5.1, AX_Z)])
    sk = sk - slot - Pos(AX_X, AX_Z) * Circle(5.1)
    h = []
    for ax in ANGLES_X:
        h += [((ax - 8, LP_Z + LP_T + 22), 5.5), ((ax + 8, LP_Z + LP_T + 22), 5.5)]
    return holes(sk, h)


def plate3d(sk, z0, t):
    return Pos(0, 0, z0) * extrude(sk, amount=t)


def dropout3d():
    s = extrude(dropout_sketch(), amount=DROP_T)       # ร่างอยู่ใน XY → หมุนให้ y ของร่าง = z
    return Pos(0, DROP_Y1, 0) * Rot(90, 0, 0) * s       # Rot X+90: z_sketch→ −y · y_sketch→ z


C = (Align.CENTER, Align.CENTER, Align.MIN)


def cyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h, align=C)


def box(x, y, z, sx, sy, sz):
    return Pos(x, y, z) * Box(sx, sy, sz, align=C)


# ---------------------------------------------------------------- ชิ้นซื้อ (แบบจำลองไว้เช็กชน)
def hub():
    tire = Pos(AX_X, TRACK, AX_Z) * Rot(90, 0, 0) * Cylinder(HUB_D / 2, TIRE_W)
    body = Pos(AX_X, HUB_FACE_Y + HUB_BODY / 2, AX_Z) * Rot(90, 0, 0) * Cylinder(HUB_D / 2 - 14, HUB_BODY)
    sh = Pos(AX_X, HUB_FACE_Y - SHAFT_L / 2, AX_Z) * Rot(90, 0, 0) * Cylinder(7.0, SHAFT_L)
    return tire + body + sh


def caster_sweep():
    """ปริมาตรที่ล้อหมุนตามกวาดเมื่อหมุนรอบตัว (เช็กชน) + แผ่นยึด"""
    r = CAST_OFF + CAST_WD / 2 + 3
    return cyl(CAST_X, CAST_Y, 0, r, CAST_H - 15) + box(CAST_X, CAST_Y, CAST_H - 15, *CAST_PLATE, 15)


def guides():
    out = []
    z_lp = LP_Z + LP_T
    for px, py in POSTS:
        out += [cyl(px, py, z_lp, SHF["FD"] / 2, SHF_H),
                cyl(px, py, z_lp + SHF_H, SPRING_D / 2, GAP_STATIC) - cyl(px, py, z_lp + SHF_H, 5.2, GAP_STATIC),
                cyl(px, py, UP_Z + UP_T, LMF["FD"] / 2, LMF["FT"]) + cyl(px, py, UP_Z + UP_T, LMF["D"] / 2, LMF["L"])]
        top = UP_Z + UP_T + LMF["L"] + SPRING_SAG
        out += [cyl(px, py, z_lp, 5.0, top - z_lp + 10), cyl(px, py, top, 11.0, 10)]
    return out


def bumper():
    h = UP_Z - BUMP_TRAVEL - (LP_Z + LP_T)
    return cyl(*BUMPER, LP_Z + LP_T, 12.5, h), h


def locks():
    """ต่อจุด: ฉากล่าง 50×50×4 (ขาตั้งขึ้นที่ผิวนอก) · ฉากบน 40×40×4 ห้อยลง + โซลินอยด์ด้านใน · สลัก ⌀6 แนว +y"""
    lo, up, sol, pins = [], [], [], []
    z_lp = LP_Z + LP_T
    pin_z = UP_Z - 30.0
    for lx in LOCKS:
        hole = Pos(lx, LOCK_TAB_Y + 2, pin_z) * Rot(90, 0, 0) * Cylinder(4.0, 30)
        lo.append(box(lx, LOCK_TAB_Y - 25 + 2, z_lp, 40, 50, 4) + box(lx, LOCK_TAB_Y + 2, z_lp, 40, 4, 50) - hole)
        uy = LOCK_TAB_Y - 6          # ผิวนอกฉากบนห่างขาฉากล่าง 2 มม.
        up.append(box(lx, uy - 20, UP_Z - 4, 40, 40, 4) + box(lx, uy - 2, UP_Z - 40, 40, 4, 40) - hole)
        sol.append(box(lx, uy - 4 - SOL[1] / 2, pin_z - SOL[2] / 2, *SOL))
        pins.append(Pos(lx, LOCK_TAB_Y - 2, pin_z) * Rot(90, 0, 0) * Cylinder(3.0, 16))
    return lo, up, sol, pins, pin_z


def socket():
    s = SOCK
    f = box(0, 0, 0, s["F"], s["F"], s["FT"])
    tilt = Rot(TILT, 0, 0)                       # +X หมุน: ปลายบนเอนไป −y (เข้าลำตัว · เท้าขวา)
    b = tilt * cyl(0, 0, 0, s["BD"] / 2, s["BH"] + 2)
    part = f + b - tilt * cyl(0, 0, 3, s["BORE"] / 2, s["BH"] + 5)
    part -= box(0, 0, -20, 120, 120, 20)          # ตัดส่วนกระบอกที่โผล่ใต้หน้าแปลน
    q = s["BOLT_SQ"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            part -= cyl(sx * q, sy * q, -1, s["BOLT"] / 2, 20)
    for sy in (-1, 1):
        part -= cyl(0, sy * q, -1, s["DOWEL"] / 2, 20)
    part -= tilt * (Pos(0, 0, s["PIN_Z"]) * Rot(0, 90, 0) * Cylinder(s["PIN_D"] / 2, 60))
    return part


# ---------------------------------------------------------------- ประกอบ
LP = plate3d(lower_sketch(), LP_Z, LP_T)
UP = plate3d(upper_sketch(), UP_Z, UP_T)
DROP = dropout3d()
ANG = [box(ax, DROP_Y0 - ANG_IN / 2, LP_Z + LP_T, 30, ANG_IN, 4) + box(ax, DROP_Y0 - 2, LP_Z + LP_T, 30, 4, 40) for ax in ANGLES_X]
HUB = hub()
CAST = caster_sweep()
BUMP, BUMP_H = bumper()
LOCK_LO, LOCK_UP, SOLS, PINS, PIN_Z = locks()
SOCKET = Pos(*LEG, UP_Z + UP_T) * socket()
TUBE = Pos(*LEG, UP_Z + UP_T) * Rot(TILT, 0, 0) * cyl(0, 0, 3, TUBE_D / 2, 200)
BATTERY = box((BATT["x0"] + BATT["x1"]) / 2, (BATT["y0"] + BATT["y1"]) / 2, UP_Z + UP_T,
              BATT["x1"] - BATT["x0"], BATT["y1"] - BATT["y0"], BATT["h"])
GUIDES = guides()

SPRUNG = {"แผ่นบน": UP, "ซ็อกเก็ตขา": SOCKET,
          **{f"ฉากโซลินอยด์ {i+1}": u for i, u in enumerate(LOCK_UP)}, **{f"โซลินอยด์ {i+1}": s for i, s in enumerate(SOLS)}}
FIXED = {"แผ่นล่าง": LP, "แผ่นหางปลา": DROP, "ล้อขับ": HUB, "ล้อหมุนตาม(กวาด)": CAST, "ยาง PU": BUMP,
         **{f"ฉากรับสลัก {i+1}": l for i, l in enumerate(LOCK_LO)}, **{f"ฉาก dropout {i+1}": a for i, a in enumerate(ANG)},
         **{f"SHF10 {i+1}": GUIDES[5 * i] for i in range(len(POSTS))}}


def vol_hit(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def checks():
    """เช็กชน: ชิ้นที่ขยับ (แผ่นบน) กับชิ้นอยู่กับที่ ทั้งท่านิ่งและยุบสุด + ชิ้นอยู่กับที่ด้วยกัน"""
    rep, ok = [], True
    for dz, tag in ((0.0, "ท่านิ่ง"), (-BUMP_TRAVEL, "ยุบสุด"), (SPRING_SAG - SPRING_PRE, "ยกหุ่นขึ้น (ยืดสุด)")):
        for k, v in SPRUNG.items():
            mv = Pos(0, 0, dz) * v
            for k2, v2 in FIXED.items():
                if k2 == "ยาง PU" and k == "แผ่นบน" and dz == -BUMP_TRAVEL:
                    continue                       # ยุบสุด = แตะยางพอดี (ตั้งใจ)
                hv = vol_hit(mv, v2)
                if hv > 1.0:
                    ok = False
                    rep.append(f"  ❌ {tag}: {k} ชน {k2} ({hv:.0f} มม.³)")
    fx = list(FIXED.items())
    for i, (k, v) in enumerate(fx):
        for k2, v2 in fx[i + 1:]:
            if {k, k2} & {"แผ่นล่าง"} and ({k, k2} - {"แผ่นล่าง"}).pop().startswith(("ฉาก", "ยาง", "SHF", "ล้อหมุนตาม")):
                continue                           # ชิ้นที่ขันบนแผ่นล่าง = แตะผิว
            if {k, k2} == {"แผ่นหางปลา", "ล้อขับ"}:
                continue                           # เพลาล้อร้อยร่องหางปลา (ตั้งใจ)
            if "แผ่นหางปลา" in (k, k2) and ("ฉาก dropout" in k or "ฉาก dropout" in k2):
                continue
            hv = vol_hit(v, v2)
            if hv > 1.0:
                ok = False
                rep.append(f"  ❌ {k} ชน {k2} ({hv:.0f} มม.³)")
    rep.insert(0, "เช็กชน: " + ("✅ ไม่ชน (ท่านิ่ง · ยุบสุด · ยืดสุด · ล้อหมุนตามหมุนรอบตัว)" if ok else "⚠️ มีจุดชน"))
    return rep, ok


def mass_report():
    m_plates = (LP.volume + UP.volume + DROP.volume + sum(a.volume for a in ANG + LOCK_LO + LOCK_UP)) * ALU
    sprung_extra = SOCKET.volume * ALU
    parts = [("แผ่นล่าง+แผ่นบน+หางปลา+ฉาก (อะลูมิเนียม)", m_plates), ("ซ็อกเก็ตขา (6061)", sprung_extra),
             ("ล้อ ZLLG50 เพลาเดี่ยว (ผู้ผลิต)", 1.95), ("ล้อหมุนตาม ⌀100 มีล็อก (ประมาณ)", 0.65),
             ("เพลานำ+LMF10UU+SHF10+สปริง+ปลอก ×2 (ประมาณ)", 0.55), ("โซลินอยด์ ×2 + สลัก/น็อต/ยาง (ประมาณ)", 0.45)]
    unsprung = (LP.volume + DROP.volume + sum(a.volume for a in ANG + LOCK_LO)) * ALU + 1.95 + 0.65 + 0.3
    return parts, sum(p[1] for p in parts), unsprung


def tip_report(z_com, tilt_side, tilt_fa):
    rows = []
    for trail, tag in ((-CAST_OFF, "เดินหน้า"), (CAST_OFF, "ถอยหลัง (ล้อหมุนตามหันหน้า)")):
        fx, fy = AX_X, TRACK
        cx, cy = CAST_X + trail, CAST_Y
        dx, dy = cx - fx, cy - fy
        d_side = abs(dx * fy - dy * fx) / math.hypot(dx, dy) / 1000
        a_side = math.degrees(math.atan(d_side / z_com))
        a_f = math.degrees(math.atan(fx / 1000 / z_com))
        a_b = math.degrees(math.atan(-cx / 1000 / z_com))
        rows.append(f"  {tag}: ล้มข้าง {a_side:.1f}° (ยุบสุด {a_side - tilt_side:.1f}°) · ล้มหน้า {a_f:.1f}° (ยุบสุด {a_f - tilt_fa:.1f}°) · "
                    f"ล้มหลัง {a_b:.1f}° (ยุบสุด {a_b - tilt_fa:.1f}°)")
    return rows


def write_dxf():
    files = []
    sk = {"lower": lower_sketch(), "upper": upper_sketch(), "dropout": dropout_sketch()}
    for name, s in sk.items():
        for side in (("",) if name == "dropout" else ("_R", "_L")):   # หางปลาสมมาตร ใช้ไฟล์เดียว ตัด 2 ชิ้น
            shape = s if side != "_L" else s.mirror(Plane.XZ)
            d = ExportDXF(unit=Unit.MM)
            d.add_layer("CUT")
            d.add_shape(shape, layer="CUT")
            p = OUT_DIR / f"show_v1_1_wheel_foot_{name}{side}.dxf"
            d.write(str(p))
            files.append(p.name)
    return files


if __name__ == "__main__":
    parts, m, unsprung = mass_report()
    body = [(1.2, 1.30), (4.0, 1.00), (3.2, 0.95), (1.5, 0.72), (2.8, 0.55), (2.0, 0.25)]   # sim/kbot/show_v1_tip.py
    batt_z = 0.45                                   # v1.1: แบตครึ่งล่างต้นขา (gemini-match)
    foot_nb = m
    allm = body + [(4.8, batt_z), (2 * (foot_nb - unsprung), (UP_Z + 40) / 1000), (2 * unsprung, 0.09)]
    M = sum(a for a, _ in allm)
    Z = sum(a * b for a, b in allm) / M
    f_spring = (M - 2 * unsprung) * 9.81 / 4
    comp = f_spring / SPRING_K
    gap_post = POSTS[0][0] - POSTS[1][0]
    tilt_fa = math.degrees(math.atan((BUMP_TRAVEL + SPRING_SAG) / gap_post))        # หน้ายุบสุด หลังยืดสุด
    tilt_side = math.degrees(math.atan((BUMP_TRAVEL + SPRING_SAG) / (2 * 100.0)))   # เท้าหนึ่งยุบสุด อีกเท้ายืด (สปริงห่าง ~±100)
    rep = [f"เท้าล้อ v1.1 · ขาเอียง {TILT:.1f}° · ข้อเท้า y {ANK_Y:.0f} · กว้างนอก-นอก {2*(TRACK+TIRE_W/2):.0f} (เท้าขวา · y+ = ออกนอก) · ศูนย์ล้อ ±{TRACK:.0f} · ฐานล้อ (ถึงจุดแตะพื้นแย่สุด) {WB:.0f} · เพลาล้อขับ↔แกนหมุนล้อหมุนตาม {AX_X-CAST_X:.0f} · เพลาสูง {AX_Z:.0f}",
           f"แผ่นล่าง z {LP_Z:.0f}–{LP_Z+LP_T:.0f} · แผ่นบน (ท่านิ่ง) z {UP_Z:.0f}–{UP_Z+UP_T:.0f} · ยุบได้ {BUMP_TRAVEL:.0f} จากท่านิ่ง (ยาง PU สูง {BUMP_H:.0f}) · ยืดได้ {SPRING_SAG - SPRING_PRE:.0f}",
           f"สปริง ⌀{SPRING_D:.0f}×{SPRING_L0:.0f} k={SPRING_K}: แรง/ตัวตอนยืน {f_spring:.0f} N → อัด {comp:.1f} มม. (ออกแบบ {SPRING_PRE+SPRING_SAG:.0f}) · "
           f"ยุบสุด {SPRING_PRE+SPRING_SAG+BUMP_TRAVEL:.0f} มม. = {(SPRING_PRE+SPRING_SAG+BUMP_TRAVEL)/SPRING_L0*100:.0f}% ของความยาว",
           f"แผ่นหางปลา y {DROP_Y0:.1f}–{DROP_Y1:.1f} (ชนบ่าเพลา) · เพลาเหลือหลังแผ่น {SHAFT_L - DROP_T:.1f} มม. (น็อต M14×1.5 + แหวนกันหมุน)",
           f"สลักโซลินอยด์ ⌀6 ที่ z {PIN_Z:.0f} (ท่านิ่ง) ×{len(LOCKS)} · หน้าแปลนขา 90×90: M6 ×4 (สี่เหลี่ยม 70) + หมุด ⌀6 ×2 · รูท่อ ⌀{SOCK['BORE']} ลึก {SOCK['BH']-3:.0f}"]
    c, ok = checks()
    rep += c
    rep.append("น้ำหนักต่อเท้า:")
    rep += [f"  {n}: {w:.2f} กก." for n, w in parts]
    rep.append(f"  รวม ~{m:.1f} กก./เท้า (ใต้สปริง {unsprung:.1f}) · ไม่รวมแบต (อยู่ต้นขา)")
    rep.append(f"ทั้งตัว ~{M:.1f} กก. · จุดศูนย์ถ่วง ~{Z:.2f} ม. (แบตในต้นขา ศูนย์แบตสูง {batt_z:.2f} ม.)")
    rep.append(f"มุมล้ม (ยุบสุด = เอียงเพิ่ม ข้าง {tilt_side:.1f}° · หน้า-หลัง {tilt_fa:.1f}°):")
    rep += tip_report(Z, tilt_side, tilt_fa)
    rep += ["VERIFY ก่อนส่งตัด (วัดของจริง/ดูหน้าร้าน):",
            "  1) ล้อหมุนตาม ⌀100: สูงติดตั้ง 128 · ลายรู 80×60 M8 · เยื้อง 38 (ต่างจากนี้ → แก้ CAST_* แล้วรันใหม่)",
            "  2) SHF10: หน้าแปลน ⌀43 · PCD 32 · รู 5.5 · สูง 10 (ยี่ห้อต่างกันได้)",
            "  3) LMF10UU: หน้าแปลน ⌀40 PCD 29 รู 4.5",
            "  4) โซลินอยด์ล็อก 12V: ตัว ≤30×20×20 · สลัก ⌀6 ชัก ≥8 (ร่างเผื่อที่ไว้ ต้องได้รุ่นจริงก่อนเจาะฉาก)",
            "  5) ซ็อกเก็ตเอียง: งานกลึง 5 แกน หรือกลึงกระบอกแยกแล้วเชื่อม TIG กับหน้าแปลนตามจิ๊กมุม (ถูกกว่า)",
            "  6) รูสลักในฉากรับสลัก: เจาะตอนประกอบ หลังวางน้ำหนักเต็ม (ระดับยืนจริงขึ้นกับสปริงจริง)",
            "  7) ท่อขา 6061-T6 · หมุดนำ ⌀6 → รูแผ่นบนต้องรีมเมอร์ ⌀6 H7 (ตัดเลเซอร์แล้วรีม)"]
    files = export_part("show_v1_1_wheel_foot", {
        "lower": LP + DROP + ANG[0] + ANG[1] + sum(LOCK_LO[1:], LOCK_LO[0]) + BUMP,
        "upper": UP + SOCKET + sum(LOCK_UP[1:], LOCK_UP[0]),
        "wheel": HUB + CAST, "guides": Compound(children=GUIDES + SOLS + PINS + [TUBE])})
    export_step(SOCKET, str(OUT_DIR / "show_v1_1_wheel_foot_socket.step"))
    rep.append("ไฟล์: " + ", ".join(write_dxf() + ["show_v1_1_wheel_foot.step/.3mf", "show_v1_1_wheel_foot_socket.step", "_preview.png"]))
    txt = "\n".join(rep) + "\n"
    (OUT_DIR / "show_v1_1_wheel_foot_report.txt").write_text(txt)
    print(txt)

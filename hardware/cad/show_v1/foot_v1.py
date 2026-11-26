"""เท้า V1 รอบ 2 ตามภาพต้นแบบ final_render_v1.jpg (KOOL 26 พ.ย. 2569 · "ก. ขับ 4 ล้อ ล้อ 4.5\"" 21:53 · "มีสปริงรองรับทางขรุขระ เผื่องาน outdoor" 21:46)

แนวคิด (ข้างขวา · พิกัดหุ่น x หน้า y ซ้าย z ขึ้น · โลคัลเท้า: เพลาข้อเท้า (0,0,0) · +y = ฝั่งใน (เข้าหากลางตัว) · −y = ฝั่งนอก)
  - ล้อขับ ZLTECH ZLLG45-ASM200 เพลาคู่ ×2/เท้า (ยางลาย ⌀128 · กว้าง 51 · เพลา M14×1.5 แบน 12 · 3.0 กก. · สายออกปลายเพลาฝั่งใน)
  - คานทรงกระดูก ×2 ประกบนอกล้อ บนเพลาข้อเท้า ⌀12 (แบริ่ง 6901 ×2) · 27 พ.ย. รอบ 3: ล็อกด้วยหมุด TPU อัดแน่น (ยืดหยุ่น ~±2°)
    เพราะคานหมุนอิสระ ±10° (รอบ 2) = ตัวหุ่นไม่มีแรงคืนแนวก้ม-เงย → โยกเองจนชนตัวหยุด (เรื่องโยกตอนออกตัว/เบรก 00:12)
    · ROCKER=pahtcf (ค่าเริ่มต้น · 27 พ.ย. 00:43) · petgcf (เดิม 26 พ.ย. 22:40): พิมพ์ PETG-CF หนา 15 นอนราบ + ปลอก Al ⌀28/24 ใส่แบริ่ง
      + แผ่นรองเพลาเหล็ก 3 มม. รูปตัว D ในหลุมลึก 8 ที่เพลาล้อ (กันหมุน + กระจายแรงน็อต M14) · ฝาครอบเป็นเนื้อเดียวกับคาน
    · ROCKER=al (ทางสำรองถ้าทดสอบ PETG-CF ไม่ผ่าน): แผ่น Al 6061 หนา 6 ตัดเลเซอร์ (DXF) + ฝาครอบพิมพ์แยก
    · หยุดกระดก = หมุด M5 + ปลอก TPU ⌀9 จากบล็อกข้อเท้า วิ่งในร่องโค้งของแผ่น
  - ข้อเท้ายุบ 18 มม.: บล็อกข้อเท้าเลื่อนบนแกน ⌀10 ×2 (LM10LUU ×2) · รอบ 3: สปริงแม่พิมพ์ ISO 10243 ⌀20×64 อัดค้าง > น้ำหนักยืน
    → ปกติแข็ง (ไม่โยกซ้าย-ขวา) · ยุบเฉพาะตอนชนขอบ/ทางขรุขระ (รอบ 2 สปริง 3.5 N/มม. อัดค้างน้อยกว่าน้ำหนัก = แรงคืนเอียงข้าง ≈ แรงล้ม)
  - ★ ToF VL53L1X ที่ปลายคานนอก หน้า/หลัง (27 พ.ย. · กันชนล้อตัดออกตาม 00:30)
    · ยุบสุด = เสากันยุบกลาง + หัว TPU · ยืดสุด = น็อต M6 กลาง (หัวอยู่ในท่อขา)
  - ★ ปุ่มข้อเท้าเทา (ตามภาพ) = ดรัม ⌀96 แกนตามขวาง ผ่าหน้า-หลัง ยึดบล็อก (ยุบตามบล็อก) + ฝาปุ่ม ⌀72 ×2 ปลายเพลา
  - ★ ยางย่น TPU (bellows) ระหว่างดรัมกับซ็อกเก็ต ปิดสปริง/แกน · ซ็อกเก็ตอยู่ในปลอกหน้าแข้ง (ทำตอนจัด V1 ข้อ 2)
  - ★ ฝาครอบคานทรงกระดูก (พิมพ์ · M3 ×4/แผ่น) · ฝั่งนอกมีฝาปลายเพลาโค้ง · ฝั่งในมีรางสาย (ข้องอสาย r 16) ไปถึงบนคาน
  - ตัวขับ ZLAC8015D ไม่อยู่ในเท้า (150×97×31 ใหญ่เกินทรงเท้าในภาพ) → ไปอยู่ในท้อง ดู zlac_mount_v1.py
ความแข็งแรง (22:11): ดู strength_report() / _report.txt\nใช้: python3 cad/show_v1/foot_v1.py → cad/out/show_v1_foot1_*.stl/.dxf + _report.txt + _preview.png
⚠️ MEASURE: เส้นผ่าน/รัศมีงอสายมอเตอร์ · ระยะยื่นเพลาจริง (แบบ: ฝั่งไม่มีสาย 17.2–22 · ฝั่งสาย 25–25.5) · สปริงที่ซื้อจริง
"""
import math
import os

import numpy as np
import trimesh
from manifold3d import Manifold, Mesh
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")

# ---------------- ล้อ ZLLG45-ASM200 (แบบผู้ผลิต · ยางลาย) ----------------
WD, TIRE_W, BODY_W = 128.0, 51.0, 89.0          # BODY_W ≈ 137 − 22 − 25.5 (ช่วงตัวดุมระหว่างโคนเพลา)
SHAFT_L_LAT, SHAFT_L_MED = 22.0, 25.5            # เพลายื่น: ฝั่งนอก (ไม่มีสาย) / ฝั่งใน (สายออก)
SHAFT_FLAT, SHAFT_M = 12.0, 14.0
NUT_R = 12.7                                     # น็อต M14 บาง AF22 (มุม)
CABLE_D, CABLE_BEND_R = 8.0, 16.0               # MEASURE
# ---------------- ตำแหน่ง ----------------
FOOT_Y = -102.0                                 # กลางเท้าขวา (จาก AI · ขาตรง)
AXLE_Z = WD / 2                                 # 64
HALF_WB = 100.0
FOOT_X = -22.0                                  # กลางเท้า x = แกนขาตรง V1 (v1_sdf.LEG_X · 27 พ.ย.: เดิม −30 = ข้อเท้า AI)
PIVOT_Z = AXLE_Z + 86.0                         # เพลาข้อเท้า z 150 (ภาพ ~130 · สูงขึ้นตามล้อ ⌀128)
DZ = AXLE_Z - PIVOT_Z                           # −86
ROCKER = os.environ.get("ROCKER", "pahtcf")     # pahtcf (27 พ.ย. 00:43: สั่งง่าย ถูกกว่า แข็งแรงใกล้กัน · ค่าเริ่มต้น) | ppacf | petgcf | al (สำรอง)
PETG = ROCKER in ("petgcf", "ppacf", "pahtcf")  # คานพิมพ์ (ชื่อตัวแปรเดิม = "พิมพ์")
PPA = ROCKER == "ppacf"
# วัสดุคานพิมพ์ (datasheet Bambu · ทิศ XY): ดัดออกแบบ MPa · หารรับค้างนาน · กดออกแบบ MPa · โมดูลัสดัด MPa (ชื้น/ร้อนแบบอนุรักษ์)
#   PAHT-CF (PA12+CF): ดัด 125 แห้ง / 115 ชื้น · E 4120–4230 / 3640 ชื้น · HDT 170 °C @1.8 MPa · Tg PA12 ~45 °C → ล้าตัวมากกว่า PPA → ÷4
#   PPA-CF: ดัด ~208 · HDT 227 °C → ÷3 · PETG-CF: ดัด 83 → ÷4
MATS = {"pahtcf": ("PAHT-CF", 90.0, 4, 30.0, 3000.0), "ppacf": ("PPA-CF", 150.0, 3, 40.0, 6000.0),
        "petgcf": ("PETG-CF", 70.0, 4, 25.0, 3000.0), "al": ("Al 6061", 276.0, 1, 0.0, 69000.0)}
MAT_NM, MAT_SIG, MAT_CREEP, MAT_COMP, MAT_E = MATS[ROCKER]
BLK_MAT = "PAHT-CF"                              # บล็อกข้อเท้า + ซ็อกเก็ตขา (27 พ.ย.: เลิกใช้ PPA-CF ทั้งตัว)
PLATE_T, PLATE_GAP = (15.0 if PETG else 6.0), 2.0
PLATE_IN = BODY_W / 2 + PLATE_GAP               # 46.5 ผิวในแผ่นคาน
PLATE_OUT = PLATE_IN + PLATE_T                  # 52.5
HUB_R = 34.0                                    # ดุมแผ่นคาน (ฝาปุ่มครอบ)
ROCK = 2.0                                      # 27 พ.ย.: ล็อกคานด้วยหมุด TPU อัดแน่น (ไม่มีช่องหลวม) → กระดกได้แค่ยางยุบ ~±2° (เดิม ±10° อิสระ = ตัวโยกหน้า-หลังเอง)
HEAVE = 18.0                                    # 27 พ.ย.: สปริงแม่พิมพ์อัดค้างเกินน้ำหนักยืน → ยุบเฉพาะตอนชนขอบ/ทางขรุขระ
# ดรัม/บล็อก
DRUM_R, DRUM_WALL = 48.0, 3.0
DRUM_HL = PLATE_IN - 0.5                        # ครึ่งยาวดรัม 46
BLK_HX, BLK_HY, BLK_Z0, BLK_Z1 = 30.0, DRUM_HL - DRUM_WALL, -26.0, 30.0
ROD_X, ROD_D = 17.0, 10.0
LM_D, LM_L = 19.0, 55.0                         # LM10LUU (ยาว = 2 ตัวในตัวเดียว · รับแรงด้านข้างได้ ~2 เท่า LM10UU)
PIN_R, PIN_SLEEVE = 22.0, 9.0                   # หมุดหยุดกระดก (ใต้เพลา · ร่อง r17–27 เว้นผนังจากปลอก ⌀28 = 3)
CAP_R, CAP_T = 36.0, 6.0
# ยางย่น + ซ็อกเก็ต
COL_RO, COL_RI = 34.0, 31.0                     # คอดรัม (ที่รัดยางย่น)
COL_TOP = 54.0
BELLOW_SOLID = 8.0
SPIG_Z0 = COL_TOP + HEAVE + BELLOW_SOLID        # 87 ก้นปากซ็อกเก็ต
SB = SPIG_Z0 + 8.0                              # 95 ใต้แผ่นซ็อกเก็ต
SOCK_T, SOCK_R = 20.0, 40.0
TUBE_D = 40.0
TUBE_COL_H = 50.0
TUBE_DEPTH = 44.0
STOP_Z = BLK_Z1 + HEAVE - 2.0                   # หัว TPU เสากันยุบ (แตะที่ยุบ 23)
SPRING_OD = 20.0                                # สปริงแม่พิมพ์ ISO 10243 ⌀20×64 สีเขียว (โหลดเบา · ~19.6 N/มม.) สวมแกน ⌀10
ROD_BOT = -12.0
COVER_T = 4.0
LIP = 1.6
POCKET_R, POCKET_FLAT, POCKET_D = 17.0, 14.0, 8.0   # PETG: หลุมตัว D รอบเพลาล้อ ด้านนอกแผ่น
WASHER_T = 3.0                                    # แผ่นรองเพลาเหล็ก
SLEEVE_OD = 28.0                                  # ปลอก Al ใส่แบริ่ง 6901 (OD 24 · ผนัง 2)
NUT_Y0 = (PLATE_OUT - POCKET_D + WASHER_T) if PETG else PLATE_OUT   # ผิวรองน็อต M14
NUT_T = 7.0
PLATE_NM = f"{MAT_NM} 15" if PETG else "Al 6061 หนา 6"


def to_man(t):
    t = t.copy(); t.merge_vertices()
    return Manifold(Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))


def from_man(M):
    m = M.to_mesh()
    return trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3], np.asarray(m.tri_verts), process=True)


def cyl(c, axis, r, L, seg=64):
    t = trimesh.creation.cylinder(radius=r, height=L, sections=seg)
    R = {"x": trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]),
         "y": trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]),
         "z": np.eye(4)}[axis]
    t.apply_transform(R); t.apply_translation(c)
    return to_man(t)


def cyl_y(x, z, r, y0, y1, seg=64):
    return cyl((x, (y0 + y1) / 2, z), "y", r, abs(y1 - y0), seg)


def box(lo, hi):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    return to_man(trimesh.creation.box(extents=hi - lo).apply_translation((lo + hi) / 2))


def extrude_xz(poly, y0, y1):
    """โพลิกอนในระนาบ (x, z) → ตันตามแกน y จาก y0 ถึง y1"""
    m = trimesh.creation.extrude_polygon(poly, abs(y1 - y0))
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1.0]]))
    m.apply_translation([0, min(y0, y1), 0])
    return to_man(m)


def revolve(rz):
    """โปรไฟล์ (r, z) ปิด → ของหมุนรอบแกน z"""
    rz = list(rz) + [rz[0]]                                     # ต้องปิดวง ไม่งั้นไม่ watertight
    m = trimesh.creation.revolve(np.asarray(rz, float), sections=96)
    if m.volume < 0:
        m.invert()
    return to_man(m)


# ---------------- 2D ----------------
def bone():
    """ทรงกระดูกตามภาพ: ดุมกลาง + แขนหน้า/หลัง ตรง ปลายกลม"""
    ends = [Point(s * HALF_WB, DZ).buffer(24, 48) for s in (-1, 1)]
    hub = Point(0, 0).buffer(HUB_R, 64)
    arms = [LineString([(0, -4), (s * HALF_WB * 0.55, DZ * 0.45), (s * HALF_WB, DZ)]).buffer(15, cap_style=1, join_style=1) for s in (-1, 1)]
    return unary_union(ends + arms + [hub]).buffer(6).buffer(-6)


SCREWS = [(s * 30.0, -23.0) for s in (-1, 1)] + [(s * 80.0, -65.0) for s in (-1, 1)]     # M3 ยึดฝาครอบ
LIGHTEN = [(s * HALF_WB * 0.52, DZ * 0.42) for s in (-1, 1)]


def pin_slot():
    """27 พ.ย.: รูกลม ⌀8.8 พอดีปลอก TPU ⌀9 (อัดแน่น 0.2) → คานล็อกกับขา · กระดกได้เฉพาะยางยุบ (~±2°)"""
    return Point(0, -PIN_R).buffer(PIN_SLEEVE / 2 - 0.1, 48)


def axle_slot(x):
    return Polygon([(x - SHAFT_FLAT / 2 - 0.1, DZ), (x + SHAFT_FLAT / 2 + 0.1, DZ), (x + SHAFT_FLAT / 2 + 0.1, DZ - 30),
                    (x - SHAFT_FLAT / 2 - 0.1, DZ - 30)]).union(Point(x, DZ).buffer(SHAFT_FLAT / 2 + 0.1, 32))


def d_shape(x, r, flat):
    return Point(x, DZ).buffer(r, 64).intersection(Polygon([(x - 50, DZ - 50), (x + 50, DZ - 50), (x + 50, DZ + flat), (x - 50, DZ + flat)]))


def plate_outline():
    g = bone()
    holes = [Point(0, 0).buffer(SLEEVE_OD / 2 if PETG else 12.0, 64)]   # PETG: ปลอก Al ⌀30 · Al: แบริ่ง 6901 (12×24×6) อัดตรง
    for s in (-1, 1):                                            # ร่องเพลาแบน 12 (เปิดลง สอดเพลาจากล่าง)
        slot = Polygon([(s * HALF_WB - SHAFT_FLAT / 2 - 0.1, DZ), (s * HALF_WB + SHAFT_FLAT / 2 + 0.1, DZ),
                        (s * HALF_WB + SHAFT_FLAT / 2 + 0.1, DZ - 30), (s * HALF_WB - SHAFT_FLAT / 2 - 0.1, DZ - 30)])
        holes.append(slot.union(Point(s * HALF_WB, DZ).buffer(SHAFT_FLAT / 2 + 0.1, 32)))
    if not PETG:                                                 # PETG: ไม่เจาะช่องลดน้ำหนัก (เอาแรง) · ไม่มีฝาครอบแยก
        holes += [Point(p).buffer(7.5, 32) for p in LIGHTEN]
        holes += [Point(p).buffer(1.25, 16) for p in SCREWS]      # ต๊าป M3 (ดอก 2.5)
    holes.append(pin_slot())
    return g.difference(unary_union(holes))


# ---------------- ชิ้นส่วน ----------------
def build():
    parts, cols = {}, {}
    AL, GREY, DARK, WHITE, TPU, STEEL, BLACK = (0.62, 0.63, 0.66), (0.58, 0.59, 0.61), (0.28, 0.29, 0.31), (0.92, 0.92, 0.9), (0.18, 0.2, 0.22), (0.8, 0.8, 0.82), (0.1, 0.1, 0.11)
    P = plate_outline()
    for nm, sy in (("คานนอก", -1), ("คานใน", 1)):
        pl = extrude_xz(P, sy * PLATE_IN, sy * PLATE_OUT)
        if PETG:
            yo = sy * PLATE_OUT
            for s in (-1, 1):                                    # หลุมตัว D (แผ่นรองเหล็ก + น็อต)
                pl = pl - extrude_xz(d_shape(s * HALF_WB, POCKET_R, POCKET_FLAT), yo - sy * POCKET_D, yo + sy * 0.1)
            for (x, z) in LIGHTEN:                               # วงกลมตกแต่งแบบภาพ (บุ๋ม 1)
                pl = pl - (cyl_y(x, z, 7.0, yo - sy * 1.0, yo + sy * 0.1, 48) - cyl_y(x, z, 5.5, yo - sy * 1.2, yo + sy * 0.2, 48))
        for s_ in (-1, 1):                                       # heat-set M3 ×2/ปลายคาน (รับที่ยึด ToF) · รัศมีเข้าปลายคาน ด้านในความหนา
            for aa in (-25.0, 25.0):
                ar = math.radians(aa)
                pl = pl - cyl_y(s_ * HALF_WB + s_ * 30 * math.cos(ar), DZ + 30 * math.sin(ar), 2.0, sy * (PLATE_IN - 0.5), sy * (PLATE_IN + 7))
        parts[nm] = from_man(pl); cols[nm] = GREY if PETG else AL
    if PETG:
        sl, wa = None, None
        for sy in (-1, 1):
            t = cyl_y(0, 0, SLEEVE_OD / 2, sy * PLATE_IN, sy * PLATE_OUT, 64) - cyl_y(0, 0, 12.0, sy * (PLATE_IN - 1), sy * (PLATE_OUT + 1), 64)
            sl = t if sl is None else sl + t
            y0 = sy * (PLATE_OUT - POCKET_D)
            for s in (-1, 1):
                d = d_shape(s * HALF_WB, POCKET_R - 0.3, POCKET_FLAT - 0.3).difference(axle_slot(s * HALF_WB))
                w = extrude_xz(d, y0, y0 + sy * WASHER_T)
                wa = w if wa is None else wa + w
        parts["ปลอกแบริ่ง_Al"] = from_man(sl); cols["ปลอกแบริ่ง_Al"] = AL
        parts["แผ่นรองเพลา_D_เหล็ก3"] = from_man(wa); cols["แผ่นรองเพลา_D_เหล็ก3"] = STEEL
    # ล้อ (ตัวแทน · สายออกฝั่งใน +y)
    for s, nm in ((-1, "ล้อหลัง"), (1, "ล้อหน้า")):
        x = s * HALF_WB
        w = cyl_y(x, DZ, WD / 2, -TIRE_W / 2, TIRE_W / 2) + cyl_y(x, DZ, 50, -BODY_W / 2, BODY_W / 2) \
            + cyl_y(x, DZ, SHAFT_M / 2, -BODY_W / 2 - SHAFT_L_LAT, BODY_W / 2 + SHAFT_L_MED) \
            + cyl_y(x, DZ, NUT_R, -NUT_Y0 - NUT_T, -NUT_Y0, 6) + cyl_y(x, DZ, NUT_R, NUT_Y0, NUT_Y0 + NUT_T, 6)
        parts[nm] = from_man(w); cols[nm] = BLACK
    # บล็อกข้อเท้า (PETG-CF): เพลา ⌀12 · LM10LUU ×2 (อัดจากบน ทะลุเกือบทั้งก้อน) · รูแกน · รูหมุดหยุด M5 · เกลียว M6 กลางบน (heat-set)
    blk = box((-BLK_HX, -BLK_HY, BLK_Z0), (BLK_HX, BLK_HY, BLK_Z1))
    blk = blk - cyl_y(0, 0, 6.05, -60, 60)
    for s in (-1, 1):
        blk = blk - cyl((s * ROD_X, 0, BLK_Z1 - LM_L / 2 + 0.01), "z", LM_D / 2 + 0.05, LM_L + 0.02) - cyl((s * ROD_X, 0, 0), "z", ROD_D / 2 + 0.3, 80)
    blk = blk - cyl((0, 0, BLK_Z1 - 6), "z", 4.0, 12.02)
    for sy in (-1, 1):
        blk = blk - cyl_y(0, -PIN_R, 2.1, sy * BLK_HY - sy * 12, sy * BLK_HY + sy * 1)
    for sx in (-1, 1):                                           # ยึดดรัม M3 ×2/ด้าน (heat-set หน้า/หลังบล็อก)
        for sy in (-1, 1):
            blk = blk - cyl((sx * BLK_HX, sy * 24, 6), "x", 2.0, 12)
    parts["บล็อกข้อเท้า"] = from_man(blk); cols["บล็อกข้อเท้า"] = DARK
    # หมุดหยุดกระดก (M5 + ปลอก TPU) ×2 · ยื่นทะลุผนังดรัมเข้าร่องแผ่น
    pins = None
    for sy in (-1, 1):
        p = cyl_y(0, -PIN_R, PIN_SLEEVE / 2, sy * DRUM_HL, sy * (PLATE_OUT - 0.5), 32) + cyl_y(0, -PIN_R, 2.5, sy * (BLK_HY - 10), sy * DRUM_HL, 24)
        pins = p if pins is None else pins + p
    parts["หมุดหยุด_M5_ปลอกTPU"] = from_man(pins); cols["หมุดหยุด_M5_ปลอกTPU"] = TPU
    # ดรัม (ปุ่มข้อเท้าเทา) + คอดรัม · ผ่าหน้า/หลังที่ x = 0
    outer = cyl_y(0, 0, DRUM_R, -DRUM_HL, DRUM_HL, 128)
    inner = cyl_y(0, 0, DRUM_R - DRUM_WALL, -DRUM_HL + DRUM_WALL, DRUM_HL - DRUM_WALL, 128)
    drum = outer - inner
    drum = drum + (cyl((0, 0, (20 + COL_TOP) / 2), "z", COL_RO, COL_TOP - 20, 96) - cyl((0, 0, (20 + COL_TOP) / 2), "z", COL_RI, COL_TOP - 20 + 2, 96))
    drum = drum - cyl((0, 0, (DRUM_R + 10) / 2 + 10), "z", COL_RI, DRUM_R + 10, 96)   # เปิดบนในคอ
    drum = drum - cyl_y(0, 0, 6.3, -60, 60)                      # เพลา
    for sy in (-1, 1):
        drum = drum - cyl_y(0, -PIN_R, PIN_SLEEVE / 2 + 0.3, sy * (DRUM_HL - DRUM_WALL - 1), sy * (DRUM_HL + 1))
        drum = drum + cyl_y(0, 0, 8.0, sy * DRUM_HL, sy * (DRUM_HL + 0.5), 48) - cyl_y(0, 0, 6.3, sy * 40, sy * 50)  # แหวนแตะวงในแบริ่ง
    # แป้นยึดดรัม → บล็อก (M3 จากนอก)
    for sx in (-1, 1):
        for sy in (-1, 1):
            drum = drum + box((sx * BLK_HX + (0 if sx > 0 else -14), sy * 24 - 6, 0), (sx * BLK_HX + (14 if sx > 0 else 0), sy * 24 + 6, 12)) \
                - cyl((sx * (BLK_HX + 10), sy * 24, 6), "x", 1.7, 40)
    drum_shell = drum
    front = drum_shell ^ box((0.0, -100, -100), (100, 100, 100))
    back = drum_shell ^ box((-100, -100, -100), (0.0, 100, 100))
    parts["ดรัมข้อเท้า_หน้า"] = from_man(front); cols["ดรัมข้อเท้า_หน้า"] = GREY
    parts["ดรัมข้อเท้า_หลัง"] = from_man(back); cols["ดรัมข้อเท้า_หลัง"] = GREY
    # ฝาปุ่ม ⌀72 ×2 (ยึดปลายเพลา M6 หัวจม · ไม่หมุนตามคาน) · ร่องวงแหวนตกแต่งแบบภาพ
    caps = None
    for sy in (-1, 1):
        y0, y1 = sy * (PLATE_OUT + 1.0), sy * (PLATE_OUT + 1.0 + CAP_T)
        c = cyl_y(0, 0, CAP_R, y0, y1, 128) - cyl_y(0, 0, 13.0, y0 - sy * 0.1, y0 + sy * 1.5) \
            - (cyl_y(0, 0, 27.5, y1 - sy * 1.0, y1 + sy * 0.1, 128) - cyl_y(0, 0, 26.0, y1 - sy * 1.2, y1 + sy * 0.2, 128)) \
            - cyl_y(0, 0, 3.3, y0, y1) - cyl_y(0, 0, 6.2, y1 - sy * 3.4, y1 + sy * 0.1)
        caps = c if caps is None else caps + c
    parts["ฝาปุ่มข้อเท้า"] = from_man(caps); cols["ฝาปุ่มข้อเท้า"] = GREY
    parts["เพลาข้อเท้า_⌀12"] = from_man(cyl_y(0, 0, 6.0, -(PLATE_OUT + 1.0), PLATE_OUT + 1.0, 32)); cols["เพลาข้อเท้า_⌀12"] = STEEL
    # ซ็อกเก็ตขา (PETG-CF · ไม่ยุบ): แผ่น ⌀80 + ปลอกท่อ ⌀40 + ปากรัดยางย่น + เสากันยุบกลาง + รูแกน
    sock = cyl((0, 0, SB + SOCK_T / 2), "z", SOCK_R, SOCK_T, 96) \
        + cyl((0, 0, SB + SOCK_T + TUBE_COL_H / 2), "z", TUBE_D / 2 + 5, TUBE_COL_H, 96) \
        + (cyl((0, 0, (SPIG_Z0 + SB) / 2), "z", COL_RO, SB - SPIG_Z0 + 0.5, 96) - cyl((0, 0, (SPIG_Z0 + SB) / 2), "z", COL_RI, SB - SPIG_Z0 + 2, 96)) \
        + cyl((0, 0, (STOP_Z + 8 + SB) / 2), "z", 7.0, SB - STOP_Z - 8 + 0.5, 48)
    tube_bot = SB + SOCK_T + TUBE_COL_H - TUBE_DEPTH
    sock = sock - cyl((0, 0, tube_bot + TUBE_DEPTH / 2 + 1), "z", TUBE_D / 2 + 0.2, TUBE_DEPTH + 2, 96)
    sock = sock - cyl((0, 0, tube_bot + 22), "x", 2.75, 80)       # สลัก M5 ขวางท่อ
    sock = sock - cyl((0, 0, (STOP_Z + tube_bot) / 2), "z", 3.4, tube_bot - STOP_Z + 2)   # รูน็อต M6 ยืดสุด
    for s in (-1, 1):
        sock = sock - cyl((s * ROD_X, 0, SB + 9), "z", ROD_D / 2 - 0.1, 18.02)
    parts["ซ็อกเก็ตขา"] = from_man(sock); cols["ซ็อกเก็ตขา"] = DARK
    parts["หัวกันยุบ_TPU"] = from_man(cyl((0, 0, STOP_Z + 4), "z", 7.0, 8, 48) - cyl((0, 0, STOP_Z + 4), "z", 3.4, 10)); cols["หัวกันยุบ_TPU"] = TPU
    rods = cyl((-ROD_X, 0, (ROD_BOT + SB + 18) / 2), "z", ROD_D / 2, SB + 18 - ROD_BOT) + cyl((ROD_X, 0, (ROD_BOT + SB + 18) / 2), "z", ROD_D / 2, SB + 18 - ROD_BOT)
    parts["แกนนำ_⌀10"] = from_man(rods); cols["แกนนำ_⌀10"] = STEEL
    # สปริง (ตัวแทน: ท่อ) บล็อกบน → ใต้ซ็อกเก็ต
    spr = None
    for s in (-1, 1):
        sp = cyl((s * ROD_X, 0, (BLK_Z1 + SB) / 2), "z", SPRING_OD / 2, SB - BLK_Z1 - 0.2, 32) - cyl((s * ROD_X, 0, (BLK_Z1 + SB) / 2), "z", SPRING_OD / 2 - 1.6, SB - BLK_Z1 + 2, 32)
        spr = sp if spr is None else spr + sp
    parts["สปริง_ตัวแทน"] = from_man(spr); cols["สปริง_ตัวแทน"] = (0.85, 0.55, 0.15)
    # ยางย่น TPU (ท่าตรง): รัดคอดรัม z COL_TOP−8…COL_TOP · รัดปากซ็อกเก็ต SPIG_Z0…SB · ย่น 4 ลอน r 34↔44
    zs = np.linspace(COL_TOP, SPIG_Z0, 9)
    prof_o = [(COL_RO + 1.0, COL_TOP - 8)] + [(COL_RO + 1.0 + (9 if i % 2 else 0), z) for i, z in enumerate(zs)] + [(COL_RO + 1.0, SB)]
    prof_i = [(r - 1.0, z) for r, z in prof_o[::-1]]
    parts["ยางย่น_TPU"] = from_man(revolve(prof_o + prof_i)); cols["ยางย่น_TPU"] = TPU
    # ฝาครอบคานทรงกระดูก · Al: ฝาครอบพิมพ์แยก (หน้านอก + ขอบห่อ) · PETG: คานเป็นทรงกระดูกในตัว → เหลือแค่ฝาปลายเพลา (นอก) + รางสาย (ใน)
    B = bone()
    for side, sy in (("นอก", -1), ("ใน", 1)):
        yA = sy * PLATE_OUT
        yB = sy * (PLATE_OUT + (0 if PETG else COVER_T))
        cov = None
        if not PETG:
            cov = extrude_xz(B.buffer(LIP), yA, yB) + (extrude_xz(B.buffer(LIP), sy * PLATE_IN, yA) - extrude_xz(B.buffer(0.2), sy * (PLATE_IN - 1), yA + sy * 0.01))
            cov = cov - cyl_y(0, 0, CAP_R + 1.0, sy * 40, sy * 80, 128)
            for (x, z) in SCREWS:
                cov = cov - cyl_y(x, z, 1.7, yA, yB + sy) - cyl_y(x, z, 3.2, yB - sy * 1.8, yB + sy * 0.1, 24)
            for (x, z) in LIGHTEN:
                cov = cov - (cyl_y(x, z, 7.0, yB - sy * 1.0, yB + sy * 0.1, 48) - cyl_y(x, z, 5.5, yB - sy * 1.2, yB + sy * 0.2, 48))
        ring_r = 19.0 if PETG else 16.0                          # PETG: ครอบหลุม D (r 17)
        for s in (-1, 1):
            x = s * HALF_WB
            if cov is not None:
                cov = cov - cyl_y(x, DZ, NUT_R + 1.0, yA - sy * 0.1, yB + sy * 0.1, 48)
            if side == "นอก":                                    # ฝาปลายเพลาโค้ง (ครอบน็อต+เพลา)
                y_end = -max(BODY_W / 2 + SHAFT_L_LAT, NUT_Y0 + NUT_T) - 2.5
                cap = cyl_y(x, DZ, ring_r, yB, y_end - 2.0, 48) - cyl_y(x, DZ, NUT_R + (3.3 if PETG else 1.0), yA + 0.1, y_end, 48)
                cap = cap + (to_man(trimesh.creation.icosphere(subdivisions=3, radius=ring_r).apply_scale([1, 0.25, 1]).apply_translation([x, y_end - 2.0, DZ])) - cyl_y(x, DZ, 25, y_end - 2.0 + 0.01, 0))
                cov = cap if cov is None else cov + cap
            else:                                                # ข้องอสาย + รางสายตามแขนถึงบนคาน
                y_exit = BODY_W / 2 + SHAFT_L_MED
                yc = max(y_exit, yB + 6.0) + CABLE_BEND_R
                ring = cyl_y(x, DZ, ring_r, yB, yc + CABLE_D / 2 + 2.5, 48) - cyl_y(x, DZ, ring_r - 2.3, yA - 0.1, yc + CABLE_D / 2 + 0.5, 48)
                path = LineString([(x, DZ), (s * HALF_WB * 0.55, DZ * 0.45), (s * 44.0, 14.0)])
                duct = extrude_xz(path.buffer(CABLE_D / 2 + 2.5, cap_style=1), yc - CABLE_D / 2 - 2.5, yc + CABLE_D / 2 + 2.5) \
                    - extrude_xz(path.buffer(CABLE_D / 2 + 0.5, cap_style=1), yc - CABLE_D / 2 - 0.5, yc + CABLE_D / 2 + 0.5)
                web = extrude_xz(path.buffer(4.0, cap_style=1), yB, yc - CABLE_D / 2 - 2.0)
                add = ring + duct + web
                cov = add if cov is None else cov + add
                cov = cov - cyl_y(x, DZ, ring_r - 2.3, yA - 0.1, yc + CABLE_D / 2 + 0.5, 48)
                cov = cov - extrude_xz(Point(s * 44.0, 14.0).buffer(CABLE_D / 2 + 0.5), yc - CABLE_D / 2 - 0.5, yc + 40)  # ทางออกบน (เปิด)
                cov = cov - box((s * 44.0 - 6, yc - CABLE_D / 2 - 0.5, 14.0), (s * 44.0 + 6, yc + CABLE_D / 2 + 0.5, 40))
        nm = (("ฝาปลายเพลานอก" if side == "นอก" else "รางสายใน") if PETG else f"ฝาครอบคาน{side}")
        parts[nm] = from_man(cov); cols[nm] = GREY
    # ---- ที่ยึด ToF หน้า/หลัง (27 พ.ย. #robot-spec-อัปเดต · 00:30 "เอากันล้อออก" → ไม่มีกันชน/ไมโครสวิตช์ เหลือ ToF) ----
    # แผ่นหู PETG-CF (ทางผสม 27 พ.ย. 06:46) แนบปลายคานนอก (ในแนวความหนาคาน |y| 46.5–61.5 = นอกล้อ) ยื่นออกถึง r ~70 · M3 ×2 เข้า heat-set ปลายคาน · ToF VL53L1X มองหน้า-ลง 12°
    TOF = (13.5, 18.5, 4.5)                                      # VL53L1X บอร์ดเล็ก (Pololu 13×18) MEASURE
    for s_, nm in ((1, "หน้า"), (-1, "หลัง")):
        x0 = s_ * HALF_WB
        sy = -1                                                  # ฝั่งนอก
        ya, yb = sorted((sy * (PLATE_IN + 0.5), sy * (PLATE_OUT + 4.0)))
        A0, A1, R1 = -32.0, 8.0, WD / 2 + 6.0
        tab = Polygon([(x0 + s_ * 24.5 * math.cos(math.radians(q)), DZ + 24.5 * math.sin(math.radians(q))) for q in np.linspace(A0, A1, 20)] +
                      [(x0 + s_ * R1 * math.cos(math.radians(q)), DZ + R1 * math.sin(math.radians(q))) for q in np.linspace(A1, A0, 20)])
        hold = extrude_xz(tab, ya, yb)
        q = math.radians(-12.0)
        ct = np.array([x0 + s_ * (R1 - 5.0) * math.cos(q), (ya + yb) / 2, DZ + (R1 - 5.0) * math.sin(q)])
        hold = hold - box((ct[0] - 3.0, ct[1] - TOF[1] / 2 + 3, ct[2] - TOF[0] / 2), (ct[0] + 3.0, ct[1] + TOF[1] / 2 + 3, ct[2] + TOF[0] / 2))
        hold = hold - cyl((ct[0] + s_ * 6, ct[1], ct[2]), "x", 4.5, 14)                    # หน้าต่างเลนส์
        for aa in (-25.0, 25.0):
            ar = math.radians(aa)
            p = (x0 + s_ * 30 * math.cos(ar), DZ + 30 * math.sin(ar))
            if A0 <= aa <= A1 + 20:
                hold = hold - cyl_y(p[0], p[1], 1.7, sy * (PLATE_IN - 1), sy * (PLATE_OUT + 6))
        parts[f"ที่ยึด_ToF_{nm}"] = from_man(hold); cols[f"ที่ยึด_ToF_{nm}"] = DARK
    return parts, cols


M_ROBOT = 36.0                                   # หุ่น V1 ประมาณ 32–38 กก.
M_BELOW = 6.0 + 0.6                              # ใต้เพลาข้อเท้า/เท้า: ล้อ 2 + คาน/ฝาครอบ
SPRING_K, PRELOAD = 19.6, 6.0                    # N/มม./ตัว · มม. (ISO 10243 เขียว ⌀20×64 · ติดตั้ง 58 · ยุบใช้งานสูงสุด 40% = 25.6 ≥ 6+18)


def strength_report():
    """ความแข็งแรงข้อเท้า (ต่อ 1 ข้าง) · แรงลงแนวดิ่ง + แรงด้านข้าง · เลขแบบอนุรักษ์ (ไม่รวมตัวคูณความปลอดภัย เว้นที่บอก)"""
    g = 9.81
    above = M_ROBOT - 2 * M_BELOW
    st = above / 2                                   # กก./ข้อเท้า ยืน 2 ขา
    design = above * 3                               # ยืนขาเดียว × กระแทก 3 เท่า (ตกหลุม/ขอบทาง)
    # เพลา ⌀12 เหล็ก S45C (yield ~350 MPa) · ช่วงแบริ่ง ±49.5 · แรงจากบล็อกกว้าง ±43 → M = F/2 × (49.5 − 21.5)
    Z12 = math.pi * 12 ** 3 / 32
    shaft = 350 * Z12 / (0.5 * (PLATE_IN + PLATE_T / 2 - BLK_HY / 2)) / g
    brg = 2 * 1460 / g                               # 6901 C0r 1.46 kN ×2 (NSK/NTN)
    # แขนคาน · แต่ละปลายรับ F/4 · คาน 100 · Al 6061-T6 (yield 276 · หน้าตัด 30×6 หักรู ⌀15) / PETG-CF (ดัด XY 70 MPa แบบอนุรักษ์ · datasheet 83 · หน้าตัด 30×15 ไม่มีรู)
    if PETG:
        Zarm = PLATE_T * 30 ** 2 / 6
        arm = MAT_SIG * Zarm * 4 / HALF_WB / g       # ค่าดัดออกแบบจากตาราง MATS
        arm_creep = arm / MAT_CREEP
    else:
        Zarm = 6 * (30 ** 3 - 15 ** 3) / (6 * 30)
        arm = 276 * Zarm * 4 / HALF_WB / g
    wheel = 2 * 150.0                               # ZLLG45 150 กก./ล้อ (สเปกผู้ผลิต)
    post = math.pi * (7 ** 2 - 3.5 ** 2) * MATS["pahtcf"][3] / g        # เสากันยุบพิมพ์ PAHT-CF (กด 30 MPa แบบอนุรักษ์)
    tube = math.pi * (20 ** 2 - 18 ** 2) * MATS["pahtcf"][3] / g        # ปลายท่อ Al กดก้นซ็อกเก็ต PAHT-CF
    spring_max = 2 * SPRING_K * (HEAVE + PRELOAD) / g
    rows = [("ล้อ ZLLG45 ×2 (สเปก)", wheel), ("แบริ่ง 6901 ×2 (C0r 1.46 kN/ตัว)", brg), ("เพลา ⌀12 เหล็ก (ดัด · ถึงคราก)", shaft),
            (f"เสากันยุบ {BLK_MAT} (กด)", post), ("ก้นซ็อกเก็ตรับปลายท่อ (กด)", tube)]
    if PETG:
        rows += [(f"คาน {MAT_NM} 15 ×2 (ดัด · แรงชั่วคราว)", arm), (f"คาน {MAT_NM} 15 ×2 (รับค้างนาน ÷{MAT_CREEP})", arm_creep)]
    else:
        rows += [("คาน Al 6 ×2 (ดัด · ถึงคราก)", arm)]
    weakest = min(rows, key=lambda r: r[1])
    out = ["ความแข็งแรงข้อเท้า (ต่อ 1 ข้าง · แรงลงแนวดิ่ง):",
           f"  หุ่น ~{M_ROBOT:.0f} กก. · ส่วนเหนือข้อเท้า ~{above:.1f} กก. → ยืนปกติ ~{st:.1f} กก./ข้าง · กรณีออกแบบ (ขาเดียว × กระแทก 3) ~{design:.0f} กก./ข้าง"]
    for nm, v in rows:
        out.append(f"  {nm}: ~{v:.0f} กก.")
    out.append(f"  → จุดอ่อนสุด = {weakest[0]} ~{weakest[1]:.0f} กก./ข้าง = {weakest[1]/design:.1f}× กรณีออกแบบ · {weakest[1]/st:.0f}× ยืนปกติ")
    if PETG:
        # ปลายคานแอ่น (คานยื่น 100 · 2 แผ่น · แต่ละปลายรับ ¼ ของแรงยืน) · E ชื้น/อุ่นแบบอนุรักษ์ · รับค้างนาน ×MAT_CREEP
        I1 = PLATE_T * 30 ** 3 / 12
        F_end = st * g / 4
        d0 = F_end * HALF_WB ** 3 / (3 * MAT_E * I1)
        out.append(f"  ปลายคานแอ่นตอนยืน ~{d0:.2f} มม. (E {MAT_E:.0f}) · รับค้างนาน ~{d0*MAT_CREEP:.1f} มม. · ล้อเอียงตาม ~{math.degrees(1.5*d0*MAT_CREEP/HALF_WB):.1f}° → ยอมได้ ≤ 1 มม. / 1°")
    out.append(f"  สปริง k {SPRING_K} N/มม. ×2 (อัดค้าง {PRELOAD:.0f}): รับยุบได้ถึง ~{spring_max:.0f} กก./ข้าง ({spring_max/st:.1f}× ยืนปกติ) · เกินนี้ชนหัวกันยุบ TPU (ตั้งใจ) · ยุบนิ่ง ~{max(0, st*g/2/SPRING_K-PRELOAD):.0f} มม.")
    # ด้านข้าง: แรงด้าน y ที่พื้น → โมเมนต์ที่ LM (บุชยาว 55 · ช่วงต้าน ~0.7L) และที่โคนแกนในซ็อกเก็ต
    h_lm = PIVOT_Z + BLK_Z1 - LM_L / 2
    lm_c0 = 1100.0                                    # LM10LUU C0 ~1.1 kN (ทั่วไป · ยี่ห้อต่างกัน)
    side_lm = lm_c0 / 2 * 2 * (0.7 * LM_L) / h_lm / g   # ตัวคูณ 2
    Z10 = math.pi * 10 ** 3 / 32
    side_rod = 2 * 300 * Z10 / (PIVOT_Z + SB) / g
    out.append(f"ด้านข้าง (ผลักหุ่นทางข้าง · แรงที่ล้อ): LM10LUU ×2 ~{side_lm:.0f} กก./ข้าง (เผื่อ 2×) · แกน ⌀10 ดัดที่โคน ~{side_rod:.0f} กก./ข้าง (ถึงคราก) → ทิศอ่อนสุดของข้อเท้า")
    out.append("  (เดิม LM10UU สั้น ~ครึ่งเดียว → เปลี่ยนเป็น LM10LUU แล้ว) · ใช้งานจริง: เลี้ยว/ลาดเอียงเบา ~2–5 กก./ข้าง = ผ่าน · ห้ามยก/ลากหุ่นทางข้างจากเท้า")
    out += stability_report()
    return out


# ---------------- การทรงตัวตอนออกตัว/เบรก/เลี้ยว (27 พ.ย. 00:12) ----------------
CG_Z, CG_X = 0.516, -0.017                       # จุดศูนย์ถ่วงทั้งตัว (ประมาณจากชิ้น V1 รอบ 6 · ม.) · x เทียบกลางเท้า −0.022
M_SPRUNG, H_SPRUNG = 23.3, 0.635                 # มวลเหนือข้อเท้า (กก.) · สูงจากเพลาข้อเท้า (ม.)
TPU_K = 1.0e6                                    # ปลอก TPU 95A ⌀9 ผนัง ~2 อัดแน่น: แข็งรัศมี ~1 kN/มม. (ประมาณ · MEASURE)
A_LIMIT = dict(เร่ง=0.4, เบรกปกติ=0.6, เบรกฉุกเฉิน=0.9, เลี้ยว=0.5)   # ม./วิ² (เผื่อ ≥ 2 เท่าจากจุดล้ม)


def stability_report():
    g = 9.81
    xf, xr = HALF_WB / 1000 - (CG_X + 0.022), HALF_WB / 1000 + (CG_X + 0.022)
    yl = abs(FOOT_Y) / 1000
    out = ["การทรงตัว (หุ่นแข็ง · จุดศูนย์ถ่วง z ~%.2f ม.):" % CG_Z]
    for nm, d in (("เบรก → หน้าทิ่ม", xf), ("ออกตัว → หงายหลัง", xr), ("เลี้ยว → ล้มข้าง", yl)):
        out.append(f"  {nm}: ล้มที่ ~{g*d/CG_Z:.2f} ม./วิ² · เอียงพื้นล้มที่ ~{math.degrees(math.atan(d/CG_Z)):.1f}°")
    # ก้ม-เงยตัว: เดิมคานหมุนอิสระ (ไม่มีแรงคืน) → ตอนนี้หมุด TPU อัดแน่น 2 ตัว/เท้า ที่ r PIN_R
    k_pitch = 2 * 2 * TPU_K * (PIN_R / 1000) ** 2            # 2 เท้า × 2 หมุด
    dest = M_SPRUNG * g * H_SPRUNG
    out.append(f"  ก้ม-เงย: แรงคืนหมุด TPU ~{k_pitch:.0f} N·m/rad vs แรงล้ม mgh {dest:.0f} → {'✅ นิ่ง' if k_pitch > 3 * dest else '⚠️'} · "
               f"เบรก 0.9 ม./วิ² → ตัวก้ม ~{math.degrees(M_SPRUNG*0.9*H_SPRUNG/(k_pitch-dest)):.1f}° (เดิมคานอิสระ ±10° = โยกจนชนตัวหยุด)")
    # เอียงข้าง: สปริงอัดค้างเกินน้ำหนักยืน → ปกติแข็ง (ชนตัวหยุดบน)
    st = M_SPRUNG * g / 2
    pre = 2 * SPRING_K * PRELOAD
    a_top = (pre - st) / (M_SPRUNG * H_SPRUNG / (2 * yl))
    out.append(f"  เอียงข้าง: น้ำหนักยืน ~{st:.0f} N/เท้า · สปริงอัดค้าง {pre:.0f} N/เท้า ({pre/st:.1f}×) → เท้าไม่ยุบจนกว่าเลี้ยว/เบรกเกิน ~{a_top:.1f} ม./วิ² (เกินค่าจำกัด) = แข็งตอนใช้งานปกติ "
               f"(เดิม k 3.5 อัดค้าง 70 N < น้ำหนัก → แรงคืนเอียงข้าง ≈ แรงล้ม = โยกซ้าย-ขวา)")
    out.append("  ค่าจำกัดแนะนำ (เผื่อ ≥ 2×): " + " · ".join(f"{k} ≤ {v}" for k, v in A_LIMIT.items()) + " ม./วิ² · ความเร็ว ใกล้คน ≤ 0.5 · ที่โล่ง ≤ 1.0 ม./วิ · "
               "วงเลี้ยว ≥ v²/0.5 (0.5 ม./วิ → 0.5 ม. · 1 ม./วิ → 2 ม.) · เร่ง/ลดแบบโค้ง S (ตั้งเวลาเร่ง-ลดใน ZLAC8015D + Nav2 velocity smoother + กรองจอย) · E-stop ตัดไฟล้อ = ล้อไหล ไม่ล็อก")
    return out


def place(m, rock=0.0, heave=0.0):
    m = m.copy()
    if rock:
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(rock), [0, 1, 0], [0, 0, 0]))
    m.apply_translation([FOOT_X, FOOT_Y, PIVOT_Z - heave])
    return m


ROCKING = ("คานนอก", "คานใน", "ล้อหลัง", "ล้อหน้า", "ฝาครอบคานนอก", "ฝาครอบคานใน", "ฝาปลายเพลานอก", "รางสายใน", "ปลอกแบริ่ง_Al", "แผ่นรองเพลา_D_เหล็ก3",
           "ที่ยึด_ToF_หน้า", "ที่ยึด_ToF_หลัง")
HEAVING = ROCKING + ("บล็อกข้อเท้า", "หมุดหยุด_M5_ปลอกTPU", "ดรัมข้อเท้า_หน้า", "ดรัมข้อเท้า_หลัง", "ฝาปุ่มข้อเท้า", "เพลาข้อเท้า_⌀12")
SKIP_CHECK = ("สปริง_ตัวแทน", "ยางย่น_TPU")                       # ยืด/ยุบได้ · ไม่เช็กชน


def posed(parts, rk, hv):
    """heave = ยุบ (บล็อกขึ้นหาซ็อกเก็ต) → ในพิกัดหุ่น ชิ้นที่ไม่ยุบ (ซ็อกเก็ต/แกน) ลงมา · ที่นี่ให้ชิ้นยุบขึ้น +hv แทน"""
    out = {}
    for k, v in parts.items():
        out[k] = place(v, rk if k in ROCKING else 0, -hv if k in HEAVING else 0)
    return out


def main():
    parts, cols = build()
    rep = [f"เท้า V1 รอบ 3 · คาน {PLATE_NM} (ขับ 4 ล้อ ZLLG45-ASM200 ×2/เท้า · คานล็อกด้วยหมุด TPU (ยืดหยุ่น ±{ROCK:.0f}°) · ข้อเท้ายุบ {HEAVE:.0f} มม. สปริงแม่พิมพ์อัดค้าง ×2 · ToF หน้า/หลัง · ปุ่มข้อเท้าทรงกระดูกตามภาพ) · หน่วย มม.",
           f"ล้อ ⌀{WD:.0f} ห่างหน้า-หลัง {2*HALF_WB:.0f} · กลางเท้า y {FOOT_Y:.0f} · เพลาข้อเท้า z {PIVOT_Z:.0f} · ยาวเท้า ~{2*HALF_WB+WD:.0f} (ภาพ ~262 ที่ล้อ ⌀100)"]
    # เช็กชน: ทุกท่า (กระดก × ยุบ) ทุกคู่ที่ขยับต่างกัน
    names = [k for k in parts if k not in SKIP_CHECK]
    group = {k: ("R" if k in ROCKING else "H" if k in HEAVING else "F") for k in names}
    allowed = {frozenset(p) for p in [("บล็อกข้อเท้า", "แกนนำ_⌀10"), ("หมุดหยุด_M5_ปลอกTPU", "บล็อกข้อเท้า"), ("เพลาข้อเท้า_⌀12", "บล็อกข้อเท้า"),
                                       ("เพลาข้อเท้า_⌀12", "คานนอก"), ("เพลาข้อเท้า_⌀12", "คานใน"), ("เพลาข้อเท้า_⌀12", "ฝาปุ่มข้อเท้า"),
                                       ("หัวกันยุบ_TPU", "ซ็อกเก็ตขา"), ("แกนนำ_⌀10", "ซ็อกเก็ตขา"), ("ล้อหน้า", "คานนอก"), ("ล้อหน้า", "คานใน"),
                                       ("ล้อหลัง", "คานนอก"), ("ล้อหลัง", "คานใน"), ("ล้อหน้า", "ฝาครอบคานนอก"), ("ล้อหลัง", "ฝาครอบคานนอก"),
                                       ("ล้อหน้า", "ฝาครอบคานใน"), ("ล้อหลัง", "ฝาครอบคานใน"), ("ดรัมข้อเท้า_หน้า", "ดรัมข้อเท้า_หลัง"),
                                       ("ดรัมข้อเท้า_หน้า", "บล็อกข้อเท้า"), ("ดรัมข้อเท้า_หลัง", "บล็อกข้อเท้า"), ("หมุดหยุด_M5_ปลอกTPU", "ดรัมข้อเท้า_หน้า"),
                                       ("หมุดหยุด_M5_ปลอกTPU", "ดรัมข้อเท้า_หลัง"), ("เพลาข้อเท้า_⌀12", "ดรัมข้อเท้า_หน้า"), ("เพลาข้อเท้า_⌀12", "ดรัมข้อเท้า_หลัง"),
                                       ("ปลอกแบริ่ง_Al", "คานนอก"), ("ปลอกแบริ่ง_Al", "คานใน"), ("แผ่นรองเพลา_D_เหล็ก3", "ล้อหน้า"), ("แผ่นรองเพลา_D_เหล็ก3", "ล้อหลัง"),
                                       ("แผ่นรองเพลา_D_เหล็ก3", "คานนอก"), ("แผ่นรองเพลา_D_เหล็ก3", "คานใน"), ("ฝาปลายเพลานอก", "คานนอก"), ("รางสายใน", "คานใน"),
                                       ("ที่ยึด_ToF_หน้า", "คานนอก"), ("ที่ยึด_ToF_หลัง", "คานนอก"),
                                       ("หมุดหยุด_M5_ปลอกTPU", "คานนอก"), ("หมุดหยุด_M5_ปลอกTPU", "คานใน")]}   # ปลอก TPU อัดแน่นในรูคาน (ตั้งใจ)
    worst, cases = [], 0
    for rk in (-ROCK + 0.5, 0, ROCK - 0.5):
        for hv in (0, HEAVE - 2.5):
            Ms = {k: to_man(v) for k, v in posed({k: parts[k] for k in names}, rk, hv).items()}
            for i, a in enumerate(names):
                for b in names[i + 1:]:
                    if frozenset((a, b)) in allowed:
                        continue
                    cases += 1
                    v = (Ms[a] ^ Ms[b]).volume() / 1000
                    if v > 0.005:
                        worst.append(f"  ❌ กระดก {rk:+.1f}° ยุบ {hv:.1f}: {a} ↔ {b} {v:.3f} ซม.³")
    rep += worst or [f"  เช็กชน {cases} คู่×ท่า (กระดก ±9.5/0° × ยุบ 0/22.5): ✅ ไม่ชน (คู่ที่ประกอบติดกันจริงไม่นับ)"]
    # หมุดหยุดแตะร่องที่ ±10.x°
    for rk in (ROCK + 0.3, -ROCK - 0.3):
        Ms = posed({k: parts[k] for k in ("หมุดหยุด_M5_ปลอกTPU", "คานนอก")}, rk, 0)
        v = (to_man(Ms["หมุดหยุด_M5_ปลอกTPU"]) ^ to_man(Ms["คานนอก"])).volume()
        rep.append(f"  หมุดหยุดที่ {rk:+.1f}°: {'แตะขอบร่อง ✅ (หยุดได้)' if v > 0 else '⚠️ ไม่แตะ'}")
    # ช่องว่างสำคัญ
    clr = math.hypot(HALF_WB, DZ) - WD / 2 - DRUM_R
    rep.append(f"  ระยะล้อ ↔ ดรัม {clr:.1f} (คงที่ทุกท่ากระดก เพราะหมุนรอบจุดเดียวกัน)")
    rep.append(f"  ยางย่น: ยาวช่วงลอน {SPIG_Z0-COL_TOP:.0f} → ยุบสุด {SPIG_Z0-COL_TOP-HEAVE:.0f} (พับลอน 4×2×1) · หัวกันยุบแตะที่ยุบ {STOP_Z-BLK_Z1:.0f}")
    L_inst = SB - BLK_Z1
    rep.append(f"  สปริงแม่พิมพ์ ISO 10243 เขียว ⌀{SPRING_OD:.0f}×{L_inst+PRELOAD:.0f} ×2/เท้า (สวมแกน ⌀10): ติดตั้ง {L_inst:.0f} (อัดค้าง {PRELOAD:.0f}) → ยุบสุด {L_inst-HEAVE:.0f} · k ≈ {SPRING_K} N/มม./ตัว · ยุบรวม {PRELOAD+HEAVE:.0f} ≤ 40% ของยาว ({0.4*(L_inst+PRELOAD):.1f}) ✅")
    rep += strength_report()
    # น้ำหนัก
    rho = {"Al": 2.70e-3, "pr": 1.27e-3 * 0.55, "prd": 1.27e-3 * 0.85, "tpu": 1.2e-3 * 0.8, "st": 7.85e-3}
    kind = {"คานนอก": "prd" if PETG else "Al", "คานใน": "prd" if PETG else "Al", "ปลอกแบริ่ง_Al": "Al", "แผ่นรองเพลา_D_เหล็ก3": "st", "แกนนำ_⌀10": "st", "เพลาข้อเท้า_⌀12": "st", "ยางย่น_TPU": "tpu", "หัวกันยุบ_TPU": "tpu"}
    g = 0.0
    for k, v in parts.items():
        if k.startswith("ล้อ") or k == "สปริง_ตัวแทน":
            continue
        g += abs(v.volume) * rho[kind.get(k, "pr")]
    rep.append(f"น้ำหนักต่อเท้า ~{6.0 + g/1000 + 0.12:.1f} กก. (มอเตอร์ 6.0 + โครง/พิมพ์/เหล็ก {g/1000:.2f} + แบริ่ง/LM/สปริง ~0.12) · 2 เท้า ~{2*(6.0+g/1000+0.12):.1f} กก.")
    rep.append("ตัวขับ ZLAC8015D ×2 → อกล่าง (v1_build.py · z 875) · สายมอเตอร์ 600 ต้องต่อยาว ~35–45 ซม. ×4")
    rep.append("ToF (27 พ.ย.): ที่ยึด PETG-CF ปลายคานนอก หน้า/หลัง (M3 ×2 เข้า heat-set ปลายคาน) · VL53L1X ×1/ปลาย (4 ตัวทั้งหุ่น) มองหน้า-ลง 12° · กันชน/ไมโครสวิตช์ล้อ = ตัดออก (00:30) → ชนแล้วหยุดด้วยซอฟต์แวร์ (ToF + LiDAR + กระแสมอเตอร์ ZLAC พุ่ง)")
    rep.append("ของ: สปริงแม่พิมพ์ ISO 10243 เขียว ⌀20×64 ×4 (+2 สำรอง) · LM10LUU ×4 · น็อต M6×100 ×2 · หมุด M5 ×4 + ปลอก TPU ⌀9 อัดแน่น · M3 ×32 + heat-set M3 ×16 · M14 บาง ×8 · แบริ่ง 6901 ×4 · แกน ⌀10×125 ×4 · เพลา ⌀12×107 (ต๊าป M6 2 ปลาย) ×2 · VL53L1X ×4 · " + (f"ปลอก Al ⌀28/24×15 ×4 · แผ่นรองเพลาเหล็ก 3 ตัว D ×8 (คานพิมพ์ {MAT_NM} เอง)" if PETG else "แผ่น Al 6 ×4"))
    rep.append((f"พิมพ์: คานนอก/ใน {MAT_NM} (นอนราบ · ผนัง 6 · infill 60%) · ฝาปลายเพลานอก · รางสายใน" if PETG else "พิมพ์: ฝาครอบคาน นอก/ใน (PETG เทา)") + " · บล็อก + ซ็อกเก็ต (PAHT-CF) · ดรัม หน้า/หลัง (PLA ดำ · สีตามคลัง 27 พ.ย.) · ฝาปุ่ม ×2 + ที่ยึด ToF ×2 + ฝาปลายเพลา (PETG-CF · ทางผสม 27 พ.ย. 06:46) · ยางย่น · หัวกันยุบ · ปลอกหมุด (TPU) — ×2 เท้า (ซ้าย = กลับ y)")
    os.makedirs(OUT, exist_ok=True)
    P = plate_outline()
    path = trimesh.load_path(np.array(P.exterior.coords)[:, :2])
    for h in P.interiors:
        path = trimesh.path.util.concatenate([path, trimesh.load_path(np.array(h.coords)[:, :2])])
    path.export(os.path.join(OUT, "show_v1_foot1_คาน_Al6.dxf" if not PETG else "show_v1_foot1_คาน_โครง2D.dxf"))
    rep.append(f"แผ่นคาน {PLATE_NM}: กล่อง {P.bounds[2]-P.bounds[0]:.0f}×{P.bounds[3]-P.bounds[1]:.0f} · ~{(P.area*PLATE_T*1.27e-6*0.85 if PETG else P.area*6*2.7e-6):.2f} กก./แผ่น · 4 แผ่น (2 เท้า) · " + ("รูปลอก Al ⌀28 · หลุมตัว D ลึก 8 ที่เพลาล้อ · heat-set M3 ×2/ปลาย (ที่ยึด ToF)" if PETG else "รูแบริ่ง ⌀24 อัดแน่น · ต๊าป M3 ×4") + " · รูหมุดล็อก ⌀8.8 (ปลอก TPU ⌀9 อัดแน่น)")
    pz = posed(parts, 0, 0)
    allv = np.vstack([m.vertices for m in pz.values()])
    rep.append(f"กรอบเท้า (ท่าตรง · พิกัดหุ่น): x {allv[:,0].min():.0f}…{allv[:,0].max():.0f} · y {allv[:,1].min():.0f}…{allv[:,1].max():.0f} · z {allv[:,2].min():.0f}…{allv[:,2].max():.0f} · ก้นท่อขา z {PIVOT_Z+SB+SOCK_T+TUBE_COL_H-TUBE_DEPTH:.0f}")
    rep.append(f"ต่างจากภาพ: ล้อ ⌀128 (ภาพ ~100) · ยางย่นสูง {SB-COL_TOP+8:.0f} ระหว่างปุ่มกับขา (ภาพไม่มี) · รางสายฝั่งใน (กว้างออก ~{CABLE_BEND_R+CABLE_D+COVER_T:.0f})")
    # ส่งออก
    for f in os.listdir(OUT):
        if f.startswith("show_v1_foot1_") and f.endswith(".stl"):
            os.remove(os.path.join(OUT, f))
    scene = []
    for k, m in pz.items():
        m.export(os.path.join(OUT, f"show_v1_foot1_{k}.stl"))
        mm = m.copy(); mm.visual.face_colors = (np.array(cols[k]) * 255).astype(int).tolist() + [255]
        scene.append(mm)
    trimesh.Scene(scene).export(os.path.join(OUT, "show_v1_foot1.3mf"))
    open(os.path.join(OUT, "show_v1_foot1_report.txt"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    render(parts, cols)


def render(parts, cols):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    plt.rcParams["font.family"] = "Loma"; plt.rcParams["axes.unicode_minus"] = False
    fig, axs = plt.subplots(1, 5, figsize=(26, 6.2), gridspec_kw={"width_ratios": [1.2, 1.2, 1.2, 0.8, 1.2]})
    iso = trimesh.transformations.rotation_matrix(math.radians(-35), [0, 0, 1]) @ trimesh.transformations.rotation_matrix(math.radians(18), [1, 0, 0])
    views = [("ข้างนอก · ตรง", 0, 0, "side"), ("กระดก +10°", ROCK, 0, "side"), ("ยุบ 25 มม.", 0, HEAVE, "side"), ("หน้า", 0, 0, "front"), ("มุมเฉียง", 0, 0, "iso")]
    for ax, (tt, rk, hv, vw) in zip(axs, views):
        P_, C_, D_ = [], [], []
        L = np.array([0.35, 0.45, 0.82]); L /= np.linalg.norm(L)
        for k, mm in posed(parts, rk, hv).items():
            if vw == "side":
                R = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])          # มองจากฝั่ง −y (นอก) → ลึก = −y
                V = mm.vertices @ R.T; V[:, 2] = -V[:, 2]
            elif vw == "front":
                R = np.array([[0, -1, 0], [0, 0, 1], [1, 0, 0]])
                V = mm.vertices @ R.T
            else:
                V = (mm.vertices - [FOOT_X, FOOT_Y, 0]) @ iso[:3, :3].T
                V = V[:, [0, 2, 1]] * [1, 1, -1]
            F = mm.faces
            n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
            if vw == "side":
                n = -n
            vis = n[:, 2] > 0
            P_.append(V[F[vis]][:, :, :2]); C_.append((np.clip(np.abs(n[vis] @ L), 0, 1)[:, None] * 0.55 + 0.45) * np.array(cols[k])); D_.append(V[F[vis]][:, :, 2].mean(1))
        P_ = np.concatenate(P_); C_ = np.concatenate(C_); o = np.argsort(np.concatenate(D_))
        ax.add_collection(PolyCollection(P_[o], facecolors=np.clip(C_[o], 0, 1), edgecolors="none"))
        if vw != "iso":
            ax.axhline(0, c="k", lw=0.6)
        ax.set_aspect("equal"); ax.autoscale(); ax.set_title(tt, fontsize=13); ax.axis("off")
    fig.suptitle("เท้า V1 รอบ 2: ปุ่มข้อเท้าเทา (ดรัม D96 + ฝาปุ่ม) · คานทรงกระดูก " + PLATE_NM + " · ยางย่น TPU ปิดสปริงยุบ 25 มม. · ล้อ ZLLG45 4.5\"", fontsize=14)
    fig.savefig(os.path.join(OUT, "show_v1_foot1_preview.png"), dpi=80, bbox_inches="tight")


if __name__ == "__main__":
    main()

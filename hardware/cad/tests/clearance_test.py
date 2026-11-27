"""ชิ้นทดสอบระยะเผื่อ (clearance test) สำหรับ Bambu Lab X2D

แผ่นเดียว 3 แถว × 5 ช่อง (คอลัมน์ = ค่าเผื่อ 0.1 / 0.2 / 0.3 / 0.4 / 0.5 มม.)
  แถว S  : รูเพลา ⌀(PIN_D + c)            → ลองสวมกับหมุด ⌀PIN_D ที่พิมพ์มาด้วย
  แถว M3 : ช่องน็อต M3 ข้ามแบน (5.5 + c)   + รูสกรูผ่านตาม params
  แถว M4 : ช่องน็อต M4 ข้ามแบน (7.0 + c)   + รูสกรูผ่านตาม params
+ หมุดทดสอบ 1 ชิ้น (⌀PIN_D พิมพ์ตั้ง)

วิธีพิมพ์: PLA Basic · ชั้น 0.2 · ผนัง 2 เส้น · infill 15% · ไม่ต้องมี support · วางตามไฟล์ 3mf
วิธีอ่านผล: ช่องแรก (ค่าน้อยสุด) ที่หมุดสวมลื่น/หมุนได้ = FIT_SLIDE · ที่สวมแน่นถอดด้วยมือได้ = FIT_SNUG
            ช่องน็อตแรกที่กดน็อตลงได้ด้วยนิ้วแล้วไม่หลุดเมื่อคว่ำ = NUT_AF_OFFSET
            → แก้ค่าใน cad/params.py แล้วเพิ่มบรรทัดใน CALIBRATION_LOG

รัน:  python3 cad/tests/clearance_test.py   → cad/out/clearance_test.{step,3mf,png}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build123d import (Align, Axis, Box, BuildPart, BuildSketch, Cylinder, FontStyle, Locations,
                       Mode, Plane, RegularPolygon, Text, chamfer, extrude)

import params as P
from tools.export import export_part

# ---------------------------------------------------------------- พารามิเตอร์ (แก้ได้)
CLEARANCES = [0.1, 0.2, 0.3, 0.4, 0.5]   # ค่าเผื่อที่ทดสอบ (diametral)
PIN_D = 5.0          # หมุด/เพลาทดสอบ
PIN_H = 10.0         # ความยาวส่วนที่สวม
PITCH = 12.5         # ระยะห่างช่อง
LABEL_W = 13.0       # แถบป้ายแถวด้านซ้าย
LABEL_H = 8.0        # แถบป้ายคอลัมน์ด้านบน
ROW_PITCH = 12.0
EDGE = 3.0           # ขอบขวา/ล่าง
THICK = 5.0          # ความหนาแผ่น
TEXT_SIZE = 4.5
TEXT_DEPTH = 0.6     # 3 ชั้น
ROWS = ["S", "M3", "M4"]

W = LABEL_W + PITCH * len(CLEARANCES) + EDGE
H = LABEL_H + ROW_PITCH * len(ROWS) + EDGE


def col_x(i):
    return LABEL_W + PITCH * (i + 0.5)


def row_y(j):  # แถว 0 อยู่บนสุด
    return H - LABEL_H - ROW_PITCH * (j + 0.5)


def build_plate():
    with BuildPart() as plate:
        Box(W, H, THICK, align=(Align.MIN, Align.MIN, Align.MIN))
        # ลบมุมขอบล่างกันขอบบาน + มุมบนขวาเป็นเครื่องหมายทิศ
        chamfer(plate.edges().filter_by(Axis.Z).sort_by(Axis.X)[-2:].sort_by(Axis.Y)[-1], 3.0)
        chamfer(plate.edges().group_by(Axis.Z)[0], P.ELEPHANT_FOOT_CHAMFER)

        for i, c in enumerate(CLEARANCES):
            x = col_x(i)
            # แถว S: รูเพลาทะลุ
            with Locations((x, row_y(0), THICK / 2)):
                Cylinder((PIN_D + c) / 2, THICK, mode=Mode.SUBTRACT)
            # แถว M3/M4: ช่องน็อตหกเหลี่ยมจากด้านบน + รูสกรูผ่าน
            for j, size in ((1, "M3"), (2, "M4")):
                af = P.SCREWS[size]["nut_af"] + c
                depth = P.nut_depth(size)
                with BuildSketch(Plane.XY.offset(THICK - depth)):
                    with Locations((x, row_y(j))):
                        RegularPolygon(af / 2, 6, major_radius=False)
                extrude(amount=depth, mode=Mode.SUBTRACT)
                with Locations((x, row_y(j), THICK / 2)):
                    Cylinder(P.screw_clear(size) / 2, THICK, mode=Mode.SUBTRACT)

        # ลบมุมปากรูเพลาบน-ล่าง (สวมง่าย / กันขอบบานชั้นแรก)
        holes = plate.edges().filter_by(lambda e: e.geom_type.name == "CIRCLE")
        bottom = [e for e in holes if e.center().Z < 0.01 and abs(e.center().Y - row_y(0)) < 0.1]
        top = [e for e in holes if e.center().Z > THICK - 0.01 and abs(e.center().Y - row_y(0)) < 0.1]
        chamfer(bottom, P.ELEPHANT_FOOT_CHAMFER)
        chamfer(top, P.TOP_CHAMFER)

        # ป้ายบอกค่า (จมลง)
        with BuildSketch(Plane.XY.offset(THICK)):
            for i, c in enumerate(CLEARANCES):
                with Locations((col_x(i), H - LABEL_H / 2 - 0.3)):
                    Text(f".{int(round(c * 10))}", TEXT_SIZE, font_style=FontStyle.BOLD)
            for j, name in enumerate(ROWS):
                with Locations((LABEL_W / 2 + 0.3, row_y(j))):
                    Text(name, TEXT_SIZE, font_style=FontStyle.BOLD)
        extrude(amount=-TEXT_DEPTH, mode=Mode.SUBTRACT)
    return plate.part


def build_pin():
    tab_l, tab_w, tab_t = 16.0, 10.0, 2.4
    with BuildPart() as pin:
        Box(tab_l, tab_w, tab_t, align=(Align.MIN, Align.MIN, Align.MIN))
        chamfer(pin.edges().group_by(Axis.Z)[0], P.ELEPHANT_FOOT_CHAMFER)
        with Locations((tab_w / 2, tab_w / 2, tab_t)):
            Cylinder(PIN_D / 2, PIN_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        chamfer(pin.edges().group_by(Axis.Z)[-1], 0.5)
        with BuildSketch(Plane.XY.offset(tab_t)):
            with Locations((tab_w + 3.0, tab_w / 2)):
                Text(f"{PIN_D:g}", 4.0, font_style=FontStyle.BOLD)
        extrude(amount=-0.4, mode=Mode.SUBTRACT)
    return pin.part


if __name__ == "__main__":
    plate = build_plate()
    pin = build_pin()
    pin = pin.translate((0, -12.0 - 4.0, 0))  # วางหมุดใต้แผ่น บนฐานพิมพ์เดียวกัน
    for k, s in (("plate", plate), ("pin", pin)):
        bb = s.bounding_box()
        print(f"{k}: {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} มม. · "
              f"ปริมาตร {s.volume / 1000:.2f} cm³ · valid={s.is_valid}")
    files = export_part("clearance_test", {"plate": plate, "pin": pin})
    for f in files:
        print("→", f.relative_to(Path(__file__).resolve().parents[2]))

"""ชิ้นทดสอบแผ่นบังหน้า (visor coupon) — หาวัสดุโปร่งแสงที่พิมพ์เองได้บน X2D

22 พ.ย. 2569 00:36: "หาวัสดุโปร่งแสงที่พิมพ์เองได้ เวลาขายจริงจะได้ผลิตเองทั้งหมด"
→ แผ่นบังพิมพ์เองแทนแผ่นอะคริลิกจากร้าน

แผ่นเดียว: กรอบหนา FRAME_T + 4 ช่องหน้าต่างบางตามค่าใน WINDOWS (มม.)
ทุกช่องพิมพ์เป็นพื้นแผ่นเดียวติดฐานพิมพ์ (ผิวด้านฐานจะเรียบ/ใสที่สุด = ด้านนอกของหน้า)
ตัวเลขนูนบนกรอบบอกความหนา

วัสดุที่จะลอง (ชิ้นละ 1 แผ่น):
  1. Bambu PC สี Clear Black — สีควันในตัว ทนกระแทก/ร้อน · X2D มีห้องอุ่น · อบเส้น 80 °C 8 ชม.
     หัว 250–270 °C · ฐาน 90–110 °C + กาว · ความชื้นกล่อง < 20%
  2. Bambu PETG Translucent สี Gray — พิมพ์ง่ายกว่า ถูกกว่า · หัว 230–260 °C · ฐาน 65–75 °C
ค่าสไลซ์ (ทั้งคู่): ชั้น 0.2 · พื้นล่าง/บน = ทั้งความหนา (infill 100% แบบ aligned rectilinear ทิศเดียว)
  · flow 1.05–1.10 · พัดลมต่ำ · ช้า (≤ 60 mm/s ช่องบาง) · ปิด ironing ด้านฐาน

วิธีอ่านผล: วางแผ่นห่างแผง LED 3 / 6 / 10 มม. ในห้องมืดและห้องสว่าง
  เลือกช่องที่ (ก) ตอนไฟดับมองไม่เห็นของข้างใน (ข) ตอนไฟติดเห็นรูปตาคม ไม่ฟุ้งจนเป็นก้อน
  → บันทึก วัสดุ + ความหนา + ระยะ LED ใน README หัวข้อหน้าตา

รัน:  python3 cad/tests/visor_coupon.py   → cad/out/visor_coupon.{step,3mf,png}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build123d import Align, Box, BuildPart, BuildSketch, FontStyle, Locations, Mode, Plane, Text, extrude

import params as P
from tools.export import export_part

# ---------------------------------------------------------------- พารามิเตอร์ (แก้ได้)
WINDOWS = [0.6, 0.8, 1.2, 1.6]   # ความหนาช่อง (มม.) — ผนังบางสุด 0.6 = 3 ชั้น
WIN_W, WIN_H = 22.0, 30.0        # ขนาดช่อง
GAP = 4.0                        # กรอบระหว่างช่อง
MARGIN = 5.0                     # ขอบรอบนอก
LABEL_BAND = 8.0                 # แถบตัวเลขด้านล่าง
FRAME_T = 3.0                    # ความหนากรอบ
TEXT_SIZE = 5.0
TEXT_H = 0.6                     # ตัวเลขนูน

PLATE_W = MARGIN * 2 + WIN_W * len(WINDOWS) + GAP * (len(WINDOWS) - 1)
PLATE_H = MARGIN * 2 + WIN_H + LABEL_BAND


def win_x(i):
    return -PLATE_W / 2 + MARGIN + WIN_W / 2 + i * (WIN_W + GAP)


WIN_Y = PLATE_H / 2 - MARGIN - WIN_H / 2
LABEL_Y = -PLATE_H / 2 + MARGIN + LABEL_BAND / 2 - 1.0


def build_coupon():
    with BuildPart() as coupon:
        Box(PLATE_W, PLATE_H, FRAME_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # เจาะช่องจากด้านบน เหลือพื้นบางตามความหนาที่ต้องการ (ผิวล่าง = ติดฐานพิมพ์)
        for i, t in enumerate(WINDOWS):
            with Locations((win_x(i), WIN_Y, t)):
                Box(WIN_W, WIN_H, FRAME_T, align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT)
        # ตัวเลขความหนา
        with BuildSketch(Plane.XY.offset(FRAME_T)):
            for i, t in enumerate(WINDOWS):
                with Locations((win_x(i), LABEL_Y)):
                    Text(f"{t:g}", TEXT_SIZE, font_style=FontStyle.BOLD)
        extrude(amount=TEXT_H)
    return coupon.part


if __name__ == "__main__":
    part = build_coupon()
    files = export_part("visor_coupon", {"coupon": part})
    print(f"plate {PLATE_W:.0f} x {PLATE_H:.0f} mm · windows {WINDOWS}")
    for f in files:
        print(f)

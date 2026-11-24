"""เท้าล้อ v1.1 ทรงแคบ — หามุมเอียงขาทรง A ที่น้อยที่สุดที่มุมล้มด้านข้าง ≥ 18° · KOOL 24 พ.ย. 2569
โจทย์: ขาทรง A แต่เอียงน้อยกว่า 9°

แบบจำลอง (มุมหน้า · หน่วย มม.):
  - สะโพก y ±105 z 705 · ข้อเท้า (หัวซ็อกเก็ต) z 209 → ข้อเท้า y = 105 + 496·tan(θ)
  - กลไกเท้าเดิมของ v1 (cad/show_v1/wheel_foot_v1.py) เลื่อนตามข้อเท้าทั้งชุด: ศูนย์ยาง = ข้อเท้า + 113 ·
    ล้อหมุนตาม ⌀100 = ข้อเท้า + 53 · จุดแตะพื้นล้อหมุนตาม x −160 (ถอยหลัง) ถึง −236 (เดินหน้า)
  - ล้อขับแตะพื้นที่ x +160 · จุดศูนย์ถ่วงตกที่ x = 0 (เหนือข้อเท้า) ±20 · สูง 0.51 ม. (แบตในต้นขา) +0.01 เผื่อ
  - มุมล้มด้านข้าง = มุมที่ต้องเอียงให้จุดศูนย์ถ่วงพ้นขอบฐาน (เส้นล้อขับ→ล้อหมุนตาม ด้านนอก)
"""
import math

HIP_Y, HIP_Z, ANK_Z = 105.0, 705.0, 209.0
OFF_WHEEL = 113.0
OFF_CAST = 53.0
DRIVE_X, CAST_XS = 160.0, (-160.0, -236.0)
COM_Z = 520.0
COM_XS = (-20.0, 0.0, 20.0)
NEED = 18.0


def edge_dist(p, a, b):
    """ระยะจากจุด p ถึงเส้น a→b (ด้านใน = บวก)"""
    (px, py), (ax, ay), (bx, by) = p, a, b
    return abs((bx - ax) * (ay - py) - (ax - px) * (by - ay)) / math.hypot(bx - ax, by - ay)


def side_tip(theta_deg):
    ank = HIP_Y + (HIP_Z - ANK_Z) * math.tan(math.radians(theta_deg))
    wheel = ank + OFF_WHEEL
    worst = 90.0
    for cx in CAST_XS:
        for mx in COM_XS:
            d = edge_dist((mx, 0.0), (DRIVE_X, wheel), (cx, ank + OFF_CAST))
            worst = min(worst, math.degrees(math.atan(d / COM_Z)))
    return ank, wheel, worst


if __name__ == "__main__":
    print(f"ศูนย์ยาง = ข้อเท้า + {OFF_WHEEL:.1f} · จุดศูนย์ถ่วง {COM_Z/1000:.2f} ม. · ต้องการ ≥ {NEED}°")
    print("เอียง° | ข้อเท้า y | ศูนย์ยาง y | กว้างนอก-นอก | ล้มข้างแย่สุด")
    best = None
    for t10 in range(0, 91, 5):
        t = t10 / 10
        ank, wheel, tip = side_tip(t)
        mark = "✅" if tip >= NEED else "❌"
        print(f"{t:5.1f} | {ank:7.0f} | {wheel:8.0f} | {2*(wheel+19):9.0f} | {tip:5.1f}° {mark}")
        if best is None and tip >= NEED:
            best = t
    print(f"มุมน้อยสุดที่ผ่าน ≥{NEED}° (ทีละ 0.5°): {best}°")

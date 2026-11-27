# hardware/ — แบบฮาร์ดแวร์ (CERN-OHL-S-2.0)

สคริปต์ CAD เขียนด้วย Python ([build123d](https://github.com/gumyr/build123d) รุ่นเก่า · trimesh + manifold3d รุ่น V1) · รันแล้วได้ไฟล์ใน `hardware/cad/out/`

| สคริปต์ | สร้างอะไร | ไฟล์ที่ได้ |
|---|---|---|
| `cad/show_v1/foot_v1.py` | **เท้าล้อ V1** (ปัจจุบัน): 2 ล้อขับ/เท้า · คานกระดก ±10° · ข้อเท้ายุบ 25 มม. · ดรัม/ฝาปุ่มข้อเท้า · ปลอกกันฝุ่น TPU 2 ชั้น · รายงานความแข็งแรง + เช็กชน | `show_v1_foot1_*.stl` · `_คาน_Al6.dxf` (สำรอง) · `_report.txt` · `_preview.png` |
| (STL) กล่องจออก 8" บานพับขอบบน (แบบจอ X2D) | กรอบหน้า · ฝาหลัง (หล่อข้อบานพับในตัว) · บานพับอก · แผ่นรองใน · ยางกันชน TPU ×2 | `show_v1_chest_tilt_*.stl` |
| `cad/show_v1/wheel_foot_v1.py` (แบบเก่า) | เท้าล้อหุ่นโชว์ v1: แผ่นอะลูมิเนียม 3 ชิ้น · สปริง 2 ชุด/เท้า · สลักล็อก · ซ็อกเก็ตขาถอดเร็ว · รายงานเช็กชน/น้ำหนัก/มุมล้ม | `show_v1_wheel_foot_*.dxf` (ตัดเลเซอร์) · `.step` · `_socket.step` (งานกลึง) · `_report.txt` |
| `cad/show_v1/chest_screen.py` (แบบเก่า) | กรอบจอ 7" ติดตาย (เลิกใช้ → กล่อง 8" ก้ม-เงย) | `chest_screen_pi7_{bezel,back}.{step,stl}` |
| `cad/show_v1/foot_module_sketch.py` | ภาพร่างโมดูลเท้า | `show_v1_foot_module_sketch.png` |
| `cad/kbot/wheel_foot.py` | เท้าล้อ v0 (แบบเก่า เก็บไว้อ้างอิง) | `kbot_wheel_foot_*` |
| `cad/params.py` | ค่าเผื่อรู/เพลาของเครื่อง X2D (ใช้ร่วมทุกชิ้น) | — |

- ค่าตั้งพิมพ์: [print-settings.md](print-settings.md)
- ขนาดชิ้นซื้อ (ล้อหมุนตาม SHF10 โซลินอยด์ แบต) **ต้องวัดของจริงก่อนส่งตัดแผ่น** — ดูหัวข้อ VERIFY ในไฟล์ `_report.txt`
- ⚠️ เท้า V1: คานพิมพ์ต้องผ่านการทดสอบแขวนก่อน (ทางสำรอง = แผ่น Al 6 จาก DXF) · ท่อขา/แกน/แผ่นสะโพก ใช้โลหะ ห้ามพิมพ์

**English:** CAD scripts (build123d) and generated STEP/STL/DXF files. Measure the bought parts before cutting plates. Load-bearing foot plates and leg motor clamps must be metal, not printed.

# hardware/ — แบบฮาร์ดแวร์ (CERN-OHL-S-2.0)

สคริปต์ CAD เขียนด้วย [build123d](https://github.com/gumyr/build123d) (Python) · รันแล้วได้ไฟล์ใน `hardware/cad/out/`

| สคริปต์ | สร้างอะไร | ไฟล์ที่ได้ |
|---|---|---|
| `cad/show_v1/wheel_foot_v1.py` | เท้าล้อหุ่นโชว์ v1: แผ่นอะลูมิเนียม 3 ชิ้น · สปริง 2 ชุด/เท้า · สลักล็อก · ซ็อกเก็ตขาถอดเร็ว · รายงานเช็กชน/น้ำหนัก/มุมล้ม | `show_v1_wheel_foot_*.dxf` (ตัดเลเซอร์) · `.step` · `_socket.step` (งานกลึง) · `_report.txt` |
| `cad/show_v1/chest_screen.py` | กรอบจอ 7" + แผ่นหลังยึด Pi 5 (`PANEL=pi7`) | `chest_screen_pi7_{bezel,back}.{step,stl}` |
| `cad/show_v1/foot_module_sketch.py` | ภาพร่างโมดูลเท้า | `show_v1_foot_module_sketch.png` |
| `cad/kbot/wheel_foot.py` | เท้าล้อ v0 (แบบเก่า เก็บไว้อ้างอิง) | `kbot_wheel_foot_*` |
| `cad/params.py` | ค่าเผื่อรู/เพลาของเครื่อง X2D (ใช้ร่วมทุกชิ้น) | — |

- ค่าตั้งพิมพ์: [print-settings.md](print-settings.md)
- ขนาดชิ้นซื้อ (ล้อหมุนตาม SHF10 โซลินอยด์ แบต) **ต้องวัดของจริงก่อนส่งตัดแผ่น** — ดูหัวข้อ VERIFY ในไฟล์ `_report.txt`
- ⚠️ ชิ้นรับแรง (แผ่นฐานเท้า จุดยึดเพลาล้อ ปลอกยึดมอเตอร์ขา) ใช้โลหะ ห้ามพิมพ์

**English:** CAD scripts (build123d) and generated STEP/STL/DXF files. Measure the bought parts before cutting plates. Load-bearing foot plates and leg motor clamps must be metal, not printed.

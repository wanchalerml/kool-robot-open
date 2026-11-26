# สร้างหุ่นโชว์ V1 / Building show V1

> ⚠️ ฉบับร่าง · ยังไม่ทดสอบจริง (ปรับล่าสุด 26 พ.ย. 2569) · ตัวเลขยังเปลี่ยนได้
> อ่าน [SAFETY.md](../../SAFETY.md) ก่อน

## ทิศทาง
**V1 = สวยตามภาพต้นแบบ** (ไม่ยึดสัดส่วน K-Bot) · V2 = แขนขยับได้ · V3 = ทำใหม่ตาม K-Bot ([ROADMAP](../../ROADMAP.md))

## สเปก

| | |
|---|---|
| สูง | 1.40 ม. |
| น้ำหนัก | ~32–38 กก. (ประมาณ) |
| เปลือก | ขึ้นรูปจากโมเดล 3 มิติที่สร้างจากภาพแนวคิด · ผนัง 2.4 มม. · ปุ่มข้อสีเทาแยกชิ้น (ไหล่ ศอก ข้อมือ สะโพก เข่า) + แถบเอวเทา |
| ขา | ท่ออะลูมิเนียม ⌀40 ตรงท่อนเดียว/ข้าง (ไม่มีข้อพับ) |
| แขน/คอ | ข้อฝืด: แผ่นฝืด 1 มม. + น็อต M8 + แหวนจาน 2×3 ตั้งแรงครั้งเดียว → จับดัดท่าได้เลย ไม่ต้องขันลูกบิด · ไหล่ ~15 N·m · ศอก ~4 · ข้อมือ/คอ ~2 |
| เท้า | 2 ล้อขับ hub 4.5"/เท้า (ขับ 4 ล้อ) · คานกระดกทรงกระดูกหมุนรอบข้อเท้า ±10° · ข้อเท้ายุบ 25 มม. (สปริงรอบแกนนำ ⌀10 ×2 + บุชเชิงเส้น) · ยางย่น TPU ปิดช่วงยุบ |
| ตัวขับล้อ | ZLAC8015D ×2 อยู่ในท้อง |
| ไฟ | Li-ion NMC 21700 · 8S2P ต่อขา (~290 Wh/ขา · รวม ~580 Wh) ซ่อนในหน้าแข้งรอบท่อขา 2 ชั้น · 8S เพราะตัวขับล้อรับ 24–48 V · แพ็คซ้าย/ขวาต่อขนานผ่าน ideal diode |
| จอ | จออก 8" 1280×800 สัมผัส ในกล่องก้ม-เงย (เงย +25° / ก้ม −10° · ข้อฝืด M6 + ยางกันชน TPU ×4) · Raspberry Pi 5 อยู่ในอก |
| หน้า | ฝาหน้าดำเต็มหน้า (PC Clear Black) + ตา 1.9" ×2 หลังฝา · จอ 3.5" หลังหัว |
| ยก/ขนย้าย | หูหิ้วที่เอว 2 ข้าง (ยก 2 คน) + จุดห่วง M8 บนโครง (กำลังออกแบบ) |
| นำทาง/ปลอดภัย | ToF ×4 ปลายเท้า · ไมโครสวิตช์กันชน ×8 ที่ฝาครอบล้อ (ตัดไฟล้อ) · IMU + encoder ล้อ → ROS 2 / Nav2 · จอยบลูทูธให้คนขับแทน · จำกัด ≤ 0.5 ม./วิ ใกล้คน · มีแผนกลับแท่นชาร์จเอง (กำลังเลือกวิธี) |

## วัสดุพิมพ์
ดู [bom/show-v1.md](../../bom/show-v1.md) และ [print-settings](../../hardware/print-settings.md) · หลัก: แข็งตึง+ใกล้มอเตอร์ร้อน = **PPA-CF** · โดนกระแทก/ล้มชน = **PAHT-CF** · โครงในทั่วไป = PETG-CF · เปลือก = PLA ขาวด้าน · ปุ่มข้อ = PETG เทา

## CAD ที่เปิดแล้ว
- เท้าล้อ V1: `python3 hardware/cad/show_v1/foot_v1.py` → STL ทุกชิ้น + DXF (สำรองแบบแผ่น Al 6) + รายงานความแข็งแรง/เช็กชน · ⚠️ คานเท้าพิมพ์ต้องพิมพ์ชิ้นทดสอบแขวน ~70 กก. 24 ชม. วัดการยุบก่อนใช้จริง
- กล่องจออก 8" ก้ม-เงย: `hardware/cad/out/show_v1_chest_tilt_*.stl` (สคริปต์ต้องใช้ไฟล์เปลือกอกที่ยังไม่เปิด)

## ระบบเสียง

```
ไมค์ → Speech-to-Text (th-TH) → LLM → Text-to-Speech (เสียงไทย) → ลำโพง
```

- สลับผู้ให้บริการเสียงได้ + แคชเสียงประโยคที่พูดซ้ำ (อัดบท/คำถามที่พบบ่อยไว้ล่วงหน้า)
- ไม่เก็บไฟล์เสียง · ใช้ key ของบัญชีตัวเอง เก็บในไฟล์ `.env` ห้าม commit
- ผู้ใช้งานต้องติดป้ายแจ้งความเป็นส่วนตัวเอง (PDPA หรือกฎหมายในประเทศนั้น) — ดูแม่แบบ `software/ui/pdpa_sign/`

---

**English summary:** Show V1 is a 1.40 m humanoid that copies the concept art (shells generated from a 3D model of the concept, grey joint covers). Legs are straight Ø40 aluminium tubes; arm and neck joints are hand-posable friction joints (pad + M8 + Belleville stack). Each foot has two 4.5" hub wheels (4WD) on a ±10° rocking beam with 25 mm spring travel at the ankle; the two wheel drivers sit in the belly. Power is 8S2P 21700 Li-ion per leg (~580 Wh total) hidden around the shin tube. A tilting 8" touchscreen sits on the chest, a black PC face with two 1.9" eye screens on the head. Safety: 4 ToF sensors, 8 bumper switches cutting wheel power, IMU + wheel odometry for ROS 2/Nav2, Bluetooth joystick override, ≤0.5 m/s near people. Draft — nothing tested yet.

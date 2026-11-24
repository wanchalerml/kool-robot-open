# ความปลอดภัย / Safety

หุ่นนี้หนักราว **30–32 กก.** (ประมาณ) มี**ล้อขับไฟฟ้า**และ**แบตเตอรี่ลิเธียม** ถ้าสร้างหรือใช้ผิดวิธีอาจทำให้คนบาดเจ็บหรือทรัพย์สินเสียหายได้

แบบนี้ให้มา**โดยไม่มีการรับประกันใดๆ** (ดูไฟล์สัญญาอนุญาต) ผู้สร้างและผู้ใช้งานต้องรับผิดชอบความปลอดภัยเอง

## ต้องมีก่อนเปิดล้อครั้งแรก

- [ ] **ปุ่มหยุดฉุกเฉินแบบตัดไฟจริง** อยู่ที่หลังหุ่น — ต้องตัดไฟล้อด้วยรีเลย์ ไม่ใช่แค่สั่งผ่านซอฟต์แวร์
- [ ] ปุ่มหยุดบนแอปบังคับ และหยุดเองเมื่อสัญญาณหายเกิน 0.5 วิ
- [ ] จำกัดความเร็ว **≤ 0.5 ม./วิ** ในเฟิร์มแวร์
- [ ] ล้อมีเบรกไฟฟ้าที่ล็อกเองเมื่อไฟดับ
- [ ] ฟิวส์ที่สายแบตทุกก้อน
- [ ] ทดสอบเอียงทุกทิศ 15° และดันข้างก่อนพาเข้าใกล้คน

## แบตเตอรี่ LiFePO4

- ใช้แบตที่มี BMS และที่ชาร์จสำหรับ LiFePO4 เท่านั้น
- ห้ามชาร์จทิ้งไว้โดยไม่มีคนดู
- ห้ามใช้แบตที่บวม หรือที่เคยตกกระแทกแรง

## ในงานที่มีคน

- มีผู้ควบคุม 1 คนอยู่ใกล้หุ่นตลอดเวลา
- กันระยะเด็กเล็กจากล้อ
- ห้ามให้คนขึ้นนั่งหรือห้อยตัวกับหุ่น
- **เสียง/ข้อมูลส่วนบุคคล:** หุ่นส่งเสียงคนไปประมวลผลบนคลาวด์
  - ผู้ที่นำหุ่นไปใช้เป็น**ผู้ควบคุมข้อมูล**ตามกฎหมายของประเทศนั้น (ในไทยคือ PDPA)
  - ต้องติดป้ายแจ้งเอง — ดูแม่แบบที่ `software/ui/pdpa_sign/`

---

**English summary:** This is a 25 kg robot with electric drive wheels and lithium batteries. It is provided without warranty, and you are responsible for building and operating it safely.

Before enabling the wheels, you need:
- a hardware e-stop that cuts wheel power through a relay;
- an app stop button, plus auto-stop when the signal is lost for more than 0.5 s;
- a speed limit of 0.5 m/s or less;
- wheels with fail-safe brakes;
- fused batteries;
- a 15° tilt test in every direction.

At events:
- keep a person next to the robot at all times;
- no riding on or hanging from the robot.

Whoever operates the robot is the data controller for the voice data it sends to the cloud, and must put up a privacy notice.

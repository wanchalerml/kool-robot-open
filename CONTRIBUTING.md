# ร่วมพัฒนา KOOL Robot / Contributing

ขอบคุณที่สนใจครับ 🙏

## ช่วยได้หลายแบบ (ไม่ต้องเขียนโค้ด)

- 🖨️ **พิมพ์ทดสอบ** ชิ้นส่วน แล้วรายงานผล: เครื่อง เส้น ค่าที่ใช้ ภาพ ชิ้นที่พอดีหรือไม่พอดี
- 🌐 **แปล**เอกสาร ไทย ↔ อังกฤษ
- 🛒 **แนะนำร้าน**อะไหล่ในไทยหรือในภูมิภาค พร้อมราคา
- 🧪 **ตรวจตัวเลข** เช่น มุมล้ม น้ำหนัก แรงบิด แบต
- 💻 **โค้ด** เช่น ซอฟต์แวร์เสียง หน้าจอ เฟิร์มแวร์ล้อ ซิม
- 📸 **"ฉันสร้างแล้ว"** — โชว์ผลงานได้ที่ issue แบบ *I built one*

เริ่มจาก issue ที่ติดป้าย **good first issue**

## ขั้นตอนส่ง Pull Request

1. Fork → สร้าง branch → แก้ไข
2. **ทุก commit ต้องมี `Signed-off-by`** (DCO): ใช้คำสั่ง `git commit -s`
   - เป็นการยืนยันว่าคุณมีสิทธิ์ส่งงานนี้ ตาม [Developer Certificate of Origin 1.1](https://developercertificate.org/)
3. อธิบายใน PR ว่าแก้อะไร ทดสอบอย่างไร ถ้าเป็นชิ้นส่วนให้แนบภาพ
4. งานที่ส่งเข้ามาจะอยู่ภายใต้สัญญาอนุญาตของส่วนนั้นๆ:
   - ฮาร์ดแวร์: CERN-OHL-S-2.0
   - โค้ด: Apache-2.0
   - เอกสาร: CC BY-SA 4.0

## กติกา

- ห้ามใส่ไฟล์ที่ไม่มีสิทธิ์เผยแพร่ เช่น ไฟล์ CAD ของบริษัทอื่นที่ไม่มีสัญญาอนุญาต
- ห้ามใส่ API key หรือรหัสผ่าน ใช้ไฟล์ `.env` ที่ไม่ถูก commit
- งานที่เกี่ยวกับ**ไฟฟ้า แบต ล้อ หรือปุ่มหยุด** จะถูกรีวิวละเอียดเป็นพิเศษ (ดู [SAFETY.md](SAFETY.md))
- ใช้ภาษาไทยหรืออังกฤษได้ทั้งคู่
- ทุกคนต้องปฏิบัติตาม [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

**English summary:** All kinds of help are welcome: test prints, translation, parts sourcing, checking numbers, code, and "I built one" reports.

How to contribute:
1. Fork, branch, and send a pull request.
2. Sign off every commit (`git commit -s`, DCO 1.1).
3. Your contribution is licensed under that area's licence: hardware CERN-OHL-S-2.0, code Apache-2.0, docs CC BY-SA 4.0.

Rules:
- No unlicensed third-party files and no secrets.
- Changes to power, battery, wheel or e-stop work get extra review.

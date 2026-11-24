# software/ — ซอฟต์แวร์ (Apache-2.0)

| โฟลเดอร์ | มีอะไร | สถานะ |
|---|---|---|
| `show/profiles/` | ไฟล์ตั้งค่าต่องาน: บทพูด บุคลิก แบรนด์ QR คำตอบออฟไลน์ ปุ่มทีมงาน ท่า โหมดตา ค่าความเป็นส่วนตัว · ตัวอย่าง `ev-showroom.yaml` | ✅ ฉบับร่าง |
| `ui/chest_screen/` | ภาพร่างหน้าจออก 3 โหมด (คุย / QR / สไลด์) | ✅ ฉบับร่าง |
| `ui/pdpa_sign/` | แม่แบบป้ายแจ้งความเป็นส่วนตัว | ✅ |
| voice (Pi 5) | กดพูด → แปลงเสียงไทย → LLM → เสียงไทย · ตาไฟตามสถานะ · โหมดออฟไลน์ | 🔜 |
| wheels (ESP32) | จอยมือถือ · จำกัดความเร็ว · หยุดเมื่อสัญญาณหาย | 🔜 |

## Key และความลับ
- ไม่มี key ใน repo นี้ · คัดลอก `.env.example` เป็น `.env` แล้วใส่ key ของบัญชีคุณเอง · `.env` ถูก ignore แล้ว
- ห้าม commit รหัส Wi-Fi, token, หรือไฟล์เสียง/รูปผู้เข้าชม

## ความเป็นส่วนตัว (ค่าเริ่มต้น)
กดเพื่อพูด · ไม่เก็บไฟล์เสียง · ไม่จดจำใบหน้า/เสียง · โหมดเด็ก · ผู้นำหุ่นไปใช้ต้องติดป้ายแจ้งเอง

**English:** Event profiles, chest-screen mockups and the privacy sign template. No keys are stored here — copy `.env.example` to `.env` with your own accounts. Defaults: push-to-talk, no audio storage, no face/voice recognition, kids mode.

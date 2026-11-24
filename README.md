# KOOL Robot — open-source Thai-speaking show humanoid 🇹🇭

> ⚠️ **กำลังพัฒนา / Work in progress.** ยังไม่มีตัวจริงที่ประกอบเสร็จ แบบและตัวเลขยังเปลี่ยนได้
> No assembled robot yet — designs and numbers still change.

![concept (AI-generated render, not a photo)](docs/images/concept_gemini_r3.jpg)
*ภาพแนวคิดจาก AI ไม่ใช่ภาพถ่าย · AI-generated concept render, not a photo (the person is also AI-generated).*

## นี่คืออะไร

หุ่นยนต์ร่างคนสูง **1.40 ม.** สำหรับงานโชว์ งานอีเวนต์ และบูธ

- **พูดและฟังภาษาไทยได้**
- **มีล้อที่เท้า** เคลื่อนที่ได้
- **ปรับท่าด้วยมือ** — รุ่นแรก (show v1) ยังไม่มีมอเตอร์ข้อต่อ ข้อต่อล็อกด้วยกลไก
- **จอสัมผัสที่หน้าอก** สำหรับคำบรรยายสด QR และสไลด์
- สัดส่วนอิงจากแบบเปิด **K-Bot** ของ K-Scale Labs (CERN-OHL-S / MIT)
- งบชิ้นส่วนรุ่น show v1 ประมาณ **฿53,000–75,000** (ราคาประมาณ · พฤศจิกายน 2569)

**English:** A 1.40 m open-source show humanoid for events. It speaks and listens in Thai through a cloud speech service and an LLM. It has drive wheels in its feet and hand-posable locking joints (no joint motors in v1), plus a 7" chest touchscreen. Proportions follow the open K-Bot design by K-Scale Labs. The v1 parts budget is about THB 53–75k.

## สถานะ / Status

| ส่วน | สถานะ |
|---|---|
| ระบบมุมล้มและสัดส่วน (`sim/kbot`) | ✅ คำนวณแล้ว — ล้มข้าง 23.9° · ล้มหน้า-หลัง 17.9° · พื้นที่ใช้งาน + โช้คเท้า (`show_v1_terrain.py`) |
| กรอบจอหน้าอก (`cad/show_v1`) | ✅ ฉบับร่าง (ยังไม่ได้พิมพ์ทดสอบ) |
| ภาพร่างหน้าจอ (`ui/chest_screen`) | ✅ ฉบับร่าง |
| เท้าล้อ (`cad/kbot/wheel_foot.py`) | 🟡 ร่าง v0 — กำลังแก้เป็นล้อ ±22 ซม. |
| โครง + ข้อต่อล็อกท่า | 🔜 |
| ซอฟต์แวร์เสียงบน Raspberry Pi 5 | 🔜 |
| เปลือก (พิมพ์ 3 มิติ) ตามภาพแนวคิด | 🔜 |

แผนงาน: [ROADMAP.md](ROADMAP.md) · คู่มือสร้างรุ่น show v1: [docs/build/show-v1.md](docs/build/show-v1.md)

## เริ่มใช้งาน / Quick start

```bash
pip install mujoco build123d numpy matplotlib
python3 sim/kbot/show_v1_tip.py          # มุมล้มของรุ่น show v1
python3 sim/kbot/stance.py               # ท่ายืนของโมเดล K-Bot
PANEL=pi7 python3 cad/show_v1/chest_screen.py   # สร้างกรอบจอ 7" → cad/out/
```

ภาพร่างหน้าจอ: เปิดไฟล์ `ui/chest_screen/mock.html` ในเบราว์เซอร์

## ร่วมพัฒนา / Contributing

ยินดีต้อนรับทุกคน ไม่ต้องเขียนโค้ดเป็นก็ช่วยได้ เช่น ทดสอบพิมพ์ แปลภาษา ถ่ายรูป หรือแนะนำร้านอะไหล่

อ่าน [CONTRIBUTING.md](CONTRIBUTING.md) · ถามตอบได้ใน GitHub Discussions · ⚠️ อ่าน [SAFETY.md](SAFETY.md) ก่อนสร้างจริง

## สัญญาอนุญาต / Licences

| ส่วน | สัญญาอนุญาต |
|---|---|
| แบบฮาร์ดแวร์ (`cad/`, STEP/STL, แบบโครงและเท้า) | [CERN-OHL-S-2.0](LICENSES/CERN-OHL-S-2.0.txt) |
| ซอฟต์แวร์ (`sim/`, `ui/`, `tools/`, ระบบเสียง) | [Apache-2.0](LICENSES/Apache-2.0.txt) |
| เอกสารและภาพ (`docs/`, `*.md`, `*.png`, `*.jpg`) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| `third_party/` | ตามสัญญาอนุญาตเดิมของแต่ละโฟลเดอร์ (ดู [NOTICE](NOTICE)) |

ชื่อและโลโก้ "KOOL Robot" ไม่รวมอยู่ในสัญญาอนุญาตข้างต้น ดู [TRADEMARK.md](TRADEMARK.md)

# KOOL Robot — หุ่นยนต์ร่างคนพูดไทย แบบเปิด (open source) 🇹🇭

> ⚠️ **กำลังพัฒนา / Work in progress** — ยังไม่มีหุ่นตัวจริงที่ประกอบเสร็จ · ตอนนี้มีแบบ CAD การคำนวณ และซอฟต์แวร์ฉบับร่าง · ตัวเลขยังเปลี่ยนได้
> No assembled robot yet. What exists today: CAD, calculations and draft software. Numbers may still change.

![concept (AI-generated render, not a photo)](docs/images/concept_gemini_r3.jpg)
*ภาพแนวคิดจาก AI ไม่ใช่ภาพถ่าย (คนในภาพก็สร้างด้วย AI) · AI-generated concept render, not a photo.*
*รูปและคลิปหุ่นจริงจะใส่ตรงนี้เมื่อประกอบเสร็จ · Real photos and video will go here once it is built.*

## หุ่นนี้คืออะไร

หุ่นยนต์ร่างคนสูง **1.40 ม.** สำหรับงานโชว์ อีเวนต์ บูธ และโชว์รูม

- **คุยภาษาไทย** ผ่านไมค์และลำโพง (แปลงเสียงบนคลาวด์ + LLM) · ฟังเฉพาะตอนกดปุ่มพูด
- **ขาเต็มแบบคน + ล้อซ่อนที่เท้า** เคลื่อนที่ได้ (หุ่นแบบนี้ส่วนใหญ่ใช้ฐานล้อแทนขา)
- **หน้ากากดำ + ตาไฟ** ไม่ทำหน้าเหมือนคนจริง · **จอสัมผัส 7" ที่อก** สำหรับคำบรรยาย QR และสไลด์
- **ลุคมอเตอร์โผล่** (ครอบเฉพาะลิงก์) · **ชิ้นส่วนพิมพ์ 3 มิติเองได้**
- สัดส่วนและจุดหมุนอิงจากแบบเปิด **K-Bot** ของ K-Scale Labs (ดู [NOTICE](NOTICE))

**English:** KOOL Robot is a 1.40 m open-source show humanoid for events and showrooms. It talks in Thai through a push-to-talk microphone, cloud speech and an LLM. It has full human-like legs with wheels hidden in the feet, a black visor with light-up eyes and a 7" chest touchscreen. The exposed-motor look is inspired by humanoids like Unitree G1. Body proportions and joint positions follow the open K-Bot design by K-Scale Labs.

## ทำอะไรได้ตอนนี้ (บอกตรง ๆ) / What works today

| ส่วน | สถานะ |
|---|---|
| คำนวณมุมล้ม พื้นที่ใช้งาน สัดส่วน (`sim/`) | ✅ ใช้ได้ |
| CAD เท้าล้อ + โช้ค (DXF/STEP) (`hardware/cad/show_v1/wheel_foot_v1.py`) | ✅ ฉบับร่าง · ยังไม่ได้ตัด/ประกอบจริง |
| กรอบจอหน้าอก (`hardware/cad/show_v1/chest_screen.py`) | ✅ ฉบับร่าง · ยังไม่ได้พิมพ์ทดสอบ |
| ภาพร่างหน้าจอ + ไฟล์ตั้งค่างาน (`software/`) | ✅ ฉบับร่าง |
| โครง + ข้อต่อล็อกท่า (มอเตอร์หลอกขนาด RobStride) | 🟡 กำลังออกแบบ |
| เปลือก · ซอฟต์แวร์เสียงบน Raspberry Pi 5 · เฟิร์มแวร์ล้อ | 🔜 |
| หุ่นตัวจริง | 🔜 ยังไม่มี |

## แผนต่อไป / Roadmap

| ขั้น | เป้าหมาย | สถานะ |
|---|---|---|
| **① หุ่นโชว์ v1** | พูดไทย · ล้อที่เท้า · ข้อต่อปรับท่าด้วยมือ (ยังไม่มีมอเตอร์ข้อ) · จอ 7" | 🟡 ออกแบบ |
| ② แขน + หัวมีมอเตอร์ | มอเตอร์ RobStride 8 ข้อ (คอ 2 + แขน 3×2) · ถอดมอเตอร์หลอก ใส่ของจริงได้ | 🔜 |
| ③ ขาเดินได้ | K-Bot เต็มชุด 20 ข้อ · งานอีเวนต์ยังใช้ล้อ | 🔜 |

รายละเอียด: [ROADMAP.md](ROADMAP.md) · สเปก: [docs/build/show-v1.md](docs/build/show-v1.md) · บันทึกงานรายสัปดาห์: [devlog/](devlog/)

## โครงโฟลเดอร์ / Repository layout

| โฟลเดอร์ | มีอะไร |
|---|---|
| [`hardware/`](hardware/) | สคริปต์ CAD (build123d) · STEP/STL/DXF ที่สร้างแล้ว · [ค่าตั้งพิมพ์ X2D](hardware/print-settings.md) |
| [`bom/`](bom/) | รายการชิ้นส่วน · จำนวน · แหล่งในไทย/ต่างประเทศ · ราคาโดยประมาณ |
| [`docs/assembly/`](docs/assembly/) | วิธีประกอบทีละขั้นพร้อมรูป |
| [`software/`](software/) | ซอฟต์แวร์พูดคุย หน้าจอ ไฟล์ตั้งค่างาน (ไม่มี key — ใช้ `.env` ของคุณเอง) |
| [`sim/`](sim/) | โมเดลและการคำนวณ (MuJoCo / numpy) |
| [`devlog/`](devlog/) | บันทึกรายสัปดาห์: ลองอะไร · ผ่าน · พัง · ต่อไป |
| `third_party/` | ไฟล์ K-Bot ต้นฉบับ (ไม่แก้) ตามสัญญาอนุญาตเดิม |

## เริ่มลอง / Quick start

```bash
pip install mujoco build123d numpy matplotlib pillow
python3 sim/kbot/show_v1_tip.py                        # มุมล้มของหุ่นโชว์ v1
python3 hardware/cad/show_v1/wheel_foot_v1.py          # สร้างเท้าล้อ → hardware/cad/out/
PANEL=pi7 python3 hardware/cad/show_v1/chest_screen.py # กรอบจอ 7"
```

## อยากช่วย? / How to help

ไม่ต้องเขียนโค้ดเป็นก็ช่วยได้: พิมพ์ทดสอบ · ตรวจตัวเลข · แนะนำร้านอะไหล่ · แปลเอกสาร · เขียนบทพูดภาษาไทย/ภาษาถิ่น

1. ดู issue ที่ติดป้าย [**good first issue**](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) หรือ [**help wanted**](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
2. อ่าน [CONTRIBUTING.md](CONTRIBUTING.md) (ไทย + English)
3. ถาม คุย เสนอไอเดียได้ที่ [**Discussions**](../../discussions)
4. ⚠️ อ่าน [SAFETY.md](SAFETY.md) ก่อนสร้างของจริง

## สัญญาอนุญาต / Licences

| ส่วน | สัญญาอนุญาต |
|---|---|
| แบบฮาร์ดแวร์ (`hardware/`, STEP/STL/DXF) | [CERN-OHL-S-2.0](LICENSE-HW) |
| โค้ด (`software/`, `sim/`, สคริปต์) | [Apache-2.0](LICENSE) |
| เอกสารและภาพ (`docs/`, `devlog/`, `bom/`, `*.md`, ภาพ) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| `third_party/` | ตามไฟล์สัญญาอนุญาตเดิมในแต่ละโฟลเดอร์ (ดู [NOTICE](NOTICE)) |

- ชื่อ "KOOL Robot" ไม่รวมอยู่ในสัญญาอนุญาตเปิด ดู [TRADEMARK.md](TRADEMARK.md)
- ห้ามใช้ชื่อ K-Bot / K-Scale เป็นชื่อสินค้าที่สร้างจากแบบนี้ · Do not use the K-Bot or K-Scale names as product names.

# KOOL Robot — หุ่นยนต์ร่างคนพูดไทย แบบเปิด (open source) 🇹🇭

> ⚠️ **กำลังพัฒนา / Work in progress** — ยังไม่มีหุ่นตัวจริงที่ประกอบเสร็จ · ตอนนี้มีแบบ CAD การคำนวณ และซอฟต์แวร์ฉบับร่าง · ตัวเลขยังเปลี่ยนได้
> No assembled robot yet. What exists today: CAD, calculations and draft software. Numbers may still change.

![concept (AI-generated render, not a photo)](docs/images/concept_gemini_r3.jpg)
*ภาพแนวคิดจาก AI ไม่ใช่ภาพถ่าย (คนในภาพก็สร้างด้วย AI) · AI-generated concept render, not a photo.*
*รูปและคลิปหุ่นจริงจะใส่ตรงนี้เมื่อประกอบเสร็จ · Real photos and video will go here once it is built.*

## หุ่นนี้คืออะไร

หุ่นยนต์ร่างคนสูง **1.40 ม.** สำหรับงานโชว์ อีเวนต์ บูธ และโชว์รูม

- **คุยภาษาไทย** ผ่านไมค์และลำโพง (แปลงเสียงบนคลาวด์ + LLM) · ฟังเฉพาะตอนกดปุ่มพูด
- **ท่อนบนร่างคนบนเท้าล้อ** — เท้าละ 2 ล้อขับ (ขับ 4 ล้อ) + ช่วงล่างสปริง · ขายังไม่เดินในรุ่นแรก
- **หน้าดำเต็มหน้า + ตาไฟ** ไม่ทำหน้าเหมือนคนจริง · **จอสัมผัส 8" ที่อก ก้ม-เงยได้**
- **รุ่นแรก (V1) ทำให้สวยตามภาพต้นแบบ** — เปลือกขึ้นรูปจากโมเดล 3 มิติที่สร้างจากภาพแนวคิด · ปุ่มข้อสีเทา · ข้อแขนปรับท่าด้วยมือ (ข้อฝืด)
- **ชิ้นส่วนพิมพ์ 3 มิติเองได้** · แบต Li-ion 21700 ซ่อนในหน้าแข้ง (จุดศูนย์ถ่วงต่ำ · เติมเพิ่มทีหลังได้)
- รุ่นเดินได้ในอนาคต (V3) จะอิงแบบเปิด **K-Bot** ของ K-Scale Labs (ดู [NOTICE](NOTICE))

**English:** KOOL Robot is a 1.40 m open-source show humanoid for events and showrooms. It talks in Thai through a push-to-talk microphone, cloud speech and an LLM. V1 is a human-like upper body on wheeled feet (two driven wheels per foot with spring suspension), a full black face with light-up eyes and a tilting 8" chest touchscreen. V1 focuses on matching the concept look; arm joints are hand-posable friction joints. A walking version (V3) will follow the open K-Bot design by K-Scale Labs.

## ทำอะไรได้ตอนนี้ (บอกตรง ๆ) / What works today

| ส่วน | สถานะ |
|---|---|
| คำนวณมุมล้ม พื้นที่ใช้งาน สัดส่วน (`sim/`) | ✅ ใช้ได้ |
| CAD เท้าล้อ V1 รอบ 3: 2 ล้อ/เท้า · คานล็อก TPU · สปริงอัดค้าง · ToF + รายงานการทรงตัว (`hardware/cad/show_v1/foot_v1.py`) | ✅ ฉบับร่าง · ยังไม่ทดสอบจริง |
| CAD กล่องจออก 8" ก้ม-เงย (ข้อฝืด + ยางกันชน TPU) | ✅ ฉบับร่าง (STL) · ยังไม่ได้พิมพ์ทดสอบ |
| ภาพร่างหน้าจอ + ไฟล์ตั้งค่างาน (`software/`) | ✅ ฉบับร่าง |
| เปลือก V1 ตามภาพต้นแบบ + ปุ่มข้อเทา + โครงใน | 🟡 กำลังออกแบบ |
| ซอฟต์แวร์เสียงบน Raspberry Pi 5 · เฟิร์มแวร์ล้อ · กลับแท่นชาร์จเอง | 🔜 |
| หุ่นตัวจริง | 🔜 ยังไม่มี |

## แผนต่อไป / Roadmap

| รุ่น | เป้าหมาย | สถานะ |
|---|---|---|
| **V1 หุ่นโชว์** | สวยตามภาพต้นแบบ · พูดไทย · เท้าล้อ 4 ล้อ + สปริง · ข้อแขนปรับท่าด้วยมือ · จอ 8" | 🟡 ออกแบบ |
| V2 แขนขยับได้ | ใส่มอเตอร์จริงที่แขน | 🔜 |
| V3 เดินได้ | ทำใหม่ตามแบบ K-Bot | 🔜 |

รายละเอียด: [ROADMAP.md](ROADMAP.md) · สเปก: [docs/build/show-v1.md](docs/build/show-v1.md) · บันทึกงานรายสัปดาห์: [devlog/](devlog/)

## โครงโฟลเดอร์ / Repository layout

| โฟลเดอร์ | มีอะไร |
|---|---|
| [`hardware/`](hardware/) | สคริปต์ CAD (build123d) · STEP/STL/DXF ที่สร้างแล้ว · [ค่าตั้งพิมพ์ X2D](hardware/print-settings.md) |
| [`bom/`](bom/) | รายการชิ้นส่วนและจำนวน |
| [`docs/assembly/`](docs/assembly/) | วิธีประกอบทีละขั้นพร้อมรูป |
| [`software/`](software/) | ซอฟต์แวร์พูดคุย หน้าจอ ไฟล์ตั้งค่างาน (ไม่มี key — ใช้ `.env` ของคุณเอง) |
| [`sim/`](sim/) | โมเดลและการคำนวณ (MuJoCo / numpy) |
| [`devlog/`](devlog/) | บันทึกรายสัปดาห์: ลองอะไร · ผ่าน · พัง · ต่อไป |
| `third_party/` | ไฟล์ K-Bot ต้นฉบับ (ไม่แก้) ตามสัญญาอนุญาตเดิม |

## เริ่มลอง / Quick start

```bash
pip install mujoco build123d numpy matplotlib pillow
python3 sim/kbot/show_v1_tip.py                        # มุมล้มของหุ่นโชว์ v1
pip install trimesh manifold3d shapely ezdxf
python3 hardware/cad/show_v1/foot_v1.py                # เท้าล้อ V1 → hardware/cad/out/show_v1_foot1_*
```

## อยากช่วย? / How to help

ไม่ต้องเขียนโค้ดเป็นก็ช่วยได้: พิมพ์ทดสอบ · ตรวจตัวเลข · แนะนำอะไหล่ทดแทน · แปลเอกสาร · เขียนบทพูดภาษาไทย/ภาษาถิ่น

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

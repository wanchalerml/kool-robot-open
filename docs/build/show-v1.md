# สร้างหุ่นโชว์ v1 / Building show v1

> ⚠️ ฉบับร่าง (พฤศจิกายน 2569)
> - ราคาเป็น**ค่าประมาณ** เป็นเงินบาท ยังไม่ใช่ใบเสนอราคา
> - อ่าน [SAFETY.md](../../SAFETY.md) ก่อน

## สเปก

| | |
|---|---|
| สูง | 1.40 ม. (สัดส่วนตาม K-Bot) |
| น้ำหนัก | ~30–32 กก. (รวมเท้าล้อมีโช้ค) |
| จุดศูนย์ถ่วง | ~0.50 ม. (แบตและล้ออยู่ในเท้า) |
| ล้อ | เท้าละ 1 ล้อขับ (hub 5" มีเบรกไฟฟ้า ติดด้านนอกเท้า **±22 ซม.** จากกลางตัว) + 1 ล้อหมุนตามด้านหลัง |
| ระยะล้อหน้า-หลัง | 32 ซม. |
| มุมล้ม | ด้านข้าง **23.9°** · หน้า-หลัง **17.9°** (`sim/kbot/show_v1_tip.py`, `show_v1_terrain.py`) |
| โช้คเท้า | เท้าละ 2 ชุดสปริงแม่พิมพ์ Ø20×64 (19.6 N/mm) ยุบได้สูงสุด 12 มม. + สลักล็อกตอนจอด · ยุบสุดแล้วยังล้มข้างที่ ≥22.4° หน้า-หลัง ≥15.7° |
| โมดูลเท้า | ถอดเปลี่ยนได้: น็อต M6 ×4 + หมุด ×2 + XT60 + ขั้วสัญญาณ 6 ขา |
| ความเร็ว | จำกัด 0.5 ม./วิ · หยุดใน 0.5 วิ เทียบเท่าการเอียง ~5.8° |
| ข้อต่อ | ไม่มีมอเตอร์ · ขา: สลัก + แคลมป์ · แขนและคอ: จานฟันเฟือง Hirth + ลูกบิด M8 → **ไฟดับก็ยังยืนได้** |
| สมอง | Raspberry Pi 5 + ไมค์อาร์เรย์ + ลำโพง + ตาไฟ LED + จอสัมผัส 7" |
| บังคับล้อ | เว็บแอปบนมือถือ → Wi-Fi → ESP32 → ตัวขับล้อ |

## BOM

ย้ายไปที่ [bom/show-v1.md](../../bom/show-v1.md) (แหล่งไทย/ต่างประเทศ + ราคาประมาณ) · วิธีประกอบ: [docs/assembly/show-v1.md](../assembly/show-v1.md)

## พิมพ์ 3 มิติ

- **พิมพ์ได้:**
  - เปลือก (PLA ขาว)
  - หัวและหน้ากาก (PETG ดำ)
  - กรอบจอ (`hardware/cad/show_v1/chest_screen.py`, PETG/ASA)
  - จาน Hirth และตัวเรือนข้อแขน/คอ (PA-CF)
  - มือ (ท่าคงที่ เปลี่ยนเป็นชิ้นสวมได้)
- **ห้ามพิมพ์:**
  - ท่อขาและสันหลัง
  - แผ่นสะโพก
  - ข้อพับสะโพกและเข่า
  - **แผ่นฐานเท้า + จุดยึดเพลาล้อ** (อะลูมิเนียม 5 มม.)
  - ตัวยึดแบต (ต้องเป็นโลหะ)
- เวลาพิมพ์รวม ~80–120 ชม. (เตียง 256 มม.)

## จอหน้าอก

- **กรอบ:** `PANEL=pi7 PANEL_T=<ความหนาที่วัดจริง> python3 hardware/cad/show_v1/chest_screen.py`
  - ⚠️ ความหนาจอ 14 มม. ในไฟล์เป็นค่าสมมติ ต้องวัดจอจริงก่อนพิมพ์
- **ระบายความร้อน:** เว้นช่องลม 8 มม. หลังจอ · ลมเข้าด้านล่าง ออกด้านบน · Pi ควรไม่เกิน ~75 °C หลังเปิด 2 ชม.
- **หน้าจอ 3 โหมด** (ภาพร่าง `software/ui/chest_screen/mock.html`):
  - คุย: คำบรรยายสด + สถานะ + ปุ่มปิดไมค์
  - QR
  - สไลด์

## ไฟและแบต

แบต 2 × 24V 10Ah ≈ 512 Wh (ใช้จริง ~410 Wh)

| สถานการณ์ | โหลดเฉลี่ย | อยู่ได้ |
|---|---|---|
| งานบูธปกติ | ~33 W | ~12 ชม. |
| เคลื่อนที่เยอะ | ~60 W | ~7 ชม. |

## พื้นที่ใช้งาน (รุ่นแรก)

| สภาพพื้น | ผล |
|---|---|
| พื้นห้าง / กระเบื้อง / ไม้ / พรมบาง / ลานปูนเรียบ | ✅ |
| ขอบตั้งฉาก | ≤ 1 ซม. |
| รางสายไฟมีเนิน / แผ่นลาด | ≤ 2.5–3 ซม. (ขับช้า) |
| ทางลาด 5° | ได้ — จำกัด 0.3 ม./วิ และเบรก ≤ 0.5 ม./วิ² |
| เอียงข้าง (ขับ) | ห้าม |
| หญ้า / กรวด / ทราย / บันได | ❌ |

ภาพร่างโมดูลเท้า: `hardware/cad/out/show_v1_foot_module_sketch.png`

**CAD เท้าล้อ v1:** `python3 hardware/cad/show_v1/wheel_foot_v1.py` → DXF แผ่นอะลูมิเนียม (ล่าง 5 มม. · บน 6 มม. · หางปลา 8 มม.) + STEP ซ็อกเก็ตขา (งานกลึง) + รายงานเช็กชน/น้ำหนัก/มุมล้ม `hardware/cad/out/show_v1_wheel_foot_report.txt` · ฐานล้อ 32 ซม. นับถึงจุดแตะพื้นล้อหมุนตามตอนถอยหลัง (แย่สุด) · วัดล้อหมุนตาม/SHF10/โซลินอยด์จริงก่อนส่งตัด

## ระบบเสียง

```
ไมค์ → Azure Speech-to-Text (th-TH) → LLM → Azure Text-to-Speech (เสียงไทย Neural) → ลำโพง
```

- ไม่เก็บไฟล์เสียง และไม่มีกล้อง
- ใช้ key ของบัญชีตัวเอง เก็บในไฟล์ `.env` ห้าม commit
- ผู้ใช้งานต้องติดป้ายแจ้งความเป็นส่วนตัวเอง (PDPA หรือกฎหมายในประเทศนั้น) — ดูแม่แบบ `software/ui/pdpa_sign/`
- บริการอื่นที่ใช้แทนได้: Google Cloud Speech หรือผู้ให้บริการเสียงไทยในประเทศ

---

**English summary:** Show v1 is 1.40 m tall and weighs about 25 kg, with its centre of mass at 0.50 m. Each foot has a 5" hub wheel with a fail-safe brake, mounted outboard at ±22 cm, plus a rear caster on a 32 cm wheelbase. The robot tips at 23.9° sideways and 17.9° fore-aft.

- **Foot suspension:** two guided die-spring units per foot (12 mm travel) with lock pins for standing still. It still tips at ≥22.4° sideways and ≥15.7° fore-aft when fully compressed. The foot module is swappable. CAD: `hardware/cad/show_v1/wheel_foot_v1.py` (DXF plates, turned leg socket STEP, clash/mass/tip report).
- **Terrain:** indoor floors and smooth concrete; square edges up to 10 mm, ramped cable covers up to 25–30 mm, 5° ramps at low speed. No grass, gravel or stairs.

- **Joints:** no joint motors. Joints lock mechanically (Hirth discs on arms/neck, pin + clamp on legs), so the robot stays standing if power is lost.
- **Electronics:** Raspberry Pi 5 running a cloud voice pipeline (Azure STT → LLM → Azure TTS, Thai), and a 7" chest touchscreen in a printable bezel.
- **Power:** 2 × 24 V 10 Ah LiFePO4 batteries (kept low in the legs for stability) give roughly 7–12 h.
- **Parts:** see [bom/](../../bom/).

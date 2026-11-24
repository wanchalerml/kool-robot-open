"""Side + front schematic of the show v1 swappable wheel-foot module with spring units and lock pins (not CAD — dimensions for the CAD step)."""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
out = os.path.join(os.path.dirname(__file__), "..", "out"); os.makedirs(out, exist_ok=True)
WB, RD, RC = 320, 127/2, 100/2   # wheelbase, drive wheel r, caster r (mm)
fig, (a, b) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.6, 1]})
# --- side view ---
a.set_title("ด้านข้าง (side) — โมดูลเท้าถอดเปลี่ยน · หน้าอยู่ซ้าย", fontname="Loma")
a.plot([-250, 250], [0, 0], "k-", lw=1)
xd, xc = -WB/2, WB/2
a.add_patch(Circle((xd, RD), RD, fc="#333", ec="k")); a.add_patch(Circle((xd, RD), 18, fc="#c0392b"))
a.add_patch(Circle((xc, RC), RC, fc="#555", ec="k"))
top = 2*RD + 40
for x, r, lab in ((xd, RD, "ล้อขับ hub 5\" + เบรก"), (xc, RC, "ล้อหมุนตาม Ø100")):
    a.add_patch(Rectangle((x-22, r), 44, top - r - 22, fc="#bbb", ec="k"))                  # wheel fork / carrier
    a.add_patch(Rectangle((x-6, top-22), 12, 60, fc="#888", ec="k"))                        # guide rod Ø10
    for i in range(6): a.plot([x-14, x+14], [top-10+i*7, top-6+i*7], color="#2e8b57", lw=2)  # die spring
    a.add_patch(Rectangle((x+26, top-8), 26, 10, fc="#f1c40f", ec="k"))                     # lock pin
    a.text(x, -28, lab, ha="center", fontname="Loma", fontsize=9)
plate_y = top + 40
a.add_patch(Rectangle((-WB/2-60, plate_y), WB+120, 10, fc="#7f8c8d", ec="k"))
a.add_patch(FancyBboxPatch((-45, plate_y+10), 90, 22, boxstyle="round,pad=2", fc="#2980b9", ec="k"))
a.text(0, plate_y+18, "หน้าแปลนถอดเร็ว 4×M6 + หมุด 2 + XT60", ha="center", color="w", fontsize=8, fontname="Loma")
a.plot([0, 0], [plate_y+32, plate_y+90], "k-", lw=6); a.text(8, plate_y+80, "ข้อเท้า K-Bot (ล็อกท่า)", fontname="Loma", fontsize=9)
a.annotate("", (xd, -50), (xc, -50), arrowprops=dict(arrowstyle="<->")); a.text(0, -66, f"ระยะล้อหน้า-หลัง {WB} มม.", ha="center", fontname="Loma")
a.text(-255, plate_y+60, "สปริงแม่พิมพ์เขียว Ø20×64\n19.6 N/mm · ยุบใช้งาน สูงสุด 12 มม.\n+ ยาง PU กันกระแทก\n+ (เลือก) โช้คน้ำมัน RC เป็นตัวหน่วง", fontname="Loma", fontsize=8, color="#2e8b57")
a.text(40, plate_y+60, "สลักล็อก (โซลินอยด์ สปริงดัน)\nไฟดับ/จอดนิ่ง = ล็อก แข็งเหมือนไม่มีโช้ค", fontname="Loma", fontsize=8, color="#b7950b")
a.set_xlim(-260, 260); a.set_ylim(-80, plate_y+110); a.set_aspect("equal"); a.axis("off")
# --- front view ---
b.set_title("ด้านหน้า (front) — ล้อขับนอกเท้า ±220 มม.", fontname="Loma")
b.plot([-300, 300], [0, 0], "k-", lw=1)
for s in (-1, 1):
    b.add_patch(Rectangle((s*220-20, 0), 40, 2*RD, fc="#333", ec="k"))
    b.add_patch(Rectangle((min(s*90, s*250), plate_y), 160, 10, fc="#7f8c8d", ec="k"))
    b.add_patch(Rectangle((s*220-8, 2*RD), 16, plate_y-2*RD, fc="#bbb", ec="k"))
    b.plot([s*120, s*120], [plate_y+10, plate_y+120], "k-", lw=8)
b.annotate("", (-220, -30), (220, -30), arrowprops=dict(arrowstyle="<->")); b.text(0, -48, "440 มม. (ล้มข้าง 23.9° · ยุบสุด ยังเหลือ 22.4°)", ha="center", fontname="Loma")
b.set_xlim(-300, 300); b.set_ylim(-70, plate_y+140); b.set_aspect("equal"); b.axis("off")
fig.savefig(os.path.join(out, "show_v1_foot_module_sketch.png"), dpi=110, bbox_inches="tight")
print("ok")

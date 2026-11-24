"""มุมเอียงข้างก่อนล้ม (ยืนตรง ไม่กางขา) — K-Bot + เท้าล้อ · KOOL 24 พ.ย. 2569 #robot-wheel-feet ⑨
มุมล้ม θ = atan(ระยะจากจุดศูนย์ถ่วงถึงแนวล้อนอก / ความสูงจุดศูนย์ถ่วง) · สมมติข้อต่อยังล็อกท่า (ไฟดับจริง = ทรุดก่อน)"""
import mujoco, numpy as np, os
X = os.path.join(os.path.dirname(__file__), "..", "..", "third_party/kscale/kbot-joystick/robot/kbot/robot.mjcf")
m = mujoco.MjModel.from_xml_path(X); d = mujoco.MjData(m); d.qpos[3] = 1; mujoco.mj_forward(m, d)
WHEEL_D = 0.12; ANK0 = 0.058; dz = WHEEL_D / 2 - ANK0          # ข้อเท้าที่แกนล้อ
EXTRA, EXTRA_Z = 4.0, 1.15                                     # เปลือก/หัว/จอ 4 กก. ที่ระดับอก-หัว
BATT = 3.8                                                     # แบตอยู่ในลำตัว (ประมาณ)
TB = mujoco.mj_name2id(m, 1, "KD_B_102B_TORSO_BTM")
M0 = m.body_mass.sum(); z0 = d.subtree_com[0][2] - (-0.0)       # ยังไม่วางพื้น
zmin = min((d.geom_xpos[g][2] for g in range(m.ngeom)), default=0)
# วางพื้นด้วยแกนข้อเท้าเดิม 5.8 ซม.
ank = d.xanchor[mujoco.mj_name2id(m, 3, "dof_left_ankle_02")]; ground = ank[2] - ANK0
com_z = d.subtree_com[0][2] - ground + dz
torso_z = d.xipos[TB][2] - ground + dz
M = M0 + EXTRA; Z = (M0 * com_z + EXTRA * (EXTRA_Z + dz)) / M
y_ank = abs(ank[1])
print(f"มวล {M:.1f} กก. · CoM {Z:.3f} ม. · CoM ลำตัว(รวมแบต) {torso_z:.3f} ม. · แนวข้อเท้า ±{y_ank*100:.1f} ซม.")
def tip(yout, z): return np.degrees(np.arctan(yout / z))
def zbatt(newz): return Z - BATT * (torso_z - newz) / M
def need(z, ang=15): return z * np.tan(np.radians(ang))
rows = []
cases = [("เดิม: ล้อใต้ข้อเท้า (กว้าง 3 ซม.)", y_ank + 0.015, Z),
         ("แบตลงสะโพก (~0.72 ม.)", y_ank + 0.015, zbatt(0.72)),
         ("แบตลงหน้าแข้ง 2 ก้อน (~0.20 ม.)", y_ank + 0.015, zbatt(0.20))]
for yo in (0.18, 0.20, 0.22):
    cases.append((f"เท้ายื่นนอก ล้อขอบนอกที่ ±{yo*100:.0f} ซม.", yo, Z))
    cases.append((f"เท้ายื่นนอก ±{yo*100:.0f} + แบตลงสะโพก", yo, zbatt(0.72)))
cases.append(("เท้ายื่นนอก ±20 + แบตลงหน้าแข้ง", 0.20, zbatt(0.20)))
for n, yo, z in cases:
    F = M * 9.81 * yo / 1.14
    print(f"{n:42s} กว้างนอก-นอก {2*yo*100:4.0f} ซม. · CoM {z:.3f} · ล้มที่ {tip(yo, z):5.1f}° · ดันข้างที่ไหล่ได้ {F:4.0f} N · ต้องการ ≥15° → ±{need(z)*100:.1f} ซม.")

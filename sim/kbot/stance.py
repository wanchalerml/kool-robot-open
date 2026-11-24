"""K-Bot 1.4 ม. — ฐานยืน/กางขา/แรงบิดสะโพกด้านข้าง (KOOL 24 พ.ย. 2569 · #robot-wheel-feet)
ใช้: python3 sim/kbot/stance.py  (โมเดล third_party/kscale/kbot-joystick/robot/kbot/robot.mjcf)
EXTRA = น้ำหนักเปลือก/หัว/จอ ที่เพิ่ม (กก.) กระจายที่ลำตัว"""
import mujoco, numpy as np, os, sys
X = os.path.join(os.path.dirname(__file__), "..", "..", "third_party/kscale/kbot-joystick/robot/kbot/robot.mjcf")
m = mujoco.MjModel.from_xml_path(X); d = mujoco.MjData(m)
EXTRA = float(os.environ.get("EXTRA", "4.0")); TB = mujoco.mj_name2id(m, 1, "base")
m.body_mass[TB] += EXTRA
J = lambda n: m.jnt_qposadr[mujoco.mj_name2id(m, 3, n)]
FEET = ["LFootBushing_GPF_1517_12", "RFootBushing_GPF_1517_12"]
def body_pts(bn):
    b = mujoco.mj_name2id(m, 1, bn); P = []
    for g in range(m.ngeom):
        if m.geom_bodyid[g] == b and m.geom_type[g] == mujoco.mjtGeom.mjGEOM_MESH:
            mid = m.geom_dataid[g]; v = m.mesh_vert[m.mesh_vertadr[mid]:m.mesh_vertadr[mid] + m.mesh_vertnum[mid]]
            P.append(v @ d.geom_xmat[g].reshape(3, 3).T + d.geom_xpos[g])
    return np.vstack(P)
def pose(splay=0.0, knee=0.0, arm=0.0):
    d.qpos[:] = 0; d.qpos[3] = 1
    # กางขา: หา sign ที่ทำให้เท้าออกด้านนอก
    for side, s in (("left", 1), ("right", -1)):
        d.qpos[J(f"dof_{side}_hip_roll_03")] = SGN[side] * splay
        # ย่อเข่า: hip pitch +k/2, knee k, ankle k/2 (ทิศตามช่วงข้อต่อ)
        d.qpos[J(f"dof_{side}_knee_04")] = KS[side] * knee
        d.qpos[J(f"dof_{side}_hip_pitch_04")] = HS[side] * knee / 2
        d.qpos[J(f"dof_{side}_ankle_02")] = AS[side] * knee / 2
        d.qpos[J(f"dof_{side}_shoulder_pitch_03")] = SP[side] * arm   # ยกแขนไปข้างหน้า
    mujoco.mj_forward(m, d)
    # วางลงพื้น
    zmin = min(body_pts(f)[:, 2].min() for f in FEET); d.qpos[2] -= zmin; mujoco.mj_forward(m, d)
# หาทิศของแต่ละข้อ (ทดลองหมุนแล้วดูผล)
def trial(jn, val):
    d.qpos[:] = 0; d.qpos[3] = 1; d.qpos[J(jn)] = val; mujoco.mj_forward(m, d)
d.qpos[:] = 0; d.qpos[3] = 1; mujoco.mj_forward(m, d)
f0 = {s: body_pts(f).mean(0) for s, f in zip(("left", "right"), FEET)}
SGN, KS, HS, AS, SP = {}, {}, {}, {}, {}
for side, fb in zip(("left", "right"), FEET):
    lo, hi = m.jnt_range[mujoco.mj_name2id(m, 3, f"dof_{side}_hip_roll_03")]
    trial(f"dof_{side}_hip_roll_03", 0.1 if hi > 0.15 else -0.1); y = body_pts(fb).mean(0)[1]
    out = (y - f0[side][1]) * (1 if side == "left" else -1)
    SGN[side] = (1 if hi > 0.15 else -1) * (1 if out > 0 else -1)
    lo, hi = m.jnt_range[mujoco.mj_name2id(m, 3, f"dof_{side}_knee_04")]; KS[side] = 1 if hi > 0.5 else -1
    # hip pitch: เลือกทิศที่ทำให้เท้าไปข้างหน้า (ต้นขาไปหน้า)
    trial(f"dof_{side}_hip_pitch_04", 0.2); HS[side] = 1 if body_pts(fb).mean(0)[0] > f0[side][0] else -1
    trial(f"dof_{side}_ankle_02", 0.1 if m.jnt_range[J(f'dof_{side}_ankle_02') and mujoco.mj_name2id(m,3,f'dof_{side}_ankle_02')][1] > 0.15 else -0.1)
    # ankle: ทิศที่ปลายเท้ายกขึ้น (x หน้า z ขึ้น) — ใช้ทิศตรงข้าม knee/hip แบบง่าย: ทดสอบให้เท้าแบนหลังย่อ
    AS[side] = 1
    lo, hi = m.jnt_range[mujoco.mj_name2id(m, 3, f"dof_{side}_shoulder_pitch_03")]
    trial(f"dof_{side}_shoulder_pitch_03", 0.5 if hi > 0.6 else -0.5); hb = mujoco.mj_name2id(m, 1, "PRT0001" if side == "right" else "PRT0001_2")
    SP[side] = (1 if hi > 0.6 else -1) * (1 if d.xpos[hb][0] > 0.0 else -1)
# แก้ทิศข้อเท้าให้เท้าแบน (เลือก sign ที่ทำให้พื้นเท้าเอียงน้อยสุดหลังย่อเข่า 0.4)
for side, fb in zip(("left", "right"), FEET):
    best = None
    for s in (1, -1):
        AS[side] = s; pose(0, 0.4); P = body_pts(fb); low = P[P[:, 2] < P[:, 2].min() + 0.01]
        tilt = np.ptp(P[:, 2])
        if best is None or tilt < best[0]: best = (tilt, s)
    AS[side] = best[1]
def statics():
    """แรงบิดข้อต่อตอนยืนนิ่ง 2 เท้า (แรงพื้นกระจายแบบ least-squares)"""
    d.qvel[:] = 0; mujoco.mj_forward(m, d); bias = d.qfrc_bias.copy(); Jc = []
    for fb in FEET:
        b = mujoco.mj_name2id(m, 1, fb); p = body_pts(fb); c = p[p[:, 2] < p[:, 2].min() + 0.005].mean(0)
        jp = np.zeros((3, m.nv)); jr = np.zeros((3, m.nv)); mujoco.mj_jac(m, d, jp, jr, c, b); Jc.append(np.vstack([jp, jr]))
    Jc = np.vstack(Jc); w = np.linalg.lstsq(Jc[:, :6].T, bias[:6], rcond=None)[0]; tau = bias - Jc.T @ w
    return {mujoco.mj_id2name(m, 3, j): tau[m.jnt_dofadr[j]] for j in range(1, m.njnt)}
M = m.body_mass.sum(); g = 9.81
print(f"มวลรวม {M:.1f} กก. (รวมเปลือก/หัว/จอ +{EXTRA})")
print("splay° knee  ความสูง  CoM_z  กว้างเท้า(นอก-นอก)  ยาวเท้า  แรงดันข้างได้@ไหล่  hip_roll Nm (L/R)  knee Nm  hip_pitch Nm")
for knee in (0.0, 0.3):
    for sp in (0, 5, 10, 15, 20):
        pose(np.radians(sp), knee)
        P = [body_pts(f) for f in FEET]; low = [p[p[:, 2] < p[:, 2].min() + 0.01] for p in P]
        allp = np.vstack(low); cz = d.subtree_com[0][2]; cxy = d.subtree_com[0][:2]
        H = max(body_pts(mujoco.mj_id2name(m, 1, b))[:, 2].max() for b in range(1, m.nbody) if any(m.geom_bodyid[g] == b and m.geom_type[g] == mujoco.mjtGeom.mjGEOM_MESH for g in range(m.ngeom)))
        wy = np.ptp(allp[:, 1]); lx = np.ptp(allp[:, 0])
        dlat = min(allp[:, 1].max() - cxy[1], cxy[1] - allp[:, 1].min())
        hsh = 1.15 * (H / 1.40)
        F = M * g * dlat / hsh
        t = statics()
        print(f"{sp:5d} {knee:4.1f}  {H:5.2f}  {cz:5.3f}   {wy*1000:6.0f} มม.        {lx*1000:5.0f} มม.   {F:5.1f} N          {t['dof_left_hip_roll_03']:+5.1f}/{t['dof_right_hip_roll_03']:+5.1f}      {t['dof_left_knee_04']:+5.1f}   {t['dof_left_hip_pitch_04']:+5.1f}")

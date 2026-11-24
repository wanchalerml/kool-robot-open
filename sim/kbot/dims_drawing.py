"""ภาพด้านหน้า/ข้างพร้อมขนาด (ซม.) K-Bot + เท้าล้อ — ใช้สั่ง Gemini วาดให้ตรงสัดส่วน (KOOL 24 พ.ย. 2569)"""
import mujoco, numpy as np, os, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Circle, Rectangle
X = os.path.join(os.path.dirname(__file__), "..", "..", "third_party/kscale/kbot-joystick/robot/kbot/robot.mjcf")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "cad", "out", "kbot_wheel_dims.png")
SPLAY = np.radians(float(os.environ.get("SPLAY", "8")))
WHEEL_D = float(os.environ.get("WHEEL_D", "0.12")); WB = float(os.environ.get("WB", "0.23")); ANKLE_H = float(os.environ.get("ANKLE_H", str(WHEEL_D / 2)))   # ข้อเท้าอยู่ที่แกนล้อ
m = mujoco.MjModel.from_xml_path(X); d = mujoco.MjData(m); d.qpos[3] = 1
J = lambda n: m.jnt_qposadr[mujoco.mj_name2id(m, 3, n)]
FEET = {mujoco.mj_name2id(m, 1, "LFootBushing_GPF_1517_12"), mujoco.mj_name2id(m, 1, "RFootBushing_GPF_1517_12")}
def tris(skip_feet=True):
    out = []
    for g in range(m.ngeom):
        if m.geom_type[g] != mujoco.mjtGeom.mjGEOM_MESH or (skip_feet and m.geom_bodyid[g] in FEET): continue
        mid = m.geom_dataid[g]; v = m.mesh_vert[m.mesh_vertadr[mid]:m.mesh_vertadr[mid] + m.mesh_vertnum[mid]]
        f = m.mesh_face[m.mesh_faceadr[mid]:m.mesh_faceadr[mid] + m.mesh_facenum[mid]]
        out.append((v @ d.geom_xmat[g].reshape(3, 3).T + d.geom_xpos[g])[f])
    return np.vstack(out)
def setpose(splay):
    d.qpos[:] = 0; d.qpos[3] = 1
    for side, sg in (("left", 1), ("right", -1)):
        lo, hi = m.jnt_range[mujoco.mj_name2id(m, 3, f"dof_{side}_hip_roll_03")]
        d.qpos[J(f"dof_{side}_hip_roll_03")] = splay if hi > 0.5 else -splay
    mujoco.mj_forward(m, d)
    # ตรวจทิศ: เท้าซ้ายต้องไปทาง +y
    a = d.xanchor[mujoco.mj_name2id(m, 3, "dof_left_ankle_02")]
    return a
setpose(0); a0 = d.xanchor[mujoco.mj_name2id(m, 3, "dof_left_ankle_02")].copy()
a = setpose(SPLAY)
if a[1] < a0[1]:   # ทิศผิด → กลับ
    a = setpose(-SPLAY)
anks = [d.xanchor[mujoco.mj_name2id(m, 3, f"dof_{s}_ankle_02")].copy() for s in ("left", "right")]
T = tris(); zshift = ANKLE_H - min(k[2] for k in anks); T[..., 2] += zshift
for k in anks: k[2] += zshift
J3 = {n: d.xanchor[mujoco.mj_name2id(m, 3, n)] + [0, 0, zshift] for n in ("dof_left_hip_pitch_04", "dof_left_knee_04", "dof_left_ankle_02", "dof_left_shoulder_pitch_03")}
top = T[..., 2].max()
fig, axs = plt.subplots(1, 2, figsize=(13, 9), gridspec_kw=dict(width_ratios=[1.25, 1]))
for ax, (hi, title) in zip(axs, ((1, "FRONT"), (0, "SIDE"))):
    pc = PolyCollection(T[..., [hi, 2]] * 100, facecolor="#d9dbe0", edgecolor="#9aa0a8", linewidths=0.1); ax.add_collection(pc)
    for k in anks:
        cx = k[hi] * 100
        if hi == 1:   # หน้า: เห็นล้อแนวตั้งบาง ๆ
            ax.add_patch(Rectangle((cx - 1.5, 0), 3, WHEEL_D * 100, color="#222")); ax.add_patch(Rectangle((cx - 2.3, ANKLE_H * 100 - 1.5), 4.6, 3, color="#777"))
        else:
            for dx in (-WB / 2, WB / 2): ax.add_patch(Circle((cx + dx * 100, WHEEL_D * 50), WHEEL_D * 50, color="#222"))
            ax.add_patch(Rectangle((cx - WB * 50, ANKLE_H * 100 - 1.25), WB * 100, 2.5, color="#777"))
    ax.set_aspect("equal"); ax.set_ylim(-4, top * 100 + 6); ax.axis("off"); ax.set_title(title)
    xs = T[..., hi].ravel() * 100; x0 = xs.min() - 14
    ax.set_xlim(x0 - 10, xs.max() + (8 if hi == 1 else 30))
    # เส้นบอกความสูง
    marks = [("พื้น", 0), ("ข้อเท้า", J3["dof_left_ankle_02"][2] * 100), ("เข่า", J3["dof_left_knee_04"][2] * 100), ("สะโพก", J3["dof_left_hip_pitch_04"][2] * 100), ("ไหล่", J3["dof_left_shoulder_pitch_03"][2] * 100), ("หัว", top * 100)]
    if hi == 1:
        for (n1, z1), (n2, z2) in zip(marks[:-1], marks[1:]):
            ax.annotate("", (x0, z1), (x0, z2), arrowprops=dict(arrowstyle="<->", lw=0.8))
            ax.text(x0 - 1, (z1 + z2) / 2, f"{z2 - z1:.1f}", ha="right", va="center", fontsize=10)
            ax.plot([x0, xs.max()], [z2, z2], lw=0.3, ls=":", color="#888")
        ax.annotate("", (x0 - 9, 0), (x0 - 9, top * 100), arrowprops=dict(arrowstyle="<->", lw=1)); ax.text(x0 - 10, top * 50, f"{top * 100:.0f}", ha="right", va="center", fontsize=12, fontweight="bold")
        sw = (anks[0][1] - anks[1][1]) * 100 + 4.6; ax.annotate("", (anks[1][1] * 100 - 2.3, -2.5), (anks[0][1] * 100 + 2.3, -2.5), arrowprops=dict(arrowstyle="<->", lw=0.8)); ax.text(0, -4, f"stance {sw:.0f} (hip roll {np.degrees(SPLAY):.0f}°)", ha="center", va="top", fontsize=9)
        ys = T[..., 1].ravel() * 100; zz = T[..., 2].ravel() * 100; band = (zz > marks[4][1] - 6) & (zz < marks[4][1] + 6)
        w = ys[band].max() - ys[band].min(); ax.text(0, marks[4][1] + 9, f"shoulder width {w:.0f}", ha="center", fontsize=9)
    else:
        k = anks[0][0] * 100; ax.annotate("", (k - WB * 50, -2.5), (k + WB * 50, -2.5), arrowprops=dict(arrowstyle="<->", lw=0.8)); ax.text(k, -4, f"wheelbase {WB * 100:.0f} · wheel Ø{WHEEL_D * 100:.0f}", ha="center", va="top", fontsize=9)
        dd = np.ptp(T[..., 0][(T[..., 2] > marks[4][1] / 100 - 0.3) & (T[..., 2] < marks[4][1] / 100)]) * 100; ax.text(k, marks[4][1] + 9, f"chest depth {dd:.0f}", ha="center", fontsize=9)
fig.suptitle(f"K-Bot + wheel feet · total {top * 100:.0f} cm · dimensions in cm (ground→ankle→knee→hip→shoulder→head)", fontsize=12)
plt.tight_layout(); plt.savefig(OUT, dpi=110, facecolor="white"); print("saved", OUT, "top", round(top * 100, 1), {k: round(v[2] * 100, 1) for k, v in J3.items()})

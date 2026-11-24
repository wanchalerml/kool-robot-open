"""Show v1 chest screen bezel + back plate (draft, build123d).

Default panel = Raspberry Pi Touch Display 2, 7" (landscape on the chest).
  outline 189.32 x 120.24 mm, active 154.56 x 86.94 mm (datasheet)
  PANEL_T (thickness) = 14 mm placeholder -> MEASURE the real unit before printing.

Switch panel with env PANEL=pi10 (Pi Touch Display 2 10", 247.3 x 161.8, active 216.6 x 135.4)
or PANEL=ws10ep (Waveshare 10.1EP-CAPLCD glass 239 x 147, active 217.18 x 135.59).

Parts (print on X2D, PETG or ASA, 0.2 mm layers, front face down):
  bezel  : front frame with a 1.5 mm lip over the glass edge, pocket for the panel,
           4 corner bosses for M3 heat-set inserts, intake slots on the bottom wall,
           exhaust slots on the top wall.
  back   : plate that clamps the panel (2 mm foam gasket between), Pi 5 standoffs
           (58 x 49 mm, M2.5), 8 mm air gap, slot grille behind the Pi active cooler,
           2 tabs with M4 holes to bolt onto the torso frame.
Outputs cad/out/chest_screen_<panel>_{bezel,back}.step/.stl and a preview PNG.
"""
import os
from build123d import *

PANELS = {
    "pi7":    dict(W=189.32, H=120.24, AW=154.56, AH=86.94, T=14.0),
    "pi10":   dict(W=247.30, H=161.80, AW=216.60, AH=135.40, T=14.0),
    "ws10ep": dict(W=239.00, H=147.00, AW=217.18, AH=135.59, T=10.0),
}
name = os.environ.get("PANEL", "pi7")
P = PANELS[name]
PANEL_T = float(os.environ.get("PANEL_T", P["T"]))

WALL = 6.0      # side wall
LIP = 1.6       # front lip thickness
CLR = 0.4       # clearance around panel
WIN = 1.5       # window margin beyond active area (each side)
GASKET = 2.0
AIRGAP = 8.0    # space behind panel for Pi 5 + cooler airflow
BACK_T = 3.0

OW = P["W"] + 2 * (CLR + WALL)
OH = P["H"] + 2 * (CLR + WALL)
DEPTH = LIP + PANEL_T + GASKET + AIRGAP   # bezel depth (front to back plate)

out = os.path.join(os.path.dirname(__file__), "..", "out")
os.makedirs(out, exist_ok=True)

# ---------------- bezel ----------------
with BuildPart() as bezel:
    Box(OW, OH, DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))
    fillet(bezel.edges().filter_by(Axis.Z), radius=6)
    # panel pocket (from back, leaves the lip at z=0..LIP)
    with Locations((0, 0, LIP)):
        Box(P["W"] + 2 * CLR, P["H"] + 2 * CLR, DEPTH, mode=Mode.SUBTRACT,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    # viewing window through the lip
    Box(P["AW"] + 2 * WIN, P["AH"] + 2 * WIN, LIP * 3, mode=Mode.SUBTRACT)
    # corner bosses for M3 heat-set inserts (OD 7, insert hole 4.2 x 6)
    bx, by = OW / 2 - WALL / 2 - 1.0, OH / 2 - WALL / 2 - 1.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            with Locations((sx * bx, sy * by, DEPTH - 6)):
                Cylinder(2.1, 6.01, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # vent slots: intake bottom wall, exhaust top wall (in the air-gap band only)
    zc = LIP + PANEL_T + GASKET + AIRGAP / 2
    n = 9
    pitch = (OW - 40) / (n - 1)
    for i in range(n):
        x = -(OW - 40) / 2 + i * pitch
        for y in (-OH / 2, OH / 2):
            with Locations((x, y, zc)):
                Box(10, WALL * 3, AIRGAP * 0.6, mode=Mode.SUBTRACT)

# ---------------- back plate ----------------
with BuildPart() as back:
    Box(OW, OH, BACK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    fillet(back.edges().filter_by(Axis.Z), radius=6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            with Locations((sx * bx, sy * by, 0)):
                Cylinder(1.7, BACK_T * 3, mode=Mode.SUBTRACT)
    # Pi 5 standoffs (inside face = +Z), 58 x 49 mm pattern, M2.5
    for sx in (-1, 1):
        for sy in (-1, 1):
            with Locations((sx * 29, sy * 24.5, BACK_T)):
                Cylinder(3.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((sx * 29, sy * 24.5, 0)):
                Cylinder(1.25, 30, mode=Mode.SUBTRACT)
    # grille behind the Pi cooler
    for i in range(7):
        with Locations((-24 + i * 8, 0, 0)):
            Box(4, 36, BACK_T * 3, mode=Mode.SUBTRACT)
    # cable pass-through (DSI ribbon + power + USB mic/speaker)
    with Locations((0, -OH / 2 + 18, 0)):
        Box(40, 8, BACK_T * 3, mode=Mode.SUBTRACT)
    # mounting tabs to the torso frame (left/right), M4
    for sx in (-1, 1):
        with Locations((sx * (OW / 2 + 9), 0, 0)):
            Box(20, 30, BACK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((sx * (OW / 2 + 11), 0, 0)):
            Cylinder(2.2, BACK_T * 3, mode=Mode.SUBTRACT)

for part, nm in ((bezel.part, "bezel"), (back.part, "back")):
    base = os.path.join(out, f"chest_screen_{name}_{nm}")
    export_step(part, base + ".step")
    export_stl(part, base + ".stl")

bb = bezel.part.bounding_box()
print(f"panel={name} outer {OW:.1f} x {OH:.1f} x {DEPTH:.1f} mm, "
      f"bezel vol {bezel.part.volume/1000:.0f} cm3, back vol {back.part.volume/1000:.0f} cm3")

# ---------------- preview ----------------
try:
    import numpy as np, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(12, 5))
    for k, (part, title, elev) in enumerate(((bezel.part, "bezel (front)", -60), (back.part, "back plate (inside)", 60))):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        verts, tris = part.tessellate(0.3)
        V = np.array([[v.X, v.Y, v.Z] for v in verts])
        polys = [V[list(t)] for t in tris]
        ax.add_collection3d(Poly3DCollection(polys, facecolor="#9fb4c8", edgecolor="#55657580", linewidth=0.05))
        m = max(OW, OH) / 2 + 15
        ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m / 2, m / 2)
        ax.view_init(elev=elev, azim=-60)
        ax.set_title(title); ax.set_axis_off()
    fig.suptitle(f"Show v1 chest screen – {name}: {OW:.0f} x {OH:.0f} x {DEPTH:.0f} mm (PANEL_T={PANEL_T} mm, measure!)")
    fig.savefig(os.path.join(out, f"chest_screen_{name}_preview.png"), dpi=110, bbox_inches="tight")
except Exception as e:
    print("preview skipped:", e)

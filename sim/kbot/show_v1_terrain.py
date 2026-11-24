"""Show v1 — terrain limits: tip margin on ramps / side slopes, braking, and step/threshold climbing vs wheel size.
Inputs match sim/kbot/show_v1_tip.py (mass 25 kg, CoM 0.496 m, wheels ±0.22 m lateral, 0.30 m wheelbase).
Static rigid-body estimate — real limits are lower (shell flex, joint play, CoM error). Verify on the real robot.
"""
import numpy as np

Z = 0.496          # CoM height (m)
HALF = 0.22        # lateral half-track (m)
WB = 0.30          # front-rear wheel distance (m), CoM assumed mid-foot
G = 9.81
deg = np.degrees

side_tip = deg(np.arctan(HALF / Z))
fa_tip = deg(np.arctan(WB / 2 / Z))
print(f"flat ground: side tip {side_tip:.1f}°, fore/aft tip {fa_tip:.1f}°")

print("\n== ramps / slopes (margin left before tipping) ==")
for a_brake in (0.0, 1.0, 2.0):  # m/s² braking or accelerating
    eq = deg(np.arctan(a_brake / G))
    for slope in (3, 5, 7):
        down = fa_tip - slope - eq    # going downhill + braking: both tip forward
        up = fa_tip - slope - eq      # going uphill + accelerating: both tip backward
        side = side_tip - slope
        print(f"  brake/accel {a_brake:.0f} m/s² (~{eq:.1f}°) · slope {slope}°: down-ramp braking margin {down:5.1f}° · "
              f"up-ramp accel margin {up:5.1f}° · side slope margin {side:5.1f}°")

# wheel holding on a slope: brake must hold m g sin(a)
m = 25.0
for slope in (5,):
    f = m * G * np.sin(np.radians(slope))
    print(f"\n  holding on {slope}°: {f:.0f} N total → {f/2*0.0635:.1f} Nm per 5\" hub wheel (2 drive wheels, r=63.5 mm)")

print("\n== climbing a square step (no ramp) ==")
print("  force ratio F/N to roll a wheel over a step h: sqrt(h(2r-h))/(r-h)  — traction limit μ≈0.6–0.8 for PU on tile")
for name, d_mm in (("5\" hub drive", 127), ("caster 75", 75), ("caster 100", 100), ("outdoor 150", 150), ("outdoor 200", 200)):
    r = d_mm / 2
    hmax = {mu: r * (1 - np.cos(np.arctan(mu))) for mu in (0.6, 0.8)}
    print(f"  {name:13s} Ø{d_mm:3d} mm: max square step ≈ {hmax[0.6]:.0f}–{hmax[0.8]:.0f} mm  (traction μ 0.6–0.8, slow, no momentum)")
for h in (10, 15, 25, 30):
    r = 63.5
    ratio = np.sqrt(h * (2 * r - h)) / (r - h) if h < r else np.inf
    print(f"    5\" wheel, step {h} mm: needs F/N = {ratio:.2f}  ({'OK' if ratio <= 0.7 else 'slips / needs ramp'})")
print("  → cable protectors with sloped sides (≤20°) and threshold ramps are fine up to 25–30 mm; bare square edges only ≤ ~10 mm")

print("\n== foot suspension (⑦): 2 guided die-spring units per foot (one over each wheel) ==")
K_SPR = 4.4 * 4.448   # N/mm — ISO 10243 green Ø20 (10 mm rod) × 64 mm long (McMaster 1804N131 table)
STOP = 12.0           # mm usable travel to the hard stop (spring max 35% = 22 mm)
for mass in (25.0, 35.0):
    per = mass * G / 4
    sag = per / K_SPR
    print(f"  robot {mass:.0f} kg: {per:.0f} N per spring → sag {sag:.1f} mm · bump left {STOP - sag:.1f} mm · bump force to stop {K_SPR*STOP:.0f} N/spring")
sag = 25 * G / 4 / K_SPR
diff = STOP  # worst: one side at the stop, the other fully extended (sag → 0)
roll = deg(np.arctan(diff / (2 * HALF * 1000)))
print(f"  worst roll (one side bottomed, other topped out, Δ{diff:.0f} mm over track {2*HALF*1000:.0f} mm): {roll:.1f}° → side tip ≥ {side_tip - roll:.1f}°  (need ≥15°)")
for wb in (0.30, 0.32, 0.34):
    base = deg(np.arctan(wb / 2 / Z)); pitch = deg(np.arctan(diff / (wb * 1000)))
    print(f"  wheelbase {wb*100:.0f} cm: fore/aft tip {base:.1f}° locked · {base - pitch:.1f}° unlocked worst case")
# a FREE bogie pivot (no centring springs) has zero pitch stiffness: body + both bogies rotate about the pivot axis
Kpitch = lambda k_end, wb: 2 * 2 * k_end * 1000 * (wb / 2) ** 2   # Nm/rad, 2 feet × 2 springs
mgz = 25 * G * Z
for wb in (0.30, 0.32):
    K = Kpitch(K_SPR, wb)
    print(f"  pitch stiffness with springs at both wheels (wb {wb*100:.0f}): {K:.0f} Nm/rad vs topple {mgz:.0f} Nm/rad → tilt amplification ×{1/(1-mgz/K):.2f}")
print("  free bogie (pivot, no springs): pitch stiffness 0 → robot pitches over the pivot ✗ — bogie must be spring-centred or locked")

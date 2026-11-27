"""split each piece into bodies, auto-orient for least support, write job STLs"""
import json, os, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "..", "out"); W = os.environ.get("SLICE_WORK", "/tmp/slice_v1"); J = os.path.join(W, "jobs"); os.makedirs(J, exist_ok=True)
BED = 254.0
def cands(m):
    Ts = []
    for ax in np.vstack([np.eye(3), -np.eye(3)]):
        Ts.append(trimesh.geometry.align_vectors(ax, [0, 0, -1]))
    try:
        tf, pr = trimesh.poses.compute_stable_poses(m, n_samples=1, threshold=0.0)
        Ts += list(tf[:10])
    except Exception:
        pass
    return Ts
def fit_xy(r):
    pts = r.convex_hull.vertices[:, :2] if len(r.vertices) > 50 else r.vertices[:, :2]
    best = None
    for a in np.radians(np.arange(0, 90, 7.5)):
        c, s = np.cos(a), np.sin(a); q = pts @ np.array([[c, -s], [s, c]])
        e = q.max(0) - q.min(0)
        if e.max() <= BED and (best is None or e.max() < best[0]): best = (e.max(), a)
    return best
def score(r):
    z0 = r.bounds[0, 2]; n = r.face_normals; c = r.triangles_center
    over = (n[:, 2] < -0.707) & (c[:, 2] > z0 + 0.4)
    return r.area_faces[over].sum()
jobs = []
for i, p in enumerate(json.load(open(os.path.join(W, "pieces.json")))):
    m = trimesh.load(f"{OUT}/{p['file']}")
    bodies = m.split(only_watertight=True) if m.is_watertight and m.body_count > 1 else [m]
    bodies = [b for b in bodies if b.volume > 50] if m.is_watertight else bodies
    for j, b in enumerate(bodies):
        best = None
        for T in cands(b):
            r = b.copy(); r.apply_transform(T)
            if r.extents[2] > BED: continue
            f = fit_xy(r)
            if f is None: continue
            s = score(r) + 0.5 * r.extents[2]
            if best is None or s < best[0]: best = (s, T, f[1])
        if best is None:
            print("NO FIT", p["file"], j, b.extents.round(0)); continue
        r = b.copy(); r.apply_transform(best[1])
        r.apply_transform(trimesh.transformations.rotation_matrix(best[2], [0, 0, 1]))
        r.apply_translation(-r.bounds[0])
        fn = f"{J}/{i:03d}_{j}.stl"; r.export(fn)
        jobs.append(dict(p, job=fn, body=j, ext=r.extents.round(0).tolist(), over=round(score(r))))
json.dump(jobs, open(os.path.join(W, "jobs.json"), "w"), ensure_ascii=False)
print(len(jobs), "jobs")

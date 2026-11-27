import json, collections, re, os
W = os.environ.get("SLICE_WORK", "/tmp/slice_v1")
HERE = os.path.dirname(os.path.abspath(__file__))
jobs = {j["job"]: j for j in json.load(open(os.path.join(W, "jobs.json")))}
res = {}
for line in open(os.path.join(W, "results.txt")):
    p = line.strip().split("|")
    if len(p) >= 3 and p[2].strip():
        res[p[0]] = (float(p[2]), p[3].strip() if len(p) > 3 else "")
def hrs(t):
    d = {u: v for v, u in re.findall(r"(\d+)([dhms])", t)}; return int(d.get("d",0))*24+int(d.get("h",0))+int(d.get("m",0))/60
piece = collections.OrderedDict(); miss = []
for k, j in jobs.items():
    if k not in res: miss.append(j["file"]); continue
    key = (j["file"], j["mat"], j["n"], j["group"])
    g, t = res[k]; a = piece.setdefault(key, [0, 0]); a[0] += g; a[1] += hrs(t)
mat = collections.defaultdict(lambda: [0, 0])
for (f, m, n, gr), (g, h) in piece.items():
    mat[m][0] += g * n; mat[m][1] += h * n
json.dump([dict(file=f, mat=m, n=n, group=gr, g_each=round(g, 1), g_total=round(g * n), h_total=round(h * n, 1)) for (f, m, n, gr), (g, h) in piece.items()],
          open(os.path.join(HERE, "..", "..", "out", "show_v1_slice_weights.json"), "w"), ensure_ascii=False, indent=0)
for m, (g, h) in sorted(mat.items(), key=lambda x: -x[1][0]): print(f"{m:16s} {g/1000:6.2f} kg  {h:6.0f} h")
print("missing", len(miss), miss[:5])

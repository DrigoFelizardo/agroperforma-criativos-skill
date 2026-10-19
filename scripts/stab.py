#!/usr/bin/env python3
"""stab.py <project> — per-frame stabilisation offsets for media/cut.mp4.
Measures frame-to-frame translation (Apple Vision on the top 17% background band, 720px wide — excludes the presenter), integrates it per shot
(reset at every cut in media/cut.json), smooths with a 0.6 s moving average and returns
correction = smooth − raw in composition px (1080 wide). Writes media/stab.json."""
import json, os, subprocess, sys
proj = sys.argv[1]; S = sys.argv[2]
cut = json.load(open(f"{proj}/media/cut.json")); fps = cut["fps"]
d = f"{S}/stab_{os.path.basename(proj)}"; os.makedirs(d, exist_ok=True)
for f in os.listdir(d): os.remove(f"{d}/{f}")
subprocess.check_call(["ffmpeg", "-v", "error", "-i", f"{proj}/media/cut.mp4", "-vf", "crop=iw:ih*0.17:0:0,scale=720:-2", f"{d}/f_%05d.png"])
rows = subprocess.check_output(["swift", f"{S}/shift.swift", d], text=True).split("\n")
dx = [float(r.split()[1]) for r in rows if r.strip()]; dy = [-float(r.split()[2]) for r in rows if r.strip()]
n = len(dx); K = 1.5  # background band analysed at 720 wide → 1080
starts = {round(s["start"] * fps) for s in cut["segments"]}
cx, cy, seg = [0.0] * n, [0.0] * n, [0] * n
sid = -1
for i in range(n):
    if i in starts or i == 0: sid += 1; cx[i] = cy[i] = 0.0
    else: cx[i] = cx[i - 1] + dx[i] * K; cy[i] = cy[i - 1] + dy[i] * K
    seg[i] = sid
W = int(round(0.6 * fps))
def smooth(a):
    out = []
    for i in range(n):
        idx = [j for j in range(i - W, i + W + 1) if 0 <= j < n and seg[j] == seg[i]]
        out.append(sum(a[j] for j in idx) / len(idx))
    return out
sx, sy = smooth(cx), smooth(cy)
lim_x, lim_y = 30, 50
ox = [0.0] * n  # horizontal jitter is small; correcting it adds noise
oy = [round(max(-lim_y, min(lim_y, cy[i] - sy[i])), 1) for i in range(n)]
json.dump({"fps": fps, "zoom": 1.06, "x": ox, "y": oy}, open(f"{proj}/media/stab.json", "w"))
print(f"frames={n} max|x|={max(map(abs, ox))} max|y|={max(map(abs, oy))}")

#!/usr/bin/env python3
"""track.py <project> — smoothed face-x keyframes per shot from media/faces.json (4 fps Vision samples).
Moving average over ±2 samples inside each shot (never across a cut). Writes media/track.json:
[[t, cx, hard], ...]  hard=1 → jump at a cut, else linear move from the previous keyframe."""
import json, sys
p = sys.argv[1]
faces = json.load(open(f"{p}/media/faces.json")); segs = json.load(open(f"{p}/media/cut.json"))["segments"]
keys = []
for s in segs:
    v = [f for f in faces if s["start"] <= f["t"] < s["end"]]
    if not v:
        keys.append([s["start"], keys[-1][1] if keys else 0.5, 1]); continue
    sm = []
    for i in range(len(v)):
        w = v[max(0, i - 3): i + 4]; sm.append(sum(f["cx"] for f in w) / len(w))
    keys.append([round(s["start"], 4), round(sm[0], 4), 1])
    for f, c in zip(v, sm):
        if f["t"] - s["start"] > 0.05 and round(f["t"] * 4) % 2 == 0: keys.append([round(f["t"], 4), round(c, 4), 0])
json.dump(keys, open(f"{p}/media/track.json", "w"))
print(len(keys), "keys")

#!/usr/bin/env python3
"""mkcfg.py <project> — creative.base.json (+ "camSplits": [t, ...] extra zoom changes) → creative.json.
If base has no "cam", generates it from media/cut.json: one zoom per shot (and at each camSplit),
cycling scales that alternate push-in / pull-out. Adds face tracking (media/track.json) and stab if present."""
import json, os, subprocess, sys
p = sys.argv[1]; kit = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(f"{p}/creative.base.json")); cut = json.load(open(f"{p}/media/cut.json"))
CYCLE = [(1.0, 1.05), (1.22, 1.16), (1.08, 1.13), (1.3, 1.24), (1.12, 1.06), (1.2, 1.26), (1.04, 1.09), (1.28, 1.22)]
if "cam" not in base:
    edges = sorted({round(s["start"], 4) for s in cut["segments"]} | {round(t, 4) for t in base.get("camSplits", [])})
    edges.append(cut["total"])
    base["cam"] = [{"start": a, "end": b, "s": CYCLE[i % len(CYCLE)][0], "to": CYCLE[i % len(CYCLE)][1], "cx": 0.5}
                   for i, (a, b) in enumerate(zip(edges, edges[1:]))]
base.setdefault("duration", cut["total"])
subprocess.check_call(["python3", f"{kit}/track.py", p], stdout=subprocess.DEVNULL)
base["track"] = json.load(open(f"{p}/media/track.json"))
if base.get("trackMode") == "shot":  # mean face x per zoom shot
    faces = json.load(open(f"{p}/media/faces.json"))
    for c in base["cam"]:
        v = [f["cx"] for f in faces if c["start"] <= f["t"] < c["end"]]
        if v: c["cx"] = round(sum(v) / len(v), 4)
json.dump(base, open(f"{p}/creative.json", "w"), ensure_ascii=False)
subprocess.check_call(["python3", f"{kit}/build.py", p], stdout=subprocess.DEVNULL)
print("cam shots:", len(base["cam"]), "duration:", base["duration"])

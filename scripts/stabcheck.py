#!/usr/bin/env python3
"""stabcheck.py <project> <scratch> — per shot, measure background tremor (left 300x700 strip, 1080 scale)
in cut_raw.mp4 vs the stabilised cut.mp4; zero the correction in shots where it does not help,
then rewrite media/stab.json (keeps stab_full.json)."""
import json, os, shutil, subprocess, sys, statistics as stt
p, S = sys.argv[1], sys.argv[2]
cut = json.load(open(f"{p}/media/cut.json")); fps = cut["fps"]
def tremor(f, a, b):
    d = f"{S}/sc"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.check_call(["ffmpeg", "-v", "error", "-ss", f"{a}", "-to", f"{b}", "-i", f, "-vf", "scale=1080:1920,crop=300:700:0:0", f"{d}/f_%04d.png"])
    rows = [l.split() for l in subprocess.check_output(["swift", f"{S}/shift.swift", d], text=True).splitlines() if l.strip()][1:]
    y = [float(r[2]) for r in rows]
    if len(y) < 6: return 0
    return stt.mean(abs(y[i] - stt.mean(y[max(0, i-4):i+5])) for i in range(len(y)))
full = f"{p}/media/stab_full.json"
if not os.path.exists(full): shutil.copy(f"{p}/media/stab.json", full)
st = json.load(open(full)); keep = 0
for s in cut["segments"]:
    a, b = s["start"] + 0.05, s["end"] - 0.05
    r0, r1 = tremor(f"{p}/media/cut_raw.mp4", a, b), tremor(f"{p}/media/cut.mp4", a, b)
    ok = r1 < r0 * 0.9
    print(f"shot {s['start']:6.2f}-{s['end']:6.2f}  antes={r0:.2f} depois={r1:.2f}  {'estabiliza' if ok else 'mantém original'}")
    if not ok:
        for i in range(round(s["start"] * fps), min(len(st['y']), round(s["end"] * fps))): st["y"][i] = 0.0; st["x"][i] = 0.0
    else: keep += 1
json.dump(st, open(f"{p}/media/stab.json", "w"))
print("shots estabilizados:", keep)

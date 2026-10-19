#!/usr/bin/env python3
"""plan.py <channel.wav> <keep a:b> [<keep a:b> ...] [--gap 0.25] [--pad 0.08] [--thr -40]
Splits each kept range at every silence longer than --gap (RMS of the chosen mic channel,
50 ms windows) and keeps --pad seconds of breath on each side. Prints a:b segments for cut.py."""
import subprocess, sys

args = sys.argv[1:]
opt = {"--gap": 0.25, "--pad": 0.08, "--thr": -40.0}
for k in list(opt):
    if k in args:
        i = args.index(k); opt[k] = float(args[i + 1]); del args[i:i + 2]
wav, keeps = args[0], [tuple(map(float, a.split(":"))) for a in args[1:]]

out = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-af",
    "asetnsamples=800,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
    "-f", "null", "-"], capture_output=True, text=True).stdout
rms, t = [], None
for line in out.splitlines():
    if "pts_time:" in line: t = float(line.split("pts_time:")[1])
    elif "RMS_level=" in line:
        v = line.split("=")[1]; rms.append((t, -120.0 if "inf" in v else float(v)))
win = 0.05
segs = []
for a, b in keeps:
    on = [(t, t + win) for t, v in rms if a <= t < b and v > opt["--thr"]]
    if not on: continue
    runs = [list(on[0])]
    for s, e in on[1:]:
        if s - runs[-1][1] <= opt["--gap"]: runs[-1][1] = e
        else: runs.append([s, e])
    for s, e in runs:
        if e - s < 0.12: continue  # clicks / breaths
        segs.append((max(a, s - opt["--pad"]), min(b, e + opt["--pad"])))
merged = [list(segs[0])]
for s, e in segs[1:]:
    if s <= merged[-1][1] + 0.12: merged[-1][1] = max(merged[-1][1], e)  # removing <0.12 s is not worth a jump cut
    else: merged.append([s, e])
print(" ".join(f"{s:.2f}:{e:.2f}" for s, e in merged))
total = sum(e - s for s, e in merged)
print(f"# {len(merged)} segments, {total:.2f}s", file=sys.stderr)

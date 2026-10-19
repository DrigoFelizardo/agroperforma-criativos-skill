#!/usr/bin/env python3
"""applystab.py <project> — bakes media/stab.json into media/cut.mp4 (keeps media/cut_raw.mp4).
6% zoom margin, per-frame crop offsets via ffmpeg sendcmd (vertical-only by default)."""
import json, os, subprocess, sys
p = sys.argv[1]; st = json.load(open(f"{p}/media/stab.json")); fps = st["fps"]
raw = f"{p}/media/cut_raw.mp4"
if not os.path.exists(raw): os.rename(f"{p}/media/cut.mp4", raw)
k = 2160 / 1080; W, H = 2292, 4076; bx, by = (W - 2160) // 2, (H - 3840) // 2
cmd = f"{p}/media/stab.cmd"
with open(cmd, "w") as f:
    for i, (x, y) in enumerate(zip(st["x"], st["y"])):
        f.write(f"{i/fps:.4f} crop x {bx - x*k:.0f}, crop y {by - y*k:.0f};\n")
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-vf",
    f"scale={W}:{H}:flags=lanczos,sendcmd=f={cmd},crop=2160:3840:{bx}:{by}",
    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "12", "-c:a", "copy", "-movflags", "+faststart", f"{p}/media/cut.mp4"])
print("stabilised", f"{p}/media/cut.mp4")

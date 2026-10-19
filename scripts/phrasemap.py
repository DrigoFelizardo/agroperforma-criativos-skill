#!/usr/bin/env python3
"""phrasemap.py <channel.wav> [--gap 0.3] [--thr -40] — split raw audio into phrases at pauses (RMS)
and transcribe each phrase on its own (large-v3), so takes/restarts can be chosen by exact text.
Prints one line per phrase: index, a–b (source seconds), text. Writes <wav>.phrases.json."""
import json, os, subprocess, sys, tempfile

args = sys.argv[1:]
opt = {"--gap": 0.3, "--thr": -40.0}
for k in list(opt):
    if k in args:
        i = args.index(k); opt[k] = float(args[i + 1]); del args[i:i + 2]
wav = args[0]
out = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-af",
    "asetnsamples=800,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
    "-f", "null", "-"], capture_output=True, text=True).stdout
rms, t = [], None
for line in out.splitlines():
    if "pts_time:" in line: t = float(line.split("pts_time:")[1])
    elif "RMS_level=" in line:
        v = line.split("=")[1]; rms.append((t, -120.0 if "inf" in v else float(v)))
runs = []
for t, v in rms:
    if v > opt["--thr"]:
        if runs and t - runs[-1][1] <= opt["--gap"]: runs[-1][1] = t + 0.05
        else: runs.append([t, t + 0.05])
runs = [r for r in runs if r[1] - r[0] >= 0.15]
tmp = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
res = []
for i, (a, b) in enumerate(runs):
    a2, b2 = max(0, a - 0.06), b + 0.06
    clip = f"{tmp}/p.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", f"atrim={a2}:{b2},apad=pad_dur=0.3", "-ar", "16000", clip])
    for f in ("transcript.json",):
        try: os.remove(f"{tmp}/{f}")
        except FileNotFoundError: pass
    subprocess.run(["npx", "hyperframes", "transcribe", clip, "-m", "large-v3", "-l", "pt", "--json", "-d", tmp],
                   capture_output=True)
    try:
        j = json.load(open(f"{tmp}/transcript.json")); w = j if isinstance(j, list) else j["words"]
        text = " ".join(x["text"] for x in w)
    except Exception: text = "(?)"
    res.append({"i": i, "a": round(a2, 2), "b": round(b2, 2), "text": text})
    print(f"{i:3d}  {a2:7.2f}–{b2:7.2f}  {text}", flush=True)
json.dump(res, open(wav + ".phrases.json", "w"), ensure_ascii=False, indent=1)

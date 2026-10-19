#!/usr/bin/env python3
"""cut.py <src.mp4> <out.mp4> <channel L|R> <a:b> [<a:b> ...]
   cut.py --multi <out.mp4> <channel> <src0> [<src1> ...] -- <i:a:b> ...   (i = source index)
Frame-aligned trims of one source, concatenated into one continuous file (2160x3840, 4K),
chosen mic channel on both sides, 20 ms audio fades at every joint. Prints cut times."""
import sys, subprocess, json, os
PREVIEW = "--preview" in sys.argv  # 1080p fast encode for cut approval (4K only at execution)
if PREVIEW: sys.argv.remove("--preview")
RES = "1080:1920" if PREVIEW else "2160:3840"
# Default ending: the last segment's end = end of the last word; we add HOLD s of picture,
# then a FADE s fade to black. Audio fades right after the word so off-mic chatter never leaks in.
HOLD, FADE = 0.5, 0.7
NOFADE = "--no-fade" in sys.argv
if NOFADE: sys.argv.remove("--no-fade")
if sys.argv[1] == "--multi":
    out, ch = sys.argv[2], sys.argv[3]; sep = sys.argv.index("--")
    srcs = sys.argv[4:sep]; segs = sys.argv[sep + 1:]
else:
    src, out, ch, *segs = sys.argv[1:]; srcs = [src]; segs = ["0:" + s for s in segs]
src = srcs[0]
c = 0 if ch.upper() == "L" else 1
p = json.loads(subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=r_frame_rate","-of","json",src]))
n, d = map(int, p["streams"][0]["r_frame_rate"].split("/")); fps = n / d
rng = []
for s in segs:
    si, a, b = s.split(":"); a, b = float(a), float(b)
    if s is segs[-1] and not NOFADE: b += HOLD + FADE
    fa, fb = round(a * fps), round(b * fps); rng.append((int(si), fa / fps, fb / fps))
k = len(rng)
fc = []
for j in range(len(srcs)):
    use = [i for i, r in enumerate(rng) if r[0] == j]
    if not use: continue
    fc.append(f"[{j}:v]scale={RES}:flags=lanczos,format=yuv420p,split={len(use)}" + "".join(f"[v{i}]" for i in use) + ";")
    fc.append(f"[{j}:a]pan=stereo|c0=c{c}|c1=c{c},asplit={len(use)}" + "".join(f"[a{i}]" for i in use) + ";")
acc = 0.0; cuts = []
for i, (si, a, b) in enumerate(rng):
    dur = b - a
    fades = (",afade=t=in:d=0.02" if i > 0 else "") + (f",afade=t=out:st={dur-0.02:.4f}:d=0.02" if i < k - 1 else "")
    fc.append(f"[v{i}]trim={a:.6f}:{b:.6f},setpts=PTS-STARTPTS[x{i}];[a{i}]atrim={a:.6f}:{b:.6f},asetpts=PTS-STARTPTS{fades}[y{i}];")
    cuts.append((round(acc, 4), round(acc + dur, 4), round(a, 4), si)); acc += dur
if NOFADE:
    fc.append("".join(f"[x{i}][y{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=1[v][a]")
else:
    vf, af = acc - FADE, acc - HOLD - FADE
    fc.append("".join(f"[x{i}][y{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=1[vc][ac];"
              f"[vc]fade=t=out:st={vf:.4f}:d={FADE}:color=black[v];[ac]afade=t=out:st={af:.4f}:d=0.35[a]")
inputs = sum((["-i", x] for x in srcs), [])
subprocess.check_call(["ffmpeg","-v","error","-y",*inputs,"-filter_complex","".join(fc),"-map","[v]","-map","[a]",
    "-c:v","libx264","-crf","20" if PREVIEW else "14","-preset","veryfast" if PREVIEW else "medium","-g","12","-c:a","aac","-b:a","256k","-movflags","+faststart",out])
subprocess.check_call(["ffmpeg","-v","error","-y","-i",out,"-ac","1","-ar","16000",out.rsplit(".",1)[0]+".wav"])
print(json.dumps({"fps": fps, "total": round(acc, 4), "segments": [{"start": s, "end": e, "src": m, "file": f} for s, e, m, f in cuts]}))

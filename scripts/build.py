#!/usr/bin/env python3
"""build.py <project_dir> — renders <project>/creative.json into <project>/index.html via _kit/template.html.

creative.json:
  theme: "green" | "blue"
  duration: seconds (cut.json total)
  cam: [{start, end, s, cx}]          punch-in scale + face centre x (0..1) per segment
  captions: [[text, start, end], ...] static captions (auto-hidden under motions)
  motions: [{start, end, top, items: [{text, at, kind?, small?, check?, ring?}], arrow?}]
"""
import json, os, sys

proj = sys.argv[1]
kit = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(proj, "creative.json")))
html = open(os.path.join(kit, "template.html")).read()
adj = dict(cfg.get("adjust", {})); adj.setdefault("exposure", cfg.get("exposure", 0))  # grade tweaks: exposure / highlights / shadows …
html = html.replace("__ADJUST__", json.dumps(adj))
html = html.replace("__DURATION__", str(cfg["duration"])).replace("__CONFIG__", json.dumps(cfg, ensure_ascii=False, indent=2))
open(os.path.join(proj, "index.html"), "w").write(html)
print("built", os.path.join(proj, "index.html"))

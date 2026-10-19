#!/usr/bin/env python3
"""caps.py <project> [--max 26] — static caption groups from media/transcript.json (cut timeline).
Breaks at sentence punctuation, at pauses > 0.35 s, at every cut in media/cut.json, or when a line
would pass --max characters. Each group shows from its first word until the next group (≤ +0.5 s
after its last word). Prints JSON [[text, start, end], ...] and writes media/captions.json."""
import json, re, sys

p = sys.argv[1]
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 26
FIX = {"Eo": "E o", "Ea": "E a", "Eaí": "E aí", "Eaqui": "E aqui", "Eagora": "E agora",
       "agroperforma": "AgroPerforma", "Agroperforma": "AgroPerforma", "Agroperform": "AgroPerforma",
       "Blindado": "Blindada", "Blindado.": "Blindada.", "Eaí,": "E aí,", "Eaqui,": "E aqui,"}
j = json.load(open(f"{p}/media/transcript.json")); words = j if isinstance(j, list) else j["words"]
cuts = [s["start"] for s in json.load(open(f"{p}/media/cut.json"))["segments"]][1:]
groups, cur = [], []
def flush():
    if cur: groups.append(list(cur)); cur.clear()
for i, w in enumerate(words):
    t = FIX.get(w["text"], w["text"])
    if cur:
        gap = w["start"] - cur[-1]["end"]
        crossed = any(cur[-1]["end"] - 0.05 <= c <= w["start"] + 0.05 for c in cuts)
        line = " ".join(x["t"] for x in cur) + " " + t
        if gap > 0.35 or crossed or len(line) > MAX: flush()
    cur.append({"t": t, "start": w["start"], "end": w["end"]})
    if re.search(r"[.?!]$", t): flush()
flush()
# merge orphan groups (one short word or < 0.45 s) into the next group, or the previous if last
i = 0
while i < len(groups):
    g = groups[i]
    dur = g[-1]["end"] - g[0]["start"]; txt = " ".join(x["t"] for x in g)
    if (len(g) == 1 and len(txt) <= 7) or dur < 0.45:
        if i + 1 < len(groups) and len(txt + " " + " ".join(x["t"] for x in groups[i + 1])) <= MAX + 8:
            groups[i + 1] = g + groups[i + 1]; groups.pop(i); continue
        if i > 0:
            groups[i - 1] += g; groups.pop(i); continue
    i += 1
caps = []
for k, g in enumerate(groups):
    text = " ".join(x["t"] for x in g)
    start = g[0]["start"]
    nxt = groups[k + 1][0]["start"] if k + 1 < len(groups) else g[-1]["end"] + 0.5
    caps.append([text, round(start, 3), round(min(nxt, g[-1]["end"] + 0.5), 3)])
json.dump(caps, open(f"{p}/media/captions.json", "w"), ensure_ascii=False)
print(json.dumps(caps, ensure_ascii=False))

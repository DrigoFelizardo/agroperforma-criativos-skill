#!/usr/bin/env python3
"""AP-08 A/B/C: one shared body (times relative to version A) shifted by each hook's length."""
import json, subprocess
P = "/Volumes/AGROPERFORMA-HF/projetos"
A_HOOK = 1.251
HOOKS = {"a": ("Empresário do agro", 1.251), "b": ("Representante do agro", 1.376), "c": ("Homem do agro", 1.126)}
CAPS = [["você que está enfrentando", 1.12, 2.48], ["dificuldade de montar", 2.48, 3.68], ["time comercial,", 3.68, 4.68],
        ["que de repente", 4.68, 5.45], ["pessoas que criam", 11.9, 12.56], ["independência", 12.56, 13.48],
        ["e conseguem construir", 13.48, 15.05], ["e ser independente de suas vendas.", 15.05, 16.9], ["E o principal,", 16.9, 17.74],
        ["Eu, através desses", 25.26, 26.14], ["25 anos de experiência,", 26.14, 27.85], ["que vai fazer com que você possa", 30.04, 31.56],
        ["levar o seu negócio", 31.56, 32.58], ["para outro nível,", 32.58, 33.92], ["onde você possa construir", 33.92, 35.05],
        ["e você transformar o seu negócio.", 36.4, 38.24]]
MOT = [
 {"start": 5.45, "end": 6.78, "top": 900, "items": [{"text": "Tudo depende de você?", "at": 5.45}]},
 {"start": 6.78, "end": 11.85, "top": 860, "items": [{"text": "+25 anos de experiência", "at": 7.51},
    {"text": "Vendas no agronegócio", "at": 8.99, "kind": "secondary", "check": True},
    {"text": "Formando time campeão", "at": 10.23, "kind": "secondary", "check": True}]},
 {"start": 17.74, "end": 20.14, "top": 900, "items": [{"text": "Trazer resultado", "at": 17.76},
    {"text": "para o teu negócio", "at": 18.72, "kind": "secondary", "ring": 19.0}]},
 {"start": 20.14, "end": 25.26, "top": 900, "items": [{"text": "AgroPerforma", "at": 20.74},
    {"text": "O que limita seu crescimento?", "at": 23.55, "kind": "secondary", "small": True, "ring": 24.0}]},
 {"start": 27.85, "end": 30.04, "top": 900, "items": [{"text": "Método exclusivo", "at": 28.64, "ring": 29.0}]},
 {"start": 35.05, "end": 36.4, "top": 900, "items": [{"text": "Liberdade financeira", "at": 35.29}]},
 {"start": 38.24, "end": 999, "top": 940, "items": [{"text": "Venha fazer parte", "at": 38.3},
    {"text": "Clique em saiba mais", "at": 38.75, "kind": "secondary"}], "arrow": 39.05}]
CAM = [(1.251, 6.78, 1.0, 1.06), (6.78, 11.85, 1.18, 1.12), (11.85, 17.74, 1.05, 1.1), (17.74, 20.14, 1.28, 1.22),
       (20.14, 25.26, 1.0, 1.06), (25.26, 30.04, 1.2, 1.14), (30.04, 36.4, 1.06, 1.12), (36.4, 38.24, 1.25, 1.2), (38.24, 999, 1.12, 1.16)]
for v, (hook, hend) in HOOKS.items():
    d = hend - A_HOOK; sh = lambda t: round(t + d, 3)
    cut = json.load(open(f"{P}/ap08{v}/media/cut.json")); total = cut["total"]
    base = {"theme": "green", "exposure": 0.15,
            "cam": [{"start": 0, "end": hend, "s": 1.25, "to": 1.2, "cx": 0.5}] +
                   [{"start": sh(a), "end": min(total, sh(b)), "s": s, "to": t, "cx": 0.5} for a, b, s, t in CAM],
            "captions": [[c[0], sh(c[1]), sh(c[2])] for c in CAPS],
            "motions": [{"start": 0.0, "end": hend, "top": 900, "items": [{"text": hook, "at": 0.08}]}]}
    for m in MOT:
        mm = json.loads(json.dumps(m)); mm["start"] = sh(m["start"]); mm["end"] = sh(m["end"]) if m["end"] < 900 else 999
        for it in mm["items"]:
            it["at"] = sh(it["at"])
            if "ring" in it: it["ring"] = sh(it["ring"])
        if "arrow" in mm: mm["arrow"] = sh(mm["arrow"])
        base["motions"].append(mm)
    json.dump(base, open(f"{P}/ap08{v}/creative.base.json", "w"), ensure_ascii=False, indent=1)
    subprocess.check_call(["python3", f"{P}/_kit/mkcfg.py", f"{P}/ap08{v}"])

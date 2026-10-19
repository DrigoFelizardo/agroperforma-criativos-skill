#!/bin/zsh
# chunk.sh <wav> <a> <b> — word timings (whisper large-v3) for a short raw-audio window, in source seconds
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
D=$S/chunk; mkdir -p $D; ffmpeg -v error -y -i "$1" -ss $2 -to $3 $D/c.wav; rm -f $D/transcript.json
npx hyperframes transcribe $D/c.wav -m large-v3 -l pt --json -d $D >/dev/null 2>&1
node -e 'const j=JSON.parse(require("fs").readFileSync(process.argv[1]));const w=Array.isArray(j)?j:j.words;console.log(w.map(x=>(x.start+ +process.argv[2]).toFixed(2)+"-"+(x.end+ +process.argv[2]).toFixed(2)+" "+x.text).join(" | "))' $D/transcript.json $2

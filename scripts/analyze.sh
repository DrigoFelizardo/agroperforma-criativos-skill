#!/bin/zsh
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
# analyze.sh <project_dir>: faces per segment + word transcript of media/cut.wav
S=/Volumes/AGROPERFORMA-HF/_scratch
cd $1; id=$(basename $1); rm -rf $S/f_$id; mkdir -p $S/f_$id
ffmpeg -v error -i media/cut.mp4 -vf "fps=4,scale=720:1280" $S/f_$id/f_%04d.png && swift $S/faces.swift $S/f_$id > media/faces.txt
npx hyperframes transcribe media/cut.wav -m large-v3 -l pt --json -d media > /dev/null 2>&1
node -e '
const fs=require("fs");
const L=fs.readFileSync("media/faces.txt","utf8").trim().split("\n").map(l=>{const m=l.match(/f_(\d+).*cx=([\d.]+) cy=([\d.]+)/);return m?{t:(+m[1]-1)/4,cx:+m[2],cy:+m[3]}:null}).filter(Boolean);
fs.writeFileSync("media/faces.json",JSON.stringify(L));
const j=JSON.parse(fs.readFileSync("media/transcript.json"));const w=Array.isArray(j)?j:j.words;
console.log(w.map(x=>x.start.toFixed(2)+"-"+x.end.toFixed(2)+" "+x.text).join("\n"));'

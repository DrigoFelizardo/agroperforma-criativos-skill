#!/bin/zsh
# prep_lote.sh <pasta_brutos> <lote> — per raw file: L/R levels, keep louder channel, 16 kHz wav, transcript (large-v3), contact sheet
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
SRC="$1"; L="$S/batch_$2"; mkdir -p "$L"
for IN in "$SRC"/*.MP4; do
  b=$(basename "$IN" .MP4); [[ $b == ._* ]] && continue; D="$L/$b"; mkdir -p "$D"
  [ -s "$D/transcript.json" ] && { echo "SKIP $b"; continue; }
  ffmpeg -v error -y -i "$IN" -af "pan=mono|c0=c0" -ar 16000 "$D/L.wav"
  ffmpeg -v error -y -i "$IN" -af "pan=mono|c0=c1" -ar 16000 "$D/R.wav"
  l=$(ffmpeg -hide_banner -i "$D/L.wav" -af astats=metadata=0 -f null - 2>&1 | grep "RMS level dB" | tail -1 | awk '{print $NF}')
  r=$(ffmpeg -hide_banner -i "$D/R.wav" -af astats=metadata=0 -f null - 2>&1 | grep "RMS level dB" | tail -1 | awk '{print $NF}')
  ch=$(python3 -c "print('L' if float('$l')>float('$r') else 'R')"); echo "$b L=$l R=$r usar=$ch" > "$D/channels.txt"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  ffmpeg -v error -y -i "$IN" -vf "fps=16/$dur,scale=270:-1,tile=8x2" -frames:v 1 "$D/sheet.jpg"
  (cd "$D" && npx hyperframes transcribe $ch.wav -m large-v3 -l pt --json -d . >/dev/null 2>&1)
  echo "DONE $(cat $D/channels.txt)"
done
echo ALLDONE

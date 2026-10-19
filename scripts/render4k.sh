#!/bin/zsh
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
# render4k.sh <project> <OutName> — 4K 24fps delivery render, audio/format check, copy to SSD EDICAO
P=~/Movies/AGROPERFORMA-HF/$1; cd $P; mkdir -p renders; F=renders/$2.mp4
npx hyperframes render -q delivery --fps 24 --resolution portrait-4k -o $F 2>&1 | grep -E "MB ·|rror"
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of compact $F | tr '\n' ' '
ffmpeg -hide_banner -i $F -af "channelsplit[L][R];[L]astats=metadata=0[a];[R]astats=metadata=0[b];[a][b]amix" -f null - 2>&1 | grep "RMS level dB" | sort -u | awk '{print $NF}' | tr '\n' ' '
cp $F "${HF_DEST:-/Volumes/SSDDRIGO1/AGROPERFORMA/13 de OUT/Manhã/CRIATIVOS/SELECIONADOS/EDICAO}/" && echo "COPIED $2"

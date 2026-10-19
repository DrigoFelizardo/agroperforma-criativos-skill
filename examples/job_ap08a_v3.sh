#!/bin/zsh
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh; P=/Volumes/AGROPERFORMA-HF/projetos
export HF_DEST="/Volumes/SSDDRIGO1/AGROPERFORMA/11 de OUT/Criativos Instagram/EDICAO"
echo "[$(date +%H:%M)] render"
for try in 1 2; do $P/_kit/render4k.sh ap08a AP-08A_Empresario_v3_4K; [ -f "$HF_DEST/AP-08A_Empresario_v3_4K.mp4" ] && break; echo RETRY; sleep 20; done
$P/_kit/barscan.sh "$HF_DEST/AP-08A_Empresario_v3_4K.mp4" | sed 's/^/CHECK /'
echo "[$(date +%H:%M)] JOB_OK"

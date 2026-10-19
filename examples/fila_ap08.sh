#!/bin/zsh
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
export HF_DEST="/Volumes/SSDDRIGO1/AGROPERFORMA/11 de OUT/Criativos Instagram/EDICAO"
SRC="/Volumes/SSDDRIGO1/AGROPERFORMA/11 de OUT/Criativos Instagram/SELECIONADAS/RFZ2333.MP4"; P=/Volumes/AGROPERFORMA-HF/projetos
BODY=(7.85:11.60 11.70:18.35 18.60:19.55 19.70:25.10 25.20:27.25 36.49:38.22 49.46:52.85 53.34:53.62 56.85:59.40 59.50:63.15 63.25:68.20 68.30:71.25)
typeset -A HOOK NAME; HOOK=(a 0.83:2.10 b 3.40:4.80 c 5.90:7.00); NAME=(a Empresario b Representante c Homem-do-Agro)
for v in a b c; do
  [ -f "$HF_DEST/AP-08${(U)v}_${NAME[$v]}_v1_4K.mp4" ] && { echo "SKIP $v"; continue; }
  echo "[$(date +%H:%M)] AP-08${(U)v} corte 4K"
  cd $P/ap08$v && rm -f media/cut.mp4 && python3 ../_kit/cut.py "$SRC" media/cut.mp4 L ${HOOK[$v]} $BODY > media/cut.json && python3 ../_kit/mkcfg.py $PWD >/dev/null
  echo "[$(date +%H:%M)] AP-08${(U)v} render 4K"
  $P/_kit/render4k.sh ap08$v AP-08${(U)v}_${NAME[$v]}_v1_4K
done
echo "[$(date +%H:%M)] FILA_AP08_OK"

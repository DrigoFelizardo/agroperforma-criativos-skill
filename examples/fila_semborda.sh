#!/bin/zsh
# re-render dos vídeos com barra lateral (enquadramento quadro a quadro), um por vez, com checagem no fim
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
P=/Volumes/AGROPERFORMA-HF/projetos
E13="/Volumes/SSDDRIGO1/AGROPERFORMA/13 de OUT/Manhã/CRIATIVOS/SELECIONADOS/EDICAO"; E11="/Volumes/SSDDRIGO1/AGROPERFORMA/11 de OUT/Criativos Instagram/EDICAO"
JOBS=(
 "rfz2552|RFZ2552_AgroPerforma_v2_4K|$E13" "rfz2642a|RFZ2642A_AgroPerforma_v2_4K|$E13" "rfz2549|RFZ2549_AgroPerforma_v3_4K|$E13"
 "rfz2643|RFZ2643_AgroPerforma_v2_4K|$E13" "rfz2645|RFZ2645_AgroPerforma_v2_4K|$E13" "rfz2553|RFZ2553_AgroPerforma_v2_4K|$E13"
 "ap08a|AP-08A_Empresario_v2_4K|$E11" "ap08b|AP-08B_Representante_v2_4K|$E11" "ap08c|AP-08C_Homem-do-Agro_v2_4K|$E11"
 "rfz2640|FB-02_Aula-Fabrica-Blindada_v2_4K|$E13")
for j in $JOBS; do
  p=${j%%|*}; rest=${j#*|}; name=${rest%%|*}; dest=${rest#*|}
  [ -f "$dest/$name.mp4" ] && { echo "SKIP $name"; continue; }
  echo "[$(date +%H:%M)] $name"
  python3 $P/_kit/build.py $P/$p >/dev/null || { echo "ERRO build $p"; continue; }
  for try in 1 2; do HF_DEST="$dest" $P/_kit/render4k.sh $p $name; [ -f "$dest/$name.mp4" ] && break; echo "  RETRY $name"; sleep 20; done
  $P/_kit/barscan.sh "$dest/$name.mp4" | sed 's/^/  CHECK /'
done
echo "[$(date +%H:%M)] FILA_SEMBORDA_OK"

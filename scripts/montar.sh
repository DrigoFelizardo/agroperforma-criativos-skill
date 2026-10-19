#!/bin/zsh
# montar.sh — monta o volume de trabalho (APFS dentro do SSD) em /Volumes/AGROPERFORMA-HF
IMG="/Volumes/SSDDRIGO1/AGROPERFORMA/HyperFrames-Trabalho.sparsebundle"
if mount | grep -q "/Volumes/AGROPERFORMA-HF"; then echo "já montado"; exit 0; fi
[ -e "$IMG" ] || { echo "SSD SSDDRIGO1 não conectado ($IMG)"; exit 1; }
hdiutil attach "$IMG" -nobrowse -mountpoint /Volumes/AGROPERFORMA-HF | tail -1

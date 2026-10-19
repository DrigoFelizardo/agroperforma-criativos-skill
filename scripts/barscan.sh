#!/bin/zsh
# barscan.sh <video>... — per video: time ranges where the left/right 2 px edge is background-dark (exposed frame edge).
# The final 1.3 s (fade to black) is ignored.
for F in "$@"; do
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
  for side in L R; do
    [ $side = L ] && X=0 || X="iw-2"
    ffmpeg -nostdin -v error -i "$F" -vf "crop=2:ih*0.5:$X:ih*0.05,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -an -f null - | awk -v s=$side -v f="$(basename "$F")" -v D=$D '/pts_time/{split($0,a,"pts_time:");t=a[2]} /YAVG/{split($0,b,"=");if(b[2]<26 && t<D-1.3){n++; if(st=="")st=t; en=t} else if(st!=""){r=r sprintf(" %.1f–%.1f",st,en); st=""}} END{if(st!="")r=r sprintf(" %.1f–%.1f",st,en); printf "%-50.50s %s: %3d quadros%s\n",f,s,n+0,r}'
  done
done

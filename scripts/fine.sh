#!/bin/zsh
# fine.sh <wav> <a> <b> — 20 ms RMS strip (dB) of a raw-audio window, for locating stutters
ffmpeg -v error -i "$1" -af "atrim=$2:$3,asetpts=PTS-STARTPTS,asetnsamples=320,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - | awk -v a=$2 '/pts_time/{split($0,x,"pts_time:");t=x[2]+a} /RMS_level/{split($0,y,"=");v=y[2]; bar=""; n=int((v+70)/3); for(i=0;i<n;i++)bar=bar"#"; printf "%.2f %4d %s\n",t,v,bar}'

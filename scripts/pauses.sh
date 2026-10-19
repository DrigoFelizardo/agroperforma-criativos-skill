#!/bin/zsh
# usage: pauses.sh <wav> [thr=-42] [min=0.15]
W=$1; T=${2:--42}; M=${3:-0.15}
ffmpeg -v error -i $W -af "asetnsamples=800,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=$W.rms" -f null -
awk '/pts_time/{split($0,a,"pts_time:");t=a[2]} /RMS_level/{split($0,b,"=");printf "%.2f %s\n",t,b[2]}' $W.rms > $W.rms2
awk -v T=$T -v M=$M '{ if($2<T || $2=="-inf"){ if(s=="")s=$1; e=$1 } else { if(s!="" && e-s>=M) print "pausa", s, "->", e+0.05, "("e+0.05-s"s)"; if(!on){print "inicio fala", $1; on=1} s=""; last=$1 } } END{print "fim fala", last; if(s!="")print "pausa final", s}' $W.rms2

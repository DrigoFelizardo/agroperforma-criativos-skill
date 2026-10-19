#!/bin/zsh
source /Volumes/AGROPERFORMA-HF/projetos/_kit/env.sh
# usage: newproj.sh <id>
P=~/Movies/AGROPERFORMA-HF; id=$1
cd $P && [ -d $id ] || HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init $id --non-interactive --example=blank --skill=general-video --resolution=portrait >/dev/null 2>&1
cd $P/$id && mkdir -p media && cp -R $P/_kit/fonts . && cp $P/_kit/fundo-degrade.png $P/_kit/agroperforma1.cube media/ && npx hyperframes media-use resolve --type lut --from media/agroperforma1.cube --project . --json | tail -1

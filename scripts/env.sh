# source env.sh — tudo pesado (temporários, histórico, cache) no volume do SSD, nunca no Mac
mount | grep -q "/Volumes/AGROPERFORMA-HF" || zsh "${0:A:h}/montar.sh"
export TMPDIR=/Volumes/AGROPERFORMA-HF/_scratch/tmp; mkdir -p $TMPDIR
export HYPERFRAMES_HISTORY_ROOT=/Volumes/AGROPERFORMA-HF/cache/history
export HYPERFRAMES_EXTRACT_CACHE_DIR=/Volumes/AGROPERFORMA-HF/cache/extract
export HYPERFRAMES_FONT_CACHE_DIR=/Volumes/AGROPERFORMA-HF/cache/fonts
export S=/Volumes/AGROPERFORMA-HF/_scratch

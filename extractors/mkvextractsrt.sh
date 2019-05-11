#!/usr/bin/env bash

# Extract two subtitles from all MKV files using mkvtoolnix.
# You need run 'mkvinfo', figure out which tracks numbers and edit this file.

# Change 'track ID', 'language' manually. Choose tracks with `mkvinfo`.
lang1=(5 rus)  # track ID, language prefix. Will be shown at top of player
lang2=(7 eng)                             # Will be shiwn at bottom of player

OUTDIR="./Subs"  # ./Subtitles, ./subtitles, ./Subs, ./subs are valid for VLC
mkdir -p ${OUTDIR}

for video_file in *.mkv
do
  echo "Processing $video_file"
  mkvextract tracks "$video_file" \
    "${lang1[0]}:${OUTDIR}/${video_file}_${lang1[1]}.srt" \
    "${lang2[0]}:${OUTDIR}/${video_file}_${lang2[1]}.srt"
  langmix "${OUTDIR}/${video_file}_{${lang1[1]}:${lang2[1]}}.srt" --verbose
done

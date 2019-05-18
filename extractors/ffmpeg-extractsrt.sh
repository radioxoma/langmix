#!/usr/bin/env bash

E_NOARGS=65

usage="Automatically extract all subtitles from video file,
convert to SRT and put them in the specified folder. Usage:

    $(basename "$0") [-h] video.mkv output_folder

where:
    -h  show this help text"

if [[ $# -ne 2 ]] ; then
    echo "$usage"
    exit $E_NOARGS
fi

if [ ! -f "$1" ] ; then
    echo "File not found"
    exit 0
fi

filename=$(basename -- "${1}")
basename="${filename%.*}"

echo "Streams found:"
ffprobe -i "$1" -loglevel error \
-show_entries stream=index:stream_tags=language:stream_tags=title:\
stream=codec_type:stream=codec_long_name -of csv=p=0

streams=(`ffprobe -i "$1" -loglevel error -select_streams s \
    -show_entries stream=index:stream_tags=language -of csv=p=0`)

if [ ${#streams[@]} -eq 0 ]; then
    echo "No subtitles in file?"
    exit 0
else
    echo "Extracting subtitles as SRT..."
fi

# Generate ffmpeg parameters for subtitle extraction
args=()
for stream in "${streams[@]}"
do
    IFS=','
    read -ra i <<< "${stream//[$'\t\r\n']}"
    # unset IFS
    str=${i[0]}
    lng=${i[1]}
    # Stream numbers always present, so we use it at first position
    # in filename for convenient sorting in file manager
    args+=(-map 0:${str} "${2}/${basename}-${str}-${lng}.srt")
done

ffmpeg -i "$1" -loglevel error -stats -c:s srt ${args[@]}

#!/usr/bin/env bash

# Automatically extract all subtitles from video file, convert to SRT
# and put them in the specified folder

E_NOARGS=65

if [[ $# -eq 0 ]] ; then
    echo "Usage: '`basename $0` video.mkv output_folder'"
    exit $E_NOARGS
fi

# case "$1" in
#     --help) echo "Extract subtitles from given video and put it in a working directory" & exit 0;;
#     # *) echo 'you gave something else' ;;
# esac

if [ ! -f "$1" ] ; then
    echo "File not found"
    exit 0
fi

filename=$(basename -- "${1}")
basename="${filename%.*}"

echo 'Streams found:'
ffprobe -i "$1" -loglevel error -show_entries stream=index:stream_tags=language:stream_tags=title:stream=codec_type:stream=codec_long_name -of csv=p=0
echo

streams=(`ffprobe -i "$1" -loglevel error -select_streams s \
    -show_entries stream=index:stream_tags=language -of csv=p=0`)

if [ ${#streams[@]} -eq 0 ]; then
    echo "No subtitles?"
    exit 0
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

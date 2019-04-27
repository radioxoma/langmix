#!/usr/bin/env bash

# Automatically extract all subtitles from video file
# and put them in a working directory

if [[ $# -eq 0 ]] ; then
    echo "Video file name required"
    exit 0
fi

case "$1" in
    --help) echo "Extract subtitles from given video and put it in a working directory" & exit 0;;
    # *) echo 'you gave something else' ;;
esac

filepath="${1}"
filename=$(basename -- "${1}")
basename="${filename%.*}"

extract_subs() {
    # Generate ffmpeg parameters for subtitle extraction
    streams=(`ffprobe -loglevel error -select_streams s \
        -show_entries stream=index:stream_tags=language \
        -of csv=p=0 -i "${1}"`)

    # if [[ ${streams[@]} -eq 0 ]] ; then
    #     echo "No subtitles?"
    #     exit 0
    # fi

    local args=("-i ${filename} -c copy")

    for stream in "${streams[@]}"
    do
        IFS=','
        read -ra i <<< "${stream//[$'\t\r\n']}"
        unset IFS
        str=${i[0]}
        lng=${i[1]}
        # Stream numbers always present, so we use it at first position
        # in filename for convenient sorting in file manager
        args+=("-map 0:${str} ${basename}_${str}-${lng}.srt")
    done
    echo ${args[@]}
}

ffprobe -loglevel error -select_streams s \
        -show_entries stream=index:stream_tags=language \
        -of csv=p=0 -i ${filepath}
ffmpeg -loglevel error `extract_subs $filepath`

# langmix

Create multilanguage subtitles by merging two SRT video subtitles into one.
The tool is handy for language learning.

Subtitles from the first file will be shown at top (with smaller letters),
and subtitles from the second at bottom (with regular letters) of the screen.

Both GUI and featured command line interfaces are available.

Windows users can download [precompiled *ffmpeg*](https://ffmpeg.org/download.html). Make sure it in the system `PATH`.

## General how-to

1. Get the SRT files. Subtitles could be extracted more-or-less automatically with scripts from `extractors` folder.
2. Merge them with langmix.
3. Put the file along with movie or in the subfolder named "subtitles", "subs" (VLC convention).
4. Watch. [VLC](https://videolan.org) will load subtitle file automatically. Choose the right one by pressing <kbd>V</kbd>.


An example - extract subtitles from one file and merge them:

    $ mkdir subs
    $ ls
    Movie.mkv subs
    $ ffmpeg-extractsrt.sh Movie.mkv subs
    $ ls subs
    Movie-1-rus.srt Movie-2-eng.srt
    $ langmix  # Merge srt files in GUI


Batch procesing in Cygwin (e.g. for series):

    mkdir subs
    find . -type f -iname "*.mkv" -exec sh /cygdrive/c/dev/src/langmix/extractors/ffmpeg-extractsrt.sh {} subs/ \;
    $ langmix "True.Detective.s03e*.WEBDL.720p.NewStudio-{3-rus:4-eng}.srt"

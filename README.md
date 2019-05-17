# langmix

Create multilanguage subtitles by merging two SRT video subtitles into one.
The tool is handy for language learning.

Subtitles from the first file will be shown at top (with smaller letters),
and subtitles from the second at bottom (with regular letters) of the screen.

Both GUI and featured command line interfaces are available.

Intended to use with VideoLAN player. Unfortunately new VLC 3 and above doesn't support font tags in SRT files, so [version 2.2.8 is latest compatible](https://get.videolan.org/vlc/2.2.8/).

Windows users can install *mkvtoolnix* with [Cygwin](https://www.cygwin.com/) and download precompiled *ffmpeg* [here](https://ffmpeg.org/download.html).

## General how-to

1. Get the SRT files. Subtitles could be extracted more-or-less automatically with scripts from `extractors` folder.
2. Merge them with langmix.
3. Put the file along with movie or in the subfolder named "subtitles", "subs" (VLC convention).
4. Watch. VLC will load subtitle file automatically. Choose the right one by pressing <kbd>V</kbd>.


## An example - extract subtitles and merge them

    $ mkdir Subs
    $ ls
    Movie.mkv Subs
    $ ffmpeg-extractsrt.sh Movie.mkv Subs
    $ ls Subs
    Movie-1-rus.srt Movie-2-eng.srt
    $ langmix  # Merge srt files in GUI

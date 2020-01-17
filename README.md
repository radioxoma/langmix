# langmix

Create multilanguage subtitles by merging two SubRip SRT video subtitles into one.
The tool is handy for language learning. Both GUI and featured command line interfaces are available.

Subtitles from the first file will be shown at top (with smaller letters),
and subtitles from the second at bottom (with regular letters) of the screen.

## General how-to

1. Use `extractors/langmix-extractsrt.sh` to extract all subtitles from one video file as *SubRip SRT*
2. Merge SRT subtitles with `langmix` (GUI or cli batch mode)
3. Watch:
    * For [MPV](https://mpv.io/) put merged SRT file along with movie
    * For [VLC](https://videolan.org/) put merged SRT file along with movie or in the subfolder named "subtitles", "subs" (default VLC folder). Choose the right one by pressing <kbd>V</kbd>.

### Example 1. One movie
Simplest case: extract subtitles from one movie and merge them:

    $ mkdir subs
    $ ls
    Movie.mkv subs
    $ langmix-extractsrt.sh Movie.mkv subs
    $ ls subs
    Movie-1-rus.srt Movie-2-eng.srt
    $ langmix  # If no parameters given, will show GUI file dialogs

### Example 2. Batch processing for series
Extract subtitles from all video files:

    mkdir subs
    # For Linux
    find . -type f -iname "*.mkv" -exec langmix-extractsrt {} subs/ \;
    
    # Cygwin
    find . -type f -iname "*.mkv" -exec sh /cygdrive/c/dev/src/langmix/extractors/langmix-extractsrt.sh {} subs/ \;

Merge files, using filename mask (read `langmix --help`):

    $ cd subs
    $ langmix "True.Detective.s01e*720p-{3-rus:4-eng}.srt"


## Installation

### Windows

I personally recommend [Cygwin enviroment](https://www.cygwin.com/), as it helps install *git*, *python3-setuptools* and gives reasonable *cli* interface. Unfortunately it doesn't provide *ffmpeg*, so download it [here](https://ffmpeg.org/download.html) and add it in the system `PATH`.

    $ pip install https://github.com/radioxoma/heval/archive/master.zip


### Linux
> Tip: Archlinux [AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository/) package [`langmix-git`](https://aur.archlinux.org/packages/langmix-git/) available.

* `langmix` is written in pure python3 and uses tkinter for file dialogs
* `langmix-extractsrt.sh` just a wrapper around ffmpeg

Install dependencies and use scripts without installation:

    $ sudo apt install git python3-tk python3-pysrt  # Debian / Ubuntu
    $ sudo pacman -S git python tk python-pysrt  # Archlinux
    $ git clone https://github.com/radioxoma/langmix.git
    $ cd langmix

Run the scripts as described above:

    $ python3 ./langmix/langmix.py
    $ sh ./extractors/langmix-extractsrt.sh movie.mkv .

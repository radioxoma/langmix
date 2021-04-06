#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import difflib
import errno
import fnmatch
import os
import re
import sys
try:  # python 3
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
import pysrt  # https://github.com/byroot/pysrt


__description__ = """\
Create multilanguage subtitles by merging two SRT video subtitles into one.
The tool is handy for language learning.

Subtitles from the first file will be shown at top (with smaller letters by default),
and subtitles from the second at bottom (with regular letters by default) of the screen.

GUI
---
Just run the script without any parameters. You will be asked for two input
and one output SRT files.


Command line interface
----------------------

Allows batch processing by file mask. All subtitles must be in the same folder
and have similar names. E.g. for files:

    s01e01.Russian.srt
    s01e01.English.srt

You should specify mask which corresponds both of them. Mask must contain '{:}'
symbols e.g.: '{top:bottom}', so script will produce file with name
's01e01.XviD.AC3.RussianEnglish.srt'.

    $ python langmix.py "s01e01.{Russian:English}.srt"

You can use glob ('*') in file mask which is useful for video series.
An example for merging all subtitles for all episodes of first season (s01)
with saving to `subs` folder:

    $ python langmix.py "s01e*.{Russian:English}.srt" --out subs
"""

TOP_SRT_TEMPLATE = "{{\\an8}}{}"
FONT_SIZE_TEMPLATE = "<font size=\"{}\">{}</font>"
FONT_COLOR_TEMPLATE = "<font color=\"#{}\">{}</font>"
FONT_SIZE_COLOR_TEMPLATE = "<font size=\"{}\" color=\"#{}\">{}</font>"


def construct_fn(s1, s2, lang_top, lang_btm):
    """Return three SRT filenames: top, bottom, out.

    s1 must have {:} pattern to bring heuristic to work.
    """
    matcher = difflib.SequenceMatcher(None, s1, s2)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            # print("Replace '%s' from [%d:%d] of s1 with '%s' from [%d:%d]"
            #     " of s2" % (s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
            if s1[i1:i2] == "{:}":
                break

    filename2 = ''.join((s2[:j1], lang_btm, s2[j2:]))
    filename_out = ''.join((s2[:j1], lang_top + lang_btm, s2[j2:]))
    return s2, filename2, filename_out


def files_exist(*args):
    """Check if files exists in the file system.
    """
    do_exit = False
    for f in args:
        if not os.path.isfile(f):
            do_exit = True
            print("No such file: '{}'".format(f))

    if do_exit:
        sys.exit(1)


def join_srt_files(srt_top, srt_btm, srt_out, topsize=None, botsize=None, topcolor=None, botcolor=None):
    """Join two subtitles and save result.
    """
    def change_font(srts, size, color):
        if size is not None and color is not None:
            for i in srts:
                i.text = FONT_SIZE_COLOR_TEMPLATE.format(size, color, i.text)
        elif size is not None:
            for i in srts:
                i.text = FONT_SIZE_TEMPLATE.format(size, i.text)
        elif color is not None:
            for i in srts:
                i.text = FONT_COLOR_TEMPLATE.format(color, i.text)
        return srts

    top = change_font(pysrt.open(srt_top), topsize if topsize is not None else 16, topcolor)
    btm = change_font(pysrt.open(srt_btm), botsize, botcolor)

    merged = pysrt.SubRipFile(items=btm)
    for item in top:
        item.text = TOP_SRT_TEMPLATE.format(item.text)
        merged.append(item)

    merged.sort()
    merged.clean_indexes()
    merged.save(srt_out)


def main():
    # Simple file dialogs
    if len(sys.argv) == 1:
        print("If you would like to use the batch mode, please read `--help`.")
        root = Tk()
        root.withdraw()

        top_filepath = filedialog.askopenfilename(
            title='Choose top subtitle (small text size)',
            filetypes=[('SRT files', '.srt'), ('All files', '*')],
            initialdir=os.getcwd())
        if top_filepath:
            btm_filepath = filedialog.askopenfilename(
                title='Choose bottom subtitle (regular text size)',
                filetypes=[('SRT files', '.srt'), ('All files', '*')],
                initialdir=os.path.dirname(top_filepath))
        else:
            btm_filepath = None
        if btm_filepath:
            fname, ext = os.path.splitext(os.path.basename(top_filepath))
            dst_filepath = filedialog.asksaveasfilename(
                title='Output subtitle file',
                filetypes=[('SRT files', '.srt'), ('All files', '*')],
                defaultextension='.srt',
                initialdir=os.path.dirname(top_filepath),
                initialfile=fname + 'merged' + ext)
        else:
            dst_filepath = None
        if not all((top_filepath, btm_filepath, dst_filepath)):
            print("You didn't specify the files, exiting")
            sys.exit(0)
        join_srt_files(top_filepath, btm_filepath, dst_filepath)
        sys.exit(0)

    # CLI with bath processing
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mask", nargs=1, help="Mask of SRT files.")
    parser.add_argument("--out",help=(
            "Output directory. Will be created if not exists."
            " If not given, writes merged files in working directory."))
    parser.add_argument("--verbose", action='store_true', help="Print discovered file paths.")
    parser.add_argument("--topsize", type=int, help="Set font size for the top subtitle.")
    parser.add_argument("--botsize", type=int, help="Set font size for the bottom subtitle.")
    parser.add_argument("--topcolor", help="Set font color for the top subtitle.")
    parser.add_argument("--botcolor", help="Set font color for the bottom subtitle.")
    args = parser.parse_args()

    mask = os.path.basename(args.mask[0])
    srt_dir = os.path.dirname(os.path.abspath(args.mask[0]))

    languages = re.search("\{(.+?)\:(.+?)\}", mask)
    if not languages:
        print(
            "Passed invalid filename mask '{}'."
            " Consider reading `--help`.".format(mask))
        sys.exit(1)

    lang_top = languages.group(1)
    lang_btm = languages.group(2)

    mask_top = re.sub("\{.+?\}", lang_top, mask)
    mask_abstract = re.sub("\{.+?\}", '{:}', mask)

    if args.out:
        try:
            os.makedirs(args.out)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    topfiles = [f for f in os.listdir(srt_dir) if fnmatch.fnmatch(f, mask_top)]
    print("{} files".format(len(topfiles)))
    for fname in topfiles:
        names = construct_fn(mask_abstract, fname, lang_top, lang_btm)
        top_filepath = os.path.join(srt_dir, names[0])
        btm_filepath = os.path.join(srt_dir, names[1])
        if args.out:
            dst_filepath = os.path.join(args.out, names[2])
        else:
            dst_filepath = os.path.join(srt_dir, names[2])
        if args.verbose:
            print(top_filepath, btm_filepath, dst_filepath)
        files_exist(top_filepath, btm_filepath)
        join_srt_files(top_filepath, btm_filepath, dst_filepath, args.topsize, args.botsize, args.topcolor, args.botcolor)


if __name__ == '__main__':
    main()

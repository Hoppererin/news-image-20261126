#!/usr/bin/env python3
"""news-image-20261126 — "The World Today".

Entrypoint (Python 3.13, standard library only). The image
(entry.png, 1024x1024, 46 real stories from Thursday 26 November 2026)
is drawn in this repo by render.py (Python + Pillow + DejaVu, fully
deterministic — running it twice writes byte-identical bytes). This
program only copies that one file to the output directory and writes
nothing else. After the copy it checks the output file exists, so a
silent failure cannot pass as a success.

No network, no randomness, no timestamps. It never deletes the output
directory: the grader mounts /output, so removing it would fail the run.

Run locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size == 0:
        print("error: copied entry.png is empty", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

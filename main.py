#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry.

The grader runs this file with no network; it copies the finished
infographic (entry.png, drawn by draw.py at build time) into the
output directory. Both runs write identical bytes because the source
file never changes.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Copy the bytes explicitly (no metadata, no transforms) so every
    # run writes exactly the same file.
    with open(os.path.join(HERE, "entry.png"), "rb") as src:
        data = src.read()
    with open(os.path.join(out_dir, "entry.png"), "wb") as dst:
        dst.write(data)


if __name__ == "__main__":
    main()

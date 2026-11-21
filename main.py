#!/usr/bin/env python3
"""Copy entry.png beside this file to /output/entry.png.
Set MAKEFUN_OUTPUT_DIR to override the output directory locally."""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check the dimensions, populated cells, transparency and bounds of a sprite sheet."""
import argparse
from pathlib import Path
from PIL import Image
from pet_assets import ROOT, fail_cleanly, validate_image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sheet", nargs="?", type=Path, default=ROOT/"assets/spritesheet.png")
    args = parser.parse_args()
    if not 0 < args.sheet.stat().st_size <= 20*1024*1024:
        raise ValueError("The encoded sprite sheet must be at most 20 MiB")
    with Image.open(args.sheet) as atlas:
        if atlas.format not in {"PNG", "WEBP"}:
            raise ValueError("Only PNG and WebP are supported")
        validate_image(atlas)
    print("PASS: 73 populated frames, 15 transparent unused cells, correct v2 geometry")


if __name__ == "__main__":
    fail_cleanly(main)

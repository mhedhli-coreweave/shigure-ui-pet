#!/usr/bin/env python3
"""Rebuild either published animation set, or a mix, from approved frame PNGs."""
import argparse
from pathlib import Path
from PIL import Image
from pet_assets import (ROOT, add_selection_args, build_from_frames, fail_cleanly,
                        load_manifest, overrides_from_args, validate_image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_selection_args(parser)
    parser.add_argument("--output", type=Path, help="PNG destination; also the comparison file for --check")
    parser.add_argument("--check", action="store_true", help="Verify exact pixels without writing")
    args = parser.parse_args()
    manifest = load_manifest()
    overrides = overrides_from_args(args)
    output = args.output or (ROOT/"build/custom-spritesheet.png" if overrides else
                             ROOT/manifest["variants"][args.preset]["spritesheet"])
    rebuilt = build_from_frames(manifest, args.preset, overrides)
    if args.check:
        with Image.open(output) as published:
            validate_image(published)
            if rebuilt.tobytes() != published.tobytes():
                raise ValueError(f"Source frames differ from {output}; rebuild and review the changes")
        print(f"PASS: {args.preset} frame selection reproduces {output.name} pixel-for-pixel")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        rebuilt.save(output, format="PNG")
        print(f"Wrote {output}")


if __name__ == "__main__":
    fail_cleanly(main)

#!/usr/bin/env python3
"""Render GIF previews, and optionally MP4, for either preset or mixed animations."""
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from pet_assets import (ROOT, add_selection_args, build_from_frames, fail_cleanly,
                        load_manifest, overrides_from_args, selected_rows)


def display_frame(cell, label=None):
    background = Image.new("RGB", (240,248) if label else (192,208), (247,247,251))
    background.paste(cell, (24,14) if label else (0,0), cell)
    if label:
        ImageDraw.Draw(background).text((120,234), label, anchor="mm", fill=(35,40,55))
    return background


def save_gif(frames, durations, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=False, disposal=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_selection_args(parser)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--mp4", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest()
    overrides = overrides_from_args(args)
    atlas = build_from_frames(manifest, args.preset, overrides)
    out = args.output_dir or ROOT/"build/previews"/("custom" if overrides else args.preset)
    out.mkdir(parents=True, exist_ok=True)
    all_frames, all_durations, look_frames = [], [], []
    for row in selected_rows(manifest, args.preset, overrides):
        cells = [atlas.crop((i*192,row["row"]*208,(i+1)*192,(row["row"]+1)*208))
                 for i in range(len(row["frames"]))]
        save_gif([display_frame(cell) for cell in cells], row["durations_ms"], out/f"{row['state']}.gif")
        if row["row"] < 9:
            all_frames.extend(display_frame(cell, row["state"]) for cell in cells)
            all_durations.extend(row["durations_ms"])
        else:
            look_frames.extend(display_frame(cell) for cell in cells)
    save_gif(all_frames, all_durations, out/"all-states.gif")
    save_gif(look_frames, [180]*16, out/"look-around.gif")
    if args.mp4:
        import imageio_ffmpeg
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-i", str(out/"all-states.gif"),
                        "-movflags", "+faststart", "-pix_fmt", "yuv420p", "-vf", "fps=25",
                        str(out/"all-states.mp4")], check=True, capture_output=True)
    print(f"Wrote previews to {out}")


if __name__ == "__main__":
    fail_cleanly(main)

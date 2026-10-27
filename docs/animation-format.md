# Animation format and variants

The v2 atlas is a transparent **1536 × 2288 RGBA PNG**, with eight columns and eleven rows. Each cell is **192 × 208**. There are 73 used cells and 15 fully transparent unused cells.

| Row | State | Frames |
| --- | --- | ---: |
| 0 | Idle | 6 |
| 1 | Moving right | 8 |
| 2 | Moving left | 8 |
| 3 | Waving | 4 |
| 4 | Jumping | 5 |
| 5 | Failed | 8 |
| 6 | Waiting | 6 |
| 7 | Working (`running` in the manifest) | 6 |
| 8 | Review | 6 |
| 9 | Look 000° through 157.5° | 8 |
| 10 | Look 180° through 337.5° | 8 |

Look directions run clockwise in 22.5° steps. Zero is up, 90 is screen-right, 180 is down, and 270 is screen-left.

`pet.json` lists the More Dancing frames as the default row sources. The Original preset overrides only idle, waiting, working, and failed. A per-state selection overrides the chosen preset. Shared rows retain the same frame files, preventing accidental drift between variants.

## Dance source selection

| State | Source | Selected source frames |
| --- | --- | --- |
| Idle | Opening cycle of `Shigure Ui_1.gif` | 0, 3, 6, 9, 12, 15 |
| Waiting | `Shigure Ui_2.gif` | 0, 3, 6, 9, 12, 15 |
| Working | `Shigure Ui_dance.gif` | 0, 20, 52, 72, 98, 130 |

The source working animation has 151 frames over 10.07 seconds. Its six-pose version preserves selected choreography highlights rather than the complete motion or original timing. The failure reaction was generated as a new eight-pose sequence.

## Editing artwork

The saved frames are the reproducible build source. Generated strips and prompts preserve the creative inputs. Image generation is not deterministic, so repeating a prompt can produce a different result.

For a new visual revision, ground image generation in the canonical identity, inspect the complete animation strip, remove its chroma background, preserve a shared scale and baseline, and review the animation at native cell size. Use the Pets plugin's creation/update workflow for its full visual and upload checks. The repository's integrity checker only checks grid and alpha structure.

Both published sheets already passed that workflow. Rebuilding them from the supplied frames does not require a local Pets plugin installation or image-generation credentials.

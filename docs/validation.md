# Published asset validation

Both published sets were validated on 2026-10-27.

| Sheet | Encoded SHA-256 |
| --- | --- |
| Original | `62bebc95fa414f78e1bf2121e2b56b55fa650b6ac18f7bc86dbfa99d76cde24a` |
| More Dancing | `b782021d879ced38bbd1e5f12715a74327366c15b5f06c4522ac609cbcbd7314` |

The original Pets workflow passed its bundled atlas, alpha/chroma, standard-frame, jump-transition, direction-continuity, and final quality checks. Independent blind direction checks passed. Five intermediate gaze directions retain reviewed warnings for subtle directional components; all cardinal directions passed.

The dance update replaced rows 0, 5, 6 and 7. All other rows are pixel-identical to the original sheet. The replacement passed the same applicable structural and quality checks, and Pets preflight returned `valid: true`. The artwork downloaded after the update matched the submitted pixels.

The local build verifies exact RGBA pixels rather than encoded PNG bytes, because encoder versions may produce different compression for identical pixels. Tests also cover mixing original and new rows, missing required frames, occupied unused cells, and incorrect geometry. GIF and MP4 rendering passed locally. A ready-to-enable GitHub Actions template includes those same checks; it is not installed as an active workflow.

After editing artwork, regenerate previews and rerun checks before uploading through Pets.

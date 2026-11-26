# Report — news-image-20261126

Built on the morning of Thursday 26 November 2026 (WIB) by an AI agent
session. All files were written directly in the session.

## Files and hashes

| File | sha256 |
|---|---|
| `entry.png` | `9e2adede561b375368bb17327e390973f36241c24927721af4dddf5e20f08b64` |
| `render.py` | see `git show` / local `sha256sum` at submit time |
| `main.py` | see `git show` / local `sha256sum` at submit time |

- `entry.png`: 1024×1024 PNG, RGB, 190,495 bytes (under the 1 MiB gate).

## Verification performed

1. `python3 render.py` run twice: byte-identical `entry.png`
   (sha256 `9e2adede…08b64` both runs).
2. `MAKEFUN_OUTPUT_DIR=out python3 main.py` and
   `MAKEFUN_OUTPUT_DIR=out2 python3 main.py`: both copies byte-identical
   to `entry.png` (same sha256).
3. Visual check of `entry.png`: masthead, lead, 6 big-story cards, 7
   region briefs (39 stories) and footer all render legibly with no
   overlap; the "How to read" box sits clear of the footer.
4. Kit check: `node cli/makefun.mjs check --repo <dir> --worktree`
   (see the check output in the submission log).

## Content

46 real stories from 7 regions, all reported on 25–26 November 2026,
listed with sources in `RESEARCH.md`. Lead: US tariffs on 14 partners.

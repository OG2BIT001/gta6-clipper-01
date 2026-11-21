[![make.fun · gta6-clipper-01](https://make.fun/badge/gta6-clipper-01.svg)](https://make.fun/bounty/gta6-clipper-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)
[![rank](https://make.fun/badge/gta6-clipper-01/OG2BIT001/gta6-clipper-01/rank.svg)](https://make.fun/bounty/gta6-clipper-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)
[![reward](https://make.fun/badge/gta6-clipper-01/OG2BIT001/gta6-clipper-01/reward.svg)](https://make.fun/bounty/gta6-clipper-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)

# "This Game Is Absolute Cinema" — a GTA 6 clip, cut by an AI agent

The entry for make.fun's [gta6-clipper-01](https://make.fun/bounty/gta6-clipper-01) bounty
("Clip GTA 6 for the most YouTube views", $500). The video itself is the entry; this
repository names it in `VIDEO.json` and its `main.ts` hands that file to the grader.

## The clip

- **Moment:** the police chase in IShowSpeed's GTA 6 launch stream (19 Nov 2026) at
  10:41:26–10:42:04 — he orders shots at the tyres, the chase peaks, and he chants
  "this game is absolute cinema". One moment, chosen because it is self-contained,
  quotable and loops well: action, reaction and a catchphrase in 38 seconds.
- **Format:** 1080×1920 vertical — facecam strip on top, gameplay below, word-by-word
  captions with the spoken word highlighted, −14 LUFS. Opens mid-chase on the hook line.
- **The pitch:** a 6-second end card — "Make clips like this with AI and earn money on
  make.fun" with the bounty's address, `make.fun/bounty/gta6-clipper-01`.
- **Made by the agent, in session:** the moment was found by loudness-scanning the
  stream's audio and reading word-level transcripts; `render.py` in this repo is the
  exact program that cut and rendered `clip.mp4` with ffmpeg (trim, crops, ASS captions
  generated from the transcript, loudnorm, PIL pitch card, concat).

## Run it the way the grader does

```
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Copies `VIDEO.json` to `out/VIDEO.json` and prints nothing on success.

## Files

- `main.ts` — the entry program (Node 22, standard library only, from the kit starter)
- `VIDEO.json` — the YouTube address of the clip
- `render.py` — how the clip was cut and rendered
- `SESSION.md` — who built this, and how

MIT licensed — see `LICENSE`.

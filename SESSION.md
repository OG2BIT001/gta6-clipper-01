# Session notes — gta6-clipper-01

Built by **OG2BIT** (a Muse Spark agent in the Muse app) working for **Mateo**, for
make.fun's "Clip GTA 6 for the most YouTube views" bounty ($500, entries close
2026-11-23 01:00 UTC).

## How the clip was made (all in the agent's sessions)

1. **Finding the moment.** The source is IShowSpeed's GTA 6 launch stream
   (youtube.com/watch?v=qSyo5d-dVzA, 23h47m). The agent downloaded the audio track,
   scanned loudness in 5-second windows to find the biggest reactions, transcribed the
   top windows with faster-whisper (word-level timestamps), and read the transcripts.
2. **The choice.** The police chase at 10:41:26 — "shoot at the tires… this game is
   absolute cinema" — picked over the other candidates because it is one self-contained
   moment with a chantable catchphrase, not a montage.
3. **The creative.** Wizard-style vertical: facecam on top, gameplay below, word-by-word
   captions; hook first (mid-chase), then a 6-second pitch card carrying make.fun's
   pitch and the bounty address. Title: "This Game Is Absolute Cinema 😂 GTA 6 Chase".
4. **The render.** `render.py` (this repo) ran ffmpeg in-session: trim + split, facecam
   crop 392×246 at (0,459) → 1080×678, gameplay crop 940×1080 at (490,0) → 1080×1242,
   vstack, ASS captions generated from the transcript's word timestamps, loudnorm to
   −14 LUFS, then the PIL-drawn pitch card concatenated. Frames were extracted and
   inspected before upload.
5. **The upload.** The agent uploaded `clip.mp4` to Mateo's YouTube channel
   (@OG2BIT001) as a public Short, with the bounty's exact line and his play code
   (`makefun-warbler-blimp-cobalt`) in the description, then wrote the video's address
   into `VIDEO.json`.

`main.ts` is the kit starter's entry program, unchanged: it copies `VIDEO.json` to the
grader's output directory.

## Round 2 (2026-11-22)

Round 1 stalled at 27 views (rank ~1020 of 1821): 44s, slow open, pitch on an
end card. This session installed the claude-youtube skill
(github.com/AgriciDaniel/claude-youtube) and applied its Shorts playbook:
seed-audience test, hook in the first 1-3s, completion 70%+ and loops are
the gates. render2.py cuts stream 38503.8-38521.4 (17.6s): opens mid-chase
on "this game is absolute cinema", hook text from frame 1, make.fun pitch
as an on-screen overlay at 9-13s, hard cut after the final chant so it
loops. Rendered clip2.mp4 in this session; frames inspected.

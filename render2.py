#!/usr/bin/env python3
"""Render the gta6-clipper-01 round-2 clip, cut to the Shorts algorithm.

Creative decisions (from the claude-youtube skill's algorithm guide and
shorts playbook, installed this session):
- The Shorts feed tests each upload on a small seed audience; the gates are
  viewed-vs-swiped-away (hook must land in the first 1-3 seconds),
  completion (70%+ triggers aggressive promotion) and loops.
- Round 1 was 44s with a slow facecam open and the make.fun pitch on an
  end card most viewers never reached: 27 views, rank ~1020 of 1821.
- Round 2: 17.6s, opens mid-chase on the exact moment Speed shouts
  "this game is absolute cinema" (stream 38503.8-38521.4), big hook text
  from frame 1, the make.fun pitch as an on-screen overlay mid-clip
  (9-13s, during the wordless stretch), and a hard cut right after the
  final "absolute cinema... yes" so the chase loops back into the hook.

Source (fetched/cut in this agent's own earlier session):
  ~/workspace/clips-gta6-speed/sections/c4.mp4   (starts at stream 38470s)
  ~/workspace/clips-gta6-speed/cand/104140.json  (word timestamps)
  ~/workspace/clips-gta6-speed/audio.webm       (full-stream audio)
"""
import json, subprocess

WS = "/home/hatch/workspace/clips-gta6-speed"
OUT = "/home/hatch/workspace/makefun-bounties/entries/gta6-clipper-01"
START, END = 38503.8, 38521.4          # stream-time window
SEC_START = 38470.0                    # sections/c4.mp4 begins here
DUR = END - START

# ---------- 1. ASS: word captions + hook (frame 1) + pitch overlay ----------
words = []
for seg in json.load(open(f"{WS}/cand/104140.json"))["segments"]:
    for w in seg.get("words", []):
        if START <= w["s"] < END:
            words.append((w["s"] - START, w["e"] - START, w["w"].strip()))
assert len(words) >= 15, f"too few words: {len(words)}"

def ts(t):
    return f"{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}"

lines = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Cap,Lato Black,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,0,2,40,40,400,1",
    "Style: Hook,Lato Black,96,&H0000FFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,8,0,2,30,30,1150,1",
    "Style: Pitch,Lato Black,62,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,3,4,0,2,30,30,730,1",
    "", "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    f"Dialogue: 1,{ts(0.0)},{ts(3.2)},Hook,,0,0,0,,GTA 6 IS\\NABSOLUTE CINEMA!",
    f"Dialogue: 1,{ts(9.0)},{ts(13.2)},Pitch,,0,0,0,,AN AI AGENT CUT THIS CLIP\\N EARN MAKING YOURS ON MAKE.FUN ",
]
for i in range(0, len(words), 3):
    chunk = words[i:i + 3]
    for j, (s, e, w) in enumerate(chunk):
        text = " ".join(
            (f"{{\\c&H00FFFF&}}{cw}{{\\c&HFFFFFF&}}" if k == j else cw)
            for k, (_, _, cw) in enumerate(chunk)).upper()
        lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{text}")
open(f"{OUT}/clip2.ass", "w").write("\n".join(lines) + "\n")
print(f"captions: {len(words)} words, hook + pitch overlays written")

# ---------- 2. ffmpeg: compose, burn captions, loudnorm, single pass ----------
LOCAL = START - SEC_START
fc = (
    f"[0:v]trim=start={LOCAL}:duration={DUR},setpts=PTS-STARTPTS,split=2[fc][gp];"
    "[fc]crop=392:246:0:459,scale=1080:678[face];"
    "[gp]crop=940:1080:490:0,scale=1080:1242[game];"
    f"[face][game]vstack=inputs=2,fps=30,subtitles={OUT}/clip2.ass:fontsdir=/home/hatch/.clipwise/fonts[v];"
    "[1:a]asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1:LRA=11[a]"
)
subprocess.run([
    "ffmpeg", "-y", "-v", "error", "-i", f"{WS}/sections/c4.mp4",
    "-ss", str(START), "-t", str(DUR), "-i", f"{WS}/audio.webm",
    "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/clip2.mp4",
], check=True, capture_output=True)
print("rendered clip2.mp4")

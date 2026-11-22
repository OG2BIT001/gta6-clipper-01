#!/usr/bin/env python3
"""Render the gta6-clipper-01 round-3 clip: a DIFFERENT moment.

Mateo's direction (2026-11-22): round 2 was the same moment as round 1;
clip another one. Chosen moment: the "One Enemy Left" shootout from
IShowSpeed's GTA 6 launch stream, section c5 (starts at stream 46785s),
word timings in cand/125845.json.

Creative (claude-youtube shorts playbook, as round 2):
- Hook in the first 1-3s: opens on Speed's own line "There's only
  literally one more person left. There's no way I die" with big hook
  text from frame 1.
- Jump cuts keep a visual change every few seconds and cut the dead air:
  seg1 46799.5-46804.3 (the claim), seg2 46833.5-46842.7 (the hunt; chat
  roasts his "L AIM"), seg3 46845.3-46848.0 ("Where's he at?" button).
  Total ~16.7s.
- make.fun pitch as an on-screen overlay mid-clip (7.5-11.5s), not an
  end card. Hard cut at the end so it loops into the hook.
"""
import json, subprocess

WS = "/home/hatch/workspace/clips-gta6-speed"
OUT = "/home/hatch/workspace/makefun-bounties/entries/gta6-clipper-01"
SEC_START = 46785.0
SEGS = [(46799.5, 46804.3), (46833.5, 46842.7), (46845.3, 46848.0)]

# ---------- 1. ASS: captions on the joined timeline + hook + pitch ----------
allw = []
for seg in json.load(open(f"{WS}/cand/125845.json"))["segments"]:
    allw += seg.get("words", [])
allw.sort(key=lambda w: w["s"])

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
    f"Dialogue: 1,{ts(0.0)},{ts(3.4)},Hook,,0,0,0,,ONE ENEMY LEFT IN GTA 6\\NHE SAID HE CAN'T DIE",
    f"Dialogue: 1,{ts(7.5)},{ts(11.5)},Pitch,,0,0,0,,AN AI AGENT CUT THIS CLIP\\N EARN MAKING YOURS ON MAKE.FUN ",
]
offset = 0.0
for (s0, s1) in SEGS:
    words = [(w["s"], w["e"], w["w"].strip()) for w in allw if s0 <= w["s"] < s1]
    for i in range(0, len(words), 3):
        chunk = words[i:i + 3]
        for j, (s, e, w) in enumerate(chunk):
            text = " ".join(
                (f"{{\\c&H00FFFF&}}{cw}{{\\c&HFFFFFF&}}" if k == j else cw)
                for k, (_, _, cw) in enumerate(chunk)).upper()
            lines.append(f"Dialogue: 0,{ts(offset + s - s0)},{ts(offset + e - s0)},Cap,,0,0,0,,{text}")
    offset += s1 - s0
open(f"{OUT}/clip3.ass", "w").write("\n".join(lines) + "\n")
print(f"captions written; joined duration {offset:.1f}s")

# ---------- 2. ffmpeg: per-segment Wizard layout, concat, burn, loudnorm ----------
parts = ["[0:v]split=3[v0][v1][v2]", "[0:a]asplit=3[a0][a1][a2]"]
for i, (s0, s1) in enumerate(SEGS):
    loc, dur = s0 - SEC_START, s1 - s0
    parts.append(f"[v{i}]trim=start={loc}:duration={dur},setpts=PTS-STARTPTS,split=2[fc{i}][gp{i}]")
    parts.append(f"[fc{i}]crop=392:246:0:459,scale=1080:678[f{i}]")
    parts.append(f"[gp{i}]crop=940:1080:490:0,scale=1080:1242[g{i}]")
    parts.append(f"[f{i}][g{i}]vstack=inputs=2,fps=30[seg{i}]")
    parts.append(f"[a{i}]atrim=start={loc}:duration={dur},asetpts=PTS-STARTPTS[sa{i}]")
parts.append("[seg0][seg1][seg2]concat=n=3:v=1:a=0[catv]")
parts.append("[sa0][sa1][sa2]concat=n=3:v=0:a=1, loudnorm=I=-14:TP=-1:LRA=11[a]".replace(", ", ","))
parts.append(f"[catv]subtitles={OUT}/clip3.ass:fontsdir=/home/hatch/.clipwise/fonts[v]")
fc = ";".join(parts)
subprocess.run([
    "ffmpeg", "-y", "-v", "error", "-i", f"{WS}/sections/c5.mp4",
    "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/clip3.mp4",
], check=True, capture_output=True)
print("rendered clip3.mp4")

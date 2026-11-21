#!/usr/bin/env python3
"""Render the gta6-clipper-01 entry clip.

Moment: IShowSpeed's GTA 6 launch stream, 10:41:26-10:42:04 (stream time
38486-38524s) - the police chase where he shouts "shoot at the tires" and
chants "this game is absolute cinema". Source section and word-level
transcript were fetched/cut in this agent's own earlier session:
  ~/workspace/clips-gta6-speed/sections/c4.mp4      (starts at stream 38470s)
  ~/workspace/clips-gta6-speed/cand/104140.json     (word timestamps)

Format (Wizard style): 1080x1920, facecam strip on top, gameplay below,
word-by-word captions with the current word highlighted. Then a 6s pitch
card: "Make clips like this with AI and earn money on make.fun" +
make.fun/bounty/gta6-clipper-01. Loudness normalised to -14 LUFS.
"""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

WS = "/home/hatch/workspace/clips-gta6-speed"
OUT = "/home/hatch/workspace/makefun-bounties/entries/gta6-clipper-01"
START, END = 38486.0, 38524.0          # stream-time window of the moment
SEC_START = 38470.0                    # sections/c4.mp4 begins here
DUR = END - START

# ---------- 1. word-by-word ASS captions from the transcript ----------
words = []
for seg in json.load(open(f"{WS}/cand/104140.json"))["segments"]:
    for w in seg.get("words", []):
        if START <= w["s"] < END:
            words.append((w["s"] - START, w["e"] - START, w["w"].strip()))
assert len(words) > 20, f"too few words: {len(words)}"

def ts(t):
    return f"{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}"

lines = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Cap,Lato Black,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,0,2,40,40,400,1",
    "", "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
# group words into caption chunks of <=3 words; highlight the spoken word
for i in range(0, len(words), 3):
    chunk = words[i:i+3]
    for j, (s, e, w) in enumerate(chunk):
        text = " ".join(
            (f"{{\\c&H00FFFF&}}{cw}{{\\c&HFFFFFF&}}" if k == j else cw)
            for k, (_, _, cw) in enumerate(chunk)).upper()
        lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{text}")
open(f"{OUT}/clip.ass", "w").write("\n".join(lines) + "\n")
print(f"captions: {len(words)} words")

# ---------- 2. pitch card (PIL) ----------
W, H = 1080, 1920
img = Image.new("RGB", (W, H), (10, 10, 18))
d = ImageDraw.Draw(img)
def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)
def centre(y, text, f, fill):
    while d.textlength(text, font=f) > W - 80:   # auto-fit inside the frame
        f = font(f.size - 4)
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)
centre(560, "AN AI AGENT", font(64), (140, 220, 255))
centre(650, "CUT THIS CLIP", font(64), (140, 220, 255))
centre(820, "Make clips like this", font(88), (255, 255, 255))
centre(930, "with AI and earn money", font(88), (255, 255, 255))
centre(1060, "on make.fun", font(110), (255, 210, 60))
centre(1300, "make.fun/bounty/gta6-clipper-01", font(52, False), (200, 200, 210))
img.save(f"{OUT}/pitch.png")
print("pitch card drawn")

# ---------- 3. ffmpeg: compose moment, burn captions, append card ----------
LOCAL = START - SEC_START
# NOTE: c4.mp4's own audio stream is defective (it breaks the muxed encode);
# the proven recipe takes audio from the full-stream audio.webm instead.
fc = (
    f"[0:v]trim=start={LOCAL}:duration={DUR},setpts=PTS-STARTPTS,split=2[fc][gp];"
    "[fc]crop=392:246:0:459,scale=1080:678[face];"
    "[gp]crop=940:1080:490:0,scale=1080:1242[game];"
    f"[face][game]vstack=inputs=2,fps=30,subtitles={OUT}/clip.ass:fontsdir=/home/hatch/.clipwise/fonts[v];"
    "[1:a]asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1:LRA=11[a]"
)
import os
if not (os.path.exists(f"{OUT}/moment.mp4") and os.path.getsize(f"{OUT}/moment.mp4") > 1_000_000):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", f"{WS}/sections/c4.mp4",
        "-ss", str(START), "-t", str(DUR), "-i", f"{WS}/audio.webm",
        "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/moment.mp4",
    ], check=True, capture_output=True)
else:
    print("moment.mp4 already rendered, reusing")
subprocess.run([
    "ffmpeg", "-y", "-loop", "1", "-t", "6", "-i", f"{OUT}/pitch.png",
    "-f", "lavfi", "-t", "6", "-i", "anullsrc=r=44100:cl=stereo",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30",
    "-c:a", "aac", "-b:a", "128k", "-shortest", f"{OUT}/pitch.mp4",
], check=True, capture_output=True)
open(f"{OUT}/concat.txt", "w").write(f"file '{OUT}/moment.mp4'\nfile '{OUT}/pitch.mp4'\n")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/concat.txt",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
    f"{OUT}/clip.mp4",
], check=True, capture_output=True)
print("rendered clip.mp4")

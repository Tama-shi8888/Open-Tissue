#!/usr/bin/env python3
"""Generate impact subtitles (ASS + SRT) for assets/presentation.mp4.

Timings come from silence detection of the narration; text is hand-written.
[[...]] marks a keyword rendered large and gold.
"""
import re, sys, pathlib

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/subtitles")
GOLD = r"\c&H4AB8E6&"

# (start, end, text)
LINES = [
    (1.56, 2.18, "ティッシュは、"),
    (2.86, 3.95, "[[会社の顔]]。"),
    (4.57, 6.49, "オーダーメイドのティッシュを、ご提案します。"),
    (7.56, 10.15, "販促品は、使われないまま[[捨てられ]]、"),
    (10.75, 12.41, "[[記憶にも残らない]]。"),
    (13.61, 15.96, "[[御社だけ]]のティッシュボックスを、"),
    (16.33, 18.54, "箱のデザインからつくります。"),
    (19.84, 21.96, "定番の[[香り]]から、"),
    (22.50, 24.53, "ブランドの香りの再現、"),
    (25.07, 26.51, "オリジナル香料まで。"),
    (27.67, 29.58, "柔らかさは[[3グレード]]。"),
    (30.06, 33.52, "用途と予算で選べます。"),
    (35.40, 37.80, "[[ロゴ]]やメッセージを、"),
    (37.80, 40.40, "[[1枚1枚]]に印刷。"),
    (42.28, 44.30, "[[ホテル]]の客室では、"),
    (44.30, 46.37, "上質なアメニティに。"),
    (47.45, 48.92, "オフィスの[[受付]]では、"),
    (49.33, 51.45, "お客様への[[第一印象]]に。"),
    (52.92, 54.40, "[[ご家庭]]では、"),
    (54.40, 57.17, "毎日手に取るブランドに。"),
    (58.31, 59.57, "1日に何度も、"),
    (60.05, 61.83, "ブランドと[[触れ合う]]。"),
    (62.69, 64.39, "まずは[[無料サンプル]]から。"),
    (64.76, 66.51, "お気軽にご相談ください。"),
]
# (start, end, tag) chapter chips, top-left
TAGS = [
    (7.2, 12.6, "課題"),
    (13.3, 18.7, "01  BOX"),
    (19.6, 26.7, "02  SCENT"),
    (27.4, 34.4, "03  SOFTNESS"),
    (35.1, 40.6, "04  LOGO"),
    (42.0, 57.3, "SCENE"),
    (58.0, 66.6, "FREE SAMPLE"),
]
# big cinematic cards (centered): start, end, text
CARDS = [
    (0.15, 1.45, "ティッシュが、[[会社の顔]]になる。"),
    (67.6, 73.9, "[[無料サンプル]]受付中"),
]

def ts(t):
    cs = int(round(t * 100)); h, r = divmod(cs, 360000); m, r = divmod(r, 6000); s, c = divmod(r, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"

def srt_ts(t):
    ms = int(round(t * 1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def kw(text, size):
    return re.sub(r"\[\[(.+?)\]\]", lambda m: "{" + GOLD + rf"\fs{size}" + "}" + m.group(1) + r"{\r}", text)

header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,IPAGothic,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,1,0,1,6,4,2,40,40,64,1
Style: Tag,IPAGothic,32,&H00101010,&H00101010,&H004AB8E6,&H00000000,1,0,0,0,100,100,3,0,3,9,0,7,48,40,42,1
Style: Card,IPAGothic,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,4,0,1,6,4,8,40,40,90,1
Style: CardEnd,IPAGothic,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,3,0,1,5,3,2,40,40,56,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

ev = []
POP = r"{\fad(110,160)\fscx118\fscy118\t(0,170,\fscx100\fscy100)}"
for s, e, t in LINES:
    ev.append(f"Dialogue: 1,{ts(s)},{ts(e)},Main,,0,0,0,,{POP}{kw(t, 64)}")
for s, e, t in TAGS:
    ev.append(f"Dialogue: 2,{ts(s)},{ts(e)},Tag,,0,0,0,,{{\\fad(200,200)\\move(20,52,48,52,0,260)}}{t} ")
for s, e, t in CARDS:
    st = "Card" if s < 10 else "CardEnd"
    ev.append(f"Dialogue: 3,{ts(s)},{ts(e)},{st},,0,0,0,,{{\\fad(300,400)\\fscx92\\fscy92\\t(0,{int((e-s)*1000)},\\fscx104\\fscy104)}}{kw(t, 72 if s < 10 else 62)}")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "ja.ass").write_text(header + "\n".join(ev) + "\n", encoding="utf-8")
with open(OUT / "ja.srt", "w", encoding="utf-8") as f:
    for i, (s, e, t) in enumerate(LINES, 1):
        f.write(f"{i}\n{srt_ts(s)} --> {srt_ts(e)}\n{t.replace('[[','').replace(']]','')}\n\n")
print("ok", len(LINES))

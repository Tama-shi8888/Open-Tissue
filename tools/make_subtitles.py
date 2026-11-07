#!/usr/bin/env python3
"""Generate impact subtitles + creative overlays (ASS + SRT) for the promo video.

usage: make_subtitles.py OUT_DIR [INSERT_LEN]
Timings come from silence detection of the narration; text is hand-written.
[[...]] marks a keyword rendered large and gold.
"""
import re, sys, random, pathlib

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/subtitles")
D = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0   # length of inserted examples segment
INSERT_AT = 57.8
STEP = 2.25      # seconds per example image (4 beats @ 106.67 bpm)
MOSAIC_AT = 4 * STEP
GOLD = r"\c&H4AB8E6&"

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
TAGS = [
    (7.2, 12.6, "課題"),
    (13.3, 18.7, "01  BOX"),
    (19.6, 26.7, "02  SCENT"),
    (27.4, 34.4, "03  SOFTNESS"),
    (35.1, 40.6, "04  LOGO"),
    (42.0, 57.3, "SCENE"),
    (58.0, 66.6, "FREE SAMPLE"),
]
CARDS = [(67.6, 73.9, "[[無料サンプル]]受付中")]
EXAMPLES = [
    ("[[アウトドア]]の世界観を、1箱に。", "OUTDOOR"),
    ("ロボット型の[[おもしろ造形]]も。", "CHARACTER"),
    ("ホテルの[[格]]を、触れるものに。", "HOTEL"),
    ("[[ロゴ]]を、ティッシュ1枚1枚に。", "LOGO PRINT"),
]

def shift(items):
    return [(a + D if a >= INSERT_AT else a, b + D if a >= INSERT_AT else b, *r) for a, b, *r in items]

LINES, TAGS, CARDS = shift(LINES), shift(TAGS), shift(CARDS)

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
Style: Main,IPAGothic,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,1,0,1,6,4,2,40,40,64,1
Style: Tag,IPAGothic,32,&H00101010,&H00101010,&H004AB8E6,&H00000000,1,0,0,0,100,100,3,0,3,9,0,7,48,40,42,1
Style: Card,IPAGothic,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,4,0,1,6,4,8,40,40,90,1
Style: CardEnd,IPAGothic,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,3,0,1,5,3,2,40,40,56,1
Style: Note,IPAGothic,24,&H00F0F0F0,&H00F0F0F0,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,3,1,9,40,36,40,1
Style: Num,IPAGothic,150,&H66FFFFFF,&H66FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,3,40,48,30,1
Style: Glitch,IPAGothic,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,6,0,1,5,0,5,40,40,40,1
Style: Print,IPAGothic,30,&H00707070,&H00707070,&H00FFFFFF,&H00000000,1,0,0,0,100,100,5,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

ev = []
POP = r"{\fad(110,160)\fscx118\fscy118\t(0,170,\fscx100\fscy100)}"
ACC = r"{\an5\pos(640,574)\p1\bord0\shad0\1c&H4AB8E6&\fscx0\t(0,280,\fscx100)\fad(0,140)}m -46 0 l 46 0 46 3 -46 3{\p0}"
def accent(a, b):
    return f"Dialogue: 0,{ts(a)},{ts(b)},Main,,0,0,0,,{ACC}"
def dlg(layer, a, b, style, text, name=""):
    return f"Dialogue: {layer},{ts(a)},{ts(b)},{style},{name},0,0,0,,{text}"

# --- cold open: glitch "捨てられる" -> "愛される" (0.15 - 1.5s, narration starts at 1.56)
rnd = random.Random(11)
t = 0.15
while t < 0.80:
    a, b = t, min(t + 0.06, 0.80)
    dx, dy = rnd.randint(-9, 9), rnd.randint(-5, 5)
    pos = lambda ox: rf"\an5\pos({640 + dx + ox},{150 + dy})"
    ev.append(dlg(2, a, b, "Glitch", "{" + pos(-5) + r"\1c&H3030FF&\alpha&H70&\blur1}捨てられる"))
    ev.append(dlg(2, a, b, "Glitch", "{" + pos(5) + r"\1c&HFFFF30&\alpha&H70&\blur1}捨てられる"))
    ev.append(dlg(3, a, b, "Glitch", "{" + pos(0) + r"\1c&HB0B0B0&}捨てられる"))
    t += 0.06
ev.append(dlg(4, 0.55, 0.80, "Glitch", r"{\an5\pos(640,150)\p1\bord0\1c&H3030FF&\fscx0\t(0,200,\fscx100)}m -280 -3 l 280 -3 280 3 -280 3{\p0}"))
ev.append(dlg(3, 0.80, 1.50, "Glitch", r"{\an5\pos(640,150)\fad(60,380)\fsp40\fscx90\fscy90\t(0,500,\fsp8\fscx100\fscy100)" + GOLD + r"\fs112}愛される"))
# --- subtitles
for s, e, text in LINES:
    ev.append(dlg(1, s, e, "Main", POP + kw(text, 68)))
    ev.append(accent(s, e))
for s, e, text in TAGS:
    ev.append(dlg(2, s, e, "Tag", "{\\fad(200,200)\\move(20,52,48,52,0,260)}" + text + " "))
for s, e, text in CARDS:
    ev.append(dlg(3, s, e, "CardEnd", "{\\fad(300,400)\\fsp44\\t(0," + str(int((e - s) * 700)) + ",\\fsp4)}" + kw(text, 62)))
# --- "YOUR LOGO" printing onto the tissue, tile by tile (scene 0:35-0:40)
cols, rows = 5, 3
idx = 0
for r in range(rows):
    for c in range(cols):
        x = 300 + c * 170 + (85 if r % 2 else 0)
        y = 175 + r * 150
        a = 35.55 + idx * 0.16
        ev.append(dlg(0, a, 40.40, "Print", rf"{{\an5\pos({x},{y})\frz-16\fad(150,250)\alpha&H40&\fscx130\fscy130\t(0,220,\fscx100\fscy100)}}YOUR LOGO"))
        idx += 1
# --- examples segment
if D:
    for k, (text, cat) in enumerate(EXAMPLES):
        a = INSERT_AT + k * STEP + 0.10
        ev.append(dlg(1, a, a + 2.0, "Main", POP + kw(text, 68)))
        ev.append(accent(a, a + 2.0))
        ev.append(dlg(2, a - 0.05, a + 2.2, "Tag", f"{{\\fad(150,150)\\move(20,52,48,52,0,200)}}0{k+1} / 04  {cat} "))
        ev.append(dlg(0, a - 0.05, a + 2.2, "Num", f"{{\\fad(200,200)\\fscx110\\fscy110\\t(0,600,\\fscx100\\fscy100)}}0{k+1}"))
    m = INSERT_AT + MOSAIC_AT
    ev.append(dlg(1, m + 0.35, INSERT_AT + D - 0.03, "Main", POP + kw("[[あなたのブランド]]も、ここに。", 68)))
    ev.append(accent(m + 0.35, INSERT_AT + D - 0.03))
    ev.append(dlg(2, m + 0.1, INSERT_AT + D - 0.03, "Tag", "{\\fad(150,150)\\move(20,52,48,52,0,200)}YOUR BRAND, HERE "))
    ev.append(dlg(2, INSERT_AT + 0.1, INSERT_AT + MOSAIC_AT, "Note", "※デザイン例(イメージ)です。掲載ブランドの導入実績を示すものではありません。"))
    ev.append(dlg(2, m + 0.1, INSERT_AT + D - 0.1, "Note", "※デザイン例(イメージ)です。掲載ブランドの導入実績を示すものではありません。"))

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "ja.ass").write_text(header + "\n".join(ev) + "\n", encoding="utf-8")
with open(OUT / "ja.srt", "w", encoding="utf-8") as f:
    for i, (s, e, text) in enumerate(LINES, 1):
        f.write(f"{i}\n{srt_ts(s)} --> {srt_ts(e)}\n{text.replace('[[','').replace(']]','')}\n\n")
print("ok", len(LINES), "events", len(ev))

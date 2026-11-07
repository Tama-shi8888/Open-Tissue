#!/usr/bin/env bash
# Build assets/presentation_ja_examples.mp4:
# original video + "order examples" cuts inserted before the CTA, impact subtitles,
# colour grade (vignette + grain) and an original BGM ducked under the narration.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/presentation.mp4
INSERT_AT=57.8
W=$(mktemp -d)
FONTS=/usr/share/fonts/opentype/ipafont-gothic
IMGS=(assets/examples/01_nanga.jpg assets/examples/02_kobe_choco.jpg assets/examples/03_ritz_carlton.jpg assets/examples/04_marriott.jpg)
FR=60   # 2.5s per image at 24fps; 0.25s transitions; one cut every 2.25s = 4 beats @106.67bpm

# 1) each image -> 16:9 clip: blurred backdrop + fitted foreground (logos never cropped) + slow push/pull
for i in 0 1 2 3; do
  if (( i % 2 == 0 )); then Z="1+0.08*on/$FR"; else Z="1.08-0.08*on/$FR"; fi
  ffmpeg -v error -y -i "${IMGS[$i]}" -filter_complex \
   "[0]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:6,eq=brightness=-0.2[bg];[b]scale=1760:990:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,zoompan=z='$Z':d=$FR:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24,format=yuv420p" \
   -c:v libx264 -crf 16 -preset medium -r 24 "$W/i$i.mp4"
done
# 1b) 2x2 mosaic of all four, tiles popping in one by one, hairlines in gold
ffmpeg -v error -y -f lavfi -i color=c=black:s=1280x720:d=2.25:r=24 \
 -loop 1 -framerate 24 -t 2.25 -i "${IMGS[0]}" -loop 1 -framerate 24 -t 2.25 -i "${IMGS[1]}" \
 -loop 1 -framerate 24 -t 2.25 -i "${IMGS[2]}" -loop 1 -framerate 24 -t 2.25 -i "${IMGS[3]}" -filter_complex "
 [1:v]split[a1][b1];[a1]scale=640:360:force_original_aspect_ratio=increase,crop=640:360,boxblur=14:3,eq=brightness=-0.2[g1];[b1]scale=600:338:force_original_aspect_ratio=decrease[f1];[g1][f1]overlay=(W-w)/2:(H-h)/2,format=yuva420p,fade=in:st=0.00:d=0.2:alpha=1[t1];
 [2:v]split[a2][b2];[a2]scale=640:360:force_original_aspect_ratio=increase,crop=640:360,boxblur=14:3,eq=brightness=-0.2[g2];[b2]scale=600:338:force_original_aspect_ratio=decrease[f2];[g2][f2]overlay=(W-w)/2:(H-h)/2,format=yuva420p,fade=in:st=0.28:d=0.2:alpha=1[t2];
 [3:v]split[a3][b3];[a3]scale=640:360:force_original_aspect_ratio=increase,crop=640:360,boxblur=14:3,eq=brightness=-0.2[g3];[b3]scale=600:338:force_original_aspect_ratio=decrease[f3];[g3][f3]overlay=(W-w)/2:(H-h)/2,format=yuva420p,fade=in:st=0.56:d=0.2:alpha=1[t3];
 [4:v]split[a4][b4];[a4]scale=640:360:force_original_aspect_ratio=increase,crop=640:360,boxblur=14:3,eq=brightness=-0.2[g4];[b4]scale=600:338:force_original_aspect_ratio=decrease[f4];[g4][f4]overlay=(W-w)/2:(H-h)/2,format=yuva420p,fade=in:st=0.84:d=0.2:alpha=1[t4];
 [0:v][t1]overlay=0:0[o1];[o1][t2]overlay=640:0[o2];[o2][t3]overlay=0:360[o3];[o3][t4]overlay=640:360,
 drawbox=x=638:y=0:w=4:h=720:color=0xE6B84A@0.9:t=fill,drawbox=x=0:y=358:w=1280:h=4:color=0xE6B84A@0.9:t=fill,format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -crf 16 -r 24 $W/mosaic.mp4
# 2) punchy transitions, one cut every 4 beats; flash into the mosaic
ffmpeg -v error -y -i $W/i0.mp4 -i $W/i1.mp4 -i $W/i2.mp4 -i $W/i3.mp4 -i $W/mosaic.mp4 -filter_complex \
 "[0][1]xfade=transition=smoothleft:duration=0.25:offset=2.25[x1];[x1][2]xfade=transition=zoomin:duration=0.25:offset=4.5[x2];[x2][3]xfade=transition=smoothup:duration=0.25:offset=6.75[x3];[x3][4]xfade=transition=fadewhite:duration=0.25:offset=9.0,format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -crf 16 -r 24 $W/ins_v.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $W/ins_v.mp4)
ffmpeg -v error -y -i $W/ins_v.mp4 -f lavfi -t "$D" -i anullsrc=r=48000:cl=stereo -c:v copy -c:a aac -shortest $W/ins.mp4
# 3) split source at the pause before the CTA narration, concat
ffmpeg -v error -y -to $INSERT_AT -i $SRC -c:v libx264 -crf 16 -preset medium -r 24 -c:a aac -ar 48000 -ac 2 $W/a.mp4
ffmpeg -v error -y -ss $INSERT_AT -i $SRC -c:v libx264 -crf 16 -preset medium -r 24 -c:a aac -ar 48000 -ac 2 $W/b.mp4
printf "file '%s'\nfile '%s'\nfile '%s'\n" $W/a.mp4 $W/ins.mp4 $W/b.mp4 > $W/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $W/list.txt -c copy $W/joined.mp4
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $W/joined.mp4)
# 4) subtitles + BGM
python3 -I tools/make_subtitles.py assets/subtitles "$D"
python3 -I tools/make_bgm.py $W/bgm.wav "$TOTAL" "$INSERT_AT" "$(python3 -c "print($INSERT_AT+$D)")"
# 5) grade + burn subtitles, mix BGM with ducking
ffmpeg -v error -y -i $W/joined.mp4 -i $W/bgm.wav -filter_complex \
 "[0:v]eq=contrast=1.05:saturation=1.06,vignette=PI/6,noise=alls=4:allf=t+u,ass=assets/subtitles/ja.ass:fontsdir=$FONTS[v];
  [0:a]asplit[n1][n2];
  [1:a]aecho=0.8:0.6:70|140:0.22|0.12,volume=0.9[bg];
  [bg][n2]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=600[duck];
  [n1][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 22 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k assets/presentation_ja_examples.mp4
echo "built, inserted ${D}s, total ${TOTAL}s"

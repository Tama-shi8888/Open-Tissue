#!/usr/bin/env python3
"""音声: tts(合成) / stt(文字起こし) (OpenAI Audio API)。
例: voice.py tts "こんにちは" -o assets/hello.mp3 / voice.py stt meeting.mp3"""
import argparse, json
from pathlib import Path
from _common import need, post_json, request, multipart
ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["tts", "stt"]); ap.add_argument("input")
ap.add_argument("-o", default="assets/out.mp3"); ap.add_argument("--voice", default="alloy")
a = ap.parse_args(); H = {"Authorization": "Bearer " + need("VOICE_API_KEY")}
if a.mode == "tts":
    body, _ = post_json("https://api.openai.com/v1/audio/speech",
        {"model": "gpt-4o-mini-tts", "voice": a.voice, "input": a.input}, H)
    Path(a.o).write_bytes(body); print("saved", a.o)
else:
    data, ct = multipart({"model": "whisper-1"}, {"file": (Path(a.input).name, Path(a.input).read_bytes())})
    body, _ = request("https://api.openai.com/v1/audio/transcriptions", {**H, "Content-Type": ct}, data, "POST")
    print(json.loads(body)["text"])

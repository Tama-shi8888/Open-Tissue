#!/usr/bin/env python3
"""Synthesize an original cinematic BGM (no external samples): pad + sub + pulse + pluck.

usage: make_bgm.py OUT.wav DURATION_SEC [BUILD_START BUILD_END]
Energy builds between BUILD_START..BUILD_END (the "examples" section), then settles for the CTA.
"""
import sys, wave
import numpy as np

SR = 48000
out = sys.argv[1]
T = float(sys.argv[2])
B0 = float(sys.argv[3]) if len(sys.argv) > 3 else 57.8
B1 = float(sys.argv[4]) if len(sys.argv) > 4 else 69.0
N = int(T * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
BPM = 106.6667   # 4 beats = 2.25s = one example cut
beat = 60.0 / BPM
phase = B0 % beat   # beat grid is aligned so the examples start exactly on a beat
MOS = B1 - 2.25     # mosaic start

def hz(m):  # midi -> Hz
    return 440.0 * 2 ** ((m - 69) / 12)

# Am - F - C - G, 2 bars (8 beats) each
prog = [(57, [57, 60, 64, 67]), (53, [53, 57, 60, 64]), (48, [60, 64, 67, 72]), (55, [55, 59, 62, 67])]
chord_len = 8 * beat

def smooth(x, n):
    k = np.ones(n) / n
    return np.convolve(x, k, mode="same")

pad = np.zeros(N); sub = np.zeros(N)
for ci in range(int(T / chord_len) + 2):
    root, notes = prog[ci % 4]
    s = int((phase + ci * chord_len) * SR); e = min(N, int((phase + (ci + 1) * chord_len) * SR) + int(1.2 * SR))
    if s >= N: break
    tt = np.arange(e - s) / SR
    env = np.minimum(1, tt / 1.6) * np.exp(-np.maximum(0, tt - chord_len) * 3.0)
    seg = np.zeros(e - s)
    for m in notes:
        for det in (-0.12, 0.12):
            f = hz(m) * 2 ** (det / 12)
            seg += np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) + 0.12 * np.sin(2 * np.pi * 3 * f * tt)
    pad[s:e] += seg * env / 8
    sub[s:e] += np.sin(2 * np.pi * hz(root - 12) * tt) * env
pad *= 0.55 + 0.25 * np.sin(2 * np.pi * t / 9.0)  # slow swell
sub *= 0.55

# energy curve: 0.35 at start, rising into the examples, high during, back to 0.5 for CTA
energy = np.interp(t, [0, 40, B0 - 2, B0, B1, B1 + 3, T], [0.25, 0.45, 0.6, 1.0, 1.0, 0.6, 0.35])

# kick + hat + pluck
kick = np.zeros(N); hat = np.zeros(N); pluck = np.zeros(N)
def add(buf, start, sig):
    s = int(start * SR)
    if s >= N: return
    e = min(N, s + len(sig)); buf[s:e] += sig[: e - s]

kt = np.arange(int(0.45 * SR)) / SR
kick_sig = np.sin(2 * np.pi * (45 * kt + 70 * (1 - np.exp(-kt * 28)) / 28 * 1.0)) * np.exp(-kt * 9)
ht = np.arange(int(0.07 * SR)) / SR
hat_sig = rng.standard_normal(len(ht)) * np.exp(-ht * 70)
hat_sig = hat_sig - smooth(hat_sig, 6)  # crude high-pass
pt = np.arange(int(0.9 * SR)) / SR
arp_notes = {0: [69, 72, 76, 72], 1: [65, 69, 72, 69], 2: [72, 76, 79, 76], 3: [67, 71, 74, 71]}

nb = int(T / beat) + 1
for b in range(nb):
    tb = phase + b * beat
    ev = float(np.interp(tb, [0, 40, B0 - 2, B0, B1, B1 + 3, T], [0.25, 0.45, 0.6, 1.0, 1.0, 0.6, 0.35]))
    on_kick = (b % 2 == 0) if ev < 0.8 else True
    if tb > 6 and on_kick:
        add(kick, tb, kick_sig * (0.5 + 0.5 * ev))
    if tb > 20:
        for h in (0.5,) if ev < 0.8 else (0.0, 0.5):
            add(hat, tb + h * beat, hat_sig * (0.12 + 0.12 * ev))
    ci = int((tb - phase) // chord_len) % 4
    if tb > 12:
        for q in range(2):
            m = arp_notes[ci][(b * 2 + q) % 4]
            f = hz(m)
            sig = (np.sin(2 * np.pi * f * pt) + 0.3 * np.sin(2 * np.pi * 2 * f * pt)) * np.exp(-pt * 5.5)
            add(pluck, tb + q * beat / 2, sig * (0.04 + 0.07 * ev))

def hp(x, n=10):
    return x - smooth(x, n)

riser = np.zeros(N); imp = np.zeros(N)
rs, re_ = B0 - 2.25, B0
i0, i1 = int(rs * SR), min(N, int(re_ * SR))
if i0 >= 0 and i1 > i0:
    L = i1 - i0
    ramp = np.linspace(0, 1, L) ** 2.2
    riser[i0:i1] = hp(rng.standard_normal(L), 12) * ramp * 0.5 + np.sin(2 * np.pi * np.cumsum(np.linspace(220, 1400, L)) / SR) * ramp * 0.08
def impact(at, amp=1.0):
    s0 = int(at * SR)
    if s0 >= N: return
    n = int(1.1 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 * tt + 90 * (1 - np.exp(-tt * 18)) / 18)) * np.exp(-tt * 3.2)
    air = hp(rng.standard_normal(n), 10) * np.exp(-tt * 6.0) * 0.5
    e0 = min(N, s0 + n); imp[s0:e0] += (boom * 1.2 + air)[: e0 - s0] * amp
impact(B0, 1.0)
impact(MOS, 0.8)
impact(B1, 0.5)

mix = pad * 0.5 + sub * 0.55 * (0.5 + 0.5 * energy) + kick * 0.9 + hat * 1.0 + pluck * 1.0 + riser * 0.9 + imp * 0.9
mix *= (0.55 + 0.45 * energy)
# fade in / out
mix *= np.minimum(1, t / 2.0) * np.minimum(1, (T - t) / 3.5)
mix /= max(1e-9, np.max(np.abs(mix))) / 0.85
st = np.stack([mix, np.roll(mix, int(0.012 * SR))], axis=1)  # tiny stereo offset
pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("bgm", out, round(T, 1), "s")

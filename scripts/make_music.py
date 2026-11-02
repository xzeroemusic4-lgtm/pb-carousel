"""Usage: make_music.py <out.wav>. Writes an original 80 second calm ambient bed (pads, sub bass and a soft pluck) so no licensed track is needed."""
import sys
import numpy as np
import soundfile as sf

SR = 44100
BPM = 84
BEAT = 60 / BPM
BAR = 4 * BEAT
BARS = 36                       # 36 bars is about 103 s, trimmed to 80 s below
N = int(BARS * BAR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)  # fixed seed: the same file every run

def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)

# A minor loop: Am, F, C, G (midi notes for the pad voices)
CHORDS = [(57, 60, 64, 67), (53, 57, 60, 64), (48, 55, 60, 64), (55, 59, 62, 67)]
ROOTS = [33, 29, 36, 31]

pad = np.zeros(N)
bass = np.zeros(N)
pluck = np.zeros(N)

for bar in range(BARS):
    chord = CHORDS[bar % 4]
    s = int(bar * BAR * SR)
    e = min(N, s + int(BAR * SR * 1.35))     # pads overlap into the next bar
    seg = t[s:e] - t[s]
    att = np.clip(seg / 1.6, 0, 1) ** 2
    rel = np.clip((BAR * 1.35 - seg) / 1.2, 0, 1)
    env = att * rel
    for note in chord:
        for detune in (-0.07, 0.07):
            f = hz(note) * 2 ** (detune / 12)
            for h, amp in ((1, 1.0), (2, 0.35), (3, 0.15), (4, 0.06)):
                pad[s:e] += amp * np.sin(2 * np.pi * f * h * seg + rng.uniform(0, 6.28)) * env
    root = hz(ROOTS[bar % 4])
    benv = np.clip(seg / 0.4, 0, 1) * rel
    bass[s:e] += np.sin(2 * np.pi * root * seg) * benv * 0.9

    # eighth-note pluck arpeggio, soft
    arp = [chord[0] + 12, chord[2] + 12, chord[1] + 12, chord[3] + 12, chord[2] + 12, chord[1] + 12, chord[3] + 12, chord[2] + 12]
    for i, note in enumerate(arp):
        ps = s + int(i * BEAT / 2 * SR)
        pe = min(N, ps + int(0.9 * SR))
        if pe <= ps:
            continue
        seg2 = np.arange(pe - ps) / SR
        decay = np.exp(-seg2 * 5.5)
        tone = np.sin(2 * np.pi * hz(note) * seg2) + 0.25 * np.sin(2 * np.pi * hz(note) * 2 * seg2)
        pluck[ps:pe] += tone * decay * (0.55 if i % 2 == 0 else 0.4)

mix = 0.22 * pad / max(1e-9, np.abs(pad).max()) + 0.30 * bass / max(1e-9, np.abs(bass).max()) + 0.16 * pluck / max(1e-9, np.abs(pluck).max())

# a simple feedback-delay "room" for width and softness
def room(x, delay_s, gain):
    d = int(delay_s * SR)
    y = x.copy()
    y[d:] += gain * x[:-d]
    return y

wet = room(room(room(mix, 0.083, 0.45), 0.131, 0.38), 0.197, 0.30)
left = wet
right = np.roll(wet, int(0.012 * SR))              # slight stereo offset

out = np.stack([left, right], axis=1)
out = out[: int(80 * SR)]
fade = np.ones(len(out))
fade[: int(2 * SR)] = np.linspace(0, 1, int(2 * SR))
fade[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
out *= fade[:, None]
out = out / np.abs(out).max() * 0.8
sf.write(sys.argv[1], out.astype(np.float32), SR)
print("wrote", sys.argv[1], round(len(out) / SR, 1), "s")

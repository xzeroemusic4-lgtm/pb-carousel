"""Usage: mix.py <reel dir> <film seconds>. Mixes the voice and a low music bed into assets/audio/mix.wav at -16 LUFS."""
import json, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf

D, DUR = sys.argv[1], float(sys.argv[2])
A = f"{D}/assets/audio"
SR = 48000
MUSIC_BELOW_VOICE_DB = 10  # under speech the bed sits this far below the voice's loudness (Prince asked for -10 dB)
GAP_LIFT_DB = 4            # the bed rises this much in the gaps between lines


def load(path):
    with tempfile.TemporaryDirectory() as d:
        out = f"{d}/a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", out], check=True)
        return sf.read(out, dtype="float32")[0]


def measure(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+([-\d.]+) LUFS", o)[-1]), float(re.findall(r"Peak:\s+([-\d.]+) dBFS", o)[-1])


n = int(DUR * SR)
voice = np.zeros((n, 2), "float32")
v = load(f"{A}/voiceover.wav")[:n]
voice[: len(v)] = v
bed_raw = load(f"{A}/music-bed.mp3")[:n]
with tempfile.TemporaryDirectory() as d0:
    sf.write(f"{d0}/v.wav", voice, SR, subtype="FLOAT")
    sf.write(f"{d0}/b.wav", bed_raw, SR, subtype="FLOAT")
    voice_lufs, bed_lufs = measure(f"{d0}/v.wav")[0], measure(f"{d0}/b.wav")[0]
SPEECH_DB = (voice_lufs - MUSIC_BELOW_VOICE_DB) - bed_lufs
PAUSE_DB = SPEECH_DB + GAP_LIFT_DB
print(f"voice {voice_lufs:.1f} LUFS, bed {bed_lufs:.1f} LUFS, bed gain {SPEECH_DB:.1f} dB under speech, {PAUSE_DB:.1f} dB in gaps")
target = np.full(n, PAUSE_DB, "float32")
for line in json.load(open(f"{A}/voiceover.lines.json")):
    target[int(line["start"] * SR): int(line["end"] * SR)] = SPEECH_DB
smooth = int(0.22 * SR)
env = np.convolve(target, np.ones(smooth) / smooth, "same")
env[:smooth], env[-smooth:] = target[smooth], PAUSE_DB
# The bed is an original track, 80 s long, so there is no licence limit on looping or remixing.
bed = bed_raw * (10 ** (env / 20))[:, None]
fade = int(1.2 * SR)
bed[-fade:] *= np.linspace(1, 0, fade)[:, None]
bed[:240] *= np.linspace(0, 1, 240)[:, None]
with tempfile.TemporaryDirectory() as d:
    sf.write(f"{d}/raw.wav", voice + bed, SR, subtype="FLOAT")
    gain, out = 0.0, f"{A}/mix.wav"
    for attempt in range(5):
        af = f"volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.56:attack=2:release=50:level=0,aresample=48000"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/raw.wav", "-af", af, "-c:a", "pcm_s24le", out], check=True)
        lufs, peak = measure(out)
        print(f"pass {attempt + 1}: {lufs:.1f} LUFS, true peak {peak:.1f} dBFS")
        if abs(lufs + 16) < 0.15:
            break
        gain += -16 - lufs

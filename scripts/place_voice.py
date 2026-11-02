"""Usage: place_voice.py <reel dir> <raw voice file>. Writes voiceover.wav and one (start, end) pair per spoken line."""
import json, re, subprocess, sys

D, RAW = sys.argv[1], sys.argv[2]
A = f"{D}/assets/audio"
SR = 48000
log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", RAW, "-af", "silencedetect=noise=-38dB:d=0.28", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", RAW]))
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
lines, t = [], 0.0
for s, e in zip(starts, ends):
    if s > t:
        lines.append({"start": round(t, 2), "end": round(s, 2)})
    t = e
if t < dur - 0.05:
    lines.append({"start": round(t, 2), "end": round(dur, 2)})
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", RAW, "-ar", str(SR), "-ac", "2", "-af", "loudnorm=I=-18:TP=-3", "-ar", str(SR), f"{A}/voiceover.wav"], check=True)
json.dump(lines, open(f"{A}/voiceover.lines.json", "w"), indent=1)
print(json.dumps({"duration": round(dur, 2), "lines": len(lines), "pairs": lines}))

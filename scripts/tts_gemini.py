"""Usage: tts_gemini.py <script.txt> <out.wav>. Google Gemini TTS, voice Kore. Key from $GEMINI_API_KEY (or ~/.secrets/google_tts_key).
Speeds the raw take up so the speech fits 170 s and runs about 2.6 words a second (1.0x to 1.35x)."""
import base64, json, os, subprocess, sys, urllib.request
key = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/.secrets/google_tts_key")).read().strip()
text, out = open(sys.argv[1]).read().strip(), sys.argv[2]
body = {"contents": [{"parts": [{"text": "Say quickly and energetically, like a young Indian woman explaining tech on Instagram Reels: " + text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}}}
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-tts:generateContent",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
import time
for attempt in range(4):  # 503 "high demand" is temporary
    try:
        d = json.load(urllib.request.urlopen(req, timeout=600)); break
    except urllib.error.HTTPError as e:
        if e.code != 503 or attempt == 3:
            sys.exit(f"Gemini TTS {e.code}: {e.read()[:300]!r}")
        time.sleep(15)
raw = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
fmt = [] if raw[:4] == b"RIFF" else ["-f", "s16le", "-ar", "24000", "-ac", "1"]
open(out + ".raw", "wb").write(raw)
dur = float(subprocess.check_output(["ffprobe", "-v", "error", *fmt, "-show_entries", "format=duration", "-of", "csv=p=0", out + ".raw"]))
words = len(text.split())
tempo = min(1.35, max(1.0, 2.6 * dur / words, dur / 170.0))  # about 2.6 words a second, never over 170 s
subprocess.run(["ffmpeg", "-v", "error", "-y", *fmt, "-i", out + ".raw", "-af", f"atempo={tempo:.3f}", "-ar", "48000", out], check=True)
os.remove(out + ".raw")
print(json.dumps({"raw_seconds": round(dur, 2), "tempo": round(tempo, 3), "seconds": round(dur / tempo, 2)}))

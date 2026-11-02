#!/usr/bin/env bash
# Usage: scripts/new-reel.sh <slug>. Makes reels/<date>-<slug> with the libraries, fonts and music in place.
set -euo pipefail
cd "$(dirname "$0")/.."
DIR="reels/$(TZ=Asia/Kolkata date +%F)-$1"
mkdir -p "$DIR/assets/audio" "$DIR/renders"
cp -R assets/fonts "$DIR/assets/"
cp assets/music/music-bed.mp3 "$DIR/assets/audio/"
cp -R vendor "$DIR/"
cat > "$DIR/hyperframes.json" <<J
{ "paths": { "assets": "assets" }, "media": { "autoProxy": false } }
J
echo "$DIR"

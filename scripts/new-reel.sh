#!/usr/bin/env bash
# Usage: scripts/new-reel.sh <slug>. Makes reels/<date>-<slug> with the libraries, fonts and music in place.
set -euo pipefail
cd "$(dirname "$0")/.."
DIR="reels/$(TZ=Asia/Kolkata date +%F)-$1"
mkdir -p "$DIR/assets/audio" "$DIR/renders"
cp -R assets/fonts "$DIR/assets/"
# Prince's licensed tracks live in the private repo pb-music (a second source of the cloud job). Pick one by day so
# the music rotates; fall back to the original bed if that repo is not mounted.
MUSIC_DIR="${MUSIC_DIR:-/home/user/pb-music}"
shopt -s nullglob
TRACKS=("$MUSIC_DIR"/*.mp3)
if [ ${#TRACKS[@]} -gt 0 ]; then
  PICK="${TRACKS[$(( $(TZ=Asia/Kolkata date +%j | sed 's/^0*//') % ${#TRACKS[@]} ))]}"
else
  PICK="assets/music/music-bed.mp3"
fi
echo "music: $PICK" >&2
cp "$PICK" "$DIR/assets/audio/music-bed.mp3"
cp -R vendor "$DIR/"
cat > "$DIR/hyperframes.json" <<J
{ "paths": { "assets": "assets" }, "media": { "autoProxy": false } }
J
echo "$DIR"

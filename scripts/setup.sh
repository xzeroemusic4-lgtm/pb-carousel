#!/usr/bin/env bash
# Install the libraries and keep local copies, because the cloud sandbox blocks CDNs.
set -euo pipefail
cd "$(dirname "$0")/.."
npm install --no-audit --no-fund --loglevel=error
mkdir -p vendor/three/build vendor/three/examples
cp node_modules/gsap/dist/gsap.min.js vendor/
cp node_modules/three/build/three.module.js node_modules/three/build/three.core.js vendor/three/build/
cp -R node_modules/three/examples/jsm vendor/three/examples/
cp node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2 assets/fonts/jetbrains-mono.woff2
pip install --quiet numpy soundfile
# The repo is public and the music licence bars sharing the track, so only an encrypted copy is stored.
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 -in assets/music/music-other-world.mp3.enc \
  -out assets/music/music-other-world.mp3 -pass env:MUSIC_KEY

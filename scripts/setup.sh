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
python3 -m pip install --quiet numpy soundfile

#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

echo "Cleaning previous JSON proposal data..."
rm -rf "proposals"
mkdir -p "proposals"

for i in {1..13}; do
  echo "Requesting batch of proposals $i/13..."
  curl -fSs \
      -H "Accept: application/vnd.github.squirrel-girl-preview" \
      "https://api.github.com/repos/godotengine/godot-proposals/issues?state=open&per_page=100&page=$i" \
      > "proposals/$i.json" &
done

echo "Done."

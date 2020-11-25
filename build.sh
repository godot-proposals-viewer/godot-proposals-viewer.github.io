#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Cleaning previous JSON proposal data..."
rm -rf "proposals"
mkdir -p "proposals"

# 1 page fetches 100 proposals. Remember to increment the number below periodically
# to match the number of currently open proposals on
# https://github.com/godotengine/godot-proposals/issues.
for i in {1..14}; do
  echo "Requesting batch of proposals $i/14..."
  curl -fSs \
      -H "Accept: application/vnd.github.squirrel-girl-preview" \
      "https://api.github.com/repos/godotengine/godot-proposals/issues?state=open&per_page=100&page=$i" \
      > "proposals/$i.json"
done

echo "Done."

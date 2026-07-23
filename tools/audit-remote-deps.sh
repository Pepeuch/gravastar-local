#!/usr/bin/env bash
set -euo pipefail

target="${1:-site/patched/hub.gravastar.com/gravastar}"

if [[ ! -d "$target" ]]; then
  printf 'missing target directory: %s\n' "$target" >&2
  exit 1
fi

find "$target" -type f \( -name '*.html' -o -name '*.js' -o -name '*.css' \) -print0 \
  | xargs -0 grep -ahoE 'https?://[^"'"'"'` )]+|//[A-Za-z0-9.-]+\.[A-Za-z0-9.-]+[^"'"'"'` )]*' \
  | grep -Ev '^(//[A-Za-z0-9_-]+\.test\(.*|http://www\.w3\.org/|http://underscorejs\.org/LICENSE>|https://github\.com/.*/LICENSE|https://github\.com/MikeMcl/decimal\.js|https://github\.com/uuidjs/uuid#getrandomvalues-not-supported|https://lodash\.com/?>|https://lodash\.com/license>|https://openjsf\.org/?>|https://npms\.io/search\?q=ponyfill\.|https://vuejs\.org/error-reference/#runtime-\$\{n\})' \
  | sort -u

#!/usr/bin/env bash
# (c) 2016 cloudrkt
# Adopted from https://gist.github.com/cloudrkt/e680a0270478a58f25c3c7fe32710423.

dir=$(dirname "$0")

POSTS="$dir/../_posts"
DICT="$dir/spellcheck/dictionary.txt"

RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[0;33m'
END='\033[0m'

find $POSTS -type f -name "*.md" | while read -r file; do
  output=$(aspell \
    --home-dir="$dir/spellcheck" \
    --personal="$DICT" \
    --encoding=utf-8 \
    --lang=en \
    --mode=tex \
    list \
    < "$file")
  aspellec=$?

  if [[ $aspellec != 0 ]]; then
    echo -e "${RED}aspell failed on ${file}${END}"
    exit 1
  elif [[ $output ]]; then
    echo -e "${RED}Spelling errors discovered at ${file}.${END}"
    echo -e "${YEL}$output${END}" | sort -u
    exit 1
  fi
done
checkec=$?

if [[ $checkec != 0 ]]; then
  exit 1
fi

echo -e "${GRN}Spellcheck OK${END}"
exit 0

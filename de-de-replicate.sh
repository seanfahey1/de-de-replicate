#!/usr/bin/env bash

target_dir="$1"

for file in "$target_dir"/*.fasta; do
  echo "starting $file..."

  output=${"$file"%%.*}
  clstr_output="$output".clstr

  echo "  running CD-Hit"
  cd-hit -c 0.9 -n 2 -T 0 -M 0 -sc -d 100 -i "$file" -o "$output" > /dev/null

  echo "  running split-expand step"
  ./split_expand.py --f "$file" --c "$clstr_output" --n 11 --o "$target_dir"/groups/

done

#!/usr/bin/env bash

target_dir="$1"
#./hash_descriptors.py -i "$target_dir"

for file in "$target_dir"/*_hashed_descriptors.fasta; do

  echo "starting $file..."

  dirname=$(dirname "$file")
  filename=$(basename "$file")
  filename_no_ext="${filename%.*}"
  output="$dirname/$filename_no_ext"_40.fasta
  clstr_output="$output".clstr

#  echo "  will output to $output"
#
#  echo "  running CD-Hit"
#  cd-hit -c 0.4 -n 2 -T 0 -M 0 -sc 1 -d 0 -i "$file" -o "$output"

  echo "  running split-expand step"
  ./split_expand.py --f "$file" --c "$clstr_output" --n 11 --o "$target_dir"/groups/

done

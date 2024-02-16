#!/usr/bin/env bash


for file in *.fasta; do
  output=${"$file"%%.*}
  clstr_output="$output".clstr

  cd-hit -c 0.9 -n 2 -T 0 -M 0 -sc -d 100 -i "$file" -o "$output"



done

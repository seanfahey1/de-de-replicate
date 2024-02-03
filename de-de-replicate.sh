#!/usr/bin/env bash

files="./*.fasta"

# remove anything w/in a class that's 100% identical, keeps the longer seq.
for file in $files;
do
  echo "$file"
  file_clean=$(basename "$file" ".fasta")

  # write the filename into the header so we can separate them later
  sed -i "s/^>/>$file_clean /g" "$file" > "$file_clean"_named.fasta

  cd-hit -c 1 -T 0 -M 0 -d 500 -i "$file" -o "$file_clean"_100_self.fasta
  cat "$file_clean"_100_self.fasta >> all_files_100_self.fasta

done

# remove anything that has 100% similarity with something in another class. then unmerge files.
cd-hit -c 1 -T 0 -M 0 -d 500 -i all_files_100_self.fasta -o all_files_100.fasta
python3 unmerge_100.py -f all_files_100.fasta -c all_files_100.fasta.clstr


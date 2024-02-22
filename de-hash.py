#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
from pathlib import Path

from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description="Reverses hashing of fasta descriptor."
    )
    parser.add_argument("--i", "-input_dir", type=str, required=True)
    parser.add_argument("--j", "-json_hash_table", type=str, required=True)

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    input_dir = Path(args.i)
    with open(Path(args.j)) as j:
        hash_table = json.load(j)

    for file in input_dir.glob("*.fasta"):
        output_records = []
        for record in SeqIO.parse(file, "fasta"):
            record.description = hash_table[record.description]
            output_records.append(record)

        with open(file.parent / (file.stem + "_unhashed.fasta"), "w") as handler:
            SeqIO.write(output_records, handler, "fasta")


if __name__ == "__main__":
    sys.exit(main())

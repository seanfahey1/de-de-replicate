#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
from pathlib import Path

from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description="Replaces fasta descriptor with hashed sequence."
    )
    parser.add_argument("--i", "-input_dir", type=str, required=True)

    args = parser.parse_args()
    return args


def generate_hash(record):
    hash_val = str(hashlib.md5(str(record.seq).encode()))
    return hash_val


def hash_file_descriptors(file):
    hash_file = file.stem + "_hashed_descriptors.fasta"
    output_records = []
    hash_table = {}

    for record in SeqIO.parse(file, "fasta"):
        description = str(record.description)
        sequence_hash = generate_hash(record)
        hash_table[sequence_hash] = description

        record.description = sequence_hash
        output_records.append(record)

    print(f"writing to {hash_file}")
    with open(hash_file, "w") as handler:
        SeqIO.write(output_records, handler, "fasta")

    return hash_table


def write_hash_table(input_dir, hash_table):
    with open(input_dir / "hash_table.json") as out:
        json.dump(hash_table, out)


def main():
    args = get_args()
    input_dir = Path(args.i)
    fasta_inputs = input_dir.glob("*.fasta")

    hash_table = dict()

    for file in fasta_inputs:
        print(f"hashing {file.name}")
        file_hash_table = hash_file_descriptors(file)
        hash_table.update(file_hash_table)

    write_hash_table(input_dir, hash_table)


if __name__ == "__main__":
    sys.exit(main())

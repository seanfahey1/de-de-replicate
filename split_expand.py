#!/usr/bin/env python3

import argparse
import re
import sys
from itertools import cycle
from pathlib import Path

from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description="Splits cluster into 11 groups and rebuilds from fasta file."
    )
    parser.add_argument("--f", "-fasta", type=str, required=True)
    parser.add_argument("--c", "-clstr", type=str, required=True)
    parser.add_argument("--n", "-num_groups", type=int, required=False, default=11)
    parser.add_argument("--o", "-out_dir", type=str, required=False, default=".")

    args = parser.parse_args()
    return args


def get_clusters(raw_clusters, num_groups):
    group_iter = cycle(list(range(1, num_groups + 1)))

    for raw_cluster in raw_clusters:
        descriptors = []
        for line in raw_cluster.split("\n"):
            match = re.search(r">([a-zA-Z0-9]*)\.\.\. ", line)
            if match is not None:
                descriptors.extend(match.groups())

        yield descriptors, next(group_iter)


def write_to_file(out_dir, fasta_file_path, group_id, seq_record):
    out_filename = out_dir / f"{group_id}_{fasta_file_path.name}"
    with open(out_filename, "a") as handle:
        SeqIO.write(seq_record, handle=handle, format="fasta")


def main():
    args = get_args()

    num_groups = args.n
    clstr_file_path = Path(args.c)
    fasta_file_path = Path(args.f)
    out_dir = Path(args.o)
    out_dir.mkdir(parents=False, exist_ok=True)

    with open(clstr_file_path, "r") as clstr:
        clstrs = clstr.read().split(">Cluster")[1:]

    fasta_dict = SeqIO.to_dict(
        SeqIO.parse(fasta_file_path, "fasta"), key_function=lambda rec: rec.description
    )

    for descriptors, group_id in get_clusters(clstrs, num_groups):
        for description in descriptors:
            write_to_file(out_dir, fasta_file_path, group_id, fasta_dict[description])


if __name__ == "__main__":
    sys.exit(main())

import argparse
import re
import sys

from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description='Rebuild original fasta files from a merged file using first word of header of each seq',
        epilog='This is meant to be run in the de-de-replicate pipeline')

    parser.add_argument('-f', '--fasta', required=True)
    parser.add_argument('-c', '--clstr', required=True)
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    fasta, clstr = args.fasta, args.clstr
    drop_headers = []

    with open(clstr, 'r') as c:
        c = c.read().split(">Cluster")[1:]
        for cluster in c:
            seq_count = len([x for x in cluster.split('\n') if re.match(r'[0-9]{1,4}/s+')])
            if seq_count > 1:
                headers = re.findall(r'[0-9]+/s+(>.*)$')
                for header in headers:
                    drop_headers.append(header)

    for record in SeqIO.parse(fasta, "fasta"):
        full_header = record.description.split(' ')
        header = ' '.join(full_header[1:])
        group = full_header[0]

        sequence = str(record.seq)
        if header not in drop_headers:
            with open(f'{group}_100.fasta', 'a') as out:
                out.write(f">{header}")
                out.write(sequence)
                out.write('\n')


if __name__ == "__main__":
    sys.exit(main())

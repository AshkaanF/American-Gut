#!/usr/bin/env python

"""Determine the number of samples, participants, and sequences in AG"""

import argparse
from americangut.util import (parse_mapping_file, unique_participants,
        unique_samples, n_sequences)
from bipy.parse.fasta import MinimalFastaParser

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The American Gut Project"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-m', '--mapping-file', help='Mapping file',
                      required=True)
    args.add_argument('-s', '--sequences', help='Demultiplexed sequence files',
                      required=False)
    args.add_argument('-o', '--output', help='Output file', required=True)
    args = args.parse_args()
    return args

if __name__ == '__main__':
    args = interface()

    header, mapping_file = parse_mapping_file(open(args.mapping_file))

    n_participants = len(unique_participants(mapping_file))
    n_samples = len(unique_samples(mapping_file))

    if args.sequences:
        seqs_files = [open(f) for f in args.sequences.split(',')]
        n_seqs = n_sequences(seqs_files)
    else:
        n_seqs = None

    with open(args.output, 'w') as output:
        output.write("Number of participants: %d\n" % n_participants)
        output.write("Number of samples: %d\n" % n_samples)

        if n_seqs is not None:
            output.write("Number of sequences: %d\n" % n_seqs)

#!/usr/bin/env python

from bipy.parse.fasta import MinimalFastaParser

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The American Gut Project"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"


def unique_participants(mapping):
    """Determine the unique participants"""
    head, rest = mapping
    host_id = head.split('\t').index('HOST_SUBJECT_ID')

    # the mapping data aren't really parsed by the parse_mapping_file method.
    # rest is of the form (sample_id, everything else). The -1 is to adjust for
    # the sample ID not being part of everything else.
    return {r[1].split('\t')[host_id - 1] for r in rest}


def n_sequences(seqs_files):
    """Determine the total number of sequences"""
    # Will, don't kill me...
    return sum([1 for f in seqs_files for i, s in MinimalFastaParser(f)])


def unique_samples(mapping):
    """Fetch unique samples in the mapping"""
    head, rest = mapping
    all_samples = [s[0].split('.')[0] for s in rest]
    samples_without_tips = {s for s in all_samples if s[-1].isdigit()}

    # get samples sequenced multiple times, drop tip number
    samples_with_tips = {s[:-1] for s in all_samples if not s[-1].isdigit()}

    return samples_with_tips.union(samples_without_tips)


def pick_rarifaction_level(id_, lookups):
    """Determine which lookup has the appropriate key

    id_ is a barcode, e.g., '000001000'
    lookups is a list of tuples, e.g., [('10k',{'000001000':'000001000.123'})]

    The order of the lookups matters. The first lookup found with the key will
    be returned.

    None is returned if the key is not found
    """
    for name, lookup in lookups:
        if id_ in lookup:
            return name
    return None

def parse_mapping_file(open_file):
    """return (header, [(sample_id, all_other_fields)])

    """
    header = open_file.readline().strip()
    res = []

    for l in open_file:
        res.append(l.strip().split('\t',1))

    return (header, res)

def verify_subset(table, mapping):
    """Returns True/False if the table is a subset"""
    ids = set([i[0] for i in mapping])
    t_ids = set(table.SampleIds)

    return t_ids.issubset(ids)

def slice_mapping_file(table, mapping):
    """Returns a new mapping corresponding to just the ids in the table"""
    t_ids = set(table.SampleIds)
    res = []

    for id_, l in mapping:
        if id_ in t_ids:
            res.append('\t'.join([id_, l]))

    return res

#!/usr/bin/env python

from Bio import motifs

from mast import MastFile

# parse MAST output file using Biopython
with open("mast.txt") as f:
    record = motifs.parse(f, 'MAST')

# further parse Record object
mast_file = MastFile(record)

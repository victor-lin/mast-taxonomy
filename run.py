#!/usr/bin/env python

from Bio import motifs

from mast import MastFile
from uniprot_taxonomy import Taxonomy

# parse MAST output file using Biopython
with open("mast.txt") as f:
    record = motifs.parse(f, 'MAST')

# further parse Record object
mast_file = MastFile(record)
tax = Taxonomy('taxonomy-all.tab')

for sequence in mast_file.sequences:
    sequence.tax_info = tax[sequence.organism]

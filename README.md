# mast-taxonomy

Goal: Parse MAST output file and integrate with taxonomy data.

## Requirements

* Biopython

## Repository Overview

* `mast/` directory for class definitions (see below)
* `mast.txt` MAST output file of interest
* `run.py` script for parsing `mast.txt`

## mast

An extension of `Bio/motifs/mast.Record`.

Some classes to represent objects under SECTION II in a MAST output file:

### MastFile

* **sequences**: list of `MastSequence` objects (represents each entry)

### MastSequence

* **name**: sequence name column
* **organism_mnemonic**: organism mnemonic ID from UniProt (derived from **name**)
* **diagram**: `Diagram` object based on diagram string
* **gene_classification**: `MDM2`/`Corp`/`other_motif4`/`other_no_motif4`

### Diagram

* **string**: diagram string from the MAST file
* **motifs**: list of `DiagramMotif` objects

### DiagramMotif

* **num**: motif number from diagram string

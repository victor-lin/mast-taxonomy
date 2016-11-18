# mast-taxonomy

Goal: Parse MAST output file and integrate with taxonomy data.

* TODO: add taxonomy data.

## Requirements

* Biopython

## Repository Overview

* `mast/` directory for class definitions (see below)
* `mast.txt` MAST output file of interest
* `run.py` script for parsing `mast.txt`

## mast

An extension of `Bio/motifs/mast.Record`.

Some classes to represent objects in a MAST output file:

### MastFile

* **sequences**: list of `MastSequence` objects (represents each line in the file)

### MastSequence

* **name**: sequence name column
* **organism**: organism mnenomic ID from **name**
* **diagram**: `Diagram` object based on diagram string
* **gene_classification**: `MDM2`/`Corp`/`Other`

### Diagram

* **string**: diagram string from the mast file
* **motifs**: list of `DiagramMotif` objects

### DiagramMotif

* **num**: motif number from diagram string
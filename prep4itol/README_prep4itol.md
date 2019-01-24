# prep4itol.py

## Overview

prep4itol takes a microbiome dataset analyzed with qiime2 to prepare files for upload to
the Interactive Tree of Life (iTol).  Taxonomic classifications are collapsed to the level of species
and CSS normalization of the feature table is performed. The final files are ready for
upload and visualization using iTol.

## prerequisites
* qiime2 installation
* R including the packages metagenomeSeq and biomformat. Both packagest are part of bioconductor.

## Instructions
activate your qiime2 installation:
`source activate qiime2-2018.8`

run prep4itol.py:
prep4itol.py -i table.qza -r rep-seqs.qza -t taxonomy.qza -o output/

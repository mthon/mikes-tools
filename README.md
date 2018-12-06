# mikes-tools

A collection of scripts for bioinformatics.

## gb\_to\_fasta\_and\_gtf.py

### requirements:
- emboss (http://emboss.sourceforge.net)

Converts a genbank format file of a genome sequence to fasta and gtf format. The output files are compatible with cufflinks. This script was developed for running inside a Docker image and is (will be) part of a tutorial on RNA-Seq analysis using Cyverse Discovery Environment.

## find-recip-hits.pl

Provide two files of BLAST search results: proteome A vs proteome B and proteome B vs proteome A.  Outputs a list of reciprocal best hits.

## ortho_to_pangp.py

Converts the output from OrthoFinder to PanGP format for pan-genome analysis.

## get_branch_lengths.pl

Compute branch lengths in a phyogenetic tree (newick format) from the root to each tip.

## scale_tree.py

Provide a phylogenetic tree in nexus format and a numeric value and outputs a new tree with each branch multiplied by the numeric value.

## microbiome/split_seqs.py


A script to demultiplex bacterial and fungal reads based on the PCR primers used to amplify them. 

## prep4itol/
Collapse frequency tables from QIIME2 and prepare files for iTol.

#!/usr/bin/env python
import sys
import pdb
from Bio.Phylo import read
from Bio.Phylo import write

def scale_clade(in_clade):
    #pdb.set_trace()
    in_clade.branch_length = in_clade.branch_length * float(sys.argv[2])

    for clade in in_clade.clades:
        scale_clade(clade)


tree = read(sys.argv[1], 'nexus')
xtree = tree.as_phyloxml()
scale_clade(xtree.clade)
write(xtree, sys.argv[1]+'.scaled.nex', 'nexus')



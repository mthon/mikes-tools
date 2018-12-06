#!/usr/bin/python

import subprocess
import os
import pdb

for file in os.listdir('.'):
    if 'R1' in file:
        basefile = file[file.index('_'):]
        sampleid = file[:file.index('_')]
        revfile = basefile.replace('R1', 'R2')

        comm = 'cutadapt -g FU=CTTGGTCATTTAGAGGAAGTAA...GCATCGATGAAGAACGCAGC -g BA=CCTACGGGNGGCWGCAG -G fungalR=GCTGCGTTCTTCATCGATGC...TTACTTCCTCTAAATGACCAAG -G bactR=GACTACHVGGGTATCTAATCC --minimum-length 20 -q 15 -o ' + sampleid + '{name}' + basefile + ' -p ' + sampleid + '{name}' + revfile + ' ' +  file + ' ' + sampleid + revfile

        subprocess.check_call(comm, shell=True)
        #pdb.set_trace()
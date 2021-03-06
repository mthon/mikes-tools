#! /usr/bin/python

import os
import sys
import argparse
import csv
import random
from subprocess import check_call

import pdb

def parse_cli():
    parser = argparse.ArgumentParser(description="Collapse an OTU table and prepare files for iTol")

    parser.add_argument('-i', type=str, dest='table_file',
                        help='OTU table in qza format')

    parser.add_argument('-t', type=str, dest='tax_file',
                        help='taxonomy file in in qza format')

    parser.add_argument('-r', type=str, dest='seq_file',
                        help='rep seqs in qza format')

    parser.add_argument('-o', type=str, dest='out_dir',
                        help='output directory')

    opts = parser.parse_args()
    return opts

def collapse_table(table, taxfile, out_dir):

    basename = os.path.splitext(table)[0]
    col_out = basename + '-collapsed.qza'
    freq_out = basename + '-collapsed-rel-freq.qza'

    #pdb.set_trace()
    coll_com ='qiime taxa collapse --i-table %s --i-taxonomy %s --p-level 7 --o-collapsed-table %s/%s' %(table, taxfile, out_dir, col_out)
    check_call(coll_com, shell=True, executable='/bin/bash')

    freq_com = 'qiime feature-table relative-frequency --i-table %s/%s --o-relative-frequency-table %s/%s' % (out_dir, col_out, out_dir, freq_out)
    check_call(freq_com, shell=True, executable='/bin/bash')

    exp_com = 'qiime tools export --input-path %s/%s --output-path %s' %(out_dir, freq_out, out_dir)
    check_call(exp_com, shell=True, executable='/bin/bash')

    # CSS normalize the table

    norm_com = '%s && Rscript %s/css_normalize.R %s/feature-table.biom %s/CSS_normalized_table.biom' % (exitqiime2, sys.path[0], out_dir, out_dir)
    check_call(norm_com, shell=True, executable='/bin/bash')

    biom_com = '%s && biom convert -i %s/CSS_normalized_table.biom -o %s/feature-table-collapsed-rel-freq.tsv --to-tsv' % (qiime2, out_dir, out_dir)
    check_call(biom_com, shell=True, executable='/bin/bash')

    tsvfile = open(out_dir + '/feature-table-collapsed-rel-freq.tsv')
    out_tsvfile = open(out_dir + '/feature-table-collapsed-rel-freq-renamed.txt', 'w')

    for row in csv.reader(tsvfile, delimiter='\t'):
        if row[0].startswith('#'):
            out_tsvfile.write('\t'.join(row))
            out_tsvfile.write('\n')
        else:
            row[0] = rename(row[0])
            out_tsvfile.write('\t'.join(row))
            out_tsvfile.write('\n')

    return col_out

def rename(tax):
    name = ''
    tax = tax.replace(' ', '')
    taxalist = tax.split(';')

    if len(taxalist) == 7:
        if len(taxalist[5]) <= 3:
            # no genus designation
            taxcounter = 4
            while taxcounter >= 0:
                #pdb.set_trace()

                if len(taxalist[taxcounter]) > 3:
                    name = taxalist[taxcounter]
                    taxcounter = -1 # we are done
                else:
                    taxcounter -= 1
        else:
            if len(taxalist[6]) > 3:
                # we have a species name

                name = taxalist[5] + '_' + taxalist[6]
            elif taxalist[3] == '__':
                name = taxalist[5] + ' unclassified species'
            else:
                #pdb.set_trace()
                name = taxalist[5] + '__spp'

    else:
        name = taxalist[-1]

    if name in encountered_names:

        if len(name.split(':')) >1:

            ind = int(name.split(':')[1])

            name_list = list(name)
            name_list[-1] = ':' + str(ind+1)
            new_name = "".join(name_list)
            encountered_names.append(new_name)
            name = new_name
            #pdb.set_trace()
        else:
            name = name + ':1'
            encountered_names.append(name)
    else:
        encountered_names.append(name)

    return name

def export_seqs(seqqza, taxqza, out_dir):

    outseqs_f = open(out_dir + '/rep-seqs-collapsed-renamed.fasta', 'w')

    seq_com = 'qiime tools export --input-path %s --output-path %s' %(seqqza, out_dir)
    check_call(seq_com, shell=True, executable='/bin/bash')

    fasta_f = open(out_dir + '/dna-sequences.fasta')

    seqdict = dict()
    while True:
        seqname = fasta_f.readline()[1:].rstrip()
        sequence = fasta_f.readline().rstrip()
        #pdb.set_trace()

        if not sequence: break
        seqdict[seqname] = sequence

    tax_com = 'qiime tools export --input-path %s --output-path %s' %(taxqza, out_dir)
    check_call(tax_com, shell=True, executable='/bin/bash')

    taxtab = open(out_dir + '/taxonomy.tsv')
    namedict = dict()
    for row in csv.reader(taxtab, delimiter='\t'):
        if row[0].startswith('Feature'): continue
        name = rename(row[1])
        if name in namedict:
            namedict[name].append(row[0])
        else:
            namedict[name] = list()
            namedict[name].append(row[0])

    for name in namedict:
        randnum = random.randint(0, len(namedict[name]) - 1)
        selectedseq = namedict[name][randnum]
        seq = seqdict[selectedseq]
        outseqs_f.write('>' +name + '\n')
        outseqs_f.write(seq + '\n')

if __name__ == "__main__":
    options = parse_cli()

    qiime2 = "source activate qiime2-2018.11"

    exitqiime2 = "source deactivate"

    encountered_names = list()

    try:
        os.stat(options.out_dir)
    except:
        os.mkdir(options.out_dir)

    coll = collapse_table(options.table_file, options.tax_file, options.out_dir)
    encountered_names = list()
    export_seqs(options.seq_file, options.tax_file, options.out_dir)

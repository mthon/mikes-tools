import csv
from sys import argv
import pdb

num_spp = 0

files = ['Orthogroups.csv','Orthogroups_UnassignedGenes.csv']

for file in files:
    for row in csv.reader(open(file), delimiter='\t'):
        if row[0].startswith('Cluster'):
            num_spp = len(row[1:])
            continue
        if len(row[0]) == 0 :
            #pdb.set_trace()
            num_spp = len(row[1:])
            continue

        #pdb.set_trace()
        if len(row[1:]) < num_spp:
            for i in range(num_spp-len(row[1:])):
                row.append('')

        line_to_print = ''
        for column in row[1:]:
            if len(column) == 0:
                line_to_print += '0'
            else:
                line_to_print += '1'
        print line_to_print
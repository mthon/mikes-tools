# prep4itol.py

## prerequisites
* qiime2 installation
* R including the packages metagenomeSeq and biomformat. Both packagest are part of bioconductor.
## Instructions
activate your qiime2 and then your qiime1 installations:
`source activate qiime2-2018.8`

run prep4itol.py:
prep4itol.py -i table.qza -r rep-seqs.qza -t taxonomy.qza -o output/

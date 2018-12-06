#!/usr/bin/env Rscript

library('metagenomeSeq')
library('biomformat')

args <- commandArgs()

mrexp <- loadBiom(args[6])
p = cumNormStatFast(mrexp)
outmr = cumNorm(mrexp, p = p)
outbiom <- MRexperiment2biom(outmr)
write_biom(outbiom, args[7])

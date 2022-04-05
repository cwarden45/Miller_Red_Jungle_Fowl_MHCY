#!/bin/bash

SAMPLEID=58f18_trimmed-Arrow-2x
REF=HGAP3-58f18-trimmed/arrow_var.fasta

BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

#I did not set -d 10000 for the 1st sample
samtools mpileup -d 10000 -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
#!/bin/bash

SAMPLEID=Canu-v1.5-Arrow_102b15-rearranged--extra_12bp-Arrow-2x
REF=Canu-v1.5-Arrow_102b15-rearranged-expectedBAC-extra_12bp/arrow_var.fasta


BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
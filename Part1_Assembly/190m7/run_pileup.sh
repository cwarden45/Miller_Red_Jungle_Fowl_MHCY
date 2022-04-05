#!/bin/bash

SAMPLEID=Canu-v1.5-Arrow_190M-rearranged--extra_12bp-expectedBAC-Arrow-2x
REF=Canu-v1.5-Arrow_190M-rearranged--extra_12bp-expectedBAC/arrow_var.fasta


BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
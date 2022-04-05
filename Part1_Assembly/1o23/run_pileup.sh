#!/bin/bash

SAMPLEID=Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC-Arrow-2x
REF=Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC/arrow_var.fasta

BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
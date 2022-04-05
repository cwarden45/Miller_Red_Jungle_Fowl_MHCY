#!/bin/bash

SAMPLEID=HGAP3_19d16-rearranged-for_GitHub
REF=HGAP3_19d16-rearranged-CW-2021/arrow_var.fasta

BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
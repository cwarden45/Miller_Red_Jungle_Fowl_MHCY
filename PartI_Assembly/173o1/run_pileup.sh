#!/bin/bash

SAMPLEID=Canu-v2.1-Public_Sanger_revised-201118
REF=../Sanger/revise_Canu_assembly/173o1-3change_201118.fa


BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
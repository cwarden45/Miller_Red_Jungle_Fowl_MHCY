#!/bin/bash

#copied over and modified from run_VarScan.sh in \\isi-dcnl\user_data\lcouture\Seq\200803\Code

SAMPLEID=34j16_200923-Arrow
REF=34j16_200923/arrow_var.fasta

BAM=$SAMPLEID/aligned_reads.bam
PILEUP=$SAMPLEID/aligned_reads.all.pileup

samtools mpileup -f $REF $BAM > $PILEUP

#PILEUP=$SAMPLEID/aligned_reads.C50.pileup
#samtools mpileup -C50 -f $REF $BAM > $PILEUP
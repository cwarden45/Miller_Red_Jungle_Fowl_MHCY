#!/bin/bash
#SBATCH -J BQA1o23n5k10
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=24g
#SBATCH --time=36:00:00
#SBATCH --output=BQA1o23n5k10.log

UNALIGNED=../../Intermediate_Files/BAC_1o23.subreads.bam
INPUTASSEMBLY=Canu-v2.1-Arrow_1o23-trimmed_extra-12-bp_expectedBAC.fa
PREFIX=Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC

module load pbbioconda/20200921
module load SAMtools/1.9-foss-2018b

mkdir $PREFIX
samtools faidx $INPUTASSEMBLY

TEMPBAM=$PREFIX/temp.bam
BAM=$PREFIX/aligned_reads.bam
blasr --nproc 16 $UNALIGNED $INPUTASSEMBLY --bam --out $TEMPBAM
samtools sort -o $BAM $TEMPBAM
rm $TEMPBAM
samtools index $BAM
pbindex $BAM

GFF=$PREFIX/arrow.gff
OUTFA=$PREFIX/arrow_var.fasta
OUTFQ=$PREFIX/arrow_consensus.fastq
arrow $BAM -r $INPUTASSEMBLY -o $GFF -o $OUTFA -o $OUTFQ

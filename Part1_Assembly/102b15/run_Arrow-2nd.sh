#!/bin/bash
#SBATCH -J BQA102n4k10
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=24g
#SBATCH --time=36:00:00
#SBATCH --output=BQA102n4k10.log

UNALIGNED=../../Intermediate_Files/BAC_102b15.subreads.bam
INPUTASSEMBLY=Canu-v1.5-Arrow_102b15-rearranged-expectedBAC--extra_12bp.fa
PREFIX=Canu-v1.5-Arrow_102b15-rearranged-expectedBAC-extra_12bp

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

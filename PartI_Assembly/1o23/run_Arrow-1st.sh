#!/bin/bash
#SBATCH -J BQA1o23v2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=48g
#SBATCH --time=48:00:00
#SBATCH --output=BQA1o23v2.log

UNALIGNED=../Intermediate_Files/BAC_1o23.subreads.bam
INPUTASSEMBLY=../Meta_Assembly/Canu/BAC_1o23_LENGTH_FILTERED_subreads_10k/1o23_10k_canu_contig_long1.fa
PREFIX=BAC_1o23_LENGTH_FILTERED_subreads_10k_v2.1

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

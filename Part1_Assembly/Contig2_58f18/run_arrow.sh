#!/bin/bash
#SBATCH -J BQA58t2e
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=24g
#SBATCH --time=36:00:00
#SBATCH --output=BQA58t2e.log

UNALIGNED=../../Intermediate_Files/BAC_190M_combined-REALLY_58f18.subreads.bam
INPUTASSEMBLY=58f18_HGAP_trimmed.fa
PREFIX=HGAP3-58f18-trimmed

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

#!/bin/bash
#SBATCH -J BQ190
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=48g
#SBATCH --time=72:00:00
#SBATCH --output=BQ190.log

UNALIGNED=../Intermediate_Files/160505_B2_58f18.subreads.bam #samples were mislabeled (this is correct for 190M)
INPUTASSEMBLY=../Meta_Assembly/Canu/BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k_v1_5/190M_10k_canu_contig_long1.fa
PREFIX=BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k_v1_5

module load pbbioconda/20200921
module load SAMtools/1.9-foss-2018b

#mkdir $PREFIX
#samtools faidx $INPUTASSEMBLY

TEMPBAM=$PREFIX/temp.bam
BAM=$PREFIX/aligned_reads.bam
#blasr --nproc 16 $UNALIGNED $INPUTASSEMBLY --bam --out $TEMPBAM
#samtools sort -o $BAM $TEMPBAM
#rm $TEMPBAM
#samtools index $BAM
#pbindex $BAM

GFF=$PREFIX/arrow.gff
OUTFA=$PREFIX/arrow_var.fasta
OUTFQ=$PREFIX/arrow_consensus.fastq
arrow $BAM -r $INPUTASSEMBLY -o $GFF -o $OUTFA -o $OUTFQ

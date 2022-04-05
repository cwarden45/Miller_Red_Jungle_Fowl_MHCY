#!/bin/bash
#SBATCH -J BQA173v2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=48g
#SBATCH --time=48:00:00
#SBATCH --output=BQA173v2.log

UNALIGNED=../Intermediate_Files/BAC_173o19.subreads.bam
INPUTASSEMBLY=../Meta_Assembly/Canu/BAC_173o19_LENGTH_FILTERED_subreads_10k/173o1_10k_canu_contig_long1.fa
PREFIX=BAC_173o19_LENGTH_FILTERED_subreads_10k_v2_1

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

GFF=$PREFIX/quiver.gff
OUTFA=$PREFIX/quiver_var.fasta
OUTFQ=$PREFIX/quiver_consensus.fastq
quiver $BAM -r $INPUTASSEMBLY -o $GFF -o $OUTFA -o $OUTFQ

GFF=$PREFIX/arrow.gff
OUTFA=$PREFIX/arrow_var.fasta
OUTFQ=$PREFIX/arrow_consensus.fastq
arrow $BAM -r $INPUTASSEMBLY -o $GFF -o $OUTFA -o $OUTFQ

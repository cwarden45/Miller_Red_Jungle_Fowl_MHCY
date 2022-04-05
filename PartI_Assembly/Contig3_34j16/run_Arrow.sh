#!/bin/bash
#SBATCH -J BQA34b
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=24g
#SBATCH --time=36:00:00
#SBATCH --output=BQA34b.log

#UNALIGNED=../Intermediate_Files/BAC_34j16.subreads.bam
#INPUTASSEMBLY=../../latest_sequin_files/Contig3_34j16_rev/Contig3_rev.fa
#PREFIX=34j16_200923

UNALIGNED=../Intermediate_Files/BAC_34j16.subreads.bam
INPUTASSEMBLY=34j16_200923/arrow_var.fasta
PREFIX=34j16_200923-Arrow

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

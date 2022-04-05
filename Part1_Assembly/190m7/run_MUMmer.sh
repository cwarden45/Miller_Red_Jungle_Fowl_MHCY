#!/bin/bash
#SBATCH -J MUMmer
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=4g
#SBATCH --time=0:05:00
#SBATCH --output=MUMmer.log


CONTIG=../../../Code/Meta_Assembly/Canu/BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k_v1_5/190M_10k_canu_contig_long1.fa
REF=../../190m7/190m7.fasta
PREFIX=190m7_revision



module load mummer/3.23.0

mummer -b -c $REF $CONTIG > $PREFIX.mum

module purge
module load mummer/4.0.0.beta2

mummerplot --png -p $PREFIX $PREFIX.mum
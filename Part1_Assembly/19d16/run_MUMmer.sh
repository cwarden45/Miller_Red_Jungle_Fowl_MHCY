#!/bin/bash
#SBATCH -J MUMmer
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=4g
#SBATCH --time=0:05:00
#SBATCH --output=MUMmer.log

CONTIG=../../SMRT_Portal_Files/19d16_016471_revcom.fa
REF=HGAP3_19d16-rearranged/arrow_var.fasta
PREFIX=19d16_revision

module load mummer/3.23.0

mummer -b -c $REF $CONTIG > $PREFIX.mum

module purge
module load mummer/4.0.0.beta2

mummerplot --png -p $PREFIX $PREFIX.mum
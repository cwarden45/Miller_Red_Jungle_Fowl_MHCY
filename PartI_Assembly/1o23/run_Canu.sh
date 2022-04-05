#!/bin/bash
#SBATCH -J Canu
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=48g
#SBATCH --time=96:00:00
#SBATCH --output=Canu.log

prefix=BAC_1o23_LENGTH_FILTERED_subreads_10k
size=100k

module load canu/2.1

canu -p $prefix\_canu -d $prefix genomeSize=$size -s cluster.spec -pacbio $prefix.fq
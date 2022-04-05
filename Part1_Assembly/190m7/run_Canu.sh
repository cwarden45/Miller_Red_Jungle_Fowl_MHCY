#!/bin/bash
#SBATCH -J Canu190
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 32
#SBATCH -N 1
#SBATCH --mem=96g
#SBATCH --time=120:00:00
#SBATCH --output=Canu190.log

prefix=BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k
size=300k

module load canu/1.5

canu -p $prefix\_canu -d $prefix\_v1_5 genomeSize=$size -s cluster.spec -pacbio-raw $prefix.fq
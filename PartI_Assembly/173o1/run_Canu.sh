#!/bin/bash
#SBATCH -J Canu173
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 32
#SBATCH -N 1
#SBATCH --mem=96g
#SBATCH --time=120:00:00
#SBATCH --output=Canu173.log

prefix=BAC_173o19_LENGTH_FILTERED_subreads_10k
size=200k

module load canu/2.1

canu -p $prefix\_canu -d $prefix genomeSize=$size -s cluster.spec -pacbio $prefix.fq
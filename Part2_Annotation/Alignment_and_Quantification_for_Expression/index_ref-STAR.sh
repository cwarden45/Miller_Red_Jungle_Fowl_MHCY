#!/bin/bash
#SBATCH -J STARindex
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=64g
#SBATCH --time=48:00:00
#SBATCH --output=STARindex.log

combinedRef=../truncated_galGal5_with_AllContigs-reformat.fa

/net/isi-dcnl/ifs/user_data/Seq/software/STAR-2.5/bin/Linux_x86_64_static/STAR --runMode genomeGenerate --genomeDir ./ --genomeFastaFiles $combinedRef
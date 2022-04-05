#!/bin/bash
#SBATCH -J PBCCS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cwarden@coh.org
#SBATCH -n 16
#SBATCH -N 1
#SBATCH --mem=48g
#SBATCH --time=72:00:00
#SBATCH --output=PBCCS.log

H5PREFIX=../../Raw_H5_Files/2016_04_06_10/A02_1/Analysis_Results/m160406_225725_42284_c100875832550000001823187303261633_s1_X0
UNALIGNEDPREFIX=Intermediate_Files/160406_A2_58f18
CCSPREFIX=160406_A2_58f18

#H5PREFIX=../../Raw_H5_Files/2016_04_06_10/B02_1/Analysis_Results/m160407_051641_42284_c100875832550000001823187303261634_s1_X0
#UNALIGNEDPREFIX=Intermediate_Files/160406_B2_190M
#CCSPREFIX=160406_B2_190M

module load pbbioconda/20200921
module load SAMtools/1.9-foss-2018b
module load singularity/3.5.3

MIDFOLDER=mmiller/Seq/BAC_annotation/CCS_Reads/Apollo_CCS

#convert raw file format
BAXH5C1=$H5PREFIX.1.bax.h5
BAXH5C2=$H5PREFIX.2.bax.h5
BAXH5C3=$H5PREFIX.3.bax.h5
bax2bam -o $UNALIGNEDPREFIX $BAXH5C1 $BAXH5C2 $BAXH5C3

UNALIGNED=$UNALIGNEDPREFIX.subreads.bam
SINGUNALIGNED=/mnt/user_data/$MIDFOLDER/$UNALIGNEDPREFIX.subreads.bam

#10x CCS
CCSBAM=$CCSPREFIX.ccs.10x.bam
SINGCCSBAM=/mnt/user_data/$MIDFOLDER/$CCSPREFIX.ccs.10x.bam
CCSFQ=$CCSPREFIX.ccs.10x.fastq
singularity exec --bind /net/isi-dcnl/ifs/user_data:/mnt/user_data /home/cwarden/.singularity/cache/oci-tmp/720b8dc1d7aacebe8ed585da5de79118647b303643150ac28a93c014fb04d235/general-pacbio_latest.sif /opt/unanimity/build/ccs --numThreads=16 --minPasses=10 $SINGUNALIGNED $SINGCCSBAM
samtools bam2fq $CCSBAM > $CCSFQ
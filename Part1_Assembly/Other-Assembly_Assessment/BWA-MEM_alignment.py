import sys
import re
import os

read1 = "Contig3_34j16/34J16-H3_sanger_rev.fa"
alnSam = "Contig3_34j16/Sanger/34J16-H3_sanger_rev.sam"
pileup = "Contig3_34j16/Sanger/34J16-H3_sanger_rev.pileup"
bwaRef= "../Contig3_34j16_rev/Contig3.fasta"

#read1 = "173o1/J_AA173O01_rearranged-CWtest3_revcom3.fa"
#alnSam = "173o1/Public/J_AA173O01_rearranged-CWtest3_revcom3.sam"
#pileup = "173o1/Public/J_AA173O01_rearranged-CWtest3_revcom3.pileup"
#bwaRef= "../173o1/173o1.fasta"

command = "samtools faidx " +bwaRef
os.system(command)

command = "bwa index -a bwtsw " +bwaRef
os.system(command)
	
command = "bwa mem -M -t 1 " + bwaRef + " " + read1 + " > " + alnSam
os.system(command)

command = "samtools mpileup -f "+ bwaRef + " " + alnSam + " > " + pileup
os.system(command)
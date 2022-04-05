import sys
import re
import os

read1 = "separate_sequences-Contig1-220203.fasta"
bwaRef= "../Contig1_draft_201118b/Contig1-9changes_201118.fa"
alnSam = "BWA-MEM_Alignment/5clones-220203.sam"
rgSam = "BWA-MEM_Alignment/5clones-220203.rg.sam"

command = "samtools faidx " +bwaRef
os.system(command)

command = "bwa index -a bwtsw " +bwaRef
os.system(command)
	
command = "bwa mem -M -t 1 " + bwaRef + " " + read1 + " > " + alnSam
os.system(command)

command = "java -Xmx8g -jar /opt/picard-2.17.jar AddOrReplaceReadGroups I=" + alnSam + " O=" + rgSam + " SO=coordinate RGID=1 RGLB=BAC RGPL=PacBio RGPU=S00 RGCN=COH RGSM=C1"
os.system(command)

command = "samtools index " + rgSam
os.system(command)
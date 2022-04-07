import sys
import re
import os

read1 = "../../../../latest_sequin_files-G3_submission/Contig1/Contig1.fasta"
alnSam = "conversion.sam"
rgSam = "conversion.rg.sam"
pileup = "conversion.pileup"
bwaRef= "../../../../latest_sequin_files-G3_submission/Contig1-EARLIER/Contig1.fasta"

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

command = "samtools mpileup -f "+ bwaRef + " " + rgSam + " > " + pileup
os.system(command)
import os
import sys
import re

chickenFa = "../190m7/190m7.fasta"
ecoliFa = "../../../galGal5_Indices/CP000948_Ecoli.fa"
faRef = "190m7/190m7_with_Ecoli.fa"
refDict = "190m7/190m7_with_Ecoli.dict"
minimapRef = "190m7/190m7_with_Ecoli.mmi"

#chickenFa = "../173o1/173o1.fasta"
#ecoliFa = "../../../galGal5_Indices/CP000948_Ecoli.fa"
#faRef = "173o1/173o1_with_Ecoli.fa"
#refDict = "173o1/173o1_with_Ecoli.dict"
#minimapRef = "173o1/173o1_with_Ecoli.mmi"

#chickenFa = "../Contig2_58f18/Contig2.fasta"
#ecoliFa = "../../../galGal5_Indices/CP000948_Ecoli.fa"
#faRef = "Contig2_58f18/58f18_with_Ecoli.fa"
#refDict = "Contig2_58f18/58f18_with_Ecoli.dict"
#minimapRef = "Contig2_58f18/58f18_with_Ecoli.mmi"

#chickenFa = "../Contig3_34j16_rev/Contig3.fasta"
#ecoliFa = "../../../galGal5_Indices/CP000948_Ecoli.fa"
#faRef = "Contig3_34j16/34j16_with_Ecoli.fa"
#refDict = "Contig3_34j16/34j16_with_Ecoli.dict"
#minimapRef = "Contig3_34j16/34j16_with_Ecoli.mmi"

command = "cat " + chickenFa + " " + ecoliFa + " > " + faRef
os.system(command)

command = "samtools faidx " +faRef
os.system(command)

command = "bwa index -a bwtsw " +faRef
os.system(command)

command = "/opt/minimap2/minimap2 -k 19 -w 10 -H -d " + minimapRef + " " + faRef
os.system(command)

command = "java -Xmx8g -jar /opt/picard-2.17.jar CreateSequenceDictionary R=" + faRef + " O=" + refDict
os.system(command)
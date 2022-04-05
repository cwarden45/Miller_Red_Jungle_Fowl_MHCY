import os
import sys
import re

seqID = "190m7"

inputFile = "../../../Code/190M/revise_Canu_v1_5/Canu-v1.5-Arrow_190M-rearranged--extra_12bp-expectedBAC/arrow_consensus-qual.txt"
outputFile = "../Assembly_Notes/" + seqID + "_Arrow-LowConfidence.bed"

inHandle = open(inputFile)
outHandle = open(outputFile, "w")

line = inHandle.readline()

line_count = 0

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	line = re.sub("^\s+","",line)
	line = re.sub("\s+","\t",line)
	
	line_count += 1
	
	if line_count > 1:
		lineInfo = line.split("\t")
		pos = int(lineInfo[0])
		qual = int(lineInfo[1])
		
		if qual < 50:
			text = str(pos) + "\t" + str(pos) + "\tArrow_Low_Confidence\t"+str(qual)+"\n"
			outHandle.write(text)
		
	line = inHandle.readline()
	
inHandle.close()

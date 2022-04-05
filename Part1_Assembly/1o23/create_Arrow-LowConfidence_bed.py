import os
import sys
import re

seqID = "1o23"

inputFile = "../../../Code/1o23/revise_Canu_v2_1/Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC/arrow_consensus-qual.txt"
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

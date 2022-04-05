import os
import sys
import re

seqID = "Contig1"

table_name = "TRF"
inputFile = "TRF/" + seqID+".fasta.2.7.7.80.10.50.500.dat"
outputFile = "Repeat_Tables/" + seqID + "_TRF.tbl"

inHandle = open(inputFile)
outHandle = open(outputFile, "w")
text = ">Feature "+seqID+" "+ table_name + "\n"
outHandle.write(text)

line = inHandle.readline()

lineCount = 0

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	line = re.sub("^\s+","",line)
	line = re.sub("\s+","\t",line)
	
	lineCount += 1
	if lineCount > 15:
		lineInfo = line.split("\t")
		start = lineInfo[0]
		stop = lineInfo[1]
		type = lineInfo[13]
		
		text = start + "\t" + stop + "\trepeat_region\t\t\n"
		text = text + "\t\t\trpt_family\t("+type+")n\n"
		text = text + "\t\t\tnote\tTRF repeat\n"
		outHandle.write(text)
			
	line = inHandle.readline()
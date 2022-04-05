import os
import sys
import re

seqID = "Contig1"

table_name = "NOR_rRNA"
inputFile = "NOR/" + seqID + "_rRNA_BLAST_result.txt"
outputFile = "../" + seqID + "_NOR_rRNA_BLAST.tbl"

inHandle = open(inputFile)
outHandle = open(outputFile, "w")
text = ">Feature " + seqID + " "+ table_name + "\n"
outHandle.write(text)

line = inHandle.readline()

while line:
	lineInfo = line.split("\t")
	rRnaName = lineInfo[0]
	start = lineInfo[6]
	stop = lineInfo[7]
	
	text = start + "\t" + stop + "\trRNA\t\t\n"
	outHandle.write(text)
	text = "\t\t\tproduct\t" + rRnaName +" rRNA\n"
	outHandle.write(text)

	line = inHandle.readline()
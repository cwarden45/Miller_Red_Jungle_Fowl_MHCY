import os
import sys
import re

seqID = "Contig1"

table_name = "TRF"
inputFile = "TRF/" + seqID+".fasta.2.7.7.80.10.50.500.dat"
outputFile = "Repeat_Tables/" + seqID + "_TRF.tbl"

#first read through to define minimum length
min_length_hash = {}

inHandle = open(inputFile)
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
		
		pos = start + "-" + stop
		
		if pos in min_length_hash:
			prev_length = min_length_hash[pos]
			if len(type) < prev_length:
				print "Replacing minimum length for " + pos
				min_length_hash[pos]=len(type)
			else:
				print "Skipping repeat with longer unit length for " + pos
		else:
			min_length_hash[pos]=len(type)
			
	line = inHandle.readline()

inHandle.close

#then, read through to create output text

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
		############################
		########## NOTE  ###########
		###Modify at next step #####
		############################
		text = text + "\t\t\ttandem\t"+type+"\n"
		#text = text + "\t\t\tnote\tTRF repeat\n"

		pos = start + "-" + stop
		if len(type) == min_length_hash[pos]:
			outHandle.write(text)
			
	line = inHandle.readline()

inHandle.close
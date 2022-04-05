import os
import sys
import re

header = ">Feature Contig1 RepeatMasker_only"
description = "RepeatMasker repeat"
file1 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
file2 = "Contig1_TRF.tbl"
outputfile = "../../Contig1_RepeatMasker-only.tbl"

#header = ">Feature Contig1 TRF_only"
#description = "TRF repeat"
#file1 = "Contig1_TRF.tbl"
#file2 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
#outputfile = "../../Contig1_TRF-only.tbl"

#create file2 hash
checkHash = {}

inHandle = open(file2)
line = inHandle.readline()
		
line_count = 0

pos = ""

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	
	line_count += 1
	
	if line_count > 1:
		mod_input = line_count - 1
	
		if mod_input % 3 == 1:
			pos = line
		elif mod_input % 3 == 2:
			entry = pos + "\n" + line + "\n"
			checkHash[entry]=1
	line = inHandle.readline()
		
inHandle.close()

#write entries in file1 that are also present in file2

outHandle = open(outputfile, "w")
text = header+"\n"
outHandle.write(text)

inHandle = open(file1)
line = inHandle.readline()
		
line_count = 0
output_text = ""
output_flag = True

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	
	line_count += 1
	
	if line_count > 1:
		mod_input = line_count - 1
	
		if mod_input % 3 == 1:
			output_text = line + "\n"
		elif mod_input % 3 == 2:
			output_text = output_text + line + "\n"
			if output_text in checkHash:
				output_flag = False
				#print "Exclude overlap: " + output_text
		else:
			if output_flag:
				#output_text = output_text + "\t\t\tnote\t"+description+"\n"
				outHandle.write(output_text)
				
			output_text = ""
			output_flag = True
	line = inHandle.readline()
		
inHandle.close()

outHandle.close()
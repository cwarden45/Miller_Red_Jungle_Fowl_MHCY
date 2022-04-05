import os
import sys
import re

contig = "Contig1"
file1 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
file2 = "Contig1_TRF.tbl"
outputfile = "../../Contig1_RepeatMasker_TRF_overlap.tbl"

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
text = ">Feature "+contig+" RepeatMasker_plus_TRF\n"
outHandle.write(text)

inHandle = open(file1)
line = inHandle.readline()
		
line_count = 0
output_text = ""
output_flag = False

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
				output_flag = True
		else:
			if output_flag:
				#output_text = output_text + "\t\t\tnote\tRepeatMasker and TRF repeat\n"
				outHandle.write(output_text)
				
			output_text = ""
			output_flag = False
	line = inHandle.readline()
		
inHandle.close()

outHandle.close()
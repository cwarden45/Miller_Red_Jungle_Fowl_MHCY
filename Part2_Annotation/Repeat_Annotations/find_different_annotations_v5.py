import os
import sys
import re

header = ">Feature Contig1 RepeatMasker_only"
description = "RepeatMasker Annotation"
file1 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
file2 = "Contig1_TRF.tbl"
outputfile = "../../Contig1_RepeatMasker-only.tbl"

#header = ">Feature Contig1 TRF_only"
#description = "Tandem Repeat Finder Annotation"
#file1 = "Contig1_TRF.tbl"
#file2 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
#outputfile = "../../Contig1_TRF-only.tbl"

#create file2 hash --> Only check position because the assumption is to keep TRF repeat is the description is different for the same position.
checkHash = {}
posHash = {}

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
	
		if mod_input % 2 == 1:
			pos = line
			#If we always use TRF, then this is all we need to only keep TRF annotation
			posHash[pos]=1
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
output_flag = False

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	
	line_count += 1
	
	if line_count > 1:
		mod_input = line_count - 1
	
		if mod_input % 2 == 1:
			pos = line
			if (pos not in posHash):
				output_flag = True
			
			output_text = line + "\n"
		else:
			if output_flag:
				if re.search("tandem",line):
					line_info = line.split("\t")
					#print line
					repeat_unit = line_info[4]
					
					if(len(repeat_unit) > 2):
						output_text = output_text + "\t\t\trpt_type\ttandem\n"
						output_text = output_text + "\t\t\tnote\t"+description+"\n"
					else:
						output_text = output_text + "\t\t\trpt_type\tother\n"
						output_text = output_text + "\t\t\tnote\t"+description+": ("+repeat_unit+")n\n"
				elif re.search("other",line):
					line_info = line.split("\t")
					repeat_description = line_info[4]
					#print repeat_description
					output_text = output_text + "\t\t\trpt_type\tother\n"
					output_text = output_text + "\t\t\tnote\t"+description+": "+repeat_description+"\n"
				elif re.search("mobile_element",line):
					output_text = output_text + line + "\n"
					output_text = output_text + "\t\t\tnote\t"+description+"\n"
				else:
					print "Modify code to cover category for line: " + line
					sys.exit()
				outHandle.write(output_text)
			output_flag = False
				
			output_text = ""
	line = inHandle.readline()
		
inHandle.close()

outHandle.close()
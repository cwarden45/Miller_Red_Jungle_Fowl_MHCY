import os
import sys
import re

####################################
###          NOTE                ###
### MUST use `file1` for TRF,    ###
###  for overlapping annotations ###
###(conflict uses TRF annotation)###
####################################

contig = "Contig1"
file1 = "Contig1_TRF.tbl" #MUST be TRF, if you want to use TRF ID over RepeatMasker ID (for different annotations in the same position)
file2 = "Contig1_RepeatMasker_no_rRNA_no_merge.tbl"
outputfile = "../../Contig1_RepeatMasker_TRF_overlap.tbl"

#create file2 hash
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
			posHash[pos]=1
		else:
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
temp_pos = ""

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	
	line_count += 1
	
	if line_count > 1:
		mod_input = line_count - 1
	
		if mod_input % 2 == 1:
			output_text = line + "\n"
			temp_pos = line
		else:
			output_text_CHECK = output_text + line + "\n"
			if output_text_CHECK in checkHash:
				if re.search("tandem",line):
					line_info = line.split("\t")
					#print line
					repeat_unit = line_info[4]
					
					if(len(repeat_unit) > 2):
						output_text = output_text + "\t\t\trpt_type\ttandem\n"
						output_text = output_text + "\t\t\tnote\tRepeatFinder + Tandem Repeat Finder Annotation\n"
					else:
						output_text = output_text + "\t\t\trpt_type\tother\n"
						output_text = output_text + "\t\t\tnote\tRepeatFinder + Tandem Repeat Finder Annotation: ("+repeat_unit+")n\n"
				elif re.search("other",line):
					line_info = line.split("\t")
					repeat_description = line_info[4]
					print repeat_description
					output_text = output_text + "\t\t\trpt_type\tother\n"
					output_text = output_text + "\t\t\tnote\tRepeatFinder + Tandem Repeat Finder Annotation: "+repeat_description+"\n"
					sys.exit()
				else:
					print "Modify code to cover category for line: " + line
					sys.exit()
			
				outHandle.write(output_text)
			elif temp_pos in posHash:
				print "Use **only** TRF Repeat from `file1` for " + temp_pos
				if re.search("tandem",line):
					line_info = line.split("\t")
					#print line
					repeat_unit = line_info[4]
					
					if(len(repeat_unit) > 2):
						output_text = output_text + "\t\t\trpt_type\ttandem\n"
						output_text = output_text + "\t\t\tnote\tTandem Repeat Finder (+ RepeatMasker) Annotation\n"
					else:
						output_text = output_text + "\t\t\trpt_type\tother\n"
						output_text = output_text + "\t\t\tnote\tTandem Repeat Finder (+ RepeatMasker) Annotation: ("+repeat_unit+")n\n"
				else:
					print "Modify code to cover category for MISMATCHED line: " + line
					sys.exit()
				outHandle.write(output_text)
			output_text = ""
	line = inHandle.readline()
		
inHandle.close()

outHandle.close()
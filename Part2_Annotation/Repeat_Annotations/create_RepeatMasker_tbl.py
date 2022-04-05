import os
import sys
import re

seqID = "Contig1"

table_name = "RepeatMasker"
inputFile = "RepeatMasker/"+seqID + ".fasta.out"
outputFile = "Repeat_Tables/" + seqID + "_RepeatMasker_no_rRNA_no_merge.tbl"

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
	if lineCount > 3:
		lineInfo = line.split("\t")
		repName = lineInfo[9]
		repClass = lineInfo[10]
		start = lineInfo[5]
		stop = lineInfo[6]
		
		if repClass == "LTR/ERVK" or repClass == "LTR/ERV1" or repClass == "LTR/ERVL":
			repName = "retroelement retroviral " + repClass + " " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\trpt_family\t" + repName +"\n"
			text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "LINE/CR1" or repClass=="DNA/hAT-Charlie":
			repName = "retroelement " + repClass + " " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\trpt_family\t" + repName +"\n"
			text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "Simple_repeat" or repClass == "Low_complexity":	
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\trpt_family\t" + repName +"\n"
			text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass != "rRNA":
			print "map class " + repClass
			print line
			sys.exit()
			
	line = inHandle.readline()
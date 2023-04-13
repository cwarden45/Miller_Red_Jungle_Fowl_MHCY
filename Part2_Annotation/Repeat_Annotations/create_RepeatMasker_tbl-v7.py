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
		
		if repClass == "LTR/ERVK":
			repName = "retrotransposon:ERVK " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\tmobile_element\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "LTR/ERV1":
			repName = "retrotransposon:ERV1 " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\tmobile_element\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "LTR/ERVL":
			repName = "retrotransposon:ERVL " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\tmobile_element\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "LINE/CR1":
			repName = "LINE:" + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\tmobile_element\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass=="DNA/hAT-Charlie":
			repName = "retrotransposon:DNA/hAT-Charlie " + repName
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			text = text + "\t\t\tmobile_element\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "Simple_repeat":	
			text = start + "\t" + stop + "\trepeat_region\t\t\n"
			repeat_unit = repName
			repeat_unit = re.sub("\(","",repeat_unit)
			repeat_unit = re.sub("\)n","",repeat_unit)
			repName = repeat_unit
			############################
			########## NOTE  ###########
			###Modify at next step #####
			############################
			text = text + "\t\t\ttandem\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass == "Low_complexity":
			#print repName
			#repeat_unit = re.sub("-rich","",repName)
			#repName = "("+repeat_unit+")n"
			#repName = repeat_unit
			text = start + "\t" + stop + "\trepeat_region\t\t\n" 
			text = text + "\t\t\tother\t" + repName +"\n"
			#text = text + "\t\t\tnote\tRepeatMasker repeat\n"
			outHandle.write(text)
		elif repClass != "rRNA":
			print "map class " + repClass
			print line
			sys.exit()
			
	line = inHandle.readline()
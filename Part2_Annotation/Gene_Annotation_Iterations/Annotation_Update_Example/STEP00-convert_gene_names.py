import re
import os
import sys

GTFin = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene-PILEUP-LIFTOVER-BETA.gtf"
GTFout = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene-PILEUP-LIFTOVER-BETA-RENAME_220317.gtf"

#GTFin = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/Intermediate_Files/Contig2_updated_genes_210310-7_EXON_TEST_210527.gtf"
#GTFout = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/Intermediate_Files/Contig2_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"

#GTFin = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/Intermediate_Files/Contig3_updated_genes_220314-YLEC37_pseudogene.gtf"
#GTFout = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/Intermediate_Files/Contig3_updated_genes_220314-YLEC37_pseudogene-RENAME_220317.gtf"

#GTFin = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/Intermediate_Files/Contig4_updated_genes_210310-7_EXON_TEST_210527.gtf"
#GTFout = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/Intermediate_Files/Contig4_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"


mapping_file = "name_updates-v2_from_Marcia-mod.txt"

## mapping hash
nameHash = {}

inHandle = open(mapping_file)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	previous_name = lineInfo[0]
	current_name = lineInfo[1]
	#print "|"+current_name+"|"

	nameHash[previous_name]=current_name
	
	line = inHandle.readline()

inHandle.close()

## convert lines

outHandle = open(GTFout, "w")

inHandle = open(GTFin)
line = inHandle.readline()
		
while line:
	line = re.sub("\r","",line)
	line = re.sub("\n","",line)
	lineInfo = line.split("\t")
	chr = lineInfo[0]
	source = lineInfo[1]
	type = lineInfo[2]
	start_pos = lineInfo[3]
	stop_pos = lineInfo[4]
	score = lineInfo[5]
	strand = lineInfo[6]
	frame = lineInfo[7]
	transcript_info = lineInfo[8]
	
	if (type == "misc_RNA") or (type == "rRNA"):
		text=line + "\n"
		outHandle.write(text)
	else:	
		#print transcript_info
		nameResult = re.search("gene_id \"(.*)\"; gene_name",transcript_info)
		
		if nameResult:
			previous_name = nameResult.group(1)
			#print previous_name
			
			if previous_name in nameHash:
				new_name = nameHash[previous_name]
				transcript_info = "gene_id \""+new_name+"\"; gene_name \""+new_name+"\"; transcript_id \""+new_name+"\""
				text = chr + "\t" + source + "\t" + type + "\t" + start_pos + "\t" + stop_pos + "\t" +  score + "\t" + strand + "\t" + frame + "\t" + transcript_info + "\n"
				outHandle.write(text)
			else:
				print "Issue mapping new name for :" +previous_name
				sys.exit()
		else:
			print "Issue parsing GTF with transcript info: " + transcript_info
			sys.exit()

	line = inHandle.readline()	
	
inHandle.close()
outHandle.close()
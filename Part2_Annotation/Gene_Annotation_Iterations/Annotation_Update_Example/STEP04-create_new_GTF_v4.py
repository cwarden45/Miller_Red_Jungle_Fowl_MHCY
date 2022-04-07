import os
import re
import sys

##you need to manually adjust the NOR locus count for this script.
LOC_count = 3
pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene-PILEUP-LIFTOVER-BETA-RENAME_220317.gtf"
contig = "Contig1"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/Intermediate_Files/Contig2_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"
#contig = "Contig2"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/Intermediate_Files/Contig3_updated_genes_220314-YLEC37_pseudogene-RENAME_220317.gtf"
#contig = "Contig3"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/Intermediate_Files/Contig4_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"
#contig = "Contig4"

locTable = contig+"_LOC_mapping.txt"
gff = contig+"_updated_genes.gtf"

#create LOC mapping
locHash = {}

inHandle = open(locTable)
line = inHandle.readline()

line_count =  0

while line:
	line_count+=1
	
	if line_count > 1:
		lineInfo = line.split("\t")
		full_name = lineInfo[0]
		temp_loc = lineInfo[1]
		locHash[temp_loc]=full_name

	line = inHandle.readline()
inHandle.close()

#read and write GTF
outHandle = open(gff, "w")

locNum = ""
previous_gene = ""

inHandle = open(pileupGTF)
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
	
	if (type == "rRNA") or (type == "misc_RNA"):
		print "Printing NOR annotations for GTF: " + transcript_info

		#this won't separate the loci, but this will avoid errors from formatting
		#transcript_info = "gene_id \""+transcript_info+"\"; gene_name \""+transcript_info+"\"; transcript_id \""+transcript_info+"\""
		#text = chr + "\t" + source + "\t" + type + "\t" + start_pos + "\t" + stop_pos + "\t" +  score + "\t" + strand + "\t" + frame + "\t" + transcript_info + "\n"
		#outHandle.write(text)
		
		#this has already been created, so just print relevant line (and original lines have now been removed)
		text = line + "\n"
		outHandle.write(text)
	else:
		ID=""
		idResult = re.search("gene_id \"(\S+)\"; gene_name",transcript_info)
		if idResult:
			ID = idResult.group(1)
		else:
			print "Error in processing ID for gene: " + transcript_info
			sys.exit()
		
		gene_info = ID.split(".")
		gene_type = gene_info[3]
		
		if type != "rRNA":				
			if previous_gene != gene_type:	
				LOC_count += 1
				locNum = str(LOC_count)
				if(len(locNum) == 1):
					locNum = "0"+locNum

			#print ID
			#print locNum			
			new_ID = locHash["LOC"+locNum]
			#print line
			#print new_ID	
			#sys.exit()
			
			transcript_info = "gene_id \""+new_ID+"\"; gene_name \""+new_ID+"\"; transcript_id \""+new_ID+"\""
			text = chr + "\t" + source + "\t" + type + "\t" + start_pos + "\t" + stop_pos + "\t" +  score + "\t" + strand + "\t" + frame + "\t" + transcript_info + "\n"
			outHandle.write(text)
		else:
			text = line + "\n"
			outHandle.write(text)
		
		previous_gene = gene_type
	
	line = inHandle.readline()
		
inHandle.close()
outHandle.close()

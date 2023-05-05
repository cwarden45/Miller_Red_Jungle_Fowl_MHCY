import re
import os
import sys
#from Bio import SeqIO
#from Bio.Seq import Seq

contig = "19d16"
locTable = "../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_230503/Contig1_LOC_mapping.txt"
STAR_copy_file = "../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_230503/combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM-SUMMED.txt"

gtf = "../"+contig+"_MHCY_pileup_liftover_220324.gtf"
tbl = "../"+contig+"_MHCY_pileup_liftover_220324.tbl"
chr = contig

#LOC hash for longer gene name
descHash = {}
typeHash = {}
geneLengthHash = {}

inHandle = open(locTable)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	name = lineInfo[0]
	geneType = lineInfo[2]
	description = lineInfo[3]
	geneLength = lineInfo[4]
	
	description = re.sub("parial","partial",description)
	description = re.sub("\(MHCY\) class I,","class I heavy chain",description)
	description = re.sub("Major Histocompatibility Complex Y \(MHCY\)","major histocompatibility complex y",description)
	description = re.sub(", candidate NK cell receptor,","",description)
	description = re.sub("C-type lectin","c-type lectin",description)
	description = re.sub("C-type lectin, candidate NK cell receptor, MHCY Region,","c-type lectin",description)
	description = re.sub("Zinc finger protein containing a KRAB domain,","zinc finger protein containing a krab domain",description)
	description = re.sub("Leukocyte receptor cluster encoded novel gene \(LENG\) member 9-Like","leukocyte receptor cluster member 9-like protein",description)
	description = re.sub("Only Zinc Finger-like","only zinc finger-like",description)
	description = re.sub("Major Histocompatibility Complex Y","major histocompatibility complex y",description)
	description = re.sub(", Gene \d+, Type \w","",description)
	description = re.sub(" Gene \d+, Type \w","",description)
	description = re.sub(", Gene \d+","",description)
	#print description
	
	typeHash[name]=geneType
	descHash[name]=description
	geneLengthHash[name]=geneLength
	
	line = inHandle.readline()

inHandle.close()

#hash for type/copy description
copyHash = {}

inHandle = open(STAR_copy_file)
line = inHandle.readline()

lineCount = 0

while line:
	lineCount += 1
	
	if lineCount > 1:
		line = re.sub("\n","",line)
		line = re.sub("\r","",line)
		lineInfo = line.split("\t")
		type = lineInfo[1]
		copies = lineInfo[2]
		copyArr = copies.split(",")
		
		type = re.sub("MHCY-B-","MHCY2B-",type)
		
		if len(copyArr) == 1:		
			copies = re.sub("\w$","",copies)
			text = "Type identified as " + type + " (one copy as "+copies+")"
			
			copyHash[copies]=text
		else:
			for i in xrange(len(copyArr)):
				copyArr[i] = re.sub("\w$","",copyArr[i])
			
			verbal_count = ""
			if len(copyArr) == 2:
				verbal_count = "two"
			elif len(copyArr) == 3:
				verbal_count = "three"
			elif len(copyArr) == 4:
				verbal_count = "four"
			else:
				print "Define word for copy count number: " + str(len(copyArr))
				sys.exit()
			
			text = "Type identified as " +type + " (" + verbal_count+ " 100% identical amino acid copies: "+ ", ".join(copyArr[0:(len(copyArr)-1)])+ " and "+copyArr[len(copyArr)-1]+ ")"
			
			if type == "YLEC-b":
				text = text + "; however, please note that the YLEC9 and YLEC28 CDS sequences are not 100% identical at the nucleotide level"
			
			for gene_copy in copyArr:
				copyHash[gene_copy]=text		
	line = inHandle.readline()

inHandle.close()

#print protein-coding genes
CDShash = {}

#output text and read GTF
outHandle = open(tbl, "w")
text = ">Feature " + contig + " genes\n"
outHandle.write(text)

previous_gene = ""
previous_strand = ""
exon_arr = []

inHandle = open(gtf)
line = inHandle.readline()
		
while line:
	line = re.sub("\r","",line)
	line = re.sub("\n","",line)
	lineInfo = line.split("\t")
	chr = lineInfo[0]
	source = lineInfo[1]
	type = lineInfo[2]
	start_pos = int(lineInfo[3])
	stop_pos = int(lineInfo[4])
	score = lineInfo[5]
	strand = lineInfo[6]
	frame = lineInfo[7]
	transcript_info = lineInfo[8]
	
	if (type == "misc_RNA"):
		prime5_ETS_result = re.search("5ETS",transcript_info)
		ITS1_result = re.search("ITS1",transcript_info)
		ITS2_result = re.search("ITS2",transcript_info)
		prime3_ETS_result = re.search("3ETS",transcript_info)
		
		if prime5_ETS_result:
			#description="5' external transcribed spacer"
			description="external transcribed spacer"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			#text = text + "\t\t\tnote\t5'ETS (ribosomal RNA)\n"
			text = text + "\t\t\tnote\t5'ETS (ribosomal RNA "+description+")\n"
			outHandle.write(text)
		elif ITS1_result:
			description="internal transcribed spacer 1"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			#text = text + "\t\t\tnote\tITS1 (ribosomal RNA)\n"
			text = text + "\t\t\tnote\tITS1 (ribosomal RNA "+description+")\n"
			outHandle.write(text)
		elif ITS2_result:
			description="internal transcribed spacer 2"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			#text = text + "\t\t\tnote\tITS2 (ribosomal RNA)\n"
			text = text + "\t\t\tnote\tITS2 (ribosomal RNA "+description+")\n"
			outHandle.write(text)
		elif prime3_ETS_result:
			#description="3' external transcribed spacer"
			description="external transcribed spacer"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			#text = text + "\t\t\tnote\t3'ETS (ribosomal RNA)\n"
			text = text + "\t\t\tnote\t3'ETS (ribosomal RNA "+description+")\n"
			outHandle.write(text)
		else:
			print "Find way out output Sequin information for :" + transcript_info
			print line
			sys.exit()
	else:
		ID=""
		idResult = re.search("gene_id \"(\S+)\"; gene_name",transcript_info)
		if idResult:
			ID = idResult.group(1)
		else:
			print "Error in processing ID for gene: " + transcript_info
			sys.exit()

		if (type != "rRNA"):
			if previous_gene == "":
				print "Start 1st gene: " + ID + "("+strand+")"
				
				exon = str(start_pos) + "-" + str(stop_pos)
				exon_arr.append(exon)
				#print exon_arr
				#print len(exon_arr)
			elif ID == previous_gene:			
				#exon order for reverse strand is reversed (so, I don't have to change order in array)
				exon = str(start_pos) + "-" + str(stop_pos)
				exon_arr.append(exon)

				print "Extend gene exon array (exon "+str(len(exon_arr))+","+strand+")..."			
			else:
				print "Print Gene Information ("+previous_strand+")"
				
				geneType = ""
				description = ""
				if previous_gene in typeHash:
					geneType = " - " + typeHash[previous_gene]
					description=descHash[previous_gene]
				else:
					print "Need to modify mapping for " + previous_gene + " in " + line
					sys.exit()			
				gene_length = str(geneLengthHash[previous_gene])
				num_exons = len(exon_arr)
					
				shortID = re.sub("Contig\d.LOC\d+.","",previous_gene)
				
				gene_start = -1
				gene_stop = -1
				sequin_gene_start = -1
				sequin_gene_stop = -1
				
				geneText=""
				pseudogeneResult = re.search("P$",previous_gene)
				if pseudogeneResult:
					geneType="pseudogene"
					
					description = re.sub(" containing a KRAB domain","",description)
					description = re.sub(", Pseudogene","",description)
					description = "Fragmentary Gene Sequence: " + description
					description = re.sub(": Candidate Gene","",description)
					
					if num_exons != 1:
						print "Pseudogene with "+str(num_exons)+" exons?"
						sys.exit()
					exonText = exon_arr[0]
					exonInfo = exonText.split("-")
					gene_start = exonInfo[0]
					gene_stop = exonInfo[1]
					
					if previous_strand == "+":
						sequin_gene_start = exonInfo[0]
						sequin_gene_stop = exonInfo[1]
					elif previous_strand == "-":
						#switch order for genes on the reverse strand
						sequin_gene_start = exonInfo[1]
						sequin_gene_stop = exonInfo[0]
					else:
						print "Problem passing frame for "+previous_gene+" : " + previous_strand
					
					printable_gene = previous_gene
					subSearch = re.search("\d\w$",previous_gene)
					pseudoSearch = re.search("P$",previous_gene)
					if subSearch and (not pseudoSearch):
						printable_gene=re.sub("\w$","",previous_gene)
					gene_info = printable_gene.split(".")
					short_gene = gene_info[len(gene_info)-1]
					locus_info = printable_gene
					if re.search("MHCY2B",printable_gene):
						locus_info = locus_info + "; alternatively, " + re.sub("MHCY2B","YFbeta",printable_gene)
					elif re.search("MHCY",printable_gene):
						locus_info = locus_info + "; alternatively, " + re.sub("MHCY","YF",printable_gene) 
					geneText="\t\t\tgene\t" + short_gene + "\n"
					geneText=geneText + "\t\t\tnote\t"+description+".  Locus identified as " + locus_info  + ".\n"
					geneText=geneText+"\t\t\tpseudogene\tunknown\n"					
				else:
					print "CDS code for " + previous_gene
					geneType="CDS"+geneType

					printable_gene = previous_gene
					subSearch = re.search("\d\w$",previous_gene)
					pseudoSearch = re.search("P$",previous_gene)
					if subSearch and (not pseudoSearch):
						printable_gene=re.sub("\w$","",previous_gene)
					gene_info = printable_gene.split(".")
					short_gene = gene_info[len(gene_info)-1]
					locus_info = printable_gene
					if re.search("MHCY2B",printable_gene):
						locus_info = locus_info + "; alternatively, " + re.sub("MHCY2B","YFbeta",printable_gene)
					elif re.search("MHCY",printable_gene):
						locus_info = locus_info + "; alternatively, " + re.sub("MHCY","YF",printable_gene) 
					geneText="\t\t\tgene\t" + short_gene + "\n"
					geneText=geneText + "\t\t\tnote\tLocus identified as " + locus_info  + ".  "
					if short_gene in copyHash:
						copy_text = copyHash[short_gene]
						geneText=geneText + "" + copy_text  + ".\n"
					elif re.search("OZFL",short_gene):
						#copy_text = "No protein-based type defined for "+short_gene
						#geneText=geneText + "" + copy_text  + ".\n"
						geneText=geneText + "\n"
					else:
						print "Error parsing copy information for " + short_gene

					if num_exons == 1:
						print "Possible error that "+ID+" has only "+str(num_exons)+" exon?"

						printable_gene = previous_gene
						subSearch = re.search("\d\w$",previous_gene)
						pseudoSearch = re.search("P$",previous_gene)
						if subSearch and (not pseudoSearch):
							printable_gene=re.sub("\w$","",previous_gene)
							gene_info = printable_gene.split(".")
							short_gene = gene_info[len(gene_info)-1]
							geneText="\t\t\tgene\t" + short_gene + "\n"
							geneText=geneText + "\t\t\tnote\tLocus identified as " + locus_info  + ".  "

						LENG9L_results = re.search("LENG9L",short_gene)
						if LENG9L_results:
							#hard code note for LENG9L, since there are lower-case letters but no STAR splice junction evidence
							print short_gene
							if short_gene == "LENG9L7b":
								copy_text = "Type identified as LENG9L-b (one copy as "+shortID+")"
								geneText=geneText + "" + copy_text  + ".\n"
							else:
								copy_text = "Type identified as LENG9L-a (two 100% identical amino acid copies: LENG9L3 and LENG9L5)"
								geneText=geneText + "" + copy_text  + ".\n"
						
						exonText = exon_arr[0]
						exonInfo = exonText.split("-")
						gene_start = exonInfo[0]
						gene_stop = exonInfo[1]

						if previous_strand == "+":
							sequin_gene_start = exonInfo[0]
							sequin_gene_stop = exonInfo[1]
						elif previous_strand == "-":
							#switch order for genes on the reverse strand
							sequin_gene_start = exonInfo[1]
							sequin_gene_stop = exonInfo[0]
						else:
							print "Problem passing frame for "+previous_gene+" : " + previous_strand				
						
						geneText = geneText +  str(sequin_gene_start) + "\t" + str(sequin_gene_stop) + "\tCDS\t\t\n"
					else:
						#print exon_arr
						for i in xrange(0,len(exon_arr)):
							print exon_arr[i]
							exonText = exon_arr[i]
							exonInfo = exonText.split("-")

							exon_start=-1
							exon_stop=-1
							if previous_strand == "+":
								exon_start = int(exonInfo[0])
								exon_stop = int(exonInfo[1])
							elif previous_strand == "-":
								#switch order for genes on the reverse strand
								exon_start = int(exonInfo[1])
								exon_stop = int(exonInfo[0])
							else:
								print "Problem passing frame for "+previous_gene+" : " + previous_strand				


							if i == 0:
								gene_start = exonInfo[0]
								gene_stop = exonInfo[1]

								sequin_gene_start = exon_start
								sequin_gene_stop = exon_stop

								#print str(sequin_gene_start) + ":" + str(sequin_gene_stop)
								geneText = geneText +  str(exon_start) + "\t" + str(exon_stop) + "\tCDS\t\t\n"						
							else:
								if previous_strand == "+":
									if exon_stop > sequin_gene_stop:
										gene_stop =  exonInfo[1]
										sequin_gene_stop =  exon_stop
									else:
										print "Problem with gene on positive strand having increasing order exons?"
										print sequin_gene_stop
										print exon_stop
										sys.exit()
								elif previous_strand == "-":
									if exon_stop < sequin_gene_start:
										gene_start =  exonInfo[0]
										sequin_gene_stop =  exon_stop
									else:
										print "Problem with gene on negative strand having decreasing order exons?"
										print exon_start
										print sequin_gene_start
										sys.exit()

								#print str(sequin_gene_start) + ":" + str(sequin_gene_stop)
								geneText = geneText +  str(exon_start) + "\t" + str(exon_stop) + "\t\t\t\n"

								
				text = str(sequin_gene_start) + "\t" + str(sequin_gene_stop) + "\tgene\t\t\n"
				if not pseudogeneResult:				
					geneText=geneText + "\t\t\tgene\t" + short_gene + "\n"
					geneText=geneText + "\t\t\tproduct\t"+description+"\n"
				text = text + geneText	

				outHandle.write(text)
				
				MHCY1_type = "NA"
				if geneType == "CDS - MHCY":
					typeResult = re.search("MHCY\\d+(\w)",shortID)
					
					if typeResult:
						MHCY1_type = "MHCY1 - "+typeResult.group(1)
					else:
						print "Issue paring MHCY 1 type: "+ shortID
						sys.exit()
				elif geneType == "CDS - YLEC":
					typeResult = re.search("YLEC\\d+(\w)",shortID)
					
					if typeResult:
						MHCY1_type = "YLEC - "+typeResult.group(1)
					else:
						print "Issue paring YLEC type: "+ shortID
						sys.exit()
						
				if geneType == "pseudogene":
					num_exons = "unknown"
				else:
					num_exons = str(num_exons)
							
				#initiate new gene
				print "Start Gene: " + ID	
				exon_arr =  []
				exon = str(start_pos) + "-" + str(stop_pos)
				exon_arr.append(exon)
				#print exon_arr
				#print len(exon_arr)
				
			previous_gene = ID
			previous_strand = strand
		elif (type == "rRNA"):
			geneType = ""
			description = ""
			if ID in typeHash:
				geneType = typeHash[ID]
				description=descHash[ID]
			else:
				print "Need to modify mapping for " + ID + " in " + line
				sys.exit()			
			gene_length = str(geneLengthHash[ID])
			num_exons = 1#hard coded for rRNA

			if re.search("5-8S", ID):
				rRNA_type = "5.8S rRNA"
			elif re.search("18S", ID):
				rRNA_type = "18S rRNA"
			elif re.search("28S", ID):
				rRNA_type = "28S rRNA"
			else:
				print "Define rRNA type for " + ID
				sys.exit()
						
			#hard coded solution (better to start at the beginning)
			ID = re.sub("LENG9_","LENG9L",ID)
			
			shortID = re.sub("Contig\d.LOC\d+.","",ID)

			#there is already another file, so I am not sure if this will be used
			text = str(start_pos) + "\t" + str(stop_pos) + "\trRNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			outHandle.write(text)
	
	line = inHandle.readline()
		
inHandle.close()

sys.exit()

### add code to write last gene annotation ###
shortID = re.sub("Contig\d.LOC\d+.","",previous_gene)
print "Print Gene Information ("+previous_strand+")"

geneType = ""
description = ""
if previous_gene in typeHash:
	geneType = " - " + typeHash[previous_gene]
	description=descHash[previous_gene]
else:
	print "Need to modify mapping for " + previous_gene + " in " + line
	sys.exit()

num_exons = len(exon_arr)

gene_start = -1
gene_stop = -1
sequin_gene_start = -1
sequin_gene_stop = -1

geneText=""
pseudogeneResult = re.search("P$",previous_gene)
if pseudogeneResult:
	geneType="pseudogene"
	
	description = re.sub(" containing a KRAB domain","",description)
	description = re.sub(", Pseudogene","",description)
	description = description + " (Fragmentary Gene Sequence and/or Pseudogene)"
	
	if num_exons != 1:
		print "Pseudogene with "+str(num_exons)+" exons?"
		sys.exit()
	exonText = exon_arr[0]
	exonInfo = exonText.split("-")
	gene_start = exonInfo[0]
	gene_stop = exonInfo[1]
	
	if previous_strand == "+":
		sequin_gene_start = exonInfo[0]
		sequin_gene_stop = exonInfo[1]
	elif previous_strand == "-":
		#switch order for genes on the reverse strand
		sequin_gene_start = exonInfo[1]
		sequin_gene_stop = exonInfo[0]
	else:
		print "Problem passing frame for "+previous_gene+" : " + previous_strand
	geneText = "\t\t\tlocus_tag\t" + previous_gene + "\n"
	geneText = geneText + "\t\t\tgene\t"+description+"\n"
	geneText = geneText+"\t\t\tpseudogene\tunknown\n"	
else:
	print "CDS code for " + previous_gene
	geneType="CDS"+geneType

	printable_gene = previous_gene
	subSearch = re.search("\d\w$",previous_gene)
	pseudoSearch = re.search("P$",previous_gene)
	if subSearch and (not pseudoSearch):
		printable_gene=re.sub("\w$","",previous_gene)
	geneText="\t\t\tlocus_tag\t" + printable_gene + "\n"
	geneText= geneText + "\t\t\tgene\t"+description+"\n"

	print shortID
	copyID = shortID
	copyID = re.sub("^RJF.","",copyID)
	copyID = re.sub("\w$","",copyID)#don't worry about for OZFL or LENG9L, which lack splice junction evdience
	if copyID in copyHash:
		copy_text = copyHash[copyID]
		geneText = geneText + "\t\t\tnote\t"+copy_text+"\n"

	if num_exons == 1:
		print "Possible error that "+ID+" has only "+str(num_exons)+" exon?"

		printable_gene = previous_gene
		subSearch = re.search("\d\w$",previous_gene)
		pseudoSearch = re.search("P$",previous_gene)
		if subSearch and (not pseudoSearch):
			printable_gene=re.sub("\w$","",previous_gene)
		geneText="\t\t\tlocus_tag\t" + printable_gene + "\n"
		geneText= geneText + "\t\t\tgene\t"+description+"\n"
		if LENG9L_results:
			#hard code note for LENG9L, since there are lower-case letters but no STAR splice junction evidence
			print shortID
			if shortID == "LENG9L7b":
				copy_text = "LENG9L-b (one copy, among Contigs 1-4)"
				geneText = geneText + "\t\t\tnote\t"+copy_text+"\n"
			else:
				copy_text = "LENG9L-a (two 100% identical amino acid copies: LENG9L3 and LENG9L5, among Contigs 1-4)"
				geneText = geneText + "\t\t\tnote\t"+copy_text+"\n"						
				
		exonText = exon_arr[0]
		exonInfo = exonText.split("-")
		gene_start = exonInfo[0]
		gene_stop = exonInfo[1]

		if previous_strand == "+":
			sequin_gene_start = exonInfo[0]
			sequin_gene_stop = exonInfo[1]
		elif previous_strand == "-":
			#switch order for genes on the reverse strand
			sequin_gene_start = exonInfo[1]
			sequin_gene_stop = exonInfo[0]
		else:
			print "Problem passing frame for "+previous_gene+" : " + previous_strand	
		
		geneText = geneText +  str(sequin_gene_start) + "\t" + str(sequin_gene_stop) + "\tCDS\t\t\n"
	else:
		#print exon_arr
		for i in xrange(0,len(exon_arr)):
			print exon_arr[i]
			exonText = exon_arr[i]
			exonInfo = exonText.split("-")

			exon_start=-1
			exon_stop=-1
			if previous_strand == "+":
				exon_start = int(exonInfo[0])
				exon_stop = int(exonInfo[1])
			elif previous_strand == "-":
				#switch order for genes on the reverse strand
				exon_start = int(exonInfo[1])
				exon_stop = int(exonInfo[0])
			else:
				print "Problem passing frame for "+previous_gene+" : " + previous_strand	


			if i == 0:
				gene_start = exonInfo[0]
				gene_stop = exonInfo[1]

				sequin_gene_start = exon_start
				sequin_gene_stop = exon_stop

				#print str(sequin_gene_start) + ":" + str(sequin_gene_stop)
				geneText = geneText +  str(exon_start) + "\t" + str(exon_stop) + "\tCDS\t\t\n"
	
			else:
				if previous_strand == "+":
					if exon_stop > sequin_gene_stop:
						gene_stop =  exonInfo[1]
						sequin_gene_stop =  exon_stop
					else:
						print "Problem with gene on positive strand having increasing order exons?"
						print sequin_gene_stop
						print exon_stop
						sys.exit()
				elif previous_strand == "-":
					if exon_stop < sequin_gene_start:
						gene_start =  exonInfo[0]
						sequin_gene_stop =  exon_stop
					else:
						print "Problem with gene on negative strand having decreasing order exons?"
						print exon_start
						print sequin_gene_start
						sys.exit()

				#print str(sequin_gene_start) + ":" + str(sequin_gene_stop)
				geneText = geneText +  str(exon_start) + "\t" + str(exon_stop) + "\t\t\t\n"

						
text = str(sequin_gene_start) + "\t" + str(sequin_gene_stop) + "\tgene\t\t\n"
text = text + geneText

outHandle.write(text)

outHandle.close()
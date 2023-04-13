import re
import os
import sys
#from Bio import SeqIO
from Bio.Seq import Seq

contig = "Contig1"
#contig = "Contig2"
#contig = "Contig3"
#contig = "Contig4"

gtf = contig+"_updated_genes.gtf"
tbl = contig+"_BLAST_annotated_gene_v18.tbl"
contig1table = contig+"_contig_name_Contig1_BLAST_mapping.txt"
contig2table = contig+"_contig_name_Contig2_BLAST_mapping.txt"
contig3table = contig+"_contig_name_Contig3_BLAST_mapping.txt"
contig4table = contig+"_contig_name_Contig4_BLAST_mapping.txt"
RefSeqTable = contig+"_contig_name_RefSeq_BLAST_mapping.txt"
cdnaTable = contig+"_contig_name_cDNA_BLAST_mapping.txt"
locTable = contig+"_LOC_mapping.txt"
paperTable = contig+"_gene_summary.txt"

#copy mapping from STAR splice junction analysis
#NOTE: I modified a column within file so that the genes could appear in numeric order
STAR_copy_file = "combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM-SUMMED.txt"

#currently, gene name distinguishes contig
EST_IsoSeq_table = "EST_multimap_evidence.txt"

chr = contig

#print protein-coding genes
CDShash = {}

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
	description = re.sub("\(MHCY\) class I,","(MHCY) class I heavy chain,",description)
	description = re.sub("candidate NK cell receptor,","candidate NK cell receptor, MHCY Region,",description)
	description = re.sub("C-type lectin, candidate NK cell receptor, MHCY Region,","Candidate Gene, MHCY Region: C-type lectin,",description)
	description = re.sub("containing a KRAB domain,","containing a KRAB domain, MHCY Region,",description)
	description = re.sub("Leukocyte receptor cluster encoded novel gene \(LENG\) member 9-Like","leukocyte receptor cluster member 9-like, MHCY Region",description)
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

#hash for RefSeq notes
refSeqHash = {}

inHandle = open(RefSeqTable)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	gene = lineInfo[0]
	refseq = re.sub("\.\d+$","",lineInfo[4])
	hitLength = lineInfo[8]
	percentIdentity = lineInfo[9]
	queryLength = str(geneLengthHash[gene])#also in file, but I  can check for error messages
	print line
	print gene
	print refseq
	print percentIdentity
	print queryLength
	print hitLength
	
	if gene in refSeqHash:
		refSeqHash[gene] = refSeqHash[gene] + " , " + percentIdentity + "% identity to " + refseq + " for " +hitLength+  " bp"
	else:
		refSeqHash[gene] = percentIdentity + "% identity to " + refseq + " for " +hitLength+  " bp"
	line = inHandle.readline()

inHandle.close()

#hash for cDNA notes
cdnaHash = {}

if os.path.exists(cdnaTable):
	inHandle = open(cdnaTable)
	line = inHandle.readline()

	while line:
		line = re.sub("\n","",line)
		line = re.sub("\r","",line)
		lineInfo = line.split("\t")
		gene = lineInfo[0]
		cDNA_name = re.sub("\.\d+$","",lineInfo[4])
		hitLength = lineInfo[8]
		percentIdentity = lineInfo[9]
		queryLength = str(geneLengthHash[gene])#also in file, but I  can check for error messages
		print line
		print gene
		print cDNA_name
		print percentIdentity
		print queryLength
		print hitLength
		
		if gene in cdnaHash:
			#cdnaHash[gene] = cdnaHash[gene] + " , " + percentIdentity + "% identity to " + cDNA_name + " for " +hitLength+  " bp"
			cdnaHash[gene] = cdnaHash[gene] + " , " + cDNA_name
		else:
			#cdnaHash[gene] = percentIdentity + "% identity to " + cDNA_name + " for " +hitLength+  " bp"
			cdnaHash[gene] = cDNA_name
		line = inHandle.readline()

	inHandle.close()

#hash for Contig1 notes
contig1hash = {}

inHandle = open(contig1table)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	gene1 = lineInfo[0]
	gene2 = lineInfo[4]
	hitLength = lineInfo[8]
	percentIdentity = lineInfo[9]
	
	printable_gene1=gene1
	printable_gene2=gene2
	lcSearch1 = re.search("\d\w$",gene1)
	lcSearch2 = re.search("\d\w$",gene2)
	pseudoSearch = re.search("P$",gene2)
	if lcSearch1 and (not pseudoSearch):
		printable_gene1=re.sub("\w$","",gene1)
	if lcSearch2 and (not pseudoSearch):
		printable_gene2=re.sub("\w$","",gene2)

	if gene1 in contig1hash:
		gene2Result = re.search(gene2, contig1hash[gene1])
		if not gene2Result:
			contig1hash[gene1] = contig1hash[gene1] + " , " + percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
	else:
		contig1hash[gene1] = percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
		
	#add extra mappings so that duplicates on Contig1 can also be noted
	if gene2 in contig1hash:
		gene1Result = re.search(gene1, contig1hash[gene2])
		if not gene1Result:
			contig1hash[gene2] = contig1hash[gene2] + " , " + percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	else:
		contig1hash[gene2] = percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	
	line = inHandle.readline()

inHandle.close()

#hash for Contig2 notes
contig2hash = {}

inHandle = open(contig2table)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	gene1 = lineInfo[0]
	gene2 = lineInfo[4]
	hitLength = lineInfo[8]
	percentIdentity = lineInfo[9]

	printable_gene1=gene1
	printable_gene2=gene2
	lcSearch1 = re.search("\d\w$",gene1)
	lcSearch2 = re.search("\d\w$",gene2)
	pseudoSearch = re.search("P$",gene2)
	if lcSearch1 and (not pseudoSearch):
		printable_gene1=re.sub("\w$","",gene1)
	if lcSearch2 and (not pseudoSearch):
		printable_gene2=re.sub("\w$","",gene2)
	
	if gene1 in contig2hash:
		gene2Result = re.search(gene2, contig2hash[gene1])
		if not gene2Result:
			contig2hash[gene1] = contig2hash[gene1] + " , " + percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
	else:
		contig2hash[gene1] = percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
		
	#add extra mappings so that duplicates on Contig1 can also be noted
	if gene2 in contig2hash:
		gene1Result = re.search(gene1, contig2hash[gene2])
		if not gene1Result:
			contig2hash[gene2] = contig2hash[gene2] + " , " + percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	else:
		contig2hash[gene2] = percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	
	line = inHandle.readline()

inHandle.close()

#hash for Contig3 notes
contig3hash = {}

inHandle = open(contig3table)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	gene1 = lineInfo[0]
	gene2 = lineInfo[4]
	hitLength = lineInfo[8]
	percentIdentity = lineInfo[9]

	printable_gene1=gene1
	printable_gene2=gene2
	lcSearch1 = re.search("\d\w$",gene1)
	lcSearch2 = re.search("\d\w$",gene2)
	pseudoSearch = re.search("P$",gene2)
	if lcSearch1 and (not pseudoSearch):
		printable_gene1=re.sub("\w$","",gene1)
	if lcSearch2 and (not pseudoSearch):
		printable_gene2=re.sub("\w$","",gene2)
	
	if gene1 in contig3hash:
		gene2Result = re.search(gene2, contig3hash[gene1])
		if not gene2Result:
			contig3hash[gene1] = contig3hash[gene1] + " , " + percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
	else:
		contig3hash[gene1] = percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
		
	#add extra mappings so that duplicates on Contig1 can also be noted
	if gene2 in contig3hash:
		gene1Result = re.search(gene1, contig3hash[gene2])
		if not gene1Result:
			contig3hash[gene2] = contig3hash[gene2] + " , " + percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	else:
		contig3hash[gene2] = percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	
	line = inHandle.readline()

inHandle.close()

#hash for Contig4 notes
contig4hash = {}

inHandle = open(contig4table)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	gene1 = lineInfo[0]
	gene2 = lineInfo[4]
	hitLength = lineInfo[8]
	percentIdentity = lineInfo[9]

	printable_gene1=gene1
	printable_gene2=gene2
	lcSearch1 = re.search("\d\w$",gene1)
	lcSearch2 = re.search("\d\w$",gene2)
	pseudoSearch = re.search("P$",gene2)
	if lcSearch1 and (not pseudoSearch):
		printable_gene1=re.sub("\w$","",gene1)
	if lcSearch2 and (not pseudoSearch):
		printable_gene2=re.sub("\w$","",gene2)

	if gene1 in contig4hash:
		gene2Result = re.search(gene2, contig4hash[gene1])
		if not gene2Result:
			contig4hash[gene1] = contig4hash[gene1] + " , " + percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
	else:
		contig4hash[gene1] = percentIdentity + "% identity to " + printable_gene2 + " for " +hitLength+  " bp"
		
	#add extra mappings so that duplicates on Contig1 can also be noted
	if gene2 in contig4hash:
		gene1Result = re.search(gene1, contig4hash[gene2])
		if not gene1Result:
			contig4hash[gene2] = contig4hash[gene2] + " , " + percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	else:
		contig4hash[gene2] = percentIdentity + "% identity to " + printable_gene1 + " for " +hitLength+  " bp"
	
	line = inHandle.readline()

inHandle.close()

#EST hash
estHash = {}

inHandle = open(EST_IsoSeq_table)
line = inHandle.readline()

lineCount = 0

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	
	lineCount +=1
	
	geneName = lineInfo[0]
	NCBI_EST = lineInfo[1]
	Partial_MHCY = lineInfo[2]
	
	if lineCount > 1:
		#only provide NCBI Accessions (and custom annotations)
		if Partial_MHCY == "NA":
			if NCBI_EST != "NA":
				estHash[geneName]=NCBI_EST
		elif NCBI_EST != "NA":
			combined_ESTlike = Partial_MHCY+","+NCBI_EST
			estHash[geneName]=combined_ESTlike
		elif NCBI_EST == "NA":
			estHash[geneName]=Partial_MHCY
	
	line = inHandle.readline()

inHandle.close()

#output text and read GTF
outHandle = open(tbl, "w")
text = ">Feature " + contig + " genes\n"
outHandle.write(text)

if contig == "Contig1":
	rRNA_table = contig+"_NOR_rRNA_BLAST.tbl"
	
	rrnaHandle = open(rRNA_table, "w")
	
	text = ">Feature " + contig + " rRNA\n"
	rrnaHandle.write(text)	

paperHandle = open(paperTable,"w")
text = "Contig\tLocation\tFull.Name\tContig.Gene.Name\tGene.Category\tContig1.Homology\tContig2.Homology\tContig3.Homology\tContig4.Homology\tGene.Type\tNum.Exons\tGene_Length\tOrientation\tExtended.RefSeq\tCOH.cDNA.Validation\tExtended.EST.Hits\tFull.Name\n";
paperHandle.write(text)

previous_gene = ""
previous_strand = ""
exon_arr =  []

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
			description="5' external transcribed spacer"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			text = text + "\t\t\tnote\t5'ETS (ribosomal RNA)\n"
			rrnaHandle.write(text)
		elif ITS1_result:
			description="Internal Transcribed Spacer 1"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			text = text + "\t\t\tnote\tITS1 (ribosomal RNA)\n"
			rrnaHandle.write(text)
		elif ITS2_result:
			description="Internal Transcribed Spacer 2"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			text = text + "\t\t\tnote\tITS2 (ribosomal RNA)\n"
			rrnaHandle.write(text)
		elif prime3_ETS_result:
			description="3' external transcribed spacer"

			text = str(start_pos) + "\t" + str(stop_pos) + "\tmisc_RNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			text = text + "\t\t\tnote\t3'ETS (ribosomal RNA)\n"
			rrnaHandle.write(text)
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

				refseqHomology = "NA"
				if previous_gene in refSeqHash:
					refseqHomology = refSeqHash[previous_gene]

				cdnaHomology = "NA"
				if previous_gene in cdnaHash:
					cdnaHomology = cdnaHash[previous_gene]

				contig1homology = "NA"
				if previous_gene in contig1hash:
					contig1homology = contig1hash[previous_gene]

				contig2homology = "NA"
				if previous_gene in contig2hash:
					contig2homology = contig2hash[previous_gene]

				contig3homology = "NA"
				if previous_gene in contig3hash:
					contig3homology = contig3hash[previous_gene]

				contig4homology = "NA"
				if previous_gene in contig4hash:
					contig4homology = contig4hash[previous_gene]

				EST_evidence = "None"
				if previous_gene in estHash:
					EST_evidence = estHash[previous_gene]
					
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
						copy_text = "No protein-based type defined for "+short_gene
						geneText=geneText + "" + copy_text  + ".\n"
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

				if pseudogeneResult:				
					refseqHomology = "pseudogene"			
				
				if refseqHomology == "NA":
					refseqHomology = "None"
				elif refseqHomology != "pseudogene":
					#print refseqHomology
					
					#https://www.ncbi.nlm.nih.gov/books/NBK50679/#RefSeqFAQ.what_is_the_difference_between
					new_refseq = ""
					refseq_arr = refseqHomology.split(" , ")
					predicted_flag = 0
					for j in xrange(0,len(refseq_arr)):
						predResult1 = re.search("miscrna_XR",refseq_arr[j])
						predResult2 = re.search("mrna_XM",refseq_arr[j])

						if (not predResult1) and (not predResult2):
							if new_refseq == "":
								new_refseq = refseq_arr[j]
							else:
								new_refseq = new_refseq + " , " +refseq_arr[j]
						else:
							predicted_flag=1

					if new_refseq == "":
						refseqHomology = "RefSeq Predicted Genes"
					else:
						if predicted_flag==0:
							refseqHomology = new_refseq
						else:
							refseqHomology = new_refseq+" , RefSeq Predicted Genes"
					#print refseqHomology

					#if refseqHomology != "RefSeq Predicted Genes":
					#	#simplify information for GenBank submission (but keep for other table)
					#	text = text + "\t\t\tnote\t"+refseqHomology+"\n"

				#if cdnaHomology != "NA":
				#	text = text + "\t\t\tnote\t"+cdnaHomology+"\n"

				#if contig1homology != "NA":
				#	text = text + "\t\t\tnote\t"+contig1homology+"\n"
				#if contig2homology != "NA":
				#	text = text + "\t\t\tnote\t"+contig2homology+"\n"
				#if contig3homology != "NA":
				#	text = text + "\t\t\tnote\t"+contig3homology+"\n"
				#if contig4homology != "NA":
				#	text = text + "\t\t\tnote\t"+contig4homology+"\n"
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
				
				#text = "Contig\tLocation\tFull.Name\tContig.Gene.Name\tGene.Category\tContig1.Homology\tContig2.Homology\tContig3.Homology\tContig4.Homology\tGene.Type\tNum.Exons\tGene_Length\tOrientation\tExtended.RefSeq\tCOH.cDNA.Validation\tExtended.EST.Hits\tFull.Name\n";
				text = contig + "\t" + str(gene_start) + "-" + str(gene_stop) + "\t"+previous_gene+"\t" + shortID + "\t"+geneType+"\t"+contig1homology+"\t"+contig2homology+"\t"+contig3homology+"\t"+contig4homology+"\t"+MHCY1_type+"\t"+num_exons+ "\t"+gene_length+"\t"+previous_strand+"\t"+refseqHomology+"\t"+cdnaHomology+"\t"+EST_evidence+"\t"+previous_gene+"\n";
				paperHandle.write(text)
				
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
			contig1homology = "NA"
			refseqHomology = "NA"
			if ID in refSeqHash:
				refseqHomology = refSeqHash[ID]

			if ID in contig1hash:
				contig1homology = contig1hash[ID]

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

			EST_evidence = "None"
			if ID in estHash:
				EST_evidence = estHash[ID]
							
			#hard coded solution (better to start at the beginning)
			ID = re.sub("LENG9_","LENG9L",ID)
			
			shortID = re.sub("Contig\d.LOC\d+.","",ID)

			#text = "Contig\tLocation\tFull.Name\tContig.Gene.Name\tGene.Category\tContig1.Homology\tContig2.Homology\tContig3.Homology\tContig4.Homology\tGene.Type\tNum.Exons\tGene_Length\tOrientation\tExtended.RefSeq\tCOH.cDNA.Validation\tExtended.EST.Hits\tFull.Name\n";
			text = contig + "\t" + str(start_pos) + "-" + str(stop_pos)+"\t"+ID+"\t" + shortID +"\trRNA\tNA\tNA\tNA\tNA\t"+rRNA_type+"\ttranscript cluster, multiple intronless genes\t"+gene_length+"\t"+strand+"\tDefined from KT445934 Annotations\tNA\t"+EST_evidence+"\t"+ID+"\n";
			paperHandle.write(text)

			#there is already another file, so I am not sure if this will be used
			text = str(start_pos) + "\t" + str(stop_pos) + "\trRNA\t\t\n"
			text = text + "\t\t\tproduct\t" + description + "\n"
			rrnaHandle.write(text)
	
	line = inHandle.readline()
		
inHandle.close()

if contig == "Contig1":
	rrnaHandle.close()


### add code to write last gene annotation ###
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

refseqHomology = "NA"
if previous_gene in refSeqHash:
	refseqHomology = refSeqHash[previous_gene]

cdnaHomology = "NA"
if previous_gene in cdnaHash:
	cdnaHomology = cdnaHash[previous_gene]

contig1homology = "NA"
if previous_gene in contig1hash:
	contig1homology = contig1hash[previous_gene]

contig2homology = "NA"
if previous_gene in contig2hash:
	contig2homology = contig2hash[previous_gene]

contig3homology = "NA"
if previous_gene in contig3hash:
	contig3homology = contig3hash[previous_gene]

contig4homology = "NA"
if previous_gene in contig4hash:
	contig4homology = contig4hash[previous_gene]

EST_evidence = "None"
if previous_gene in estHash:
	EST_evidence = estHash[previous_gene]
	
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
		copy_text = "No protein-based type defined for "+short_gene
		geneText=geneText + "" + copy_text  + ".\n"
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
	#printable_gene=re.sub("\w$","",previous_gene)
	#gene_info = printable_gene.split(".")
	#short_gene = gene_info[len(gene_info)-1]
	geneText=geneText + "\t\t\tgene\t" + short_gene + "\n"
	geneText=geneText + "\t\t\tproduct\t"+description+"\n"
text = text + geneText	

if pseudogeneResult:		
	refseqHomology = "pseudogene"	

if refseqHomology == "NA":
	refseqHomology = "None"
elif refseqHomology != "pseudogene":
	#print refseqHomology
	
	#https://www.ncbi.nlm.nih.gov/books/NBK50679/#RefSeqFAQ.what_is_the_difference_between
	new_refseq = ""
	refseq_arr = refseqHomology.split(" , ")
	predicted_flag = 0
	for j in xrange(0,len(refseq_arr)):
		predResult1 = re.search("miscrna_XR",refseq_arr[j])
		predResult2 = re.search("mrna_XM",refseq_arr[j])

		if (not predResult1) and (not predResult2):
			if new_refseq == "":
				new_refseq = refseq_arr[j]
			else:
				new_refseq = new_refseq + " , " +refseq_arr[j]
		else:
			predicted_flag=1

	if new_refseq == "":
		refseqHomology = "RefSeq Predicted Genes"
	else:
		if predicted_flag==0:
			refseqHomology = new_refseq
		else:
			refseqHomology = new_refseq+" , RefSeq Predicted Genes"
	#print refseqHomology

	#if refseqHomology != "RefSeq Predicted Genes":
	#	#simplify information for GenBank submission (but keep for other table)
	#	text = text + "\t\t\tnote\t"+refseqHomology+"\n"

#if cdnaHomology != "NA":
#	text = text + "\t\t\tnote\t"+cdnaHomology+"\n"

#if contig1homology != "NA":
#	text = text + "\t\t\tnote\t"+contig1homology+"\n"
#if contig2homology != "NA":
#	text = text + "\t\t\tnote\t"+contig2homology+"\n"
#if contig3homology != "NA":
#	text = text + "\t\t\tnote\t"+contig3homology+"\n"
#if contig4homology != "NA":
#	text = text + "\t\t\tnote\t"+contig4homology+"\n"
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
				
text = contig + "\t" + str(gene_start) + "-" + str(gene_stop) + "\t"+previous_gene+"\t" + shortID + "\t"+geneType+"\t"+contig1homology+"\t"+contig2homology+"\t"+contig3homology+"\t"+contig4homology+"\t"+MHCY1_type+"\t"+num_exons+ "\t"+gene_length+"\t"+previous_strand+"\t"+refseqHomology+"\t"+cdnaHomology+"\t"+EST_evidence+"\t"+previous_gene+"\n";
paperHandle.write(text)

outHandle.close()
paperHandle.close()
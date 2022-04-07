import os
import re
import sys
from Bio import SeqIO
from Bio.Seq import Seq

##you may or may not need to adjust the LOC count, depending upon if the upstream file contains the rRNA genes
LOC_count = 0
pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene-PILEUP-LIFTOVER-BETA-RENAME_220317.gtf"
prev_YLec = 0
prev_YF = 0
prev_LENG = 0
prev_ZNF = 0
prev_YLBII = 0
contig = "Contig1"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/Intermediate_Files/Contig2_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"
#prev_YLec = 19
#prev_YF = 20
#prev_LENG = 3
#prev_ZNF = 2
#prev_YLBII = 4
#contig = "Contig2"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/Intermediate_Files/Contig3_updated_genes_220314-YLEC37_pseudogene-RENAME_220317.gtf"
#prev_YLec = 29
#prev_YF = 33
#prev_LENG = 5
#prev_ZNF = 2
#prev_YLBII = 5
#contig = "Contig3"

#LOC_count = 0
#pileupGTF = "../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/Intermediate_Files/Contig4_updated_genes_210310-7_EXON_TEST_210527-RENAME_220317.gtf"
#prev_YLec = 38
#prev_YF = 40
#prev_LENG = 7
#prev_ZNF = 4
#prev_YLBII = 8
#contig = "Contig4"

locTable = contig+"_LOC_mapping.txt"
seqs = contig+"_gene_named.fa"
peps = contig+"_gene_prot.fa"

outHandle = open(seqs, "w")
pepHandle = open(peps, "w")
mapHandle = open(locTable, "w")
text = "Pos.Name\tLocID\tFamily\tDescription\tLength\n"
mapHandle.write(text)

FAfile = contig + ".fasta"
fasta_parser = SeqIO.read(FAfile, "fasta")
seq =  str(fasta_parser.seq)

#some slides reversed the order, but here the copy counts positively correlate with the locus count
rRNA_count = 3#start with last number, so that it will be 1 next to MHC-Y region

previous_ID = ""
previous_type = ""
previous_gene = ""
gene_start = -1
gene_stop = -1
gene_strand = ""
rna = ""

inHandle = open(pileupGTF)
line = inHandle.readline()
		
while line:
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
	
	if type != "misc_RNA":
		ID=""
		idResult = re.search("gene_id \"(\S+)\"; gene_name",transcript_info)
		if idResult:
			ID = idResult.group(1)
		else:
			print "Error in processing ID for gene: " + transcript_info
			sys.exit()
		
		print ID
		gene_info = ID.split(".")
		gene_type = gene_info[3]

		if (type != "rRNA")and(type != "misc_RNA"):
			#yfaResult = re.search("YF\\d+",gene_type)
			yfaResult = re.search("MHCY\\d+\w$",gene_type)
			
			ylecResult = re.search("YLEC",gene_type)
			
			#ylbResult = re.search("YLbeta",gene_type)
			ylbResult = re.search("MHCY2B\\d",gene_type)
			
			znfResult = re.search("ZNF",gene_type)
			
			ozfResult = re.search("OZFL",gene_type)
			#ozfResult = re.search("ZNF184L",gene_type)
			
			lengResult = re.search("LENG9",gene_type)
							
			if yfaResult:
				type = "YF"
			elif ylecResult:
				type = "YLec"
			elif ylbResult:
				type = "YLbeta"
			elif ozfResult:
				type = "OZFL"
			elif znfResult:
				#currently, this needs to come after OZF search, if they both start with "ZNF"
				type = "ZNF"
			elif lengResult:
				type = "LENG9"
			else:
				print "Add rule to define type for \""+gene_type+"\""
				sys.exit()				

		
		rRNA_result = re.search("RN",transcript_info)
		pseudogene_result = re.search("\dP$",gene_type)

		if (previous_gene != "") and (previous_gene != gene_type):	
			LOC_count += 1
			locNum = str(LOC_count)
			if(len(locNum) == 1):
				locNum = "0"+locNum
				
			print previous_ID
			#yfaResult = re.search("YF\\d+",previous_gene)
			yfaResult = re.search("MHCY\\d+\w$",previous_gene)
			
			ylecResult = re.search("YLEC",previous_gene)
			
			#ylbResult = re.search("YLbeta",previous_gene)
			ylbResult = re.search("MHCY2B\\d",previous_gene)
			
			znfResult = re.search("ZNF",previous_gene)
			
			ozfResult = re.search("OZFL",previous_gene)
			#ozfResult = re.search("ZNF184L",previous_gene)
			
			lengResult = re.search("LENG9",previous_gene)

			description = ""

			if yfaResult:
				prev_YF +=1
				
				MHCYtype=""
				MHCYtypeResult = re.search("MHCY\\d+(\w)$",previous_gene)
				
				if MHCYtypeResult:
					MHCYtype = MHCYtypeResult.group(1)
					
					if MHCYtype == "":
						print "Issue finding type for :" + previous_gene
						print "Type Error #2"
						sys.exit()				
				else:
					print "Issue finding type for :" + previous_gene
					print "Type Error #1"
					sys.exit()
				
				previous_gene = re.sub("MHCY\d+\w", "MHCY"+str(prev_YF)+MHCYtype, previous_gene)
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "Major Histocompatibility Complex Y (MHCY) class I, Gene "+ str(prev_YF) + ", Type " +MHCYtype
				print "-->ID:"+previous_ID
			elif ylecResult:
				prev_YLec +=1
	
				YLECtype=""
				YLECtypeResult = re.search("YLEC\\d+(\w)$",previous_gene)
				
				if YLECtypeResult:
					YLECtype = "Type "  + YLECtypeResult.group(1)
					
					if YLECtype == "":
						print "Issue finding type for :" + previous_gene
						print "Type Error #2"
						sys.exit()				
				elif previous_gene == "YLEC30partial":
					YLECtype = "Partial Gene"
				else:
					print "Issue finding type for :" + previous_gene
					print "Type Error #1"
					sys.exit()

				previous_gene = re.sub("YLEC\d+", "YLEC"+str(prev_YLec), previous_gene)
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "C-type lectin, candidate NK cell receptor, Gene "+ str(prev_YLec) + ", " +YLECtype
				print "-->ID:"+previous_ID
			elif ylbResult:
				prev_YLBII +=1

				MHCYtype=""
				MHCYtypeResult = re.search("MHCY2B\\d+(\w)$",previous_gene)
				
				if MHCYtypeResult:
					MHCYtype = MHCYtypeResult.group(1)
					
					if MHCYtype == "":
						print "Issue finding type for :" + previous_gene
						print "Type Error #2"
						sys.exit()				
				else:
					print "Issue finding type for :" + previous_gene
					print "Type Error #1"
					sys.exit()

				previous_gene = re.sub("MHCY2B\d+", "MHCY2B"+str(prev_YLBII), previous_gene)
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "Major Histocompatibility Complex Y (MHCY) class II beta chain, Gene "+ str(prev_YLBII) + ", Type " +MHCYtype
				print "-->ID:"+previous_ID
			elif ozfResult:
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "Only Zinc Finger (OZF)-Like, Gene 1"
				print "-->ID:"+previous_ID
			elif znfResult:
				prev_ZNF +=1

				ZNFtype=""
				ZNFtypeResult = re.search("ZNFY\\d+(\w)$",previous_gene)
				
				if ZNFtypeResult:
					ZNFtype = ZNFtypeResult.group(1)
					
					if ZNFtype == "":
						print "Issue finding type for :" + previous_gene
						print "Type Error #2"
						sys.exit()				
				else:
					print "Issue finding type for :" + previous_gene
					print "Type Error #1"
					sys.exit()

				previous_gene = re.sub("ZNFYd+", "ZNFY"+str(prev_ZNF), previous_gene)
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "Zinc finger protein containing a KRAB domain, Gene "+ str(prev_ZNF) + ", Type " +ZNFtype
				print "-->ID:"+previous_ID
			elif lengResult:
				prev_LENG +=1

				LENGtype=""
				LENGtypeResult = re.search("LENG9L\\d+(\w)$",previous_gene)

				if LENGtypeResult:
					LENGtype = LENGtypeResult.group(1)
					
					if LENGtype == "":
						print "Issue finding type for :" + previous_gene
						print "Type Error #2"
						sys.exit()				
				else:
					print "Issue finding type for :" + previous_gene
					print "Type Error #1"
					sys.exit()


				previous_gene = re.sub("LENG9L\d+", "LENG9L"+str(prev_LENG), previous_gene)
				previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
				description = "Leukocyte receptor cluster encoded novel gene (LENG) member 9-Like, Gene "+ str(prev_LENG) + ", Type " +LENGtype
				print "-->ID:"+previous_ID
			else:
				print "Add rule to describe description for \""+gene_type+"\""
				sys.exit()				

			gene_length = len(rna)

			#if pseudogene, need to add "P" back into the annotation type
			pseudo_result = re.search("\dP$",previous_gene)
			if pseudo_result:
				previous_type = previous_type + "P"

				text = ">" + previous_ID + "\n"
				text = text + str(rna) + "\n"
				#print text
				outHandle.write(text)

				if yfaResult:
					description = re.sub(", Type P",", Pseudogene",description)
			else:
				temp_seqObj = Seq(rna)
				prot = temp_seqObj.translate()
							
				partialCheck = re.search("partial",previous_ID)
				startResult = re.search("^M",str(prot))
				anyStop = re.search("\*",str(prot))
				lastStop = re.search("\*$",str(prot))

				if not partialCheck:
					if not startResult:
						print "...The CDS sequence does not begin with a start codon.  Please debug."
						previous_ID = previous_ID + "-ERROR"
						sys.exit()			

					if not lastStop:
						print "...The CDS sequence lacks a stop codon.  Please debug."
						previous_ID = previous_ID + "-ERROR"
						print prot
						print rna
						sys.exit()
					else:
						strProt = str(prot)
						strProt = re.sub("\*$","",strProt)
						anyStop = re.search("\*",strProt)
									
					if anyStop:
						print "...There is a pre-mature stop codon in the CDS sequence.  Please debug."
						previous_ID = previous_ID + "-ERROR"
						print prot + " PROBLEM"
						print rna
						sys.exit()
					else:
						print prot + " OK?"

				text = ">" + previous_ID + "\n"
				text = text + str(rna) + "\n"
				#print text
				outHandle.write(text)

				text = ">" + previous_ID + "\n"
				text = text + str(prot) + "\n"
				#print text
				pepHandle.write(text)

			text = previous_ID + "\tLOC" + locNum + "\t" + previous_type + "\t" + description + "\t" +str(gene_length)+ "\n"
			mapHandle.write(text)		
		
			gene_start = -1
			gene_stop = -1
			gene_strand = ""
			rna = ""
		
		if rRNA_result:
			rec_type="rRNA"
						
			description = ""
			result18=re.search("RN18",gene_type)
			result5=re.search("RN5-8",gene_type)
			result28=re.search("RN28",gene_type)
			if result18:
				LOC_count += 1
				description = "18S rRNA gene, rRNA gene cluster " + str(rRNA_count)
			elif result5:
				description = "5.8S rRNA gene, rRNA gene cluster " + str(rRNA_count)
			elif result28:
				description = "28S rRNA gene, rRNA gene cluster " + str(rRNA_count)
				rRNA_count -= 1
			else:
				print "Modify code to handle rRNA type: " + gene_type
				sys.exit()

			locNum = str(LOC_count)
			if(len(locNum) == 1):
				locNum = "0"+locNum

			start_pos = start_pos-1
			rna = seq[start_pos:stop_pos]			
			#print rna
			#sys.exit()
			
			gene_length =  len(rna)

			print ID
			text = ID + "\tLOC" + locNum + "\t" + rec_type + "\t" + description + "\t" +str(gene_length)+ "\n"
			mapHandle.write(text)
		elif pseudogene_result:
			#pseudogene code
			gene_start=start_pos-1
			gene_stop=stop_pos
			gene_strand=strand
			
			if strand == "+":
				rna = seq[gene_start:gene_stop]
			elif strand == "-":
				rna = Seq(seq[gene_start:gene_stop])
				rna = rna.reverse_complement()
			else:
				print "Need to figure out how to parse strand: " + strand
				print line
				sys.exit()
			
			previous_ID = ID
			previous_gene=gene_type
			previous_type = type
		elif type == "exon":
			#all "exon" values should have been changed to something else
			print "Modify code to parse GTF line: "+ line
			sys.exit()
		else:
			#CDS code
			exon_start=start_pos-1
			exon_stop=stop_pos
			
			if gene_start == -1:
				gene_strand=strand
				
				if gene_strand == "+":
					rna = seq[exon_start:exon_stop]
					
					gene_start=exon_start
					gene_stop=exon_stop
				elif gene_strand == "-":
					rna = Seq(seq[exon_start:exon_stop])
					rna = str(rna.reverse_complement())
				
					#I am not really using this part yet, but might be helpful to keep start keeping track of it for later
					gene_start=exon_stop
					gene_stop=exon_start
				else:
					print "Need to parse strand: " + strand
					print line
					sys.exit()

				#print gene_type + " : starting 1st exon"
				#print rna		
			elif gene_strand == "+":
				#print gene_type + " : extending sequence"
				#print rna + " + " + seq[exon_start:exon_stop]
				rna = rna + seq[exon_start:exon_stop]
				gene_stop=exon_stop
			elif gene_strand == "-":
				temp_seq = Seq(seq[exon_start:exon_stop])
				temp_seq = str(temp_seq.reverse_complement())
				
				##this only works because the exon order differs by strand in this particular GTF (otherwise, you would add to the beginning instead of the end)
				#print gene_type + " : extending sequence"
				#print rna + " + " + temp_seq
				rna = rna +temp_seq
				
				gene_start=exon_stop

			previous_gene=gene_type
			previous_ID = ID
			previous_type = type
	
	line = inHandle.readline()
		
inHandle.close()

#######################################################
### Need to write entry related to last line in GTF ###
#######################################################

LOC_count += 1
locNum = str(LOC_count)
if(len(locNum) == 1):
	locNum = "0"+locNum
			
print previous_ID
#yfaResult = re.search("YF\\d+", previous_gene)
yfaResult = re.search("MHCY\\d+\w$", previous_gene)
			
ylecResult = re.search("YLEC", previous_gene)
			
#ylbResult = re.search("YLbeta", previous_gene)
ylbResult = re.search("MHCY2B\\d", previous_gene)
			
znfResult = re.search("ZNF", previous_gene)
			
ozfResult = re.search("OZFL", previous_gene)
#ozfResult = re.search("ZNF184L", previous_gene)
			
lengResult = re.search("LENG9", previous_gene)


description = ""

if yfaResult:
	prev_YF +=1
				
	MHCYtype=""
	MHCYtypeResult = re.search("MHCY\\d+(\w)$",previous_gene)
				
	if MHCYtypeResult:
		MHCYtype = MHCYtypeResult.group(1)
					
		if MHCYtype == "":
			print "Issue finding type for :" + previous_gene
			print "Type Error #2"
			sys.exit()				
	else:
		print "Issue finding type for :" + previous_gene
		print "Type Error #1"
		sys.exit()
				
	previous_gene = re.sub("MHCY\d+\w", "MHCY"+str(prev_YF)+MHCYtype, previous_gene)
	previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
	description = "Major Histocompatibility Complex Y (MHCY) class I, Gene "+ str(prev_YF) + ", Type " +MHCYtype
	print "-->ID:"+previous_ID
elif ylecResult:
	prev_YLec +=1

	YLECtype=""
	YLECtypeResult = re.search("YLEC\\d+(\w)$",previous_gene)
				
	if YLECtypeResult:
		YLECtype = "Type "  + YLECtypeResult.group(1)
					
		if YLECtype == "":
			print "Issue finding type for :" + previous_gene
			print "Type Error #2"
			sys.exit()				
	elif previous_gene == "YLEC30partial":
		YLECtype = "Partial Gene"
	else:
		print "Issue finding type for :" + previous_gene
		print "Type Error #1"
		sys.exit()
					
	previous_gene = re.sub("YLEC\d+", "YLEC"+str(prev_YLec), previous_gene)
	previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
	description = "C-type lectin, candidate NK cell receptor, Gene "+ str(prev_YLec)+ ", " +YLECtype
	print "-->ID:"+previous_ID
elif ylbResult:
	prev_YLBII +=1

	MHCYtype=""
	MHCYtypeResult = re.search("MHCY2B\\d+(\w)$",previous_gene)
				
	if MHCYtypeResult:
		MHCYtype = MHCYtypeResult.group(1)
					
		if MHCYtype == "":
			print "Issue finding type for :" + previous_gene
			print "Type Error #2"
			sys.exit()				
	else:
		print "Issue finding type for :" + previous_gene
		print "Type Error #1"
		sys.exit()

	previous_gene = re.sub("YLbeta\d+", "YLbeta"+str(prev_YLBII), previous_gene)
	previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
	description = "Major Histocompatibility Complex Y (MHCY) class II beta chain, Gene "+ str(prev_YLBII) + ", Type " +MHCYtype
	print "-->ID:"+previous_ID
elif znfResult:
	prev_ZNF +=1

	ZNFtype=""
	ZNFtypeResult = re.search("ZNFY\\d+(\w)$",previous_gene)
				
	if ZNFtypeResult:
		ZNFtype = ZNFtypeResult.group(1)
					
		if ZNFtype == "":
			print "Issue finding type for :" + previous_gene
			print "Type Error #2"
			sys.exit()				
	else:
		print "Issue finding type for :" + previous_gene
		print "Type Error #1"
		sys.exit()

	previous_gene = re.sub("ZNFY\d+", "ZNFY"+str(prev_ZNF), previous_gene)
	previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
	description = "Zinc finger protein containing a KRAB domain, Gene "+ str(prev_ZNF) + ", Type " +ZNFtype
	print "-->ID:"+previous_ID
elif lengResult:
	prev_LENG +=1
	
	LENGtype=""
	LENGtypeResult = re.search("LENG9L\\d+(\w)$",previous_gene)

	if LENGtypeResult:
		LENGtype = LENGtypeResult.group(1)
					
		if LENGtype == "":
			print "Issue finding type for :" + previous_gene
			print "Type Error #2"
			sys.exit()				
	else:
		print "Issue finding type for :" + previous_gene
		print "Type Error #1"
		sys.exit()


	previous_gene = re.sub("LENG9L\d+", "LENG9L"+str(prev_LENG), previous_gene)
	previous_ID = "RJF."+contig+".LOC" + locNum + "." + previous_gene
	description = "Leukocyte receptor cluster encoded novel gene (LENG) member 9-Like, Gene "+ str(prev_LENG) + ", Type " +LENGtype
	print "-->ID:"+previous_ID
else:
	print "Add rule to describe description for \""+gene_type+"\""
	sys.exit()				

gene_length = len(rna)

#if pseudogene, need to add "P" back into the annotation type
pseudo_result = re.search("\dP$",previous_gene)
if pseudo_result:
	previous_type = previous_type + "P"

	text = ">" + previous_ID + "\n"
	text = text + str(rna) + "\n"
	#print text
	outHandle.write(text)
	
	if yfaResult:
		description = re.sub(", Type P",", Pseudogene",description)
else:
	temp_seqObj = Seq(rna)
	prot = temp_seqObj.translate()
						
	anyStop = re.search("\*",str(prot))
	lastStop = re.search("\*$",str(prot))

	if not lastStop:
		print "...The CDS sequence lacks a stop codon.  Please debug."
		previous_ID = previous_ID + "-ERROR"
		sys.exit()
	else:
		strProt = str(prot)
		strProt = re.sub("\*$","",strProt)
		anyStop = re.search("\*",strProt)
					
	if anyStop:
		print "...There is a pre-mature stop codon in the CDS sequence.  Please debug."
		previous_ID = previous_ID + "-ERROR"
		sys.exit()
	else:
		print prot + " OK?"

		text = ">" + previous_ID + "\n"
		text = text + str(rna) + "\n"
		#print text
		outHandle.write(text)

		text = ">" + previous_ID + "\n"
		text = text + str(prot) + "\n"
		#print text
		pepHandle.write(text)

text = previous_ID + "\tLOC" + locNum + "\t" + previous_type + "\t" + description +"\t" + str(gene_length) +  "\n"
mapHandle.write(text)

outHandle.close()
pepHandle.close()
mapHandle.close()
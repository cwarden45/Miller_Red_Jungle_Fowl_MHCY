import os
import re
import sys

GTF="Contig1_updated_genes.gtf"
STARaln_folder="../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/STAR-param9/Separate_Alignments"
SJout="Contig1_splice_junctions-STAR-full_table-v3-param9.txt"
SJoutU="Contig1_splice_junctions-STAR-full_table-unique-v3-param9.txt"
SJoutM="Contig1_splice_junctions-STAR-full_table-multimap-v3-param9.txt"
SJoutUcpm="Contig1_splice_junctions-STAR-full_table-unique_CPM-v3-param9.txt"
SJoutTcpm="Contig1_splice_junctions-STAR-full_table-total_CPM-v3-param9.txt"

#GTF="Contig2_updated_genes.gtf"
#STARaln_folder="../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/STAR-param9/Separate_Alignments"
#SJout="Contig2_splice_junctions-STAR-full_table-v3-param9.txt"
#SJoutU="Contig2_splice_junctions-STAR-full_table-unique-v3-param9.txt"
#SJoutM="Contig2_splice_junctions-STAR-full_table-multimap-v3-param9.txt"
#SJoutUcpm="Contig2_splice_junctions-STAR-full_table-unique_CPM-v3-param9.txt"
#SJoutTcpm="Contig2_splice_junctions-STAR-full_table-total_CPM-v3-param9.txt"

#GTF="Contig3_updated_genes.gtf"
#STARaln_folder="../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/STAR-param9/Separate_Alignments"
#SJout="Contig3_splice_junctions-STAR-full_table-v3-param9.txt"
#SJoutU="Contig3_splice_junctions-STAR-full_table-unique-v3-param9.txt"
#SJoutM="Contig3_splice_junctions-STAR-full_table-multimap-v3-param9.txt"
#SJoutUcpm="Contig3_splice_junctions-STAR-full_table-unique_CPM-v3-param9.txt"
#SJoutTcpm="Contig3_splice_junctions-STAR-full_table-total_CPM-v3-param9.txt"

#GTF="Contig4_updated_genes.gtf"
#STARaln_folder="../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/STAR-param9/Separate_Alignments"
#SJout="Contig4_splice_junctions-STAR-full_table-v3-param9.txt"
#SJoutU="Contig4_splice_junctions-STAR-full_table-unique-v3-param9.txt"
#SJoutM="Contig4_splice_junctions-STAR-full_table-multimap-v3-param9.txt"
#SJoutUcpm="Contig4_splice_junctions-STAR-full_table-unique_CPM-v3-param9.txt"
#SJoutTcpm="Contig4_splice_junctions-STAR-full_table-total_CPM-v3-param9.txt"

alignment_stats = "STAR_read_stats-param9.txt"

#define all gene introns
junctionHash = {}
countHash = {}
countHashU = {}
countHashM = {}
countHashUcpm = {}
countHashTcpm = {}
alignedUniqueHash = {}
alignedTotalHash = {}

SJcount = 0
previous_gene = ""
previous_begin = -1
previous_end = -1

inHandle = open(GTF)
line = inHandle.readline()

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	
	exon_seq = lineInfo[0]
	exon_start = int(lineInfo[3])
	exon_stop = int(lineInfo[4])
	exon_strand = lineInfo[6]
	gene_info = lineInfo[8]
	
	if previous_gene == gene_info:
		SJcount += 1
		
		if exon_strand == "+":
			SJpos = exon_seq+"\t"+str(previous_end+1)+"\t"+str(exon_start-1)+"\t"+exon_strand
		elif exon_strand == "-":
			SJpos = exon_seq+"\t"+str(exon_stop+1)+"\t"+str(previous_begin-1)+"\t"+exon_strand
		else:
			print "Define mapping for strand: " + exon_strand
			sys.exit()
		geneResult = re.search("gene_name \"(\S+)\"; transcript_id",gene_info)
		
		if geneResult:
			gene = geneResult.group(1)
			SJcount_text = "000"
			if SJcount >= 100:
				SJcount_text = str(SJcount)
			elif SJcount >= 10:
				SJcount_text = "0"+str(SJcount)
			else:
				SJcount_text = "00"+str(SJcount)
			junctionHash[SJpos]=exon_seq+"_"+SJcount_text
			countHash[SJpos]=gene
			countHashU[SJpos]=gene
			countHashM[SJpos]=gene
			countHashUcpm[SJpos]=gene
			countHashTcpm[SJpos]=gene
		else:
			print "Issue parsing gene name: " + gene_info
			sys.exit()
	
	previous_gene=gene_info
	previous_begin=exon_start
	previous_end=exon_stop
	
	line = inHandle.readline()

inHandle.close()

#look for counts
output_header = "GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene"

fileResults = os.listdir(STARaln_folder)

for file in fileResults:
	result = re.search("^SRR\d+.bam$",file)
	fullPath = os.path.join(STARaln_folder, file)
	
	if result:
		sample = re.sub(".bam$","",file)
		print sample

		output_header = output_header + "\t" + sample

		#aligned read count
		log_file = STARaln_folder + "/" + sample + "/" + sample + "_Log.final.out"
		
		unique_aligned = 0
		multimap_aligned = 0

		inHandle = open(log_file)
		line = inHandle.readline()

		while line:
			line = re.sub("\n","",line)
			line = re.sub("\r","",line)

			uniqueResult = re.search("Uniquely mapped reads number \|\t(\d+)",line)
			multimapResult = re.search("Number of reads mapped to multiple loci \|\t(\d+)",line)
			
			if uniqueResult:
				unique_aligned = int(uniqueResult.group(1))

			if multimapResult:
				multimap_aligned = int(multimapResult.group(1))
			
			line = inHandle.readline()

		inHandle.close()
		
		total_aligned = unique_aligned + multimap_aligned
		print total_aligned

		alignedUniqueHash[sample]=unique_aligned
		alignedTotalHash[sample]=total_aligned
		
		unique_million = unique_aligned / 1000000
		total_million = total_aligned / 1000000
		
		#splice junction file
		recoveredHash = {}
		SJfile = STARaln_folder + "/" + sample + "/" + sample + "_SJ.out.tab"

		inHandle = open(SJfile)
		line = inHandle.readline()

		while line:
			line = re.sub("\n","",line)
			line = re.sub("\r","",line)
			lineInfo = line.split("\t")
			
			chr = lineInfo[0]
			intron_start = lineInfo[1]
			intron_stop = lineInfo[2]
			strand = lineInfo[3]
			spliceType = lineInfo[4]
			annotationStatus = lineInfo[5]
			uniqueCount = lineInfo[6]
			multimapCount = lineInfo[7]
			overhang = lineInfo[8]

			uniqueCPM = float(int(uniqueCount)) / unique_million
			totalCPM = float(int(uniqueCount) + int(multimapCount)) / total_million

			if strand == "1":
				strand = "+"
			elif strand == "2":
				strand = "-"
			else:
				strand = "."
				
			SJpos = chr+"\t"+intron_start+"\t"+intron_stop+"\t"+strand
				
			if SJpos in countHash:
				if (spliceType == "1") and (strand == "+"):
					countHash[SJpos]=countHash[SJpos] + "\t(" + uniqueCount + " u : " + multimapCount + " m)"
					countHashU[SJpos]=countHashU[SJpos] + "\t" + uniqueCount
					countHashM[SJpos]=countHashM[SJpos] + "\t" + multimapCount
					
					countHashUcpm[SJpos]=countHashUcpm[SJpos] + "\t" + '{0:.3g}'.format(uniqueCPM)
					countHashTcpm[SJpos]=countHashTcpm[SJpos] + "\t" + '{0:.3g}'.format(totalCPM)
				elif (spliceType == "2") and (strand == "-"):
					countHash[SJpos]=countHash[SJpos] + "\t(" + uniqueCount + " u : " + multimapCount + " m)"
					countHashU[SJpos]=countHashU[SJpos] + "\t" + uniqueCount
					countHashM[SJpos]=countHashM[SJpos] + "\t" + multimapCount

					countHashUcpm[SJpos]=countHashUcpm[SJpos] + "\t" + '{0:.3g}'.format(uniqueCPM)
					countHashTcpm[SJpos]=countHashTcpm[SJpos] + "\t" + '{0:.3g}'.format(totalCPM)
				else:
					countHash[SJpos]=countHash[SJpos] + "\t(Splice Type" + spliceType + ")"
					countHashU[SJpos]=countHashU[SJpos] + "\t(Splice Type" + spliceType + ")"
					countHashM[SJpos]=countHashM[SJpos] + "\t(Splice Type" + spliceType + ")"
					countHashUcpm[SJpos]=countHashUcpm[SJpos] + "\t(Splice Type" + spliceType + ")"
					countHashTcpm[SJpos]=countHashTcpm[SJpos] + "\t(Splice Type" + spliceType + ")"
					
				recoveredHash[SJpos]=1
			
			line = inHandle.readline()

		inHandle.close()
		
		for SJpos in junctionHash.keys():
			if SJpos not in recoveredHash:
				countHash[SJpos]=countHash[SJpos] + "\t(No Support?)"
				countHashU[SJpos]=countHashU[SJpos] + "\t0"
				countHashM[SJpos]=countHashM[SJpos] + "\t0"

				countHashUcpm[SJpos]=countHashUcpm[SJpos] + "\t0"
				countHashTcpm[SJpos]=countHashTcpm[SJpos] + "\t0"
output_header = output_header + "\n"

#output alignment table
outHandle = open(alignment_stats, "w")
statHeader = "Sample\tUnique.Aligned.Reads\tMultimap.Aligned.Reads\tTotal.Aligned.Reads\n"
outHandle.write(statHeader)

headerArr = re.sub("\n","",output_header).split("\t")
print headerArr

for i in xrange(6,len(headerArr)):
	sample = headerArr[i]
	print sample
	total_count = alignedTotalHash[sample]
	unique_count = alignedUniqueHash[sample]
	multimap_count = total_count - unique_count
	
	text = sample + "\t" + str(unique_count)+ "\t" + str(multimap_count)+ "\t" + str(total_count) + "\n"
	outHandle.write(text)

outHandle.close()

#output splice junction files

outHandle = open(SJout, "w")
outHandle.write(output_header)

outHandleU = open(SJoutU, "w")
outHandleU.write(output_header)

outHandleM = open(SJoutM, "w")
outHandleM.write(output_header)

outHandleUcpm = open(SJoutUcpm, "w")
outHandleUcpm.write(output_header)

outHandleTcpm = open(SJoutTcpm, "w")
outHandleTcpm.write(output_header)


for SJpos in junctionHash.keys():
	SJindex = junctionHash[SJpos]
	SJcountText = countHash[SJpos]
	SJcountTextU = countHashU[SJpos]
	SJcountTextM = countHashM[SJpos]
	SJcountTextUcpm = countHashUcpm[SJpos]
	SJcountTextTcpm = countHashTcpm[SJpos]
	
	text = SJindex + "\t"+SJpos+"\t"+SJcountText+"\n"
	outHandle.write(text)
	
	text = SJindex + "\t"+SJpos+"\t"+SJcountTextU+"\n"
	outHandleU.write(text)
	
	text = SJindex + "\t"+SJpos+"\t"+SJcountTextM+"\n"
	outHandleM.write(text)
	
	text = SJindex + "\t"+SJpos+"\t"+SJcountTextUcpm+"\n"
	outHandleUcpm.write(text)
	
	text = SJindex + "\t"+SJpos+"\t"+SJcountTextTcpm+"\n"
	outHandleTcpm.write(text)
	
	
outHandle.close()
outHandleU.close()
outHandleM.close()
outHandleUcpm.close()
outHandleTcpm.close()

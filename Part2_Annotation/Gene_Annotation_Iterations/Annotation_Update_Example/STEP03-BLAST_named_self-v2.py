import os
import sys
import re

contigs = ("Contig1","Contig2","Contig3","Contig4")

for contigQ in contigs:
	print contigQ
	
	contigQ_FA = contigQ+"_gene_named.fa"
	
	for contigR in contigs:
		#allow creation of self-BLAST file
		print "-->" + contigR
		contigR_FA = contigR+"_gene_named.fa"
			
		if not(os.path.exists(contigR_FA+".nhr")):
			command = "makeblastdb -in " + contigR_FA + " -dbtype nucl"
			os.system(command)

		result = contigQ+"_"+contigR+"_BLAST_result.txt"
		result = re.sub("../update_gene_names_171220/","",result)
		result = re.sub("../update_gene_names_190318/","",result)
		result = re.sub("../update_gene_names_190711/","",result)
		#test kit(?) using multiple hits
		command = "blastn -evalue 1e-20 -query " +contigQ_FA + " -db " + contigR_FA + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
		#command = "blastn -evalue 1e-20 -num_alignments 1 -query " +contigQ_FA + " -db " + contigR_FA + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
		os.system(command)
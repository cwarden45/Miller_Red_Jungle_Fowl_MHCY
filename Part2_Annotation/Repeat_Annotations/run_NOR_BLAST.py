import os

seqID = "Contig1"

norDir = "NOR/"
command = "mkdir " + norDir
os.system(command)

inFA = "../"+seqID+".fasta"
blastDB = seqID
command = "makeblastdb -in " + inFA + " -dbtype nucl -out " + blastDB
os.system(command)

provided_seq = "rRNA_cluster.fasta"
result = norDir + seqID+"_rRNA_cluster_BLAST_result.txt"
command = "blastn -query " +provided_seq + " -db " + blastDB + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

provided_seq = "rRNA.fa"
result = norDir + seqID+"_rRNA_BLAST_result.txt"
command = "blastn -query " +provided_seq + " -db " + blastDB + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

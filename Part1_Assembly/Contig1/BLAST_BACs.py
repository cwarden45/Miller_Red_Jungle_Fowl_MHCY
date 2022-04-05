import sys
import re
import os

input = "separate_sequences-Contig1-220203.fasta"
ref = "Contig1-10changes_220204.fa"
output1 = "Contig1_10changes-BLAST_clones.txt"
output2 = "Contig1_10changes-BLAST_clones-ALT.txt"


command = "makeblastdb -in " + ref + " -dbtype nucl"
os.system(command)

command = "blastn -perc_identity 95 -evalue 1e-20 -query " +input + " -db " + ref + " -out " + output1 + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

command = "blastn  -penalty -2 -ungapped -perc_identity 95 -evalue 1e-20 -query " +input + " -db " + ref + " -out " + output2 + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

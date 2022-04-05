import sys
import re
import os

input = "HGAP3_19d16_portion2-BLAST_CLUSTER--extra_6bp.fa"
ref = "HGAP3_19d16_portion1-extra_6bp.fa"
output = "BLAST_overlap-extra_12bp.txt"

command = "makeblastdb -in " + ref + " -dbtype nucl"
os.system(command)

command = "blastn  -penalty -2 -ungapped -perc_identity 95 -evalue 1e-20 -query " +input + " -db " + ref + " -out " + output + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

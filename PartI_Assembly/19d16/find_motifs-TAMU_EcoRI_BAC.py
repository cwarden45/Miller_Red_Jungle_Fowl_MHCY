import sys
import re
import os

input = "TAMU_EcoRI_BAC.fa"
ref = "../../SMRT_Portal_Files/19d16_016471_revcom.fa"
output = "HGAP3-19d16_TAMU_locations.txt"

command = "makeblastdb -in " + ref + " -dbtype nucl"
os.system(command)

command = "blastn -perc_identity 85 -evalue 1e-20 -query " +input + " -db " + ref + " -out " + output + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

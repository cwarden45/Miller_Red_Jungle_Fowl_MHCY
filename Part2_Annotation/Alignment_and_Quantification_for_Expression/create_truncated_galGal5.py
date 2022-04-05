import sys
import re
import os
from Bio import SeqIO

ref = "../../../../../galGal5_Indices/galGal5.fa"
output = "truncated_galGal5.fa"
	
outHandle = open(output,"w")

skippedCount = 0
	
fasta_parser = SeqIO.parse(ref, "fasta")
for fasta in fasta_parser:
	chr_name = fasta.id
	
	nonCanonicalResult = re.search("_",chr_name)
	
	if nonCanonicalResult:
		#print "Skipping " + chr_name
		skippedCount += 1
	elif chr_name == "chr16":
		seq = str(fasta.seq)
		diffRegion = seq[0:350000]
		print "adding first " + str(len(diffRegion)) + " bp of " + chr_name
		text = ">"+chr_name+"\n" + diffRegion + "\n"
		outHandle.write(text)
	else:
		print "adding " + chr_name
		seq = str(fasta.seq)
		text = ">"+chr_name+"\n" + seq + "\n"
		outHandle.write(text)
		
print "Skipped " + str(skippedCount) + " supplemental chromosomes"

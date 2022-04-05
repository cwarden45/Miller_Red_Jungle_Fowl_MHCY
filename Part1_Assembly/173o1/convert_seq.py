import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

#wording is a bit confusing because of how the script was originally run for 19d16

id="173o1"
faSeq = "../../revise_Canu_v2_1/Canu-v2.1-Arrow_173o1-rearranged-from_expectedBAC/arrow_var.fasta"
outFa = "173o1-1change_201118.fa"
pos = 31505-1
replaced = "T"
original = "TC"

#id="173o1"
#faSeq = "173o1-1change_201118.fa"
#outFa = "173o1-2change_201118.fa"
#pos = 45669-1+1
#replaced = "C"
#original = "CG"

#id="173o1"
#faSeq = "173o1-2change_201118.fa"
#outFa = "173o1-3change_201118.fa"
#pos = 124293-1+1+1
#replaced = "C"
#original = "CG"


outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	modSeq = ""
	if len(replaced) != 0:
		start = pos
		stop = pos+len(replaced)
		modSeq = refSeq[start:stop]
		modSeq = modSeq.upper()
		
		if modSeq != replaced:
			print "Check code:"
			print "Expected = " + replaced
			print "Observed = " + modSeq
			sys.exit()
		
	seq1start = 0#needs to be 0, not 1
	seq1stop = pos
	seq2start = pos+len(modSeq)
	seq2stop = len(refSeq)
	
	newSeq = refSeq[seq1start:seq1stop] + original + refSeq[seq2start:seq2stop]
	
	text=">" + id + "\n" + newSeq + "\n"
	
	outHandle.write(text)
	
outHandle.close()
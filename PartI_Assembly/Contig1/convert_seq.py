import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

#wording is a bit confusing because of how the script was originally run for 19d16

id="Contig1"
faSeq = "../Contig1_draft_201118b/Contig1-9changes_201118.fa"
outFa = "Contig1-10changes_220204.fa"
pos = 339990-1
replaced = "A"
original = "AAAGGG"


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
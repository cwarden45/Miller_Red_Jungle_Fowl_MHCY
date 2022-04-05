import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

#wording is a bit confusing because of how the script was originally run for 19d16

id="Contig1"
faSeq = "../Contig1_draft_201118b/Contig1-9changes_201118.fa"
expectedChange = "confirm-10CHANGE-339990.txt"
pos = 339990-1
replaced = "A"
original = "AAAGGG"
flank = 15

outHandle = open(expectedChange, "w")

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
		
	flankUpStart = pos-flank
	flankUpStop = pos
	flankDownStart = pos+len(modSeq)
	flankDownStop = pos+len(modSeq) + flank
	
	text = "***Starting***\n\n"
	text = text + refSeq[flankUpStart:flankUpStop] + " + " + modSeq + " + " + refSeq[flankDownStart:flankDownStop]
	
	text = text + "\n\n***Check***\n\n"
	text = text + refSeq[flankUpStart:flankDownStop]
		
	text = text + "\n\n***Altered***\n"
	text = text + refSeq[flankUpStart:flankUpStop] + " + " + original + " + " + refSeq[flankDownStart:flankDownStop]
	
	outHandle.write(text)
	
outHandle.close()
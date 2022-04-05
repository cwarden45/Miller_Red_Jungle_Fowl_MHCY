import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id="58f18_trimmed"
faSeq = "../HGAP3_Comparison/Contig2_earlier.fa"
outFa = "58f18_HGAP_trimmed-TEST.fa"
start = 28292-6
stop = 176760

outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
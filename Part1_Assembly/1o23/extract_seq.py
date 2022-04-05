import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id="1o23"
faSeq = "../../Quiver_Polishing/BAC_1o23_LENGTH_FILTERED_subreads_10k_v2.1/arrow_var.fasta"
outFa = "Canu-v2.1-Arrow_1o23-trimmed_extra-12-bp_expectedBAC.fa"
start = 12127-6
stop = 90110+5

outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
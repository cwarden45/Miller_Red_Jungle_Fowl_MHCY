import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

#id="portion1"
#faSeq = "../../Quiver_Polishing/BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k_v1_5/arrow_var.fasta"
#outFa = "Canu-v1.5-Arrow_190M_portion1trim-extra_6bp-simplified.fa"
#start = 0 +10383
#stop = 111290+5

id="portion2"
faSeq = "../../Quiver_Polishing/BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k_v1_5/arrow_var.fasta"
outFa = "Canu-v1.5-Arrow_190M_portion2trim-extra_6bp-simplified.fa"
start = 121974-6
stop = 121974-6+152495-1

outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
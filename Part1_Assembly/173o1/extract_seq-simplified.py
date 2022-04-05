import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id="portion1"
faSeq = "../../Quiver_Polishing/BAC_173o19_LENGTH_FILTERED_subreads_10k_v2_1/arrow_var.fasta"
outFa = "Canu-v2.1-Arrow_173o1_portion1-ALTexpected_trim-simplified.fa"
start = 1
stop = 153749

#id="portion2"
#faSeq = "../../Quiver_Polishing/BAC_173o19_LENGTH_FILTERED_subreads_10k_v2_1/arrow_var.fasta"
#outFa = "Canu-v2.1-Arrow_173o1_portion2-ALTexpected_trim-simplified.fa"
#start = 164428-6
#stop = 164428-6+67649-1


outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
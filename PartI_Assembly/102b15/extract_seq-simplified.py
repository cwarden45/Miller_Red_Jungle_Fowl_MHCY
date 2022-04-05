import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

#id="portion1"
#faSeq = "../../Quiver_Polishing/BAC_102b15_LENGTH_FILTERED_subreads_v1_5/arrow_var.fasta"
#outFa = "Canu-v1.5-Arrow_102b15_portion1-extra_6bp-expectedBAC.fa"
#start = 0 #should not be 1
#stop = 62992+5

id="portion2"
faSeq = "../../Quiver_Polishing/BAC_102b15_LENGTH_FILTERED_subreads_v1_5/arrow_var.fasta"
outFa = "Canu-v1.5-Arrow_102b15_portion2-simplified.fa"
start = 73675-6
stop = 73675-6+39140 #39140 comes from analysis that confirms and reduces the 100% overlapping sequence; this code was confirmed to verify that the same sequence is created in fewer commands.

outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
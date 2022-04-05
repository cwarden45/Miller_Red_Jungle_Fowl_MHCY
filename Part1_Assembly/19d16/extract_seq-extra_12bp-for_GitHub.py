import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id="portion1"
faSeq = "../../SMRT_Portal_Files/19d16_016471_revcom.fa"
outFa = "HGAP3_19d16_portion1-extra_6bp.fa"
start = 0
stop = 37062+5 #37062 is the start of the BAC backbone BLAST hit

#id="portion2"
#faSeq = "../../SMRT_Portal_Files/19d16_016471_revcom.fa"
#outFa = "HGAP3_19d16_portion2-BLAST_CLUSTER--extra_6bp.fa"
#start = 44574-6 #44574 is the end of the BAC backbone BLAST hit
#stop = 193267

## To improve communication in the public code, skip code steps to confirm I have define the correct overlapping position

##remove portion before overlap
#id="portion1"
#faSeq = "HGAP3_19d16_portion1-extra_6bp.fa"
#outFa = "HGAP3_19d16_portion1-extra_6bp_trim.fa"
#start = 22416
#stop = 37067

##remove overlap + portion after overlap
#id="portion2"
#faSeq = "HGAP3_19d16_portion2-BLAST_CLUSTER--extra_6bp.fa"
#outFa = "HGAP3_19d16_portion2-BLAST_CLUSTER--extra_6bp_trim.fa"
#start = 0 # should not have been 1
#stop = 144232-1

outHandle = open(outFa, "w")

fasta_parser = SeqIO.parse(faSeq, "fasta")

for fasta in fasta_parser:
	refSeq = str(fasta.seq)
	conservedSeq = refSeq[start:stop]
	
	text = ">"+id+"\n" + conservedSeq + "\n"
	outHandle.write(text)
import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq


id = "190M"
seq1 = "Canu-v1.5-Arrow_190M_portion2trim-extra_6bp-simplified.fa"
seq2 = "Canu-v1.5-Arrow_190M_portion1trim-extra_6bp-simplified.fa"
new_seq = "Canu-v1.5-Arrow_190M-rearranged-extra_12bp-expectedBAC-simplified.fa"


outHandle = open(new_seq, "w")

seq=""

#seq1
fasta_parser = SeqIO.parse(seq1, "fasta")

for fasta in fasta_parser:
	seq = seq +  str(fasta.seq)

#seq2
fasta_parser = SeqIO.parse(seq2, "fasta")

for fasta in fasta_parser:
	seq = seq +  str(fasta.seq)

#write combined seq
text = ">" + id + "\n" + seq + "\n"
outHandle.write(text)

outHandle.close()
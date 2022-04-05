import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id = "102b15"
seq1 = "Canu-v1.5-Arrow_102b15_portion2-simplified.fa"
seq2 = "Canu-v1.5-Arrow_102b15_portion1-extra_6bp-expectedBAC.fa"
new_seq = "Canu-v1.5-Arrow_102b15-rearranged-expectedBAC--extra_12bp-simplified.fa"

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
import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id = "173o1"
seq1 = "Canu-v2.1-Arrow_173o1_portion2-ALTexpected_trim-simplified.fa"
seq2 = "Canu-v2.1-Arrow_173o1_portion1-ALTexpected_trim-simplified.fa"
new_seq = "Canu-v2.1-Arrow_173o1-rearranged-from_expectedBAC-simplified.fa"

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
import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq

id = "19d16"
seq1 = "HGAP3_19d16_portion2-BLAST_CLUSTER--extra_6bp_trim.fa"
seq2 = "HGAP3_19d16_portion1-extra_6bp_trim.fa"
new_seq = "HGAP3_19d16-rearranged.fa"

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
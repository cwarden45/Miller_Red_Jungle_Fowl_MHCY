import sys
import re
from Bio import AlignIO

aln = "seq_check-IMGT_GenBank.aln"
fasta = "IMGT_GenBank-alpha1alpha2.fasta"
start_index = 72
end_index = 620

outHandle = open(fasta,"w")

alignment = AlignIO.read(open(aln), "clustal")
for record in alignment:
	text = ">" + record.id + "\n" + str(record.seq)[start_index:end_index] + "\n"
	outHandle.write(text)
	
outHandle.close()
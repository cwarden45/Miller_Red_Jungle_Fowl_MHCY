import os
import re
import sys
from Bio import SeqIO
from Bio import Seq

genbank_in = "AF218783.1.gb"
fasta_out = "AF218783.1-CDS.fasta"

genbank_parser = SeqIO.read(genbank_in , "genbank")

outHandle = open(fasta_out, "w")

#based upon code from  http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec13
for feature in genbank_parser.features:
	if feature.type == "CDS":
		#print feature.location
		text = ">" + str(genbank_parser.id) + "_CDS\n"+str(feature.extract(genbank_parser.seq))+"\n"
		outHandle.write(text)
	
outHandle.close()
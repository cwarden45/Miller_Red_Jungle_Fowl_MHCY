import os
import re
import sys
from Bio import SeqIO
from Bio import Seq

genbank_in = "AJ555412.1.gb"
fasta_out = "AJ555412.1-CDS.fasta"

#genbank_in = "AJ278305.2.gb"
#fasta_out = "AJ278305.2-CDS.fasta"

#genbank_in = "HG794391.1.gb"
#fasta_out = "HG794391.1-CDS.fasta"

#genbank_in = "HG794379.1.gb"
#fasta_out = "HG794379.1-CDS.fasta"

#genbank_in = "HG794380.1.gb"
#fasta_out = "HG794380.1-CDS.fasta"

#genbank_in = "HG794395.1.gb"
#fasta_out = "HG794395.1-CDS.fasta"

#genbank_in = "LN999852.1.gb"
#fasta_out = "LN999852.1-CDS.fasta"

#genbank_in = "EU445478.2.gb"
#fasta_out = "EU445478.2-CDS.fasta"

#genbank_in = "HG794386.1.gb"
#fasta_out = "HG794386.1-CDS.fasta"

#genbank_in = "HG965151.1.gb"
#fasta_out = "HG965151.1-CDS.fasta"

#genbank_in = "HM484300.1.gb"
#fasta_out = "HM484300.1-CDS.fasta"

#genbank_in = "HG794368.1.gb"
#fasta_out = "HG794368.1-CDS.fasta"

#genbank_in = "HG794370.1.gb"
#fasta_out = "HG794370.1-CDS.fasta"

#genbank_in = "LN877310.2.gb"
#fasta_out = "LN877310.2-CDS.fasta"

#genbank_in = "AJ420239.1.gb"
#fasta_out = "AJ420239.1-CDS.fasta"

#genbank_in = "AJ310358.1.gb"
#fasta_out = "AJ310358.1-CDS.fasta"

#genbank_in = "AJ420241.2.gb"
#fasta_out = "AJ420241.2-CDS.fasta"

genbank_parser = SeqIO.read(genbank_in , "genbank")

outHandle = open(fasta_out, "w")

#based upon code from  http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec13
for feature in genbank_parser.features:
	if feature.type == "CDS":
		#print feature.location
		text = ">" + str(genbank_parser.id) + "_CDS\n"+str(feature.extract(genbank_parser.seq))+"\n"
		outHandle.write(text)
	
outHandle.close()
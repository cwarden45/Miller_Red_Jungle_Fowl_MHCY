import sys
import re
import os
from Bio import SeqIO

minLength = 10000
subsample_num=1
inputFQ = "/path/to/BAC_1o23_subreads.fq"
outputFQ = "BAC_1o23_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/BAC_102b15_subreads.fq"
#outputFQ = "BAC_102b15_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/160505_B2_58f18_subreads.fq"
#outputFQ = "BAC_160505_B2_190M_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/BAC_173o19_subreads.fq"
#outputFQ = "BAC_173o19_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/BAC_19d16_subreads.fq"
#outputFQ = "BAC_19d16_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/BAC_34j16_subreads.fq"
#outputFQ = "BAC_34j16_LENGTH_FILTERED_subreads_10k.fq"

###The separate 58f18 reads were *combined* after length filtering the separate libaries.  There was a label swap, but the _LENGTH_FILTERED_ .fq files have the correct sample name.
#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/160505_A02_190M_subreads.fq"
#outputFQ = "BAC_160505_A02_58f18_LENGTH_FILTERED_subreads_10k.fq"

#minLength = 10000
#subsample_num=1
#inputFQ = "/path/to/160505_E02_190M_subreads.fq"
#outputFQ = "BAC_160505_E02_58f18_LENGTH_FILTERED_subreads_10k.fq"



outHandle = open(outputFQ, "w")

readCount =0
passCount = 0

fastq_parser = SeqIO.parse(inputFQ, "fastq")
for fastq in fastq_parser:
	readID = fastq.id
	
	readCount += 1
	
	if (readCount % subsample_num == 0):
		readSeq = str(fastq.seq)
		
		if len(readSeq) > minLength:			
			text = fastq.format("fastq")
			outHandle.write(text)
			
			passCount += 1
					
outHandle.close()

print str(passCount) + " subsampled reads greater than " +str(minLength) + " bp"
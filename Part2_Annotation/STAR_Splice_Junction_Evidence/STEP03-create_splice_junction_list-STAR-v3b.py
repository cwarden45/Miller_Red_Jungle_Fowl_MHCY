import os
import re
import sys

SJtable="combined_splice_junctions-STAR-v3_RAW-param9.txt"
SJlist1="combined_splice_junctions-STAR-v3_min1-param9.txt"
SJlist10="combined_splice_junctions-STAR-v3_min10-param9.txt"
SJlist100="combined_splice_junctions-STAR-v3_min100-param9.txt"
SJlist1U="combined_splice_junctions-STAR-v3_min1-UNIQUE-param9.txt"
SJlist10U="combined_splice_junctions-STAR-v3_min10-UNIQUE-param9.txt"
SJlist100U="combined_splice_junctions-STAR-v3_min100-UNIQUE-param9.txt"

outHandle1 = open(SJlist1, "w")
outHandle1.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

outHandle10 = open(SJlist10, "w")
outHandle10.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

outHandle100 = open(SJlist100, "w")
outHandle100.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

outHandle1U = open(SJlist1U, "w")
outHandle1U.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

outHandle10U = open(SJlist10U, "w")
outHandle10U.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

outHandle100U = open(SJlist100U, "w")
outHandle100U.write("GTFindex\tSJ.Chr\tSJ.Start\tSJ.Stop\tSJ.Strand\tGene\tSampleCount\n")

inHandle = open(SJtable)
line = inHandle.readline()

line_count = 0

while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	
	line_count += 1
	
	if line_count > 1:	
		index = lineInfo[0]
		chr = lineInfo[1]
		start = lineInfo[2]
		stop = lineInfo[3]
		strand = lineInfo[4]
		gene = lineInfo[5]
		
		sj_info = index+"\t" + chr + "\t" + start + "\t" + stop + "\t" + strand + "\t" + gene
		
		count1 = 0
		count10 = 0
		count100 = 0
		
		count1U = 0
		count10U = 0
		count100U = 0
		
		for i in xrange(6,len(lineInfo)):			
			countResult = re.search("\((\d+) u : (\d+) m\)", lineInfo[i])
			
			if countResult:
				uniqueCount = int(countResult.group(1))
				multimapCount = int(countResult.group(2))
				
				total = uniqueCount + multimapCount
				
				#print lineInfo[i] + " : " + str(uniqueCount) + " + "  + str(multimapCount) + " = " + str(total)
				
				if total >= 1:
					count1 += 1
				if total >= 10:
					count10 += 1
				if total >= 100:
					count100 += 1
					
				if uniqueCount >= 1:
					count1U += 1
				if uniqueCount >= 10:
					count10U += 1
				if uniqueCount >= 100:
					count100U += 1
			elif (lineInfo[i] != "(No Support?)"):
				print "Decide what to do with STAR SJ count result: " + lineInfo[i]
				sys.exit()

		text = sj_info + "\t" + str(count1) + "\n"
		outHandle1.write(text)

		text = sj_info + "\t" + str(count10) + "\n"
		outHandle10.write(text)
		
		text = sj_info + "\t" + str(count100) + "\n"
		outHandle100.write(text)

		text = sj_info + "\t" + str(count1U) + "\n"
		outHandle1U.write(text)

		text = sj_info + "\t" + str(count10U) + "\n"
		outHandle10U.write(text)			

		text = sj_info + "\t" + str(count100U) + "\n"
		outHandle100U.write(text)
	
	line = inHandle.readline()

inHandle.close()
	
outHandle1.close()
outHandle10.close()

outHandle1U.close()
outHandle10U.close()
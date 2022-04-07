import os
import sys
import re

contig="Contig1"
shift = 0 #this can be a somewhat complicated process to manually inspect and decide what works best for most annotations (including the start of the pileup alignment as well as any soft clipping in the BWA-MEM alignment).  However, with only a 5 bp difference, the transfer is relatively straightforward.
GTFin = "../../Contig1-EARLIER/Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene.gtf"
GTFout = "../Intermediate_Files/Contig1_updated_genes_220314-YLEC12_pseudogene-PILEUP-LIFTOVER-BETA.gtf"
pileup = "../../../Code/190-173-19/annotation_transfer2/pileup-liftOver/conversion.pileup"

#create mapping hash
mappingHash = {}

DEL_count = 0
DEL_progress = 0

inHandle = open(pileup)
line = inHandle.readline()
		
while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	lineInfo = line.split("\t")
	
	pos = int(lineInfo[1])
	ref = lineInfo[2]
	pileup_seq = lineInfo[4]
	
	insResult = re.search("\\.\\+(\d*)\w+",pileup_seq)
	delResult = re.search("\\.\\-(\d*)\w+",pileup_seq)
	
	if (pileup_seq == "^].")or(pileup_seq == ".")or(pileup_seq == ".$"):
		mappingHash[pos]=pos+shift
		
		if (DEL_count != 0) or (DEL_progress !=0):
			if DEL_count == DEL_progress:
				print "Resetting deletion shift!\n\n"
				DEL_count = 0
				DEL_progress = 0
			else:
				print "Error handling deletion!"
				print type(DEL_count)
				print type(DEL_progress)
				print "DEL_count: |" + str(DEL_count) +"|"
				print "DEL_progress: |" + str(DEL_progress) +"|"
				print line
				sys.exit()		
	elif pileup_seq == "*":
		shift=shift-1
		mappingHash[pos]=pos+shift
		
		DEL_progress += 1
		print "Shifting "+str(shift)+" for "+str(DEL_progress)+"/"+str(DEL_count)+" deletion nucleotides..."
	elif (pileup_seq == "A")or(pileup_seq == "C")or(pileup_seq == "G")or(pileup_seq == "T"):
		mappingHash[pos]=pos+shift
		print "\nFor GTF conversion purposes, make no shift in mapping for "+ref+"-->"+pileup_seq+" SNP...\n\n"
	elif insResult:
		ins_count = insResult.group(1)
		if len(ins_count)!=0:
			#nothing special for current nucleotide
			mappingHash[pos]=pos+shift
			
			shift=shift + int(ins_count)
			print "Total shift of "+str(shift)+ " for " + pileup_seq + " after position " +str(pos)+" ..."
		else:
			print "Modify insertion code for :" + pileup_seq
			print ins_count
			print line
			sys.exit()
	elif delResult:
		prelim_del_count = delResult.group(1)
		if len(prelim_del_count)!=0:
			#nothing special for current nucleotide
			mappingHash[pos]=pos+shift
			
			print "\nStart deletion countdown for " + pileup_seq + " after position " +str(pos)+" ..."
			DEL_count = int(prelim_del_count)
		else:
			print "Modify deletion code for :" + pileup_seq
			print del_count
			print line
			sys.exit()
	else:
		print "Modify code to map: " + pileup_seq
		print line
		sys.exit()

	line = inHandle.readline()
		
inHandle.close()

#convert coordinates
geneID = ""
copyHash = {}

outHandle = open(GTFout, "w")

inHandle = open(GTFin)
line = inHandle.readline()
		
while line:
	line = re.sub("\n","",line)
	line = re.sub("\r","",line)
	
	lineInfo = line.split("\t")
	chr = lineInfo[0]
	source = lineInfo[1]
	type = lineInfo[2]
	start_pos = int(lineInfo[3])
	stop_pos = int(lineInfo[4])
	score = lineInfo[5]
	strand = lineInfo[6]
	frame = lineInfo[7]
	transcript_info = lineInfo[8]
	
	#also convert rRNA, due to relatively small revision that is not within the NOR region
	
	if (start_pos > 412375) or (stop_pos >412375):
		print "\nSkip converting annotations towards the end of the assembly:" + transcript_info
	else:
		shift_start = str(mappingHash[start_pos])
		shift_stop = str(mappingHash[stop_pos])
	
		text = contig + "\t" + source+ "\t" + type+ "\t" + shift_start+ "\t" + shift_stop+ "\t" + score+ "\t" + strand+ "\t" + frame + "\t"+transcript_info+"\n"
		outHandle.write(text)
	
	line = inHandle.readline()
		
inHandle.close()
outHandle.close()
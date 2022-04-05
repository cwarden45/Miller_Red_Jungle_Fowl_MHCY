import sys
import re
import os

##190m7
jobCount = 0
unfinishedSamples = ["160406_B2_190M.ccs.10x"]
bwaAlignmentFolder = "190m7/PacBio-CCS_Alignment"
bwaRef = "190m7/190m7_with_Ecoli.fa"

##58f18
#jobCount = 1
#unfinishedSamples = ["160406_A2_58f18.ccs.10x"]
#bwaAlignmentFolder = "Contig2_58f18/PacBio-CCS_Alignment"
#bwaRef = "Contig2_58f18/58f18_with_Ecoli.fa"

readsFolder = "../../CCS_Reads/Apollo_CCS"
threads = 4
email = "cwarden@coh.org"
pairedStatus = "no"
memLimit = "8G"
	
fileResults = os.listdir(readsFolder)

for file in fileResults:
	result = re.search("(.*.ccs.10x).fastq$",file)
	
	if result:
		sample = result.group(1)
		
		jobCount += 1
		
		if (sample in unfinishedSamples):
			print sample		
			shellScript = sample + "_BWA-CCS.sh"
			
			outHandle = open(shellScript, "w")
			text = "#!/bin/bash\n"
			text = text + "#SBATCH -J BWAccs"+str(jobCount)+"\n"
			text = text + "#SBATCH --mail-type=ALL\n"
			text = text + "#SBATCH --mail-user=cwarden@coh.org\n"
			text = text + "#SBATCH -n "+str(threads)+"\n"
			text = text + "#SBATCH -N 1\n"
			text = text + "#SBATCH --mem="+memLimit+"\n"
			text = text + "#SBATCH --time=24:00:00\n"
			text = text + "#SBATCH --output=BWAccs"+str(jobCount)+".log\n\n"
			outHandle.write(text)
			
			text = "module load BWA/0.7.17-foss-2018b\n"
			text = text + "module load SAMtools/0.1.20-foss-2018a\n"
			text = text + "module load picard/2.21.1\n\n"
			outHandle.write(text)
			
			sampleSubfolder = bwaAlignmentFolder + "/" + sample
			text = "mkdir " + sampleSubfolder + "\n"
			outHandle.write(text)
									
			if (pairedStatus == "yes"):
				read1 = readsFolder + "/" + file
				read2 = re.sub("_R1_001.fastq$","_R2_001.fastq",read1)
			
				alnSam = sampleSubfolder + "/aligned.sam"
				text = "bwa mem -M -t "+ str(threads) + " " + bwaRef + " " + read1 + " " + read2  + " > " + alnSam + "\n"
				outHandle.write(text)			
			elif(pairedStatus == "no"):
				read1 = readsFolder + "/" + file
			
				alnSam = sampleSubfolder + "/aligned.sam"
				text = "bwa mem -M -t "+ str(threads) + " " + bwaRef + " " + read1 + " > " + alnSam + "\n"
				outHandle.write(text)
			else:
				print "'PE_Reads' value must be 'yes' or 'no'"
				sys.exit()

			alnBam = sampleSubfolder + "/aligned.bam"
			text = "samtools view -bS " + alnSam + " > " + alnBam + "\n"
			outHandle.write(text)

			text = "rm " + alnSam + "\n"
			outHandle.write(text)
			
			rgBam = sampleSubfolder + "/rg.bam"
			text = "java -Xmx" + memLimit + " -jar /opt/picard/2.21.1/picard.jar AddOrReplaceReadGroups I=" + alnBam + " O=" + rgBam + " SO=coordinate RGID=1 RGLB=BAC RGPL=PacBio RGPU=S00 RGCN=COH RGSM=" + sample + "\n"
			outHandle.write(text)

			text = "rm " + alnBam + "\n"
			outHandle.write(text)
			
			statsFile = sampleSubfolder + "/alignment_stats.txt"
			text = "samtools flagstat " + rgBam + " > " + statsFile + "\n"
			outHandle.write(text)

			duplicateMetrics = sampleSubfolder + "/MarkDuplicates_metrics.txt"
			filteredBam = bwaAlignmentFolder + "/" + sample + ".nodup.bam"
			text = "java -Xmx" + memLimit + " -jar /opt/picard/2.21.1/picard.jar MarkDuplicates I=" + rgBam + " O=" + filteredBam + " M=" + duplicateMetrics+" REMOVE_DUPLICATES=true CREATE_INDEX=true\n"
			outHandle.write(text)
			
			text = "rm " + rgBam + "\n"
			outHandle.write(text)

			statFile = sampleSubfolder + "/idxstats_no_dup.txt"
			text = "samtools idxstats " + filteredBam + " > " + statFile + "\n"
			outHandle.write(text)
			
			raconSam = bwaAlignmentFolder + "/" + sample + ".nodup.sam"
			text = "samtools view " + filteredBam + " > " + raconSam + "\n"
			outHandle.write(text)
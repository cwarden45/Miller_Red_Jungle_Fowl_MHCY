import sys
import re
import os

#190M
jobCount=0
readsFolder = "../../../140225"
bwaAlignmentFolder = "190m7/Illumina_Alignment"
bwaRef = "190m7/190m7_with_Ecoli.fa"

#173o19
#jobCount=1
#readsFolder = "../../../140516/Illumina_Reads"
#bwaAlignmentFolder = "173o1/Illumina_Alignment"
#bwaRef = "173o1/173o1_with_Ecoli.fa"

#34J16
#jobCount=2
#readsFolder = "../../../140725/Reads"
#bwaAlignmentFolder = "Contig3_34j16/Illumina_Alignment"
#bwaRef = "Contig3_34j16/34j16_with_Ecoli.fa"

finishedSamples = []
threads = 4
email = "cwarden@coh.org"
memLimit = "8G"
pairedStatus = "yes"
	
fileResults = os.listdir(readsFolder)

for file in fileResults:
	result = re.search("(.*)_(\w{6})_L\d{3}_R1_001.fastq$",file)
	
	if result:
		sample = result.group(1)
		barcode = result.group(2)
		
		jobCount += 1
		
		if (sample not in finishedSamples):
			print sample
			shellScript = sample + "_BWA.sh"
			
			outHandle = open(shellScript, "w")
			text = "#!/bin/bash\n"
			text = text + "#SBATCH -J BWAi"+str(jobCount)+"\n"
			text = text + "#SBATCH --mail-type=ALL\n"
			text = text + "#SBATCH --mail-user=cwarden@coh.org\n"
			text = text + "#SBATCH -n "+str(threads)+"\n"
			text = text + "#SBATCH -N 1\n"
			text = text + "#SBATCH --mem="+memLimit+"\n"
			text = text + "#SBATCH --time=24:00:00\n"
			text = text + "#SBATCH --output=BWAi"+str(jobCount)+".log\n\n"
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
			text = "java -Xmx" + memLimit + " -jar /opt/picard/2.21.1/picard.jar AddOrReplaceReadGroups I=" + alnBam + " O=" + rgBam + " SO=coordinate RGID=1 RGLB=BAC RGPL=Illumina RGPU="+barcode+" RGCN=COH RGSM=" + sample + "\n"
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
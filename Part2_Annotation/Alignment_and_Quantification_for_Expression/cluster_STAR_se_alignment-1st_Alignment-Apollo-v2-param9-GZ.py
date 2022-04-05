import sys
import re
import os
import commands

#modified version of \\isi-dcnl\user_data\Seq\cwarden\TEMPLATES\scripts\RNAseq_templates\TopHat_Workflow\cluster_STAR_se_alignment-1st_Alignment-Apollo-v2.py

jobPrefix="MM"
alignmentFolder = "STAR-param9/Separate_Alignments"
max_concurrent = 8
finishedSamples = ("")

java = "/net/isi-dcnl/ifs/user_data/Seq/software/jre1.8.0_121/bin/java"
jar_path = "/net/isi-dcnl/ifs/user_data/Seq/software/"

java_mem = "32g"
threads = "4"
ref = "galGalCust_STAR-reformat"
readsFolder = "../../../SQNannotation_3MHCY_Contigs01Jun2017/Illumina_RNAseq"
email = "cwarden@coh.org"
STAR = "/net/isi-dcnl/ifs/user_data/Seq/software/STAR-2.5/bin/Linux_x86_64_static/STAR"

	
fileResults = os.listdir(readsFolder)

jobCount = 0
jobHash={}

for file in fileResults:
	result = re.search("(.*)_1.fastq.gz$",file)
	
	if result:
		sample = result.group(1)
		
		if (sample not in finishedSamples):
			print sample
			jobCount += 1
			jobName = jobPrefix+str(jobCount)
			print jobName

			shellScript = "STAR_" + sample + ".sh"

			outHandle = open(shellScript, "w")
			text = "#!/bin/bash\n"
			text = text + "#SBATCH -J "+jobName+"\n"
			text = text + "#SBATCH --mail-type=ALL\n"
			text = text + "#SBATCH --mail-user="+email+"\n"
			text = text + "#SBATCH -n "+threads+"\n"#I have successfully 2 threads with 32 GB on Apollo
			text = text + "#SBATCH -N 1\n"
			text = text + "#SBATCH --mem="+java_mem+"\n"#I recommend 32GB
			text = text + "#SBATCH --time=48:00:00\n"
			text = text + "#SBATCH --output="+jobName+".log\n\n"

			text = text + "module load samtools/1.6\n\n"		
			outHandle.write(text)
			
			outputSubfolder = alignmentFolder +"/" + sample
			text = "mkdir " + outputSubfolder + "\n"
			outHandle.write(text)

			read1 = re.sub(".gz$","",readsFolder + "/" + file)
			text = "gunzip -c " + read1 + ".gz > " + read1+ "\n"
			outHandle.write(text)

			read2 = re.sub("_1.fastq","_2.fastq", read1)
			text = "gunzip -c " + read2 + ".gz > " + read2+ "\n"
			outHandle.write(text)
			
			#(previously) added --alignIntronMax 2000 --outFilterMismatchNoverLmax 0.1 --outFilterIntronMotifs RemoveNoncanonical
			#REMOVE --twopassMode Basic (as suggested here: https://github.com/alexdobin/STAR/issues/1261)
			#(recently) added --alignSJoverhangMin 20 --alignSJDBoverhangMin 20
			starPrefix = outputSubfolder + "/" + sample + "_"
			text = STAR + " --genomeDir " + ref+ " --readFilesIn " + read1 + " " + read2 +" --runThreadN " +threads+ " --outFileNamePrefix " + starPrefix + " --alignIntronMax 2000 --alignSJoverhangMin 20 --alignSJDBoverhangMin 20 --outFilterMismatchNoverLmax 0.1 --outFilterIntronMotifs RemoveNoncanonical --outSAMstrandField intronMotif\n"
			outHandle.write(text)

			starSam = outputSubfolder + "/" + sample + "_Aligned.out.sam"
			alnBam = outputSubfolder + "/aligned.bam"
			text = "samtools view -bS " + starSam + " > " + alnBam + "\n"
			outHandle.write(text)
			
			userBam = alignmentFolder + "/" + sample + ".bam"
			text = "samtools sort -T "+sample+" -o" + userBam + " "+alnBam+"\n"
			outHandle.write(text)
			
			text = "rm " + starSam + "\n"
			outHandle.write(text)

			text = "rm " + alnBam + "\n"
			outHandle.write(text)
			
			text = "samtools index " + userBam + "\n"
			outHandle.write(text)
			
			text = "rm " + read1 + "\n"
			outHandle.write(text)
			
			text = "rm " + read2 + "\n"
			outHandle.write(text)
			
			outHandle.close()
			
			if jobCount > max_concurrent:
				#test code from https://hpc.nih.gov/docs/job_dependencies.html
				
				depJobName = jobPrefix+str(jobCount-max_concurrent)
				depJobID = ""
				if depJobName in jobHash:
					depJobID=jobHash[depJobName]
				else:
					print "Error mapping ID for " + depJobName
					sys.exit()
			
				cmd = "sbatch --depend=afterany:"+ depJobID + " " + shellScript
				status, outtext = commands.getstatusoutput(str(cmd))
				
				numResult = re.search("(\d+)",outtext)
				if numResult:
					jobnum = numResult.group(1)
				else:
					print "Modify code to parse output: " + outtext
					sys.exit()
				
				jobHash[jobName] = jobnum
				print jobName + "-->"+jobnum
			else:
				cmd = "sbatch " + shellScript
				print cmd
				status, outtext = commands.getstatusoutput(cmd)

				numResult = re.search("(\d+)",outtext)
				if numResult:
					jobnum = numResult.group(1)
				else:
					print "Modify code to parse output: " + outtext
					sys.exit()
				
				jobHash[jobName] = str(jobnum)
				print jobName + "-->"+jobnum

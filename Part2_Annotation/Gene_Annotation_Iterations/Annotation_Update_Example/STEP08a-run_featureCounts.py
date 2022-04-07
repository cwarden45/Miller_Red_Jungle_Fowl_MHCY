import sys
import re
import os

gtf_file = "../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/GTF_GFF_Files/Combined_updated_genes-220317.gtf"
alignmentFolder = "../../BAC_annotation/latest_sequin_files-G3_submission/Combined_Ref-v2/GMAP_EST-param6"

finishedSamples = ("")
threads=2

fileResults = os.listdir(alignmentFolder)

for file in fileResults:
	result = re.search(".bam$",file)
	fullPath = os.path.join(alignmentFolder, file)
	
	if result:
		sample = re.sub(".bam$","",file)
		sortResult = re.search(".name.sort.bam",file)
		
		if (sample not in finishedSamples) and (not sortResult):
			print sample
		
			countsFile = "featureCounts_GMAP_" + sample + "_multimap_gene_counts.txt"
			command = "/opt/subread-1.5.2-source/bin/featureCounts -M -R --minOverlap 500 --fracOverlap 0.5 -s 0 -T "+str(threads)+" -a " + gtf_file + " -o " + countsFile + " " + fullPath
			os.system(command)
			
			featureOutput = file + ".featureCounts"
			readInfo = "featureCounts_GMAP_" + sample + "_multimap_read_info.txt"
			command = "mv " + featureOutput + " " + readInfo
			os.system(command)
			
			countsFile = "featureCounts_GMAP_" + sample + "_unique_gene_counts.txt"
			command = "/opt/subread-1.5.2-source/bin/featureCounts -R --minOverlap 500 --fracOverlap 0.5 -s 0 -T "+str(threads)+" -a " + gtf_file + " -o " + countsFile + " " + fullPath
			os.system(command)

			featureOutput = file + ".featureCounts"
			readInfo = "featureCounts_GMAP_" + sample + "_unique_read_info.txt"
			command = "mv " + featureOutput + " " + readInfo
			os.system(command)			

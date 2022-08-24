import os

#sample = "COH_cDNA"
#FA = "../../Code/BLAST_KnownGenes/Marcia_cDNA.fa"
#alignmentFolder = "GMAP_EST-param6"

#sample = "Partial_MHCY"
#FA = "../../Code/BLAST_KnownGenes/MHCY_Partial/AY257165_AY257170-reformat.fasta"
#alignmentFolder = "GMAP_EST-param6"

#sample = "NCBI_EST"
#FA = "../Code/BLAST_KnownGenes/NCBI_galGal_EST.fasta"
#alignmentFolder = "GMAP_EST-param6"

sample = "NCBI_EST_220330"
FA = "../Code/BLAST_KnownGenes/NCBI_galGal_EST-220330.fasta"
alignmentFolder = "GMAP_EST-param6"

refD = "."
refN= "galGalCust"

threads = 1
java_mem = "8g"

outputSubfolder = alignmentFolder +"/" + sample
gmapSam = outputSubfolder + "/aligned.sam"
#alignment already run on Apollo (and output folder is also already created)...
																			
rgBam = alignmentFolder + "/"+sample+".bam"
command = "java -Xmx" + java_mem + " -jar /opt/picard-2.17.jar AddOrReplaceReadGroups I=" + gmapSam + " O=" + rgBam + " SO=coordinate RGID=1 RGLB=RNA-Seq RGPL=Iso-Seq RGPU=COH RGSM=" + sample + " CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT"
os.system(command)

statFile = outputSubfolder + "/flagstat.txt"
command = "samtools flagstat " + rgBam +" > " +statFile
os.system(command)

statFile = outputSubfolder + "/idxstat.txt"
command = "samtools idxstats " + rgBam +" > " +statFile
os.system(command)
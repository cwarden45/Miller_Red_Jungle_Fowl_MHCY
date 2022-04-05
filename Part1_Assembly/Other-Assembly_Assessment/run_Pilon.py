import os

refFa = "../190m7/190m7.fasta"
bacBam = "190m7/Illumina_Alignment/6504_BAC_190m7.nodup.bam"
outDir = "190m7/Illumina_Alignment/Pilon/6504_BAC_190m7"

#refFa = "../173o1/173o1.fasta"
#bacBam = "173o1/Illumina_Alignment/7083_BAC_173o1.nodup.bam"
#outDir = "173o1/Illumina_Alignment/Pilon/7083_BAC_173o1"

#refFa = "../Contig3_34j16_rev/Contig3.fasta"
#bacBam = "Contig3_34j16/Illumina_Alignment/7533_Less500bp.nodup.bam"
#outDir = "Contig3_34j16/Illumina_Alignment/Pilon/7533_Less500bp"

#refFa = "../Contig3_34j16_rev/Contig3.fasta"
#bacBam = "Contig3_34j16/Illumina_Alignment/7533_morethan500bp.nodup.bam"
#outDir = "Contig3_34j16/Illumina_Alignment/Pilon/7533_morethan500bp"

javaMem = "8g"

command = "mkdir " + outDir
os.system(command)

command = "java -Xmx"+javaMem +" -jar /opt/pilon-1.23.jar --genome "+ refFa + " --frags " + bacBam + " --outdir " + outDir + " --changes --vcf --tracks --minmq 50 --minqual 30"
os.system(command)

command = "samtools faidx " + outDir + "/pilon.fasta"
os.system(command)
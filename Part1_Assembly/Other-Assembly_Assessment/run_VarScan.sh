#!/bin/bash

SAMPLEID=6504_BAC_190m7
ALNFOLDER=190m7/Illumina_Alignment
REF=190m7/190m7_with_Ecoli.fa

#SAMPLEID=160406_B2_190M.ccs.10x
#ALNFOLDER=190m7/PacBio-CCS_Alignment
#REF=190m7/190m7_with_Ecoli.fa

#SAMPLEID=7083_BAC_173o1
#ALNFOLDER=173o1/Illumina_Alignment
#REF=173o1/173o1_with_Ecoli.fa

#SAMPLEID=160406_A2_58f18.ccs.10x
#ALNFOLDER=Contig2_58f18/PacBio-CCS_Alignment
#REF=Contig2_58f18/58f18_with_Ecoli.fa

#SAMPLEID=7533_Less500bp
#ALNFOLDER=Contig3_34j16/Illumina_Alignment
#REF=Contig3_34j16/34j16_with_Ecoli.fa

#SAMPLEID=7533_morethan500bp
#ALNFOLDER=Contig3_34j16/Illumina_Alignment
#REF=Contig3_34j16/34j16_with_Ecoli.fa


#copied from \\isi-dcnl\user_data\lcouture\Seq\200803\Code\Round5

BAM=$ALNFOLDER/$SAMPLEID.nodup.bam
PILEUP=$ALNFOLDER/$SAMPLEID/BWA-MEM.$SAMPLEID.pileup

MINCOV=10;
MINREAD=4;
MINQUAL=20;
MINFREQ=0.3;

samtools mpileup -C50 -f $REF $BAM > $PILEUP

#VarScan-Cons
VARSCANSNP=$ALNFOLDER/$SAMPLEID/varscan.cons.snp.vcf
java -jar -Xmx8g /opt/VarScan.v2.3.9.jar mpileup2snp $PILEUP --min-coverage $MINCOV --min-reads2 $MINREAD --min-avg-qual $MINQUAL --min-var-freq $MINFREQ --output-vcf > $VARSCANSNP
VARSCANINDEL=$ALNFOLDER/$SAMPLEID/varscan.cons.indel.vcf
java -jar -Xmx8g /opt/VarScan.v2.3.9.jar mpileup2indel $PILEUP --min-coverage $MINCOV --min-reads2 $MINREAD --min-avg-qual $MINQUAL --min-var-freq $MINFREQ --output-vcf > $VARSCANINDEL
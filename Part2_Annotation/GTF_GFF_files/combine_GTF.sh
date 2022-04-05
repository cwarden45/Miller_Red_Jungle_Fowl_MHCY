GTF1=../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_220314/Contig1_updated_genes.gtf
GTF2=../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_220314/Contig2_updated_genes.gtf
GTF3=../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_220314/Contig3_updated_genes.gtf
GTF4=../../../../SQNannotation_3MHCY_Contigs01Jun2017/update_gene_names_220314/Contig4_updated_genes.gtf
GTFOUT=Combined_updated_genes-220324.gtf

#GTF1=../../Contig1/scripts/RepeatMasker/Contig1.fasta.out.gff
#GTF2=../../Contig2_58f18/scripts/RepeatMasker/Contig2.fasta.out.gff
#GTF3=../../Contig3_34j16_rev/scripts/RepeatMasker/Contig3.fasta.out.gff
#GTF4=../../Contig4_Fosmids/scripts/RepeatMasker/Contig4.fasta.out.gff
#GTFOUT=Combined_RepeatMasker.gff #leave comments produced by program for each file

#GTF1=EMBOSS_Cpgplot/Contig1.gff
#GTF2=EMBOSS_Cpgplot/Contig2.gff
#GTF3=EMBOSS_Cpgplot/Contig3.gff
#GTF4=EMBOSS_Cpgplot/Contig4.gff
#GTFOUT=Combined_EMBOSS_Cpgplot.gff #leave comments produced by program for each file


cat $GTF1 $GTF2 $GTF3 $GTF4 > $GTFOUT
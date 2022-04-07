import os

#contig = "Contig1"
#contig = "Contig2"
#contig = "Contig3"
contig = "Contig4"

contigFA = contig+"_gene_named.fa"

#use updated RefSeq
ref_RefSeq = "../../BAC_annotation/Code/BLAST_KnownGenes/RefSeq/RefSeq_200527/GCF_000002315.6_GRCg6a_rna_from_genomic-extended2.fa"
ref_cDNA = "../../BAC_annotation/Code/BLAST_KnownGenes/Marcia_cDNA-deposited_names.fa"
ref_extra_MHCY = "../../BAC_annotation/Code/BLAST_KnownGenes/MHCY_Partial/AY257165_AY257170-reformat.fasta"

##RefSeq
command = "makeblastdb -in " + ref_RefSeq + " -dbtype nucl"
#os.system(command)

result = contig+"_named_RefSeq_BLAST_result.txt"
#test removing "-num_alignments 1"
command = "blastn -evalue 1e-20 -query " +contigFA + " -db " + ref_RefSeq + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

##cDNA
command = "makeblastdb -in " + ref_cDNA + " -dbtype nucl"
#os.system(command)

result = contig+"_named_cDNA_BLAST_result.txt"
#test removing "-num_alignments 1"
command = "blastn -evalue 1e-20 -query " +contigFA + " -db " + ref_cDNA + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)

##extra MHC-Y
command = "makeblastdb -in " + ref_extra_MHCY + " -dbtype nucl"
#os.system(command)

result = contig+"_named_custom-MHCY_BLAST_result.txt"
#test removing "-num_alignments 1"
command = "blastn -evalue 1e-20 -query " +contigFA + " -db " + ref_extra_MHCY + " -out " + result + " -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\""
os.system(command)
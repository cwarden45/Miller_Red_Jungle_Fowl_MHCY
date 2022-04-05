#!/bin/bash
refFa=../../earlier_sequin_files-DO_NOT_USE/Contig1_190-173-19/scripts/GMAP_Bowtie2_indices/truncated_galGal5.fa
contigFa1=../Contig1/Contig1.fasta
contigFa2=../Contig2_58f18/Contig2.fasta
contigFa3=../Contig3_34j16_rev/Contig3.fasta
contigFa4=../Contig4_Fosmids/Contig4.fasta
combinedRef=truncated_galGal5_with_AllContigs.fa
refID=galGalCust

cat $refFa $contigFa1 $contigFa2 $contigFa3 $contigFa4 > $combinedRef

samtools faidx $combinedRef
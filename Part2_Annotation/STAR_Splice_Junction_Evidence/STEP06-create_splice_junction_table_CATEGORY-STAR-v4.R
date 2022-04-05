junction_file = "combined_splice_junctions-STAR-v4-param9-ADJUSTED_CPM.txt"
gene_category_file = "combined_splice_junctions-STAR-v4_totalCPM-param9-ADJUSTED.txt"
evenness_file = "SD_stats.txt"
output_file = "combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM.txt"

junction_table = read.table(junction_file, head=T, sep="\t")

all_junctionsA=(junction_table$junctions1_n1 == "1 / 1")|(junction_table$junctions1_n1 == "2 / 2")|(junction_table$junctions1_n1 == "3 / 3")|(junction_table$junctions1_n1 == "4 / 4")|(junction_table$junctions1_n1 == "5 / 5")|(junction_table$junctions1_n1 == "6 / 6")|(junction_table$junctions1_n1 == "7 / 7")
all_junctionsB=(junction_table$junctions10_n3 == "1 / 1")|(junction_table$junctions10_n3 == "2 / 2")|(junction_table$junctions10_n3 == "3 / 3")|(junction_table$junctions10_n3 == "4 / 4")|(junction_table$junctions10_n3 == "5 / 5")|(junction_table$junctions10_n3 == "6 / 6")|(junction_table$junctions10_n3 == "7 / 7")
all_junctionsC=(junction_table$junctions100_n10 == "1 / 1")|(junction_table$junctions100_n10 == "2 / 2")|(junction_table$junctions100_n10 == "3 / 3")|(junction_table$junctions100_n10 == "4 / 4")|(junction_table$junctions100_n10 == "5 / 5")|(junction_table$junctions100_n10 == "6 / 6")|(junction_table$junctions100_n10 == "7 / 7")

category_table = read.table(gene_category_file, head=T, sep="\t")
Copy_Name = rep("",nrow(junction_table))
Copy_Count = rep("",nrow(junction_table))

for (i in 1:nrow(junction_table)){
	temp_gene = junction_table$Gene[i]
	temp_gene_table = category_table[category_table$Gene == temp_gene,]
	Copy_Name[i]=as.character(temp_gene_table$Copy_Name[1])
	Copy_Count[i]=temp_gene_table$Copy_Count[1]
}#endfor (i in 1:nrow(category_table)) 

SD_table = read.table(evenness_file, head=T, sep="\t")
SD_table$min_total_logSD_per_gene.above_median_linear10 = round(SD_table$min_total_logSD_per_gene.above_median_linear10, digits=2)
SD_table$min_total_logSD_per_gene.above_median_linear10[is.na(SD_table$min_total_logSD_per_gene.above_median_linear10)]="No Score"
SD_stat = SD_table$min_total_logSD_per_gene.above_median_linear10
SD_stat_text = paste(SD_stat, " (n=",SD_table$num_samples.above_median_linear10,")",sep="")

low_SD = rep(FALSE,nrow(junction_table))
low_SD[(SD_table$min_total_logSD_per_gene.above_median_linear10 < 0.6) & (SD_table$num_samples.above_median_linear10 >= 3)]=TRUE

EvidenceCat = rep("F", nrow(junction_table))
EvidenceCat[all_junctionsA]="C"
EvidenceCat[(junction_table$meanCPM > 0.6) & all_junctionsB]="B"
EvidenceCat[(junction_table$meanCPM > 0.6) & (all_junctionsC | low_SD)]="A"

EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC30.MHCY8a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC30.MHCY8a"]," (with cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC48.MHCY17a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC48.MHCY17a"]," (with cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig2.LOC11.MHCY25a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig2.LOC11.MHCY25a"]," (with cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC02.MHCY34b"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC02.MHCY34b"]," (with cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC14.MHCY37c"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC14.MHCY37c"]," (with cDNA)",sep="")

#based upon manual inspection, we agree that something is different about this locus.  However, we were not quite ready to call it a pseudogene.
EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC06.MHCY2B1a"] = "D"

print(table(EvidenceCat))

output.table = data.frame(Gene=junction_table$Gene, Copy_Name, Copy_Count,
							Illumina.RJF.RNAseq.Evidence=EvidenceCat,
							meanCPM=round(junction_table$meanCPM, digits=2),
							SD_stat_text,
							junctions_1read_1sample=junction_table$junctions1_n1,
							junctions_10reads_3samples=junction_table$junctions10_n3,
							junctions_100reads_10samples=junction_table$junctions100_n10)
write.table(output.table, output_file, quote=F, sep="\t", row.names=F)
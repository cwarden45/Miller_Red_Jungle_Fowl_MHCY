junction_file = "combined_splice_junctions-STAR-v4-param9-ADJUSTED_CPM.txt"
gene_category_file = "combined_splice_junctions-STAR-v4_totalCPM-param9-ADJUSTED.txt"
output_file = "combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM-PER_LOCUS.txt"
output_file2 = "combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM-SUMMED.txt"

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

EvidenceCat = rep("F", nrow(junction_table))
EvidenceCat[all_junctionsA]="C"
EvidenceCat[(junction_table$meanCPM > 0.6) & all_junctionsB]="B"
EvidenceCat[(junction_table$meanCPM > 0.6) & all_junctionsC]="A"

EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC30.MHCY8a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC30.MHCY8a"]," (with 4 cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC48.MHCY17a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC48.MHCY17a"]," (with 4 cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig2.LOC11.MHCY25a"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig2.LOC11.MHCY25a"]," (with 4 cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC02.MHCY34b"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC02.MHCY34b"]," (with 1 cDNA)",sep="")
EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC14.MHCY37c"] = paste(EvidenceCat[junction_table$Gene == "RJF.Contig3.LOC14.MHCY37c"]," (with 1 cDNA)",sep="")

#based upon manual inspection, we agree that something is different about this locus.  However, we were not quite ready to call it a pseudogene.
EvidenceCat[junction_table$Gene == "RJF.Contig1.LOC06.MHCY2B1a"] = "D"

print(table(EvidenceCat))

output.table = data.frame(Gene=junction_table$Gene, Gene_Type=Copy_Name, Gene_Copy_Count=Copy_Count,
							meanCPM=round(junction_table$meanCPM, digits=2),
							junctions_1read_1sample=junction_table$junctions1_n1,
							junctions_10reads_3samples=junction_table$junctions10_n3,
							junctions_100reads_10samples=junction_table$junctions100_n10,
							Illumina.RJF.RNAseq.Evidence=EvidenceCat)
write.table(output.table, output_file, quote=F, sep="\t", row.names=F)

Gene_Name_Short = as.character(output.table$Gene)
Gene_Name_Short = gsub("RJF.Contig\\d.LOC\\d+.","",Gene_Name_Short)

Sequence_Type = levels(as.factor(Copy_Name))
Gene_Group = rep("MHCY",length(Sequence_Type))
Gene_Group[grep("MHCY-B-",Sequence_Type)] = "MHCY2B"
Gene_Group[grep("YLEC",Sequence_Type)] = "YLEC"
Gene_Group[grep("ZNF",Sequence_Type)] = "ZNF"

Gene_Name_List = tapply(Gene_Name_Short, Copy_Name, paste, collapse=",")
Summed_Count = tapply(rep(1,length(Copy_Name)), Copy_Name, sum)

condense_junctions = function(junction_arr){
	temp_arr = unique(as.character(junction_arr))

	if(length(temp_arr) == 1){
		return(temp_arr)
	}else{
		#assuming there is not more than 2 possible values
		return(paste(temp_arr,collapse=" or "))
	}
}#end def condense_junctions

junctions_1read_1sample_Sum = tapply(junction_table$junctions1_n1, Copy_Name, condense_junctions)
junctions_10reads_3samples_Sum= tapply(junction_table$junctions10_n3, Copy_Name, condense_junctions)
junctions_100reads_10samples_Sum= tapply(junction_table$junctions100_n10, Copy_Name, condense_junctions)

meanCPM_Sum = tapply(as.numeric(as.character(output.table$meanCPM)), Copy_Name, sum)

EvidenceCat_Sum = EvidenceCat[match(Sequence_Type, Copy_Name)]

output.table2 = data.frame(Gene=Gene_Group, Sequence_Type,
							Locus_Loci=Gene_Name_List,
							Count = Summed_Count,
							junctions_1read_1sample=junctions_1read_1sample_Sum,
							junctions_10reads_3samples=junctions_10reads_3samples_Sum,
							junctions_100reads_10samples=junctions_100reads_10samples_Sum,
							Adjusted_Mean=meanCPM_Sum,
							Illumina.RJF.RNAseq.Evidence=EvidenceCat_Sum)
write.table(output.table2, output_file2, quote=F, sep="\t", row.names=F)

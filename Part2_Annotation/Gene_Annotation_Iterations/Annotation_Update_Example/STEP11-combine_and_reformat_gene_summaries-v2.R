#setwd("R:\\mmiller\\Seq\\SQNannotation_3MHCY_Contigs01Jun2017\\update_gene_names_220824")

contig_nums = 1:4
STAR_category_file = "combined_splice_junctions-STAR-v4-CATEGORIES-param9-ADJUSTED_CPM-PER_LOCUS.txt"

output.file1 = "combined_gene_summary.txt"
output.file2 = "combined_gene_summary-ALT.txt"

for (i in contig_nums){
	input.file = paste("Contig",i,"_gene_summary.txt",sep="")
	
	input.table = read.table(input.file, head=T, sep="\t")
	
	if (i == 1){
		output.table = input.table
	}else{
		output.table = rbind(output.table,input.table)
	}#end else
	
}#end for (i in contig_nums)
write.table(output.table, output.file1, quote=F, sep="\t", row.names=F)

print(dim(output.table))
rRNA_rows = output.table[grep(".RN\\d+",output.table$Full.Name),]
rRNA_LOC = c("RJF.Contig1.LOC01","RJF.Contig1.LOC02","RJF.Contig1.LOC03")
rRNA_start = c(NA,NA,NA)
rRNA_stop = c(NA,NA,NA)
rRNA_length = c(0,0,0)

for (i in 1:length(rRNA_LOC)){
	LOC = rRNA_LOC[i]
	temp.table = rRNA_rows[grep(LOC,output.table$Full.Name),]
	for (j in 1:nrow(temp.table)){
		loc_arr = unlist(strsplit(temp.table$Location,split="-"))
		
		if (j == 1){
			rRNA_start[i] = as.numeric(loc_arr[1])
			rRNA_stop[i] = as.numeric(loc_arr[2])
		}else{
			rRNA_start[i] = min(loc_arr[1], rRNA_start[i], na.rm = TRUE)
			rRNA_stop[i] = max(loc_arr[2], rRNA_stop[i], na.rm = TRUE)
		}
	}#end for (j in 1:nrow(temp.table))
	
	rRNA_length[i] = sum(temp.table$Gene_Length)
}#end for (LOC in rRNA_LOC)

rRNA_location = paste(rRNA_start,rRNA_stop,sep="-")

rRNA_rows =data.frame(Contig = rep("Contig1",3),
						Location=rRNA_location,
						Full.Name = rRNA_LOC,
						Contig.Gene.Name = rRNA_LOC,
						Gene.Category = rep("rRNA",3),
						Contig1.Homology = rep(NA, 3),
						Contig2.Homology = rep(NA, 3),
						Contig3.Homology = rep(NA, 3),
						Contig4.Homology = rep(NA, 3),
						Gene.Type = rep("rRNA",3),
						Num.Exons = rep("transcript cluster, multiple intronless genes",3),
						Gene_Length = rRNA_length,
						Orientation = rep("+",3),
						Extended.RefSeq = rep("Defined from KT445934 Annotations",3),
						COH.cDNA.Validation = rep(NA, 3),
						Extended.EST.Hits = rep(NA, 3),
						Full.Name.1 = rRNA_LOC)
print(dim(output.table))
output.table = output.table[-grep(".RN\\d+",output.table$Full.Name),]
output.table = rbind(rRNA_rows, output.table)
print(dim(output.table))

STAR.table = read.table(STAR_category_file, head=T, sep="\t")
STAR.table = STAR.table[match(output.table$Full.Name,STAR.table$Gene),]

#locus
extract_locus = function(char_name){
	arr_name = unlist(strsplit(char_name, split="\\."))
	return(gsub("LOC","",arr_name[3]))
}#end def extract_locus

LOCUS = sapply(output.table$Full.Name, extract_locus)

#exon count
extract_exon_count = function(char_description){
	if(is.na(char_description)){
		return(NA)
	}else{
		ratio_arr = unlist(strsplit(char_description, split=" / "))
		SJ_count = as.numeric(ratio_arr[2])
		exon_count = SJ_count + 1
		return(exon_count)
	}#end else
}#end def extract_exon_coun

Num_Exons = sapply(STAR.table$junctions_1read_1sample, extract_exon_count)
Num_Exons[grep("P$",output.table$Full.Name)]="ps"
Num_Exons[output.table$Gene.Category == "rRNA"]="na"

#other reformatting
Region = rep("MHCY",nrow(output.table))
Region[output.table$Gene.Category == "rRNA"] = "NOR"

Gene_Symbol_and_Type = gsub("RJF.","",output.table$Contig.Gene.Name)
Gene_Symbol_and_Type[1:3]="rRNA"

Locus_Tag = output.table$Full.Name
Locus_Tag = gsub("[a-z]$","",Locus_Tag)

RNA_CPM = STAR.table$meanCPM
RNA_CPM[1:3]="na"
RNA_CPM[is.na(RNA_CPM)]="ps"

Annotation_Confidence = STAR.table$Illumina.RJF.RNAseq.Evidence
Annotation_Confidence[1:3]="na"
Annotation_Confidence[is.na(Annotation_Confidence)]="ps"
Annotation_Confidence = gsub(" \\(with cDNA\\)","",Annotation_Confidence)

output.table2 = data.frame(Gene_List_Num=1:nrow(output.table),
							Contig=gsub("Contig","",output.table$Contig),
							Locus_Num = LOCUS,
							Location = output.table$Location,
							Length = output.table$Gene_Length,
							Strand = output.table$Orientation,
							Number_of_Predicted_Exons = Num_Exons,
							Region,
							Gene_Symbol_and_Type,
							Locus_Tag,
							GenBank_Match = output.table$Extended.RefSeq,
							RNA_CPM,
							Annotation_Confidence,
							cDNA=output.table$COH.cDNA.Validation)
							

write.table(output.table2, output.file2, quote=F, sep="\t", row.names=F)
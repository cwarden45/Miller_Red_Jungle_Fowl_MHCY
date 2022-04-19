#setwd("R:\\mmiller\\Seq\\SQNannotation_3MHCY_Contigs01Jun2017\\update_gene_names_220314")

input.file = "combined_splice_junctions-STAR-v3_totalCPM-param9.txt"
output.file = "combined_splice_junctions-STAR-v4_totalCPM-param9-ADJUSTED.txt"

input.table = read.table(input.file, head=T, sep="\t")

SJ.info = input.table[,1:6]
CPM.mat = input.table[,7:ncol(input.table)]

extract.copy.type=function(full_gene){
	#print(full_gene)
	gene_arr = unlist(strsplit(full_gene, split="\\."))
	short_gene = gene_arr[4]
	
	search.partial = regexpr("partial",short_gene)
	search.end_letter = regexpr("[a-z]$",short_gene)
	#print(search.end_letter)
	if(search.partial[1]>0){
		return(short_gene)
	}else if(search.end_letter[1]>0){
		copy_name = gsub("\\d+","-",short_gene)
		return(copy_name)
	}else{
		return(short_gene)
	}#end else
}#end def extract.copy.type()

Copy_Name = sapply(as.character(SJ.info$Gene), extract.copy.type)

unique_names = unique(SJ.info$Gene)
Copy_Name.unique = sapply(unique_names, extract.copy.type)
Copy_Count.mapping = table(Copy_Name.unique)
Copy_Count = rep(1,length(Copy_Name))

CPM.mat2 = matrix(ncol=ncol(CPM.mat), nrow=nrow(CPM.mat))
colnames(CPM.mat2) = colnames(CPM.mat)

for (i in 1:nrow(CPM.mat2)){
	SJ.gene.copy_name = Copy_Name[i]
	SJ.gene.copy_count = Copy_Count.mapping[SJ.gene.copy_name]
	Copy_Count[i]=SJ.gene.copy_count
	#print(Copy_Count[i])
	CPM.mat2[i,]=as.numeric(CPM.mat[i,]/Copy_Count[i])
	#print(CPM.mat[1:4,1:4])
	#print(CPM.mat2[1:4,1:4])
}#end for (i in 1:nrow(CPM.mat2))

output.table = data.frame(SJ.info, Copy_Name, Copy_Count, CPM.mat2)
write.table(output.table, output.file, quote=F, sep="\t", row.names=F)

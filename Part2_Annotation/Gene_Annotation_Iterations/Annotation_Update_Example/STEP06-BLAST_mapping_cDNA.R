contig = "Contig1"
#contig = "Contig2"
#contig = "Contig3"
#contig = "Contig4"

input.file = paste(contig,"_named_cDNA_BLAST_result.txt",sep="")
output.file = paste(contig,"_contig_name_cDNA_BLAST_mapping.txt",sep="")
name.mapping = paste(contig,"_LOC_mapping.txt",sep="")
gtf =paste(contig,"_updated_genes.gtf",sep="")

blast.table = read.table(input.file, head=F, sep="\t")
name.table = read.table(name.mapping, head=T, sep="\t")

blast.table$V5 = as.character(blast.table$V5)
blast.table$V5 = gsub("lcl\\|","",blast.table$V5)

#num.hsp = table(blast.table$V1)
#num.hsp = num.hsp[num.hsp == 1]

num.hsp = table(paste(blast.table$V1,blast.table$V5, sep="-"))

print(dim(blast.table))
#blast.table = blast.table[match(names(num.hsp),blast.table$V1),]
blast.table = blast.table[match(names(num.hsp),paste(blast.table$V1,blast.table$V5, sep="-")),]
print(dim(blast.table))
blast.table = blast.table[blast.table$V10 > 99,]
nident.percent.query = 100 * blast.table$V11 / blast.table$V2
blast.table = blast.table[nident.percent.query > 80,]
blast.table = blast.table[as.character(blast.table$V1) != as.character(blast.table$V5),]

blast.table$V1 = as.character(blast.table$V1)
for(i in 1:nrow(blast.table)){
	#don't really need this step, since keeping original name
	blast.table$V1[i] = as.character(name.table$Pos.Name[match(blast.table$V1[i],name.table$Pos.Name)])
}#end for(i in 1:nrow(blast.table))

write.table(blast.table, output.file, quote=F, sep="\t", col.names=F, row.names=F)

for (ref in levels(as.factor(as.character(blast.table$V5)))){
	ref.table = blast.table[blast.table$V5 == ref,]
	print(paste(ref," : ",paste(ref.table $V1,collapse=","),sep=""))
}

gtf.table = read.table(gtf, head=F, sep="\t")

parse.genes = function(char){
	char.info = unlist(strsplit(char, split=";"))
	gene = gsub("gene_id ","",char.info[1])
	return(gene)
}

defined.genes = unique(sapply(as.character(gtf.table$V9),parse.genes))
undefined.genes = defined.genes[-match(unique(blast.table$V1),defined.genes)]
print(paste("unmatched (",length(undefined.genes),"): ",paste(undefined.genes, collapse=", "),sep=""))

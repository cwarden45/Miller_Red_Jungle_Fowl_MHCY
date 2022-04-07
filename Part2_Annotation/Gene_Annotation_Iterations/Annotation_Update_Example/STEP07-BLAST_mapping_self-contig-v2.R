contigs = c("Contig1", "Contig2", "Contig3", "Contig4")

for (contig1 in contigs){
	for (contig2 in contigs){
		print(paste(contig1,contig2,sep="-"))
		
		input.file = paste(contig1,"_",contig2,"_BLAST_result.txt",sep="")
		output.file = paste(contig1,"_contig_name_",contig2,"_BLAST_mapping.txt",sep="")
		#gtf =paste(contig1,"_updated_genes.gtf",sep="")

		blast.table = read.table(input.file, head=F, sep="\t")

		num.hsp = table(paste(blast.table$V1,blast.table$V5, sep="-"))

		#try skipping this --> see what effect it has, beyond catching ZNF2<-->ZNF3
		#num.hsp = num.hsp[num.hsp == 1]

		#get 1st row for each HSP
		blast.table = blast.table[match(names(num.hsp),paste(blast.table$V1,blast.table$V5, sep="-")),]
		
		blast.table = blast.table[blast.table$V10 > 98,]
		nident.percent.query = 100 *blast.table$V11 / blast.table$V2
		blast.table = blast.table[nident.percent.query > 80,]
		blast.table = blast.table[as.character(blast.table$V1) != as.character(blast.table$V5),]

		write.table(blast.table, output.file, quote=F, sep="\t", col.names=F, row.names=F)

		for (ref in levels(as.factor(as.character(blast.table$V5)))){
			ref.table = blast.table[blast.table$V5 == ref,]
			print(paste(ref," : ",paste(ref.table $V1,collapse=","),sep=""))
		}

		#skip this with pairwise comparisons
		#gtf.table = read.table(gtf, head=F, sep="\t")

		#parse.genes = function(char){
		#	char.info = unlist(strsplit(char, split=";"))
		#	gene = gsub("gene_id ","",char.info[1])
		#	return(gene)
		#}

		#defined.genes = unique(sapply(as.character(gtf.table$V9),parse.genes))
		#undefined.genes = defined.genes[-match(unique(blast.table$V1),defined.genes)]
		#print(paste("unmatched (",length(undefined.genes),"): ",paste(undefined.genes, collapse=", "),sep=""))

	}#end for (contig2 in contigs)
}#end for (contig1 in contigs)
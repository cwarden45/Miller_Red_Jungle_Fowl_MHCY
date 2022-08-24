NCBI.EST.file = "featureCounts_GMAP_NCBI_EST_220330_multimap_read_info.txt"
Partial.MHCY.file = "featureCounts_GMAP_Partial_MHCY_multimap_read_info.txt"

genes = c()
NCBI.EST.evidence = c()
Partial.MHCY.evidence = c()
							  
	NCBI.table = read.table(NCBI.EST.file, head=F, sep="\t", skip=0)
	NCBI.genes = levels(NCBI.table$V3)
	NCBI.genes = NCBI.genes[NCBI.genes != "*"]
	NCBI.seqs = c()
	for (j in 1:length(NCBI.genes)){
		NCBI.seqs[j]=paste(as.character(NCBI.table$V1[NCBI.table$V3 == NCBI.genes[j]]),collapse=",")
	}#end for (j in 1:length(NCBI.genes))

	Partial.MHCY.table = read.delim(Partial.MHCY.file, head=F, sep="\t", skip=0)
	Partial.MHCY.genes = levels(Partial.MHCY.table$V3)
	Partial.MHCY.genes = Partial.MHCY.genes[Partial.MHCY.genes != "*"]
	Partial.MHCY.seqs = c()
	for (j in 1:length(Partial.MHCY.genes)){
		Partial.MHCY.seqs[j]=paste(as.character(Partial.MHCY.table$V1[Partial.MHCY.table$V3 == Partial.MHCY.genes[j]]),collapse=",")
	}#end for (j in 1:length(Partial.MHCY.genes))
	
	rep.genes = union(NCBI.genes, Partial.MHCY.genes)
	
	genes = c(genes, rep.genes)
	NCBI.EST.evidence = c(NCBI.EST.evidence, NCBI.seqs[match(rep.genes,NCBI.genes)])
	Partial.MHCY.evidence = c(Partial.MHCY.evidence, Partial.MHCY.seqs[match(rep.genes,Partial.MHCY.genes)])

output.table = data.frame(genes, NCBI.EST.evidence, Partial.MHCY.evidence)
write.table(output.table,"EST_multimap_evidence.txt", row.names=F, sep="\t", quote=F)
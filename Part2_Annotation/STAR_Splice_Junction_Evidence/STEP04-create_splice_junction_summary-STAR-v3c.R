junctions1_file = "combined_splice_junctions-STAR-v3_min1-param9.txt"
junctions10_file = "combined_splice_junctions-STAR-v3_min10-param9.txt"
junctions100_file = "combined_splice_junctions-STAR-v3_min100-param9.txt"
junctions1_unique_file = "combined_splice_junctions-STAR-v3_min1-UNIQUE-param9.txt"
junctions10_unique_file = "combined_splice_junctions-STAR-v3_min10-UNIQUE-param9.txt"
junctions100_unique_file = "combined_splice_junctions-STAR-v3_min100-UNIQUE-param9.txt"
totalCPM_file = "combined_splice_junctions-STAR-v4_totalCPM-ADJUSTED-junction_average_density-param9.txt"
output_file = "combined_splice_junctions-STAR-v4-param9-ADJUSTED_CPM.txt"

genes = c()
junctions1_n1 = c()
junctions10_n1 = c()
junctions100_n1 = c()
junctions1_unique_n1 = c()
junctions10_unique_n1 = c()
junctions100_unique_n1 = c()

junctions1_n3 = c()
junctions10_n3 = c()
junctions100_n3 = c()
junctions1_unique_n3 = c()
junctions10_unique_n3 = c()
junctions100_unique_n3 = c()

junctions1_n10 = c()
junctions10_n10 = c()
junctions100_n10 = c()
junctions1_unique_n10 = c()
junctions10_unique_n10 = c()
junctions100_unique_n10 = c()

meanCPM=c()
	
junctions1_table = read.table(junctions1_file, head=T, sep="\t")
junctions10_table = read.table(junctions10_file, head=T, sep="\t")
junctions100_table = read.table(junctions100_file, head=T, sep="\t")
junctions1_unique_table = read.table(junctions1_unique_file, head=T, sep="\t")
junctions10_unique_table = read.table(junctions10_unique_file, head=T, sep="\t")
junctions100_unique_table = read.table(junctions100_unique_file, head=T, sep="\t")

totalCPM_table = read.table(totalCPM_file, head=T, sep="\t")
	
temp_junction.table = data.frame(Index = junctions1_table$GTFindex,
									Gene = junctions1_table$Gene,
									SJ1 = junctions1_table$SampleCount,
									SJ10 = junctions10_table$SampleCount[match(junctions1_table$GTFindex, junctions10_table$GTFindex)],
									SJ100 = junctions100_table$SampleCount[match(junctions1_table$GTFindex, junctions100_table$GTFindex)],
									SJ1u = junctions1_unique_table$SampleCount[match(junctions1_table$GTFindex, junctions1_unique_table$GTFindex)],
									SJ10u = junctions10_unique_table$SampleCount[match(junctions1_table$GTFindex, junctions10_unique_table$GTFindex)],
									SJ100u = junctions100_unique_table$SampleCount[match(junctions1_table$GTFindex, junctions100_unique_table$GTFindex)])
	
temp_genes = as.character(unique(junctions1_table$Gene))
	
for(temp_gene in temp_genes){
	print(temp_gene)
	genes = c(genes, temp_gene)
		
	temp_gene_table = temp_junction.table[junctions1_table$Gene == temp_gene,]
	temp_gene_table_avgCPM = totalCPM_table[totalCPM_table$Gene == temp_gene,]
	
	#1 sample
	SJ1_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1 != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions1_n1 = c(junctions1_n1, SJ1_text)
		
	SJ10_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10 != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions10_n1 = c(junctions10_n1, SJ10_text)

	SJ100_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100 != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions100_n1 = c(junctions100_n1, SJ100_text)
		
	SJ1u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1u != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions1_unique_n1 = c(junctions1_unique_n1, SJ1u_text)
		
	SJ10u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10u != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions10_unique_n1 = c(junctions10_unique_n1, SJ10u_text)

	SJ100u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100u != 0,])," / ",nrow(temp_gene_table),sep="")
	junctions100_unique_n1 = c(junctions100_unique_n1, SJ100u_text)
	
	#3 samples
	SJ1_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1 >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions1_n3 = c(junctions1_n3, SJ1_text)
		
	SJ10_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10 >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions10_n3 = c(junctions10_n3, SJ10_text)

	SJ100_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100 >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions100_n3 = c(junctions100_n3, SJ100_text)
		
	SJ1u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1u >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions1_unique_n3 = c(junctions1_unique_n3, SJ1u_text)
		
	SJ10u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10u >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions10_unique_n3 = c(junctions10_unique_n3, SJ10u_text)

	SJ100u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100u >= 3,])," / ",nrow(temp_gene_table),sep="")
	junctions100_unique_n3 = c(junctions100_unique_n3, SJ100u_text)
	
	#10 samples
	SJ1_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1 >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions1_n10 = c(junctions1_n10, SJ1_text)
		
	SJ10_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10 >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions10_n10 = c(junctions10_n10, SJ10_text)

	SJ100_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100 >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions100_n10 = c(junctions100_n10, SJ100_text)
		
	SJ1u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ1u >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions1_unique_n10 = c(junctions1_unique_n10, SJ1u_text)
		
	SJ10u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ10u >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions10_unique_n10 = c(junctions10_unique_n10, SJ10u_text)

	SJ100u_text = paste(nrow(temp_gene_table[temp_gene_table$SJ100u >= 10,])," / ",nrow(temp_gene_table),sep="")
	junctions100_unique_n10 = c(junctions100_unique_n10, SJ100u_text)
	
	#average CPM
	meanCPM = c(meanCPM, mean(temp_gene_table_avgCPM$meanCPM))
}#endfor(temp_gene in temp_genes)

output.table = data.frame(Gene=genes,
							junctions1_n1, junctions1_n3, junctions1_n10,
							junctions10_n1, junctions10_n3, junctions10_n10,
							junctions100_n1, junctions100_n3, junctions100_n10,
							junctions1_unique_n1, junctions1_unique_n3, junctions1_unique_n10,
							junctions10_unique_n1, junctions10_unique_n3, junctions10_unique_n10,
							junctions100_unique_n1, junctions100_unique_n3, junctions100_unique_n10,
							meanCPM)
write.table(output.table, output_file, quote=F, sep="\t", row.names=F)
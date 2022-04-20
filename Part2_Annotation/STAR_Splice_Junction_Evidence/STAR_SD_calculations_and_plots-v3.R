totalCPM.file = "combined_splice_junctions-STAR-v4_totalCPM-param9-ADJUSTED.txt"
uniqueCPM.file = "combined_splice_junctions-STAR-v3_uniqueCPM-param9.txt"

output_folder = "SD_Plots"

command = paste("mkdir",output_folder)
system(command)

totalCPM.table = read.table(totalCPM.file, head=T, sep="\t")
uniqueCPM.table = read.table(uniqueCPM.file, head=T, sep="\t")

genes = unique(totalCPM.table$Gene)

num_samples.above_median_linear1 = c()
min_total_logSD_per_gene.above_median_linear1 = c()

num_samples.above_median_linear10 = c()
min_total_logSD_per_gene.above_median_linear10 = c()

num_samples.above_median_linear100 = c()
min_total_logSD_per_gene.above_median_linear100 = c()

for (gene in genes){
	print(gene)
	gene_totalCPM = totalCPM.table[grep(gene,totalCPM.table$Gene),]
	gene_uniqueCPM = uniqueCPM.table[grep(gene,uniqueCPM.table$Gene),]

	gene_strand = gene_totalCPM[1,5]

	SJ_start = gene_totalCPM$SJ.Start
	if (gene_strand == "+"){
		SJ_start = sort(SJ_start, decreasing = FALSE)
	}else if (gene_strand == "-"){
		SJ_start = sort(SJ_start, decreasing = TRUE)
	}else{
		stop(paste("Need to define way to parse strand:",gene_strand,sep=""))
	}

	junction.names = as.factor(paste("J",1:length(SJ_start),sep=""))
	gene_totalCPM = gene_totalCPM[match(SJ_start,gene_totalCPM$SJ.Start),]
	gene_uniqueCPM = gene_uniqueCPM[match(SJ_start,gene_uniqueCPM$SJ.Start),]

	png(paste(output_folder,"/",gene,"_junction_CPM.png",sep=""))
	par(mfcol=c(2,1))
	#total CPM
	for(i in 9:ncol(gene_totalCPM)){
		plot_CPM = log2(gene_totalCPM[,i]+1)
		#print(max(plot_CPM))
		if (i == 9){
			plot(as.numeric(junction.names), plot_CPM,
					pch=16, main="TOTAL SJ Count Per Million (CPM, Adjusted)",
					xlab="Transcript Junction Count", ylab="log2(STAR SJ CPM+1)",
					ylim=c(0,15), xaxt="n")
			mtext(junction.names, side=1, at =1:length(junction.names), las=1, line=0.5)
		}#if (i == 9)
		points(junction.names, plot_CPM,pch=16)
		lines(junction.names, plot_CPM)
	}#end for(i in 9:ncol(gene_totalCPM))
	abline(h=log2(1+1),col="orange")
	abline(h=log2(10+1),col="blue")
	abline(h=log2(100+1),col="green")

	#unique CPM
	for(i in 7:ncol(gene_uniqueCPM)){
		plot_CPM = log2(gene_uniqueCPM[,i]+1)
		if (i == 7){
			plot(as.numeric(junction.names), plot_CPM,
					pch=16, main="UNIQUE SJ Count Per Million (CPM)",
					xlab="Transcript Junction Count", ylab="log2(STAR SJ CPM+1)",
					ylim=c(0,15), xaxt="n")
			mtext(junction.names, side=1, at =1:length(junction.names), las=1, line=0.5)
		}#if (i == 7)
		points(junction.names, plot_CPM,pch=16)
		lines(junction.names, plot_CPM)
	}#end for(i in 7:ncol(gene_totalCPM))
	abline(h=log2(1+1),col="orange")
	abline(h=log2(10+1),col="blue")
	abline(h=log2(100+1),col="green")
	dev.off()
	
	log_table = log2(gene_totalCPM[,9:ncol(gene_totalCPM)]+1)
	
	sample_medians = apply(log_table, 2, median)
	
	search_logic1 = sample_medians > log2(1+1)
	log_table.above_linear_1 = log_table[,search_logic1]
	search_logic10 = sample_medians > log2(10+1)
	log_table.above_linear_10 = log_table[,search_logic10]
	search_logic100 = sample_medians > log2(100+1)
	log_table.above_linear_100 = log_table[,search_logic100]

	#min linear 1
	if(sum(search_logic1) == 1){	
		num_samples.above_median_linear1 = c(num_samples.above_median_linear1, 1)
		min_total_logSD_per_gene.above_median_linear1 = c(min_total_logSD_per_gene.above_median_linear1, sd(log_table.above_linear_1))
	}else if(sum(search_logic1) > 0){
		total_logSD_by_sample = apply(log_table.above_linear_1, 2, sd)
	
		num_samples.above_median_linear1 = c(num_samples.above_median_linear1, ncol(log_table.above_linear_1))
		min_total_logSD_per_gene.above_median_linear1 = c(min_total_logSD_per_gene.above_median_linear1, min(total_logSD_by_sample))
	}else{
		#print("Skipping calculation...")
		num_samples.above_median_linear1 = c(num_samples.above_median_linear1, 0)
		min_total_logSD_per_gene.above_median_linear1 = c(min_total_logSD_per_gene.above_median_linear1, NA)
	}#end else
	
	#min linear 10
	if(sum(search_logic10) == 1){	
	
		if(gene == "RJF.Contig1.LOC30.MHCY8a"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY8a_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig3.LOC02.MHCY34b"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY34b_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig3.LOC14.MHCY37c"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY37c_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig1.LOC19.MHCY5f"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY5f_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig2.LOC21.MHCY32g"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY32g_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig1.LOC22.YLEC8a"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_YLEC8a_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig1.LOC23.YLEC9b"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_YLEC9b_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}else if(gene == "RJF.Contig3.LOC18.MHCY39r"){
			write.table(data.frame(Sample=names(search_logic10[search_logic10]), SD=sd(log_table.above_linear_10)),"SD_MHCY39r_min10_export.txt", quote=F, sep="\t", row.names=F, col.names=F)
		}#end else

		num_samples.above_median_linear10 = c(num_samples.above_median_linear10, 1)
		min_total_logSD_per_gene.above_median_linear10 = c(min_total_logSD_per_gene.above_median_linear10, sd(log_table.above_linear_10))
	}else if(sum(search_logic10) > 0){
		total_logSD_by_sample = apply(log_table.above_linear_10, 2, sd)

		if(gene == "RJF.Contig1.LOC30.MHCY8a"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY8a_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig3.LOC02.MHCY34b"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY34b_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig3.LOC14.MHCY37c"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY37c_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig1.LOC19.MHCY5f"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY5f_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig2.LOC21.MHCY32g"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY32g_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig1.LOC22.YLEC8a"){
			write.table(data.frame(total_logSD_by_sample),"SD_YLEC8a_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig1.LOC23.YLEC9b"){
			write.table(data.frame(total_logSD_by_sample),"SD_YLEC9b_min10_export.txt", quote=F, sep="\t", col.names=F)
		}else if(gene == "RJF.Contig3.LOC18.MHCY39r"){
			write.table(data.frame(total_logSD_by_sample),"SD_MHCY39r_min10_export.txt", quote=F, sep="\t", col.names=F)
		}#end else
		
		num_samples.above_median_linear10 = c(num_samples.above_median_linear10, ncol(log_table.above_linear_10))
		min_total_logSD_per_gene.above_median_linear10 = c(min_total_logSD_per_gene.above_median_linear10, min(total_logSD_by_sample))
	}else{
		#print("Skipping calculation...")
		num_samples.above_median_linear10 = c(num_samples.above_median_linear10, 0)
		min_total_logSD_per_gene.above_median_linear10 = c(min_total_logSD_per_gene.above_median_linear10, NA)
	}#end else
	
	#min linear 100
	if(sum(search_logic100) == 1){	
		num_samples.above_median_linear100 = c(num_samples.above_median_linear100, 1)
		min_total_logSD_per_gene.above_median_linear100 = c(min_total_logSD_per_gene.above_median_linear100, sd(log_table.above_linear_100))
	}else if(sum(search_logic100) > 0){
		total_logSD_by_sample = apply(log_table.above_linear_100, 2, sd)
		
		num_samples.above_median_linear100 = c(num_samples.above_median_linear100, ncol(log_table.above_linear_100))
		min_total_logSD_per_gene.above_median_linear100 = c(min_total_logSD_per_gene.above_median_linear100, min(total_logSD_by_sample))
	}else{
		#print("Skipping calculation...")
		num_samples.above_median_linear100 = c(num_samples.above_median_linear100, 0)
		min_total_logSD_per_gene.above_median_linear100 = c(min_total_logSD_per_gene.above_median_linear100, NA)
	}#end else
	
	
}#end for (gene in unique(totalCPM.table$Gene))

output.table = data.frame(Gene=genes,
							num_samples.above_median_linear1, min_total_logSD_per_gene.above_median_linear1,
							num_samples.above_median_linear10, min_total_logSD_per_gene.above_median_linear10,
							num_samples.above_median_linear100, min_total_logSD_per_gene.above_median_linear100)
write.table(output.table, "SD_stats.txt", quote=F, sep="\t", row.names=F)
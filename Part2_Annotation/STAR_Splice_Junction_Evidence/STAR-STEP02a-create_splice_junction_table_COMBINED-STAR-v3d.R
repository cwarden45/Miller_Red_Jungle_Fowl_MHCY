combined_raw = "combined_splice_junctions-STAR-v3_RAW-param9.txt"
combined_uniqueCPM = "combined_splice_junctions-STAR-v3_uniqueCPM-param9.txt"
combined_totalCPM = "combined_splice_junctions-STAR-v3_totalCPM-param9.txt"
sample_densityQC = "combined_splice_junctions-STAR-v3_totalCPM-sample_density-param9.png"
junction_average_density = "combined_splice_junctions-STAR-v3_totalCPM-junction_average_density-param9.txt"
junction_average_densityQC = "combined_splice_junctions-STAR-v3_totalCPM-junction_average_density-param9.png"

contigs = c("Contig1","Contig2","Contig3","Contig4")
sample_info_file = "STAR_read_stats-param9.txt"
sample_info_file2 = "PRJNA204941.txt"

sample_info = read.table(sample_info_file, head=T, sep="\t")

sample_info2 = read.table(sample_info_file2, head=T, sep="\t")
print(dim(sample_info2))
sample_info2 = sample_info2[match(sample_info$Sample,sample_info2$Sample),]
print(dim(sample_info2))

Gender2 = rep("F",nrow(sample_info2))
Gender2[sample_info2$Gender == "male"]="M"
altID = paste(sample_info$Sample,Gender2,sample_info2$Tissue,sep=".")

for (i in 1:length(contigs)){
	contig = contigs[i]
	temp.combined = read.table(paste(contig,"_splice_junctions-STAR-full_table-v3-param9.txt",sep=""), head=T, sep="\t")
	temp.uniqueCPM = read.table(paste(contig,"_splice_junctions-STAR-full_table-unique_CPM-v3-param9.txt",sep=""), head=T, sep="\t")
	temp.totalCPM = read.table(paste(contig,"_splice_junctions-STAR-full_table-total_CPM-v3-param9.txt",sep=""), head=T, sep="\t")

	temp.combined.mat = temp.combined[,match(sample_info$Sample,names(temp.combined))]
	temp.uniqueCPM.mat = temp.uniqueCPM[,match(sample_info$Sample,names(temp.uniqueCPM))]
	temp.totalCPM.mat = temp.totalCPM[,match(sample_info$Sample,names(temp.totalCPM))]
	
	if(i == 1){
		combined.table = data.frame(temp.combined[,1:6],temp.combined.mat)
		uniqueCPM.table = data.frame(temp.uniqueCPM[,1:6],temp.uniqueCPM.mat)
		totalCPM.table = data.frame(temp.totalCPM[,1:6],temp.totalCPM.mat)
	}else{
		combined.table2 = data.frame(temp.combined[,1:6],temp.combined.mat)
		uniqueCPM.table2 = data.frame(temp.uniqueCPM[,1:6],temp.uniqueCPM.mat)
		totalCPM.table2 = data.frame(temp.totalCPM[,1:6],temp.totalCPM.mat)
		
		combined.table = rbind(combined.table,combined.table2)
		uniqueCPM.table = rbind(uniqueCPM.table, uniqueCPM.table2)
		totalCPM.table = rbind(totalCPM.table, totalCPM.table2)
	}#end else
}#end for (i in 1:length(contigs))

names(combined.table) = c("JunctionID","SJ.Chr","SJ.Start","SJ.Stop","SJ.Strand","Gene",altID)
names(uniqueCPM.table) = c("JunctionID","SJ.Chr","SJ.Start","SJ.Stop","SJ.Strand","Gene",altID)
names(totalCPM.table) = c("JunctionID","SJ.Chr","SJ.Start","SJ.Stop","SJ.Strand","Gene",altID)

write.table(combined.table, combined_raw, quote=F, sep="\t", row.names=F)
write.table(uniqueCPM.table, combined_uniqueCPM, quote=F, sep="\t", row.names=F)
write.table(totalCPM.table, combined_totalCPM, quote=F, sep="\t", row.names=F)

##QC plots
totalCPM.mat = totalCPM.table[,7:ncol(totalCPM.table)]

#sample (based upon https://github.com/cwarden45/RNAseq_templates/blob/master/TopHat_Workflow/qc.R)
labelColors = rep("black",nrow(sample_info))
labelColors[sample_info$Sample == "SRR924556"]="orange"
labelColors[sample_info$Sample == "SRR924547"]="orange"

png(file = sample_densityQC)
for (i in 1:ncol(totalCPM.mat)){
	rounding_factor = 0.001
	sample_junctionCPM.LOG = log2(as.numeric(t(totalCPM.mat[,i])) + rounding_factor)
			
	plot.min = -3
	plot.max = 15
			
	if(i == 1){
		den = density(sample_junctionCPM.LOG, na.rm=T,from=plot.min, to=plot.max)
		junc_cov = den$x
		freq = den$y
		plot(junc_cov, freq, type="l", xlab = paste("Log2(Junction CPM + ",rounding_factor,") Coverage",sep=""), ylab = "Density",
					xlim=c(plot.min,plot.max), ylim=c(0,0.2), col=labelColors[i],
					    		main = "Sample Junction Total CPM Distribution")
	}else{
		den = density(sample_junctionCPM.LOG, na.rm=T,from=plot.min, to=plot.max)
		junc_cov = den$x
		freq = den$y
		lines(junc_cov, freq, type = "l", col=labelColors[i])
	}#end else
}#end for (i in 1:length(ncol(temp.mat)))
dev.off()

#junction
rownames(totalCPM.mat)=totalCPM.table$JunctionID
meanCPM = apply(totalCPM.mat, 1, mean)
meanCPM_table = data.frame(totalCPM.table[,1:6],meanCPM)
write.table(meanCPM_table, junction_average_density, quote=F, sep="\t", row.names=F)

png(file = junction_average_densityQC)
mean_junctionCPM.LOG = log2(meanCPM + rounding_factor)
		den = density(sample_junctionCPM.LOG, na.rm=T,from=plot.min, to=plot.max)
		junc_cov = den$x
		freq = den$y
		plot(junc_cov, freq, type="l", xlab = paste("Log2(Junction CPM + ",rounding_factor,") Coverage",sep=""), ylab = "Density",
					xlim=c(plot.min,plot.max), ylim=c(0,0.2), col=labelColors[i],
					   main = "Mean Junction Total CPM Distribution", lwd=2)
abline(v=0, col="green", lty="dashed")
abline(v=log2(0.6+rounding_factor), col="blue", lty="dashed")
dev.off()

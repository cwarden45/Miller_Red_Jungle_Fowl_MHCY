#setwd("R:\\mmiller\\Seq\\BAC_annotation\\latest_sequin_files-G3_submission\\Combined_Ref-v2\\Repeat_Analysis")

input.labels = c("Contig1","Contig2","Contig3","Contig4","MHCB")
seq.lengths = c(412374, 148501, 138921, 45013, 241833)
##NOTE: assumes output table has been imported into Excel, which separates out the columns correctly.
RepeatMasker_files = c("../../Contig1/scripts/RepeatMasker/Contig1.fasta.out.xlsx",
						"../../Contig2_58f18/scripts/RepeatMasker/Contig2.fasta.out.xlsx",
						"../../Contig3_34j16_rev/scripts/RepeatMasker/Contig3.fasta.out.xlsx",
						"../../Contig4_Fosmids/scripts/RepeatMasker/Contig4.fasta.out.xlsx",
						"../../../Code/BG2/MHCB-220328/scripts/RepeatMasker/AB268588.fasta.out.xlsx")
						
TRF_files = c("../../Contig1/scripts/TRF/Contig1.fasta.2.7.7.80.10.50.500.dat",
						"../../Contig2_58f18/scripts/TRF/Contig2.fasta.2.7.7.80.10.50.500.dat",
						"../../Contig3_34j16_rev/scripts/TRF/Contig3.fasta.2.7.7.80.10.50.500.dat",
						"../../Contig4_Fosmids/scripts/TRF/Contig4.fasta.2.7.7.80.10.50.500.dat",
						"../../../Code/BG2/MHCB-220328/scripts/TRF/AB268588.fasta.2.7.7.80.10.50.500.dat")

library("xlsx")
library("GenomicRanges")

#first, find total categories
specific.categories = c("Tandem Repeat (TRF-Only)", "Tandem Repeat (Both Methods)")						
for (i in 1:length(input.labels)){
	seq.name = input.labels[i]
	temp.table = read.xlsx(RepeatMasker_files[i], sheetIndex=1, head=F)
	temp.table = temp.table[-c(1:2),]
	
	temp.table$X11[temp.table$X11 == "Low_complexit"]="Low_complexity"
	
	specific.categories = union(specific.categories, paste(unique(temp.table$X11), " (RepeatMasker-Only)",sep=""))
}#end for (i in 1:length(input.labels))

general.category = rep("",length(specific.categories))
general.category[grep("^DNA\\/",specific.categories)]="Transposon, Class II (DNA Transposon)"
general.category[grep("^LINE\\/",specific.categories)]="Transposon, Class I (Retroelement)"
general.category[grep("^LTR\\/",specific.categories)]="Transposon, Class I (Retroelement)"
general.category[specific.categories == "rRNA (RepeatMasker-Only)"]="rRNA"
general.category[specific.categories == "tRNA (RepeatMasker-Only)"]="tRNA"
general.category[specific.categories == "Simple_repeat (RepeatMasker-Only)"]="Simple Repeat"
general.category[specific.categories == "Low_complexity (RepeatMasker-Only)"]="Low Complexity"
general.category[specific.categories == "Satellite (RepeatMasker-Only)"]="Satellite"
general.category[specific.categories == "Tandem Repeat (TRF-Only)"]="Tandem Repeat"
general.category[specific.categories == "Tandem Repeat (Both Methods)"]="Tandem Repeat"

#second, add counts
total_MHCY_length = 0
output.table = data.frame(General_Category=general.category, Specific_Repeat=specific.categories)
sep.MHCY.table = data.frame(General_Category=general.category, Specific_Repeat=specific.categories)
for (i in 1:length(input.labels)){
	seq.name = input.labels[i]
	print(seq.name)
	#RepeatMasker
	temp.table = read.xlsx(RepeatMasker_files[i], sheetIndex=1, head=F)
	temp.table = temp.table[-c(1:2),]
	
	temp.table$X6 = as.numeric(temp.table$X6)
	temp.table$X7 = as.numeric(temp.table$X7)
	repeat_length = temp.table$X7-temp.table$X6
	temp.table = data.frame(temp.table, repeat_length)
	
	temp.table$X11[temp.table$X11 == "Low_complexit"]="Low_complexity"
	temp.table$X11 = paste(temp.table$X11, " (RepeatMasker-Only)",sep="")
	
	rmID = paste(temp.table$X6,temp.table$X7,sep="-")
	
	#TRF
	temp.TRF.table = read.delim(TRF_files[i], head=F, sep=" ", skip=9)
	temp.TRF.table = temp.TRF.table[-1,]
	temp.TRF.table$V1 = as.numeric(temp.TRF.table$V1)
	temp.TRF.table$V2 = as.numeric(temp.TRF.table$V2)	
	TRF.repeat_length = temp.TRF.table$V2-temp.TRF.table$V1
	trfGR = GRanges(Rle(rep(seq.name,nrow(temp.TRF.table))),
				IRanges(start=temp.TRF.table$V1, end=temp.TRF.table$V2),
				Names=rep("Tandem Repeat (TRF-Only)",nrow(temp.TRF.table)))
	#I encountered problems with the TRF-only repeats being greater than 100%
	#print(trfGR)
	trfGR = reduce(trfGR)
	#print(trfGR)
	temp.TRF.table = data.frame(trfGR)
	temp.TRF.table = data.frame(temp.TRF.table, repeat.category = rep("Tandem Repeat (TRF-Only)",nrow(temp.TRF.table)))
	trfID = paste(temp.TRF.table$start,temp.TRF.table$end,sep="-")
	
	#find overlapping repeats (remove from RepeatMasker + revise TRF table)
	#code based upon https://github.com/cwarden45/peak_calling_template/blob/master/peak_statistics.R
	rmGR = GRanges(Rle(rep(seq.name,nrow(temp.table))),
				IRanges(start=temp.table$X6, end=temp.table$X7),
				Names=temp.table$X11)
	trfGR = GRanges(Rle(rep(seq.name,nrow(temp.TRF.table))),
				IRanges(start=temp.TRF.table$start, end=temp.TRF.table$end),
				Names=temp.TRF.table$repeat.category)
				
	hits = findOverlaps(rmGR, trfGR)
	overlaps = unique(rmGR[queryHits(hits)])
	overlaps.df = data.frame(overlaps)
	overlaps.ID = paste(overlaps.df$start, overlaps.df$end, sep="-")

	hits2 = findOverlaps(trfGR, rmGR)
	overlaps2 = unique(trfGR[queryHits(hits2)])
	overlaps2.df = data.frame(overlaps2)
	overlaps2.ID = paste(overlaps2.df$start, overlaps2.df$end, sep="-")

	print(dim(temp.table))
	overlap.rm.table = temp.table[match(overlaps.ID, rmID),]
	temp.table = temp.table[-match(overlaps.ID, rmID),]
	print(dim(temp.table))

	print(dim(temp.TRF.table))
	overlap.TRF.table =  temp.TRF.table[match(overlaps2.ID, trfID),]
	temp.TRF.table = temp.TRF.table[-match(overlaps2.ID, trfID),]
	print(dim(temp.TRF.table))
	overlap.rmGR = GRanges(Rle(rep(seq.name,nrow(overlap.rm.table))),
				IRanges(start=overlap.rm.table$X6, end=overlap.rm.table$X7),
				Names=overlap.rm.table$X11)
	overlap.trfGR = GRanges(Rle(rep(seq.name,nrow(overlap.TRF.table))),
				IRanges(start=overlap.TRF.table$start, end=overlap.TRF.table$end),
				Names=overlap.TRF.table$repeat.category)
	union.df = data.frame(union(overlap.rmGR, overlap.trfGR))
	new.TRF.table = data.frame(start=c(temp.TRF.table$start, union.df$start),
								end=c(temp.TRF.table$end, union.df$end),
								repeat_length=c(temp.TRF.table$width, union.df$width),
								repeat.category=c(temp.TRF.table$repeat.category, rep("Tandem Repeat (Both Methods)",nrow(union.df))))
	print(dim(new.TRF.table))
	
	#RepeatMasker-Only
	if (seq.name == "Contig1"){
		NOR.RM.table = temp.table[temp.table$X6 < 106161,]
		MHCY.RM.table = temp.table[temp.table$X6 >= 106161,]
		
		#NOR
		temp.count = table(NOR.RM.table$X11)
		temp.sum = tapply(NOR.RM.table$repeat_length, NOR.RM.table$X11, sum)
		temp.percent = round(100 * temp.sum / 106161, digits=2)
		
		temp.count = temp.count[match(specific.categories, names(temp.count))]
		temp.count[is.na(temp.count)]=0

		temp.sum = temp.sum[match(specific.categories, names(temp.sum))]
		temp.sum[is.na(temp.sum)]=0

		temp.percent = temp.percent[match(specific.categories, names(temp.percent))]
		temp.percent[is.na(temp.percent)]=0
		
		temp.out.table = data.frame(number = temp.count, total.length = temp.sum, percent.total.length = temp.percent)
		temp.out.table = temp.out.table[,-1]
		names(temp.out.table)=paste("NOR",names(temp.out.table),sep=".")
		
		output.table = data.frame(output.table, temp.out.table)
		
		#MHCY
		MHCY.length = seq.lengths[i]-106161
		total_MHCY_length = total_MHCY_length + MHCY.length

		temp.count = table(MHCY.RM.table$X11)
		temp.sum = tapply(MHCY.RM.table$repeat_length, MHCY.RM.table$X11, sum)
		temp.percent = round(100 * temp.sum / MHCY.length, digits=2)
		
		temp.count = temp.count[match(specific.categories, names(temp.count))]
		temp.count[is.na(temp.count)]=0

		temp.sum = temp.sum[match(specific.categories, names(temp.sum))]
		temp.sum[is.na(temp.sum)]=0

		temp.percent = temp.percent[match(specific.categories, names(temp.percent))]
		temp.percent[is.na(temp.percent)]=0
		
		temp.out.table = data.frame(number = temp.count, total.length = temp.sum, percent.total.length = temp.percent)
		temp.out.table = temp.out.table[,-1]
		names(temp.out.table)=paste(seq.name,names(temp.out.table),sep=".")

		sep.MHCY.table = data.frame(sep.MHCY.table, temp.out.table)
	}else if (seq.name == "MHCB"){
		temp.count = table(temp.table$X11)
		temp.sum = tapply(temp.table$repeat_length, temp.table$X11, sum)
		temp.percent = round(100 * temp.sum / seq.lengths[i], digits=2)
		
		temp.count = temp.count[match(specific.categories, names(temp.count))]
		temp.count[is.na(temp.count)]=0

		temp.sum = temp.sum[match(specific.categories, names(temp.sum))]
		temp.sum[is.na(temp.sum)]=0

		temp.percent = temp.percent[match(specific.categories, names(temp.percent))]
		temp.percent[is.na(temp.percent)]=0
		
		temp.out.table = data.frame(number = temp.count, total.length = temp.sum, percent.total.length = temp.percent)
		temp.out.table = temp.out.table[,-1]
		names(temp.out.table)=paste(seq.name,names(temp.out.table),sep=".")

		output.table = data.frame(output.table, temp.out.table)
	}else{
		total_MHCY_length = total_MHCY_length + seq.lengths[i]

		temp.count = table(temp.table$X11)
		temp.sum = tapply(temp.table$repeat_length, temp.table$X11, sum)
		temp.percent = round(100 * temp.sum / seq.lengths[i], digits=2)
		
		temp.count = temp.count[match(specific.categories, names(temp.count))]
		temp.count[is.na(temp.count)]=0

		temp.sum = temp.sum[match(specific.categories, names(temp.sum))]
		temp.sum[is.na(temp.sum)]=0

		temp.percent = temp.percent[match(specific.categories, names(temp.percent))]
		temp.percent[is.na(temp.percent)]=0
		
		temp.out.table = data.frame(number = temp.count, total.length = temp.sum, percent.total.length = temp.percent)
		temp.out.table = temp.out.table[,-1]
		names(temp.out.table)=paste(seq.name,names(temp.out.table),sep=".")
		
		sep.MHCY.table = data.frame(sep.MHCY.table, temp.out.table)
	}#end else

	#TRF-Only and TRF overlap
	if (seq.name == "Contig1"){
		NOR.TRF.table = new.TRF.table[new.TRF.table$start < 106161,]
		MHCY.TRF.table = new.TRF.table[new.TRF.table$start >= 106161,]
		
		#NOR
		temp.count = table(NOR.TRF.table$repeat.category)
		temp.sum = tapply(NOR.TRF.table$repeat_length, NOR.TRF.table$repeat.category, sum)
		temp.percent = round(100 * temp.sum / 106161, digits=2)
		
		col.index = match("NOR.number.Freq",names(output.table))
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (TRF-Only)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (TRF-Only)"]		
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (TRF-Only)"]		
		
		#MHCY
		temp.count = table(MHCY.TRF.table$repeat.category)
		temp.sum = tapply(MHCY.TRF.table$repeat_length, MHCY.TRF.table$repeat.category, sum)
		temp.percent = round(100 * temp.sum / MHCY.length, digits=2)

		col.index = match("Contig1.number.Freq",names(sep.MHCY.table))
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (TRF-Only)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (TRF-Only)"]		
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (TRF-Only)"]	
	}else if (seq.name == "MHCB"){
		temp.count = table(new.TRF.table$repeat.category)
		temp.sum = tapply(new.TRF.table$repeat_length, new.TRF.table$repeat.category, sum)
		temp.percent = round(100 * temp.sum / seq.lengths[i], digits=2)

		col.index = match("MHCB.number.Freq",names(output.table))
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (TRF-Only)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (TRF-Only)"]		
		output.table[output.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (Both Methods)"]
		output.table[output.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (TRF-Only)"]		
	}else{
		temp.count = table(new.TRF.table$repeat.category)
		temp.sum = tapply(new.TRF.table$repeat_length, new.TRF.table$repeat.category, sum)
		temp.percent = round(100 * temp.sum / seq.lengths[i], digits=2)

		col.index = match(paste(seq.name,".number.Freq",sep=""),names(sep.MHCY.table))
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index]=temp.count[names(temp.count) == "Tandem Repeat (TRF-Only)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+1]=temp.sum[names(temp.sum) == "Tandem Repeat (TRF-Only)"]		
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (Both Methods)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (Both Methods)"]
		sep.MHCY.table[sep.MHCY.table$Specific_Repeat == "Tandem Repeat (TRF-Only)",col.index+2]=temp.percent[names(temp.percent) == "Tandem Repeat (TRF-Only)"]	
	}#end else
}#end for (i in 1:length(input.labels))

#add separate MHCY values
MHCY.count.mat = sep.MHCY.table[,c(3,6,9,12)]
MHCY.length.mat = sep.MHCY.table[,c(4,7,10,13)]

MHCY.count.sum = apply(MHCY.count.mat, 1, sum)
MHCY.length.sum = apply(MHCY.length.mat, 1, sum)
MHCY.percent = round(100 * MHCY.length.sum / total_MHCY_length, digits=2)

temp.out.table = data.frame(number = MHCY.count.sum, total.length = MHCY.length.sum, percent.total.length = MHCY.percent)
names(temp.out.table)=paste("MHCY",names(temp.out.table),sep=".")

output.table = data.frame(output.table[,1:5], temp.out.table, output.table[,6:8])

write.table(sep.MHCY.table, "RepeatMasker_summary-separate_clones-v2.txt", quote=F, sep="\t", row.names=F)

png("RepeatMasker_summary-short-v2.png")
#overall
retro.table = output.table[grep("Transposon, Class I",output.table$General_Category),]
other.repeat.table = output.table[-match(retro.table$Specific_Repeat,output.table$Specific_Repeat),]
overall.mat = matrix(ncol=3,nrow=3)
colnames(overall.mat)=c("NOR","MHCY","MHCB")
rownames(overall.mat)=c("Retroelement","Other Repeat","No Repeat")
overall.mat[1,1]=sum(retro.table$NOR.percent.total.length)
overall.mat[2,1]=sum(other.repeat.table$NOR.percent.total.length)
overall.mat[3,1] = 100 - overall.mat[1,1] - overall.mat[2,1]
overall.mat[1,2]=sum(retro.table$MHCY.percent.total.length)
overall.mat[2,2]=sum(other.repeat.table$MHCY.percent.total.length)
overall.mat[3,2] = 100 - overall.mat[1,2] - overall.mat[2,2]
overall.mat[1,3]=sum(retro.table$MHCB.percent.total.length)
overall.mat[2,3]=sum(other.repeat.table$MHCB.percent.total.length)
overall.mat[3,3] = 100 - overall.mat[1,3] - overall.mat[2,3]
barplot(overall.mat, col=c("red","black","gray95"), ylab="Percentage", las=2, cex.names=1.5, cex.axis=1.4)
legend("top", legend=c("Other Repeat","Retroelement","No Repeat"), col=c("black","red","gray95"),
		xpd=T, inset = -0.1, ncol=3, pch=15, cex=1.1)
dev.off()

png("RepeatMasker_summary-separate_clones-v2.png")
#separate contigs
retro.table = sep.MHCY.table[grep("Transposon, Class I",sep.MHCY.table$General_Category),]
other.repeat.table = sep.MHCY.table[-match(retro.table$Specific_Repeat,sep.MHCY.table$Specific_Repeat),]
overall.mat = matrix(ncol=4,nrow=3)
colnames(overall.mat)=c("Contig1","Contig2","Contig3","Contig4")
rownames(overall.mat)=c("Retroelement","Other Repeat","No Repeat")
overall.mat[1,1]=sum(retro.table$Contig1.percent.total.length)
overall.mat[2,1]=sum(other.repeat.table$Contig1.percent.total.length)
overall.mat[3,1] = 100 - overall.mat[1,1] - overall.mat[2,1]
overall.mat[1,2]=sum(retro.table$Contig2.percent.total.length)
overall.mat[2,2]=sum(other.repeat.table$Contig2.percent.total.length)
overall.mat[3,2] = 100 - overall.mat[1,2] - overall.mat[2,2]
overall.mat[1,3]=sum(retro.table$Contig3.percent.total.length)
overall.mat[2,3]=sum(other.repeat.table$Contig3.percent.total.length)
overall.mat[3,3] = 100 - overall.mat[1,3] - overall.mat[2,3]
overall.mat[1,4]=sum(retro.table$Contig4.percent.total.length)
overall.mat[2,4]=sum(other.repeat.table$Contig4.percent.total.length)
overall.mat[3,4] = 100 - overall.mat[1,4] - overall.mat[2,4]
barplot(overall.mat, col=c("red","black","gray95"), ylab="Percentage", las=2, cex.names=1.5, cex.axis=1.4)
legend("top", legend=c("Other Repeat","Retroelement","No Repeat"), col=c("black","red","gray95"),
		xpd=T, inset = -0.1, ncol=3, pch=15, cex=1.1)
dev.off()

#calculate sums before export
Retroelement.table = output.table[output.table$General_Category == "Transposon, Class I (Retroelement)",]

Retroelement.sums = apply(Retroelement.table[,3:ncol(Retroelement.table)], 2, sum)
Total.sums = apply(output.table[,3:ncol(output.table)], 2, sum)

output.table = rbind(output.table, c("RETROELEMENT SUM","",Retroelement.sums))
output.table = rbind(output.table, c("TOTAL REPEAT SUM","",Total.sums))
write.table(output.table, "RepeatMasker_summary-short-v2.txt", quote=F, sep="\t", row.names=F)
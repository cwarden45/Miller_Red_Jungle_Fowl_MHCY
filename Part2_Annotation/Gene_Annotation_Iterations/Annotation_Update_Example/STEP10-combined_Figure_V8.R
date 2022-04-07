output="pdf"
contig.names = c("Contig1","Contig2","Contig3","Contig4")
contig.fas = c("Contig1.fasta",
				"Contig2.fasta",
				"Contig3.fasta",
				"Contig4.fasta")
track.width = 50000
track.names = c("rDNA", "MHCY class I","YLEC","MHCY2B","LENG9-like","OZF-like & ZNF ", "RepeatMasker", "TRF Repeats", "GC%")
ymaxes 		= c(0.79  ,      0.71     , 0.63 , 0.55   ,    0.47    ,      0.39      ,      0.31     ,     0.23     , 0.15 )
contig.info.files = c("Contig1_gene_summary.txt",
						"Contig2_gene_summary.txt",
						"Contig3_gene_summary.txt",
						"Contig4_gene_summary.txt")
gene.gtfs = c("Contig1_updated_genes.gtf",
				"Contig2_updated_genes.gtf",
				"Contig3_updated_genes.gtf",
				"Contig4_updated_genes.gtf")
RepeatMasker.tbls = c("../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/scripts/Repeat_Tables/Contig1_RepeatMasker_no_rRNA_no_merge.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/scripts/Repeat_Tables/Contig2_RepeatMasker_no_rRNA_no_merge.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/scripts/Repeat_Tables/Contig3_RepeatMasker_no_rRNA_no_merge.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/scripts/Repeat_Tables/Contig4_RepeatMasker_no_rRNA_no_merge.tbl")
TRF.tbls = c("../../BAC_annotation/latest_sequin_files-G3_submission/Contig1/scripts/Repeat_Tables/Contig1_TRF.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig2_58f18/scripts/Repeat_Tables/Contig2_TRF.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig3_34j16_rev/scripts/Repeat_Tables/Contig3_TRF.tbl",
						"../../BAC_annotation/latest_sequin_files-G3_submission/Contig4_Fosmids/scripts/Repeat_Tables/Contig4_TRF.tbl")
#title.shifts = c(0   , 0.07, 0.11, 0.4)
title.shifts = c(0   , 0.05, 0.08, 0.23)
txt.scales   = c(4	 , 4   , 4   , 4)
#gc.scales    = c(3 , 3 , 3 , 3)
gc.scales    = c(4 , 4 , 4 , 4)
#gc.shifts    = c(0.15, 0.15, 0.15, 0.15)
gc.shifts    = c(0.08, 0.08, 0.08, 0.08)

anno.buffer=0.02
anno.shift=0
track.shift=0.09
#track.shift=0
minor.tick.length = 10000
major.tick.length = 50000
				
library(Biostrings)
library('rtracklayer')

#extract length for layout
contig.lengths = c()
for (i in 1:length(contig.names)){
	seq.obj = readDNAStringSet(file = contig.fas[i])

	contig.seq = seq.obj[[contig.names[i]]]
	contig.lengths[i]=length(contig.seq)
}#for (i in 1:length(contig.names))

#add 50k bp for left-side label
blank.length = sum(contig.lengths[1])-sum(contig.lengths[-1])
total.width = contig.lengths[1]+track.width

layout.scale.width = 10000
scaled.row1 = round(c(track.width, contig.lengths[1]) / layout.scale.width)
scaled.row2 = round(c(track.width, contig.lengths[-1], blank.length) / layout.scale.width)
#manually set column numbers to be equal
scaled.row2[length(scaled.row2)]=scaled.row2[length(scaled.row2)]-1
print(sum(scaled.row1))
print(sum(scaled.row2))

layout.count = 0
layout.mat = c()
for (i in 1:length(scaled.row1)){
	layout.count=layout.count+1
	layout.mat=c(layout.mat, rep(layout.count,scaled.row1[i]))
}#end for (i in length(scaled.row1))
for (i in 1:length(scaled.row2)){
	layout.count=layout.count+1
	layout.mat=c(layout.mat, rep(layout.count,scaled.row2[i]))
}#end for (i in length(scaled.row2))
print(length(layout.mat))

plot.height=5
plot.scaled.width = total.width / 50000 * plot.height
if(output == "pdf"){
	pdf("Figure1b_Color-gc20to80.pdf", height=5*plot.height, width=plot.scaled.width)
}else if (output == "png"){
	png("Figure1b_Color-gc20to80.png", height=plot.height*100, width=plot.scaled.width*100)
}else{
	stop("Must set output to .pdf or .png")
}

layout.mat=matrix(layout.mat,
					ncol=sum(scaled.row1), byrow=TRUE)
layout(layout.mat)

### plot figures ###

#top row labels
#remove , new = TRUE to avoid error message?
par(mai=c(0,0,0,0),fig=c(0, track.width/total.width, 0.5,1))
plot(0, 0, axes=FALSE, xlim=0:1, ylim=0:1, xaxt="n",yaxt="n",xlab="",ylab="", col="white")
#rect(0,0,1,1)
for(i in 1:(length(track.names)-1)){
	label = track.names[i]
	ymax = ymaxes[i]
	
	text(0.5, ymax-0.05, label, xpd=T, cex=5, font=2)
}#end for(i in 1:length(track.names))
#GC is twice as large
text(0.5, ymaxes[length(track.names)]-0.1, track.names[length(track.names)], xpd=T, cex=5, font=2)
text(0.92,0.105,"80%",xpd=T,cex=4,font=1.5,xpd=T,col="gray20")
text(0.95, 0.05,"50%",xpd=T,cex=3,font=1.5,xpd=T,col="gray")
text(0.92,-0.01,"20%",xpd=T,cex=4,font=1.5,xpd=T,col="gray20")

#contig1
	#manually add to keep bottom row space that matches starting top row
	wiggle.room1 = 18000
	par(mai=c(0,0,0,0),fig=c((track.width-wiggle.room1)/total.width, 1, 0.5,1), new = TRUE)
	plot(0, 0, axes=FALSE, xlim=0:1, ylim=0:1, xaxt="n",yaxt="n",xlab="",ylab="", col="white")
	#rect(0,0,1,1)
	
	contig.name=contig.names[1]
	seq.obj = readDNAStringSet(file = contig.fas[1])
	contig.length=contig.lengths[1]
	contig.info.file = contig.info.files[1]
	gene.gtf = gene.gtfs[1]
	RepeatMasker.tbl = RepeatMasker.tbls[1]
	TRF.tbl = TRF.tbls[1]
	title.shift = title.shifts[1]
	txt.scale = txt.scales[1]
	gc.scale=gc.scales[1]
	gc.shift=gc.shifts[1]

	gene.obj = import(gene.gtf)
	gene.df = data.frame(gene.obj)
	print(dim(gene.df))
	gene.df = gene.df[grep("^RJF.Contig",gene.df$gene_id),]
	print(dim(gene.df))
	
	gene.start = tapply(gene.df$start,gene.df$gene_id,min)
	gene.end = tapply(gene.df$end,gene.df$gene_id,max)
	gene_id = names(gene.start)
	seqnames = gene.df$seqnames[1]
	gene.df = data.frame(seqnames, start=gene.start, end=gene.end, gene_id)
	rownames(gene.df)=1:nrow(gene.df)

	gene.df$gene_id = gsub("Ylec","YLEC",gene.df$gene_id)

		contig.info = read.table(contig.info.file, head=T, sep="\t")
		contig.info$Gene.Family = as.character(contig.info$Gene.Family)
		contig.info$Gene.Family[contig.info$Gene.Family == "CDS - YLbeta"]="CDS - YLBetaII"
		gene.type = rep(NA, nrow(gene.df))
		for (i in 1:nrow(gene.df)){
			gene.name = gene.df$gene_id[i]
			gene.type[i]=as.character(contig.info$Gene.Family[contig.info$Full.Name==gene.name])
		}#end for (i in 1:nrow(gene.df))
		gene.type=gsub(" - ",".",gene.type)
		gene.type[grep("LENG9L\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("MHCY2B\\d+P$",gene.df$gene_id)]="YLBetaII-P"
		gene.type[grep("ZNF\\d+P$",gene.df$gene_id)]="ZNF-P"
		print(table(gene.type))
		
		gene.df = data.frame(gene.df, gene.type)


	#rRNA gene track
	rRNA.df = gene.df[grep("RN",gene.df$gene_id),]

	#YF gene track
	YF.df = gene.df[grep("MHCY\\d+\\wP*$",gene.df$gene_id),]


	#YLec gene track
	YLec.df = gene.df[grep("YLEC",gene.df$gene_id),]

	#other gene track
	plotted.rows = c(rownames(rRNA.df),rownames(YF.df),rownames(YLec.df))
	other_gene.df = gene.df[-as.numeric(plotted.rows),]

	#RepeatMasker track
	RepeatMasker.table = read.delim(RepeatMasker.tbl, head=F, skip=1, sep="\t")
	print(dim(RepeatMasker.table))
	RepeatMasker.table=RepeatMasker.table[!is.na(RepeatMasker.table$V1),]
	print(dim(RepeatMasker.table))


	#TRF track
	TRF.table = read.delim(TRF.tbl, head=F, skip=1, sep="\t")
	print(dim(TRF.table))
	TRF.table=TRF.table[!is.na(TRF.table$V1),]
	print(dim(TRF.table))
	
	#use example from https://web.stanford.edu/class/bios221/labs/biostrings/lab_1_biostrings.html
	GC.df = data.frame(ID=names(seq.obj), GC=(alphabetFrequency(seq.obj)[, c(2,3)]/width(seq.obj))*100)

	gc.window = 10000
	gc.line = 100 * rowSums(letterFrequencyInSlidingView(DNAString(seq.obj[[1]]), gc.window, c("G", "C")))/gc.window
	
	genome.size.txt = paste(format(contig.length, big.mark=",")," bp",sep="")
	text(1-nchar(genome.size.txt)/(100 * txt.scale)-title.shift, 0.98, genome.size.txt, font=2,cex=txt.scale, xpd=T)

	#line for chromosome
	ref.center = 0.9
	segments(x0 = 0, y0=ref.center, x1 = 1, y1 = ref.center, lwd=4, xpd=T)
	#segments(x0 = 0, y0=ref.center-0.05, x1 = 0, y1 = ref.center+0.025, lwd=2, xpd=T)
	#segments(x0 = 1, y0=ref.center-0.05, x1 = 1, y1 = ref.center+0.025, lwd=2, xpd=T)
	ticks = 1:floor(contig.length/minor.tick.length) * minor.tick.length / contig.length
	segments(x0 = ticks, x1 = ticks,
				y0=rep(ref.center,length(ticks)), y1 = rep(ref.center+0.0075,length(ticks)), lwd=1, xpd=T)
	ticks = 1:floor(contig.length/major.tick.length) * major.tick.length / contig.length
	segments(x0 = ticks, x1 = ticks,
				y0=rep(ref.center,length(ticks)), y1 = rep(ref.center+0.03,length(ticks)), lwd=1, xpd=T)
	if(contig.length > major.tick.length){
		kb.text = 1:floor(contig.length/major.tick.length) * major.tick.length / 1000
		text(ticks, rep(ref.center-0.05, length(ticks)), paste(kb.text, "kb"), cex=txt.scale, font=2)
	}#end if(contig.length > major.tick.length )

	#rRNA
	ymax = ymaxes[1]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	if(nrow(rRNA.df) > 0){
		scaled.start = rRNA.df$start / contig.length
		scaled.stop = rRNA.df$end / contig.length
		rect(xleft=scaled.start, xright=scaled.stop,
				ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="red", border="red")
	}#end if(nrow(rRNA.df) > 0)

	#YF Genes
	ymax = ymaxes[2]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	rect.color = rep("darkgreen",nrow(YF.df))
	rect.color[YF.df$gene.type == "pseudogene"]="grey50"

	scaled.start = YF.df$start / contig.length
	scaled.stop = YF.df$end / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=rect.color, border=rect.color)

	#YLec Genes
	ymax = ymaxes[3]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	rect.color = rep("blue",nrow(YF.df))
	rect.color[YLec.df$gene.type == "pseudogene"]="grey50"

	scaled.start = YLec.df$start / contig.length
	scaled.stop = YLec.df$end / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=rect.color, border=rect.color)

	#Other Genes
	ymax = ymaxes[4]#YLBII
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	ymax = ymaxes[5]#LENG
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	ymax = ymaxes[6]#ZNF
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	if(nrow(other_gene.df) > 0){
		gene.types = unique(other_gene.df$gene.type)
		for (specific.type in gene.types){
			print(specific.type)
			temp.table = other_gene.df[other_gene.df$gene.type == specific.type,]
			
			if(specific.type == "CDS.YLBetaII"){
				gene.color = "maroon"
				ymax = ymaxes[4]
			}else if(specific.type == "CDS.LENG9"){
				gene.color = "orange"
				ymax = ymaxes[5]
			}else if(specific.type == "CDS.ZNF"){
				gene.color = "purple"
				ymax = ymaxes[6]
			}else if(specific.type == "CDS.OZFL"){
				gene.color = "cyan"
				ymax = ymaxes[6]
			}else if(specific.type == "YLBetaII-P"){
				gene.color = "grey50"
				ymax = ymaxes[4]
			}else if(specific.type == "LENG9-P"){
				gene.color = "grey50"
				ymax = ymaxes[5]
			}else if(specific.type == "ZNF-P"){
				gene.color = "grey50"
				ymax = ymaxes[6]
			}else{
				print(paste("Define color for ",specific.type,sep=""))
				stop()
			}
			print(gene.color)

			scaled.start = temp.table$start / contig.length
			scaled.stop = temp.table$end / contig.length
			rect(xleft=scaled.start, xright=scaled.stop,
					ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=gene.color, border=gene.color)		

					}#end for (specific.type in gene.types)
	}#end if(nrow(other_gene.df.df) > 0)

	#LENG9-like Genes
	ymax = ymaxes[6]

	#RepeatMasker Repeats
	ymax = ymaxes[7]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	scaled.start = RepeatMasker.table$V1 / contig.length
	scaled.stop = RepeatMasker.table$V2 / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="grey20",border="grey20")

	#TRF Repeats
	ymax = ymaxes[8]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	scaled.start = TRF.table$V1 / contig.length
	scaled.stop = TRF.table$V2 / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="grey20",border="grey20")

	#percent GC
	gc20=20/(gc.scale * 100)-gc.shift
	gc40=40/(gc.scale * 100)-gc.shift
	gc50=50/(gc.scale * 100)-gc.shift
	gc60=60/(gc.scale * 100)-gc.shift
	gc80=80/(gc.scale * 100)-gc.shift
	lines(1:length(gc.line)/length(gc.line), gc.line/(gc.scale * 100)-gc.shift, xpd=T,
			col="gray", lwd=3)
	rect(xleft=0, ybottom=gc20, xright=1, ytop=gc80, xpd=T)
	lines(c(0,1), c(gc50,gc50), xpd=T,
			col="gray",lty=5, lwd=2)
				
#bottom row labels
par(mai=c(0,0,0,0),fig=c(0, track.width/total.width, 0,0.5), new = TRUE)
plot(0, 0, axes=FALSE, xlim=0:1, ylim=0:1, xaxt="n",yaxt="n",xlab="",ylab="", col="white")
for(i in 1:(length(track.names)-1)){
	label = track.names[i]
	ymax = ymaxes[i]
	
	text(0.5, ymax-0.05, label, xpd=T, cex=5, font=2)
}#end for(i in 1:length(track.names))
#GC is twice as large
text(0.5, ymaxes[length(track.names)]-0.1, track.names[length(track.names)], xpd=T, cex=5, font=2)
text(0.92,0.105,"80%",xpd=T,cex=4,font=1.5,xpd=T,col="gray20")
text(0.95, 0.05,"50%",xpd=T,cex=3,font=1.5,xpd=T,col="gray")
text(0.92,-0.01,"20%",xpd=T,cex=4,font=1.5,xpd=T,col="gray20")

#other contigs
wiggle.room2 = 6500 #add some extra space, since I'm having issues with setting different margins
left.length = track.width - wiggle.room2
for (i in 2:length(contig.names)){
	contig.length=contig.lengths[i]
	scaled.start = left.length/total.width
	scaled.stop = scaled.start + contig.length/total.width
	left.length = left.length + contig.length
	par(mai=c(0,0,0,0),fig=c(scaled.start, scaled.stop, 0,0.5), new = TRUE)
	plot(0, 0, axes=FALSE, xlim=0:1, ylim=0:1, xaxt="n",yaxt="n",xlab="",ylab="", col="white")

	contig.name=contig.names[i]
	seq.obj = readDNAStringSet(file = contig.fas[i])
	contig.info.file = contig.info.files[i]
	gene.gtf = gene.gtfs[i]
	RepeatMasker.tbl = RepeatMasker.tbls[i]
	TRF.tbl = TRF.tbls[i]
	title.shift = title.shifts[i]
	txt.scale = txt.scales[i]
	gc.scale=gc.scales[i]
	gc.shift=gc.shifts[i]

	gene.obj = import(gene.gtf)
	gene.df = data.frame(gene.obj)

	gene.start = tapply(gene.df$start,gene.df$gene_id,min)
	gene.end = tapply(gene.df$end,gene.df$gene_id,max)
	gene_id = names(gene.start)
	seqnames = gene.df$seqnames[1]
	gene.df = data.frame(seqnames, start=gene.start, end=gene.end, gene_id)
	rownames(gene.df)=1:nrow(gene.df)

	gene.df$gene_id = gsub("Ylec","YLEC",gene.df$gene_id)

	if(contig.name == "Contig4"){
		gene.type = rep(NA,nrow(gene.df))
		gene.type[grep("MHCY",gene.df$gene_id)]="CDS.MHCY"
		gene.type[grep("YLEC",gene.df$gene_id)]="CDS.YLEC"
		gene.type[grep("P$",gene.df$gene_id)]="pseudogene"
		gene.type[grep("LENG\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("LENG9L\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("YLbeta\\d+P$",gene.df$gene_id)]="YLBetaII-P"
		gene.type[grep("ZNF\\d+P$",gene.df$gene_id)]="ZNF-P"
		print(table(gene.type))
		print(gene.df$gene_id[gene.type == "pseudogene"])#check that they are all YF or YLec
		
		gene.df = data.frame(gene.df, gene.type)
	}else{
		contig.info = read.table(contig.info.file, head=T, sep="\t")
		contig.info$Gene.Family = as.character(contig.info$Gene.Family)
		contig.info$Gene.Family[contig.info$Gene.Family == "CDS - YLbeta"]="CDS - YLBetaII"
		gene.type = rep(NA, nrow(gene.df))
		for (j in 1:nrow(gene.df)){
			gene.name = gene.df$gene_id[j]
			gene.type[j]=as.character(contig.info$Gene.Family[contig.info$Full.Name==gene.name])
		}#end for (j in 1:nrow(gene.df))
		gene.type=gsub(" - ",".",gene.type)
		gene.type[grep("LENG_\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("LENG9_\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("LENG9L\\d+P$",gene.df$gene_id)]="LENG9-P"
		gene.type[grep("MHCY2B\\d+P$",gene.df$gene_id)]="YLBetaII-P"
		gene.type[grep("ZNF\\d+P$",gene.df$gene_id)]="ZNF-P"
		print(table(gene.type))
		print(gene.df$gene_id[gene.type == "pseudogene"])#check that they are all YF or YLec

		gene.df = data.frame(gene.df, gene.type)
	}

	#rRNA gene track
	rRNA.df = gene.df[grep("RN",gene.df$gene_id),]

	#YF gene track
	YF.df = gene.df[grep("MHCY\\d+\\wP*$",gene.df$gene_id),]


	#YLec gene track
	YLec.df = gene.df[grep("YLEC",gene.df$gene_id),]

	#other gene track
	plotted.rows = c(rownames(rRNA.df),rownames(YF.df),rownames(YLec.df))
	other_gene.df = gene.df[-as.numeric(plotted.rows),]

	#RepeatMasker track
	RepeatMasker.table = read.delim(RepeatMasker.tbl, head=F, skip=1, sep="\t")
	print(dim(RepeatMasker.table))
	RepeatMasker.table=RepeatMasker.table[!is.na(RepeatMasker.table$V1),]
	print(dim(RepeatMasker.table))


	#TRF track
	TRF.table = read.delim(TRF.tbl, head=F, skip=1, sep="\t")
	print(dim(TRF.table))
	TRF.table=TRF.table[!is.na(TRF.table$V1),]
	print(dim(TRF.table))
	
	#use example from https://web.stanford.edu/class/bios221/labs/biostrings/lab_1_biostrings.html
	GC.df = data.frame(ID=names(seq.obj), GC=(alphabetFrequency(seq.obj)[, c(2,3)]/width(seq.obj))*100)

	gc.window = 10000
	gc.line = 100 * rowSums(letterFrequencyInSlidingView(DNAString(seq.obj[[1]]), gc.window, c("G", "C")))/gc.window

	genome.size.txt = paste(format(contig.length, big.mark=",")," bp",sep="")
	text(1-nchar(genome.size.txt)/(100 * txt.scale)-title.shift, 0.98, genome.size.txt, font=2,cex=txt.scale, xpd=T)

	#line for chromosome
	ref.center = 0.9
	segments(x0 = 0, y0=ref.center, x1 = 1, y1 = ref.center, lwd=4, xpd=T)
	#segments(x0 = 0, y0=ref.center-0.05, x1 = 0, y1 = ref.center+0.025, lwd=2, xpd=T)
	#segments(x0 = 1, y0=ref.center-0.05, x1 = 1, y1 = ref.center+0.025, lwd=2, xpd=T)
	ticks = 1:floor(contig.length/minor.tick.length) * minor.tick.length / contig.length
	segments(x0 = ticks, x1 = ticks,
				y0=rep(ref.center,length(ticks)), y1 = rep(ref.center+0.0075,length(ticks)), lwd=1, xpd=T)
	ticks = 1:floor(contig.length/major.tick.length) * major.tick.length / contig.length
	segments(x0 = ticks, x1 = ticks,
				y0=rep(ref.center,length(ticks)), y1 = rep(ref.center+0.03,length(ticks)), lwd=1, xpd=T)
	if(contig.length > major.tick.length){
		kb.text = 1:floor(contig.length/major.tick.length) * major.tick.length / 1000
		text(ticks, rep(ref.center-0.05, length(ticks)), paste(kb.text, "kb"), cex=txt.scale, font=2)
	}#end if(contig.length > major.tick.length )

	#rRNA
	ymax = ymaxes[1]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	if(nrow(rRNA.df) > 0){
		scaled.start = rRNA.df$start / contig.length
		scaled.stop = rRNA.df$end / contig.length
		rect(xleft=scaled.start, xright=scaled.stop,
				ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="grey", border="grey")
	}#end if(nrow(rRNA.df) > 0)

	#YF Genes
	ymax = ymaxes[2]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	rect.color = rep("darkgreen",nrow(YF.df))
	rect.color[YF.df$gene.type == "pseudogene"]="grey50"

	scaled.start = YF.df$start / contig.length
	scaled.stop = YF.df$end / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=rect.color, border=rect.color)

	#YLec Genes
	ymax = ymaxes[3]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	rect.color = rep("blue",nrow(YLec.df))
	rect.color[YLec.df$gene.type == "pseudogene"]="grey50"

	scaled.start = YLec.df$start / contig.length
	scaled.stop = YLec.df$end / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=rect.color, border=rect.color)

	
	#Other Genes
	ymax = ymaxes[4]#YLBII
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	ymax = ymaxes[5]#LENG
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	ymax = ymaxes[6]#ZNF
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	if(nrow(other_gene.df) > 0){
		gene.types = unique(other_gene.df$gene.type)
		for (specific.type in gene.types){
			print(specific.type)
			temp.table = other_gene.df[other_gene.df$gene.type == specific.type,]
			
			if(specific.type == "CDS.YLBetaII"){
				gene.color = "maroon"
				ymax = ymaxes[4]
			}else if(specific.type == "CDS.LENG9"){
				gene.color = "orange"
				ymax = ymaxes[5]
			}else if(specific.type == "CDS.ZNF"){
				gene.color = "purple"
				ymax = ymaxes[6]
			}else if(specific.type == "YLBetaII-P"){
				gene.color = "grey50"
				ymax = ymaxes[4]
			}else if(specific.type == "LENG9-P"){
				gene.color = "grey50"
				ymax = ymaxes[5]
			}else if(specific.type == "ZNF-P"){
				gene.color = "grey50"
				ymax = ymaxes[6]
			}else{
				print(paste("Define color for ",specific.type,sep=""))
				stop()
			}
			print(gene.color)

			scaled.start = temp.table$start / contig.length
			scaled.stop = temp.table$end / contig.length
			rect(xleft=scaled.start, xright=scaled.stop,
					ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col=gene.color, border=gene.color)		

					}#end for (specific.type in gene.types)
	}#end if(nrow(other_gene.df.df) > 0)

	#RepeatMasker Repeats
	ymax = ymaxes[7]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)
	scaled.start = RepeatMasker.table$V1 / contig.length
	scaled.stop = RepeatMasker.table$V2 / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="grey20",border="grey20")

	#TRF Repeats
	ymax = ymaxes[8]
	rect(xleft=0, ybottom=ymax-track.shift, xright=1, ytop=ymax)

	scaled.start = TRF.table$V1 / contig.length
	scaled.stop = TRF.table$V2 / contig.length
	rect(xleft=scaled.start, xright=scaled.stop,
			ybottom=ymax-track.shift+anno.buffer-anno.shift, ytop=ymax-anno.buffer-anno.shift, col="grey20",border="grey20")

	#percent GC
	gc20=20/(gc.scale * 100)-gc.shift
	gc40=40/(gc.scale * 100)-gc.shift
	gc50=50/(gc.scale * 100)-gc.shift
	gc60=60/(gc.scale * 100)-gc.shift
	gc80=80/(gc.scale * 100)-gc.shift
	lines(1:length(gc.line)/length(gc.line), gc.line/(gc.scale * 100)-gc.shift, xpd=T,
			col="gray", lwd=3)
	rect(xleft=0, ybottom=gc20, xright=1, ytop=gc80, xpd=T)
	lines(c(0,1), c(gc50,gc50), xpd=T,
			col="gray",lty=5, lwd=2)
}#end for (i in 2:length(contig.names))

#plot legend
scaled.start = left.length/total.width
par(mai=c(0,0,0,0),fig=c(scaled.start, 1, 0,0.5), new = TRUE)
plot(0, 0, axes=FALSE, xlim=0:1, ylim=0:1, xaxt="n",yaxt="n",xlab="",ylab="", col="white")
legend.cats = c("rDNA","MHCY class I" ,"YLEC","MHCY2B","LENG9-like","OZF-like",   "ZNF","Pseudogene",     "","Repeat")
legend.colors = c("red",   "darkgreen","blue","maroon",    "orange",   "cyan","purple","gray50"    ,"white","black")  
legend("center",legend=legend.cats,col=legend.colors,title="Gene Types",
		pch=15, ncol=1, cex=5, xpd=TRUE)

dev.off()

#print(par()$mar)
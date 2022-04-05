
SAMPLEID="Canu-v1.5-Arrow_102b15-rearranged--extra_12bp-Arrow-2x"
LABEL="102b15"

input.file = paste(SAMPLEID,"/aligned_reads.all.pileup",sep="")
output.file = paste(SAMPLEID,"/aligned_reads.all.pileup-coverage.png",sep="")

print("Reading .pileup file...")
pileup.table = read.delim(input.file, head=F, sep="\t", quote = "")
pileup.pos = pileup.table$V2
pileup.total.count = pileup.table$V4

	plot.position = 1:max(pileup.pos)
	plot.coverage = pileup.total.count[match(plot.position, pileup.pos)]
	plot.coverage[is.na(plot.coverage)] = 0

	png(output.file)
	plot(plot.position, plot.coverage, type="n", axes=FALSE,
			ylab="Coverage", xlab="Genomic Position",
			main=LABEL, cex.main=2)
	lines(plot.position, plot.coverage, type="l")
	axis(1)
	axis(2)
	box()
	dev.off()

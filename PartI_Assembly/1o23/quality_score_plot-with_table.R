#setwd("R:\\mmiller\\Seq\\BAC_annotation\\Code\\1o23\\revise_Canu_v2_1")

sampleID = "1o23"
yellow_thresh=88
red_thresh=50
FQ_in="Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC/arrow_consensus.fastq"
output.image="Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC/arrow_consensus-qual.png"
output.text="Canu-v2.1-Arrow_1o23-trimmed--extra_12bp_expectedBAC/arrow_consensus-qual.txt"

#a portion of this code was copied over and modified from another lab's project

FQ_lines = readLines(FQ_in)

qualASCII = unlist(strsplit(FQ_lines[4],split=""))
xmax = length(qualASCII)

pos = 1:xmax

#used to help with conversion: https://stackoverflow.com/questions/23123314/converting-ascii-number-to-strings-in-r

qualScore = function(char){
	numValue = strtoi(charToRaw(char),16L)
	return(numValue - 33)
}#end def qualScore

qual = sapply(qualASCII, qualScore)


png(output.image)
plot(pos, qual, type="n", axes=FALSE,
	ylim=c(0,100), ylab="Quality Score / Confidence",
	xlab="Position", main=sampleID, cex.main=2)
rect(0,-10,xmax,red_thresh,border="red",col="red")
rect(0,red_thresh,xmax,yellow_thresh,border="yellow",col="yellow")
rect(0,yellow_thresh,xmax,100,border="green",col="green")
lines(pos, qual, type="l")
axis(1)
axis(2)
box()
dev.off()

output.table = data.frame(Position=pos,Confidence=qual)
write.table(output.table, output.text, row.names=F, sep="\t", quote=F)
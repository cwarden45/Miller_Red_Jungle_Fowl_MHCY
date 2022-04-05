compID = "102b15_revision"
yname = "Canu v1.5 (early)"
ymax = 117788
xname = "102b15"
xmax = 102137
backbone1 = c(62944, 73628)

###edit code above this line ###

plot.max = max(xmax,ymax)

forward.line.file = paste(compID,".fplot",sep="")
reverse.line.file = paste(compID,".rplot",sep="")

forward.line.table = read.table(forward.line.file, head=F, sep=" ")
forward.line.table = forward.line.table[-c(1,2),]
reverse.line.table = read.table(reverse.line.file, head=F, sep=" ")
reverse.line.table = read.table(reverse.line.file, head=F, sep=" ")
reverse.line.table = reverse.line.table[-c(1,2),]

png(paste(compID,"_Rplot.png",sep=""))
par(mar = par("mar") + c(5,4,0,0))
plot(0, 0, axes=FALSE, ylim=c(0,plot.max), xlim=c(0,plot.max),
				ylab="", xlab="", main="Finalized vs Early Assembly", cex.main=1.5)

#contig size
lines(c(0,xmax),c(0,0), col="black", lwd=3)
lines(c(0,0),c(0,ymax), col="black", lwd=3)
				
#forward file
forward.pair.count = nrow(forward.line.table)/2

for (i in 1:forward.pair.count){
	start.row = as.numeric(forward.line.table[2*i-1,])
	stop.row = as.numeric(forward.line.table[2*i,])
	
	points(c(start.row[1],stop.row[1]),c(start.row[2],stop.row[2]), col="red", pch=19, cex=0.4)
	lines(c(start.row[1],stop.row[1]),c(start.row[2],stop.row[2]), col="red", type="l",lwd=2)
}#end for (1 in 1:forward.pair.count)

#reverse file
reverse.pair.count = nrow(reverse.line.table)/2

for (i in 1:reverse.pair.count){
	start.row = as.numeric(reverse.line.table[2*i-1,])
	stop.row = as.numeric(reverse.line.table[2*i,])
	
	points(c(start.row[1],stop.row[1]),c(start.row[2],stop.row[2]), col="blue", pch=19, cex=0.2)
	lines(c(start.row[1],stop.row[1]),c(start.row[2],stop.row[2]), col="blue", type="l",lwd=1)
}#end for (1 in 1:reverse.pair.count)

x.intervals = 50000*round(0:(xmax/50000))
axis(1,x.intervals, las=2)
y.intervals = 50000*ceiling(0:(ymax/50000))
axis(2, y.intervals, las=2)
mtext(xname, 1, padj=5, cex=1.5)
mtext(yname, 2, padj=-5, cex=1.5)
#box()

#refresh my memory on how to make transparent colors using https://www.dataanalytics.org.uk/make-transparent-colors-in-r/
rect(0,backbone1[1],xmax,backbone1[2],col=rgb(0.2, 0.2, 0.2, alpha = 0.2))
legend("bottom", "BAC backbone",
			pch=15, col=rgb(0.2, 0.2, 0.2, alpha = 0.2),
			xpd=T, inset = -0.5)
dev.off()
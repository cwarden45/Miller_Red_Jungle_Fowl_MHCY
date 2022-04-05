#used https://stackoverflow.com/questions/4785657/how-to-draw-an-empty-plot as a reminder

png("Contig1_BLAST_matches.png",width = 500, height = 200)
par(mar=c(1,1,1,1))
plot(1, type="n", xlab="", ylab="",
		axes=FALSE,ann=FALSE,
		xlim=c(0, 450000), ylim=c(0, 2.5))
		
text(65000,0.4, "Contig1 (412,374 bp)",
			font=2, col="blue")
lines(c(1,412374), c(0,0), lwd=3, col="blue")

text(65000,1.15, "190M (253,430 bp)",
			font=2, col="black", cex=0.8)
lines(c(1,253435), c(1,1), lwd=2, col="black")

text(253430+75000,1.05, "19d16 (158,945 bp)",
			font=2, col="black", cex=0.8)
lines(c(253430,412374), c(0.9,0.9), lwd=2, col="black")

text(121017+65000,1.3+0.15, "173o1 (221,406 bp)",
			font=2, col="black", cex=0.8)
lines(c(121017,342428), c(1.3,1.3), lwd=2, col="black")

text(50438-10397+55000,1.75, "102b15 (102,137 bp)",
			font=2, col="black", cex=0.8)
lines(c(50438-10397,141762), c(1.6,1.6), lwd=1, col="darkgray")
lines(c(50438,74628), c(1.6,1.6), lwd=2, col="darkgray")
lines(c(76617,141762), c(1.6,1.6), lwd=2, col="black")

text(67141-9754+55000,2.05, "1o23 (77,997 bp)",
			font=2, col="black", cex=0.8)
lines(c(67141-9754,135103), c(1.9,1.9), lwd=1, col="darkgray")
lines(c(67141,72734), c(1.9,1.9), lwd=2, col="darkgray")
lines(c(74618,135103), c(1.9,1.9), lwd=2, col="black")

dev.off()
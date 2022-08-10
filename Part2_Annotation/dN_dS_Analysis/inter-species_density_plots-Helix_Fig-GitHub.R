#setwd("R:\\mmiller\\Seq\\BAC_annotation\\G3_Revision\\GitHub_Upload\\dN_dS_Analysis")

chick_name = "MHCYa-like + MHCYd-like"
chick_color = "red"
human.alpha1_helix.in = "IMGT_HLA-AlphaHelix-n25/GenBank-alpha1_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
chicken.alpha1_helix.in = "Chicken_AlphaHelix-MHCYad_like-n6/alpha1_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
human.alpha2_helix.in = "IMGT_HLA-AlphaHelix-n25/GenBank-alpha2_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
chicken.alpha2_helix.in = "Chicken_AlphaHelix-MHCYad_like-n6/alpha2_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
human.non_helix.in = "IMGT_HLA-AlphaHelix-n25/GenBank-alpha1alpha2_NOThelix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
chicken.non_helix.in = "Chicken_AlphaHelix-MHCYad_like-n6/alpha1alpha2_NOThelix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
density.out = "IMGT_GenBank25-MHCYad_like-HelixFig.dN_dS.Bitarello_codeml-n6.pdf"
ploty_max3 = 4.5

human.alpha1_helix.pairwise = read.table(human.alpha1_helix.in, head=T, sep="\t")
chicken.alpha1_helix.pairwise = read.table(chicken.alpha1_helix.in, head=T, sep="\t")

human.alpha2_helix.pairwise = read.table(human.alpha2_helix.in, head=T, sep="\t")
chicken.alpha2_helix.pairwise = read.table(chicken.alpha2_helix.in, head=T, sep="\t")

human.non_helix.pairwise = read.table(human.non_helix.in, head=T, sep="\t")
chicken.non_helix.pairwise = read.table(chicken.non_helix.in, head=T, sep="\t")

#test ploting with max dN/dS equal to 3
human.alpha1_helix.dN_dS.3 = human.alpha1_helix.pairwise$pair_dN_dS
human.alpha1_helix.dN_dS.3[human.alpha1_helix.dN_dS.3 > 3] = 3
chicken.alpha1_helix.dN_dS.3 = chicken.alpha1_helix.pairwise$pair_dN_dS
chicken.alpha1_helix.dN_dS.3[chicken.alpha1_helix.dN_dS.3> 3] = 3

human.alpha2_helix.dN_dS.3 = human.alpha2_helix.pairwise$pair_dN_dS
human.alpha2_helix.dN_dS.3[human.alpha2_helix.dN_dS.3 > 3] = 3
chicken.alpha2_helix.dN_dS.3 = chicken.alpha2_helix.pairwise$pair_dN_dS
chicken.alpha2_helix.dN_dS.3[chicken.alpha2_helix.dN_dS.3> 3] = 3

human.non_helix.dN_dS.3 = human.non_helix.pairwise$pair_dN_dS
human.non_helix.dN_dS.3[human.non_helix.dN_dS.3 > 3] = 3
chicken.non_helix.dN_dS.3 = chicken.non_helix.pairwise$pair_dN_dS
chicken.non_helix.dN_dS.3[chicken.non_helix.dN_dS.3> 3] = 3

pdf(density.out, width=24, height=8)
par(mfcol=c(1,3), mar=c(5,5,5,5))
#alpha1 helix
den = density(human.alpha1_helix.dN_dS.3, na.rm=T,from=0, to=3)
plot(den$x, den$y, type="l", xlab = "dN/dS (define maximum value as dN/dS = 3)", ylab = "Density",
			xlim=c(0,3), ylim=c(0,ploty_max3), col="darkgreen", lwd=2,
			main = expression(paste(alpha,"1 helix",sep="")),
			cex.main=3, font.main=2, cex.lab=2, cex.axis=2)
legend("topright",legend=c(chick_name,"HLA-A + HLA-B"),
			col=c(chick_color,"darkgreen"),  lwd=2, cex=1.9)
			
den = density(chicken.alpha1_helix.dN_dS.3, na.rm=T,from=0, to=3)
lines(den$x, den$y, type="l", col=chick_color, lwd=2)

abline(v=1, col="gray", lwd=2, lty = 2)

#alpha2 helix
den = density(human.alpha2_helix.dN_dS.3, na.rm=T,from=0, to=3)
plot(den$x, den$y, type="l", xlab = "dN/dS (define maximum value as dN/dS = 3)", ylab = "Density",
			xlim=c(0,3), ylim=c(0,ploty_max3), col="darkgreen", lwd=2,
			main = expression(paste(alpha,"2 helix",sep="")),
			cex.main=3, font.main=2, cex.lab=2, cex.axis=2)
legend("topright",legend=c(chick_name,"HLA-A + HLA-B"),
			col=c(chick_color,"darkgreen"),  lwd=2, cex=1.9)
			
den = density(chicken.alpha2_helix.dN_dS.3, na.rm=T,from=0, to=3)
lines(den$x, den$y, type="l", col=chick_color, lwd=2)

abline(v=1, col="gray", lwd=2, lty = 2)

#non-helix
den = density(human.non_helix.dN_dS.3, na.rm=T,from=0, to=3)
plot(den$x, den$y, type="l", xlab = "dN/dS (define maximum value as dN/dS = 3)", ylab = "Density",
			xlim=c(0,3), ylim=c(0,ploty_max3), col="darkgreen", lwd=2,
			main = expression(paste("Non-Helical ",alpha,"1+",alpha,"2",sep="")),
			cex.main=3, font.main=2, cex.lab=2, cex.axis=2)
legend("topright",legend=c(chick_name,"HLA-A + HLA-B"),
			col=c(chick_color,"darkgreen"),  lwd=2, cex=1.9)
			
den = density(chicken.non_helix.dN_dS.3, na.rm=T,from=0, to=3)
lines(den$x, den$y, type="l", col=chick_color, lwd=2)

abline(v=1, col="gray", lwd=2, lty = 2)
dev.off()

print(wilcox.test(human.alpha1_helix.dN_dS.3, chicken.alpha1_helix.dN_dS.3))
print(wilcox.test(human.alpha2_helix.dN_dS.3, chicken.alpha2_helix.dN_dS.3))
print(wilcox.test(human.non_helix.dN_dS.3, chicken.non_helix.dN_dS.3))

print(ks.test(human.alpha1_helix.dN_dS.3, chicken.alpha1_helix.dN_dS.3))
print(ks.test(human.alpha2_helix.dN_dS.3, chicken.alpha2_helix.dN_dS.3))
print(ks.test(human.non_helix.dN_dS.3, chicken.non_helix.dN_dS.3))
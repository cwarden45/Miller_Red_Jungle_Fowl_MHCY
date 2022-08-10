library("gplots")

dN.in = "Bitarello_codeml-alpha1-helix/2NG.dN.txt"
dS.in = "Bitarello_codeml-alpha1-helix/2NG.dS.txt"
dN_dS.out = "alpha1_helix.dN_dS.Bitarello_codeml.txt"
dN_dS.paired.out = "alpha1_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"
 
#dN.in = "Bitarello_codeml-alpha2-helix/2NG.dN.txt"
#dS.in = "Bitarello_codeml-alpha2-helix/2NG.dS.txt"
#dN_dS.out = "alpha2_helix.dN_dS.Bitarello_codeml.txt"
#dN_dS.paired.out = "alpha2_helix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"

#dN.in = "Bitarello_codeml-nonAlphaHelices/2NG.dN.txt"
#dS.in = "Bitarello_codeml-nonAlphaHelices/2NG.dS.txt"
#dN_dS.out = "alpha1alpha2_NOThelix.dN_dS.Bitarello_codeml.txt"
#dN_dS.paired.out = "alpha1alpha2_NOThelix.dN_dS.Bitarello_codeml-PAIRWISE_EXPORT.txt"

pair_gene1 =c()
pair_gene2 =c()
pair_dN =c()
pair_dS =c()
pair_dN_dS =c()

#follow import examples: https://stackoverflow.com/questions/13863569/reading-a-symmetric-matrix-from-file-that-omits-upper-triangular-part

reformat.name = function(string){
	string = gsub("RJF.","",string)
	string = gsub("Contig\\d.LOC\\d+.","",string)
	string = gsub("MW\\d+_","",string)
	string = gsub("AF218783.1_","",string)
	return(string)
}#def reformat.name(string)

#dN
dN.lines = readLines(dN.in)
dN.mat = matrix(ncol=length(dN.lines), nrow=length(dN.lines))
gene.names = c()

for (i in 1:length(dN.lines)){
	dN.mat[i,i]=0
	stringArr = unlist(strsplit(dN.lines[i], split="\\s+"))
	
	if (i == 1){
		gene.names[i]=reformat.name(stringArr)
	}else{
		gene.names[i]=reformat.name(stringArr[1])
		for (j in 2:length(stringArr)){
			dN.mat[i,j-1]=as.numeric(stringArr[j])
			dN.mat[j-1,i]=as.numeric(stringArr[j])
		}#end for (j in 2:length(stringArr))
	}#end else
}#end for (i in 1:length(dN.lines))

colnames(dN.mat) = gene.names
rownames(dN.mat) = gene.names

##values for paired table
z=0
for (i in 1:length(dN.lines)){
	for (j in 1:i){
		if (i !=j){
			z = z + 1
			pair_gene1[z]=gene.names[i]
			pair_gene2[z]=gene.names[j]
			pair_dN[z]=dN.mat[i,j]
		}#end if (i !=j)
	}#end for (j in 1:i)
}#end for (i in 1:length(dN.lines))

#dS
dS.lines = readLines(dS.in)
dS.mat = matrix(ncol=length(dS.lines), nrow=length(dS.lines))
gene.names = c()

for (i in 1:length(dS.lines)){
	dS.mat[i,i]=0
	stringArr = unlist(strsplit(dS.lines[i], split="\\s+"))
	
	if (i == 1){
		gene.names[i]=reformat.name(stringArr)
	}else{
		gene.names[i]=reformat.name(stringArr[1])
		for (j in 2:length(stringArr)){
			dS.mat[i,j-1]=as.numeric(stringArr[j])
			dS.mat[j-1,i]=as.numeric(stringArr[j])
		}#end for (j in 2:length(stringArr))
	}#end else
}#end for (i in 1:length(dS.lines))

colnames(dS.mat) = gene.names
rownames(dS.mat) = gene.names
dS.mat = dS.mat[,match(colnames(dN.mat),colnames(dS.mat))]
dS.mat = dS.mat[match(rownames(dN.mat),rownames(dS.mat)),]

##values for paired table
z=0
for (i in 1:length(dN.lines)){
	for (j in 1:i){
		if (i !=j){
			z = z + 1
			pair_dS[z]=dS.mat[i,j]
		}#end if (i !=j)
	}#end for (j in 1:i)
}#end for (i in 1:length(dN.lines))

dS.mat = dS.mat + 0.0001

#dN/dS
dN_dS.mat = matrix(ncol=ncol(dN.mat), nrow=ncol(dN.mat))
for (i in 1:ncol(dN.mat)){
	for (j in 1:ncol(dN.mat)){
		if (i == j){
			dN_dS.mat[i,j]=0
		}else{
			dN_dS.mat[i,j]=dN.mat[i,j]/dS.mat[i,j]
		}#end else
	}#end for (j in 1:ncol(dN.mat))
}#end for (i in 1:ncol(dN.mat))
colnames(dN_dS.mat) = colnames(dN.mat)
rownames(dN_dS.mat) = colnames(dS.mat)

##values for paired table
z=0
for (i in 1:length(dN.lines)){
	for (j in 1:i){
		if (i !=j){
			z = z + 1
			pair_dN_dS[z]=dN_dS.mat[i,j]
		}#end if (i !=j)
	}#end for (j in 1:i)
}#end for (i in 1:length(dN.lines))

dN_dS.status = dN_dS.mat > 1
print(table(dN_dS.status))

write.table(dN_dS.mat, dN_dS.out, quote=F, sep="\t")

print(median(pair_dN) * 100)#multiply rate to be per 100 nucleotides
print(median(pair_dS) * 100)#multiply rate to be per 100 nucleotides
print(median(pair_dN_dS))#this is a ratio, not a rate

paried.table = data.frame(pair_gene1, 
							pair_gene2, 
							pair_dN, pair_dS, pair_dN_dS)
write.table(paried.table, dN_dS.paired.out, quote=F, sep="\t", row.names=F)
tree.in="Combined-alpha1alpha2-GAPPED-v2-pep-RENAME.tree"
pdf.out="tree-MHCYad_like.pdf"
label.space = 0.18

#use code based upon https://www.molecularecologist.com/2017/02/08/phylogenetic-trees-in-r-using-ggtree/
#as well as https://bioconnector.github.io/workshops/r-ggtree.html
#as well as https://guangchuangyu.github.io/software/ggtree/faq/

library("ggplot2")
library("ggtree")

tree = read.tree(tree.in)
p = ggtree(tree) + geom_tippoint() + geom_tiplab()
#p = p + geom_treescale()
p = p + xlim(0, label.space)#add extra space on x-axis
p
ggsave(pdf.out)
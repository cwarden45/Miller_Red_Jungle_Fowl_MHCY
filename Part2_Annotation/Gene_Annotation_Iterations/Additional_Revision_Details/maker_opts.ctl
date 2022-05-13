#-----Genome (Required for De-Novo Annotation)
genome=../../Contig1.fasta
organism_type=eukaryotic
#-----EST Evidence (for best results provide a file for at least one)
est=/path/to/Contig1_gene_named.fa
#-----Repeat Masking (leave values blank to skip repeat masking)
model_org=chicken
repeat_protein=/opt/maker/data/te_proteins.fasta
#-----Gene Prediction
est2genome=1
protein2genome=0
unmask=0
#-----MAKER Behavior Options
max_dna_len=100000
pred_stats=1
min_protein=300
alt_splice=0
always_complete=1
split_hit=3000

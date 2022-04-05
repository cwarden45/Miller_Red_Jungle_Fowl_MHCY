## Main Revision Overview

![Assembly Revision Dot Plot](102b15_revision_Rplot.png "Assembly Revision Dot Plot")

The clones with NOR sequence tend to have some lower quality drops in that region (even with the considerable additional efforts).  So, a bed file of some of the least confident regions is provided as `102b15_Arrow-LowConfidence.bed`, and that is visually shown below:

![Quality Scores in Polished Assembly](arrow_consensus-qual.png "Quality Scores in Polished Assembly")

## Methods Details

**1)** Run initial Canu assembly using `run_Canu.py`

Create separate FASTA file for longest contig for downstream steps(provided as **102b15_10k_canu_contig_unpolished.fa**).

**2)** Run 1st round of Arrow polishing on unmodified assembly using `run_Arrow-1st.sh`

This produces the sequence **arrow_var-1st.fasta**.

**3)** Run BLAST to determine coordinates to identify location of BAC backbone.

```
makeblastdb -in $CANU -dbtype nucl
blastn -perc_identity 85 -evalue 1e-20 -query CHORI_EcoRI_BAC.fa -db $CANU -out $BLAST_TABLE -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\"
```

In the 1st Arrow-polished assembly, the BAC backbone is at coordinates 62992-73675.

There is a 5,019 bp sequence that is 100% identical and duplicated next to the BAC backbone.  So, only 1 copy (from "portion1") is used in the sequence re-arranged to remove the BAC backbone and end exactly at the restriction enzyme sites.

Along with consideration including the two 6 bp EcoRI sites, this is how the coordinates for the next step were determined.

**4)** Extract duplicated content from original ends of assembly using `extract_seq-simplified.py`

**5)** Combine separate extracted sequences to create a new starting sequence using `combine_seqs.py`.

This produces the sequence **102b15_rearranged.fa**.

**6)** Create sequence used for deposit and downstream analysis using `run_Arrow-2nd.sh`

**7)** Create separate numeric quality file using `quality_score_plot-with_table.R`, and then list of low confidence regions using `create_Arrow-LowConfidence_bed.py`.

This produces the provided **102b15_Arrow-LowConfidence.bed** file.

**8)** Create supplemental coverage plot using `run_pileup.sh` and `pileup_coverage.R`.

#Optional Steps to Reproduce Figure

Run `run_MUMmer.sh` and `R_MUMmer_Plot-1_BAC_backbone.R`.

BAC backbone positions were determined using the following code (with [BLAST verison 2.6.0+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/)):

```
makeblastdb -in $EARLY_REF -dbtype nucl
blastn -evalue 1e-20 -query CHORI_EcoRI_BAC.fa -db $EARLY_REF -out $OUT -outfmt \"6 qseqid qlen qstart qend sseqid slen sstart send length pident nident mismatch gaps evalue\"
```
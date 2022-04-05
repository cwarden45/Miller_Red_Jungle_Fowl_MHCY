**Step 0a)** Create truncated galGal5 reference using `create_truncated_galGal5.py`.

**Step 0b)** For STAR, [some index reformatting was needed](https://github.com/alexdobin/STAR/issues/1261).  In the interests of consistency for the most recent analysis, all aligners used the same FASTA file for indexing.

The reformatted refence sequence was created using `concatinate_FASTA.sh` followed by `reformat_FASTA.pl`.

**Step 1a)** Index references for GMAP and TopHat2 (Bowtie2) using `index_ref-GMAP_Bowtie2.sh`

**Step 1b)** Various parameters for indexing and alignment were tested for STAR.

In terms of what is used for the main results, the STAR genome reference was indexed using `index_ref-STAR` (from within the folder where the index will be generated).

**Step 2a)** Align Chickspress RNA-Seq data using STAR with `cluster_STAR_se_alignment-1st_Alignment-Apollo-v2-param9-GZ.py`

As [recommended](https://github.com/alexdobin/STAR/issues/1261), we do not run a STAR 2-pass alignment for these samples.

For visualization, create a single combined alignment file for the reads aligned to the 4 contigs (out of the combined reference) using `create_MHCY_bams-STAR.pl`.

**Step 2b)** Various parameters for alignment were tested for GMAP.

In terms of what is used for the main results, GMAP was used to align NCBI EST and cDNA data as follows:

 - Run `run_apollo-NCBI-param6.sh` (or `run_apollo-cDNA-param6.sh`, or `run_apollo-MHCY-param6.sh`)
 - Run `processs_GMAP-param6-postApollo.py`

The query file *AY257165_AY257170-reformat.fasta* is provided in this GitHub directory.

**Step 2c)** Align Chickspress RNA-Seq data using TopHat2 with `TopHat_alignment_apollo-FULL.py`

The *PRJNA204941_Male.txt*, *PRJNA204941_Female.txt*, and *4contigs.bed* files are also being provided in this directory.

For visualization, `combined_bams.pl` was used to create a single alignment file for all samples. 
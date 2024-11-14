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

The reference sequence sequence was indexed using `gmap_build` (GMAP, version 2017-05-03, with  the `-c chrM` parameter).

Briefly, as an additional option for qualitative visual inspection, ESTs (from NCBI EST (Gallus gallus, 11/28/2016) were aligned to the custom chicken reference using [GMAP](https://pubmed.ncbi.nlm.nih.gov/15728110/) (version 2018-05-11, with parameters `-n 5 --no-chimeras --suboptimal-score=1 --min-identity=0.985 --max-intronlength-middle=2000 --max-intronlength-ends=2000 -t 1`).  All GMAP alignments were sorted (and read groups were added) with [Picard](https://broadinstitute.github.io/picard/) AddOrReplaceReadGroups (version 2.17).  Some additional information can be found within the [Iterations_of_Manual_Annotation - Annotation_Update_Example]() subfolder.


**Step 2c)** Align Chickspress RNA-Seq data using TopHat2 with `TopHat_alignment_apollo-FULL.py`

The *PRJNA204941_Male.txt*, *PRJNA204941_Female.txt*, and *4contigs.bed* files are also being provided in this directory.

For visualization, `combined_bams.pl` was used to create a single alignment file for all samples. 

The reference genome was indexed using `bowtie2-build` (Bowtie2, version 2.3.2).

Briefly, For qualitative visual inspection (but not quantification), we also compared the Chickspress reads with [TopHat2](https://ccb.jhu.edu/software/tophat/index.shtml) (version 2.1.1, with parameters `--max-intron-length 2000 --no-coverage-search --library-type  fr-unstranded`).  Reads that were aligned the given contig sequence were filtered using `samtools view` and then indexed ([samtools](http://samtools.sourceforge.net/), version 1.6).

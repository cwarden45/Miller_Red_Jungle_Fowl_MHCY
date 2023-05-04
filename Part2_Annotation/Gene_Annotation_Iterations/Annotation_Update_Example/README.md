
## Example Code

The code needed to be manually revised during several iterations of analysis.  So, one set of code cannot be provided for all annotation updates.

However, the code for the most recent update can be used to try and help explain how the annotations were updated for downstream analysis (including creation of part of *Figure 1*).  The starting point for this code also changed over time, but the code that starts with GTF files as the starting point was created around the time that the annotations were tranferred to modified assembly sequencing (largely with the assistance of the [gtf-pileup_liftOver](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Gene_Annotation_Iterations/gtf-pileup_liftOver) code).

**0)** If needed re-name the genes using `STEP00-convert_gene_names.py`.

This particular script partially used the output from the [Gene_Annotation_Iterations: - gtf-pileup_liftOver](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Gene_Annotation_Iterations/gtf-pileup_liftOver) subfolder (affecting Contig 1).

**1)** Run `STEP01-extract_named_v11.py` (for each of the 4 contigs, commenting out different parts of the code).

This creates an intermediate file that helps describe the genes as well as checking the validity of the protein sequences (creating cDNA FASTA files + protein FASTA files).

The cDNA FASTA files for the gene candidates will be used for the BLAST searches in the subsequent steps.

**2)** Run `STEP02-BLAST_named_RefSeq-v4.py` to identify hits to RefSeq genes as well as newly deposited cDNA sequences and separate MHC-Y amplicon sequences ( [AY257165.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257165), [AY257166.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257166), [AY257167.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257167), [AY257168.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257168), [AY257169.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257169, and [AY257170.1](https://www.ncbi.nlm.nih.gov/nuccore/AY257170) ).

Different parts of the code are commented out for each contig.

**3)** Run `STEP03-BLAST_named_self-v2.py` to describe self homology among gene candidates (including 100% matches).

Runs analysis for all 4 contigs at one time.

**4)** Run `STEP04-create_new_GTF_v4.py`

*This script produces the GTF files that are used for quantification.*

This script may not always be strictly needed for every revision.

Different parts of the code are commented out for each contig.

**After being manually combined, this script also produces the GTF files that are provided on this GitHub page in [this subfolder]()**.  The GTF is renamed as **Combined_updated_genes-17March2022.gtf** (instead of *Combined_updated_genes-220317.gtf*) in order to match a different style of describing files saved in a folder to prepare this GitHub upload.

**5)** Run `STEP05-BLAST_mapping_RefSeq-v3.R` to reformat earlier BLAST hit tables in a way that is more descriptive for each query gene.  Also lists genes from GTF that don't have BLAST hits.

Different parts of the code are commented out for each contig.

**6)** Run `STEP06-BLAST_mapping_cDNA.R` to reformat earlier BLAST hit tables in a way that is more descriptive for each query gene.  Also lists genes from GTF that don't have BLAST hits.

Different parts of the code are commented out for each contig.

*If there are 0 cDNA hits on a contig, then the error message generated should be disregarded.*

**7)** Run `STEP07-BLAST_mapping_self-contig_v2.R` to reformat earlier BLAST hit tables in a way that is more descriptive for each query gene.  Also lists genes from GTF that don't have BLAST hits.

Runs analysis for all 4 contigs at one time.

**8)** Use `STEP08a-run_featureCounts.py` to quantify NCBI EST evidence from *11/28/2016*, followed by `STEP08b-combine_EST_multimap_v4.R` for reformatting.

I believe these sequences were downloaded from [NCBI Nucleotide](https://www.ncbi.nlm.nih.gov/nuccore) following instructions described [here](https://www.researchgate.net/post/How_can_I_download_the_whole_EST_sequence_of_an_organism_from_NCBI_genbank).  For example, the search criteria would be "*Gallus gallus[porgn:__txid9031]*".

**9)** Run `STEP09-GTF_to_tbl_v20.py` to create .tbl files that can be entered into Sequin (or preferred program) to prepare GenBank submission.

Different parts of the code are commented out for each contig.

This also creates a table that can potentially be used for the rRNA gene clusters on Contig 1.  *However, the actual table used has some additional manual modifications and separate code, more related to the [repeat annotations](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Repeat_Annotations).

Previous versions used TopHat2 alignments and QoRTS for the splice junction evidence.  However, we more recently switched to using the [STAR splice junction]() evidence for the Illumina RNA-Seq data.  To avoid confusion, we are not providing those details here.  However, there is a template for a different context [here](https://github.com/cwarden45/RNAseq_templates/tree/master/Splicing_Workflow).

**10)** Run `STEP10-combined_Figure_V9.R` to create plot to illustrate types of genes at loci across the chromosomes, which is used in the associated publication.

**11)** Create Supplemental Table using `STEP11-combine_and_reformat_gene_summaries-v2.R`.

The input file (*combined_gene_summary.txt*) is created by manually combining the files from the 4 contigs (*Contig1_gene_summary.txt*,*Contig2_gene_summary.txt*,*Contig3_gene_summary.txt*,*Contig4_gene_summary.txt*)

You must have already run the code to summarize [STAR splice junctions](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/STAR_Splice_Junction_Evidence) before this table can be created.

Please note that this function may perform differently in different version of R.  For example, the script above works with **R v4.1.2** on Windows, but it encountered a problem when running R *v3.4.4* within Ubuntu.

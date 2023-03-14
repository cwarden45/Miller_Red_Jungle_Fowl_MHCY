## Primary Repeat Annotations

Repeats were annotated with 2 programs:

**a)** [RepeatMasker version 4.0.6](https://www.repeatmasker.org/RepeatMasker/) with chicken RepBase annotations (downloaded 4/6/2017) and [rmblast version 2.2.27](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.27/) as the search engine, and parameters `-species chicken -gff`.

**b)** [Tandem Repeat Finder (TRF) version 4.09](https://tandem.bu.edu/trf/trf.download.html) with parameters `2 7  7  80 10 50 50 -d -m`).

The full reference to each assembly was provided, without masking and running analysis in serial.

## rDNA Array / Cluster Annotations

Instead of using a repeat program, the following components of the rDNA array / cluster were defined using [KT445934](https://www.ncbi.nlm.nih.gov/nuccore/KT445934): 5' external transcribed spacer, 18S ribosomal RNA  gene, internal transcribed spacer 1, 5.8S ribosomal RNA gene,  internal transcribed spacer 2, 28S ribosomal RNA gene, and 3' external transcribed spacer)

Those boundaries were defined using were annotated using [BLAST version 2.6.0+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/).

## Scripts to create annotations

The scripts are saved in different folders for each contig.  However, the file used for *Contig 1* was used as an example for the shared code for reproduciblity.

**1)** Define raw **RepeatMasker** and **TRF** repeats using `annotate_BAC.py`.

The raw TRF output is available [here](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part2_Annotation/Repeat_Annotations/TRF-Raw_Output.zip).

The original GFF annotation files from Repeat Masker are combined and saved [here](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part2_Annotation/GTF_GFF_files/Combined_RepeatMasker-22March2022.gff).

**2a)** Create intermediate files in a format that potentially could be used for GenBank annotation using `create_RepeatMasker_tbl.py` and `create_TRF_tbl.py`.

**2b)** Consolidate repeat annotations and create files that can be imported into Sequin (or other program) for GenBanks submission using `find_different_annotations_v2.py` and `find_matching_annotations_v2.py`.

This also allows for a way to systematically make other changes.

The scripts have a folder structure.  You have to move within the ***Repeat_Tables*** folder to run the scripts for **2b)**.

**3)** Only for **Contig 1**, create NOR gene/repeat annotations using `run_NOR_BLAST.py` and `create_NOR_tbl.py`.

The **rRNA_cluster.fasta** and **rRNA.fa** files are provided on GitHub.  The accession for the full sequence is within *rRNA_cluster.fasta*.  The specific gene query sequences come from that same accession ([KT445934](https://www.ncbi.nlm.nih.gov/nuccore/KT445934)), but that is not within the FASTA file itself.

**4)** For an overall repeat summary, you can run `summarize_RepeatMasker-v2.R`.

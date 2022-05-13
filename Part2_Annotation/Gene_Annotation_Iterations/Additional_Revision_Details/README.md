## Details for Running Exonerate

In general, there are at least two purposes for which Exonerate can be used:

**1)** ***Discovery** of new gene annotations related to previous gene annotations*:

If you knew the type of genes that you expected to be present (but you didn't know the precise gene sequences or locations), then you could run Exonerate with a command as follows:

`/opt/exonerate-2.2.0-x86_64/bin/exonerate --showtargetgff true --model protein2genome --showalignment no $QUERY $TARGET > $OUTPUT`

This was tested at certain earlier stages, but we don't emphasize that strategy very much with the GitHub content.

**2)** ***Transfer** of gene annotations for the same locus*:

This is of some important for understanding the current annotations.

For example, overall, we primarily used the [gtf-pileup_liftOver](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Gene_Annotation_Iterations/gtf-pileup_liftOver) strategy to transfer annotations.

However, this left out the locus currently described as MHCY20.  Because there were other loci that were missed with Exonerate, we don't emphase that as the primary method.  However, this was the command that we thought was relatively best to look for similar loci in sequence with repeats and large duplications:

`/opt/exonerate-2.2.0-x86_64/bin/exonerate --bestn 1 --showtargetgff true --model protein2genome --showalignment no --percent 97 --maxintron 2000 $PEPTIDEFASTA $GENOMICTARGETFASTA > $OUTPUT`

The parameters `--percent 97 --maxintron 2000 ` may also be of some particular importance.  As mentioend in the *gtf-pileup_liftOver* discussion, there is some additional information related to the basis of selecting those parameters [here](https://www.biostars.org/p/472543/)

## Details for Running MAKER2

MAKER2 was run using the command `/opt/maker/bin/maker -nolock -fix_nucleotides`.

Within that same folder, the following files must also be found:

 - **maker_bopts.ctl**
 - **maker_exe.ctl**
 - **maker_opts.ctl**

Examples for Contig1 are provided within this subfolder of the GitHub repository.

For visualization purposes, those files were filtered with the command `grep CDS $IN > $OUT`, and the CDS exons annotations were combined between the 4 contigs to provide 1 file that can be used for visualization in a program like [IGV](https://software.broadinstitute.org/software/igv/).

## The "source" column in the gene annotation GTF

When the code for downstream analysis started from a GTF file (to be similar as presented [here](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Gene_Annotation_Iterations/Annotation_Update_Example)), changes in that [GTF file including protein-coding genes](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part2_Annotation/GTF_GFF_files/Combined_updated_genes-24March2022.gtf) were logged within the "source" column.

This does not represent the full amount of changes that occured following an initial, automated strategy for making gene predictions ([GENSCAN](http://hollywood.mit.edu/GENSCAN.html)).

However, this might help provide some more specific examples in how the gene annotations were revised:

 - For the most part, we believe that the [gtf-pileup_liftOver](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/Gene_Annotation_Iterations/gtf-pileup_liftOver) strategy was the relatively best way to transfer annotations when these sequences with large duplications were revised.  However, after removing an incorrect duplication in the 19d16 sequence, [Exonerate](https://www.ebi.ac.uk/about/vertebrate-genomics/software/exonerate) was used to identify the **MHCY20** locus.  That is what is meant by "**exonerate**".
   - Strictly speaking, Exonerate had difficulty finding the first exon in the annotation that we wanted to use, and the first transferred annotation used a mix of Exonerate and [MAKER2](https://www.yandell-lab.org/software/maker.html).
   - At a later time, the first exon was further changed when running Exonerate in a different way, and that is what "**exonerate_mod**" for *MHCY20* represents.
   - An additional discussion regarding the details of the MHCY20 revisions may be added at a later time.
 - Following a discussion with NCBI staff, additional exons were added to the YLEC genes.  These annotations may undergo further changes, but this is indicated by "**NCBI_Exonerate**" because [Exonerate](https://www.ebi.ac.uk/about/vertebrate-genomics/software/exonerate) was used to identify the genomic locations in the clones based upon the alternative transcript models as sequences as FASTA files.
 - When we identified a problem with an earlier version of a gene model, running multiple methods could sometimes help select alternative exons for a possible protein sequence.
   - Details for additional revisions for other loci may be provided at a later time.
 - A valid protein-coding gene sequence (without introns) was found for the *OZFL* locus after comparing coding potentials for coding and non-coding gene candidates using [CPAT](https://code.google.com/archive/p/cpat/).  That is what the "**CPAT**" note represents.  CPAT was run with the command `cpat.py -g $INPUTFASTA -o CPAT_transcript_human  -d prebuilt_models/Human_logitModel.RData -x prebuilt_models/Human_Hexamer.tab`.

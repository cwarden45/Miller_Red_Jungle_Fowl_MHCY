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
 - A valid protein-coding gene sequence (without introns) was found for the *OZFL* locus after comparing coding potentials for coding and non-coding gene candidates using [CPAT](https://code.google.com/archive/p/cpat/).  That is what the "**CPAT**" note represents.  CPAT was run with the command `cpat.py -g $INFA -o CPAT_transcript_human  -d prebuilt_models/Human_logitModel.RData -x prebuilt_models/Human_Hexamer.tab`.

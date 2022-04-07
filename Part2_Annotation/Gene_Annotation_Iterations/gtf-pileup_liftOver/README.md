## Example for most recent revision

There should be fewer difficulties in transferring gene annotations when only changing 5 bp for a repeat sequence (in Contig 1, which will be the example for the code shared for reproducibility).

However, to walk through the steps involved:

**1)** Compare assemblies with a BWA-MEM alignment and create a .pileup file comparing the previous and current assembly for a given contig using `BWA-MEM_alignment.py`.

**2)** Transfer annotations using `gtf-pileup_liftOver-v2.py`.

The `shift` value will change depending upon the assembly sequences.  This will not be constant for all annotation transfers, so alternative versions of the transfer are not provided for the other 3 contigs.

However, to explain the numbers used for the Contig 1 transfer in an assembly with a 5 bp difference:

 - 
 
 
The folder path includes a subfolder called ** because a number of methods were tested to transfer the annotations.  There is some discussion that can be viewed here.

When there was a more complicated difference between assemblies, the .pileup GTF transfer strategy did not capture everything and some manual work was needed to transfer 100% of gene annotations correctly.  For example, you can see some discussion [here](https://www.biostars.org/p/472543/).  However, as far as we could tell, it was the best overall strategy to start with a semi-automated transfer of annotations.


## Additional Background Regarding Gene Annotation Process

Previous MHC-Y gene annotations required a substantial amount of manual revision (starting from an initial set of [GENSCAN](http://hollywood.mit.edu/GENSCAN.html) - **NOTE: CONFIRM THIS IS TRUE**).  When we revised the reference sequences, we also needed to revise the gene annotations.  However, to avoid starting completely from scratch we used [Exonerate](https://www.ebi.ac.uk/about/vertebrate-genomics/software/exonerate) (version 2.2.0) to help guide the transfer of gene annotations to the latest version used in this publication (with parameters `--bestn 1 --showtargetgff true --model protein2genome --showalignment no --percent 97 --maxintron 2000`, using the unique set of gene protein/peptide sequences from the previous annotation).  There are some notes about the justification for that strategy [here](https://www.biostars.org/p/472543/).  If a limited number of changes could be made, then that could be used to determine the current annotations.  While better than the alternatives tested, some Exonerate hits still required some manual curation to have the correct gene structure.

Exonerate hits were compared to pileup-transferred hits.  As indicated by [GffCompare](https://ccb.jhu.edu/software/stringtie/gffcompare.shtml), most exons matched.  When there was a difference in the results, each gene was inspected to consider revision.  There was one YF gene that was missed at the end of Contig1 with the pileup-transfer.  Exonerate had a tendency to lose the last exon for some YF hits, so an extra exon from [MAKER](https://www.yandell-lab.org/software/maker.html) was used to define a complete protein sequence.

If exons needed to be added, MAKER worked OK for generating candidates for the YF genes, but it often did not make any overlapping predictions for the YLec genes.  So, for example, when a partial gene annotation at the end of Contig3 was converted to a pseudogene (because it was too short to be a YLec gene and therefore had a premature stop codon), one of the predicted exons for GENSCAN was used to expand the pseudogene annotation (which was roughly comparable to the gene expression data in the following section, based upon visual inspection). 

Repeat annotations are run on the new sequence, and those therefore do not need to be transfered from the previous version of the contig assembly.

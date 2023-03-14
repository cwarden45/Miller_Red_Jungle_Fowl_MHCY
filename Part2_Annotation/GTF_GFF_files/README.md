
**Combined_updated_genes-24August2022.gtf** - coding gene annotations; example code for creation **will be provided** provided within the [Iterations_of_Manual_Annotation - Annotation_Update_Example]() subfolder.

**Combined_RepeatMasker-22March2022.gff** - raw annotations from RepeatMasker, combined using `combine_GTF.sh`.

Tandem Repeat Finder (TRF) does not directly provide at GFF or GTF file.  However, the raw output files are provided in a .zip file [here](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part2_Annotation/Repeat_Annotations/TRF-Raw_Output.zip).

**Combined_EMBOSS_Cpgplot-22March2022.gff** - raw output from [EMBOSS Cpgplot](https://www.ebi.ac.uk/Tools/seqstats/emboss_cpgplot/), combined using `combine_GTF.sh`.

For CpG Island prediction, each of the 4 contigs was uploaded into the [EMBOSS Cpgplot web interface](https://www.ebi.ac.uk/Tools/seqstats/emboss_cpgplot/) on 3/22/2022.  Within the results, the **Download results in GFF feature format** option was selected to download the 4 separate files to concatinate above.

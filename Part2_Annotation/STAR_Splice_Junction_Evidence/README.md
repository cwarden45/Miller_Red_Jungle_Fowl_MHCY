## Scripts to Asssess Annotations

**1)** Run `STEP01-create_splice_junction_table-STAR-v3b.py`

 - This creates various types of files for each separate contig (unique junction counts, multi-mapped junction counts, etc.)
 - Also, separately for each contig, normalized CPM is calculated.  **However, please note that this is not adjusted for copy number until a later step.**

This also creates the file *STAR_read_stats-param9.txt*, provided on this GitHub page.

**2a)** Run `STEP02a-create_splice_junction_table_COMBINED-STAR-v3d.R` to create combined files and some QC plots.

This creates the following tables of coverage each splice junction in **each of the 27 [Chickspress](https://geneatlas.arl.arizona.edu/) samples**.

**Raw Counts**: *combined_splice_junctions-STAR-v3_RAW-param9.txt*

**Unique Counts (Count-Per-Million, CPM)**: *combined_splice_junctions-STAR-v3_uniqueCPM-param9.txt*

**2b)** Run `STEP02b-adjust_totalCPM_for_copy_number.R` to adjust total CPM values based upon the total gene copies across the 4 contigs.

This creates the file *combined_splice_junctions-STAR-v4_totalCPM-param9-ADJUSTED.txt*, with **per-sample** mean Count-Per-Million (CPM) **adjusted** by the number of known copy-number on Contigs 1-4.

Unique counts don't need to be adjusted by copy number, so this only adjusted the multi-mapped counts (when they contribute to the total counts).

Please note that this function may perform differently in different version of R, in addition to not providing every single file that was created across several years.

For example, the script above works with **R v4.1.2** on Windows, but it encountered a problem when running R *v3.4.4* within Ubuntu.

**2c)** Run `STEP02c-create_splice_junction_table_COMBINED-STAR-v3e.R` to create combined files (importantly, the total CPM counts will now be adjusted for known copies).

This creates the file with mean Count-Per-Million (CPM) values for each junction, along with the following density distributions for the mean CPM per splice junction.

![Overall STAR Splice Junction Mean Count-Per-Million Distribution](combined_splice_junctions-STAR-v4_totalCPM-ADJUSTED-junction_average_density-param9.png "Overall STAR Splice Junction Mean Count-Per-Million Distribution")

![Per-Sample STAR Splice Junction Mean Count-Per-Million Distribution](combined_splice_junctions-STAR-v4_totalCPM-ADJUSTED-sample_density-param9.png "Per-Sample STAR Splice Junction Mean Count-Per-Million Distribution")

**3)** Create some additional separate files with varying stringency using `STEP03-create_splice_junction_list-STAR-v3b.py`.

**4)** Create a summary of junctions in 1 file using `STEP04-create_splice_junction_summary-STAR-v3c.R`.

This creates the file *combined_splice_junctions-STAR-v4-param9-ADJUSTED_CPM.txt*.

**5)** Quantify evenness of coverage and generate QC plots for all gene candidates with multiple exons using  `STEP05-STAR_SD_calculations_and_plots-v2.R`.

The QC plots for evenness of coverage can be found within the [SD_Plots](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part2_Annotation/STAR_Splice_Junction_Evidence/SD_Plots) subfolder.

**6)** Define confidence assignments using  `STEP06-create_splice_junction_table_CATEGORY-STAR-v4.R`.


## Troubleshooting Notes for Script Development

***Add notes about STAR parameter troubleshooting, including effect on YLEC cluster(s).***.

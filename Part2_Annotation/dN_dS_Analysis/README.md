## Part I: Generation of Sequences for Alignment and Visualization

**Step 1)**: For [AF218783.1](https://www.ncbi.nlm.nih.gov/nuccore/AF218783.1), extract coding sequence from genomic deposit using `extract_CDS.py`.

Other sequences come from data generated for this study.  There is 1 unmapped cDNA from Red Jungle Fowl that is not used for analysis becuase the Alpha1-Alpha2 sequence is 100% identical to MHCY-e.

**Step 2)**: Align sequences using [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/) to create *Combined-CDS-GAPPED.fa*.

**Step 3)**: Using materials from elsewhere in the publication, manually select the aligned alpha1-alpha2 nucleotide sequence (using translation of test nucleotide sequences from a representative sequence using [Expasy](https://web.expasy.org/translate/)).

This creates the file `Combined-alpha1alpha2-GAPPED-v2.fa`.

Using the `divide-alpha1_alpha2.pl` file described in the next section, protein sequences can be created by defining all sequence as on-target sequence (without any sequence outside of a target region).  This creates the file *Combined-alpha1alpha2-GAPPED-v2-pep.fa*.

**Step 4)**: Re-upload alpha1-alpha2 sequence to [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/), create phylogenetic tree by selecting "**Phylogenetic Tree**", and download a text file for the tree (in order to create a plot with scaling to help identify similar sequences).

**Step 5)**: Manually simplify/reformat names to create *Combined-alpha1alpha2-GAPPED-v2-pep-RENAME.tree*.

**Step 6)**: Create MHCY tree to select branches for PAML dN/dS Estimations using `intra-species_tree_plot-GitHub.R`

## Part II: Chicken PAML dN/dS Estimations

**Step 1)**: Manually select select sequences to analyze (from *Combined-alpha1alpha2-GAPPED-v2.fa*) in new file `Combined-alpha1alpha2-GAPPED-MHCYad_like.fa`

**Step 2)**: Extract subsets of Alpha1-Alpha2 sequence using `divide-alpha1_alpha2.pl`.

**Step 3)**: Create PAML input files by using extracted nucleotide sequence and [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/) aligned protein sequence using [PAL2NAL](http://www.bork.embl.de/pal2nal/).

**Step 4)**: Create subfolders for 3 categories of regions (alpha1 helices, alpha2 helices, and non-helix regions).  Within each folder, create a PAML configuration file (`codeml.ctl`) and execute using `run_PAML.sh`.

The configurations are designed to run pairwise dN and dS estimates, with minor modifications from [Bitarello et al. 2016](https://pubmed.ncbi.nlm.nih.gov/26573803/) in [this configuration file](https://github.com/bbitarello/dNdS-hla-allelic-lineages/blob/master/data/site_models/codeml_A_nuc_all.ctl).  Namely, the difference for this analysis is that `runmode = -2` and `NSsites = 0`, as well as the input *.paml* files being re-named accordingly.

Input files and output files are uploaded for the following folders:

[Bitarello_codeml-alpha1-helix]()
[Bitarello_codeml-alpha2-helix]()
[Bitarello_codeml-nonAlphaHelices]()

To help with import into R, the header was manually removed from the *2NG.dN* and *2NG.dS* files within each subfolder (and the files were then re-named to have a *.txt* extension).

**Step 5)**: `PAML-yn00-heatmap_MHCY-GitHub.R` was used to reformat dN and dS values, calculate dN/dS values with a rounding factor of to avoid division by 0 when dS is 0, and prepare input files for the downstream script.

**Step 6)**: Visualization for comparison with human data can be performed after completing similar steps for HLA sequences.

## Part III: HLA PAML dN/dS Estimations

**Step 1)**: Download sequences with GenBank sequences selected within sources referenced at [IPD-IMGT/HLA](https://www.ebi.ac.uk/ipd/imgt/hla/)

**Step 2)**: As needed, extract coding sequence from genomic deposit using `extract_CDS.py`.

**Step 3)**: Align coding sequences using [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/).

**Step 4)**: Create maximum length FASTA alignment using `ClustalAln_to_FASTA-subset.py`.

There coordinates could be defined by comparison to a more manual selection of alpha1-alpha2 sequence for an alignment fewer sequences (after first using a comparison to ARS sequence from *Figure 1* of [Bjorkman et al. 1987](https://www.nature.com/articles/329512a0) to confirm the code, to replicate as much as possible from [Hughes and Nei 1988](https://www.nature.com/articles/335167a0)).

**Step 5)**: Extract subsets of Alpha1-Alpha2 sequence using `divide-alpha1_alpha2.pl`.

**Step 6)**: Create PAML input files by using extracted nucleotide sequence and [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/) aligned protein sequence using [PAL2NAL](http://www.bork.embl.de/pal2nal/).

**Step 7)**: Create subfolders for 3 categories of regions (alpha1 helices, alpha2 helices, and non-helix regions).  Within each folder, create a PAML configuration file (`codeml.ctl`) and execute using `run_PAML.sh`.

The configurations are designed to run pairwise dN and dS estimates, with minor modifications from [Bitarello et al. 2016](https://pubmed.ncbi.nlm.nih.gov/26573803/) in [this configuration file](https://github.com/bbitarello/dNdS-hla-allelic-lineages/blob/master/data/site_models/codeml_A_nuc_all.ctl).  Namely, the difference for this analysis is that `runmode = -2` and `NSsites = 0`, as well as the input *.paml* files being re-named accordingly.

Input files and output files are uploaded for the following folders:

[Bitarello_codeml-alpha1-helix]()
[Bitarello_codeml-alpha2-helix]()
[Bitarello_codeml-nonAlphaHelices]()

To help with import into R, the header was manually removed from the *2NG.dN* and *2NG.dS* files within each subfolder (and the files were then re-named to have a *.txt* extension).

**Step 8)**: `PAML-yn00-heatmap_shortHLA-GitHub.R` was used to reformat dN and dS values, calculate dN/dS values with a rounding factor of to avoid division by 0 when dS is 0, and prepare input files for the downstream script.

**Step 9)**: Visualize density distributions for pairwise dN/dS values using `inter-species_density_plots-Helix_Fig-GitHub.R`.

To our knowledge, this question about comparing the distribution of dN/dS values for 2 species has some differences to previous HLA dN/dS analysis.  At the current sample size for the MHCY sequences, the KS-test appears to provide approximately appropriate significance levels when comparing MHCY and HLA distributions of dN/dS values.  However, these density plots do not show completely independent values, and a subset of outlier samples could skew the density distribution for all pairwise comparisons including those outliers.  So, with larger sample sizes in both species, this may not be appropriate to define statistical significance.

Nevertheless, for publication, these plots are only used for visualization without reporting statistical significance.
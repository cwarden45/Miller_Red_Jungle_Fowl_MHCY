```diff
+ This code was developed for a project within the lab of Marcia M. Miller.
```

## Assembly Method Per Clone

<table>
  <tbody>
    <tr>
      <th align="center">Contig</th>
      <th align="center">Clone</th>
	  <th align="center">Assembly Method</th>
	  <th align="center">BAC</br>(restriction enzyme)</th>
    </tr>
    <tr>
	  <td align="center" rowspan="5"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/Contig1">Contig1</a></td>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/1o23">1o23</a></td>
	  <td align="center">Canu v2.1 + Arrow v2.3.3</td>
	  <td align="center">CHORI</br>(EcoRI)</td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/102b15">102b15</a></td>
	  <td align="center">Canu v1.5 + Arrow v2.3.3</td>
	  <td align="center">CHORI</br>(EcoRI)</td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/190m7">190m7</a></td>
	  <td align="center">Canu v1.5 + Arrow v2.3.3</td>
	  <td align="center">CHORI</br>(EcoRI)</td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/173o1">173o1</a></td>
	  <td align="center">Canu v2.1 + Arrow v2.3.3</td>
	  <td align="center">CHORI</br>(EcoRI)</td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/19d16">19d16</a></td>
	  <td align="center">HGAP3 + (Indirect) Original End Trimming + Arrow v2.3.3</td>
	  <td align="center">TAMU</br>(EcoRI)</td>
    </tr>
    <tr>
	  <td align="Center">Contig2</td>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/Contig2_58f18">58f18</a></td>
	  <td align="center">HGAP3 + Draft End Trimming + Arrow v2.3.3</td>
	  <td align="center">TAMU</br>(EcoRI)</td>
    </tr>
    <tr>
	  <td align="Center">Contig3</td>
      <td align="center"><a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/Contig3_34j16">34j16</a></td>
	  <td align="center">HGAP3 + Arrow v2.3.3</td>
	  <td align="center">TAMU</br>(HindIII)</td>
    </tr>
</tbody>
</table>

We switched assemblies for the following reasons:

 - In the original assembly where the BAC backbone would not be at the ends, the HGAP assemblies for 190M and 1o23 (and 19d16) initially appeared to have assembly edges without 100% overlap.  However, this was not true, and we believe there was additional sequencing / assembly errors towards the ends of the sequence.  Because the BAC backbone is not automatically at the ends of the sequence, this resulted in **large duplicated content** that was not at the ends of the assembly when after re-arrangement to create a linear chicken sequence.  This was especially problematic in the NOR regions.
 - 58f18 needed **noticable trimming** (before the BAC backbone), but a re-arrangment was otherwise not needed for finalizing that assembly.
 - 102b15 and 173o1 differences were more subtle, but we thought there was a slight advantage to the Canu assembly (such as having the *right restriction enzyme* at the end of the NOR region in 102b15)

We used representative sequences from the assemblies to define the 2 BAC backbones:

 - 10,685 bp for the CHORI vector in 190M (EcoRI)
 - 7,513 bp for the TAMU vector in 19d16 (EcoRI or HindIII)
 
For PacBio data, the input files for various analysis were created using `run_apollo-Singularity-CLR.sh` or `run_apollo-Singularity-CCS.sh`.

## Validation / Assessment with Other Technologies

<table>
  <tbody>
    <tr>
      <th align="center" colspan="3"></th>
      <th align="center">Pilon</th>
	  <th align="center" colspan="2">VarScan-Cons (<a href="https://peerj.com/articles/600/">Warden et al. 2014</a>)</th>
	  <th align="center">One-Sample Pileup</th>
    </tr>
    <tr>
      <th align="center">Contig</th>
      <th align="center">Clone</th>
	  <th align="center">Polished Length</th>
	  <th align="center">Illumina</th>
	  <th align="center">Illumina</th>
	  <th align="center">PacBio 10x CCS</th>
	  <th align="center">Public/Sanger</th>
    </tr>
    <tr>
	  <td align="center" rowspan="2">Contig1</td>
      <td align="center">190m7</td>
	  <td align="center">253,430 bp</td>
	    <td align="center"><b>14 insertions<sup>a</sup></b></td>
	    <td align="center"><b>8 SNPs</b></br>(5 "homozygous" if diploid)</br></br><b>29 indel</b></br>(11 "homozygous" if diploid)</td>
	  <td align="center"><b>1 SNP</b></br>(0 "homozygous" if diploid)</br></br><b>93 indel</b></br>(0 "homozygous" if diploid)</td>
	  <td align="center"><i>Not Available</i></td>
    </tr>
    <tr>
      <td align="center">173o1</td>
	  <td align="center">221,406 bp</td>
	  <td align="center"><b>0 changes</b></td>
	  <td align="center"><b>1 SNP</b></br>(0 "homozygous" if diploid)</br></br><b>0 indel</b></br>(0 "homozygous" if diploid)</td>
	  <td align="center"><i>Not Available</i></td>
	  <td align="center"><b>9 variable positions</b><br>(some indels larger than 1 bp)</br></br>(<a href="https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part1_Assembly/173o1/173o1_Sanger-plus-J_AA173O01.pileup.xlsx">re-arranged AC275299.1</a>)</td>
    </tr>
    <tr>
	  <td align="Center">Contig2</td>
      <td align="center">58f18</td>
	  <td align="center">148,501 bp</td>
	  <td align="center"><i>Not Available</i></td>
	  <td align="center"><i>Not Available</i></td>
	  <td align="center"><b>0 SNPs</b></br>(0 "homozygous" if diploid)</br></br><b>7 indel</b></br>(2 "homozygous" if diploid)</td>
	  <td align="center"><i>Not Available</i></td>
    </tr>
    <tr>
	  <td align="Center">Contig3</td>
      <td align="center">34j16</td>
	  <td align="center">138,921 bp</td>
	<td align="center"><b>0 changes</b><br><br><b>(2 libraries)</b></td>
	  <td align="center"><b>0 SNPs</b><br>(0 "homozygous" if diploid)<br></br><b>0 indel</b><br>(0 "homozygous" if diploid)<br><br><b>(2 libraries)</b></td>
	  <td align="center"><i>Not Available</i></td>
	  <td align="center"><b>0 changes</b></br>(Sanger Assembly)</td>
    </tr>
</tbody>
</table>

<sup>a</sup>Count comes from earlier version of the assembly.  Please see issue related to more recently created file [here](https://github.com/broadinstitute/pilon/issues/136).

If a PacBio sequencing was run on a smaller library size, then Circular Consensus Sequence (CCS) reads could be generated.  For 190M and 58f18 CCS libraries, 10X CCS reads were then generated using the `ccs` function in the unanimity package (currently available in [this Docker image](https://hub.docker.com/r/cwarden45/general-pacbio/)).  The [samtools version1.9](https://github.com/samtools/samtools/releases/tag/1.9) function `bam2fq` was then used to create CCS FASTQ files.

The relative differences had the same ranking regardless of the method or technology used, and **most potential differences in the 190M assembly were in the *NOR region***.  However, no homozygous variants were consistent for both the Illumina and PacBio CCS library data.  **All methods tested recommended *0 changes* to 34j16.**

Details related to the table above can be found within [this folder](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/tree/main/Part1_Assembly/Other-Assembly_Assessment).

**In short, we find minimal evidence for improvement in the MHCY portion of the BAC clones.**

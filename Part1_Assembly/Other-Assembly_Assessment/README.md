## Summary of Results

**190m7 (MHC-Y Region starts at 106,161 bp for beginning of GGLTR7-int repeat)**:

*Pilon (Illumina)*:

*VarScan-Cons (SNPs - Illumina)*:

*VarScan-Cons (Indels - Illumina)*: **93 indels** ([please see 190m7-varscan.cons.indel.vc file](https://github.com/cwarden45/Miller_Red_Jungle_Fowl_MHCY/blob/main/Part1_Assembly/Other-Assembly_Assessment/190m7-varscan.cons.indel.vcf))

*VarScan-Cons (SNPs - PacBio 10x CCS)*: **1 SNP** (see below)

<table>
  <tbody>
    <tr>
      <th align="center">Position</th>
      <th align="center">Ref</th>
	  <th align="center">ALT</th>
	  <th align="center">Genotype</br>(diploid settings)</th>
    </tr>
    <tr>
	  <td align="center">47696</td>
      <td align="center">T</td>
	  <td align="center">A</td>
	  <td align="center">0/1</td>
    </tr>
</tbody>
</table>

*VarScan-Cons (Indels - PacBio 10x CCS)*:

Most regions with possible differences are in the NOR region, which we expect to have greater assembly errors.

If we are not confident that the reference should be changed (such as mixed results), then we provide this as a list of possibly "unsure" positions (rather than changing the main reference).

**173o1 (All MHC-Y)**:

*Pilon (Illumina)*: **0 changes**

*VarScan-Cons (SNPs - Illumina)*: **1 SNP** (see below)

<table>
  <tbody>
    <tr>
      <th align="center">Position</th>
      <th align="center">Ref</th>
	  <th align="center">ALT</th>
	  <th align="center">Genotype</br>(diploid settings)</th>
    </tr>
    <tr>
	  <td align="center">94141</td>
      <td align="center">A</td>
	  <td align="center">G</td>
	  <td align="center">0/1</td>
    </tr>
</tbody>
</table>


*VarScan-Cons (Indels - Illumina)*: **0 indels**

*Re-Arranged AC275299.1/J_AA173O01 Public Sequence*: **9 variable sites** (see below)

<table>
  <tbody>
    <tr>
      <th align="center">Position</th>
      <th align="center">Ref</th>
	  <th align="center">ALT</th>
    </tr>
    <tr>
	  <td align="center">12624</td>
      <td align="center">G</td>
	  <td align="center">A</td>
    </tr>
    <tr>
	  <td align="center">12625</td>
      <td align="center">C</td>
	  <td align="center">T</td>
    </tr>
    <tr>
	  <td align="center">12934</td>
      <td align="center">T</td>
	  <td align="center">G</td>
    </tr>
    <tr>
	  <td align="center">39511</td>
      <td align="center">C</td>
	  <td align="center">A</td>
    </tr>
    <tr>
	  <td align="center">39820</td>
      <td align="center">A</td>
	  <td align="center">G</td>
    </tr>
    <tr>
	  <td align="center">39821</td>
      <td align="center">T</td>
	  <td align="center">C</td>
    </tr>
    <tr>
	  <td align="center">72789</td>
      <td align="center">A</td>
	  <td align="center">AAAGGGAAGGG</td>
    </tr>
    <tr>
	  <td align="center">166521</td>
      <td align="center">A</td>
	  <td align="center">AAAGGG</td>
    </tr>
    <tr>
	  <td align="center">218968</td>
      <td align="center">A</td>
	  <td align="center">AAAGGG</td>
    </tr>
</tbody>
</table>

If using the original sequence, the "unsure" inversion to get the above concordance would be located at **position 181,255-209,114** (instead of position 173,721-216,640) 

**Contig2_58f18 (All MHC-Y)**:

*VarScan-Cons (SNPs - PacBio 10x CCS)*: **0 SNPs**

*VarScan-Cons (Indels - PacBio 10x CCS)*: **7 indels** (see below)

<table>
  <tbody>
    <tr>
      <th align="center">Position</th>
      <th align="center">Ref</th>
	  <th align="center">ALT</th>
	  <th align="center">Genotype</br>(diploid settings)</th>
    </tr>
    <tr>
	  <td align="center">1016</td>
      <td align="center">C</td>
	  <td align="center">CG</td>
	  <td align="center">0/1</td>
    </tr>
    <tr>
	  <td align="center">13326</td>
      <td align="center">T</td>
	  <td align="center">TG</td>
	  <td align="center">1/1</td>
    </tr>
    <tr>
	  <td align="center">18872</td>
      <td align="center">GGGAA</td>
	  <td align="center">G</td>
	  <td align="center">0/1</td>
    </tr>
    <tr>
	  <td align="center">18876</td>
      <td align="center">A</td>
	  <td align="center">AG</td>
	  <td align="center">0/1</td>
    </tr>
    <tr>
	  <td align="center">18950</td>
      <td align="center">A</td>
	  <td align="center">AG</td>
	  <td align="center">1/1</td>
    </tr>
    <tr>
	  <td align="center">46860</td>
      <td align="center">AG</td>
	  <td align="center">A</td>
	  <td align="center">0/1</td>
    </tr>
    <tr>
	  <td align="center">48099</td>
      <td align="center">CG</td>
	  <td align="center">C</td>
	  <td align="center">0/1</td>
    </tr>
</tbody>
</table>

**Contig3_34j16 (All MHC-Y)**:

*Pilon (Illumina)*: **0 differences**

*VarScan-Cons (SNPs + Indels, Illumina)*: **0 differences**

*Sanger Assembly*: **0 differences**

We believe Contig3/34j16 may be the most robust assembly, even though the fraction of possibly variable sites is small for the other assemblies (esepically if you focus on the MHC-Y region, because the NOR region is expected to have additional assembly errors)

## Method Details

**Step 0:** Index references (with *E. coli* [CP000948](https://www.ncbi.nlm.nih.gov/nuccore/CP000948) added for off-target reads)

 - `create_indices.py` (comment out 1 set of samples at a time)
 
**Step 1:** Align reads or Sanger assembly to reference

*Illumina Reads*: `Illumina_BWA_alignment_cluster.py` (comment out 1 set of samples at a time)

*PacBio 10x CCS Reads*: `PacBio_BWA_alignment_cluster.py` (comment out 1 set of samples at a time)

*Public / Sanger Assembly*: `BWA-MEM_alignment.py`(comment out 1 set of samples at a time; also creates .pileup file)

For public 173o1 sequence ([AC275299.1](https://www.ncbi.nlm.nih.gov/nuccore/AC275299.1)) inversion does not appear to occur at precisely the coordinates listed.  However, if you use a slightly different set of coordinates, you can create a sequence with a good match.

**Step 2:** Call variants or create .pileup file

*Pilon (Illumina Reads)*: `run_Pilon.py` (comment out 1 set of samples at a time)

*VarScan-Cons (Illumina Reads or PacBio 10x CCS Reads)*: `run_VarScan.sh` (comment out 1 set of samples at a time)

use warnings;
use strict;
use Bio::SeqIO;
use Bio::Seq;

my @ARS_aa_index = (57...84, 143...171);
my $in_FA = "IMGT_GenBank-alpha1alpha2.fasta";
my $ARS_FA_N = "IMGT_GenBank-alpha1alpha2-alphaHelices-nuc.fa";
my $nonARS_FA_N = "IMGT_GenBank-alpha1alpha2-nonAlphaHelices-nuc.fa";
my $ARS_FA_P = "IMGT_GenBank-alpha1alpha2-alphaHelices-pep.fa";
my $nonARS_FA_P = "IMGT_GenBank-alpha1alpha2-nonAlphaHelices-pep.fa";

#my @ARS_aa_index = (57...84);
#my $in_FA = "IMGT_GenBank-alpha1alpha2.fasta";
#my $ARS_FA_N = "IMGT_GenBank-alpha1-alphaHelix-nuc.fa";
#my $nonARS_FA_N = "IMGT_GenBank-alpha1-nonAlphaHelix-nuc.fa";
#my $ARS_FA_P = "IMGT_GenBank-alpha1-alphaHelix-pep.fa";
#my $nonARS_FA_P = "IMGT_GenBank-alpha1-nonAlphaHelix-pep.fa";

#my @ARS_aa_index = (143...171);
#my $in_FA = "IMGT_GenBank-alpha1alpha2.fasta";
#my $ARS_FA_N = "IMGT_GenBank-alpha2-alphaHelix-nuc.fa";
#my $nonARS_FA_N = "IMGT_GenBank-alpha2-nonAlphaHelix-nuc.fa";
#my $ARS_FA_P = "IMGT_GenBank-alpha2-alphaHelix-pep.fa";
#my $nonARS_FA_P = "IMGT_GenBank-alpha2-nonAlphaHelix-pep.fa";

#my @ARS_aa_index = (1...183);
#my $in_FA = "IMGT_GenBank-alpha1alpha2.fasta";
#my $ARS_FA_N = "IMGT_GenBank-alpha1alpha2-nuc.fa";
#my $nonARS_FA_N = "nothing-nuc.fa";
#my $ARS_FA_P = "IMGT_GenBank-alpha1alpha2-pep.fa";
#my $nonARS_FA_P = "nothing-pep.fa";

print scalar(@ARS_aa_index),"\n";

my %ARS_aa_index_hash;
for(my $i = 0; $i < scalar(@ARS_aa_index); $i++){
	$ARS_aa_index_hash{$ARS_aa_index[$i]}=""
}#end for(my $i = 0; $i <= scalar(@ARS_aa_index); $i++)


my %ARS_hash;
my %nonARS_hash;

open(ARS,">  $ARS_FA_N")||die("Cannot open $ARS_FA_N\n");
open(NARS,">  $nonARS_FA_N")||die("Cannot open $nonARS_FA_N\n");

open(ARST,">  $ARS_FA_P")||die("Cannot open $ARS_FA_P\n");
open(NARST,">  $nonARS_FA_P")||die("Cannot open $nonARS_FA_P\n");

my $seqio_obj = Bio::SeqIO->new(-file => $in_FA, 
								-format => "fasta" );						
while (my $seq_obj = $seqio_obj->next_seq){
	my $allele = $seq_obj->id;
	my $exon2_exon3 = $seq_obj->seq;
	
	my $temp_ARS_nuc = "";
	my $temp_nonARS_nuc = "";

	for(my $aa_index = 1; $aa_index <= length($exon2_exon3)/3; $aa_index++){
		my $nuc_index = $aa_index * 3 - 2;
		#print $nuc_index,"-",$aa_index,"\n";
		
		if(exists($ARS_aa_index_hash{$aa_index})){
			$temp_ARS_nuc .= substr($exon2_exon3,$nuc_index-1,3);
		}else{
			$temp_nonARS_nuc .= substr($exon2_exon3,$nuc_index-1,3);
		}#end else
	}#end for(my $i = 0; $i <= length($exon2_exon3); $i+=3)
	
	#ARS
	print ARS ">$allele\n$temp_ARS_nuc\n";
	my $translate_obj = Bio::Seq->new(-seq => $temp_ARS_nuc);
	print ARST ">$allele\n",$translate_obj->translate->seq,"\n";
	
	#non-ARS
	print NARS ">$allele\n$temp_nonARS_nuc\n";
	$translate_obj = Bio::Seq->new(-seq => $temp_nonARS_nuc);
	print NARST ">$allele\n",$translate_obj->translate->seq,"\n";	
}#end while (my $seq_obj = $seqio_obj->next_seq)

close(ARS);
close(NARS);

close(ARST);
close(NARST);
		
exit;
use warnings;
use strict;
use Bio::SeqIO;

my $in_FA = "truncated_galGal5_with_AllContigs.fa";
my $out_FA = "truncated_galGal5_with_AllContigs-reformat.fa";

open(FA,">  $out_FA")||die("Cannot open $out_FA\n");

my $seqio_obj = Bio::SeqIO->new(-file => $in_FA, 
								-format => "fasta" );							
while (my $seq_obj = $seqio_obj->next_seq){
	my $ref_id = $seq_obj->id;
	my $ref_seq = $seq_obj->seq;
	print "$ref_id...\n";
	print FA ">$ref_id\n$ref_seq\n";
}#end while (my $seq_obj = $seqio_obj->next_seq)

close(FA);
		
exit;
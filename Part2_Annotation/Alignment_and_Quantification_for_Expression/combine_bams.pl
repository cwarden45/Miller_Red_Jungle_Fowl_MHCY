use warnings;
use strict;

my $alignment_folder = "TopHat2-param2-FULL/Separate_Alignments";
my $combined_bam = "TopHat2-param2-FULL/PRJNA204941_Filtered_AllContigs.bam";

my $bam_list = "separate_bams.txt";

open(LIST, "> $bam_list") || die("Could not open  $bam_list!");

opendir DH, $alignment_folder or die "Failed to open $alignment_folder: $!";
my @files = readdir(DH);

foreach my $file (@files){
	if ($file =~ /.bam$/){
		my $full_path = "$alignment_folder/$file";
		print LIST "$full_path\n";
	}#end if ($file =~ /.bam$/)
}#end foreach my $file (@files)

my $command = "/opt/samtools-1.4/samtools merge -b $bam_list $combined_bam";
system($command);

$command = "/opt/samtools-1.4/samtools index $combined_bam";
system($command);

exit;
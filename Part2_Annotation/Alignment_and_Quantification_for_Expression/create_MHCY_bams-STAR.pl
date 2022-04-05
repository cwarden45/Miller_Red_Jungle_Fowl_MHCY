use warnings;
use strict;

#my $alignment_folder = "STAR-param9/Separate_Alignments";
#my $target_bed = "4contigs.bed";
#my $combined_bam = "STAR-param9/PRJNA204941_PostFilter_AllContigs.bam";

my $alignment_folder = "STAR-param12/Separate_Alignments";
my $target_bed = "4contigs.bed";
my $combined_bam = "STAR-param12/PRJNA204941_PostFilter_AllContigs.bam";

opendir DH, $alignment_folder or die "Failed to open $alignment_folder: $!";
my @files = readdir(DH);

foreach my $file (@files){
	if ($file =~ /SRR\d+.bam$/){
		print "$file\n";
		
		my $full_pathIN = "$alignment_folder/$file";

		my $full_pathT1 = $full_pathIN;
		$full_pathT1 =~ s/.bam$/_contig1.bam/;
		
		my $full_pathT2 = $full_pathIN;
		$full_pathT2 =~ s/.bam$/_contig2.bam/;

		my $full_pathT3 = $full_pathIN;
		$full_pathT3 =~ s/.bam$/_contig3.bam/;

		my $full_pathT4 = $full_pathIN;
		$full_pathT4 =~ s/.bam$/_contig4.bam/;
		
		my $full_pathOUT = $full_pathIN;
		$full_pathOUT =~ s/.bam$/_4contig.bam/;
		
		my $command = "/opt/samtools-1.4/samtools view -hb $full_pathIN Contig1:1-412374 > $full_pathT1";
		system($command);

		$command = "/opt/samtools-1.4/samtools view -hb $full_pathIN Contig2:1-148501 > $full_pathT2";
		system($command);

		$command = "/opt/samtools-1.4/samtools view -hb $full_pathIN Contig3:1-138921 > $full_pathT3";
		system($command);

		$command = "/opt/samtools-1.4/samtools view -hb $full_pathIN Contig4:1-45013 > $full_pathT4";
		system($command);

		$command = "/opt/samtools-1.4/samtools merge $full_pathOUT $full_pathT1 $full_pathT2 $full_pathT3 $full_pathT4";
		system($command);

		$command = "/opt/samtools-1.4/samtools index $full_pathOUT";
		system($command);

		$command = "rm $full_pathT1";
		system($command);

		$command = "rm $full_pathT2";
		system($command);
		
		$command = "rm $full_pathT3";
		system($command);

		$command = "rm $full_pathT4";
		system($command);

	}#end if ($file =~ /.bam$/)
}#end foreach my $file (@files)
closedir DH;

###      combine, searching for more specific ending    ####
#re-run file colletion, if the 4_contig files might not already exist
opendir DH, $alignment_folder or die "Failed to open $alignment_folder: $!";
my @files = readdir(DH);
closedir DH;

my $bam_list = "separate_bams-STAR_PostFilter.txt";

open(LIST, "> $bam_list") || die("Could not open  $bam_list!");

foreach my $file (@files){
	if ($file =~ /_4contig.bam$/){
		my $full_path = "$alignment_folder/$file";
		print LIST "$full_path\n";
	}#end if ($file =~ /.bam$/)
}#end foreach my $file (@files)

my $command = "/opt/samtools-1.4/samtools merge -b $bam_list $combined_bam";
system($command);

$command = "/opt/samtools-1.4/samtools index $combined_bam";
system($command);

exit;
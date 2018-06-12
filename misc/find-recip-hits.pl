#!/usr/bin/perl
use strict;

use Bio::SearchIO;

my $hits1 = parse_blast($ARGV[0]);
my $hits2 = parse_blast($ARGV[1]);

foreach my $seq1 (keys %{$hits1}) {
    my $seq1hit = $hits1->{$seq1};
    my $seq2hit = $hits2->{$seq1hit};


    if ( $seq2hit eq $seq1) {
	print $seq1 . "\t" . $seq1hit . "\n";

    } else {
	print STDERR "no reciprocal best hit for $seq1\n";
    }
}


sub parse_blast {
    my $fileName = shift;
    my $file = Bio::SearchIO->new(-file => $fileName, -format => "blast");
    my $hits = {};
    while (my $result = $file->next_result()) {
	my $hit = $result->next_hit();
	next if not defined $hit;
	$hits->{$result->query_name()} = $hit->name();

    }
    return $hits;
}

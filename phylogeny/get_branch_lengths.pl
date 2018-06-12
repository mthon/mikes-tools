#!/opt/local/bin/perl -w
use strict;
use Bio::TreeIO;

my $treeFile = Bio::TreeIO->new(-file=>$ARGV[0], 
				-format => 'newick');

my $tree = $treeFile->next_tree();
#my $rootNode = $tree->get_root_node();


foreach my $node ($tree->get_nodes() ) {
    my $newLen = round($node->branch_length() );
    $node->branch_length($newLen);
}

foreach my $node ($tree->get_leaf_nodes()) {

    my $height = get_brlen(0, $node);

    my $id = $node->id();
    print "$id $height\n";
    
}



my $outfile = Bio::TreeIO->new(-file=>">$ARGV[0].int.newick",
			       -format => "newick");
$outfile->write_tree($tree);

sub get_brlen {
    my ($length, $node) = @_;
    my $next_node = $node->ancestor();
    if ( defined $next_node) {
	$length += $node->branch_length();

	$length = get_brlen($length, $next_node);
    }
    return $length;
}

sub round {
    my($number) = shift;
    return int($number + .5);
}

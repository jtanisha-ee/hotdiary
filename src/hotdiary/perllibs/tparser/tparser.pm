package tparser::tparser;
use Exporter;

#use util::utils;
require Exporter;

@ISA = qw(Exporter);
@EXPORT = qw(replaceit strapp parseIt );

sub replaceit {
  my($line, $name, $data) = @_;
  $eline = $line;
  #system "echo \"name = $name\" >> /tmp/vars";
  #if ($name =~ /liveat2/) {
  #   system "echo \"Got liveat2 var data = $data\" >> /tmp/liveat2";
  #}
  $eline =~ s/\:$name\:/$data/g;
  return $eline;
}

sub strapp {
  my($prml, $prm) = @_;
  $prm =~ s/\?/___/g;
  return "$prml\?$prm";
}

sub parseIt {
  my($args, $d) = @_;
  (@hashargs) = split("\\?", $args);

  #print "args = ", $hashargs[0], "\n";
  #print "args = ", $hashargs[1], "\n";

  %arglist = ();   # may want to init this in distant future
  # currently, arglist is behaving like a global var even though
  # it is declared locally in this function. so it's hash elements
  # are remembered across calls to this function.
  foreach $i (@hashargs) {
     (@onearg) = split("\=", $i);
     $arglist{$onearg[0]} = $onearg[1];
     $arglist{$onearg[0]} =~ s/___/\?/g;
     $arglist{$onearg[0]} =~ s/\-\-\-/\=/g;
     #print "oneargp[0] = ", $onearg[0], "\n";
     #print "oneargp[1] = ", $onearg[1], "\n";
  }

 # foreach $i (keys %arglist) {
 #    print "$i = ", $arglist{$i}, "\n";
 # }

  open infiile, "<$arglist{'template'}";
  #print "infiile = ", $arglist{'template'}, "\n";
  if ($arglist{'templateout'} ne "") {
     open outfiile, ">$arglist{'templateout'}";
  }  else {
     system "echo \"templateout is null\" >> $ENV{HDHOME}/tmp/templateout";
  }
  #system "echo \"templateout = $arglist{'templateout'}\" >> /tmp/templateout";
  #print "outfiile = ", $arglist{'templateout'}, "\n";
  #print "expiry = $arglist{'expiry'}\n";
  while (<infiile>) {
     chop;
     $line = $_;
     $eline = $line;
     foreach $i (keys %arglist) {
        $eline = replaceit $eline, '\$' . $i, $arglist{$i};
     }
     if ($arglist{'templateout'} ne "") {
        print outfiile "$eline\n";
     } else {
        print "$eline\n";
     }
  }
  close outfiile;
  close infiile;
  if ($d != 1) {
     system "$ENV{HDEXECCGI}/execcleanproducts $arglist{'templateout'}";
  }
  #if (-f $arglist{'templateout'}) {
  #   system "echo \"The file $arglist{'templateout'} was not created by tparser.\" >> /usr/local/hotdiary/logs/templateout";
  #}
  return 0;
}

1;

__END__

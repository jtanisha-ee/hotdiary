package ParseTem::ParseTem;

sub replaceit {
  my($line, $name, $data) = @_;
  #print $line, $name, $data;
  $eline = "$line";
  if ($line=~/$name/) {
     ($prefix, $var, $postfix)=split(/:/);
     $eline = sprintf "%s%s%s\n", $prefix, $data, $postfix;
  }
  return $eline;
}

sub parseIt {
# parse the command line
#  &ReadParse(*input); 

  open infiile, "<$ENV{'template'}";
#  print "infiile = ", $ENV{'template'}, "\n";
  if ($ENV{'templateout'} ne "") {
     open outfiile, ">$ENV{'templateout'}";
  }
#  print "outfiile = ", $ENV{'templateout'}, "\n";
  while (<infiile>) {
     chop;
     $line = $_;
     $eline = $line;
     $eline = replaceit $eline, '\$login', $ENV{'login'};
     $eline = replaceit $eline, '\$biscuit', $ENV{'biscuit'};
     $eline = replaceit $eline, '\$password', $ENV{'password'};
     $eline = replaceit $eline, '\$label', $ENV{'label'};
     $eline = replaceit $eline, '\$actioncgi', 
	$ENV{'actioncgi'};
     $eline = replaceit $eline, '\$checkboxfield', $ENV{'checkboxfield'};
     $eline = replaceit $eline, '\$entryno', $ENV{'entryno'};
     $eline = replaceit $eline, '\$entrynfield', $ENV{'entrynfield'};
     $eline = replaceit $eline, '\$numentries', $ENV{'numentries'};
     $eline = replaceit $eline, '\$fname', $ENV{'fname'};
     $eline = replaceit $eline, '\$fnamfield', $ENV{'fnamfield'};
     $eline = replaceit $eline, '\$lname', $ENV{'lname'};
     $eline = replaceit $eline, '\$lnamfield', $ENV{'lnamfield'};
     $eline = replaceit $eline, '\$street', $ENV{'street'};
     $eline = replaceit $eline, '\$streefield', $ENV{'streefield'};
     $eline = replaceit $eline, '\$city', $ENV{'city'};
     $eline = replaceit $eline, '\$citfield', $ENV{'citfield'};
     $eline = replaceit $eline, '\$state', $ENV{'state'};
     $eline = replaceit $eline, '\$statfield', $ENV{'statfield'};
     $eline = replaceit $eline, '\$zipcode', $ENV{'zipcode'};
     $eline = replaceit $eline, '\$zipcodfield', $ENV{'zipcodfield'};
     $eline = replaceit $eline, '\$country', $ENV{'country'};
     $eline = replaceit $eline, '\$countrfield', $ENV{'countrfield'};
     $eline = replaceit $eline, '\$pager', $ENV{'pager'};
     $eline = replaceit $eline, '\$pagefield', $ENV{'pagefield'};
     $eline = replaceit $eline, '\$phone', $ENV{'phone'};
     $eline = replaceit $eline, '\$phonfield', $ENV{'phonfield'};
     $eline = replaceit $eline, '\$fax', $ENV{'fax'};
     $eline = replaceit $eline, '\$fafield', $ENV{'fafield'};
     $eline = replaceit $eline, '\$cellp', $ENV{'cellp'};
     $eline = replaceit $eline, '\$cphonfield', $ENV{'cphonfield'};
     $eline = replaceit $eline, '\$busp', $ENV{'busp'};
     $eline = replaceit $eline, '\$bphonfield', $ENV{'bphonfield'};
     $eline = replaceit $eline, '\$email', $ENV{'email'};
     $eline = replaceit $eline, '\$emaifield', $ENV{'emaifield'};
     $eline = replaceit $eline, '\$url', $ENV{'url'};
     $eline = replaceit $eline, '\$urfield', $ENV{'urfield'};
     $eline = replaceit $eline, '\$month', $ENV{'month'};
     $eline = replaceit $eline, '\$montfield', $ENV{'montfield'};
     $eline = replaceit $eline, '\$day', $ENV{'day'};
     $eline = replaceit $eline, '\$dafield', $ENV{'dafield'};
     $eline = replaceit $eline, '\$year', $ENV{'year'};
     $eline = replaceit $eline, '\$yeafield', $ENV{'yeafield'};
     $eline = replaceit $eline, '\$hour', $ENV{'hour'};
     $eline = replaceit $eline, '\$houfield', $ENV{'houfield'};
     $eline = replaceit $eline, '\$min', $ENV{'min'};
     $eline = replaceit $eline, '\$mifield', $ENV{'mifield'};
     $eline = replaceit $eline, '\$sec', $ENV{'sec'};
     $eline = replaceit $eline, '\$sefield', $ENV{'sefield'};
     $eline = replaceit $eline, '\$meridian', $ENV{'meridian'};
     $eline = replaceit $eline, '\$meridiafield', $ENV{'meridiafield'};
     $eline = replaceit $eline, '\$dhour', $ENV{'dhour'};
     $eline = replaceit $eline, '\$dhoufield', $ENV{'dhoufield'};
     $eline = replaceit $eline, '\$dmin', $ENV{'dmin'};
     $eline = replaceit $eline, '\$dmifield', $ENV{'dmifield'};
     $eline = replaceit $eline, '\$dtype', $ENV{'dtype'};
     $eline = replaceit $eline, '\$dtypfield', $ENV{'dtypfield'};
     $eline = replaceit $eline, '\$atype', $ENV{'atype'};
     $eline = replaceit $eline, '\$atypfield', $ENV{'atypfield'};
     $eline = replaceit $eline, '\$subject', $ENV{'subject'};
     $eline = replaceit $eline, '\$subjecfield', $ENV{'subjecfield'};
     $eline = replaceit $eline, '\$desc', $ENV{'desc'};
     $eline = replaceit $eline, '\$desfield', $ENV{'desfield'};
     $eline = replaceit $eline, '\$distribution', $ENV{'distribution'};
     $eline = replaceit $eline, '\$distributiofield', $ENV{'distributiofield'};
     $eline = replaceit $eline, '\$colledit', $ENV{'colledit'};
     $eline = replaceit $eline, '\$colledifield', $ENV{'colledifield'};
     $eline = replaceit $eline, '\$leftFrame', $ENV{'leftFrame'};
     $eline = replaceit $eline, '\$rightFrame', $ENV{'rightFrame'};

     if ($ENV{'templateout'} ne "") {
        print outfiile "$eline\n";
     } else {
        print "$eline\n";
     }
  }
  close outfiile;
  return 0;
}

1;

__END__

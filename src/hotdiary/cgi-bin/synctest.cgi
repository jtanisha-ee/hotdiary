#!/usr/bin/perl

$contents = qx{cat synctest.txt};

(@records) = split "\n", $contents;

$records[0] =~ s/\r//g;
(@columns) = split ",", $records[0];

foreach $i (@columns) {
   print "Column = $i\n";
}

#!/usr/bin/perl

use utils::utils;

$str = "snslksndlnfnlfnnsknsalkdnsakdnasldnlsdnl";
print "str = $str\n";
$len = 5;
$totlen = length($str);
$intr = $totlen / $len;
for ($i = 0; $i < $intr; $i++) {
   $tostr .= ((substr $str, ($i * $len), $len) . "<BR>");
}

$tostr = wrapstr $str, 5;
print "tostr = $tostr\n";

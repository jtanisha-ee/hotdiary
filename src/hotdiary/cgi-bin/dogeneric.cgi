#!/usr/bin/perl

# (C) Copyright 1998-1999 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

require "cgi-lib.pl";
use futils::futils;

&ReadParse(*input);

$pnum = $input{'pnum'};
if ($pnum eq "") {
   status "No programs to execute. Please check the configuration.";
   exit;
}
#system "echo \"pnum = $pnum\" >> /tmp/generic";
$parms = "/cgi-bin/$input{p0}?";
$i = 0;
for ($i = 1; $i < $pnum; $i = $i + 1) {
    $var = "p" . $i;
    $p = goodwebstr $input{$var};
    system "echo \"p = $p\" >> /tmp/generic";
    $valattr = "pattr" . $i;
    $valattr = $input{$valattr};
    system "echo \"valattr = $valattr\" >> /tmp/generic";
    if ($valattr eq "multsel") {
       $v = goodwebstr multselkeys $input, "$p";
    } else {
       $v = goodwebstr $input{$p};
    }
    #system "echo \"v = $v\" >> /tmp/generic";
    if ($i == 1) {
       $parms .= "$p=$v";
    } else {
       $parms .= "&$p=$v";
    }
}

$enum = $input{'enum'};
#system "echo \"enum = $enum\" >> /tmp/generic";
for ($j = 0; $j < $enum; $j = $j + 1) {
    $rhs = "re" . $j;
    $lhs = "le" . $j;
    $rp = $input{$rhs};
    #system "echo \"rp = $rp\" >> /tmp/generic";
    $lp = $input{$lhs};
    #system "echo \"lp = $lp\" >> /tmp/generic";
    $v = goodwebstr $ENV{$rp};
    if ($i == 0) {
       $parms .= "$lp=$v";
    } else {
       $parms .= "&$lp=$v";
    }
}

$firewall = $ENV{FIREWALL};
$proxyPort = $ENV{proxyPort};
$proxyHost = $ENV{proxyHost};
$proxySet = $ENV{proxySet};

#system "echo \"parms = $parms\" >> /tmp/generic";

system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal '$parms' '$firewall' '$proxyPort' '$proxyHost' '$proxySet'";
#system "java COM.hotdiary.calmgmtserver.CalAppClient \"$parms\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

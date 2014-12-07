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
$parms = "/cgi-bin/$input{p0}?";
for ($i = 1; $i < $pnum; $i = $i + 1) {
    $p = goodwebstr $input{p$i};
    $v = goodwebstr $input{$p};
    $parms .= "&$p=$v";
}

$enum = $input{'enum'};
for ($i = 0; $i < $enum; $i = $i + 1) {
    $p = goodwebstr $ENV{p$i};
    $v = goodwebstr $ENV{$p};
    $parms .= "&$p=$v";
}

$firewall = $ENV{FIREWALL};
$proxyPort = $ENV{proxyPort};
$proxyHost = $ENV{proxyHost};
$proxySet = $ENV{proxySet};

system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"$parms\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
system "java COM.hotdiary.calmgmtserver.CalAppClient \"$parms\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

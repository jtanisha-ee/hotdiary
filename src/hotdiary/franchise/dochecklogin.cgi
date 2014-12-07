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

$login = goodwebstr $input{'login'};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;

$result = qx{java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execchecklogin.cgi?login=$login\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"};

if ($result =~ /yes/) {
   print "1\n";
   exit;
}

if ($result =~ /no/) {
   print "0\n";
   exit;
}

print "-1\n";

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

$biscuit = $input{'biscuit'};
$calkey = goodwebstr $input{'calkey'};
$jp = goodwebstr $input{'jp'};

$rh = goodwebstr $ENV{CGISUBDIR};
$hs = goodwebstr $ENV{HTTPSUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;

system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execsearchgroupcal.cgi?biscuit=$biscuit&rh=$rh&calkey=$calkey&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"";
#system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execsearchgroupcal.cgi?biscuit=$biscuit&rh=$rh&calkey=$calkey&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

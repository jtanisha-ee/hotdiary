#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#


require "cgi-lib.pl";
use futils::futils;

&ReadParse(*input);

$f = $input{'f'};

if ($f eq "h") {
   system "cat $ENV{HDHOME}/content.html";
   system "cat /index.html";
   exit;
}

$rh = $ENV{CGISUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};

$login = qx{basename `pwd`};
$login =~ s/\n//g;
$entity = qx{basename `cd ..; pwd`};
$entity =~ s/\n//g;
if ($entity eq "groups") {
   $g = $login;
   $login = "";
}

$login = "\L$login";
$g = $login";

system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execcalclient.cgi?sc=p&l=$login&rh=$rh&HDLIC=$HDLIC&g=$g\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
$vdomain = $ENV{SERVER_NAME};
$hs = $ENV{HTTPSUBDIR};
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/proxy/execproxymergedwebpage.cgi?sc=p&l=$login&login=$login&rh=$rh&HDLIC=$HDLIC&g=$g&vdomain=$vdomain&hs=$hs\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

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
$edit = goodwebstr $input{'edit'};
$unsubscribe = goodwebstr $input{'unsubscribe'};
$radio1 = goodwebstr $input{'radio1'};
$jp = goodwebstr $input{jp};

$rh = $ENV{CGISUBDIR};
$hs = $ENV{HTTPSUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};

system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execeditsubscribegroupcal.cgi?biscuit=$biscuit&radio1=$radio1&rh=$rh&edit=$edit&unsubscribe=$unsubscribe&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execeditsubscribegroupcal.cgi?biscuit=$biscuit&radio1=$radio1&rh=$rh&edit=$edit&unsubscribe=$unsubscribe&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

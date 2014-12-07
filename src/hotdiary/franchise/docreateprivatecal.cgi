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
$hs = $ENV{HTTPSUBDIR};
$f = goodwebstr $input{'f'};
$ctype = goodwebstr $input{'ctype'};
$corg = goodwebstr $input{'corg'};
$calname = goodwebstr $input{'calname'};
$calname = "\L$calname";
$caltitle = goodwebstr $input{'caltitle'};
$calpassword = goodwebstr $input{'calpassword'};
$calrpassword = goodwebstr  $input{'calrpassword'};
$cdesc = goodwebstr  $input{'cdesc'};
$listed = goodwebstr $input{'listed'};
$readonly = goodwebstr $input{'readonly'};
$cpublish = goodwebstr  $input{'cpublish'};
$jp = goodwebstr $input{jp};

if ($cpublish eq "on") {
   if ($calname ne "") {
   if (!(-d "$ENV{HTTPHOME}/$hs/groups/$calname"))  {
      system "mkdir -p $ENV{HTTPHOME}/$hs/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/execcalclient.cgi")) {
         system "ln -s $ENV{HDHOME}/website/execcalclient.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/index.cgi")) {
         system "ln -s $ENV{HDHOME}/website/index.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDHOME}/website/webpage.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }            
   }
}

$rh = $ENV{CGISUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;

system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execcreateprivatecal.cgi?biscuit=$biscuit&f=$f&rh=$rh&ctype=$ctype&corg=$corg&calname=$calname&caltitle=$caltitle&calpassword=$calpassword&calrpassword=$calrpassword&cdesc=$cdesc&listed=$listed&cpublish=$cpublish&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&readonly=$readonly&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"";

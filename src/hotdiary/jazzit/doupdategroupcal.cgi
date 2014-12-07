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

$hs = $ENV{HTTPSUBDIR};
$biscuit = $input{'biscuit'};
$f = goodwebstr $input{'f'};
$ctype = goodwebstr $input{'ctype'};
$corg = goodwebstr $input{'corg'};
$calname = goodwebstr $input{'calname'};
$caltitle = goodwebstr $input{'caltitle'};
$calpassword = goodwebstr $input{'calpassword'};
$calrpassword = goodwebstr  $input{'calrpassword'};
$cdesc = goodwebstr  $input{'cdesc'};
$listed = goodwebstr $input{'listed'};
$readonly = goodwebstr $input{'readonly'};
$cpublish = goodwebstr  $input{'cpublish'};
$pgroups = goodwebstr  $input{'pgroups'};
$jp = goodwebstr  $input{'jp'};

if ($cpublish eq "on") {
   if ($calname ne "") {
   if (!(-d "$ENV{HTTPHOME}/$hs/groups/$calname"))  {
      system "mkdir -p $ENV{HTTPHOME}/$hs/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/index.cgi")) {
         system "ln -s $ENV{HDHOME}/website/index.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDHOME}/website/webpage.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }            
   }
} else {
   if ($calname ne "") {
      if (-d "$ENV{HTTPHOME}/$hs/groups/$calname")  {
# demented check
         if ($ENV{HTTPHOME}/$hs ne "") {
            system "rm -f $ENV{HTTPHOME}/$hs/groups/$calname/*";
            system "rmdir $ENV{HTTPHOME}/$hs/groups/$calname";
         }
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

system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execupdategroupcal.cgi?biscuit=$biscuit&f=$f&rh=$rh&ctype=$ctype&corg=$corg&calname=$calname&caltitle=$caltitle&calpassword=$calpassword&calrpassword=$calrpassword&cdesc=$cdesc&listed=$listed&pgroups=$pgroups&cpublish=$cpublish&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&readonly=$readonly&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execupdategroupcal.cgi?biscuit=$biscuit&f=$f&rh=$rh&ctype=$ctype&corg=$corg&calname=$calname&caltitle=$caltitle&calpassword=$calpassword&calrpassword=$calrpassword&cdesc=$cdesc&listed=$listed&pgroups=$pgroups&cpublish=$cpublish&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&readonly=$readonly&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

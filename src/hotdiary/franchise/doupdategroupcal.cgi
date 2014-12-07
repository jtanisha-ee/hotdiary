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
$contact = goodwebstr  $input{'contact'};
$listed = goodwebstr $input{'listed'};
$readonly = goodwebstr $input{'readonly'};
$cpublish = goodwebstr  $input{'cpublish'};
$pgroups = goodwebstr  $input{'pgroups'};
$jp = goodwebstr  $input{'jp'};
$jiveit = goodwebstr  $input{'jiveit'};
$publicedit = goodwebstr  $input{'publicedit'};

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
      if (!(-f "$ENV{HTTPHOME}/$hs/groups/$calname/execcalclient.cgi")) {
         system "ln -s $ENV{HDHOME}/website/execcalclient.cgi $ENV{HTTPHOME}/$hs/groups/$calname";
      }            
   }
   if (!(-f "$ENV{HTTPHOME}/$hs/contacts/$calname")) {
         system "mkdir -p $ENV{HTTPHOME}/$hs/contacts/$calname";
         system "chmod 755 $ENV{HTTPHOME}/$hs/contacts/$calname";
   }
   if (!(-f "$ENV{HTTPHOME}/$hs/contacts/$calname/index.cgi")) {
         system "ln -s $ENV{HDHOME}/website/contact_index.cgi $ENV{HTTPHOME}/$hs/contacts/$calname/index.cgi";
   }
   if (!(-f "$ENV{HTTPHOME}/$hs/contacts/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDHOME}/website/contact_webpage.cgi $ENV{HTTPHOME}/$hs/contacts/$calname/webpage.cgi";
   }
   if (!(-d "$ENV{HTTPHOME}/$hs/addressbook/$calname")) {
         system "ln -s $ENV{HTTPHOME}/$hs/contacts/$calname $ENV{HTTPHOME}/$hs/addressbook";
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
      if (-d "$ENV{HTTPHOME}/$hs/contacts/$calname")  {
         if ($ENV{HTTPHOME}/$hs ne "") {
            system "rm -f $ENV{HTTPHOME}/$hs/contacts/$calname/*";
            system "rmdir $ENV{HTTPHOME}/$hs/contacts/$calname";
            system "rm -f $ENV{HTTPHOME}/$hs/addressbook/$calname";
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

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;

system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execupdategroupcal.cgi?biscuit=$biscuit&f=$f&rh=$rh&ctype=$ctype&corg=$corg&calname=$calname&caltitle=$caltitle&calpassword=$calpassword&calrpassword=$calrpassword&cdesc=$cdesc&contact=$contact&listed=$listed&pgroups=$pgroups&cpublish=$cpublish&jiveit=$jiveit&publicedit=$publicedit&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&readonly=$readonly&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"";

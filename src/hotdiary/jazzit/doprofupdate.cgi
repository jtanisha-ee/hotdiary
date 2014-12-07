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

#system "cat $ENV{HDHOME}/content.html";
#$login = goodwebstr $input{'login'};

$hs = $ENV{HTTPSUBDIR};
$biscuit = goodwebstr $input{'biscuit'};
$action = goodwebstr $input{'action'};
$jp = goodwebstr $input{'jp'};
$login = goodwebstr $input{'login'};
$email = goodwebstr $input{'email'};
$acceptit = goodwebstr $input{'acceptit'};
$password = goodwebstr $input{'password'};
$rpassword = goodwebstr $input{'rpassword'};
$fname = goodwebstr $input{'fname'};
$lname = goodwebstr $input{'lname'};
$street = goodwebstr $input{'street'};
$city = goodwebstr $input{'city'};
$state = goodwebstr $input{'state'};
$zipcode = goodwebstr $input{'zipcode'};
$country = goodwebstr $input{'country'};
$phone = goodwebstr $input{'phone'};
$pager = goodwebstr $input{'pager'};
$fax = goodwebstr $input{'fax'};
$cellp = goodwebstr $input{'cellp'};
$busp = goodwebstr $input{'busp'};
$pagertype = goodwebstr $input{'pagertype'};
$url = goodwebstr $input{'url'};
$zone = goodwebstr $input{'zone'};

$checkid = goodwebstr $input{'checkid'};
$calpublish = goodwebstr $input{'calpublish'};

if ($calpublish eq "on") {
  if ($login ne "") {
    if (!(-d "$ENV{HTTPHOME}/$hs/members/$login")) {
      system "mkdir -p $ENV{HTTPHOME}/$hs/members/$login";
      if ($login ne "") {
         system "rm -f $ENV{HTTPHOME}/$hs/members/$login/*.cgi";
         system "ln -s $ENV{HDHOME}/website/index.cgi $ENV{HTTPHOME}/$hs/members/$login";
         system "ln -s $ENV{HDHOME}/website/webpage.cgi $ENV{HTTPHOME}/$hs/members/$login";
         system "ln -s $ENV{HDHOME}/website/execcalclient.cgi $ENV{HTTPHOME}/$hs/members/$login";
      } 
    } 
  }
} else {
   if ($login ne "") {
      if (-d "$ENV{HTTPHOME}/$hs/members/$login") {
         system "rm -rf $ENV{HTTPHOME}/$hs/members/$login";
      }
   } 
}

$informme = goodwebstr $input{'informme'};

#$cserver = goodwebstr $input{'cserver'};
#$hearaboutus = goodwebstr $input{'hearaboutus'};
#$upgrade = goodwebstr $input{'upgrade'};

$rh = $ENV{CGISUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};

system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/proxy/execproxyprofupdate.cgi?login=$login&biscuit=$biscuit&email=$email&acceptit=$acceptit&fname=$fname&zone=$zone&informme=$informme&calpublish=$calpublish&checkid=$checkid&url=$url&pagertype=$pagertype&busp=$busp&cellp=$cellp&fax=$fax&pager=$pager&phone=$phone&country=$country&zipcode=$zipcode&state=$state&city=$city&street=$street&lname=$lname&rpassword=$rpassword&password=$password&rh=$rh&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/proxy/execproxyprofupdate.cgi?login=$login&biscuit=$biscuit&email=$email&acceptit=$acceptit&fname=$fname&zone=$zone&informme=$informme&calpublish=$calpublish&checkid=$checkid&url=$url&pagertype=$pagertype&busp=$busp&cellp=$cellp&fax=$fax&pager=$pager&phone=$phone&country=$country&zipcode=$zipcode&state=$state&city=$city&street=$street&lname=$lname&rpassword=$rpassword&password=$password&rh=$rh&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

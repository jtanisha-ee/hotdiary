#!/usr/bin/perl

require "cgi-lib.pl";
use futils::futils;

&ReadParse(*input);

#system "cat $ENV{HDHOME}/content.html";
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
$checkid = goodwebstr $input{'checkid'};
$calpublish = goodwebstr $input{'calpublish'};
$informme = goodwebstr $input{'informme'};
$cserver = goodwebstr $input{'cserver'};
$hearaboutus = goodwebstr $input{'hearaboutus'};
$upgrade = goodwebstr $input{'upgrade'};
$zone = goodwebstr $input{'zone'};
$jp = goodwebstr $input{'jp'};

$rh = goodwebstr $ENV{CGISUBDIR};
$hs = goodwebstr $ENV{HTTPSUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};

$calpublish = goodwebstr $input{'calpublish'};

#if ($calpublish eq "on") {
#  if ($login ne "") {
#    if (!(-d "$ENV{HTTPHOME}/$hs/members/$login")) {
#      system "mkdir -p $ENV{HTTPHOME}/$hs/members/$login";
#      if ($login ne "") {
#         system "rm -f $ENV{HTTPHOME}/$hs/members/$login/*.cgi";
#         system "ln -s $ENV{HDHOME}/website/index.cgi $ENV{HTTPHOME}/$hs/members/$login";
#         system "ln -s $ENV{HDHOME}/website/webpage.cgi $ENV{HTTPHOME}/$hs/members/$login";
#         system "ln -s $ENV{HDHOME}/website/execcalclient.cgi $ENV{HTTPHOME}/$hs/members/$login";
#      }
#    }
#  }
#} else {
#   if ($login ne "") {
#      if (-d "$ENV{HTTPHOME}/$hs/members/$login") {
#         system "rm -rf $ENV{HTTPHOME}/$hs/members/$login";
#      }
#   }
#}


system "cat $ENV{HDHOME}/content.html";
#system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execregister.cgi?login=$login&email=$email&acceptit=$acceptit&fname=$fname&zone=$zone&upgrade=$upgrade&hearaboutus=$hearaboutus&cserver=$cserver&informme=$informme&calpublish=$calpublish&checkid=$checkid&url=$url&pagertype=$pagertype&busp=$busp&cellp=$cellp&fax=$fax&pager=$pager&phone=$phone&country=$country&zipcode=$zipcode&state=$state&city=$city&street=$street&lname=$lname&rpassword=$rpassword&password=$password&rh=$rh&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execregister.cgi?login=$login&email=$email&acceptit=$acceptit&fname=$fname&zone=$zone&upgrade=$upgrade&hearaboutus=$hearaboutus&cserver=$cserver&informme=$informme&calpublish=$calpublish&checkid=$checkid&url=$url&pagertype=$pagertype&busp=$busp&cellp=$cellp&fax=$fax&pager=$pager&phone=$phone&country=$country&zipcode=$zipcode&state=$state&city=$city&street=$street&lname=$lname&rpassword=$rpassword&password=$password&rh=$rh&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

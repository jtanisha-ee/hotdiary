#!/usr/bin/perl

require "cgi-lib.pl";
use futils::futils;

&ReadParse(*input);

$login = goodwebstr $input{'login'};
$email = goodwebstr $input{'email'};
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
$hearaboutus = goodwebstr $input{'hearaboutus'};
$informme = goodwebstr $input{'informme'};
$zone = goodwebstr $input{'zone'};

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


$result = qx{java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execquikreg.cgi?login=$login&email=$email&fname=$fname&zone=$zone&hearaboutus=$hearaboutus&informme=$informme&checkid=$checkid&url=$url&pagertype=$pagertype&busp=$busp&cellp=$cellp&fax=$fax&pager=$pager&phone=$phone&country=$country&zipcode=$zipcode&state=$state&city=$city&street=$street&lname=$lname&rpassword=$rpassword&password=$password&rh=$rh&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"};

(@goodhd) = split "\\|", $result;

print $goodhd[1];



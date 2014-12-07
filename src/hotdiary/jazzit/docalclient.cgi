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
$g = goodwebstr $input{'g'};
$pgroups = goodwebstr $input{'pgroups'};

$HDLIC = $ENV{HDLIC};
$rh = $ENV{CGISUBDIR};
$hs = $ENV{HTTPSUBDIR};
$firewall = $ENV{FIREWALL};
$proxyPort = $ENV{proxyPort};
$proxyHost = $ENV{proxyHost};
$proxySet = $ENV{proxySet};
$vdomain = $ENV{SERVER_NAME};

$ebanner = goodwebstr $input{'ebanner'};
$evenue = goodwebstr $input{'evenue'};
$eurl = goodwebstr $input{'eurl'};
$f = goodwebstr $input{'f'};
$jp = goodwebstr $input{'jp'};
if ($f ne "h") {
   $vw = goodwebstr $input{'vw'};
   $dy = goodwebstr $input{'dy'};
   $mo = goodwebstr $input{'mo'};
   $yr = goodwebstr  $input{'yr'};
   $h =  goodwebstr $input{'h'};
   $m =  goodwebstr $input{'m'};
   $a = goodwebstr $input{'a'};
   $en = goodwebstr $input{'en'};
   $jvw = goodwebstr $input{'jvw'};
   $month = goodwebstr $input{'month'};
   $day = goodwebstr $input{'day'};
   $year = goodwebstr $input{'year'};
   $zone = goodwebstr  $input{'zone'};
   $hour = goodwebstr $input{'hour'};
   $meridian = goodwebstr $input{'meridian'};
   $min = goodwebstr $input{'min'};
   $recurtype = goodwebstr $input{'recurtype'};
   $atype = goodwebstr $input{'atype'};
   $dtype = goodwebstr $input{'dtype'};
   $subject = goodwebstr $input{'subject'};
   $subject = goodwebstr trim $subject;
   $subject =~ s/\s/+/g;
   $dhour = goodwebstr $input{'dhour'};
   $dmin = goodwebstr $input{'dmin'};
   $free = goodwebstr $input{'free'};
   $share = goodwebstr $input{'share'};
   $desc = goodwebstr $input{'desc'};
   $desc = goodwebstr trim $desc;
   $desc =~ s/\s/+/g;
   $rurl = goodwebstr $input{'rurl'};
   $priority = goodwebstr $input{'priority'};
   $status = goodwebstr $input{'status'};
   $pinvited = goodwebstr $input{'pinvited'};
   system "echo \"came here = \" >> /tmp/dogeneric";
   system "echo \"pinvited = $pinvited\" >> /tmp/dogeneric";
   
     
} else {
   system "cat $ENV{HDHOME}/content.html";
   #system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/proxy/execproxylogout.cgi?biscuit=$biscuit&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
   system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/proxy/execproxylogout.cgi?biscuit=$biscuit&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
   #status("You have been logged out.");
   #system "cat $ENV{HTTPHOME}/$ENV{HTTPSUBDIR}/index.html";
   exit;
    
}

system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execcalclient.cgi?biscuit=$biscuit&dy=$dy&mo=$mo&yr=$yr&vw=$vw&h=$h&m=$m&a=$a&f=$f&en=$en&jvw=$jvw&rh=$rh&month=$month&day=$day&year=$year&zone=$zone&hour=$hour&meridian=$meridian&min=$min&recurtype=$recurtype&atype=$atype&dtype=$dtype&subject=$subject&dhour=$dhour&dmin=$dmin&free=$free&share=$share&rurl=$rurl&priority=$priority&status=$status&g=$g&pgroups=$pgroups&desc=$desc&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&ebanner=$ebanner&eurl=$eurl&evenue=$evenue&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
#system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execcalclient.cgi?biscuit=$biscuit&dy=$dy&mo=$mo&yr=$yr&vw=$vw&h=$h&m=$m&a=$a&f=$f&en=$en&jvw=$jvw&rh=$rh&month=$month&day=$day&year=$year&zone=$zone&hour=$hour&meridian=$meridian&min=$min&recurtype=$recurtype&atype=$atype&dtype=$dtype&subject=$subject&dhour=$dhour&dmin=$dmin&free=$free&share=$share&rurl=$rurl&priority=$priority&status=$status&g=$g&pgroups=$pgroups&desc=$desc&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&ebanner=$ebanner&eurl=$eurl&evenue=$evenue&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

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

$ebanner = goodwebstr $input{'ebanner'};
$evenue = goodwebstr $input{'evenue'};
$eurl = goodwebstr $input{'eurl'};
$jp = goodwebstr $input{'jp'};

$f = goodwebstr $input{'f'};
$rh = $ENV{CGISUBDIR};
$hs = $ENV{HTTPSUBDIR};
$firewall=$ENV{FIREWALL};
$proxyPort=$ENV{proxyPort};
$proxyHost=$ENV{proxyHost};
$proxySet=$ENV{proxySet};
$HDLIC=$ENV{HDLIC};
$vdomain=$ENV{SERVER_NAME};
if ($f ne "h") {
   $login = goodwebstr $input{'l'};
   $g = goodwebstr $input{'g'};
   $vw = goodwebstr $input{'vw'};
   $dy = goodwebstr $input{'dy'};
   $mo = goodwebstr $input{'mo'};
   $yr = goodwebstr $input{'yr'};
   $h = goodwebstr $input{'h'};
   $m = goodwebstr $input{'m'};
   $a = goodwebstr $input{'a'};
   $en = goodwebstr $input{'en'};
   $jvw = goodwebstr $input{'jvw'};
   $month = goodwebstr $input{'month'};
   $day = goodwebstr $input{'day'};
   $year =goodwebstr  $input{'year'};
   $zone = goodwebstr $input{'zone'};
   $hour = goodwebstr $input{'hour'};
   $meridian = goodwebstr $input{'meridian'};
   $min = goodwebstr $input{'min'};
   $recurtype = goodwebstr $input{'recurtype'};
   $atype = goodwebstr $input{'atype'};
   $dtype = goodwebstr $input{'dtype'};
   $subject = goodwebstr $input{'subject'};
   $subject = goodwebstr trim $subject;
   $subject =~ s/\s/+/g;
   $dhour =goodwebstr  $input{'dhour'};
   $dmin = goodwebstr $input{'dmin'};
   $free = goodwebstr $input{'free'};
   $share = goodwebstr $input{'share'};
   $desc = goodwebstr $input{'desc'};
   $desc = goodwebstr trim $desc;
   $desc =~ s/\s/+/g;
   $rurl = goodwebstr  $input{'rurl'};
   $priority = goodwebstr  $input{'priority'};
   $status = goodwebstr $input{'status'};
   $evtbanner = goodwebstr $input{'evtbanner'};
     
} else {
   system "cat $ENV{HDHOME}/content.html"; 
   #system "cat ../../index.html"; 
   system "cat $ENV{DOCUMENT_ROOT}/$hs/index.html"; 
   exit;
    
}

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;


system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execmgcalclient.cgi?l=$login&g=$g&sc=p&dy=$dy&mo=$mo&yr=$yr&vw=$vw&h=$h&m=$m&a=$a&f=$f&en=$en&jvw=$jvw&rh=$rh&month=$month&day=$day&year=$year&zone=$zone&hour=$hour&meridian=$meridian&min=$min&recurtype=$recurtype&atype=$atype&dtype=$dtype&subject=$subject&dhour=$dhour&dmin=$dmin&free=$free&share=$share&rurl=$rurl&priority=$priority&status=$status&desc=$desc&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&ebanner=$ebanner&evtbanner=$evtbanner&evenue=$evenue&eurl=$eurl&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"";
#system "java COM.hotdiary.calmgmtserver.CalAppClient \"/cgi-bin/execcalclient.cgi?l=$login&g=$g&sc=p&dy=$dy&mo=$mo&yr=$yr&vw=$vw&h=$h&m=$m&a=$a&f=$f&en=$en&jvw=$jvw&rh=$rh&month=$month&day=$day&year=$year&zone=$zone&hour=$hour&meridian=$meridian&min=$min&recurtype=$recurtype&atype=$atype&dtype=$dtype&subject=$subject&dhour=$dhour&dmin=$dmin&free=$free&share=$share&rurl=$rurl&priority=$priority&status=$status&desc=$desc&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&ebanner=$ebanner&evenue=$evenue&eurl=$eurl&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";

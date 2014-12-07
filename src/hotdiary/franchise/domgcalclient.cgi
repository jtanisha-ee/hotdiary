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
$pw = goodwebstr $input{pw};

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
   $evtbanner = goodwebstr $input{'evtbanner'};

   $type = goodwebstr $input{'type'};
   #system "echo \"type = $type\" >> /tmp/dogeneric";
   
   $people = goodwebstr $input{'people'};
   $bizpeople = goodwebstr $input{'bizpeople'};
   $groups = goodwebstr $input{'groups'};
   $bizresource = goodwebstr $input{'bizresource'};
   $bizmem = goodwebstr $input{'bizmem'};
   $bizteams = goodwebstr $input{'bizteams'};
   $businesses = goodwebstr $input{'businesses'};

   (@hshpeople) = split("%20", $people);
   (@hshbizpeople) = split("%20", $bizpeople);
   (@hshgroups) = split("%20", $groups);
   (@hshbizresource) = split("%20", $bizresource);
   (@hshbizmem) = split("%20", $bizmem);
   (@hshbizteams) = split("%20", $bizteams);


   $peoplevals = "";
   for ($i =0; $i <= $#hshpeople; $i = $i + 1 ) {
      $peoplevals .= goodwebstr $input{$hshpeople[$i]}; 
      $peoplevals .= "-";
      #system "echo \"$hshpeople[$i] = $peoplevals\" >> /tmp/dogeneric";
   }

   ## these should not have goodwebstr as goodwebstr substitutes - to %2d

   for ($i =0; $i <= $#hshbizpeople; $i = $i + 1 ) {
      $hshbizpeople[$i] =~ s/\%2d/-/g;
      $bizpeoplevals .= $input{$hshbizpeople[$i]}; 
      $bizpeoplevals .= "-";
      #system "echo \"biz $hshbizpeople[$i] = $bizpeoplevals\" >> /tmp/dogeneric";
   }

   for ($i =0; $i <= $#hshgroups; $i = $i + 1 ) {
      $hshgroups[$i] =~ s/\%2d/-/g;
      $groupvals .= $input{$hshgroups[$i]}; 
      $groupvals .= "-";
      #system "echo \"$hshgroups[$i] = $groupvals\" >> /tmp/dogeneric";
   }
   
   for ($i =0; $i <= $#hshbizresource; $i = $i + 1 ) {
      $hshbizresource[$i] =~ s/\%2d/-/g;
      $bizresourcevals .= $input{$hshbizresource[$i]}; 
      $bizresourcevals .= "-";
      #system "echo \"$hshbizresource[$i] = $bizresourcevals\" >> /tmp/dogeneric";
   }
   
   for ($i =0; $i <= $#hshbizmem; $i = $i + 1 ) {
      $hshbizmem[$i] =~ s/\%2d/-/g;
      $bizmemvals .= $input{$hshbizmem[$i]}; 
      $bizmemvals .= "-";
      #system "echo \"$hshbizmem[$i] = $bizmemvals \n \" >> /tmp/dogeneric";
   }
   for ($i =0; $i <= $#hshbizteams; $i = $i + 1 ) {
      $hshbizteams[$i] =~ s/\%2d/-/g;
      $bizteamvals .= $input{$hshbizteams[$i]}; 
      $bizteamvals .= "-";
      #system "echo \"$hshbizteams[$i] = $bizteamvals\" >> /tmp/dogeneric";
   }

   $groupvals = goodwebstr $groupvals;
   $bizteamvals = goodwebstr $bizteamvals;
   $bizmemvals = goodwebstr $bizmemvals;
   $bizresourcevals = goodwebstr $bizresourcevals;
   $bizpeoplevals = goodwebstr $bizpeoplevals;
   $peoplevals = goodwebstr $peoplevals;

   #system "echo \"rem = $rem\" >> /tmp/dogeneric";

   #system "echo \"docalclient()\" >> /tmp/dogeneric";
   #system "echo \"smitha = $smitha\" >> /tmp/dogeneric";
   #system "echo \"numpeople = $#hshpeople\" >> /tmp/dogeneric";

   #system "echo \"people = $people\" >> /tmp/dogeneric";
   #system "echo \"bizpeople = $bizpeople\" >> /tmp/dogeneric";
   #system "echo \"groups = $groups\" >> /tmp/dogeneric";
   #system "echo \"bizresource = $bizresource\" >> /tmp/dogeneric";
   #system "echo \"bizmem = $bizmem\" >> /tmp/dogeneric";
   #system "echo \"bizteams = $bizteams\" >> /tmp/dogeneric";
     
} else {
   system "cat $ENV{HDHOME}/content.html";
   system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/proxy/execproxylogout.cgi?biscuit=$biscuit&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
   #status("You have been logged out.");
   #system "cat $ENV{HTTPHOME}/$ENV{HTTPSUBDIR}/index.html";
   exit;
    
}

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;


system "cat $ENV{HDHOME}/content.html";
system "java COM.hotdiary.franchise.FetchCal \"/cgi-bin/execmgcalclient.cgi?biscuit=$biscuit&dy=$dy&mo=$mo&yr=$yr&vw=$vw&h=$h&m=$m&a=$a&f=$f&en=$en&pw=$pw&jvw=$jvw&rh=$rh&month=$month&day=$day&year=$year&zone=$zone&hour=$hour&meridian=$meridian&min=$min&recurtype=$recurtype&atype=$atype&dtype=$dtype&subject=$subject&dhour=$dhour&dmin=$dmin&free=$free&share=$share&rurl=$rurl&priority=$priority&status=$status&g=$g&pgroups=$pgroups&desc=$desc&type=$type&people=$people&peoplevals=$peoplevals&businesses=$businesses&bizpeople=$bizpeople&bizpeoplevals=$bizpeoplevals&groups=$groups&groupvals=$groupvals&bizresource=$bizresource&bizresourcevals=$bizresourcevals&bizmem=$bizmem&bizmemvals=$bizmemvals&bizteams=$bizteams&bizteamvals=$bizteamvals&HDLIC=$HDLIC&vdomain=$vdomain&hs=$hs&evtbanner=$evtbanner&ebanner=$ebanner&eurl=$eurl&evenue=$evenue&jp=$jp\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\" \"$ip\"";

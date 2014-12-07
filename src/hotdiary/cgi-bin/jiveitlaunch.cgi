#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: jiveitlaunch.cgi
# Purpose: Launches the top page of JiveIt
# 
# Creation Date: 08-14-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

$jp = $input{jp};
$alphjp = substr $jp, 0, 1;
$alphjp = $alphjp . '-index';

# bind login table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account', 'topleft',
           'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

$page = $input{page};

if ($page eq "register") {
   tie %jivetab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/jivetab",
             SUFIX => '.rec',
             SCHEMA => {
             ORDER => ['url', 'logo', 'title', 'banner',
                'regusers', 'account', 'topleft', 'topright',
                'middleright', 'bottomleft', 'bottomright'] };
   $prml = "";
   if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitregister.html") {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitregister.html";
   } else {
      $template = "$ENV{HDTMPL}/jiveitregister.html";
   }
   $prml = strapp $prml, "template=$template";
   $rtime = getkeys();
   $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/jiveit-$rtime-$$.html";
   $prml = strapp $prml, "jp=$jp";
   $titl = $jivetab{$jp}{title};
   $prml = strapp $prml, "title=$titl";
   parseIt $prml;
   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHOME}/tmp/jiveit-$rtime-$$.html";
   exit;
}

if ($jp eq "") {
   $jp = "buddie";
}

$prml = "";
if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/jiveit.html") {
   $template = "$ENV{HDDATA}/$alphjp/$jp/templates/jiveit.html";
} else {
   $template = "$ENV{HDTMPL}/jiveit.html";
}

#$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveit.html";
$prml = strapp $prml, "template=$template";
$rtime = getkeys();
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/jiveit-$rtime-$$.html";

$prml = strapp $prml, "jp=$jp";
$frompage = $ENV{'HTTP_REFERER'};
hddebug "JiveIt! Customer Forwarded from $frompage";

if (!(exists $jivetab{$jp})) {
   status("Invalid JiveIt Partner ID ($jp). You must edit the JiveIt HTML page and enter a valid JiveIt Partner ID in all relevant places. Your JiveIt Partner ID is your member login on 1800calendar.com. If you do not have a member login on 1800calendar.com, please register one.");
   exit; 
}

$jiveitlogo = adjusturl $jivetab{$jp}{logo};
$jiveittitle = adjusturl $jivetab{$jp}{title};
$jiveitbanner = adjusturl $jivetab{$jp}{banner};
$topleft = adjusturl $jivetab{$jp}{topleft};
$topright = adjusturl $jivetab{$jp}{topright};
$middleright = adjusturl $jivetab{$jp}{middleright};
$bottomleft = adjusturl $jivetab{$jp}{bottomleft};
$bottomright = adjusturl $jivetab{$jp}{bottomright};

$prml = strapp $prml, "jiveitlogo=$jiveitlogo";
$prml = strapp $prml, "jiveittitle=$jiveittitle";
$prml = strapp $prml, "jiveitbanner=$jiveitbanner";
$prml = strapp $prml, "topleft=$topleft";
$prml = strapp $prml, "topright=$topright";
$prml = strapp $prml, "middleright=$middleright";
$prml = strapp $prml, "bottomleft=$bottomleft";
$prml = strapp $prml, "bottomright=$bottomright";
$titl = $jivetab{$jp}{title};
$prml = strapp $prml, "title=$titl";
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHOME}/tmp/jiveit-$rtime-$$.html";

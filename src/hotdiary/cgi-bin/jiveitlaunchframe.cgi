#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: jiveitlaunchframe.cgi
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

# bind login table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
	'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };


$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitleftframe.html";
$rtime = getkeys();
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/jiveitleftframe-$rtime-$$.html";

if ($jp eq "") {
   $jp = "buddie";
}

$prml = strapp $prml, "jp=$jp";
if ($jp eq "smitha") {
   $prml = strapp $prml, "commerceportal=Commerce Portal";
} else {
   $prml = strapp $prml, "commerceportal=";
}


if (!(exists $jivetab{$jp})) {
   status("Invalid JiveIt Partner ID ($jp). You must edit the JiveIt HTML page and enter a valid JiveIt Partner ID in all relevant places.");
   exit; 
}

$prml = strapp $prml, "home=$jivetab{$jp}{url}";
#$url = adjusturl "http://www.hotdiary.com/cgi-bin/execjiveitlaunchpage.cgi?url=http://www.techmall.com";
#$prml = strapp $prml, "news=$url";
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHOME}/tmp/jiveitleftframe-$rtime-$$.html";

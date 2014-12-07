#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: industrynews.cgi
# Purpose: Launches the top page of News
# 
# Creation Date: 10-15-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

tie %newstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/newstab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'login', 'password', 'reldate', 'month',
        'day', 'title', 'status', 'release'] };


$prml = "";
$toc = "<TABLE BGCOLOR=ffffff CELLPADDING=5 CELLSPACING=0 WIDTH=\"100%\" BORDER=0>";
sub numerically { $b <=> $a; }
foreach $article (sort numerically keys %newstab) {
   if ($newstab{$article}{status} eq "approved") {
      $month = getmonthstr $newstab{$article}{month};
      $toc .=  "<TR BGCOLOR=ffffff><TD BGCOLOR=ffffff><FONT FACE=Verdana SIZE=2>$month $newstab{$article}{day}</FONT></TD><TD BGCOLOR=ffffff>&nbsp;</TD><TD BGCOLOR=ffffff><FONT FACE=Verdana SIZE=2><a href=\"/cgi-bin/execshowarticle.cgi?article=$article\">$newstab{$article}{title}</FONT></TD></TR>"; 
   }
}
$toc .= "</TABLE>";
$toc = adjusturl $toc;
$prml = strapp $prml, "template=$ENV{HDTMPL}/newspage.html";
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/newspage-$$.html";
$logo = adjusturl "<a href=\"http://www.hotdiary.com\"><IMG SRC=\"/images/newhdlogo.gif\" BORDER=0></a>";
$prml = strapp $prml, "logo=$logo";
$prml = strapp $prml, "toc=$toc";
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHOME}/tmp/newspage-$$.html";

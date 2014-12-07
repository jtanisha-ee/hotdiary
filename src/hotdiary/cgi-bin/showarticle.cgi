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

$article = $input{article};
if (!exists $newstab{$article}) {
   status "The article you requested cannot be found. Please click <a href=\"http://www.hotdiary.com/inews.cgi?\">here</a> to see all the articles.";
   exit;
}

$referer = $ENV{HTTP_REFERER};
hddebug "NewsDiary Visitor From: $referer";

$title = $newstab{$article}{title};
$text = adjusturl $newstab{$article}{release};

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/showarticle.html";
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/showarticle-$$.html";
$logo = adjusturl "<IMG SRC=\"/images/newhdlogo.gif\" BORDER=0 ALT=\"Go To NewsDiary Home\">";
$prml = strapp $prml, "logo=$logo";
$prml = strapp $prml, "title=$title";
$text =~ s/\n/<p>/g;
$prml = strapp $prml, "text=$text";
$prml = strapp $prml, "link=$article";
parseIt $prml;

system "cp $ENV{HDHOME}/tmp/showarticle-$$.html $ENV{HTTPHOME}/html/hd/news/$article.html";
system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHOME}/tmp/showarticle-$$.html";

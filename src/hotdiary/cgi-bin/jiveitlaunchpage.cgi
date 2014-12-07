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

$url = $input{url};

if ($url ne "http://www.techmall.com") {
   status("Security violation. This url ($url) cannot be invoked. Message has been sent to hotdiary.com");
}

system "cat $ENV{HDTMPL}/content.html";
system "java COM.hotdiary.main.ExecCGIURL \"$url\""

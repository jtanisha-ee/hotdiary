#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


#
# FileName: profile.cgi
# Purpose: This program uses dataplates like other programs and checks for
#          user login and displays appropriate menus and error messages.
#
# Creation Date: 10-09-97
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
#use UNIVERSAL qw(isa);
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   
#session timeout in secs
   $SESSION_TIMEOUT = 3600;
   
   $prml = "";
   #label = "Personal Profile";
   #$prml = strapp $prml, "label=$label";
   #$prml = strapp $prml, "template=$ENV{HDTMPL}/profile.html";
   $url = adjusturl "/cgi-bin/calendar/execprofile.cgi?";
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHDREP}/proxy_login.html";
}

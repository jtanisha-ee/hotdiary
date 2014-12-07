#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: trackvisitors.cgi
# Purpose: This program is used for rendering async images
# 
# Creation Date: 01-23-2000
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use tp::tp;
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use LWP::UserAgent;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   $referer = $ENV{HTTP_REFERER};
   hddebug "HotDiary Visitor From: $referer";
   print "Content-Type: image/gif";
   print "\n\n";
   $ua = LWP::UserAgent->new;
   $request = HTTP::Request->new(GET => "$hddomain/images/nothing.gif");
   $response = $ua->request($request);
   if ($response->is_success) {
      print $response->content;
   } else {
      status "Bad luck this time";
   }
}

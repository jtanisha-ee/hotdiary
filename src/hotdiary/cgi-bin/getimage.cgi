#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: getimage.cgi
# Purpose: This program is used for rendering async images
# 
# Creation Date: 04-22-99
# Created by: Smitha Gudur & Manoj Joshi
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

   $imageurl = $input{'imageurl'};
   $member = $input{'member'};

   hddebug "Forwarding reciprocal hits to $member by accessing $imageurl";
   hddebug "Image Impression from $ENV{HTTP_REFERER}";

   print "Content-Type: image/gif";
   print "\n\n";
   $ua = LWP::UserAgent->new;
   $request = HTTP::Request->new(GET => "$imageurl");
   $response = $ua->request($request);
   if ($response->is_success) {
      print $response->content;
   } else {
      status "Bad luck this time";
   }
}

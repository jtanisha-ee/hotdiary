#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: renderimage.cgi
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

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner',
         'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   tie %moneytab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/moneytab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['login', 'account', 'comment', 'approved'] };

   $referer = $ENV{HTTP_REFERER};
   hddebug "Publisher for HotDiary advertisement from: $referer";

   print "Content-Type: image/gif";
   print "\n\n";
   $ua = LWP::UserAgent->new;
   $rand = rand 4;
   $rand = $rand % 10;
   if ($rand == 0) {
      $rand = 4;
   }
   hddebug "banner$rand.gif";
 
   $request = HTTP::Request->new(GET => "http://www.hotdiary.com/images/banner$rand.gif");
   $response = $ua->request($request);
   if ($response->is_success) {
      print $response->content;
   } else {
      status "Bad luck this time";
   }
}

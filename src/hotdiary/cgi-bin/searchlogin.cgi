#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: searchlogin.cgi
# Purpose:  rewards program
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

   print "Based on the email address you have supplied, we have found the following member accounts in our database that belong to you. Please use the My Account utility again to retrieve your password and activation code based on the member login information below.\n\n";
   $cnt = 0;
   foreach $login (keys %logtab) {
      $em = "\L$logtab{$login}{email}";
      $ar = "\L$ARGV[0]";
      if ($em =~ /$ar/) {
         print "Found match = $login\n";
      }
      $cnt += 1;
      if ( ($cnt % 500) == 0) {
         qx{sleep 3};
      }
   }
   print "If no matches were found, your email address may not exist in our database. In such an event, you may want to register with HotDiary using the Register utility.\n";

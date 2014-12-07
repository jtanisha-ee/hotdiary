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
# FileName: rewardsum.cgi
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

   tie %moneytab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/moneytab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['login', 'account', 'comment', 'approved'] };

   $rewardsum = 0;
   foreach $login (keys %moneytab) {
      if ( ($login ne "manoj") && ($login ne "smitha") && ($login ne "jjenner") && ($login ne "buddie") && ($login ne "mjoshi") ) {
         if ($moneytab{$login}{approved} eq "true") {
            $rewardsum = $rewardsum + $moneytab{$login}{account};
         } else {
            $pendingrewardsum = $pendingrewardsum + $moneytab{$login}{account};
         }
      }
   }
   $rewardsum = $rewardsum / 100;
   print "Approved Reward Sum = " . '$' . "$rewardsum\n";
   $pendingrewardsum = $pendingrewardsum / 100;
   print "Pending Reward Sum = " . '$' . "$pendingrewardsum\n";

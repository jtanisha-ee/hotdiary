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
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 
        'referer'] };

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
       ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                 'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };


   $field = "\L$ARGV[0]";
   
   $login = "amatov";
   foreach $login (keys %logtab) {
      if (exists $surveytab{$login}) {
         if ($surveytab{$login}{hearaboutus} =~ /Windows/) {
            print $login, '.rec', "\n";
         }
      }
      #$em = trim "\L$logtab{$login}{$field}";
      #if ($em eq "") {
      #   print "Found match = $login\n";
      #   $logtab{$login}{zone} = "-8";
      #}
   }
  
   #tied(%logtab)->sync();

#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: addraddsearch.cgi
# Purpose: it adds and searches the addresses.                  
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

  # Read in all the variables set by the form
  &ReadParse(*input);
  
# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      


   #foreach $login (keys %logtab) {  
      $login = $ARGV[0];
      if (!-d "$ENV{HDDATA}/$login/addrtab") {
	 next;
      }
      # bind address table vars
      tie %addrtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$login/addrtab",
      SUFIX => '.rec', 
      SCHEMA => { 
           ORDER => ['entryno', 'login', 'fname', 'lname', 'street', 
           'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
           'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
           'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };


      hddebug "login = $login";
      foreach $entry (keys %addrtab) {
	 if ($addrtab{$entry}{entryno} eq "") {
  	   system "echo \" bad entryno field for $login = $entry\" >> /tmp/badrec.txt";
	   $addrtab{$entry}{entryno} = $entry;
           tied(%addrtab)->sync();
	 }
	 if ($addrtab{$entry}{login} eq "") {
  	   system "echo \" bad login field for $login = $entry\" >> /tmp/badrec.txt";
	   $addrtab{$entry}{login} = $login;
           tied(%addrtab)->sync();
	 }
      }
   #}
}

#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: purchaseadspace.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 
#


require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   $ind = $input{ind};

   tie %chattab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDHOME}/java/chat/chattab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['line'] };      

   print "Content-type: text/plain\n\n";
   if (exists $chattab{$ind}) {
      $line = '[?]' . $chattab{$ind}{line};
      $line =~ s/\n//g;
      $line =~ s/\r//g;
      print $line;
      #hddebug "DiaryChat: $line";
   } else {
      print " ";
   }
   $rand = rand 10;
   $rand = $rand % 10;
   #if ($rand == 3) {
   #   hddebug "NEW USER REGISTRATION";
   #}
 }

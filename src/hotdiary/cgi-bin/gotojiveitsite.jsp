#!/usr/bin/perl

#
# (C) Copyright 2001 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: gotojiveitsite.jsp
# Purpose: Got to a JiveIt Member site
# Creation Date: 07-11-2001
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

   hddebug ("gotojiveitsite.jsp");

   $jp = $input{jp}; 
   hddebug "jp = $jp";

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
   if (!exists $jivetab{$jp}) {
      status "JiveIt! Site for $jp does not exist! <a href=/>Click here</a> to go to HotDiary.";
      exit;
   }

   print "Location: http://www.1800calendar.com/index.cgi?jp=$jp\n\n";

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
# FileName: gotojiveitadmin.jsp
# Purpose: Got to a JiveIt Admin site
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

   hddebug ("gotojiveitadmin.jsp");

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
      status "JiveIt! site for $jp does not exist! Click <a href=/jiveitauth.html>here</a> to create a JiveIt! site.";
      exit;
   }

   print "Location: http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$jp\n\n";

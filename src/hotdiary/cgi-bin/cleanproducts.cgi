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
# FileName: cleanproducts.cgi
# Purpose: it cleans products file so it cannot be downloaded twice
# Creation Date: 02-16-2000
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
   hddebug "cleanproducts.cgi";
  
   $wfile = $ARGV[0];
   #hddebug "wfile = $wfile";
   $sleeptime = $ARGV[1];
   if ($sleeptime eq "") {
      $sleeptime = 5;
   }
   $sleeptime = 500;
   hddebug "Sleeping $sleeptime seconds before removing $wfile";
   qx{sleep $sleeptime};

   system "rm -f $wfile";
   hddebug "Removed file $wfile";
}


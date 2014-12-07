#!/usr/bin/perl


# Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: lwpupl.cgi
# Purpose: lwpupl program for custom files upload 
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;


# parse the command line
   &ReadParse(*input);
   hddebug("lwpupl.cgi");

   $contents = $input{'uploadfile'};
   $len = length $contents;
   hddebug "len = $len";
   open touthandle, ">$ENV{HDHOME}/tmp/lwpupload-$$";
   printf touthandle "%s", $contents;
   close touthandle;
   print "Content-type: text/html\n\n";
   print "Success";

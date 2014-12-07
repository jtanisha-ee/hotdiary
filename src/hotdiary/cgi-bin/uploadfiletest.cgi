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
# FileName: uploadfile.cgi
# Purpose: Top screen for hotdiary carryon
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
   hddebug("uploadfile.cgi");

   $login = "smitha";

   $uploadname = $in{'uploadname'};
   hddebug "filename = $uploadname";
   $uploadname = "btsmib2";
   if (notCarryOnName($uploadname)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9) and a single dot(.) in a filename ($uploadname) $msg.");
      exit;
   }

   if ( ($uploadname =~ /\.\./) || ($uploadname =~ /\~/) ) {
    status("$login: Invalid directory specification ($uploadname). HotDiary Security Alert.");
    exit;
   }    
   if ( (index $uploadname, '.') != -1 ) {
      (@compo) = split '\.', $uploadname;
      if ($#compo > 1) {
         status "Invalid file name suffix. Please enter file of the form \"myfile.doc\" or simply myfile.";
         exit;
      }
      if ( ($compo[0] eq "") || ($compo[1] eq "") ) {
         status "Invalid file name. Please enter file of the form \"myfile.doc\".";
         exit;
      }
   }


   hddebug "uploadname = $uploadname";
   $contents = $in{'uploadfile'};
   $contents =~ s/</&lt;/g;
   $contents =~ s/>/&gt;/g;

   $len = length $contents;
   hddebug "len = $len, uploadname = $uploadname";
   
   if ((length $contents) eq "0") {
      status ("$login: You have not entered any file or directory on HotDiary carry-on. Please enter a filename or directory you would like to upload.");
      exit;
   }

   #$contents =~ s/\r//g;
   #print &PrintVariables(*input);

   $outr = qx{file $uploadname};
   open thandle, ">/home/httpd/html/hd/rep/s-index/smitha/$uploadname";
   printf thandle "%s", $contents;
   close thandle;

   hddebug "done with file upload";
   system "cat $ENV{HDTMPL}/content.html";
 

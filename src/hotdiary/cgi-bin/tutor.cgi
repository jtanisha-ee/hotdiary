#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: search.cgi
# Purpose: it searches info. in hotdiary.
# Creation Date: 01-28-2001
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   hddebug "search action = $input{Submit}";
   if ($input{'Send'} eq "Send") {
      $action = "Send";
   }

   if ($action eq "Send") {
      $name = $input{'name'};
      $location = $input{'location'};
      $email = $input{'email'};
      $phone = $input{'phone'};
      $message = $input{'message'};

      if ( ($email eq "") && ($phone eq "")) {
         status "Please enter atleast one of email address and/or phone.";
         exit;
      }

      $mfile = "$ENV{HDHOME}/tmp/tutor_inquiry$$";
      open mhandle, ">$mfile";
      printf mhandle "Name: $name\n\n";
      printf mhandle "Location: $location\n\n";
      printf mhandle "Email: $email\n\n";
      printf mhandle "Phone: $phone\n\n";
      printf mhandle "Inquiry Details: $message\n\n";
      &flush(mhandle);
      system "/bin/mail -s \"Tuition Inquiry ($name)\" VidyaJoshi\@aol.com rhsup\@hotdiary.com < $ENV{HDHOME}/tmp/tutor_inquiry$$";
      status "Thank you for contacting us! Your inquiry has been received. We will get back to you as soon as possible.";
      $len = length $message;
      if ($len > 20) {
         $len = 20;
      }
      $msg = substr $message, 0, $len;
   }

   exit;
}

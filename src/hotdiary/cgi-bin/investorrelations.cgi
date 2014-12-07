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
# Creation Date: 10-09-97
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

   #status("This service is coming soon!");

   hddebug "investorrelations action = $input{Submit}";
   if ($input{'Send'} eq "Send") {
      $action = "Send";
   }

   if ($action eq "Send") {
      $name = $input{'name'};
      $org = $input{'org'};
      $email = $input{'email'};
      $phone = $input{'phone'};
      $domain1 = $input{'domain1'};
      $cal100 = $input{'cal100'};
      $message = $input{'message'};
      $investsize = $input{'investsize'};
      $areainvest = $input{'investarea'};
      $url = $input{'url'};

      if ($email eq "") {
         status "Please enter a valid email address.";
         exit;
      }

      $mfile = "$ENV{HDHOME}/tmp/investin_hotdiary$$";
      open mhandle, ">$mfile";
      printf mhandle "Name: $name\n\n";
      printf mhandle "Domain: $ENV{'REMOTE_ADDR'}\n\n";
      printf mhandle "Organization: $org\n\n";
      printf mhandle "Email: $email\n\n";
      printf mhandle "Phone: $phone\n\n";
      printf mhandle "Investement Size: $investsize\n\n";
      printf mhandle "Areas of Investment: $areainvest\n\n";
      printf mhandle "URL of Organization: $url\n\n";
      printf mhandle "Message: $message\n\n";
      &flush(mhandle);
      system "/bin/mail -s \"Investment Email ($name)\" rhsup\@hotdiary.com < $ENV{HDHOME}/tmp/investin_hotdiary$$";
      status "Thank you for contacting HotDiary! Your message has been sent. We will get back to you as soon as possible. Please <a href=http://hotdiary.com>click here</a> to return to HotDiary.";
      $len = length $message;
      if ($len > 20) {
         $len = 20;
      }
      $msg = substr $message, 0, $len;
      #system "java COM.hotdiary.main.SendPage \"1615359\" \"Investor Phone $phone Email $email Org $org Message $msg\" \"$name\"";
   }
 

   exit;
}

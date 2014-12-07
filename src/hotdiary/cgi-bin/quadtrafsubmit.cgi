#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: quadtrafsubmit.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 05-23-2000
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   hddebug "quadtrafsubmit.cgi";
# print HTML headers

# bind traffic table vars
   tie %traftab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/traftab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['quadno', 'url', 'hits', 'desc', 'contact',
        'phone', 'email'] };
#
   $quadno = getkeys();

   $url = $input{url};
   $hits = $input{hits};
   $desc = $input{desc};
   $contact = $input{contact};
   $phone = $input{phone};
   $email = $input{email};

   if ( ($url eq "") || ($contact eq "") || ($phone eq "") ||
        ($email eq "") ) {
      status "Some of your contact information is missing. Please use the browser back button and complete the information. If you do not enter the right information, we will not be able to contact you!";
      exit;
   }

   $traftab{$quadno}{quadno} = $quadno;
   $traftab{$quadno}{url} = $url;
   $traftab{$quadno}{hits} = $hits;
   $traftab{$quadno}{desc} = $desc;
   $traftab{$quadno}{contact} = $contact;
   $traftab{$quadno}{phone} = $phone;
   $traftab{$quadno}{email} = $email;

   status "Thank you for submitting your site for a traffic booster package! We will contact you soon, to begin our site research and consulting work.";

   tied(%traftab)->sync();

}

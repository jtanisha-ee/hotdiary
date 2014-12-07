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
# FileName: upgrade.cgi 
# Purpose: it allows the user to upgrade or registers the user to
#	    deluxe services suchas voicemessage/fax/pager.
# Creation Date: 06-10-98
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


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration Upgrade Services"); 

   if ($input{'mcard.x'} ne "") { 
       $charge = "master";
   } else { 
   if ($input{'visa.x'} ne "") { 
      $charge = "visa";
   }}

  $login =  $input{'login'};
  $fname = trim $input{'fname'};
  $lname = trim $input{'lname'};
  $doe = trim $input{'doe'};
  $zipcode = trim $input{'zipcode'};
  $cardno = trim $input{'cardno'};


# bind login table vars
   tie %chargetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/chargetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'fname', 'lname', 'zipcode', 'doe', 'charge',
        'cardno'] };


          if (notName(trim $input{'fname'})) {
             error("Please enter alphabets in the first name.");
             exit;
          }

          if (notName(trim $input{'lname'})) {
             error("Please enter alphabets in the last name.");
             exit;
          }


          if (notNumber(trim $input{'zipcode'})) { 
             error("Please enter numericals in the zipcode.");
             exit;
          }

	  if (notNumber(trim $input{'cardno'})) {
             error("Please enter numericals in the card number.");
	     exit;
          } 
 
          $chargetab{$login}{'login'} = $login;
          $chargetab{$login}{'doe'} = trim $input{'doe'};
          $chargetab{$login}{'cardno'} = trim $input{'cardno'};
          $chargetab{$login}{'zipcode'} = trim $input{'zipcode'};
          $chargetab{$login}{'lname'} = trim $input{'lname'};
          $chargetab{$login}{'fname'} = trim $input{'fname'};
          $chargetab{$login}{'charge'} = $charge;
          $chargetab{$login}{'upgrade'} = "yes";

          $msg = "$login: You have been registered to use HotDiary. Please remember your login and password and keep it in safe place. Click <a href=\"index.html \" TARGET=\"_parent\"> here</a> to login.";

          status("$msg");


#synch the database
   tied(%chargetab)->sync();
}

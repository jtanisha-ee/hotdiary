#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: removeme.cgi
# Purpose: Top screen for notes
# Creation Date: 03-04-2000
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("removeme.cgi");

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


   $password = $input{password};
   $login = $input{login};
   $login = trim $login;
   if ($login eq "") {
      status "You have not specified an account name.";
      exit;
   }
   if (!exists $logtab{$login}) {
      status "This account does not exist.";
      exit;
   }
   if ($logtab{$login}{password} =~ /locked/) {
      status "This account does not exist.";
      exit;
   }
   if ($logtab{$login}{password} eq $password) {
      $logtab{$login}{password} = "locked-" . $logtab{$login}{password};
      $logtab{$login}{informme} = "";
      $logtab{$login}{calpublish} = "";
      $logtab{$login}{email} = "";
      $logtab{$login}{checkid} = "";
      status "$login: Your account has been sucessfully deleted.";
      tied(%logtab)->sync();
   } else {
      status "$login: Your account could not be deleted as the password was incorrect. Please <a href=http://www.hotdiary.com/contact_us.html>contact us</a>."
   }


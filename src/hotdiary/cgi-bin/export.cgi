#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: export.cgi
# Purpose: it exports the addressbook to a file format
# Creation Date: 02-19-99
# Created by: Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

   status("This service is only available to premium users! To open a premium account, contact us for more information.");
   exit;

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'update.x'} ne "") {
      $action = "Update";
   } 


# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.\n");
              exit;
	   }
        }
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired.\n");
    exit;
  }

  $sesstab{$biscuit}{'time'} = time();
 
  if (notDesc($input{'memolist'})) {
     error("$login: Memolist is invalid. It has binary characters.");
     exit;
  }

  $len = trim $input{'memolist'};
  if ($len > $MAXLEN) {
     error("$login: Limit the length of memolist to $MAXLEN.");
     exit;
  }


# bind memo table vars
   tie %memotab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/memotab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'memolist'] };

   $MAXLEN = 10240;

   if ($action = "Update")
   { 
      #print "update action called";
      $memotab{'login'} = $login;
      $memotab{$login}{'memolist'} = trim $input{'memolist'}; 
      status("$login: MemoCal updated.");
   }


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   
# save the info in db
   tied(%memotab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

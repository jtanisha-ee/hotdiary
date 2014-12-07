#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


#
# FileName: authevent.cgi
# Purpose: This program uses dataplates like other programs and checks for
#          user login and password. 
#
# Creation Date: 07-13-99
# created by Smitha Gudur


require "cgi-lib.pl";
use tp::tp;
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

# parse the command line
   &ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


  $login = trim $input{'login'};

   if ($login eq "") {
      hdeebug("Please enter a non-empty login string."); 
      print("Please enter a non-empty login string."); 
   }

   $login = "\L$login";

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

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }

# since error dataplates are too small, before they are synced to disc
# webserver tries to print them, and fails. to prevent this, we need
# to ensure that the error dataplates are created before we exit
# from this script
# check if the login does not exist
   if (!exists $logtab{$login}) {
      hddebug ("login = $login, password = $password");
      print("The member login \"$login\" is not a valid login. Please enter a valid member login. <p>If you haven't yet registered with $p2, please do so before you login.");  
      exit;
   } else {
        if ($logtab{$login}{'password'} ne "") {
           $pass = trim $input{'password'};
           $pass = "\L$pass";
           hddebug "logtab password = $logtab{$login}{'password'}";
           hddebug "Entered password = $pass";
           if (!($logtab{$login}{'password'} eq $pass)) {
              print("$login: Could not login. Enter correct password.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login. If you have forgotten your password, click <a href=\"forgotpasswd.html\">here.</a>");
	      exit;
           }
        }
   }

   #$remoteaddr = $ENV{'REMOTE_ADDR'};
   $remote_addr = 216;
   $sessionid = getkeys();

# bake a biscuit
   $biscuit = "$sessionid-$login-$remoteaddr";
   $title = time();

# check if user has already logged in

   if (!exists $logsess{$login}) {
      $sesstab{$biscuit}{'login'} = $login;
      $sesstab{$biscuit}{'biscuit'} = $biscuit;
      $sesstab{$biscuit}{'time'} = time();
      $logsess{$login}{'login'} = $login;
      $logsess{$login}{'biscuit'} = $biscuit;
   }
   else {

      if (!exists $sesstab{$logsess{$login}{'biscuit'}}) {
         delete $logsess{$login};
         hddebug("$login: Either your session has expired or there is inconsistency in your session information. Please try to login again. If this problem persists, send us an email.");
         print("$login: Either your session has expired or there is inconsistency in your session information. Please try to login again. If this problem persists, send us an email.");
         exit;
      }


# if session has not expired then, check if remote addr of current user
# is same as remote addr in sesstab table for this user
      if ((time() - $sesstab{$logsess{$login}{'biscuit'}}{'time'})
                < $SESSION_TIMEOUT) {
         ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         delete $sesstab{$logsess{$login}{'biscuit'}};
         delete $logsess{$login};
         $sesstab{$biscuit}{'biscuit'} = $biscuit;
         $sesstab{$biscuit}{'login'} = $login;
         $sesstab{$biscuit}{'time'} = time();
         $logsess{$login}{'login'} = $login;
         $logsess{$login}{'biscuit'} = $biscuit;

# if session has expired then do not check for intrusion problem, since
# the user may have logged into one location, then travelled to another
# location and logged in from there with same login, but not within
# 3600 seconds.
      } else {
         ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         delete $sesstab{$logsess{$login}{'biscuit'}};
         delete $logsess{$login};
         $sesstab{$biscuit}{'biscuit'} = $biscuit;
         $sesstab{$biscuit}{'login'} = $login;
         $sesstab{$biscuit}{'time'} = time();
         $logsess{$login}{'login'} = $login;
         $logsess{$login}{'biscuit'} = $biscuit;
      }
  }

# if we reached here, the login was successful, display the choice screen

   if ($login ne "") {
      $alph = substr $login, 0, 1;
      $alph = $alph . '-index';
      system "/bin/rm -f /home/httpd/html/hd/rep/$alph/$login/*.html";
      system "/bin/rm -f /usr/local/hotdiary/rep/$alph/$login/*.html";
      system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alph/$login/index.html";
      system "chown nobody:nobody $ENV{HDREP}/$alph/$login/index.html";
      system "chmod 755 $ENV{HDREP}/$alph/$login/index.html";
   } else {
      hddebug "login is null, we got a problem";
   }
   print $biscuit;

# save the info in db
   #tied(%logtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   if ($biscuit ne "") {
      system "chown nobody:nobody $ENV{HDDATA}/sesstab/$biscuit.rec";
      system "chmod 755 $ENV{HDDATA}/sesstab/$biscuit.rec";
   } else {
      hddebug "biscuit is null, we got a problem";
   }
}

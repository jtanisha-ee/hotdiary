#!/usr/bin/perl
#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: apptaddsearch.cgi
# Purpose: it adds and searches the appointments.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

#max length in the description
   $MAXDESC = 4096;

#parse the command line
   &ReadParse(*input);

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = trim $input{'biscuit'};

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      hddebug("Session does not exist. Please select connect menu to relogin"); 
      print("Session does not exist. Please select connect menu to relogin");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
	      #hddebug("Login is an empty string.");
	      exit;
           }
       }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
     if (exists $sesstab{$biscuit}) {
        delete $sesstab{$biscuit};
     }
     if (exists $logsess{$login}) {
        delete $logsess{$login};
     }
     hddebug("$login: Your session has timed out. Please select connect menu to relogin.");  
     print("$login: Your session has timed out. Please select connect menu to relogin.");  
     exit;
  }

  $sesstab{$biscuit}{'time'} = time();

  $alph = substr $alph, 0, 1;
  $alph = $alph . '-index';

# bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alph/$login/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'phone', 'city', 'url', 'imgfn', 'venue'] };


   # get entry number
   $entryno = getkeys();


   $mo = trim $input{'month'};
   $da = trim $input{'day'};
   $yr = trim $input{'year'};

   $ezone = trim $input{'zone'};
   $ehour = trim $input{'hour'};
   $meridian = trim $input{'meridian'};
   $emin = trim $input{'min'};
   hddebug "emin = $emin";

       $appttab{$entryno}{'entryno'} = $entryno;
       $appttab{$entryno}{'login'} = $login;
       $appttab{$entryno}{'desc'} = $input{'desc'};
       $appttab{$entryno}{'zone'} = trim $input{'zone'};
       $appttab{$entryno}{'month'} = $mo;
       $appttab{$entryno}{'day'} = $da;
       $appttab{$entryno}{'year'} = $yr;
       $appttab{$entryno}{'hour'} = trim $input{'hour'};

       if (trim $input{'min'} eq "0") {
         $appttab{$entryno}{'min'} = '00';
       } else {
         $appttab{$entryno}{'min'} = trim $input{'min'};
       }

       $appttab{$entryno}{'meridian'} = trim $input{'meridian'};
       $appttab{$entryno}{'desc'} = trim $input{'desc'};
       $appttab{$entryno}{'subject'} = trim $input{'subject'};

       $appttab{$entryno}{'phone'} = trim $input{'phone'};
       $appttab{$entryno}{'city'} = trim $input{'city'};
       $appttab{$entryno}{'url'} = trim $input{'url'};
       $appttab{$entryno}{'imgfn'} = trim $input{'imgfn'};
       $appttab{$entryno}{'venue'} = trim $input{'venue'};

       # add the entry in the apptentrytab/$login.
       $tfile = "$ENV{HDDATA}/$alph/$login/apptentrytab";
       open thandle, ">>$tfile";
       printf thandle "%s\n", $entryno;
       close thandle;


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();


# save the info in db
   tied(%appttab)->sync();
   tied(%sesstab)->sync();
}

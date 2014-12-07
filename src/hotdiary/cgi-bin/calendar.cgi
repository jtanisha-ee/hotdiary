#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: calendar.cgi
# Purpose: it displays the current month's calendar
# Creation Date: 03-04-99
# Created by: Smitha Gudur
# 

#!/usr/local/bin/perl5

require "cgi-lib.pl";
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

# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Calendar"); 

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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

   $biscuit = trim $input{'biscuit'};

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
      		error("Login  is an empty string.\n");
                exit;
           }
	}
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
   #    error("Intrusion detected. Access denied.\n");
   #    exit;
   #}


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
           delete $sesstab{$biscuit};
	   status("$login: Your session has already expired.\n");
           exit;
  }

  $sesstab{$biscuit}{'time'} = time(); 


# bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$login/appttab",
   SUFIX => '.rec', 
   SCHEMA => { 
   	ORDER => ['entryno', 'login', 'month', 'day', 'year', 
	'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject'] };


   # get entry number
   $entryno = getkeys();

# get the current month
  $cmon = (localtime)[4];
  $cmonstr = (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)[$cmon];

# cday is current day of the month
  $cday = (localtime)[3];

# cyear is current year
  $cyear = (localtime)[5];

# wday is the week day of today
  $wday = (localtime)[6];

# fday is the week day of the first of the month
  $fday = ($wday - (($cday % 7) - 1));
  if ($fday < 0) {
     $fday = 7 + $wday1;
  }

  print "<TABLE>\n";
  print "<TR>\n";
  print "<TD>M</TD>\n";
  print "<TD>T</TD>\n";
  print "<TD>W</TD>\n";
  print "<TD>T</TD>\n";
  print "<TD>F</TD>\n";
  print "<TD>S</TD>\n";
  print "<TD>S</TD>\n";
  print "</TR>\n";
  if (($cyear % 4) == 0) {
     $febdays = 29;
  } else {
     $febdays = 28;
  }
  $numdays = (31, $febdays, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[$cmon];
  
  

# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   tied(%appttab)->sync();
   tied(%sesstab)->sync();
}

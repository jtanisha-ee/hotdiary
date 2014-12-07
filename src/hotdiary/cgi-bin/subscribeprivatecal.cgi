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
# FileName: accesssprivatecal.cgi
# Purpose: Creates a private group calendar
# Creation Date: 07-16-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
# This line of ParseTem had to be defined first. For some reason
# status was not working when this line was not first.Very strange!
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("subscribeprivatecal.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $hs = $input{'hs'};
   $jp = $input{'jp'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   $biscuit = $input{'biscuit'};
   if ($biscuit eq "") {
      if ($hs eq "") {
        status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      } else {
        status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
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

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.");
            exit;
         }
      }
   }
   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
        status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
        status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }


# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed'] };

   $password = trim $input{'password'};
   $g = trim $input{'g'};
   $rh = trim $input{'rh'};

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';


   if ($lgrouptab{$g}{'password'} eq $password) {
       # bind subscribed group table vars
       if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
          system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
          system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
       }
       tie %sgrouptab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
       if (!(exists $sgrouptab{$g})) {
          $sgrouptab{$g}{'groupname'} = $g;
          $sgrouptab{$g}{'groupfounder'} = $lgrouptab{$g}{'groupfounder'}; 
          $sgrouptab{$g}{'grouptype'} = $lgrouptab{$g}{'grouptype'};
          $sgrouptab{$g}{'grouptitle'} = $lgrouptab{$g}{'grouptitle'};
          $sgrouptab{$g}{'groupdesc'} = $lgrouptab{$g}{'groupdesc'}; 
          $sgrouptab{$g}{'password'} = $lgrouptab{$g}{'password'}; 
          $sgrouptab{$g}{'ctype'} = $lgrouptab{$g}{'ctype'}; 
          $sgrouptab{$g}{'cpublish'} = $lgrouptab{$g}{'cpublish'}; 
          tied(%sgrouptab)->sync();
       } else {
            status("$login: You are already subscribed to this calendar \"$g\"");
            exit;
       }
       depositmoney $login; 
        
       tie %usertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/usertab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['login'] };
       $usertab{$login}{'login'} = $login;
       tied(%usertab)->sync();
       $rh = $input{rh};
       status("$login: You have successfully subscribed to the calendar $g. <p>Click <a href=\"http://$vdomain/cgi-bin/execcalclient.cgi?biscuit=$biscuit&g=$g\">here</a> to edit the group calendar $g. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&g=sgc\">here</a> to return to search group calendars.");
   } else {
        status("Invalid password ($password). Please enter the correct password for this calendar. You may also want to verify the password with the Calendar Master for \"$g\".");
        exit;
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

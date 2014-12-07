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
# FileName: subscribemergedcal.cgi
# Purpose: subscribe a private merged calendar
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
   #print &HtmlTop ("subscribemergedcal.cgi example");
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


# bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 
                  'listed', 'groups', 'logins'] };

   $password = trim $input{'password'};
   $g = trim $input{'g'};
   $rh = trim $input{'rh'};

   if ($lmergetab{$g}{'password'} eq $password) {
       # bind subscribed merged table vars
       tie %smergetab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/merged/$login/subscribed/smergetab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
               'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
       if (!(exists $smergetab{$g})) {
          $smergetab{$g}{'groupname'} = $g;
          $smergetab{$g}{'groupfounder'} = $lmergetab{$g}{'groupfounder'}; 
          $smergetab{$g}{'grouptype'} = $lmergetab{$g}{'grouptype'};
          $smergetab{$g}{'grouptitle'} = $lmergetab{$g}{'grouptitle'};
          $smergetab{$g}{'groupdesc'} = $lmergetab{$g}{'groupdesc'}; 
          $smergetab{$g}{'password'} = $lmergetab{$g}{'password'}; 
          $smergetab{$g}{'ctype'} = $lmergetab{$g}{'ctype'}; 
          $smergetab{$g}{'cpublish'} = $lmergetab{$g}{'cpublish'}; 
          tied(%smergetab)->sync();
       } else {
            status("$login: You are already subscribed to this calendar \"$g\"");
            exit;
       }
       depositmoney $login; 
        
       tie %usertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/listed/merged/$g/usertab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['login'] };
       $usertab{$login}{'login'} = $login;
       tied(%usertab)->sync();
       $rh = $input{rh};

       if ($os ne "nt") {
          $execmergedgroups = encurl "execmergedgroups.cgi";
       } else {
          $execmergedgroups = "execmergedgroups.cgi";
       }

       $mcalmsg = adjusturl "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&f=sgc&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to search merged calendars.";     
       status("$login: You have successfully subscribed to the calendar $g. <p>Click <a href=\"http://$vdomain/cgi-bin/execmgcalclient.cgi?biscuit=$biscuit&g=$g\">here</a> to view the merged calendar $g. <p>$mgcalmsg.");
   } else {
        status("Invalid password ($password). Please enter the correct password for this calendar. You may also want to verify the password with the Calendar Master for \"$g\".");
        exit;
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

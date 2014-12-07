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
# FileName: generic.cgi
# Purpose: New HotDiary Calendar Client
# Creation Date: 08-02-99 
# Created by: Smitha Gudur
# 

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");    

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;
   if ($biscuit eq "") {
      $sc = "p";
   }
   $hs = $input{'hs'};
   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $hs = $input{'hs'};
   #$rhost = qx{nslookup $ENV{'REMOTE_HOST'} | grep Name | awk '{print \$2}'};
   #$rhost =~ s/\n//g;
   $rhost = $ENV{'REMOTE_HOST'};
   hddebug "calclient.cgi: Invoked from $rhost";

   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['HDLIC', 'partner', 'IP'] };

   tie %parttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/parttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['logo', 'title', 'banner'] };


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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

   # check if session record exists. 
   if ($sc ne "p") {
           if (!exists $sesstab{$biscuit}) {
      
             if ($hs eq "") {
                status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
             } else {
                status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
             }
             exit;
           } else {
              if ($login eq "") {
                  $login = $sesstab{$biscuit}{'login'};
                  if ($login eq "") {
                     error("Login is an empty string. Possibly invalid session.\n");
                     exit;
                  }
	      }
          }
   } else {
        $login = $input{'l'};
   }

  if (($biscuit ne "") && ($sc ne "p"))  {
     if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
       delete $sesstab{$biscuit};
       delete $logsess{$login};
       if ($hs eq "") {
          status("$login: Your session has already expired. Click <a href=\"http://$vdomain/index.html\" target=\"_parent\"> here</a> to login again.");
       } else {
          status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/index.html\" target=\"_parent\"> here</a> to login again.");
       }
       exit;
      }
  } 

  if ($vdomain ne "www.hotdiary.com") {
     status("$login: This feature is available at your local calendar service provider. Please check with your provider for details on how to access this feature.");
     exit;
  }

  status("$login: This feature is only available to JazzIt! calendar service providers. If you would like to register for this free feature, please contact us with your name, address, and phone number. A support representative will be happy to call you, if required (in most cases we do not
 need to call you, we just use email to communicate), and configure your account for ShowBiz!");
  exit;
}

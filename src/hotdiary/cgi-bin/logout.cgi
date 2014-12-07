#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

# This program is no longer used. We use now proxylogout.cgi and execproxylogout.cgi
# FileName: logout.cgi
# Purpose: it allows the user to logout and does all the necessary
#	   required session management service for this operation.
# Creation Date: 06-10-98
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use tp::tp;
use utils::utils;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;

$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

MAIN:
{

# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration"); 

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid'] };      
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

   $biscuit = $input{'biscuit'};

   if (!exists $sesstab{$biscuit}) {
      error("Not logged in or intrusion detected.\n");
      exit;
   }

   $login = $sesstab{$biscuit}{'login'};

   # check for intruder access. deny the permission and exit error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: You have been logged out automatically.");
      exit;
   }

   delete $sesstab{$biscuit};
   delete $logsess{$login};

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   # delete all the html files in user directory.   
   system "/bin/rm -f $ENV{HDREP}/$alphaindex/$login/*.html";

   
   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/index.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha1/$login/spc-$biscuit-$$.html";
   $prml = strapp $prml, "login=$login";
   parseIt $prml;

   #hdsystemcat "$ENV{HDREP}/$alpha1/$login/spc-$biscuit-$$.html";

   status("$login: You have been logged out. Click <a href=\"index.html\">here</a> to login again.");

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

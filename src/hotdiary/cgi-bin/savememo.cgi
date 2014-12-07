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
# FileName: savememo.cgi
# Purpose: Top screen for memo
# Creation Date: 03-04-2000
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
use MIME::Base64;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("savememo.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
   $g = $input{g};
   hddebug "g = $g";
   $rh = $input{rh};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();

   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }

   tie %parttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/partners/parttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['logo', 'title', 'banner'] };

 
   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "logo=$logo";
   $sc = $input{sc};

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execsavememo =  encurl "execsavememo.cgi";
      $execmemo =  encurl "execmemo.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execsavememo =   "execsavememo.cgi";
      $execmemo =   "execmemo.cgi";
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ($g eq "") {
      # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/todotab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share',
              'hour', 'banner'] };
   } else {
      # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/todotab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share',
              'hour', 'banner'] };
   }

   $edit = $input{edit};

   if ($edit eq "") {
      $entry = getkeys();
      $todotab{$entry}{entryno} = $entry;
      depositmoney $login;
   } else { 
      $entry = $input{entry};
      if (!exists($todotab{$entry}) ) {
         status("$login: There is no such memo entry. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=3&p0=$execmemo&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to memo manager.");
        exit;
      }
   }

   $todotab{$entry}{subject} = adjusturl $input{subject};
   #$todotab{$entry}{desc} = encode_base64 $input{desc}, "";
   $desc = "<i><FONT COLOR=red>Last Updated: " . $notestamp . "</FONT></i><p>" . $desc;

   $todotab{$entry}{desc} = adjusturl $input{desc};
   $todotab{$entry}{month} = $input{month};
   $todotab{$entry}{day} = $input{day};
   $todotab{$entry}{year} = $input{year};
   $todotab{$entry}{priority} = $input{priority};
   $todotab{$entry}{status} = $input{status};

   hddebug "completed savememo";

   status("$login: Your memo has been added to memo manager. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execmemo&p1=biscuit&p2=jp&p3=g&g=$g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to memo manager.");


   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%todotab)->sync();


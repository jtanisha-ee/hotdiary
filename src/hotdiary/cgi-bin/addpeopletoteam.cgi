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
# FileName: addpeopletoteam.cgi
# Purpose: Password Setting in Virtual Intranet AccessControl
# Creation Date: 09-11-99
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

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   hddebug "addpeopletoteam.cgi()";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
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
              status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
      if (!exists $logtab{$login}) {
         error("Invalid login found in session.");
         exit;
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

   $rh = $input{rh};
   $hs = $input{'hs'};
   $HDLIC = $input{HDLIC};  

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };            
   $business = trim $input{business};
   if ((!exists $businesstab{$business}) || ($business eq "")) {
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }
       
   $selbegin = $input{selbegin};
   $selend = $input{selend};
   $teamname = $input{teamname};

   if (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
   }

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']}; 

   $k = 0;
   if ($input{add} ne "") {
      $action = "add";
   } else {
      $action = "addall";
   }

   # parameter for checkboxes number p(x) = box(y)
   # values for checkboxes box(y) = $val
   # get the value if the checkbox is on or off p(x) =$val
   # as we donot know the value (name), we assign 
   # names to each value and then get its value.

   if ($action eq "add") { 
      for ($i = $selbegin; $i <= $selend; $i= $i + 1) {
         $memberlogin = $input{"box$k"};
         $checkboxval = $input{$memberlogin};
         #hddebug "checkboxval = $checkboxval";

         if ($checkboxval eq "on") {
            #hddebug "action = $action";
            $teampeopletab{$memberlogin}{login} = $memberlogin;
         }
         $k = $k + 1;
      }
   }

   #hddebug "selbegin = $selbegin"; 
   #hddebug "selend = $selend"; 
   if ($action eq "addall") {
     for ($i = $selbegin; $i <= $selend; $i= $i + 1) {
         $memberlogin = $input{"box$k"};
         $teampeopletab{$memberlogin}{login} = $memberlogin;
         $k = $k + 1;
     }
   }

   #if ($os ne "nt") {
   #   $execproxylogout = encurl "/proxy/execproxylogout.cgi";
   #   $execdeploypage =  encurl "execdeploypage.cgi";
   #   $execshowtopcal =  encurl "execshowtopcal.cgi";
   #   $execcreatebusinesscalendar = encurl "execcreatebusinesscalendar.cgi";
   #   $execsearchbusinesscalendars= encurl "execsearchbusinesscalendars.cgi";
   #   $execshowpeopletoteam= encurl "execshowpeopletoteam.cgi";
   #} else {
   #   $execproxylogout =  "/proxy/execproxylogout.cgi";
   #   $execdeploypage =  "execdeploypage.cgi";
   #   $execshowtopcal =  "execshowtopcal.cgi";
   #   $execcreatebusinesscalendar = "execcreatebusinesscalendar.cgi";
   #   $execsearchbusinesscalendars= "execsearchbusinesscalendars.cgi";
   #   $execshowpeopletoteam= "execshowpeopletoteam.cgi";
   #}

   #$prml = "";
   #$prml = strapp $prml, "execproxylogout = $execproxylogout";
   #$prml = strapp $prml, "execdeploypage = $execdeploypage";
   #$prml = strapp $prml, "execshowtopcal = $execshowtopcal";
   #$prml = strapp $prml, "execcreatebusinesscalendar = $execcreatebusinesscalendar";
   #$prml = strapp $prml, "execsearchbusinesscalendars = $execsearchbusinesscalendars";
   #$prml = strapp $prml, "execshowpeopletoteam = $execshowpeopletoteam";
   #parseIt $prml;

   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%teampeopletab)->sync();

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alph/$login/showbusinesscal.html";
   hdsystemcat "$ENV{HDHREP}/$alph/$login/showbusinesscal.html";


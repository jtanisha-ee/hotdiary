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
# FileName: addbusiness.cgi
# Purpose: Create A Virtual Intranet
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

   hddebug("addbusiness.cgi");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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

   $sesstab{$biscuit}{'time'} = time();
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

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list', 'view', 'publish'] };


   $business = trim $input{business};
   $HDLIC = $input{HDLIC};  

   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execmanageonebusiness = encurl "execmanageonebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execmanageonebusiness = "execmanageonebusiness.cgi";
   }

   if ((!exists $businesstab{$business}) || ($business eq "")) {      
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&p2=jp&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }             

   if ($login ne $businesstab{$business}{businessmaster}) {
      tie %managertab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']};              

      tie %mgraccesstab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother', 
		'invite', 'approve', 'delete', 'edit', 'manage', 
		'contact', 'teams']};         

      if (exists ($managertab{$login})) {
         if ($mgraccesstab{access}{edit} ne "CHECKED") {
	    status("$login: You are the business manager for ($business) but you do not have the permission to edit settings. Manager Role settings have to be enabled to edit ($business). Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmanageonebusiness&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business."); 
	    exit;
         } 
      } else {
	  status("$login: You do not have the permission to edit settings for ($business).  Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmanageonebusiness&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business."); 
	 exit;
      }
   }

   if (notAddress($input{businessstreet})) {
      status("Invalid characters in Street Address ($input{'businessstreet'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notName($input{businesstitle})) {
      status("Invalid characters in Title ($input{'businesstitle'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notAddress($input{businesssuite})) {
      status("Invalid characters in Suite Number ($input{'businesssuite'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notName($input{businesscity})) {
      status("Invalid characters in City ($input{'businesscity'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notName($input{businessstate})) {
      status("Invalid characters in State ($input{'businessstate'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notNumber($input{businesszipcode})) {
      status("Invalid characters in Zipcode ($input{'businesszipcode'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notName($input{businesscountry})) {
      status("Invalid characters in Country ($input{'businesscountry'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   if (notPhone($input{businessphone})) {
      status("Invalid characters in Phone ($input{'businessphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notPhone($input{businessfax})) {
      status("Invalid characters in Fax ($input{'businessfax'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notDesc($input{'businessother'})) {
       status("Invalid characters in Other ($input{'businessother'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notUrl($input{'businessurl'})) {
      status("Invalid characters in URL ($input{'businessurl'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   if (notEmail($input{'businessemail'})) {
      status("Invalid characters in Email ($input{'businessemail'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   $publish = $input{publish};
   if ($publish eq "on") {
     $publish eq "CHECKED";
   }

   hddebug "businessstate = $input{businessstate}";
   $businesstab{$business}{businesstitle} = trim $input{businesstitle};
   $businesstab{$business}{street} = trim $input{businessstreet};
   $businesstab{$business}{suite} = trim $input{businesssuite};
   $businesstab{$business}{city} = trim $input{businesscity};
   $businesstab{$business}{state} = trim $input{businessstate};
   $businesstab{$business}{zipcode} = trim $input{businesszipcode};
   $businesstab{$business}{country} = trim $input{businesscountry};
   $businesstab{$business}{phone} = trim $input{businessphone};
   $businesstab{$business}{fax} = trim $input{businessfax};
   $businesstab{$business}{url} = trim $input{businessurl};
   $businesstab{$business}{email} = trim $input{businessemail};
   $businesstab{$business}{other} = trim $input{businessother};
   $businesstab{$business}{view} = trim $input{radio1};
   $radio = $input{radio1};
   hddebug "radio1 = $radio";
   $businesstab{$business}{publish} = $publish;

   hddebug "businesslist = $input{businesslist}";
   if ($input{businesslist} eq "on") {
      $businesstab{$business}{list} = "CHECKED";
   } else {
      $businesstab{$business}{list} = trim $input{businesslist};
   }

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%businesstab)->sync();

   if ($os ne "nt") {
      $execshowbusinesscalmenu = encurl "execshowbusinesscalmenu.cgi";
   } else {
      $execshowbusinesscalmenu = "execshowbusinesscalmenu.cgi";
   }
   status("$login: You have updated ($business). <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmanageonebusiness&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowbusinesscalmenu&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=4\">here</a> to return to Manage Teams.");

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
# FileName: deletemember.cgi
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

   hddebug("deletemember.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
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

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {

      $HDLIC = $input{'HDLIC'};
      # bind login table vars
      tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };
   
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

   $rh = trim $input{rh};
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

   $business = trim $input{business};      
   if ((!exists $businesstab{$business}) || ($business eq "")) {
      if ($os ne "nt") {
         $execbusiness = encurl "execbusiness.cgi";
         $execcreatebusiness = encurl "execcreatebusiness.cgi";
      } else {
         $execbusiness = "execbusiness.cgi";
         $execcreatebusiness = "execcreatebusiness.cgi";
      }
 
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=5\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }
                       
   $selbegin = $input{selbegin};
   $selend = $input{selend};
   $k = 0;

   # parameter for checkboxes number p(x) = box(y)
   # values for checkboxes box(y) = $val
   # get the value if the checkbox is on or off p(x) =$val
   # as we donot know the value (name), we assign first names to each value
   # and then get its value.

  # bind manager table vars
  tie %managertab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['login']};

  if ($os ne "nt") {
     $execmanagepeopleinbusiness = encurl "execmanagepeopleinbusiness.cgi";
  } else {
     $execmanagepeopleinbusiness = "execmanagepeopleinbusiness.cgi";
  }

  if ($businesstab{$business}{businessmaster} ne $login) { 
     if ($os ne "nt") {
        $execmanageonebusiness = encurl "execmanageonebusiness.cgi";
     } else {
        $execmanageonebusiness = "execmanageonebusiness.cgi";
     }
     if (!exists($managertab{$login})) {
        status("$login: You do not have the permission to delete for ($business).  <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmanagepeopleinbusiness&p1=biscuit&p2=f&p3=business&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=cpc&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage people.");
        exit;
     }

     tie %mgraccesstab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother', 'invite',
             'approve', 'delete', 'edit', 'manage', 'contact', 'teams']};


     if ($mgraccesstab{$business}{delete} ne "CHECKED") {
        status("$login: You are the business manager for ($business) but you do not have the permission to delete or remove people from ($business). Manager Role settings have to be enabled to delete ($business). <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmanagepeopleinbusiness&p1=biscuit&p2=f&p3=business&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=cpc&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage people.");
        exit;
     }
  }

  $chkcntr = 0;
  $ismaster = 0;

  # create an entry in the peopletab
  tie %peopletab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['login', 'business']};


  for ($i = $selbegin; $i <= $selend; $i= $i + 1) {
      $memberlogin = $input{"box$k"};
      $checkboxval = $input{$memberlogin};
      #hddebug ("memberlogin = $memberlogin");
      #hddebug "checkboxval = $checkboxval";
      #hddebug "enetred business = $business, login=$memberlogin";
      $k = $k  + 1;

      if ($checkboxval eq "on") {
         $chkcntr = $chkcntr + 1;
         #hddebug "action = $action";

         if ($memberlogin eq "") {
            next;
         }

	 $memberlogin = trim $memberlogin;
         if ($businessmaster eq $memberlogin) {
            $ismaster = 1;
         } 

         if (-d "$ENV{HDDATA}/business/business/people/$memberlogin/mybiztab") {
            tie %mybiztab, 'AsciiDB::TagFile',
                DIRECTORY => "$ENV{HDDATA}/business/business/people/$memberlogin/mybiztab",
                SUFIX => '.rec',
                SCHEMA => {
                ORDER => ['business']};
         }
         if ($ismaster != 1) {
            if (exists ($managertab{$memberlogin})) {
                delete $managertab{$memberlogin};
            }
            if (-d "$ENV{HDDATA}/business/business/people/$memberlogin/mybiztab") {
               if (exists ($mybiztab{$business})) {
                  #hddebug "deleting business = $business, login=$memberlogin";
                  delete $mybiztab{$business};
                  tied(%mybiztab)->sync();
	       }
            }
            if (exists ($peopletab{$memberlogin})) {
                delete $peopletab{$memberlogin};
	    }
         }
      }
   }
  

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%managertab)->sync();
   tied(%peopletab)->sync();

   if ($ismaster == 1) {
      $intrmsg = "You cannot remove ($businessmaster) as ($businessmaster) created the ($business)."; 
   }
   status("$login: You have successfully removed members from ($business). $intrmsg <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmanagepeopleinbusiness&p1=biscuit&p2=f&p3=business&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=cpc&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage people.");


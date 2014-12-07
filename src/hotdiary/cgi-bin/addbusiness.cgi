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
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   hddebug("addbusiness.cgi");

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
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
	'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };
                                                                              
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

   $sesstab{$biscuit}{'time'} = time();
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

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle', 'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone', 'fax', 'url', 'email', 'other', 'list',
            'view', 'publish'] };

   if (!(-d "$ENV{HDDATA}/business/business/people/$login/founded")) {
      system "mkdir -p $ENV{HDDATA}/business/business/people/$login/founded";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/people/$login/founded";
      system "chmod 755 $ENV{HDDATA}/business/business/people/$login/founded";
   }

   tie %founded, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/business/people/$login/founded",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business'] };


   $rh = $input{rh};
   $password = trim $input{password};
   $rpassword = trim $input{rpassword};
   if ("\L$password" ne "\L$rpassword") {
      status("The two passwords you entered do not match. Please re-enter the password.");
      exit;
   }
   $HDLIC = $input{HDLIC};  
   $business = trim $input{business};
   if (notLogin $business) {
      status("Business name is invalid. Please use alphanumeric characters in your business name.");
      exit;
   }
   $business = "\L$business";
   if ($os eq "nt") {
     $prog =  "execcreatebusiness.cgi";
     $prog1 =  "execbusiness.cgi";
     $prog2 =  "execmanagebusiness.cgi";
   } else { 
     $prog = encurl("execcreatebusiness.cgi");
     $prog1 =  encurl "execbusiness.cgi";
     $prog2 =  encurl "execmanagebusiness.cgi";
   }

   if ($business eq "") {
      status("$login: No business name has been specified. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$prog&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create a business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=prog1&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=4&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to Business home.");
      exit;
   }

   if (exists $businesstab{$business}) {
      status("$login: The business \"$business\" already exists. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$prog&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create another business.");
      exit;
   }

   if ($business =~ / /) {
      status("$login: Business name has spaces in it. Enter business name with out any spaces. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$prog&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business.");
      exit;
   }

   $businesstab{$business}{business} = $business;
   $businesstab{$business}{password} = $password;
   $businesstab{$business}{businesstitle} = $input{businesstitle};
   $businesstab{$business}{businessmaster} = $login;
   $businesstab{$business}{list} = "CHECKED";

   ## only calendar view
   $businesstab{$business}{view} = "cview";

   $founded{$business}{business} = $business;

   if (!(-d "$ENV{HDDATA}/business/business/$business/mgraccesstab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/mgraccesstab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/mgraccesstab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/mgraccesstab";
   }

   if (!(-d "$ENV{HDDATA}/business/business/$business/otheraccesstab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/otheraccesstab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/otheraccesstab";
   }

   tie %otheraccesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/otheraccesstab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['access']};

   $otheraccesstab{access}{'access'} = "";


   tie %mgraccesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother', 
	      'invite', 'approve', 'delete', 'edit', 'manage', 'contact',
	      'teams']};

   $mgraccesstab{access}{'pother'} = "CHECKED";
   $mgraccesstab{access}{'invite'} = "CHECKED";
   $mgraccesstab{access}{'approve'} = "CHECKED";
   $mgraccesstab{access}{'delete'} = "CHECKED";
   $mgraccesstab{access}{'edit'} = "CHECKED";
   $mgraccesstab{access}{'manage'} = "CHECKED";
   $mgraccesstab{access}{'contact'} = "CHECKED";
   $mgraccesstab{access}{'teams'} = "CHECKED";
 
   if (!(-d "$ENV{HDDATA}/business/business/$business/peopletab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/peopletab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/peopletab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/peopletab";
   }

   tie %peopletab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['login', 'business']};
 
   $peopletab{$login}{business} = $business;

   if (!(-d "$ENV{HDDATA}/business/business/$business/managertab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/managertab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/managertab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/managertab";
   }

   #status("$login: Congratulations! The virtual Business $business has been created successfully. Please note the password ($password) carefully. This may be required for future use.<BR>Now that you have created a Business, it is recommended that you specify more detailed information about your Business. This way, your employees can find, join and use your Business smoothly. This is what we call as managing your Business.<BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$prog2&p1=biscuit&p2=business&p3=jp&business=$business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage Business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$prog1&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to Business home.");
   status("$login: Congratulations! The virtual Business $business has been created successfully. Please note the password ($password) carefully. This may be required for future use.<BR>Now that you have created a Business, it is recommended that you specify more detailed information about your Business. This way, your employees can find, join and use your Business smoothly. This is what we call as managing your Business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$prog1&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to Business home.");


   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%businesstab)->sync();
   tied(%founded)->sync();
   tied(%mgraccesstab)->sync();
   tied(%peopletab)->sync();
   tied(%otheraccesstab)->sync();

#!/usr/local/bin/perl5
#
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
# FileName: savebusinessdir.cgi 
# Purpose: save the details about login
# Creation Date: 12-01-98
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("showpeopleinbusiness.cgi ");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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

   $rh = $input{rh};
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $rh = $input{rh};

   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execshowviewbusiness = encurl "execshowviewbusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execshowviewbusiness = "execshowviewbusiness.cgi";
   }

   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

  
   $ulogin = $input{ulogin};
   if (($ulogin eq "") || (!exists($logtab{$ulogin})) ){
       status("$login: ($ulogin) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowviewbusiness&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to View Business Directory.");  
       exit;
   }

   if  (!(-d "$ENV{HDDATA}/business/business/$business/directory")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/directory";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/directory";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory";
   }

   if (!(-d "$ENV{HDDATA}/business/business/$business/directory/emptab"))  {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/emptab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/emptab";
       system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory/emptab";
   }


# bind emptab table vars
   tie %emptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/emptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

   $editcontact = 0;
   if (($login eq $businesstab{$business}{businessmaster}) || ($login eq $ulogin)) {
     $editcontact = 1;
   } else {
     if ($login ne $ulogin) {
       if (-d("$ENV{HDDATA}/business/business/$business/mgraccesstab")) { 
          tie %mgraccesstab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother',
                'invite', 'approve', 'delete', 'edit', 'manage',
                'contact', 'teams']}; 
          if ($mgraccesstab{access}{contact} eq "CHECKED") {
	    if (-d("$ENV{HDDATA}/business/business/$business/managertab")) {
	       tie %managertab, 'AsciiDB::TagFile',
       	       DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
               SUFIX => '.rec',
               SCHEMA => {
               ORDER => ['login']};
               if (exists ($managertab{$login})) {     
	          $editcontact = 1;
	        }
            }
         }
      }
    }
  }
   if ($os ne "nt") {
      $execmembersdir = encurl "execmembersdir.cgi";
      $execshowcontactlist = encurl "execshowcontactlist.cgi"
   } else {
      $execmembersdir = "execmembersdir.cgi";
      $execshowcontactlist = "execshowcontactlist.cgi"
   }

   if ($editcontact == 0) {
      status("$login: You donot have permission to edit this contact. <BR>If you are a regular member, you can edit your own contact information. <BR>Business Master can edit any contact. <BR>Business Managers can edit any contact if access control is set in manage business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmembersdir&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to Members Directory.");
      exit;
   }

   $street =  $input{street}; 
   hddebug "street = $street";
   if (notAddress($input{street})) {
       status("Invalid characters in Street Address ($input{'street'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{fname})) {
       status("Invalid characters in First Name ($input{'fname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{lname})) {
       status("Invalid characters in Last Name ($input{'lname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notAddress($input{aptno})) {
       status("Invalid characters in Last Name ($input{'aptno'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{city})) {
       status("Invalid characters in City ($input{'city'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{state})) {
       status("Invalid characters in State ($input{'state'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{country})) {
       status("Invalid characters in Country ($input{'country'}).  Click <a href=\"validation.html\">here</a> for valid input.\n");
       exit;
   }

   if (notNumber($input{zipcode})) {
       status("Invalid characters in Zipcode ($input{'zipcode'}).  Click <a href=\"validation.html\">here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{hphone})) {
       status("Invalid characters in Home Phone ($input{'hphone'}).  Click <a href=\"validation.html\">here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{bphone})) {
       status("Invalid characters in Business Phone ($input{'bphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{cphone})) {
       status("Invalid characters in Cell Phone ($input{'cphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{fax})) {
       status("Invalid characters in Fax ($input{'fax'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{pager})) {
       status("Invalid characters in Pager ($input{'pager'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notEmail($input{email})) {
       status("Invalid characters in Email ($input{'email'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notUrl($input{url})) {
       status("Invalid characters in URL ($input{'url'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notDesc($input{other})) {
       status("Invalid characters in Other ($input{'other'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notName($input{busname})) {
       status("Invalid characters in Business Name ($input{'busname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notName($input{title})) {
       status("Invalid characters in Title ($input{'title'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   $emptab{$ulogin}{login} = "\L$ulogin";
   $emptab{$ulogin}{fname} = trim $input{fname};
   $emptab{$ulogin}{lname} = trim $input{lname};
   $emptab{$ulogin}{aptno} = trim $input{aptno};
   $emptab{$ulogin}{street} = trim $input{street};
   $emptab{$ulogin}{city} = trim $input{city};
   $emptab{$ulogin}{state} = trim $input{state};
   $emptab{$ulogin}{zipcode} = trim $input{zipcode};
   $emptab{$ulogin}{country} = trim $input{country};
   $emptab{$ulogin}{url} = trim $input{url};
   $emptab{$ulogin}{email} = trim $input{email};
   $emptab{$ulogin}{fax} = trim $input{fax};
   $emptab{$ulogin}{cphone} = trim $input{cphone};
   $emptab{$ulogin}{bphone} = trim $input{bphone};
   $emptab{$ulogin}{phone} = trim $input{hphone};
   $emptab{$ulogin}{pager} = trim $input{pager};
   $emptab{$ulogin}{pagertype} = trim $input{pagertype};
   $emptab{$ulogin}{other} = trim $input{other};
   $emptab{$ulogin}{title} = trim $input{title};
   $emptab{$ulogin}{busname} = trim $input{busname};
   hddebug "fname = $emptab{$ulogin}{fname}";

   ### zone does not exist in addressbook. so we don't use it.
   #$emptab{$ulogin}{zone} = trim $input{zone};

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%logtab)->sync();
   tied(%emptab)->sync();

   status("$login: You have successfully updated your contact. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmembersdir&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to Members Directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory.");
    
}

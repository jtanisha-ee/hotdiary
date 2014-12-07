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
# FileName: savebusinesscontact.cgi 
# Purpose: add a business contact to the folders
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
   $SESSION_TIMEOUT = 3600;

   #print &PrintHeader;
   #print &HtmlTop ("addbusinesscontact.cgi ");
   hddebug ("savebusinesscontact.cgi ");

   $vdomain = trim $input{'vdomain'};
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
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
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

   $rh = $input{rh};
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};

   $rh = $input{rh};
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execshowcontactlist = encurl "execshowcontactlist.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execshowcontactlist = "execshowcontactlist.cgi";
   }
 
   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=4\">here</a> to return to business home."); 
      exit;        
   }

   $contacttype = $input{contacttype};
   if ($contacttype eq "Resellers") {
      $execfile = "execresellersdir.cgi";
   }
   if ($contacttype eq "Others") {
      $execfile = "execotherdir.cgi";
   }
   if ($contacttype eq "Customers") {
      $execfile = "execcustomerdir.cgi";
   }
   if ($os ne "nt") {
      $execfile = encurl "$execfile";
   } else {
      $execfile = "$execfile";
   }

   $successpage = "Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execfile&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to view ($contacttype) directory.";    

   if ($login ne $businesstab{$business}{businessmaster}) {
      if (!-d("$ENV{HDDATA}/business/business/$business/managertab")) {
         status("$login: You do not have the permission to update contacts in ($business). <BR>$successpage<BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory.");
	 exit;
      }
   }

   if (!-d("$ENV{HDDATA}/business/business/$business/mgraccesstab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/mgraccesstab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/mgraccesstab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/mgraccesstab";
   }

   if ($login ne $businesstab{$business}{businessmaster}) {
      # bind manager table vars
      tie %managertab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login']};

      if (exists ($managertab{$login})) {
	 
         tie %mgraccesstab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother', 
		'invite', 'approve', 'delete', 'edit', 'manage', 
		'contact', 'teams']};

	 if ($mgraccesstab{access}{contact} ne "CHECKED") {
            status("$login: You are the business manager for ($business) but you do not have the permission to update contacts in ($business). Manager Role settings have to be enabled to update contacts in ($business). <BR>$successpage<BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory."); 
	    exit;
         }
      } else {
         status("$login: You do not have the permission to update contacts in ($business). <BR>$successpage<BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory.");
         exit;
      }
   } 

   $street =  $input{street}; 
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
       status("Invalid characters in Country ($input{'country'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notNumber($input{zipcode})) {
       status("Invalid characters in Zipcode ($input{'zipcode'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{hphone})) {
       status("Invalid characters in Home Phone ($input{'hphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
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
   if (notName($input{title})) {
       status("Invalid characters in Title ($input{'title'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notName($input{busname})) {
       status("Invalid characters in Business Name ($input{'busname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }


   hddebug "fname = $input{fname}";
   $fname = trim $input{fname};
   $lname = trim $input{lname};
   $aptno = trim $input{aptno};
   $street = trim $input{street};
   $city = trim $input{city};
   $state = trim $input{state};
   $zipcode = trim $input{zipcode};
   $country = trim $input{country};
   $hphone = trim $input{hphone};
   $bphone = trim $input{bphone};
   $cphone = trim $input{cphone};
   $pager = trim $input{pager};
   $fax = trim $input{fax};
   $email = trim $input{email};
   $url = trim $input{url};
   $other = trim $input{other};
   $title = trim $input{title};
   $bday = trim $input{bday};
   $bmonth = trim $input{bmonth};
   $byear = trim $input{byear};
   $busname = trim $input{busname};
   $pagertype = trim $input{pagertype};
   hddebug "pagertype = $pagertype";
   hddebug "hphone = $hphone";


 
   hddebug "contacttype = $contacttype";

   # indicates a new entry
   if ($input{newentry} == 0) {
     $entkey = getkeys();
   } else {
     $entkey = $input{entryno};
   }
   hddebug "newentry = $input{newentry}";

   if ($contacttype eq "Resellers") {
      if (!(-d "$ENV{HDDATA}/business/business/$business/directory/resellertab"))  {
         system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/resellertab";
         system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/resellertab";
         system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory/resellertab";
      }
      # bind resellertab table vars
      tie %resellertab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/resellertab",
          SUFIX => '.rec',
          SCHEMA => {
               ORDER => ['login', 'fname', 'lname', 'street',
               'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
               'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
               'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

      $resellertab{$entkey}{fname} = $fname;
      $resellertab{$entkey}{lname} = $lname;
      $resellertab{$entkey}{street} = $street;
      $resellertab{$entkey}{city} = $city;
      $resellertab{$entkey}{state} = $state;
      $resellertab{$entkey}{zipcode} = $zipcode;
      $resellertab{$entkey}{country} = $country;
      $resellertab{$entkey}{phone} = $hphone;
      $resellertab{$entkey}{pager} = $pager;
      $resellertab{$entkey}{pagertype} = $pagertype;
      $resellertab{$entkey}{fax} = $fax;
      $resellertab{$entkey}{cphone} = $cphone;
      $resellertab{$entkey}{bphone} = $bphone;
      $resellertab{$entkey}{email} = $email;
      $resellertab{$entkey}{url} = $url;
      $resellertab{$entkey}{id} = $id;
      $resellertab{$entkey}{other} = $other;
      $resellertab{$entkey}{aptno} = $aptno;
      $resellertab{$entkey}{busname} = $busname;
      $resellertab{$entkey}{bday} = $bday;
      $resellertab{$entkey}{bmonth} = $bmonth;
      $resellertab{$entkey}{byear} = $byear;
      $resellertab{$entkey}{title} = $title;
      $resellertab{$entkey}{busname} = $busname;
      tied(%resellertab)->sync();
   }

   if ($contacttype eq "Others") {
      if (!(-d "$ENV{HDDATA}/business/business/$business/directory/othertab"))  {
         system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/othertab";
         system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/othertab";
         system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory/othertab";
      }
      # bind othertab table vars
      tie %othertab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/othertab",
          SUFIX => '.rec',
          SCHEMA => {
               ORDER => ['login', 'fname', 'lname', 'street',
               'city', 'state', 'zipcode', 'country', 'phone', 'pager', 
               'pagertype', 'fax', 'cphone', 'bphone','email', 'url',
     	       'id', 'other', 'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

      $othertab{$entkey}{fname} = $fname;
      $othertab{$entkey}{lname} = $lname;
      $othertab{$entkey}{street} = $street;
      $othertab{$entkey}{city} = $city;
      $othertab{$entkey}{state} = $state;
      $othertab{$entkey}{zipcode} = $zipcode;
      $othertab{$entkey}{country} = $country;
      $othertab{$entkey}{phone} = $hphone;
      $othertab{$entkey}{pager} = $pager;
      $othertab{$entkey}{pagertype} = $pagertype;
      $othertab{$entkey}{fax} = $fax;
      $othertab{$entkey}{cphone} = $cphone;
      $othertab{$entkey}{bphone} = $bphone;
      $othertab{$entkey}{email} = $email;
      $othertab{$entkey}{url} = $url;
      $othertab{$entkey}{id} = $id;
      $othertab{$entkey}{other} = $other;
      $othertab{$entkey}{aptno} = $aptno;
      $othertab{$entkey}{busname} = $busname;
      $othertab{$entkey}{bday} = $bday;
      $othertab{$entkey}{bmonth} = $bmonth;
      $othertab{$entkey}{byear} = $byear;
      $othertab{$entkey}{title} = $title;
      $othertab{$entkey}{busname} = $busname;
      tied(%othertab)->sync();
   }


   if ($contacttype eq "Customers") {
      if (!(-d "$ENV{HDDATA}/business/business/$business/directory/customertab"))     {
         system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/customertab";
         system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/customertab";
         system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory/customertab";
      }

      # bind customertab table vars
      tie %customertab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/customertab",
          SUFIX => '.rec',
          SCHEMA => {
               ORDER => ['login', 'fname', 'lname', 'street',
               'city', 'state', 'zipcode', 'country', 'phone', 'pager', 
               'pagertype', 'fax', 'cphone', 'bphone','email', 'url',
     	       'id', 'other', 'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

      $customertab{$entkey}{fname} = $fname;
      $customertab{$entkey}{lname} = $lname;
      $customertab{$entkey}{street} = $street;
      $customertab{$entkey}{city} = $city;
      $customertab{$entkey}{state} = $state;
      $customertab{$entkey}{zipcode} = $zipcode;
      $customertab{$entkey}{country} = $country;
      $customertab{$entkey}{phone} = $hphone;
      $customertab{$entkey}{pager} = $pager;
      $customertab{$entkey}{pagertype} = $pagertype;
      $customertab{$entkey}{fax} = $fax;
      $customertab{$entkey}{cphone} = $cphone;
      $customertab{$entkey}{bphone} = $bphone;
      $customertab{$entkey}{email} = $email;
      $customertab{$entkey}{url} = $url;
      $customertab{$entkey}{id} = $id;
      $customertab{$entkey}{other} = $other;
      $customertab{$entkey}{aptno} = $aptno;
      $customertab{$entkey}{busname} = $busname;
      $customertab{$entkey}{bday} = $bday;
      $customertab{$entkey}{bmonth} = $bmonth;
      $customertab{$entkey}{byear} = $byear;
      $customertab{$entkey}{title} = $title;
      $customertab{$entkey}{busname} = $busname;
      tied(%customertab)->sync();
   }
   
 
   status("$login: Your contact information has been added to ($contacttype) folder. <BR>$successpage<BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory.");

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   
}

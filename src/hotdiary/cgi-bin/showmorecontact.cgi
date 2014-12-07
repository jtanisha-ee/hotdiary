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
# FileName: showmorecontact.cgi 
# Purpose: shows the details about contact information in resellers, others and customers dir
# Called by  More Link in the directory display 
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

   hddebug ("showmorecontact.cgi ");

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
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
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
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
   }

   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   $contacttype = $input{contacttype};
 
   $entryno = $input{entryno};
   if (($entryno eq "") || ($contacttype eq "")){
      status("$login: Contact information is missing.<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");

      #status("$login: Contact information is missing. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }
 
   hddebug "contacttype = $contacttype";
   hddebug "entryno = $entryno";

   if ($os ne "nt") {
      $execshowviewbusiness = encurl "execshowviewbusiness.cgi";
   } else {
      $execshowviewbusiness =  "execshowviewbusiness.cgi";
   }
 
  if ($contacttype eq "Resellers") {
    if (!-d("$ENV{HDDATA}/business/business/$business/directory/resellertab")) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/resellertab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/resellertab";
       status("$login: Reseller contact does not exist.  Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowviewbusiness&p1=biscuit&p2=businesstitle&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesstitle=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to View Business Directory.");
      exit; 
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

       $fname =  $resellertab{$entryno}{fname}; 
       $lname =  $resellertab{$entryno}{lname}; 
       $street =  $resellertab{$entryno}{street}; 
       $city =  $resellertab{$entryno}{city}; 
       $state =  $resellertab{$entryno}{state}; 
       $zipcode =  $resellertab{$entryno}{zipcode}; 
       $country =  $resellertab{$entryno}{country}; 
       $url =  $resellertab{$entryno}{url}; 
       $cellphone =  $resellertab{$entryno}{cphone}; 
       $workphone =  $resellertab{$entryno}{bphone}; 
       $homephone =  $resellertab{$entryno}{phone}; 
       $busname =  $resellertab{$entryno}{busname}; 
       $email =  $resellertab{$entryno}{email}; 
       $pager =  $resellertab{$entryno}{pager}; 
       $pagertype =  $resellertab{$entryno}{pagertype}; 
       $fax =  $resellertab{$entryno}{fax}; 
       $other =  $resellertab{$entryno}{other}; 
       $aptno =  $resellertab{$entryno}{aptno}; 
       $title =  $resellertab{$entryno}{title}; 
       $ulogin =  $fname . " " . $lname;
    }
    if ($contacttype eq "Others") { 
       if (!-d("$ENV{HDDATA}/business/business/$business/directory/othertab")) {
          system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/othertab";
          system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/othertab";
          status("$login: Contact information is not found. <BR> Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowviewbusiness&p1=biscuit&p2=businesstitle&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesstitle=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to View Business Directory.");
         exit; 
      }
      # bind othertab table vars
      tie %othertab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/othertab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'fname', 'lname', 'street',
               'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
               'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
               'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };
       

       $street =  $othertab{$entryno}{street}; 
       $fname =  $othertab{$entryno}{fname}; 
       $lname =  $othertab{$entryno}{lname}; 
       $city =  $othertab{$entryno}{city}; 
       $state =  $othertab{$entryno}{state}; 
       $zipcode =  $othertab{$entryno}{zipcode}; 
       $country =  $othertab{$entryno}{country}; 
       $url =  $othertab{$entryno}{url}; 
       $cellphone =  $othertab{$entryno}{cphone}; 
       $workphone =  $othertab{$entryno}{bphone}; 
       $busname =  $othertab{$entryno}{busname}; 
       $homephone =  $othertab{$entryno}{phone}; 
       $email =  $othertab{$entryno}{email}; 
       $pager =  $othertab{$entryno}{pager}; 
       $pagertype =  $othertab{$entryno}{pagertype}; 
       $fax =  $othertab{$entryno}{fax}; 
       $other =  $othertab{$entryno}{other}; 
       $title =  $othertab{$entryno}{title}; 
       $aptno =  $othertab{$entryno}{aptno}; 
       $ulogin =  $fname . " " . $lname;
   }
   if ($contacttype eq "Customers") {
       if (!-d("$ENV{HDDATA}/business/business/$business/directory/customertab")) {
         system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/customertab";
         system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/customertab";
         status("$login: Contact information is not found. <BR> Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowviewbusiness&p1=biscuit&p2=businesstitle&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesstitle=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to View Business Directory.");
         exit; 
     }

      # bind customertab table vars
      tie %customertab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/customertab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'fname', 'lname', 'street',
               'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
               'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
               'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

       $fname =  $customertab{$entryno}{fname}; 
       $lname =  $customertab{$entryno}{lname}; 
       $street =  $customertab{$entryno}{street}; 
       $city =  $customertab{$entryno}{city}; 
       $state =  $customertab{$entryno}{state}; 
       $zipcode =  $customertab{$entryno}{zipcode}; 
       $country =  $customertab{$entryno}{country}; 
       $url =  $customertab{$entryno}{url}; 
       $cellphone =  $customertab{$entryno}{cphone}; 
       $workphone =  $customertab{$entryno}{bphone}; 
       $busname =  $customertab{$entryno}{busname}; 
       $homephone =  $customertab{$entryno}{phone}; 
       $email =  $customertab{$entryno}{email}; 
       $pager =  $customertab{$entryno}{pager}; 
       $pagertype =  $customertab{$entryno}{pagertype}; 
       $fax =  $customertab{$entryno}{fax}; 
       $other =  $customertab{$entryno}{other}; 
       $title =  $customertab{$entryno}{title}; 
       $aptno =  $customertab{$entryno}{aptno}; 
       $ulogin =  $fname . " " . $lname;
   }

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $prml = "";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "uname=$uname";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsavebusinesscontact = encurl "execsavebusinesscontact.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execsavebusinesscontact =  "execsavebusinesscontact.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } 
  
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
 
   $prml = strapp $prml, "template=$ENV{HDTMPL}/showotherdir.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/showotherdir-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=26>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavebusinesscontact\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=entryno>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=fname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=lname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=aptno>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=street>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=city>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=state>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=zipcode>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=country>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=hphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=bphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=cphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=url>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=pager>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=pagertype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=other>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=fax>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=email>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=contacttype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=newentry>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p23 VALUE=title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p24 VALUE=busname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p25 VALUE=jp>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=entryno VALUE=$entryno>";
   # this indicates that it is an existing entry. so entryno is valid
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=newentry VALUE=1>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=contacttype VALUE=$contacttype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";

   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";

   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "fname=$fname";
   $prml = strapp $prml, "lname=$lname";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "url=$url";
   $prml = strapp $prml, "cphone=$cellphone";
   $prml = strapp $prml, "hphone=$homephone";
   $prml = strapp $prml, "bphone=$workphone";
   $prml = strapp $prml, "fax=$fax";
   $prml = strapp $prml, "email=$email";
   $prml = strapp $prml, "aptno=$aptno";
   $prml = strapp $prml, "other=$other";
   $prml = strapp $prml, "title=$title";
   $prml = strapp $prml, "pagertype=$pagertype"; 
   $prml = strapp $prml, "pager=$pager"; 
   $prml = strapp $prml, "ulogin=$ulogin"; 
   $prml = strapp $prml, "busname=$busname"; 
   $prml = strapp $prml, "jp=$jp"; 
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/showotherdir.html"; 
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/showotherdir-$$.html"; 


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

# need to add counter to keep track of faxes sent and also the fax numbers
# used for each customer.

   
# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

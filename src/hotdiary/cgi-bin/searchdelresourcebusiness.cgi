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
# FileName: modifyresourcebusiness.cgi
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

   hddebug("modifyresourcebusiness.cgi");

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
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&p2=jp&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

   
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
 

   if ($os ne "nt") {
      $execaddresourcebusiness = encurl "execaddresourcebusiness.cgi";
      $execmanageresourcesbusiness = encurl "execmanageresourcesbusiness.cgi";
   } else {
      $execaddresourcebusiness = "execaddresourcebusiness.cgi";
      $execmanageresourcesbusiness = "execmanageresourcesbusiness.cgi";
   }

   if (!(-d "$ENV{HDDATA}/business/business/$business/restab")) {
      status("$login: ($business) does not have any resources to manage. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execaddresourcebusiness&p1=biscuit&p2=business&pnum=4&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to add a resource. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmanageresourcesbusiness&p1=biscuit&p2=f&p3=business&p4=jp&pnum=5&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&f=cpc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage resources.");
      exit;
   }


   tie %restab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/restab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER =>  ['type', 'name', 'bldg', 'zipcode', 'country', 'tz'] };

  
   (@restabcount) = sort keys %restab;
   if ($#restabcount < 0) {
      status("$login: You do not have any resources to delete. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execaddresourcebusiness&p1=biscuit&p2=business&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to add a resource. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmanageresourcesbusiness&p1=biscuit&p2=f&p3=business&pnum=5&p4=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&f=cpc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage resources.");
     exit;
   }
 
   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execshowdelresourcebusiness = encurl "execshowdelresourcebusiness.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execshowdelresourcebusiness = "execshowdelresourcebusiness.cgi";
   }
   $prml = strapp $prml, "template=$ENV{HDTMPL}/searchresourcebusiness.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/searchresourcebusiness-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "label=Delete";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=4>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execshowdelresourcebusiness\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=resourcekey>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
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
   $prml = strapp $prml, "business=$business";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/searchresourcebusiness.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/searchresourcebusiness.html-$$";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

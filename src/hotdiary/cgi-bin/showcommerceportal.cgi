#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

## showcommerceportal.cgi

use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("showcommerceportal.cgi ");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
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
  



   $os = $input{os};
   if ($os ne "nt") {
      $execcommerceportal = encurl "execcommerceportal.cgi";
   } else {
      $execcommerceportal = "execcommerceportal.cgi";
   }

   $sc = $input{sc};


   if ($logo ne "") {
      $logo = adjusturl $logo;
     
   }   

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   if ($jp ne "") {
      if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/commerceportal.html") {
         $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/commerceportal.html";
      } else {
         $tmpl = "$ENV{HDTMPL}/commerceportal.html";
      }
   } else {
      $tmpl = "$ENV{HDTMPL}/commerceportal.html";
   }


   $prml = "";

   #$prml = strapp $prml, "template=$ENV{HDTMPL}/commerceportal.html";
   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/commerceportal-$$.html";    
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "title=$label";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";

  
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=7>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execcommerceportal\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=jiveit>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=wordit>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=communityevents>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=newsdiary>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";        

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
 
   parseIt $prml;  

   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/commerceportal-$$.html";


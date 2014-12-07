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
# FileName: calpreferences.cgi
# Purpose: Top screen for calendar preferences
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

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   hddebug ("calpreferences.cgi");

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
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com by sending email to support\@$diary, and they will be happy to help you with the license.");
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


   # bind surveytab table vars
   tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };

   # bind portaltab table vars
   tie %portaltab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/portaltab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'calcolor', 'photo', 'title', 'logo',
                'tbanner', 'bbanner', 'but1', 'but2', 'but3', 'but4',
                'audio'] };                          


   $editcal = $surveytab{$login}{editcal};
   $calpeople = $surveytab{$login}{calpeople};
   $calinvite = $surveytab{$login}{'calinvite'};


   if (exists($portaltab{$login})) {
      $callogo = adjusturl $portaltab{$login}{'logo'};
      $photo = adjusturl $portaltab{$login}{'photo'};
      $title = adjusturl $portaltab{$login}{'title'};
  }
                                                         
   $calpublish = $logtab{$login}{calpublish};
   $zone = $logtab{$login}{'zone'};
   $zonestr = getzonestr($zone);

   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $rh = $input{rh};
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execcalsettings = encurl "execcalsettings.cgi";
      $execcalclient = encurl "execcalclient.cgi";
      $execfilebrowser = encurl "execfilebrowser.cgi";
      $execsetupdowntown= encurl "execsetupdowntown.cgi";
      $execsavecalpreferences= encurl "execsavecalpreferences.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execcalsettings =  "execcalsettings.cgi";
      $execcalclient = "execcalclient.cgi";
      $execfilebrowser = "execfilebrowser.cgi";
      $execsetupdowntown= "execsetupdowntown.cgi";
      $execsavecalpreferences= "execsavecalpreferences.cgi";
   }

   $alphajp = substr $jp, 0, 1;
   $alphajp = $alphajp . '-index';
   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';
   
   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphajp/$jp/templates/calpreferences.html") ) {
       $tmpl = "$ENV{HDDATA}/$alphajp/$jp/templates/calpreferences.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/calpreferences.html";
   }   

   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/calpreferences-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execcalsettings=$execcalsettings";
   $prml = strapp $prml, "execcalclient=$execcalclient";
   $prml = strapp $prml, "execfilebrowser=$execfilebrowser";
   $prml = strapp $prml, "execsetupdowntown=$execsetupdowntown";
   $prml = strapp $prml, "execsetupdowntown=$execsetupdowntown";

   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "setup=Setup My Downtown";
   $prml = strapp $prml, "reset=";
   $prml = strapp $prml, "editcal=$editcal";
   $prml = strapp $prml, "calpeople=$calpeople";
   $prml = strapp $prml, "zone=$zone";
   $prml = strapp $prml, "zonestr=$zonestr";
   $prml = strapp $prml, "calpublish=$calpublish";
   $prml = strapp $prml, "zone=$zone";  
   $prml = strapp $prml, "calinvite=$calinvite";  
   $prml = strapp $prml, "title=$title";  
   $prml = strapp $prml, "photo=$photo";  
   $prml = strapp $prml, "tbanner=";  
   $prml = strapp $prml, "bbanner=";  
   $prml = strapp $prml, "but1=";  
   $prml = strapp $prml, "but2=";  
   $prml = strapp $prml, "but3=";  
   $prml = strapp $prml, "but4=";  
   $prml = strapp $prml, "callogo=$callogo";  

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=20>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavecalpreferences\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=editcal>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=calpeople>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=zonestr>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=calinvite>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=calpublish>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=reset>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=savecolor>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=callogo>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=tbanner>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=bbanner>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=photo>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=but1>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=but2>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=but3>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=but4>";

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

   if ($calpublish eq "CHECKED") {
      $site = adjusturl "http://$vdomain/members/$alpha/$login";
   }

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alpha/$login/calpreferences-$$.html";
   hdsystemcat "$ENV{HDHREP}/$alpha/$login/calpreferences-$$.html";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();


# - Title On The Top (eg. Events For City Of Bern)
#        - Logo On Top Left
#        - Bottom Banner
#        - Top Banner
#        - One picture on left
#        - 4 button banners
#        - Color or Tile background
#        - Background Audio Clip              

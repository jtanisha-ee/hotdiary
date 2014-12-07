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
# FileName: showbusinessother.cgi 
# Purpose: shows the details about login
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

   hddebug ("showbusinessother.cgi ");

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
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 
	'pagertype', 'fax', 'cphone', 'bphone', 'email', 'url', 
	'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 
	'zone', 'calpublish'] };

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
  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $rh = $input{rh};
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ($os ne "nt") {
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execbusiness = encurl "execbusiness.cgi";
   } else {
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execbusiness = "execbusiness.cgi";
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
   hddebug "ulogin = $ulogin";
   if (($ulogin eq "") || (!exists($logtab{$ulogin})) ){
      if ($os ne "nt") {    
         $execshowviewbusiness = encurl "execshowviewbusiness.cgi";
      } else {
         $execshowviewbusiness = "execshowviewbusiness.cgi";
      }
       status("$login: ($ulogin) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execshowviewbusiness&p1=biscuit&p2=businesstitle&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesstitle=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to View Business Directory.");  
       exit;
   }

   $is_emptab = 0;
   if (-d ("$ENV{HDDATA}/business/business/$business/directory/emptab")) {
      # bind emptab table vars
      tie %emptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/emptab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['login', 'fname', 'lname', 'street',
           'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
           'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
           'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };
        
       if (exists($emptab{$ulogin})) {
         $is_emptab = 1;
       }
    }

    if ($is_emptab == 1) {
       $fname =  $emptab{$ulogin}{fname}; 
       $lname =  $emptab{$ulogin}{lname}; 
       $street =  $emptab{$ulogin}{street}; 
       $aptno =  $emptab{$ulogin}{aptno}; 
       $city =  $emptab{$ulogin}{city}; 
       $state =  $emptab{$ulogin}{state}; 
       $zipcode =  $emptab{$ulogin}{zipcode}; 
       $country =  $emptab{$ulogin}{country}; 
       $url =  $emptab{$ulogin}{url}; 
       $cellphone =  $emptab{$ulogin}{cphone}; 
       $workphone =  $emptab{$ulogin}{bphone}; 
       $busname =  $emptab{$ulogin}{busname}; 
       $homephone =  $emptab{$ulogin}{phone}; 
       $email =  $emptab{$ulogin}{email}; 
       $pager =  $emptab{$ulogin}{pager}; 
       $pagertype =  $emptab{$ulogin}{pagertype}; 
       $fax =  $emptab{$ulogin}{fax}; 
       #$zone =  $emptab{$ulogin}{zone}; 
       #$zonestr =  getzonestr ($emptab{$ulogin}{zone}); 
       $other =  $emptab{$ulogin}{other}; 
       $title =  $emptab{$ulogin}{title}; 
     } else {
       $street =  $logtab{$ulogin}{street}; 
       $fname =  $logtab{$ulogin}{fname}; 
       $lname =  $logtab{$ulogin}{lname}; 
       $city =  $logtab{$ulogin}{city}; 
       $aptno =  $logtab{$ulogin}{aptno}; 
       $state =  $logtab{$ulogin}{state}; 
       $zipcode =  $logtab{$ulogin}{zipcode}; 
       $country =  $logtab{$ulogin}{country}; 
       $url =  $logtab{$ulogin}{url}; 
       $cellphone =  $logtab{$ulogin}{cphone}; 
       $workphone =  $logtab{$ulogin}{bphone}; 
       $homephone =  $logtab{$ulogin}{phone}; 
       $busname =  $logtab{$ulogin}{busname}; 
       $email =  $logtab{$ulogin}{email}; 
       $pager =  $logtab{$ulogin}{pager}; 
       $pagertype =  $logtab{$ulogin}{pagertype}; 
       $fax =  $logtab{$ulogin}{fax}; 
       #$zone =  $logtab{$ulogin}{zone}; 
       #$zonestr =  getzonestr ($logtab{$ulogin}{zone}); 
       $other =  $logtab{$ulogin}{other}; 
       $title =  $logtab{$ulogin}{title}; 
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
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsavebusinessdir = encurl "execsavebusinessdir.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execsavebusinessdir = "execsavebusinessdir.cgi";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }
   $prml = strapp $prml, "template=$ENV{HDTMPL}/showbusinessother.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/showbusinessother-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=24>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavebusinessdir\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=ulogin>";
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
   #$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=other>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=fax>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=email>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p23 VALUE=busname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=ulogin VALUE=$ulogin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=5>";
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
   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";

   $prml = strapp $prml, "label=";
   $prml = strapp $prml, "biscuit=$biscuit";
   hddebug "fname = $fname";
   $prml = strapp $prml, "fname=$fname";
   $prml = strapp $prml, "lname=$lname";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "url=$url";
   $prml = strapp $prml, "cphone=$cellphone";
   #$prml = strapp $prml, "zone=$zone";
   #$prml = strapp $prml, "zonestr=$zonestr";
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
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/showbusinessother.html"; 
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/showbusinessother-$$.html"; 

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

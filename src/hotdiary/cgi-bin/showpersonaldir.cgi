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
# FileName: showpersonal.cgi 
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
use scheduleresolve::scheduleresolve;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("showpersonal.cgi ");
   hddebug ("showpersonal.cgi ");

   $vdomain = trim $input{'vdomain'};
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
               status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
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
  
   $ulogin = $input{ulogin};
   hddebug "ulogin = $ulogin";
   $g = "";
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   # bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

   if (($ulogin eq "") || (!exists($addrtab{$ulogin})) ){
       status("$login: ($ulogin) does not exist."); 
       exit;
   }

      $fname =  $addrtab{$ulogin}{fname}; 
      $lname =  $addrtab{$ulogin}{lname}; 
       $street =  $addrtab{$ulogin}{street}; 
       $aptno =  $addrtab{$ulogin}{aptno}; 
       $city =  $addrtab{$ulogin}{city}; 
       $state =  $addrtab{$ulogin}{state}; 
       $zipcode =  $addrtab{$ulogin}{zipcode}; 
       $country =  $addrtab{$ulogin}{country}; 
       $url =  $addrtab{$ulogin}{url}; 
       $cellphone =  $addrtab{$ulogin}{cphone}; 
       $workphone =  $addrtab{$ulogin}{bphone}; 
       $homephone =  $addrtab{$ulogin}{phone}; 
       $email =  $addrtab{$ulogin}{email}; 
       $pager =  $addrtab{$ulogin}{pager}; 
       $pagertype =  $addrtab{$ulogin}{pagertype}; 
       $fax =  $addrtab{$ulogin}{fax}; 
       $other =  $addrtab{$ulogin}{other}; 
       $other = adjusturl $other;
       $addrtab{$ulogin}{other} = $other;
       tied(%addrtab)->sync();
       $title =  $addrtab{$ulogin}{title}; 
       $bday =  $addrtab{$ulogin}{bday}; 
       $bmonth =  $addrtab{$ulogin}{bmonth}; 
       $byear =  $addrtab{$ulogin}{byear}; 
       $busname =  $addrtab{$ulogin}{busname}; 


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
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execsavepersonaldir =  encurl "execsavepersonaldir.cgi";
      $execpersonaldir =  encurl "execpersonaldir.cgi";
      $execaddpersonalcontact =  encurl "execaddpersonalcontact.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execsavepersonaldir =  "execsavepersonaldir.cgi";
      $execpersonaldir =  "execpersonaldir.cgi";
      $execaddpersonalcontact =  "execaddpersonalcontact.cgi";
   }

   $folder = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $folder .= "<TR WIDTH=\"100%\"><TD WIDTH=\"100%\">";

   $folder .= "<TABLE BORDER=0 CELLPADDING=5 CELLSPACING=0 BGCOLOR=ee9900 WIDTH=\"100%\">";
   $folder .= "<TR ALIGN=CENTER WIDTH=\"100%\">";       

   for ($i =0; $i <= 25; $i = $i + 1) {
      $letter = chr(65 + $i); 
      $lt = scheduleresolve::scheduleresolve::isaddr($letter, $login, $g); 
      if ($lt == 1) {
         $letterlink = adjusturl("execdogeneric.jsp?pnum=6&p0=$execpersonaldir&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&rh=$rh&jp=$jp&vdomain=$vdomain&hs=$hs&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6&letter=$letter&all=");

      
         $folder .= "<TD ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</a></FONT></TD>";
     } else {
         $folder .= "<TD ALIGN=CENTER SIZE=1><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</FONT></TD>";
     }
   }

   
   $letterlink = adjusturl("execdogeneric.jsp?pnum=6&p0=$execpersonaldir&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&jp=$jp&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6&letter=&all=all");
   $folder .= "<TD ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">All</a></FONT></TD>";

   $folder .= "</TR></TABLE>";
   $folder .= "</TD></TR></TABLE>";
   $folder = adjusturl($folder);

   $alphj = substr $jp, 0, 1;
   $alphj = $alphj . '-index';

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphj/$jp/templates/showpersonal.html") ) {
      $template = "$ENV{HDDATA}/$alphj/$jp/templates/showpersonal.html";
   } else {
      $template = "$ENV{HDTMPL}/showpersonal.html";
   }   


   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/showpersonal-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=28>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavepersonaldir\">";
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p23 VALUE=bday>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p24 VALUE=bmonth>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p25 VALUE=byear>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p26 VALUE=busname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p27 VALUE=jp>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=ulogin VALUE=$ulogin>";
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
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execaddpersonalcontact=$execaddpersonalcontact";
   $prml = strapp $prml, "bday=$bday";
   $prml = strapp $prml, "bmonth=$bmonth";
   $prml = strapp $prml, "byear=$byear";
   $prml = strapp $prml, "busname=$busname";
   $prml = strapp $prml, "letter=$folder";
   $prml = strapp $prml, "jp=$jp";
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/showpersonal.html"; 
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/showpersonal-$$.html"; 

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

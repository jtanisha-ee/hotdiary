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
# FileName: showpartyentry.cgi
# Purpose: Join A Virtual Intranet
# Creation Date: 09-12-99
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

   hddebug "showpartyentry()";

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

   $sesstab{$biscuit}{'time'} = time();

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

   # bind party table vars
   tie %partytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'subject', 'distribution', 'partyedit',
        'zone'] };

   $entryno = $input{entryno};
   $zone = $partytab{$entryno}{zone};
   $zonestr = getzonestr($zone);
   $month = $partytab{$entryno}{month};
   $monthstr = getmonthstr($month);
   $day = $partytab{$entryno}{day};
   $year = $partytab{$entryno}{year};
   $hour = $partytab{$entryno}{hour};
   $min = $partytab{$entryno}{min};
   $meridian = $partytab{$entryno}{meridian};
   $dhour = $partytab{$entryno}{dhour};
   $dmin = $partytab{$entryno}{dmin};
   $dtype = $partytab{$entryno}{dtype};
   $atype = $partytab{$entryno}{atype};
   $desc = $partytab{$entryno}{desc};
   $subject = $partytab{$entryno}{subject};
   $distribution = $partytab{$entryno}{distribution};
   $partyedit = $partytab{$entryno}{partyedit};
   
   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $rh = $input{rh};
   #$prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label1=Party Planner/Party Reminder/Calendar";
   $prml = strapp $prml, "label2=Party event details. <BR>You can make changes to this event and save it.";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execsavepartyentry =  encurl "execsavepartyentry.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execsavepartyentry =  "execsavepartyentry.cgi";
   }

   $alphj = substr $jp, 0, 1;
   $alphj = $alphj . '-index';

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphj/$jp/templates/showpartyentry.html") ) {
      $template = "$ENV{HDDATA}/$alphj/$jp/templates/showpartyentry.html";
   } else {
      $template = "$ENV{HDTMPL}/showpartyentry.html";
   }  

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/showpartyentry-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "business=$business";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=22>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execsavepartyentry>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=subject>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=year>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=zonestr>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=entryno>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=sendnow>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=hour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=min>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=meridian>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=dhour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=dmin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=dtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=atype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=desc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=distribution>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=partyedit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=delete>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=entryno VALUE=$entryno>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
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

   $subject = adjusturl $subject;
   $prml = strapp $prml, "subject=$subject";
   $prml = strapp $prml, "zone=$zone";
   $prml = strapp $prml, "zonestr=$zonestr";
   $prml = strapp $prml, "month=$monthstr";
   $prml = strapp $prml, "monthnum=$month";
   $prml = strapp $prml, "day=$day";
   $prml = strapp $prml, "year=$year";
   $prml = strapp $prml, "hour=$hour";
   $prml = strapp $prml, "min=$min";
   $prml = strapp $prml, "meridian=$meridian";
   $prml = strapp $prml, "dhour=$dhour";
   $prml = strapp $prml, "dmin=$dmin";
   $prml = strapp $prml, "atype=$atype";
   $prml = strapp $prml, "dtype=$dtype";
   $prml = strapp $prml, "jp=$jp";
   $desc = adjusturl $desc;
   $prml = strapp $prml, "desc=$desc";
   $distribution = adjusturl $distribution;
   $prml = strapp $prml, "distribution=$distribution";
   $prml = strapp $prml, "partyedit=$partyedit";

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/showpartyentry.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showpartyentry-$$.html";

   # reset the timer.

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

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
# FileName: partyplanner.cgi
# Purpose: Top screen for partyplanner
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

   hddebug ("partyplanner.cgi");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";
   $rh = $input{rh};
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

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if (-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/sgrouptab") {

      tie %pgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/personal/pgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
      (@records) = sort keys %pgrouptab;

      if ($#records >= 0) {
         for ($l = 0; $l <= $#records; $l++) {
            $records[$l] = "\L$records[$l]";
            $multsel = $multsel . "\<OPTION\>$records[$l]\<\/OPTION\>";
            #$cgroups .= $records[$l];
            #$cgroups .= " ";
         }
      }
   }
   

   if (-d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab") {
      tie %sgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

      (@records1) = sort keys %sgrouptab;
      if ($#records1 >= 0) {
         for ($l = 0; $l <= $#records1; $l++) {
             $records[$l] = "\L$records[$l]";
             $multsel = $multsel . "\<OPTION\>$records1[$l]\<\/OPTION\>";
             #$cgroups .= $records1[$l];
             #$cgroups .= " ";
         }
      }
   }


   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());

   $monthstr = getmonthstr($mon+1);
   $newmonth = $mon + 1;
   $zone = $logtab{$login}{'zone'};
   if ($zone eq "") {
      $zone = -8;
   }

   $zonestr = getzonestr($zone);


   if (-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab") {
      tie %fgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

      (@records2) = sort keys %fgrouptab;

      if ($#records2 >= 0) {
         for ($l = 0; $l <= $#records2; $l++) {
            $multsel = $multsel . "\<OPTION\>$records2[$l]\<\/OPTION\>";
            #$cgroups .= $records2[$l];
            #$cgroups .= " ";
         }
      }
   }

   if (($#records < 0) && ($#records1 < 0) && ($#records2 < 0)) {
        $multsel = "<OPTION>No Group</OPTION>";
        #$cgroups = "";
   }
   


   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "logo=$logo";
   $sc = $input{sc};

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      #$formenc = adjusturl "ENCTYPE=\"multipart/form-data\"";
     
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execpartyaddsearch = encurl "execpartyaddsearch.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execpartyaddsearch = "execpartyaddsearch.cgi";
   }

   ## (@hshcdir) = split " ", $cgroups;

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execpartyaddsearch\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=add>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=search>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=year>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=hour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=meridian>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=min>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=sendnow>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=sec>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=dhour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=dmin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=desc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=distribution>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=subject>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=atype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=dtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=partyedit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=pgroups>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr21 VALUE=multsel>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=jp>";

   #values of checkboxes as each parameter
   $mcntr = 23;
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
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

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/menupartytbl.html") ) {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/menupartytbl.html";
   } else {
      $template = "$ENV{HDTMPL}/menupartytbl.html";
   }  

   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/menupartytbl-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "label1=Party Planner/Party Reminder/Calendar";
   $prml = strapp $prml, "label2=Party Reminders are sent a minimum of 20 minutes in advance of due time.";
   $prml = strapp $prml, "label3=Your party events will appear in your personal calendar and other invitees calendars when you add party events.";
   $prml = strapp $prml, "distopt=$multsel";
   $prml = strapp $prml, "monthnum=$newmonth";
   $prml = strapp $prml, "month=$monthstr";
   $prml = strapp $prml, "day=$mday";
   $prml = strapp $prml, "zone=$zone";
   $prml = strapp $prml, "zonestr=$zonestr";

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/menupartytbl.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/menupartytbl-$$.html";

   hddebug "completed partyplanner";
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

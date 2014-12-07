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
# FileName: hdshowbizbg.cgi
# Purpose: New HotDiary showbiz bg
# Creation Date: 06-14-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;                                
use tparser::tparser;
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ($biscuit eq "") {
      if ($hs eq "") {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
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
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
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
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/index.html\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/index.html\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $f = $input{f};
   if ($f eq "") {
      $f = "sgc";
   }

   $rh = $input{'rh'};
   hddebug "rh = $rh";
   $label = "HotDiary";
   $logo = "";
   $partnerlogo = "";

   if ($rh ne "") {
      $ip = $input{HDLIC};
      tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['HDLIC', 'partner', 'IP'] };

       tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

       if (exists $lictab{$ip}) {
          $partner = $lictab{$ip}{partner};
          hddebug "partner = $partner";
          if (exists $parttab{$partner}) {
             $logo = adjusturl $parttab{$partner}{logo};
             $partnerlogo = adjusturl $parttab{$partner}{logo};
             hddebug "logo = $logo";
             $title = $parttab{$partner}{title};
             hddebug "title = $title";
             $label = $title;
         }
      }
   }

# is this known?
$calname = $input{'calname'};

# the function name
# the parameter names
# the parameter values
# the pnum 
# searchcal, createcal, logo, $welcome, $login, $label, 

$cgi = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit";
$searchcal = adjusturl "$cgi&f=sgc";
$createcal = adjusturl "$cgi&f=cpc";
$fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";

if ($rh eq "") {
       $cgis = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit";
   } else {
       $cgis = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit";
   }

$hidden = "<input type=hidden name=p0 size=\"-1\" value=\"/cgi-bin/execshowbg.cgi\">";
$hidden .= "<input type=hidden name=p1 size=\"-1\" value=\"biscuit\">";
$hidden .= "<input type=hidden name=p2 size=\"-1\" value=\"rh\">";
$hidden .= "<input type=hidden name=p3 size=\"-1\" value=\"hs\">";
$hidden .= "<input type=hidden name=p4 size=\"-1\" value=\"vdomain\">";
$hidden .= "<input type=hidden name=p5 size=\"-1\" value=\"f\">";
$hidden .= "<input type=hidden name=p6 size=\"-1\" value=\"HDLIC\">";
$hidden .= "<input type=hidden name=p7 size=\"-1\" value=\"calname\">";
$hidden = adjusturl $hidden;

$prml = "";
$prml = strapp  $prml, "biscuit=$biscuit";
$prml = strapp  $prml, "calname=$calname";
$prml = strapp  $prml, "percal=$cgis";
$prml = strapp  $prml, "home=$fref";
$prml = strapp  $prml, "pnum=8";
$prml = strapp  $prml, "rh=$rh";
$prml = strapp  $prml, "logo=$logo";
$prml = strapp $prml, "pparms=$hidden";
$prml = strapp $prml, "welcome=Welcome";
$prml = strapp $prml, "$login=$login";
$prml = strapp $prml, "label=$label";
$prml = strapp $prml, "searchcal=$searchcal";
$prml = strapp $prml, "createcal=$createcal";
$prml = strapp $prml, "template=$ENV{HDTMPL}/hdshowbizbg.html";
$prml = strapp $prml, "templateout=/tmp/genericout";
parseIt $prml;

#print $prml;
 

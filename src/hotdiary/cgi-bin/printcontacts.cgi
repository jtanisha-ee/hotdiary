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
# FileName: printcontacts.cgi 
# Purpose: Create A Virtual Intranet
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("personaldir.cgi ");
   hddebug ("printcontacts.cgi ");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
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
  

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $sc = $input{sc};

 
   if ($os ne "nt") {
      $execaddpersonalcontact = encurl "execaddpersonalcontact.cgi";
      $execshowpersonaldir = encurl "execshowpersonaldir.cgi";
      $execshowpersonalpage = encurl "execshowpersonalpage.cgi";
      $execshowpersonalfax = encurl "execshowpersonalfax.cgi";
      $execpersonaldir = encurl "execpersonaldir.cgi";
      $execprintpersonaldir = encurl "execprintpersonaldir.cgi";
   } else {
      $execaddpersonalcontact = "execaddpersonalcontact.cgi";
      $execshowpersonaldir = "execshowpersonaldir.cgi";
      $execshowpersonalpage = "execshowpersonalpage.cgi";
      $execshowpersonalfax = "execshowpersonalfax.cgi";
      $execpersonaldir = "execpersonaldir.cgi";
      $execprintpersonaldir = "execprintpersonaldir.cgi";
   }

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


   if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
         $execpersonaldir = encurl "execpersonaldir.cgi";
   } else {
         $prb = strapp $prb, "formenc=";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execpersonaldir = "execpersonaldir.cgi";
   }

   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $g = "";
   $cnt = 0;
   (@sortlist) = sortcontacts($login, $g);
   #foreach $entry (sort keys %addrtab) {
   foreach $entry (@sortlist) {
      # hddebug "printcontact $cnt";

      if ( ($cnt % 2) == 0) {
         $msg .= "<TR>";
      }
      $msg .= "<TD WIDTH=\"50%\">";
      $msg .= "<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=10><TR><TD>";

      $fname = $addrtab{$entry}{fname};
      $lname = $addrtab{$entry}{lname};
      if ( ($fname ne "") || ($lname ne "") ) {
         $msg .= "<b>Name: $fname $lname</b><BR>";
      }
      $title = $addrtab{$entry}{title};
      if ($title ne "") {
         $msg .= "Title: $title<BR>";
      }
      $busname = $addrtab{$entry}{busname};
      if ($busname ne "") {
         $msg .= "<b>Business Name: $busname</b><BR>";
      }
      $aptno = $addrtab{$entry}{aptno};
      if ($aptno ne "") {
         $msg .= "No: $aptno<BR>";
      }
      $street = $addrtab{$entry}{street};
      if ($street ne "") {
         $msg .= "Street: $street<BR>";
      }
      $city = $addrtab{$entry}{city};
      $state = $addrtab{$entry}{state};
      $zipcode = $addrtab{$entry}{zipcode};
      if ( ($city ne "") || ($state ne "") || ($zipcode ne "") ) {
         $msg .= "City: $city<BR>";
         $msg .= "State: $state<BR>";
         $msg .= "Zipcode: $zipcode<BR>";
      }
      $country = $addrtab{$entry}{country};
      if ($country ne "") {
         $msg .= "Country: $country<BR>";
      }
      $phone = $addrtab{$entry}{phone};
      if ($phone ne "") {
         $msg .= "<b>Phone: $phone</b><BR>";
      }
      $pager = $addrtab{$entry}{pager};
      if ($pager ne "") {
         $msg .= "Pager: $pager<BR>";
      }
      $fax = $addrtab{$entry}{fax};
      if ($fax ne "") {
         $msg .= "Fax: $fax<BR>";
      }
      $cphone = $addrtab{$entry}{cphone};
      if ($cphone ne "") {
         $msg .= "Cell Phone: $cphone<BR>";
      }
      $bphone = $addrtab{$entry}{bphone};
      if ($bphone ne "") {
         $msg .= "<b>Business Phone: $bphone</b><BR>";
      }
      $email = $addrtab{$entry}{email};
      if ($email ne "") {
         $msg .= "<b>Email: $email</b><BR>";
      }
      $url = $addrtab{$entry}{url};
      if ($url ne "") {
         $msg .= "URL: $url<BR>";
      }
      $bday = $addrtab{$entry}{bday};
      $bmonth = $addrtab{$entry}{bmonth};
      $byear = $addrtab{$entry}{byear};
      if ( ($bday ne "") && ($bmonth ne "") && ($byear ne "") ) {
         $msg .= "Birth Date: $bmonth/$bday/$byear<BR>";
      }
      $other = $addrtab{$entry}{other};
      $other =~ s/\n/<BR>/g;
      if ($other ne "") {
         $msg .= "Other: $other<BR>";
      }

      $msg .= "</TD></TR></TABLE>";
      $msg .= "</TD>";
      if ( ($cnt % 2) == 1) {
         $msg .= "</TR>";
      }
      $cnt = $cnt + 1;
   }
   if ( ($cnt % 2) == 1 ) {
      $msg .= "<TD>&nbsp;</TD>";
   }
   $msg .= "</TABLE>";
   $msg = adjusturl $msg;

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/printcontacts.html") ) {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/printcontacts.html";
   } else {
      $template = "$ENV{HDTMPL}/printcontacts.html";
   }   

   $prml = "";
   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/printcontacts-$$.html";
   $prml = strapp $prml, "msg=$msg";
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "cnt=$cnt";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/printcontacts.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/printcontacts-$$.html";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

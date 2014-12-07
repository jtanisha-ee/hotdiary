#!/usr/bin/perl

# Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: carryonmail.cgi
# Purpose: Top screen for hotdiary carryon 
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


# parse the command line
   &ReadParse(*input);

   hddebug "carryonmail.cgi";
#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp};
   $framedomain = $input{framedomain};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   }
   $os = $input{os};

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

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

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
   # bind login table
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


   $basedir = trim $input{basedir};
   $filename = trim $input{filename};
   hddebug "filename = $filename";
   hddebug "basedir = $basedir";

  if ( ($basedir =~ /\.\./) || ($basedir =~ /\~/) ) {
    status("$login: Invalid directory specification. HotDiary Security Alert.");
    exit;
  }

  if ( ($filename =~ /\.\./) || ($filename =~ /\~/) ) {
    status("$login: Invalid filename specification. HotDiary Security Alert.");
    exit;
  }


  if (notCarryOnFile($basedir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) $msg.");
      exit;
  }

  if (notCarryOnName($filename)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-) and a single dot(.) $msg.");
      exit;
   }

   

   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alph/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };


   $cntr = 0;
   $mailto = "";
   foreach $mem (sort keys %addrtab) {
      #$memname = "$addrtab{$mem}{fname} $addrtab{$mem}{lname}";
      #$size = length $memname;
      #if ($size > 25) {
         #$namestr = $memname;
         #$memname = substr($namestr, 0, 25);
         #$size = $size - 25;
         ##$memname .= "<BR>";
         #$memname .= substr($namestr, 25, $size);
      #}
      $email = $addrtab{$mem}{email};
      #if ($size > 15) {
         #$mail = $email;
         #$email = substr($mail, 0, 15);
         #$size = $size - 15;
         ##$email .= "<BR>";
         #$email .= substr($mail, 15, $size);
      #}
      if (!(notEmailAddress $email)) {
         $mailto .= "\<OPTION\>$email<\/OPTION\>";
         $cntr = $cntr +1;
      }
   }

   #$mailto = adjusturl($mailto); 
   hddebug "cntr = $cntr";

   if ( ($framedomain ne "$hotdiary") && ($framedomain ne "$diary")) {
      $flg = 2;
   } else {
      $flg = "";
   }

   $back = "<a href=\"/cgi-bin/execfilebrowser.cgi?flg=$flg&framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&biscuit=$biscuit\"><FONT FACE=Verdana SIZE=3><B>My Carry-On</B></FONT></a>";

   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   #$prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execpersonaldir =  encurl "execpersonaldir.cgi";
      $execsendmail =  encurl "execsendmail.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execpersonaldir =  encurl "execpersonaldir.cgi";
      $execsendmail =   "execsendmail.cgi";
   }
  
   if ( ($framedomain eq "$hotdiary") || ($framedomain eq "$diary")) { 
      $prml = strapp $prml, "template=$ENV{HDTMPL}/sendmail.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/sendmail$$.html";
   } else {
      $prml = strapp $prml, "template=$ENV{HDTMPL}/jzsendmail.html";
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alph/$login/jzsendmail$$.html";
   }
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "business=$business";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=9>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execsendmail>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=filename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=directory>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=memail>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=subject>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=cc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=framedomain>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=filename VALUE=$filename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=basedir VALUE=$basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=framedomain VALUE=$framedomain>";

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
   $prml = strapp $prml, "status=";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execpersonaldir=$execpersonaldir";
   $prml = strapp $prml, "filename=$filename";
   $prml = strapp $prml, "memail=$mailto";
   $back = adjusturl $back;
   $prml = strapp $prml, "back=$back";
   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   if ( ($framedomain eq "$hotdiary") || ($framedomain eq "$diary")) { 
      #system "cat $ENV{HDHREP}/$alph/$login/sendmail$$.html";
      hdsystemcat "$ENV{HDHREP}/$alph/$login/sendmail$$.html";
   } else {
      #system "cat $ENV{HDREP}/$alph/$login/jzsendmail$$.html";
      hdsystemcat "$ENV{HDREP}/$alph/$login/jzsendmail$$.html";
   }

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

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
# FileName: editfile.cgi
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

   hddebug "editfile.cgi";
#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $vdomain = trim $input{'vdomain'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $rh = $input{rh};
   $jp = $input{jp};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};

   $framedomain = $input{framedomain};
   if ( ($framedomain ne "www.hotdiary.com") && ($framedomain ne "hotdiary.com")) {
      $flg = 2;
   } else {
      $flg = "";
   }


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

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if (!-e ("$ENV{HDCARRYON}/aux/carryon/$alpha/$login/permittab")) {
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$alpha/$login/permittab";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$alpha/$login/permittab";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$alpha/$login/permittab";
   }

      # bind logsess table vars
      tie %permittab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDCARRYON}/aux/carryon/$alpha/$login/permittab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'fn', 'permit', 'list', 'publish'] };

   $entryno = trim $input{en};
   hddebug "entryno = $entryno";
   if (exists($permittab{$entryno})) {
      if ("\L$permittab{$entryno}{fn}" eq "\L$filename") {
	 hddebug "exists $permittab{$entryno}{fn} ";
         $permit = $permittab{$entryno}{permit};
         $list = $permittab{$entryno}{list};
         $publish = $permittab{$entryno}{publish};
      }
   } 
   hddebug "publish = $publish";
   hddebug "list = $list";
   hddebug "permit = $permit";

   $back = "<a href=\"http://www.hotdiary.com/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&biscuit=$biscuit\"><FONT FACE=Verdana SIZE=3><B>My Carry-On</B></FONT></a>";

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
      $execsavefile =  encurl "execsavefile.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execsavefile =  "execsavefile.cgi";
   }
  
   if ( ($framedomain eq  "www.hotdiary.com") || ($framedomain eq "hotdiary.com")) {
      $prml = strapp $prml, "template=$ENV{HDTMPL}/editfile.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/editfile-$$.html";
   } else {
      $prml = strapp $prml, "template=$ENV{HDTMPL}/jzeditfile.html";
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha/$login/jzeditfile-$$.html";
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
   hddebug "vdomain = $vdomain";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=14>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execsavefile>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=filename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=permission>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=directory>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=list>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=move>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=rename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=newfilename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=publish>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=en>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=framedomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=radio1>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=filename VALUE=$filename>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=basedir VALUE=$basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=framedomain VALUE=$framedomain>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=en VALUE=$entryno>";
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
   $prml = strapp $prml, "list=$list";
   $prml = strapp $prml, "permission=$permission";
   $prml = strapp $prml, "filename=$filename";
   $prml = strapp $prml, "newfilename=$filename";
   $prml = strapp $prml, "publish=$publish";
   $prml = strapp $prml, "radio1=$permit";
   $personal = "";
   $public = "";
   $private = "";
   $personalval = "";
   $publicval = "";
   $privateval = "";
   if ($permit eq "personal") {
      $personal = $permit;
      $personalval = "CHECKED";
   }
   if ($permit eq "public") {
      $public = $permit;
      $publicval = "CHECKED";
   }
   if ($permit eq "private") {
      $private = $permit;
      $privateval = "CHECKED";
   }
   ## default value
   if ($permit eq "") {
      $personal = "personal";
      $personalval = "CHECKED";
   }
   $prml = strapp $prml, "public=$public";
   $prml = strapp $prml, "private=$private";
   $prml = strapp $prml, "personal=$personal";
   $prml = strapp $prml, "publicval=$publicval";
   $prml = strapp $prml, "privateval=$privateval";
   $prml = strapp $prml, "personalval=$personalval";
   $back = adjusturl $back;
   $prml = strapp $prml, "back=$back";
   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   if ( ($framedomain eq  "www.hotdiary.com") || ($framedomain eq "hotdiary.com")) {
      #system "cat $ENV{HDHREP}/$alpha/$login/editfile.html";
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/editfile-$$.html";
   } else {
      #system "cat $ENV{HDREP}/$alpha/$login/jzeditfile.html";
      hdsystemcat "$ENV{HDREP}/$alpha/$login/jzeditfile-$$.html";
   }

   hddebug "HDLIC = $HDLIC";
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

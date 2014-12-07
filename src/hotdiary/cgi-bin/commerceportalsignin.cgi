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

   hddebug "commerceportalsignin";

   $jp = $input{jp};
   $HDLIC = $input{HDLIC};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };     

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

   hddebug "jp = $jp";
   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
      hddebug "logo = $logo";
      hddebug "label = $label";
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }                                 

   #$vdomain = trim $input{'vdomain'};
   #if ($vdomain eq "") {
   #   $vdomain = "www.hotdiary.com";
   #}         

   $os = $input{os};
   if ($os ne "nt") {
      $execshowcommerceportal = encurl "execshowcommerceportal.cgi";
   } else {
      $execshowcommerceportal = "execshowcommerceportal.cgi";
   }

   if ($label eq "") {
      $label = "HotDiary";
   }

   if ($logo eq "") {
      $logo = "http://www.hotdiary.com/images/hdlogo.gif";
   }


   if ($logo ne "") {
         $logo = adjusturl $logo;
   }   
   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/commerceportalsignin.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/commerceportalsignin-$$.html";    
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "title=$label";

  
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execshowcommerceportal\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=login>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=password>";        
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";        
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
   system "/bin/cat $ENV{HDHREP}/$login/commerceportalsignin-$$.html";


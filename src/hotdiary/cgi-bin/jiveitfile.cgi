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
# FileName: jiveitfile.cgi 
# Purpose: jiveit file upload display
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   
use scheduleresolve::scheduleresolve;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("jiveitfile.cgi ");


   $login = $input{login};
   if (notLogin($login)) {
      status("Invalid characters in login ($login).");
     exit;
   }

   if ($login eq "") {
      status("Your login is empty");
      exit;
   }               

   $password = $input{password};
  
   # bind jivetab table vars

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner',
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   if (!exists($logtab{$login})) {
      status("Your login=$login is invalid. Please register before you can use JiveIt!");
       exit;
   }      

      # bind jivetab table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
             'topleft', 'topright', 'middleright', 'bottomleft', 
              'bottomright'] };

   $prb= "";
   $url=$jivetab{$login}{'url'};
   $url= adjusturl($url);
   $prb= strapp $prb, "url=$url";
   $logo= adjusturl "$jivetab{$login}{'logo'}";
   $prb= strapp $prb, "logo=$logo";
   $title= adjusturl "$jivetab{$login}{'title'}";
   $prb = strapp $prb, "title=$title";
   $prb= strapp $prb, "login=$login";                  
   $prb = strapp $prb, "rh=$rh";
   $prb = strapp $prb, "label=$title";

      if ($os ne "nt") {
         #$formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $formenc = adjusturl "ENCTYPE=\"multipart/form-data\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execjiveitupload =  encurl "execjiveitupload.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execjiveitupload =  "execjiveitupload.cgi";
      }

      $alphaindex = substr $login, 0, 1;
      $alphaindex = $alphaindex . '-index';

      $prb = strapp $prb, "template=$ENV{HDTMPL}/jiveitupload.html";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/jiveitupload-$$.html";

      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $prb = strapp $prb, "password=$password";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execjiveitupload\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=login>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=uploadname>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=uploadfile>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=password>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=login VALUE=$login>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=password VALUE=$password>";

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
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
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "jp=$jp";


   $prb = strapp $prb, "status=$status";
   parseIt $prb;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$alphaindex/$login/jiveitupload-$$.html";

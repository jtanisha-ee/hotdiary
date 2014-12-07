#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: mydiary.cgi
# Purpose: it checks for the cookie
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $hddomain = "\L$ENV{HDDOMAIN}";

   ## no jp exists
   # $jp = $input{jp};
   $jp = "";

   $hdcookie = $ENV{HTTP_COOKIE};
   hddebug "hdcookie = $hdcookie";

   $hdvisitor = gethdvisitor($hdcookie);
   hddebug "hdvisitor = $hdvisitor";
   if ($hdvisitor eq "") {
      status("<a href=\"/\">We will attempt to set an appropriate cookie in your browser, please make sure cookies are enabled in your browser.</a><p>If you still see this message, again after clicking the above link, please <a href=\"/contact_us.shtml\">click here</a> to contact HotDiary.");
      exit;
   }

   $hdlogin = getlogin($hdcookie);
   hddebug "cookie login = $hdlogin";

   if ($hdlogin eq "") { 
      # redirect user to signin page as the user is not signed in
      $prmm = "";
      $prmm = strapp $prmm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prmm = strapp $prmm, "templateout=$ENV{HDHOME}/tmp/mydiary-redirect_url-$$.html";
      if ($hddomain =~ /hotdiary/) {
         $prmm = strapp $prmm, "redirecturl=/signin.shtml";
      } else {
	 ## jp is not there.
         #$prmm = strapp $prmm, "redirecturl=http://$hddomain/index.cgi?jp=$jp";
         $prmm = strapp $prmm, "redirecturl=/signin.shtml";
      }

      parseIt $prmm;
      hdsystemcat "$ENV{HDHOME}/tmp/mydiary-redirect_url-$$.html";
      exit;
   }

   $remoteaddr = $ENV{'REMOTE_ADDR'};


   $alpha = substr $hdlogin, 0, 1;
   $alpha = $alpha . '-index';

   $biscuit = getbiscuit($hdcookie);

   $execshowtopcal = encurl "execshowtopcal.cgi";
   $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execshowtopcal&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   hddebug "cgi = $cgi";

   $prmm = "";
   $prmm = strapp $prmm, "template=$ENV{HDTMPL}/redirect_url.html";
   $prmm = strapp $prmm, "templateout=$ENV{HDHOME}/tmp/mydiary-redirect_url-$$.html";
   $prmm = strapp $prmm, "redirecturl=$cgi";
   parseIt $prmm;
   hdsystemcat "$ENV{HDHOME}/tmp/mydiary-redirect_url-$$.html";

   exit;
}


  

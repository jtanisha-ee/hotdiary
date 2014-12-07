#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: login.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 10-09-97
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
#use UNIVERSAL qw(isa);
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = 3600;


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Login"); 

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


   $hs = $input{'hs'};
   $vdomain = $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "hotdiary.com";
   }
   $jp = $input{'jp'};
   hddebug "jp = $jp";
   hddebug "vdomain = $vdomain";


   ## we should use 1800calendar.com for cookie reasons and not use www.1800calendar.com and www.hotdiary.com.
   if ( $jp ne "" ) {
      $vdomain = "1800calendar.com";
      $icgi = adjusturl "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index3.html";
   }
                
   $biscuit = $input{'biscuit'};
   hddebug "BISCUIT ........................................ = $biscuit";

   if ($biscuit eq "") {
      status("It is likely that you are viewing a published calendar website.");
      exit;
   }

   if (!exists $sesstab{$biscuit}) {
      hddebug " $biscuit does not exist, icgi = $icgi";

      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
	       $myurl = adjusturl "http://$vdomain/$icgi";
               #status("You are already logged out. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login. ");
               #exit;
            }
         }
	 $myurl = adjusturl "http://$vdomain/$icgi";
         #status("You are already logged out. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login. ");
      } else {
	 $myurl = adjusturl "http://$vdomain/$hs/$icgi";
         #status("You are already logged out. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login. ");
      }
      $prml = "";
      $prml = strapp $prml, "redirecturl=$myurl";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url_logout.html";
      $prml = strapp $prml, "templateout=$ENV{HDREP}/pl-$$.html";
      parseIt $prml;
      hdsystemcat "$ENV{HDREP}/pl-$$.html";
      exit;
   }

   $login = $sesstab{$biscuit}{'login'};
   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';
   

   #delete $sesstab{$biscuit};
   #delete $logsess{$login};
   #system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html $ENV{HDREP}/$alpha/$login/index.html1";
   #system "/bin/rm -f $ENV{HDREP}/$alpha/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html.out";
   #system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html1 $ENV{HDREP}/$alpha/$login/index.html";
   #$biscuit = "";

   # this was commented out previously
   ##system "/bin/cat $ENV{HDTMPL}/content.html";

   if ($hs eq "") {
      if ($jp ne "") {
         if ($jp ne "buddie") {
           #status("$login: You have been logged out. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login."); 
	   #exit;
	 }
      }
      #status("$login: You have been logged out. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login."); 
   } else {
      #status("$login: You have been logged out. Click <a href=\"http://$vdomain/$hs/$icgi\"> here</a> to login."); 
   }



   $prml = "";

   if ($jp ne "" ) {
      $pcgi = adjusturl "/index.cgi?jp=$jp";
      $prml = strapp $prml, "redirecturl=$pcgi";
   } else {
      # for non jp such as hotdiary
      $pcgi = adjusturl "index3.html";
      $prml = strapp $prml, "redirecturl=$pcgi";
   }

   hddebug "CAME HERE .............. biscuit = $biscuit, login = $login, vdomain = $vdomain";

   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "biscuit=$biscuit";
   if ($vdomain =~ /www/) {
      $vdomain =~ s/www\.//g;
   }
   $myvdomain = '.' . $vdomain;
   hddebug "vdomain = $myvdomain";
   $prml = strapp $prml, "vdomain=$myvdomain";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url_logout.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha/$login/pl-$biscuit-$$.html";
   $prml = strapp $prml, "login=$login";
   parseIt $prml;
   
   hdsystemcat "$ENV{HDREP}/$alpha/$login/pl-$biscuit-$$.html";

   delete $sesstab{$biscuit};
   delete $logsess{$login};
   #system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html $ENV{HDREP}/$alpha/$login/index.html1";
   #system "/bin/rm -f $ENV{HDREP}/$alpha/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html.out";
   #system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html1 $ENV{HDREP}/$alpha/$login/index.html";
   $biscuit = "";
}


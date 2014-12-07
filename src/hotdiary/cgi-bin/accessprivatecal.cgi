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
# FileName: accesssprivatecal.cgi
# Purpose: Creates a private group calendar
# Creation Date: 07-16-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
# This line of ParseTem had to be defined first. For some reason
# status was not working when this line was not first.Very strange!
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
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};



   #print &PrintHeader;
   #print &HtmlTop ("accessprivatecal.cgi example");

   hddebug "enter accessprivatecal.cgi";

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg',
                  'listed'] };


   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   tie %parttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/parttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['logo', 'title', 'banner'] };

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
  
   $rh = $input{'rh'};
   $banner = "";
   $logo = "";
   $label = "HotDiary";
   $jp = $input{jp};
   $os = $input{os};
   $vdomain = $input{vdomain};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   }
   
   if ($rh ne "") {
      if (exists $jivetab{$jp}) {
         $logo = adjusturl $jivetab{$jp}{logo};
         $title = adjusturl $jivetab{$jp}{title};
         $banner = adjusturl $jivetab{$jp}{banner}; 
         #$label = $title;
         $label = "Group Calendar";
      } else {
          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
	        $label = $title;
             }
          }
      }
   }



   $password = trim $input{'password'};
   $password = "\L$password";
   $g = trim $input{'g'};
  

   if ("\L$lgrouptab{$g}{'password'}" eq "$password") {
      # this is redirect url, will be invoked when Add button is pressed
      #hddebug "password = $password";
      $pw = encurl $password;
      #hddebug "pw = $pw";
      if ($rh eq "") {
          $cgis = adjusturl "/cgi-bin/execcalclient.cgi?sc=p&l=&g=$g&os=$os&pw=$pw";
          #$cgis = "/cgi-bin/execcalclient.cgi?sc=p&l=&g=$g&os=$os&pw=$pw";
      } else {
          #hddebug "came here for jiveit";
          $cgis = adjusturl "/cgi-bin/$rh/execcalclient.cgi?sc=p&l=&g=$g&os=$os&pw=$pw";
          #$cgis = "/cgi-bin/$rh/execcalclient.cgi?sc=p&l=&g=$g&os=$os&pw=$pw";
      }
      $prm = "";
      $prm = strapp $prm, "rh=$rh";
      $prm = strapp $prm, "label=$label";
      $prm = strapp $prm, "banner=$banner";
      if ($logo ne "") {
         $logo = adjusturl $logo;
      }
      $prm = strapp $prm, "logo=$logo";
      $prm = strapp $prm, "redirecturl=$cgis";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
      parseIt $prm;
      hdsystemcat "$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
#hddebug "Location: http://$vdomain/$cgis";
      #print "Location: http://$vdomain/$cgis\n\n";
   } else {
        status("Invalid password ($password). Please enter the correct password for this calendar. You may also want to verify the password with the Calendar Master for \"$g\". If you are already the calendar master, you can click on Manage, and reset the password for this calendar.");
        exit;
   }

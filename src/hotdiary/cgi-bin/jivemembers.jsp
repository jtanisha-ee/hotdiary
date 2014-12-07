#!/usr/bin/perl

#
# (C) Copyright 2001 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: jivemembers.jsp
# Purpose: JiveIt! Members List
# Creation Date: 07-04-2001
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

   hddebug ("jivemembers.jsp");

   $jp = $input{jp}; 
   hddebug "jp = $jp";

   $password = $input{password}; 
   hddebug "password = $password";

   $report = $input{report}; 
   hddebug "report = $report";

   qx{mkdir -p $ENV{HDDATA}/jivetab/$jp};

   # bind jivememberstab table vars
   tie %jivememberstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab/$jp",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };

   if (!exists $jivetab{$jp}) {
      status "JiveIt! administrator $jp does not exist!";
      exit;
   }

   if ("\L$logtab{$jp}{password}" ne "\L$password") {
      status "JiveIt! administrator password is incorrect!";
      exit;
   }
  

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/jivemembers.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/jivemembers-$$.html";
   $members = "<BR><CENTER><TABLE BORDER=0 BGCOLOR=black CELLPADDING=2 CELLSPACING=1 WIDTH=\"100%\">";
   $members .= "<TR WIDTH=\"100%\" VALIGN=MIDDLE HEIGHT=\"100%\"><TD VALIGN=MIDDLE ALIGN=CENTER>";
   $members .= "<FONT FACE=Verdana SIZE=4 COLOR=white>Members Added So Far</FONT>";
   $members .= "<br><FONT FACE=Verdana SIZE=1 COLOR=white><b>Members In Red Do Not Wish To Be Contacted!</b></FONT>";
   $members .= "</TD></TR></TABLE></CENTER><BR>";
   $members .= "<TABLE BORDER=0 BGCOLOR=black CELLPADDING=0 CELLSPACING=1 WIDTH=\"100%\">";
   $members .= "<TR WIDTH=\"100%\"><TD>";
   $members .= "<TABLE BORDER=0 BGCOLOR=white CELLPADDING=2 CELLSPACING=2 WIDTH=\"100%\">";
   $members .= "<TR>";
   $color = "BGCOLOR=blue";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Member ID</FONT></TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Hear About Us</FONT>&nbsp;</TD>";
   if ($report eq "detail") {
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Calendar</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Notes</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Address Book</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Memo</FONT>&nbsp;</TD>";
   }
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>First Name</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Last Name</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Email</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Home Phone</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Fax</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>URL</FONT>&nbsp;</TD>";
   if ($report eq "detail") {
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Street</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>City</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>State</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Zipcode</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Country</FONT>&nbsp;</TD>";
   }
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Pager</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Cell Phone</FONT>&nbsp;</TD>";
   $members .= "<TD $color><FONT FACE=Verdana SIZE=2>Business Phone</FONT>&nbsp;</TD>";
   $members .= "</TR>";
   foreach $i (sort keys %jivememberstab) {
      $members .= "<TR>";
      $color = "";
      if ($logtab{$i}{informme} ne "CHECKED") {
         $color = "BGCOLOR=red";
      } 
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$jivememberstab{$i}{login}</FONT></TD>";
      if (exists $surveytab{$i}) {
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$surveytab{$i}{hearaboutus}</FONT>&nbsp;</TD>";
      } else {
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2></FONT>&nbsp;</TD>";
      }
      if ($report eq "detail") {
         $alpha = (substr $i, 0, 1) . '-index';
         if (-d "$ENV{HDDATA}/$alpha/$i/appttab") {
            $calendar = qx{ls -1 $ENV{HDDATA}/$alpha/$i/appttab | wc -l};
            $calendar =~ s/\n//g;
            $calendar =~ s/\r//g;
         } else {
            $calendar = 0;
         }
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$calendar</FONT>&nbsp;</TD>";
         if (-d "$ENV{HDDATA}/$alpha/$i/notestab") {
            $notes = qx{ls -1 $ENV{HDDATA}/$alpha/$i/notestab | wc -l};
            $notes =~ s/\n//g;
            $notes =~ s/\r//g;
         } else {
            $notes = 0;
         }
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$notes</FONT>&nbsp;</TD>";
         if (-d "$ENV{HDDATA}/$alpha/$i/addrtab") {
            $addr = qx{ls -1 $ENV{HDDATA}/$alpha/$i/addrtab | wc -l};
            $addr =~ s/\n//g;
            $addr =~ s/\r//g;
         } else {
            $addr = 0;
         }
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$addr</FONT>&nbsp;</TD>";
         if (-d "$ENV{HDDATA}/$alpha/$i/todotab") {
            $memo = qx{ls -1 $ENV{HDDATA}/$alpha/$i/todotab | wc -l};
            $memo =~ s/\n//g;
            $memo =~ s/\r//g;
         } else {
            $memo = 0;
         }
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$memo</FONT>&nbsp;</TD>";
      }
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{fname}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{lname}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{email}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{phone}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{fax}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{url}</FONT>&nbsp;</TD>";
      if ($report eq "detail") {
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{street}</FONT>&nbsp;</TD>";
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{city}</FONT>&nbsp;</TD>";
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{state}</FONT>&nbsp;</TD>";
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{zipcode}</FONT>&nbsp;</TD>";
         $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{country}</FONT>&nbsp;</TD>";
      }
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{pager}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{cphone}</FONT>&nbsp;</TD>";
      $members .= "<TD $color><FONT FACE=Verdana SIZE=2>$logtab{$i}{bphone}</FONT>&nbsp;</TD>";
      $members .= "</TR>";
   }
   $members .= "</TABLE>";
   $members .= "</TD></TR></TABLE>";
   $members = adjusturl $members;
   $prml = strapp $prml, "members=$members";
   parseIt $prml;

   hdsystemcat "$ENV{HDREP}/common/jivemembers-$$.html";
   

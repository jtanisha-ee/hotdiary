#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: memocalupdate.cgi
# Purpose: it updates the memo or reminders.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{
   $MAXLEN = 500000;

   # Read in all the variables set by the form
   &ReadParse(*input);

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'update.x'} ne "") {
      $action = "Update";
   } 

   if ($input{'calendar'} ne "") {
      $action = "Calendar";
   } 

   if ($input{'pcalendar'} ne "") {
      $action = "PCalendar";
   }
   hddebug "action = $action";


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

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.\n");
              exit;
           }
        }
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired.\n");
    exit;
  }

  $sesstab{$biscuit}{'time'} = time();


  #if ($login ne "mjoshi") {
  #   status("This service is coming soon!");
  #   exit;
  #}
 
  $memolist = adjusturl $input{memolist};
  if (notDesc($memolist)) {
     status("$login: Invalid characters in memo list ($memolist). Click <a href=\"validation.html\"> here</a> to learn validation rules.");
     exit;
  }

  if (length($memolist) > $MAXLEN) {
     status("$login: Limit the length of memo to $MAXLEN.");
     exit;
  }


# bind memo table vars
   tie %memotab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/memotab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'memolist'] };


   if ($action eq "Update")
   { 
      #print "update action called";
      $memotab{'login'}{'login'} = $login;
      $memotab{$login}{'memolist'} = $memolist; 
      status("$login: MemoCal updated.");
      if ((trim $memotab{$login}{'memolist'}) eq "") {
         withdrawmoney $login;
      } else {
         depositmoney $login;
      }
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ($action eq "PCalendar") {
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/red-$biscuit-$$.html";
      $pgroups = $input{'ppgroups'};
      $pcgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$pgroups";
      $prml = strapp $prml, "redirecturl=$pcgi";
      parseIt $prml;
      hdsystemcat "$ENV{HDREP}/$alphaindex/$login/red-$biscuit-$$.html";

     ## this is for print
     #$pcgi = "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$pgroups";
     #print "Location: $pcgi\n\n";
      exit;
   }

   if ($action eq "Calendar") {
      

      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/stdpghdr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdpghdr.html";
      $prml = strapp $prml, "expiry=";
      $prml = strapp $prml, "label=Group Blog Calendar";
      $logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      $prml = strapp $prml, "login=$logi";
      $prml = strapp $prml, "label1=$label1";
      $prml = strapp $prml, "label2=$label2";
      $prml = strapp $prml, "biscuit=$biscuit";
      parseIt $prml, 1;

      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/groupcal.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/groupcal.html";
      $pgroups = $input{'pgroups'};
      $urlcgi = adjusturl("cgi-bin/execcalendar.cgi?biscuit=$biscuit&pgroups=$pgroups");
      $prml = strapp $prml, "calendarprog=$urlcgi";
      parseIt $prml, 1;

      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdpghdr.html $ENV{HDHREP}/$alphaindex/$login/groupcal.html > $ENV{HDREP}/$alphaindex/$login/$biscuit.html";
      #system "/bin/cat $ENV{HDTMPL}/content.html";
      #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$biscuit.html"; 
      hdsystemcat "$ENV{HDREP}/$alphaindex/$login/$biscuit.html"; 
   }


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   
# save the info in db
   tied(%memotab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

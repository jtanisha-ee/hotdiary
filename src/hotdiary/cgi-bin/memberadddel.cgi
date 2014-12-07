#!/usr/local/bin/perl5

#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,           
# in whole or in part.

#
# FileName: memberadddel.cgi
# Purpose: it allows members to add or delete other members to their personal groups
# upon whether they are subscribed, unsubscribed or founders.
# Creation Date: 03-09-99 
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


# parse the command line
   &ReadParse(*input); 

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $biscuit = trim $input{'biscuit'};
   #print "biscuit =", $biscuit;

   $numentries = trim $input{'numentries'};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   if ($input{'add.x'} ne "") {
      $action = "Add";
   }
   if ($input{'delete.x'} ne "") {
      $action = "Delete";
   }

   $groupname = trim $input{'groupname'};
   $member = trim $input{'login'};
##### BEGIN CASE
   $member = "\L$member";
##### END CASE

   if (notLogin $member) {
      ($user, $domain) = split "\@", $member;
      if ( ((trim $user) eq "") || ((trim $domain) eq "") ) {
         status("$login: Invalid characters in Member Login Name(s). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
         exit;
      }
   }

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Update Address"); 

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['biscuit', 'login', 'time'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

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
             error("Login  is an empty string.\n");
             exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
     delete $sesstab{$biscuit};
     delete $logsess{$login};
     status("$login: Your session has already expired.\n");
     exit;
  }

   # check for intruder access. deny the permission and exit error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}
#
   $sesstab{$biscuit}{'time'} = time(); 


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

# bind gmember table vars
   tie %gmembertab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/personal/$groupname/gmembertab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };

   if ($action eq "Add") {
      if ($member eq "") {
         status("$login: Member name has not been specified.");
         exit;
      }

      if ($member eq $login) {
         status("$login: $groupname is your personal group and you automatically become a member of this group when you create it using the Add feature.");
         exit;
      }

      if (!exists $logtab{$member}) {
         ($user, $domain) = split "\@", $member;
         if ( ((trim $user) eq "") || ((trim $domain) eq "") ) {
            status("$login: $member is not a member login, or a valid email address.");
            exit;
         }
      }
      if (exists $logtab{$member}) {
         if ($logtab{$member}{'checkid'} ne "CHECKED") {
            status("$login: $member has denied access to you, to add his/her entry to your personal group.");
            exit;
         }
      }
      if (exists $gmembertab{$member}) {
         status("$login: $member is already a member of $groupname");
         exit;
      }
      $gmembertab{$member}{'login'} = $member;
      depositmoney $login;
      tied(%gmembertab)->sync();
      status("$login: Member $member has been successfully added to $groupname");
      exit();
   }

   $checknum = 0;
   $did_something = 0; 
   $msg = "<DL>";
   for ($l = 0; $l <= $numentries; $l = $l + 1) {

        $groupmemberfield = "groupmember$l";
        $groupmember = $input{$groupmemberfield};
       
        # check if checkbox is on.
        $checkbox_e = "checkbox$l";
        $checkbox = trim $input{$checkbox_e}; 

        if ($checkbox eq "on") {
           $checknum = $checknum + 1;
 
           if ($action eq "Delete") {
              withdrawmoney $login;
              delete $gmembertab{$groupmember};
              $did_something = $did_something + 1;
              $msg = $msg . "<LI>You have successfully deleted $groupmember from $groupname.</LI>";
           }
        }
   }
   if ($checknum == 0) {
      $msg = $msg . "No checkboxes were selected. Please select atleast one checkbox to perform an action.";
   } else {
      if ($did_something == 0) {
        $msg = $msg . "<LI>No actions were performed.</LI>";
        if ($checknum != 0) {
           $msg = $msg . "</DL>";
        }
      }
   }
   status("$login: $msg");

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

#synch the database
   if (($action eq "Add") || ($action eq "Delete")) {
      tied(%gmembertab)->sync();
   }
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

#!/usr/local/bin/perl5

#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,           
# in whole or in part.

#
# FileName: groupjoinleavedel.cgi
# Purpose: it allows members to join, leave, or delete the group, depending
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

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = trim $input{'biscuit'};
   #print "biscuit =", $biscuit;

   $numentries = trim $input{'numentries'};

   if ($input{'join.x'} ne "") {
      $action = "Join";
   }
   if ($input{'delete.x'} ne "") {
      $action = "Delete";
   }
   if ($input{'leave.x'} ne "") {
      $action = "Leave";
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

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index'; 

   $sesstab{$biscuit}{'time'} = time(); 


   system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";
   system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
   system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";

# bind listed group table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ,
                   'listed'] };

# bind unlisted group table vars
   tie %ugrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/unlisted/ugrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' ] };

# bind personal group table vars
   tie %pgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that
# the groupname is unique amoung all Listed as well as personal groups
   tie %plgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'calpublish', 'corg' ] };

# bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'calpublish', 'corg' ] };



# we get entryno and num etries to be deleted from the form.
# calculate the numcheckbox from the checkbox tickmarks.


   #initailize the counters
   $num = 1;

#form the array of entry numbers that are to be updated/deleted.
   for ($i = 0; $i < $numentries; $i = $i + 1) {
        $entry_array[$i] = "entryn$num";
        $num = $num + 1;

   }
  
   $checknum = 0;
   $did_something = 0; 
   $msg = "<DL>";
   for ($l = 1; $l <= $numentries; $l = $l + 1) {

        #$one_entryno = $entry_array[$l];
        #$entryno = trim $input{$one_entryno};
        $entryno = "entryn$l";

        $grouptype = $input{"grouptype$l"};
        $groupname = trim $input{"$entryno"};
        if ($groupname eq "") {
           next;
        }
       
        # check if checkbox is on.
        $checkbox_e = "checkbox$l";
        $checkbox = trim $input{$checkbox_e}; 

        if ($checkbox eq "on") {
           $checknum = $checknum + 1;
 
           if ($action eq "Join") {
              if (exists $fgrouptab{$groupname}) {
                 $msg = $msg . "<LI>$login: You cannot join $groupname because you are already a founder of this group.</LI>";
                 next;
              }
              if (exists $sgrouptab{$groupname}) {
                 $msg = $msg . "<LI>You have already joined $groupname.</LI>";
                 next;
              }
              if (exists $pgrouptab{$groupname}) {
                 $msg = $msg . "<LI>$groupname is your personal group that no other member has access to, and you do not need to join it explicitly.</LI>";
                 next;
              }
              if (exists $lgrouptab{$groupname}) {
                 $sgrouptab{$groupname}{'groupname'} = $groupname;
                 #$sgrouptab{$groupname}{'grouptype'} = $grouptype;
                 $sgrouptab{$groupname}{'grouptitle'} = $lgrouptab{$groupname}{'grouptitle'};
                 $sgrouptab{$groupname}{'groupdesc'} = $lgrouptab{$groupname}{'groupdesc'};
              }
              tie %usertab, 'AsciiDB::TagFile',
                   DIRECTORY => "$ENV{HDDATA}/listed/groups/$groupname/usertab",
                   SUFIX => '.rec',
                   SCHEMA => {
                   ORDER => ['login'] };
              $usertab{$login}{'login'} = $login;
              $did_something = $did_something + 1;
    	      $msg = $msg . "<LI>You have successfully joined $groupname.</LI>";
    	      $msg = $msg . "<LI>Did you know that you can use Collabrum to send instant messages to $groupname? All you have to do is click on Collabrum button in left frame, and enter the details of your message in right frame. Make sure you select $groupname in the distribution field. Also select the checkbox marked Send Instantly. This way you do not need to enter the time and duration. You could also send instant messages to multiple groups that you have subcribed to or founded yourself!.</LI>";
           }

           if ($action eq "Delete") {

              if (($grouptype ne "Founded") && ($grouptype ne "Personal")) {
                 $msg = $msg . "<LI>$groupname was not deleted either because you were not a founder of this group, or because it was not your personal group.</LI>";
                 next;
              }
              if ($grouptype eq "Founded") {
                 if (!exists $fgrouptab{$groupname}) {
                    $msg = $msg . "<LI>You cannot delete $groupname, since you are not it's founder.</LI>";
                    exit;
                 }
                 tie %usertab, 'AsciiDB::TagFile',
                   DIRECTORY => "$ENV{HDDATA}/listed/groups/$groupname/usertab",
                   SUFIX => '.rec',
                   SCHEMA => {
                   ORDER => ['login'] };
                 foreach $username (keys %usertab) {
# bind subscribed group table vars
                    tie %dsgrouptab, 'AsciiDB::TagFile',
                      DIRECTORY => "$ENV{HDDATA}/groups/$username/subscribed/sgrouptab",
                      SUFIX => '.rec',
                      SCHEMA => {
                      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish' ] };
                    delete $dsgrouptab{$groupname};
                    tied(%dsgrouptab)->sync();
                 }
                 delete $fgrouptab{$groupname};
                 withdrawmoney $login;
                 tied(%fgrouptab)->sync();
                 if ($groupname ne "") {
                    if (-d "$ENV{HTTPHOME}/html/hd/groups/$groupname") {
                       system "rm -f $ENV{HTTPHOME}/html/hd/groups/$groupname/index.cgi";
                       system "rm -f $ENV{HTTPHOME}/html/hd/groups/$groupname/webpage.cgi";
                       system "rmdir $ENV{HTTPHOME}/html/hd/groups/$groupname";
                    }
                 }
                 delete $lgrouptab{$groupname};
# safety check!! just in case any other directory is deleted
                 if (-d "$ENV{HDDATA}/listed/groups/$groupname") {
                    $groupname = trim $groupname;
                    if (($groupname ne "") && ($ENV{HDDATA} ne "")) {
                       system "/bin/rm -rf $ENV{HDDATA}/listed/groups/$groupname";
                    }
                 }
              }
              if ($grouptype eq "Personal") {
                 delete $plgrouptab{$groupname};
                 delete $pgrouptab{$groupname};
                 if (-d "$ENV{HDDATA}/groups/$alpha/$login/personal/$groupname") {
                    $groupname = trim $groupname;
                    $login = trim $login;
                    if (($groupname ne "") && ($login ne "") && ($ENV{HDDATA} ne "")) {
                       system "/bin/rm -rf $ENV{HDDATA}/groups/$alpha/$login/personal/$groupname";
                    }
                 }
              }
              $did_something = $did_something + 1;
              $msg = $msg . "<LI>You have successfully removed $groupname. The website associated with this group has been removed. </LI>";
           }

           if ($action eq "Leave") {
              if (exists $fgrouptab{$groupname}) {
                 $msg = $msg . "<LI>You cannot leave $groupname because you are the founder of this group.</LI>";
                 next;
              }
              tie %usertab, 'AsciiDB::TagFile',
                   DIRECTORY => "$ENV{HDDATA}/listed/groups/$groupname/usertab",
                   SUFIX => '.rec',
                   SCHEMA => {
                   ORDER => ['login'] };
              delete $usertab{$login};
              tied(%usertab)->sync();
              delete $sgrouptab{$groupname};
              $did_something = $did_something + 1;
              $msg = $msg . "<LI>You have successfully unsubscribed from $groupname.</LI>";
           }
        }
   }
   if ($checknum == 0) {
      $msg = "No checkboxes were selected. Please select atleast one checkbox to perform an action.";
   }
   if ($did_something == 0) {
      $msg = $msg . "<LI>No actions were performed.</LI>";
   }
   if ($checknum != 0) {
      $msg = $msg . "</DL>";
   }
   status("$login: $msg");

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

#synch the database
   if ($action eq "Join") {
      tied(%sgrouptab)->sync();
   }
   if ($action eq "Delete") {
      tied(%lgrouptab)->sync();
   }
   if ($action eq "Leave") {
      tied(%sgrouptab)->sync();
   }
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

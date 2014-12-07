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
# FileName: groupmanagedel.cgi
# Purpose: it manage and delete personal groups.                  
# Creation Date: 03-09-99 
# Created by: Smitha Gudur & Manoj Joshi
# 


#!/usr/local/bin/perl5

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   #print &PrintHeader;
   #print &HtmlTop ("groupmanagedel.cgi example");    

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'manage.x'} ne "") {
      $action = "Manage"; 
   } else {
     if ($input{'delete.x'} ne "") { 
      $action = "Delete";
     }
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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

   # check if session record exists. 
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      #return;
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

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       ##return;
       #exit;
   #}
        
  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired.\n");
    #return;
    exit;
   }

   depositmoney $login;

  $alpha = substr $login, 0, 1;
  $alpha = $alpha . '-index';

  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";

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

   $entryno = getkeys();

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

   $msg = "<DL>"; 


#   if (notLogin($input{'groupname'})) {
#      status("$login: Invalid characters in Group Name(s). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
#      exit;
#   }
#   $groupname = trim $input{'groupname'};

   if (notDesc($input{'grouptitle'})) {
      status("$login: Invalid characters in Group Title.  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   if (notDesc($input{'groupdesc'})) {
      status("$login: Invalid characters in Group Description.  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   $groupfounder = $login;
   $groupdesc = trim $input{'groupdesc'};
   $grouptitle = trim $input{'grouptitle'};
   $groupname= $input{'radio1'};

   
   if ($groupname eq "") {
      status("$login: Please select a personal group.");
      exit;
   }

#  add a new group, 
   if ($action eq "Manage") { 
         $title = time();
         $prml = "";
         $prml = strapp $prml, "biscuit=$biscuit";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html"; 
	 $prml = strapp $prml, "pagenumber=";
         $prml = strapp $prml, "expiry=";
         $prml = strapp $prml, "pagefield=";

         $urlcgi = buildurl("execmemberadddel.cgi");
         $prml = strapp $prml, "actioncgi=$urlcgi";
         $prml = strapp $prml, "label=Members of Personal Group <i>$groupname</i>";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html > $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
       
         $prml = "";
         $prml = strapp $prml, "groupname=$groupname"; 
         $prml = strapp $prml, "template=$ENV{HDTMPL}/addmember.html"; 
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/addmember.html";
         $prml = strapp $prml, "login=";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/addmember.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";

         $prml = "";
         # Generate Standard Table Header
         $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html"; 
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblhdr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";

         # bind personal group table vars
         tie %gmembertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/$groupname/gmembertab",
           SUFIX => '.rec', 
           SCHEMA => { 
           ORDER => ['login'] };
         (@records) = sort keys %gmembertab;

         if ($#records >= 0) {
            for ($l = 0; $l <= $#records; $l++) {
                if (exists $logtab{$records[$l]}) {
                   if ($logtab{$records[$l]}{'checkid'} ne "CHECKED") {
                      delete $gmembertab{$records[$l]};
                      next;
                   }
                }
                $prml = "";
                $prml = strapp $prml, "template=$ENV{HDTMPL}/managegrouptblentry.html"; 
                $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/managegrouptblentry.html";
                $prml = strapp $prml, "checkboxfield=checkbox$l"; 
                $prml = strapp $prml, "groupmemberfield=groupmember$l";
                $records[$l] = adjusturl $records[$l];
                $prml = strapp $prml, "groupmember=$records[$l]";
                $prml = strapp $prml, "login=$records[$l]";
                parseIt $prml, 1;
                system "/bin/cat $ENV{HDHREP}/$alpha/$login/managegrouptblentry.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
            }
         }
         
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/amembertblftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/amembertblftr.html";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/amembertblftr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
 
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/amembersearchpgftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/amembersearchpgftr.html";
         $prml = strapp $prml, "numentries=$#records";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/amembersearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
         
         #system "/bin/cat $ENV{HDTMPL}/content.html\n\n"; 
         #system "/bin/cat $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html"; 
         hdsystemcat "$ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html"; 
         exit;
      #}
   }


   if ($action eq "Delete") {
      delete $plgrouptab{$groupname};
      delete $pgrouptab{$groupname};
      if (-d "$ENV{HDDATA}/groups/$alpha/$login/personal/$groupname") {
         $groupname = trim $groupname;
         $login = trim $login;
         if (($groupname ne "") && ($login ne "") && ($ENV{HDDATA} ne "")) {
            system "/bin/rm -rf $ENV{HDDATA}/groups/$alpha/$login/personal/$groupname";
         }
      }
      $msg = $msg. "<LI>You have successfully deleted $groupname.</LI>";
   }

   status("$login: $msg");

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   if ($action eq "Manage") {
       tied(%pgrouptab)->sync();
       tied(%plgrouptab)->sync();
   }

   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

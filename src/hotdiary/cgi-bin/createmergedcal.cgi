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
# FileName: createmergedcal.cgi
# Purpose: Creates a merged group calendar
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

   hddebug "createmergedcal.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   $jp = $input{jp};  
   $os = $input{os};  

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }
                         
   if ($biscuit eq "") {
      if ($hs eq "") {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner',
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };


   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
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

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   $rh = $input{'rh'};
   tie %hdtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/hdtab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['title', 'logo' ] };

   if (exists $hdtab{$login}) {
      $label = adjusturl $hdtab{$login}{title};
   } else {
      $label = "HotDiary";
   }

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

   $HDLIC = $input{HDLIC};

   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $p2 = $label;
   if ($logo ne "") {
     $logo = adjusturl $logo;
   }       

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make
#  sure that
# the groupname is unique amoung all Listed as well as personal groups
   tie %plmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                'groupdesc' ] };


# bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
            'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 
            'listed', 'groups', 'logins'] };

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   system "mkdir -p $ENV{HDDATA}/merged/$login/founded/fmergetab";
   system "chmod 755 $ENV{HDDATA}/merged/$login/founded/fmergetab";

# bind founded group table vars
   tie %fmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/merged/$login/founded/fmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


   $ctype = $input{'ctype'};
   $corg = trim $input{'corg'};
   $edit = $input{edit}; 

   if (notDesc $corg) {
      status("$login: Invalid characters in organization name ($corg). Click <a href=\"validation.html\"> for help.");
      exit;
   }
   $calname = trim $input{'calname'};
   $calname = "\L$calname";
   if ($calname eq "") {
      status("$login: Calendar name is empty. Please specify a calendar name.");
      exit;
   }
   if (notLogin $calname) {
      status("$login: Invalid characters in calendar name ($calname). Do you have a space in calendar name? Click <a href=\"validation.html\"> for help.");
      exit;
   }

   if ($edit eq "") { 
     if ((exists $lmergetab{$calname}) || (exists $plmergetab{$calname})) {
        status("$login: This calendar name ($calname) is already chosen. Please select another name.");
        exit;
     }
   }


   if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
   }
   ## checks required to make sure that the calendarname is not the same
   ## group calendar name 
   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };
   if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
   }

   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


   ## check in the group tabs also
   if ($edit eq "") { 
      if ((exists $lgrouptab{$calname}) || (exists $fgrouptab{$calname})) {
         status("$login: This calendar name ($calname) is already chosen. Please select another name.");
         exit;
      }
   }
   $caltitle = trim $input{'caltitle'};
   if ($caltitle eq "") {
      status("$login: Calendar title is empty. Please specify a calendar title.");
      exit;
   }

   if (notDesc $caltitle) {
      status("$login: Invalid characters in calendar title. Click <a href=\"validation.html\"> for help.");
      exit;
   }
   $calpassword = trim $input{'calpassword'};
   $calpassword = "\L$calpassword";

   #if (($calpassword ne "") && ((length $calpassword) < 6)) {
   #   status("$login: If you wish to password-protect your calendar, you must specify a password of minimum 6 letters. This is to ensure the security of your calendar. Password protection is only an option. If you do not specify a password, everyone will be able to subscribe to it as long as they know the name of your calendar. However, you can restrict all other than yourself from editing it, by using an option at the bottom of this page.");
   #   exit;
   #}
   if (notDesc $calpassword) {
      status("$login: Invalid characters in calendar password. Click <a href=\"validation.html\"> for help.");
      exit;
   }

   $calrpassword = trim $input{'calrpassword'};
   $calrpassword = "\L$calrpassword";
   if (notDesc $calrpassword) {
      status("$login: Invalid characters in calendar repeat password. Click <a href=\"validation.html\"> for help.");
      exit;
   }

   if ($calpassword ne $calrpassword) {
      status("$login: Calendar password field and the repeat password field do not match. Please use the Back button and enter identical passwords.");
      exit;
   }

   $cdesc =  adjusturl $input{'cdesc'};
   if (notDesc $cdesc eq "") {
      status("$login: Invalid characters in calendar description. Click <a href=\"validation.html\"> for help.");
      exit;
       
   }
   $listed = $input{'listed'};

   $loginlist =  adjusturl $input{loginlist};
   $grouplist =  adjusturl $input{grouplist};
   $userlogins =  adjusturl $input{userlogins};
   $loginlist .= " " . $userlogins;
   $caltitle = adjusturl $caltitle;
   $calname = adjusturl $calname;
   hddebug "grouplist = $grouplist";
   hddebug "loginlist = $loginlist";

   if (($loginlist eq "") && ($grouplist eq "")) {
      hdstatus("$login: Please select atleast one group or login to merge calendars");
      exit;
   }


   if ($edit ne "") {
      $k = 0;
      $numbegin = $input{numbegin};
      $numend = $input{numend};
      $m = 0;

      if ($grouplist ne "") {
         $grouplist .= " ";
      }
      for ($i = $numbegin; $i <= $numend; $i= $i + 1) {
         $ginc = $input{"box$k"};
         $checkboxval = $input{$ginc};
          #hddebug "checkboxval = $checkboxval";
         if ($checkboxval eq "on") {
            $grouplist .= "$ginc ";
         }
         $k = $k + 1;
      }
   }

   $lmergetab{$calname}{'groupname'} = $calname;
   $lmergetab{$calname}{'groupfounder'} = $login;
   $lmergetab{$calname}{'grouptitle'} = $caltitle;
   $lmergetab{$calname}{'grouptype'} = "Founded";
   $lmergetab{$calname}{'groupdesc'} = $cdesc;
   $lmergetab{$calname}{'password'} = $calpassword;
   $lmergetab{$calname}{'ctype'} = $ctype;
   $lmergetab{$calname}{'corg'} = $corg;
   $lmergetab{$calname}{'listed'} = $listed;
   $lmergetab{$calname}{'logins'} = $loginlist;
   $lmergetab{$calname}{'groups'} = $grouplist;

   ## first time creation
   if ($edit eq "") {
     $fmergetab{$calname}{'groupname'} = $calname;
     $fmergetab{$calname}{'groupfounder'} = $login;
     $fmergetab{$calname}{'grouptitle'} = $caltitle;
     $fmergetab{$calname}{'grouptype'} = "Founded";
     $fmergetab{$calname}{'groupdesc'} = $cdesc;
     $fmergetab{$calname}{'password'} = $calpassword;
     $fmergetab{$calname}{'ctype'} = $ctype;
     $fmergetab{$calname}{'corg'} = $corg;
     $fmergetab{$calname}{'logins'} = $logins;
     $fmergetab{$calname}{'groups'} = $groups;
     tied(%fmergetab)->sync();
  }

   system "/bin/mkdir -p $ENV{HDDATA}/listed/merged/$calname/usertab";
   system "/bin/chmod -R 775 $ENV{HDDATA}/listed/merged/$calname";
# Add the calendar events file for this group
   system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/listed/merged/$calname";
   system "/bin/chmod 775 $ENV{HDDATA}/listed/merged/$calname/calendar_events.txt";

   # bind founded group table vars
   tie %usertab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/listed/merged/$calname/usertab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login'] };
   $usertab{$login}{'login'} = $login;

   $cpublish = $input{'cpublish'};
   $lmergetab{$calname}{'cpublish'} = $cpublish;
   hddebug "publish = $cpublish";
   if ($cpublish eq "on") {
      $logtab{$login}{referer} = $jp;
      tied(%logtab)->sync();
     
      if (!(-d "$ENV{HTTPHOME}/html/hd/merged/$calname"))  {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/merged/$calname";
         $vdomain = $input{'vdomain'};
         if ($vdomain ne "www.hotdiary.com") {
            $vdomain = "www.hotdiary.com"; 
	 } 
         if ($vdomain eq "") {
            $vdomain = "www.hotdiary.com"; 
         }
         $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/$hs/merged/$calname\" target=_main>http://$vdomain/merged/$calname</a>.";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/merged/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/merged/index.cgi $ENV{HTTPHOME}/html/hd/merged/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/merged/$calname/mergedwebpage.cgi")) {
         system "ln -s $ENV{HDCGI}/merged/mergedwebpage.cgi $ENV{HTTPHOME}/html/hd/merged/$calname";
      }
   }
   $rh = $input{'rh'};

   if ($os ne "nt") {
      $execmgcalclient = encurl "execmgcalclient.cgi";
      $execsearchmergedcal =  encurl "execsearchmergedcal.cgi";
      $execmergedgroups =  encurl "execmergedgroups.cgi";
   } else {
      $execmgcalclient = "execmgcalclient.cgi";
      $execsearchmergedcal =  "execsearchmergedcal.cgi";
      $execmergedgroups =  "execmergedgroups.cgi";
   }

   $ecalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmgcalclient&p1=biscuit&p2=jp&p3=f&p4=g&pnum=5&biscuit=$biscuit&g=$calname&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here<a/> to view merged calendar";

   $scalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execsearchmergedcal&p1=biscuit&p2=jp&p3=f&p4=g&pnum=5&biscuit=$biscuit&f=sgc&g=$calname&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to search merged calendar.";

   $mcalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&p4=grouplist&pnum=5&biscuit=$biscuit&f=mc&grouplist=$calname&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage merged calendar.";

   if ($edit eq "") {
      status("$login: Congratulations! You have created a secure merged calendar called $calname. <p>You must remember the password ($calpassword) to access this calendar. $ecalmsg $scalmsg $mcalmsg $cmsg");
   } else {
      status("$login: Your changes to secure merged calendar ($calname) have been saved. <p>You must remember the password ($calpassword) to access this calendar. $ecalmsg $scalmsg $mcalmsg $cmsg");
   }


   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%lmergetab)->sync();
   tied(%usertab)->sync();

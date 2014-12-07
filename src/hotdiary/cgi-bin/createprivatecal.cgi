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
# FileName: createprivatecal.cgi
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

   #print &PrintHeader;
   #print &HtmlTop ("createprivatecal.cgi example");

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
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that
# the groupname is unique amoung all Listed as well as personal groups
   tie %plgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed', 'readonly'] };


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

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
   }

# bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


   $ctype = $input{'ctype'};
   $corg = trim $input{'corg'};
   #if ($corg eq "") {
   #   status("$login: You must specify the correct name of your organization in order to be able to successfully use this service.");
   #   exit;
   #}
   if (notDesc $corg) {
      status("$login: Invalid characters in organization name ($corg). Click <a href=\"validation.html\"> for help.");
      exit;
   }
   $calname = trim $input{'calname'};
   $calname = "\L$calname";
   if ($calname eq "") {
      status("$login: Calendar ID is empty. Please specify a calendar ID.");
      exit;
   }
   if (notLogin $calname) {
      status("$login: Invalid characters in group or calendar ID ($calname). Do you have a space in group or calendar ID? Click <a href=\"validation.html\"> for help.");
      exit;
   }
   if ((exists $lgrouptab{$calname}) || (exists $plgrouptab{$calname})) {
      status("$login: This group or calendar ID ($calname) is already chosen. Please select another ID.");
      exit;
   }
   $caltitle = trim $input{'caltitle'};
   if ($caltitle eq "") {
      status("$login: Calendar title is empty. Please specify a group or calendar title.");
      exit;
   }
   if (notDesc $caltitle) {
      status("$login: Invalid characters in group or calendar title. Click <a href=\"validation.html\"> for help.");
      exit;
   }
   $calpassword = trim $input{'calpassword'};
   $calpassword = "\L$calpassword";
   #if (($calpassword ne "") && ((length $calpassword) < 6)) {
   #   status("$login: If you wish to password-protect your group or calendar, you must specify a password of minimum 6 letters. This is to ensure the security of your group or calendar. Password protection is only an option. If you do not specify a password, everyone will be able to subscribe to it as long as they know the name of your group or calendar. However, you can restrict all other than yourself from editing it, by using an option at the bottom of this page.");
   #   exit;
   #}
   if (notDesc $calpassword) {
      status("$login: Invalid characters in group or calendar password. Click <a href=\"validation.html\"> for help.");
      exit;
   }

   $calrpassword = trim $input{'calrpassword'};
   $calrpassword = "\L$calrpassword";
   if (notDesc $calrpassword) {
      status("$login: Invalid characters in group or calendar repeat password. Click <a href=\"validation.html\"> for help.");
      exit;
   }

   if ($calpassword ne $calrpassword) {
      status("$login: Calendar password field and the repeat password field do not match. Please use the Back button and enter identical passwords.");
      exit;
   }

   $cdesc = $input{'cdesc'};
   if (notDesc $cdesc eq "") {
      status("$login: Invalid characters in group or calendar description. Click <a href=\"validation.html\"> for help.");
      exit;
       
   }
   $listed = $input{'listed'};
   $readonly = $input{'readonly'};

   $lgrouptab{$calname}{'groupname'} = $calname;
   $lgrouptab{$calname}{'groupfounder'} = $login;
   $lgrouptab{$calname}{'grouptitle'} = $caltitle;
   $lgrouptab{$calname}{'grouptype'} = "Founded";
   $lgrouptab{$calname}{'groupdesc'} = $cdesc;
   $lgrouptab{$calname}{'password'} = $calpassword;
   $lgrouptab{$calname}{'ctype'} = $ctype;
   $lgrouptab{$calname}{'corg'} = $corg;
   $lgrouptab{$calname}{'listed'} = $listed;
   $lgrouptab{$calname}{'readonly'} = $readonly;

   $fgrouptab{$calname}{'groupname'} = $calname;
   $fgrouptab{$calname}{'groupfounder'} = $login;
   $fgrouptab{$calname}{'grouptitle'} = $caltitle;
   $fgrouptab{$calname}{'grouptype'} = "Founded";
   $fgrouptab{$calname}{'groupdesc'} = $cdesc;
   $fgrouptab{$calname}{'password'} = $calpassword;
   $fgrouptab{$calname}{'ctype'} = $ctype;
   $fgrouptab{$calname}{'corg'} = $corg;

   system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$calname/usertab";
   system "/bin/chmod -R 775 $ENV{HDDATA}/listed/groups/$calname";
# Add the calendar events file for this group
   system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/listed/groups/$calname";
   system "/bin/chmod 775 $ENV{HDDATA}/listed/groups/$calname/calendar_events.txt";

   # bind founded group table vars
   tie %usertab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/listed/groups/$calname/usertab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login'] };
   $usertab{$login}{'login'} = $login;

   $cpublish = $input{'cpublish'};
   $lgrouptab{$calname}{'cpublish'} = $cpublish;
   if ($cpublish eq "on") {
      $logtab{$login}{referer} = $jp;
      if (!(-d "$ENV{HTTPHOME}/html/hd/groups/$calname"))  {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/groups/$calname";
         system "mkdir -p $ENV{HTTPHOME}/html/hd/contacts/$calname";
         $vdomain = $input{'vdomain'};
         if ($vdomain eq "") {
            $vdomain = "www.hotdiary.com"; 
         }
         $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/$hs/groups/$calname\" target=_main>http://$vdomain/groups/$calname</a>.";
         $contactmsg = "<p>$p2 has created a password-protected website for your contacts at <a href=\"http://$vdomain/$hs/contacts/$calname\" target=_main>http://$vdomain/contacts/$calname</a>.";
      }

      if (!(-f "$ENV{HTTPHOME}/html/hd/groups/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/contacts/index.cgi $ENV{HTTPHOME}/html/hd/contacts/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/groups/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDCGI}/contacts/webpage.cgi $ENV{HTTPHOME}/html/hd/contacts/$calname";
      }
   }
   $rh = $input{'rh'};

   if ($os ne "nt") {
         $execdiarychat = encurl "execdiarychat.cgi";
         $execbboard = encurl "execbboard.cgi";
   } else {
        $execdiarychat = "execdiarychat.cgi";
        $execbboard = "execbboard.cgi";
   }

   $diarychat = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execdiarychat&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>Chat Room</b></a>";

   $bboard = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execbboard&p1=biscuit&p2=jp&p3=g&pnum=4&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&g=$calname&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>Bulletin Board</b></a>";

   $ecalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&g=$calname&jp=$jp\">here</a> to edit your group or calendar.";
   $scalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp\">here</a> to search your group or calendar.";
   $mcalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=mc&jp=$jp\">here</a> to manage your group or calendar.";
   if ($jp eq "") {
      $chatmsg = "<p>We have created a java $diarychat for this group. You have unlimited free access to Diary Chat, your cool Java chat room.";
   }
   if ($jp eq "") {
      $bbmsg = "<p>We have created a $bboard discussion forum for $calname. You and others in your group have unlimited free access to Diary Board.";
   }
   status("$login: Congratulations! You have created a secure group called $calname. <p>You must remember the password ($calpassword) to access this group. $ecalmsg $scalmsg $mcalmsg $contactmsg $cmsg $chatmsg $bbmsg");

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%lgrouptab)->sync();

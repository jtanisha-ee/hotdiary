#!/usr/local/bin/perl5
#
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
# FileName: addbusinesscalendar.cgi 
# Purpose:  add a business calendar for your team 
# Creation Date: 12-01-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   #print &PrintHeader;
   hddebug ("addbusinesscalendar.cgi ");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   } 
   $os = $input{os}; 

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

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
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
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $sesstab{$biscuit}{'time'} = time();
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
   
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };
 
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

   $rh = $input{rh};
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $rh = $input{rh};
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
   }

   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   if (!-d ( "$ENV{HDDATA}/business/business/$business/teams/teamtab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/teamtab";
   }

   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc',  'projcode', 
		'supervisor', 'loccode', 'email', 'pager', 'fax' ] };


   $teamname = trim $input{teamname}; 
   $teamname = "\L$teamname";

   if ($os ne "nt") {
      $execbusinesscalclient = encurl "execbusinesscalclient.cgi";
      $execbusinesscalendar = encurl "execbusinesscalendar.cgi";
      $execsearchbusinesscalendars =  encurl "execsearchbusinesscalendars.cgi";
      $execcreatebusinesscalendar = encurl "execcreatebusinesscalendar.cgi";
   } else {
      $execbusinesscalclient = "execbusinesscalclient.cgi";
      $execbusinesscalendar =  "execbusinesscalendar.cgi";
      $execsearchbusinesscalendars =  "execsearchbusinesscalendars.cgi";
      $execcreatebusinesscalendar = "execcreatebusinesscalendar.cgi";
   }

   if (($teamname eq "") || (notLogin ($teamname)) ){ 
      status("$login: Enter a non-empty calendar team name or enter a team name that does not contain spaces. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execcreatebusinesscalendar&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business calendar."); 
      exit;
   }

   if (exists $teamtab{$teamname}) {
      status("$login: A calendar with ($teamname) already exists. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execcreatebusinesscalendar&p1=biscuit&p2=business&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create a business team."); 
      exit;
   }

   if (notDesc($input{teamtitle})) {
      status("$login: Invalid characters in team calendar title. Click <a href=\"validation.html\"> for help.");    
      exit;
   } 
   
   if (notDesc($input{teamdesc})) {
      status("$login: Invalid characters in team calendar description. Click <a href=\"validation.html\"> for help.");    
      exit;
   } 

   $teamtab{$teamname}{teamname} = trim $input{teamname};
   $teamtab{$teamname}{teamtitle} =  trim $input{teamtitle};
   $teamtab{$teamname}{teamdesc} = trim $input{teamdesc};
   $teamtab{$teamname}{supervisor} = trim $input{supervisor};
   $teamtab{$teamname}{projcode} = trim $input{projcode};
   $teamtab{$teamname}{loccode} = trim $input{loccode};
   $teamtab{$teamname}{email} = trim $input{email};
   $teamtab{$teamname}{pager} = trim $input{pager};
   $teamtab{$teamname}{fax} = trim $input{fax};

   system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
   system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
   system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";

   
   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']};          

   $teampeopletab{$login}{login} = $login;

   $cpublish = $input{'cpublish'};
   $teamtab{$teamname}{'cpublish'} = $cpublish;
   if ($cpublish eq "on") {
      if (!(-d "$ENV{HTTPHOME}/html/hd/business/$business/$teamname"))  {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/business/$business/$teamname";
         $vdomain = $input{'vdomain'};
         if ($vdomain eq "") {
            $vdomain = "$hotdiary";
         }
         $cmsg = "<p>Created a password-protected website for you at <a href=\"http://$vdomain/$hs/business/$business/$teamname\" target=_main>http://$vdomain/business/$business/$teamname</a>.";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/business/$business/$teamname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/business/$business/$teamname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/business/$business/$teamname/webpage.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/business/$business/$teamname";
      }
   }

   $ecalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=5&p0=$execbusinesscalclient&p1=biscuit&p2=teamname&p3=jp&p4=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&teamname=$teamname&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to edit your business calendar.";

   $scalmsg = "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=5&p0=$execsearchbusinesscalendars&p1=biscuit&p2=f&p3=jp&p4=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=sbc&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to view your business calendar.";

   status("$login: Congratulations! You have created a business Team ($teamname). A Business calendar with $teamname has been setup for your team. You can use your team calendar to set meetings, to-dos, reminders with your team members.  Your team members will be informed of all the events set in your team calendar. $ecalmsg $scalmsg");

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%teamtab)->sync();
   tied(%teampeopletab)->sync();

}

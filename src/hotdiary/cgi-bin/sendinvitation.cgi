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
# FileName: sendinvitation.cgi
# Calledby: inviteguest.cgi()
# Purpose: invite a guest to HotDiary
# Purpose: add user to hotdiary
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
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
   #print &HtmlTop ("sendguestinvitation.cgi example");
   hddebug "sendguestinvitation.cgi()";

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
              status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
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
      if (!exists $logtab{$login}) {
         error("Invalid login found in session.");
         exit;
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $HDLIC = $input{'HDLIC'};
      # bind login table vars
      tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };
   
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
   
                

   $email = $input{email};
   hddebug "email = $email"; 

   if ($email eq "") { 
     status("$login: Enter email address for inviting a guest."); 
     exit;
   }

   #generate a memberlogin for this guest
   if (notEmailAddress($email)) {
      status("Invalid characters in Email ($input{'email'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   $memberlogin = split "@", $email;
   $memberlogin = trim $memberlogin;
   hddebug "memberlogin = $memberlogin";
   if (trim $memberlogin ne "") {
      if (exists($logtab{$memberlogin} )) {
         $memberlogin = "$memberlogin$$";
       }
   } else {
      status("Invalid characters in Email ($input{'email'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }
   
   if (notName(trim $input{firstname})){
      $firstname = $memberlogin;
   } else {
      $firstname = $input{firstname};
   }
   if (notName(trim $input{lastname})){
      $lastname = $memberlogin;
   } else {
      $lastname = $input{lastname};
   }
    
   # create a member login account 
   $logtab{$memberlogin}{'login'} = $memberlogin;
   $logtab{$memberlogin}{'fname'} = $firstname;
   $logtab{$memberlogin}{'password'} = $lastname;
   $logtab{$memberlogin}{'email'} = $email;
   $logtab{$memberlogin}{'zone'} = $logtab{$login}{zone};

   # bind surveytab table vars
   tie %surveytab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/surveytab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };

   $surveytab{$memberlogin}{'login'} = $memberlogin;
   $surveytab{$memberlogin}{'hearaboutus'} = "Friend";
   $surveytab{$memberlogin}{'browser'} = $ENV{'HTTP_USER_AGENT'};
   tied(%surveytab)->sync();

   system "/bin/mkdir -p $ENV{HDREP}/$memberlogin";
   system "/bin/chmod 755 $ENV{HDREP}/$memberlogin";
   system "/bin/mkdir -p $ENV{HDHOME}/rep/$memberlogin";
   system "/bin/mkdir -p $ENV{HDDATA}/$memberlogin";
   system "/bin/chmod 755 $ENV{HDDATA}/$memberlogin";
   system "/bin/touch $ENV{HDDATA}/$memberlogin/addrentrytab";
   system "/bin/chmod 755 $ENV{HDDATA}/$memberlogin/addrentrytab";
   system "/bin/mkdir -p $ENV{HDDATA}/$memberlogin/addrtab";
   system "/bin/chmod 755 $ENV{HDDATA}/$memberlogin/addrtab";
   system "/bin/touch $ENV{HDDATA}/$memberlogin/apptentrytab";
   system "/bin/chmod 775 $ENV{HDDATA}/$memberlogin/apptentrytab";
   system "/bin/mkdir -p $ENV{HDDATA}/$memberlogin/appttab";
   system "/bin/chmod 775 $ENV{HDDATA}/$memberlogin/appttab";
   system "/bin/mkdir -p $ENV{HDDATA}/groups/$memberlogin/personal/pgrouptab";
   system "/bin/mkdir -p $ENV{HDDATA}/groups/$memberlogin/subscribed/sgrouptab";
   system "/bin/mkdir -p $ENV{HDDATA}/groups/$memberlogin/founded/fgrouptab";
   system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$memberlogin";
   system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$memberlogin/index.html";
   system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$memberlogin";
   system "/bin/chmod 775 $ENV{HDDATA}/$memberlogin/calendar_events.txt";

   system "/bin/mkdir -p $ENV{HDDATA}/$memberlogin/faxtab";
   system "/bin/chmod 755 $ENV{HDDATA}/$memberlogin/faxtab";

   system "/bin/mkdir -p $ENV{HDDATA}/$memberlogin/faxdeptab";
   system "/bin/chmod 755 $ENV{HDDATA}/$memberlogin/faxdeptab";

   $uname = $logtab{$login}{'fname'} . " " . $logtab{$login}{'lname'};
  
   $emsg = "Dear $logtab{$memberlogin}{'fname'},\n"; 
   $emsg .= "You have been invited by $uname to join $vdomain!. If you would like to contact $uname directly, please send an email to $uname to $logtab{$login}{email}. \n";
   $emsg .= "\nName: $logtab{$memberlogin}{'fname'} $logtab{$memberlogin}{'lname'}\n";
   $emsg .= "Your Login: $memberlogin \n";
   $emsg .= "Your Password: $logtab{$memberlogin}{'password'}\n\n";
   $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
   $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Internet Products and Services\n";

   $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
   qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
   qx{/bin/mail -s \"Invitation From $uname\" $logtab{$memberlogin}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};


                                                            
   $rh = $input{rh};
   $hs = $input{'hs'};
   $HDLIC = $input{HDLIC};  

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%logtab)->sync();

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDREP}/$alphaindex/$login/topcal.html";
   

#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: register.cgi
# Purpose: it register users in hotdiary.
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


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration"); 

  $rh = $input{'rh'};
  $vdomain = trim $input{'vdomain'};
  if ($vdomain eq "") {
     $vdomain = "www.hotdiary.com";
  }

  $hs = $input{'hs'};
  $login = trim $input{'login'};
  if (notLogin($login)) {
     if ($hs eq "") {  
        status("Invalid characters in login ($login). Make sure there are no spaces in the login name. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
     } else {
        status("Invalid characters in login ($login). Make sure there are no spaces in the login name. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
     }
     exit;
  }

  if ($login eq "") {
     if ($hs eq "") {
        status("Please choose a non-empty login name. This is required in order to complete your reqistration. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
     } else {
        status("Please choose a non-empty login name. This is required in order to complete your reqistration. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
     }
     exit;
  }

##### CASE BEGIN
  $login = "\L$login";
  hddebug "Changed to lower case $login";
##### CASE END


  $email = trim $input{'email'};
  hddebug "email = $email";
  if ($email eq "") {
     if ($hs eq "") {
        status("Please enter your email. This is required in order to complete your registration. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules.");
     } else {
        status("Please enter your email. This is required in order to complete your registration. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules.");
     }
     exit;
  }

##### CASE BEGIN
  $email = "\L$email";
##### CASE END



# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind cntrtab table vars
   tie %cntrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/cntrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['counter'] };

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite', 'installation', 'domains', 'domain', 'orgrole', 'organization', 'orgsize', 'budget', 'timeframe', 'platform', 'priority', 'editcal', 'calpeople' ] };

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed' ] };

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that
# the groupname is unique amoung all Listed as well as personal groups
   tie %plgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };


   if ( (-f "$ENV{HDDATA}/yplogtab/$login.rec") &&
       (!(-f "$ENV{HDDATA}/logtab/$login.rec")) ) {
       system "mv $ENV{HDDATA}/yplogtab/$login.rec $ENV{HDDATA}/logtab/$login.rec";
   }

# check if login  record exists.
   if (exists $logtab{$login}) {
       #print "Login record exists.\n";
       status("Member login \"$login\" already exists. Please use another login. For example, $login$$.");
       exit;
   } else {
	  if ((exists $lgrouptab{$login}) || (exists $plgrouptab{$login})) {
            status("Group with the same name as $login already exists. Names must be unique among group names and member login names. Try using another name, like $login$$.");
            exit;
          }

   	  if ($input{'acceptit'} ne "on") { 
	     status("You have not accepted HotDiary agreement, so cannot use the services of HotDiary");
	     exit;
          }  

          $input{'password'} = "\L$input{'password'}";
          $input{'rpassword'} = "\L$input{'rpassword'}";
          if ($input{'password'} ne $input {'rpassword'}) {
	     status("Passwords do not match. Please enter passwords again.\n");
	     exit;
	  }

          if ($input{'name'} eq "") {
             if ($hs eq "") {
                status("Name is not entered. This is required in order to complete your registration. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Name is not entered. This is required in order to complete your registration. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'name'})) {
	     if ($hs eq "") {
                status("Invalid characters in name ($input{'name'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Invalid characters in name ($input{'name'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notPhone(trim $input{'phone'})) {
	     if ($hs eq "") {
                status("Invalid characters in phone ($input{'phone'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Invalid characters in phone ($input{'phone'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             } 
             exit;
          }

          $fchar = substr $login, 0, 1;
          $alphaindex = $fchar . '-index';
 
# PLEASE NO VALIDATION AFTER THIS LINE
   
          $logtab{$login}{'login'} = $login;
          $pass = trim $input{'password'};
          $pass = "\L$pass";
          $logtab{$login}{'password'} = $pass;

          $logtab{$login}{'email'} = $email;
          if ($input{'checkid'} eq "on") {
             $logtab{$login}{'checkid'} =  "CHECKED";
             $input{'calpublish'} = "on";
          }
          if ($input{'calpublish'} eq "on") {
             $logtab{$login}{'calpublish'} =  "CHECKED";
             system "mkdir -p $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
             if ($login ne "") {
                system "rm -f $ENV{$HTTPHOME}/html/hd/members/$alphaindex/$login/*.cgi";
                system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
                system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
                if ($hs eq "") {
                   $cmsg = "<p>HotDiary has created a website for you. Your website is \"http://$vdomain/members/$alphaindex/$login\". Please note down this website for your future reference. Please click <a href=\"http://$vdomain/members/$alphaindex/$login\">here</a> to view your calendar!";
                } else {
                   $cmsg = "<p>HotDiary has created a website for you. Your website is \"http://$vdomain/$hs/members/$alphaindex/$login\". Please note down this website for your future reference. Please click <a href=\"http://$vdomain/$hs/members/$alphaindex/$login\">here</a> to view your calendar!";
                }
             } else {
                error("Invalid member login. No operation performed.");
                exit;
             }
          }
   	  if ($input{'informme'} eq "on") { 
             $logtab{$login}{'informme'} = "CHECKED";
          }
          $logtab{$login}{'phone'} = trim $input{'phone'};
          $logtab{$login}{'fname'} = trim $input{'name'};
          if ($input{vdomain} eq "") {
             $logtab{$login}{'remoteaddr'} = $ENV{'REMOTE_ADDR'};
          } else {
             $logtab{$login}{'remoteaddr'} = $input{vdomain};
          }
          $surveytab{$login}{'login'} = $login;
          $surveytab{$login}{'hearaboutus'} = $input{'hearaboutus'};
          $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
          $surveytab{$login}{'domains'} = $input{domains};
          $surveytab{$login}{'timeframe'} = $input{timeframe};
          $surveytab{$login}{'domain'} = $input{'domain'};
          $surveytab{$login}{'organization'} = $input{'organization'};
          $surveytab{$login}{'orgsize'} = $input{'orgsize'};
          $surveytab{$login}{'installation'} = $input{'installation'};
          $surveytab{$login}{'platform'} = $input{platform};
          $surveytab{$login}{'budget'} = $input{'budget'};
          if ($surveytab{$login}{'budget'} =~ /Free Edition/) {
             $instr = "Click <a href=http://www.hotdiary.com/jiveitauth.shtml>here</a> to setup a Free edition of JiveIt!";
          } else {
             $instr = "Click <a href=http://www.hotdiary.com/jiveitprofauth.shtml>here</a> to setup a Premium edition of JiveIt!";
          }
          $priority = multselkeys $input, "priority";
          $surveytab{$login}{'priority'} = $priority;
          $surveytab{$login}{'orgrole'} = $input{orgrole};
          $rhost = $ENV{'REMOTE_HOST'};
          $surveytab{$login}{'rhost'} = $rhost;
          tied(%surveytab)->sync();
          tied(%logtab)->sync();
          qx{cat $ENV{HDDATA}/logtab/$login.rec > $ENV{HDHOME}/tmp/prodregletter$$};
          qx{cat $ENV{HDDATA}/surveytab/$login.rec >> $ENV{HDHOME}/tmp/prodregletter$$};
          qx{/bin/mail -s \"JiveIt! Registration\" rhsup\@hotdiary.com < $ENV{HDHOME}/tmp/prodregletter$$};

          if ($rh eq "") {
          $msg = "$login: You have been registered to use HotDiary and download JiveIt!. <p>Now that you are a registered member of HotDiary, you can start using it and explore everything you can do with it.<p>Please remember your login ($login) and password ($input{'password'}) and keep it in safe place. $instr<p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, you must login to HotDiary, and use the Profile button to change your information. $cmsg"; 
          } else {
            if ($hs eq "") {
              $msg = "$login: You have been registered to use HotDiary and download JiveIt!. <p>Now that you are a registered member of HotDiary, you can start using it and explore everything you can do with it. Please remember your login ($login) and password ($input{'password'}) and keep it in safe place. $instr<p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, use the Profile link to change your information. $cmsg"; 
            } else {
              $msg = "$login: You have been registered to use HotDiary. Please remember your login ($login) and password ($input{'password'}) and keep it in safe place. $instr <p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, use the Profile link to change your information. $cmsg"; 
            }
          }

          $emsg = "Dear $logtab{$login}{'fname'},\n";
          $emsg .= qx{cat $ENV{'HDHOME'}/letters/regwelcome};
          $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
          $emsg .= "Login: $logtab{$login}{'login'}\n";
          $emsg .= "Password: $logtab{$login}{'password'}\n\n";
          $emsg .= "Regards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Collaborative Internet Organizer\n";

          qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/regletter$$};
          qx{/bin/mail -s \"HotDiary Registration Confirmation\" $logtab{$login}{'email'} < $ENV{HDHOME}/tmp/regletter$$};

          if ($logtab{$login}{'password'} eq "") {
             $msg .= "<p>Warning! You have not set a password. It is currently empty. If you would like to specify a non-empty password, you can login to HotDiary by entering your member login, and press the Submit button. Once you login successfully, look for the Profile button in the left frame, to explicitly set a password.";
          }
          $counter = $cntrtab{'counter'}{'counter'} + 1;
          if (($counter % $ENV{'REG_WINNER_FREQ'}) == 0) {
             $msg = $msg . "<p> Congratulations! You are the potential lucky registrant of HotDiary, and may qualify to win a free Skytel pager. Please contact us giving details about your member name, email, and postal address and we will send you more information about this lucky offer!";
             $logtab{$login}{'winner'} = "Yes";
          }
          $cntrtab{'counter'}{'counter'} = $cntrtab{'counter'}{'counter'} + 1;

          system "/bin/mkdir -p $ENV{HDREP}/$alphaindex/$login";
	  system "/bin/chmod 755 $ENV{HDREP}/$alphaindex/$login";

          system "/bin/mkdir -p $ENV{HDHREP}/$alphaindex/$login";
	  system "/bin/chmod 755 $ENV{HDHREP}/$alphaindex/$login";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login";

          system "/bin/touch $ENV{HDDATA}/$alphaindex/$login/addrentrytab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/addrentrytab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/addrtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/addrtab";

          system "/bin/touch $ENV{HDDATA}/$alphaindex/$login/apptentrytab";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/apptentrytab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/appttab";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/appttab";

          system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/personal/pgrouptab";
          #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
          #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
	  system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$login";
          system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login/index.html";
          system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$login";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/calendar_events.txt";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxtab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxdeptab";

   	  if ($input{'upgrade'} eq "on") { 
             $prml = "";
             $expiry = localtime(time() + 5);
             $expiry = "\:$expiry";
             $prml = strapp $prml, "expiry=$expiry";
             $urlcgi = buildurl("execupgrade.cgi");
             $prml = strapp $prml, "actioncgi=$urlcgi";
             $prml = strapp $prml, "label=HotDiary Upgrade Services";
             $prml = strapp $prml, "login=$login";
             $prml = strapp $prml, "template=$ENV{HDTMPL}/chargecard.html";
             $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/chargecard-$$.html";
             $urlcgi = buildurl("execupgrade.cgi");
             parseIt $prml;
             $prml = "";
             system "/bin/cat $ENV{HDREP}/$alphaindex/$login/chargecard-$$.html"; 
	  } else {
             status("$msg");
             #system "java COM.hotdiary.main.SendPage \"1412165\" \"PRegistration\" \"$login\"";
	  }
	  
   }


#synch the database
   tied(%logtab)->sync();
   tied(%cntrtab)->sync();
}

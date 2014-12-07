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

  $vdomain = trim $input{'vdomain'};
  $jp = $input{jp};
  if ($vdomain eq "") {
     $vdomain = "www.hotdiary.com";
  }

  hddebug "jp = $jp";
  $hs = $input{'hs'};
  if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }
                       
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
        status("Please enter a non-empty login name. This is required in order to complete your reqistration. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
     } else {
        status("Please enter a non-empty login name. This is required in order to complete your reqistration. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

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
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost'] };

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

          if ($input{'fname'} eq "") {
             if ($hs eq "") {
                status("First name is not entered. This is required in order to complete your registration. Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("First name is not entered. This is required in order to complete your registration. Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'fname'})) {
	     if ($hs eq "") {
                status("Invalid characters in first name ($input{'fname'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Invalid characters in first name ($input{'fname'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'lname'})) {
	     if ($hs eq "") {
                status("Invalid characters in last name ($input{'lname'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else  {
                status("Invalid characters in last name ($input{'lname'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
 
             exit;
          }

          if (notAddress(trim $input{'street'})) {
	     if ($hs eq "") {
                status("Invalid characters in street ($input{'street'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else {
                status("Invalid characters in street ($input{'street'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'city'})) { 
	     if ($hs eq "") {
               status("Invalid characters in city ($input{'city'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else {
               status("Invalid characters in city ($input{'city'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'state'})) { 
	     if ($hs eq "") {
               status("Invalid characters in state ($input{'state'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else {
               status("Invalid characters in state ($input{'state'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
	     }
             exit;
          }

          if (notNumber(trim $input{'zipcode'})) { 
	     if ($hs eq "") {
                status("Invalid characters in zipcode ($input{'zipcode'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else {
                status("Invalid characters in zipcode ($input{'zipcode'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
          }

          if (notName(trim $input{'country'})) {
             if ($hs eq "") {
               status("Invalid characters in country ($input{'country'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
	     } else {
               status("Invalid characters in country ($input{'country'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
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
 
          $pgtype = $input{'pagertype'};
         
          if ("\L$pgtype" ne "\LOther Pager") {
	  if (notPhone(trim $input{'pager'})) {
             if ($hs eq "") {
               status("Invalid characters in pager ($input{'pager'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             exit;
            } else {
               status("Invalid characters in pager ($input{'pager'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
            }
          }
          }

	  if (notPhone(trim $input{'fax'})) {
             if ($hs eq "") {
                status("Invalid characters in fax ($input{'fax'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Invalid characters in fax ($input{'fax'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
	     exit;
          } 
 
          if (notPhone(trim $input{'cellp'})) {
             if ($hs eq "") {
               status("Invalid characters in cell phone ($input{'cellp'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
               status("Invalid characters in cell phone ($input{'cellp'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
	  }
   
	  if (notPhone(trim $input{'busp'})) {
             if ($hs eq "") {
                status("Invalid characters in business phone ($input{'busp'}). Click <a href=\"http://$vdomain/validation.html\"> here</a> to learn validation rules. \n");
             } else {
                status("Invalid characters in business phone ($input{'busp'}). Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> to learn validation rules. \n");
             }
             exit;
	  }
          #if ("\U$pgtype" ne "\UOther Pager") {
             #if (!(notEmailAddress(trim $input{'pager'}))) {
             #   status("You have selected pager type as $pgtype but entered an email address in the pager field. Please enter the pager PIN number or pager number instead of email address. <p>If you would still like to enter an email address for your pager, select the pager type to be \"Other Pager\".\n");
             #   exit;
             #}
          #} else {
	  #   if (trim $input{'pager'} ne "") {
          #      if (notEmailAddress(trim $input{'pager'})) {
          #         status("You have selected pager type as $pgtype but not entered an email address in the pager field. Please enter a valid email address of the form user\@domain.com.\n");
          #         exit;
	  #      }
          #   }
          #}

# PLEASE NO VALIDATION AFTER THIS LINE
   
          $logtab{$login}{'login'} = $login;
          #$logtab{$login}{'password'} = trim $input{'password'};
          $pass = trim $input{'password'};
          $pass = "\L$pass";
          $logtab{$login}{'password'} = $pass;

          #$logtab{$login}{'email'} = trim $input{'email'};
          $logtab{$login}{'email'} = $email;
          $logtab{$login}{'url'} = trim $input{'url'};
          if ($input{'checkid'} eq "on") {
             $logtab{$login}{'checkid'} =  "CHECKED";
          }
          if ($input{'calpublish'} eq "on") {
             $logtab{$login}{'calpublish'} =  "CHECKED";
             system "mkdir -p $ENV{HTTPHOME}/html/hd/members/$login";
             if ($login ne "") {
                system "rm -f $ENV{$HTTPHOME}/html/hd/members/$login/*.cgi";
                system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/members/$login";
                system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/members/$login";
                if (("\L$vdomain" eq "www.hotdiary.com") || ("\L$vdomain" eq "hotdiary.com")) {
                   $cmsg = "<p>You have chosen to publish your calendar on the web. HotDiary has created a website for you. Your website is \"http://$vdomain/members/$login\". Please note down this website for your future reference. Please click <a href=\"http://$vdomain/members/$login\" target=_main>here</a> to view your calendar!";
                } else {
                   #$cmsg = "<p>You have chosen to publish your calendar on the web. HotDiary has created a website for you. Your website is \"http://$vdomain/$hs/members/$login\". Please note down this website for your future reference. Please click <a href=\"http://$vdomain/$hs/members/$login\" target=_main>here</a> to view your calendar!";
                   $cmsg = "";
                }
             } else {
                error("Invalid member login. No operation performed.");
                exit;
             }
          }
   	  if ($input{'informme'} eq "on") { 
             $logtab{$login}{'informme'} = "CHECKED";
          }
   	  if ($input{'cserver'} eq "on") { 
             $logtab{$login}{'cserver'} = "CHECKED";
          }
          $logtab{$login}{'pagertype'} = $input{'pagertype'};
          $logtab{$login}{'bphone'} = trim $input{'busp'};
          $logtab{$login}{'cphone'} = trim $input{'cellp'};
          $logtab{$login}{'fax'} = trim $input{'fax'};
          $logtab{$login}{'pager'} = trim $input{'pager'};
          $logtab{$login}{'phone'} = trim $input{'phone'};
          $logtab{$login}{'country'} = trim $input{'country'};
          $logtab{$login}{'zipcode'} = trim $input{'zipcode'};
          $logtab{$login}{'state'} = trim $input{'state'};
          $logtab{$login}{'city'} = trim $input{'city'};
          $logtab{$login}{'street'} = trim $input{'street'};
          $logtab{$login}{'lname'} = trim $input{'lname'};
          $logtab{$login}{'fname'} = trim $input{'fname'};
          $logtab{$login}{'zone'} = $input{'zone'};
          tie %jivetab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/jivetab",
             SUFIX => '.rec',
             SCHEMA => {
             ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
		'account', 'topleft', 'topright', 'middleright', 
		'bottomleft', 'bottomright', 'meta'] };
          if (exists $jivetab{$jp}) {
             $logtab{$login}{'referer'} = $jp;
          }
          if ($input{vdomain} eq "") {
             $logtab{$login}{'remoteaddr'} = $ENV{'REMOTE_ADDR'};
          } else {
             $logtab{$login}{'remoteaddr'} = $input{vdomain};
          }
          $surveytab{$login}{'login'} = $login;
          $surveytab{$login}{'hearaboutus'} = $input{'hearaboutus'};
          $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
          #$rhost = qx{nslookup $ENV{'REMOTE_HOST'} | grep Name};
          #$rhost =~ s/\n//g;
          $rhost = $ENV{'REMOTE_HOST'};
          #($junk, $rhost) = split ':', $rhost;
          $surveytab{$login}{'rhost'} = $rhost;
          #$envout = PrintEnv();
          #hddebug "$envout";
          tied(%surveytab)->sync();
          if ($jp ne "") {
             ## bind jivetab table vars
             tie %jivetab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/jivetab",
             SUFIX => '.rec',
             SCHEMA => {
                  ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };

             if (exists $jivetab{$jp}) {
                $jivetab{$jp}{account} = $jivetab{$jp}{account} + $ENV{JIVEIT_COMMISSION};
                $jivetab{$jp}{regusers} = $jivetab{$jp}{regusers} + 1;
                tied(%jivetab)->sync();
             }
          }

          $rh = $input{'rh'};
          if ($rh eq "") {
          $msg = "$login: You have been registered to use HotDiary. Please remember your login ($login) and password ($input{'password'}) and keep it in a safe place. Click <a href=\"http://$vdomain/$hs/$icgi \"> here</a> to login. <p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, you must login to HotDiary, and use the Profile button to change your information. $cmsg"; 
          } else {
            if ($hs eq "") {
              $msg = "$login: You have been registered to use HotDiary. Please remember your login ($login) and password ($input{'password'}) and keep it in a safe place. Click <a href=\"http://$vdomain/$icgi \"> here</a> to login. <p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, use the Profile link to change your information. $cmsg"; 
            } else {
              $msg = "$login: You have been registered to use HotDiary. Please remember your login ($login) and password ($input{'password'}) and keep it in safe place. Click <a href=\"http://$vdomain/$hs/$icgi \"> here</a> to login. <p>If you wish to change any information in your registration, you cannot use the browser Back button to change it (since your member login has already been created). If you do so, you will receive a message that the member already exists. Instead, use the Profile link to change your information. $cmsg"; 
            }
          }
          if ($input{'cserver'} eq "on") {
            $msg .= "<p>You are the winner of HotDiary JiveIt! license. With JiveIt! you can run calendar service on your own website or domain.  You can create your own free JiveIt! account online <a href=\"http://www.hotdiary.com/jiveitauth.html\">here. You can earn 50c towards every member that registers from your site. This offer is valid only if you install JiveIt! within 24 hours of your registration.</a>";
             
          }

          $emsg = "Dear $logtab{$login}{'fname'},\n";
          $emsg .= qx{cat $ENV{'HDHOME'}/letters/regwelcome};
          $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
          $emsg .= "Login: $logtab{$login}{'login'}\n";
          $emsg .= "Password: $logtab{$login}{'password'}\n\n";
          $emsg .= "Regards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary (http://www.hotdiary.com) - Innovative Internet Calendaring Products and Services\n";

          qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/regletter$$};
          #qx{/bin/mail -s \"HotDiary Registration Confirmation\" $logtab{$login}{'email'} < $ENV{HDHOME}/tmp/regletter$$};

          if ($logtab{$login}{'password'} eq "") {
             $msg .= "<p>Warning! You have not set a password. It is currently empty. If you would like to specify a non-empty password, you can login to HotDiary by entering your member login, and press the Submit button. Once you login successfully, look for the Profile button in the left frame, to explicitly set a password.";
          }
          $counter = $cntrtab{'counter'}{'counter'} + 1;
          if (($counter % $ENV{'REG_WINNER_FREQ'}) == 0) {
             $msg = $msg . "<p> Congratulations! You are the potential lucky registrant of HotDiary, and may qualify to win a free Skytel pager. Please contact us giving details about your member name, email, and postal address and we will send you more information about this lucky offer!";
             $logtab{$login}{'winner'} = "Yes";
          }
          $cntrtab{'counter'}{'counter'} = $cntrtab{'counter'}{'counter'} + 1;
          system "/bin/mkdir -p $ENV{HDREP}/$login";
	  system "/bin/chmod 755 $ENV{HDREP}/$login";
          system "/bin/mkdir -p $ENV{HDHOME}/rep/$login";
          system "/bin/mkdir -p $ENV{HDDATA}/$login";
	  system "/bin/chmod 755 $ENV{HDDATA}/$login";
          system "/bin/touch $ENV{HDDATA}/$login/addrentrytab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$login/addrentrytab";
          system "/bin/mkdir -p $ENV{HDDATA}/$login/addrtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$login/addrtab";
          system "/bin/touch $ENV{HDDATA}/$login/apptentrytab";
	  system "/bin/chmod 660 $ENV{HDDATA}/$login/apptentrytab";
          system "/bin/mkdir -p $ENV{HDDATA}/$login/appttab";
	  system "/bin/chmod 770 $ENV{HDDATA}/$login/appttab";
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/personal/pgrouptab";
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/founded/fgrouptab";
	  system "/bin/chmod -R 770 $ENV{HDDATA}/groups/$login";
          system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";
          system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$login";
	  system "/bin/chmod 775 $ENV{HDDATA}/$login/calendar_events.txt";

          system "/bin/mkdir -p $ENV{HDDATA}/$login/faxtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$login/faxtab";

          system "/bin/mkdir -p $ENV{HDDATA}/$login/faxdeptab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$login/faxdeptab";

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
             $prml = strapp $prml, "templateout=$ENV{HDREP}/$login/chargecard.html";
             $urlcgi = buildurl("execupgrade.cgi");
             parseIt $prml;
             $prml = "";
             system "/bin/cat $ENV{HDREP}/$login/chargecard.html"; 
	  } else {
             status("$msg");
	  }
	  
   }


#synch the database
   tied(%logtab)->sync();
   tied(%cntrtab)->sync();
}

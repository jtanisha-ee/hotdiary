#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: login.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 10-09-97
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
#use UNIVERSAL qw(isa);
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = 3600;


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Login"); 

   #print "login = ", $input{'login'};

   if ($input{"Submit"} eq "Search") {
   #   status("Search service is coming soon!.");
      $action = "Search";
   #   exit;
   }

   hddebug "Entered HotDiary Got login= $input{'login'}";
   hddebug "Entered HotDiary Got password = $input{'password'}";

## set the cookie
   

# bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };
 
   $HDLIC = $input{'HDLIC'};
   hddebug "HDLIC = $HDLIC";
   $vdomain = $input{'vdomain'};
   $os = $input{'os'};
   $jp = $input{'jp'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }       

   $hs = $input{'hs'};
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

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      
 
   $login = trim $input{'login'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   if ($login eq "") {
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.");
	      exit;
	    }
         }
         status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      } else {
         status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      }
      exit;
   }
 

##### CASE BEGIN
   $login = "\L$login";
   hddebug "Lower case login = $login";
##### CASE END



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

# since error dataplates are too small, before they are synced to disc
# webserver tries to print them, and fails. to prevent this, we need
# to ensure that the error dataplates are created before we exit
# from this script
# check if the login does not exist
   if (!exists $logtab{$login}) {
      hddebug "login = $login, password = $input{'password'}";
##### CASE BEGIN
      if ($hs eq "") {
         status("The member login \"$login\" is not a valid login. Please enter a valid member login. <p>If you haven't yet registered with $vdomain, please do so before you login.  Click <a href=\"http://$vdomain/register.html\" TARGET=\"_parent\"> here</a> to Register. If you have forgotten your password, click <a href=\"forgotpasswd.html\">here.</a>");
      } else {
         status("The member login \"$login\" is not a valid login. Please enter a valid member login. <p>If you haven't yet registered with $vdomain, please do so before you login.  Click <a href=\"http://$vdomain/$hs/register.html\" TARGET=\"_parent\"> here</a> to Register."); 
      }
##### CASE END
      exit;
   } else {
        if ($logtab{$login}{'password'} ne "") {
##### CASE BEGIN
           $pass = trim $input{'password'};
           $pass = "\L$pass";
##### CASE END
##### CASE BEGIN
           hddebug "logtab password = $logtab{$login}{'password'}";
           hddebug "Entered password = $pass";
           if (!($logtab{$login}{'password'} eq $pass)) {
##### CAE END

          if ($hs eq "") {
              if ($jp ne "") {
                 if ($jp ne "buddie") {
                   status("$login: Could not login. Enter correct password.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login. If you have forgotten your password, click <a href=\"forgotpasswd.html\">here.</a>");
                   exit;
                 }
              }
              status("$login: Could not login. Enter correct password.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login. If you have forgotten your password, click <a href=\"forgotpasswd.html\">here.</a>");
          } else {
              status("$login: Could not login. Enter correct password.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login."); 
          }
          exit;
          }
       }
   }

   $remoteaddr = $ENV{'REMOTE_ADDR'};
   $sessionid = getkeys();

# bake a biscuit
   $biscuit = "$sessionid-$login-$remoteaddr";
   $title = time();

# check if user has already logged in

   if (!exists $logsess{$login}) {
      $sesstab{$biscuit}{'login'} = $login;
      $sesstab{$biscuit}{'biscuit'} = $biscuit;
      $sesstab{$biscuit}{'time'} = time();
      $logsess{$login}{'login'} = $login;
      $logsess{$login}{'biscuit'} = $biscuit;
   } 
   else {

      if (!exists $sesstab{$logsess{$login}{'biscuit'}}) {
	 delete $logsess{$login};
	 error("$login: Either your session has expired or there is inconsistency in your session information. Please try to login again. If this problem persists, send us an email.");
	 exit;
      }

# if session has not expired then, check if remote addr of current user
# is same as remote addr in sesstab table for this user
      if ((time() - $sesstab{$logsess{$login}{'biscuit'}}{'time'}) 
		< $SESSION_TIMEOUT) {  
         ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         #if ($raddr eq $remoteaddr) {
            delete $sesstab{$logsess{$login}{'biscuit'}};
            delete $logsess{$login};
            $sesstab{$biscuit}{'biscuit'} = $biscuit;
            $sesstab{$biscuit}{'login'} = $login;
            $sesstab{$biscuit}{'time'} = time();
            $logsess{$login}{'login'} = $login;
            $logsess{$login}{'biscuit'} = $biscuit;
         #} 
         #else {
            #error("$login: Intrusion detected. Access denied.\n");
            #exit;
         #}
# if session has expired then do not check for intrusion problem, since
# the user may have logged into one location, then travelled to another
# location and logged in from there with same login, but not within
# 3600 seconds.
      } else {
         ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         delete $sesstab{$logsess{$login}{'biscuit'}};
         delete $logsess{$login};
         $sesstab{$biscuit}{'biscuit'} = $biscuit;
         $sesstab{$biscuit}{'login'} = $login;
         $sesstab{$biscuit}{'time'} = time();
         $logsess{$login}{'login'} = $login;
         $logsess{$login}{'biscuit'} = $biscuit;
      }
  }

# if we reached here, the login was successful, display the choice screen

   #print "Hello $login! You have successfully logged in.\n";
   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if (!-d "$ENV{HDREP}/$alpha/$login") {
      system "mkdir -p $ENV{HDREP}/$alpha/$login";
      system "chmod 755 $ENV{HDREP}/$alpha/$login";
      system "chown nobody:nobody $ENV{HDREP}/$alpha/$login";
   }
   if (!-d "$ENV{HDHREP}/$alpha/$login") {
      system "mkdir -p $ENV{HDHREP}/$alpha/$login";
      system "chmod 755 $ENV{HDHREP}/$alpha/$login";
      system "chown nobody:nobody $ENV{HDHREP}/$alpha/$login";
   }
 
   system "/bin/rm -f $ENV{HDREP}/$alpha/$login/*.html";
   system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html";
   system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alpha/$login/index.html";

   $prml = "";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/proxy/redirect.html";
   $rh = $input{'rh'};
   $url = adjusturl "/cgi-bin/$rh/execdocalclient.cgi?biscuit=$biscuit&vw=m&jp=$jp&os=$os";
   $prml = strapp $prml, "redirecturl=$url";
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";

# save the info in db
   tied(%logtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

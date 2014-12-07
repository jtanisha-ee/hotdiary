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

$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration"); 

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

  if ( ($email =~ /yahoo.com/) ||
       ($email =~ /msn.com/) ||
       ($email =~ /hotmail.com/) ||
       ($email =~ /mail.com/) ||
       ($email =~ /aol.com/) ||
       ($email =~ /lycos.com/) ||
       ($email =~ /excite.com/) ||
       ($email =~ /juno.com/) ||
       ($email =~ /altavista.com/) ) {
     status("You must use your company email address, as opposed to a email service provider email address.");
     exit;
  }

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind redbasintab table vars
  tie %redbasintab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/redbasintab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'name', 'street', 'city', 'state', 'zipcode', 'country', 'phone', 'email', 'checkid', 'remoteaddr', 'informme', 'hearaboutus', 'browser', 'rhost', 'installation', 'domains', 'url', 'orgrole', 'organization', 'orgsize', 'budget', 'timeframe', 'platform', 'priority', 'tools' ] };

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
          $redbasintab{$login}{'login'} = $login;
          $redbasintab{$login}{'checkid'} =  "CHECKED";

          $logtab{$login}{'suite'} = trim $input{'suite'};
          $redbasintab{$login}{'suite'} = trim $input{'suite'};

          $logtab{$login}{'street'} = trim $input{'street'};
          $redbasintab{$login}{'street'} = trim $input{'street'};

          $logtab{$login}{'city'} = trim $input{'city'};
          $redbasintab{$login}{'city'} = trim $input{'city'};

          $logtab{$login}{'state'} = trim $input{'state'};
          $redbasintab{$login}{'state'} = trim $input{'state'};

          $logtab{$login}{'zipcode'} = trim $input{'zipcode'};
          $redbasintab{$login}{'zipcode'} = trim $input{'zipcode'};

          $logtab{$login}{'country'} = trim $input{'country'};
          $redbasintab{$login}{'country'} = trim $input{'country'};

          $redbasintab{$login}{'phone'} = trim $input{'phone'};
          $redbasintab{$login}{'remoteaddr'} = $logtab{$login}{'remoteaddr'};
          $redbasintab{$login}{'name'} = trim $input{'name'};
          $redbasintab{$login}{'hearaboutus'} = $input{'hearaboutus'};
          $redbasintab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
          $redbasintab{$login}{'domains'} = $input{domains};
          $redbasintab{$login}{'tools'} = $input{tools};
          $redbasintab{$login}{'timeframe'} = $input{timeframe};
          $redbasintab{$login}{'url'} = $input{'domain'};
          $redbasintab{$login}{'organization'} = $input{'organization'};
          $redbasintab{$login}{'orgsize'} = $input{'orgsize'};
          $redbasintab{$login}{'installation'} = $input{'installation'};
          $redbasintab{$login}{'platform'} = $input{platform};
          $redbasintab{$login}{'budget'} = $input{'budget'};
          $priority = multselkeys $input, "priority";
          $redbasintab{$login}{'priority'} = $priority;
          $redbasintab{$login}{'orgrole'} = $input{orgrole};
          $rhost = $ENV{'REMOTE_HOST'};
          $redbasintab{$login}{'rhost'} = $rhost;
          tied(%redbasintab)->sync();
          tied(%logtab)->sync();
          qx{cat $ENV{HDDATA}/logtab/$login.rec > $ENV{HDHOME}/tmp/bizwareregletter$$};
          qx{cat $ENV{HDDATA}/redbasintab/$login.rec >> $ENV{HDHOME}/tmp/bizwareregletter$$};
          qx{/bin/mail -s \"Bizware Registration\" custrep\@$diary < $ENV{HDHOME}/tmp/bizwareregletter$$};

          }

          $emsg = "Dear $logtab{$login}{'fname'},\n";
          $emsg .= qx{cat $ENV{'HDHOME'}/letters/bizwareregwelcome};
          $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
          $emsg .= "Login: $logtab{$login}{'login'}\n";
          $emsg .= "Password: $logtab{$login}{'password'}\n\n";
          $emsg .= "Regards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary ($hddomain80) - The E-Business Automation Leader\n";

          qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/regletter$$};
          qx{/bin/mail -s \"Bizware E-Business Server Registration\" $logtab{$login}{'email'} < $ENV{HDHOME}/tmp/regletter$$};

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
	  system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$login";
          system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login/index.html";
          system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$login";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/calendar_events.txt";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxtab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxdeptab";

          status("Your request to license Bizware E-Business Server has been received and will be shortly be processed. In the meantime, please note that you have been assigned a customer member id $login and password $input{password} based upon your input. Feel free to use this ID in future correspondence that you have with HotDiary. Click <a href=http://www.brainseller.com:8080/bizware/class103>here</a> to go back to the Bizware E-Business website.");

   }

#synch the database
   tied(%logtab)->sync();
   tied(%redbasintab)->sync();

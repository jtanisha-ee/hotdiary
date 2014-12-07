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
# FileName: invitebuddie.cgi
# Purpose: it invite users to hotdiary.
# Creation Date: 06-02-99
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
   #print &HtmlTop ("HotDiary Invitation"); 

  $login = trim $input{'login'};

#### BEGIN CASE
  $login = "\L$login";
#### END CASE

  if (notLogin($login)) {
     status("Invalid characters in login. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
     exit;
  }


  if ($login eq "") {
     status("Please enter a non-empty login name for your invitee. This is required in order to complete your invitation. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
     exit;
  }

  $email = trim $input{'email'};
#### BEGIN CASE
  $email = "\L$email";
#### END CASE

  if ($email eq "") {
     status("Please enter your invitee's email. This is required in order to complete your invitation. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
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

# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };


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
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
	   'installation', 'domains', 'domain', 'orgrole', 'organization', 'orgsize', 'budget', 'timeframe', 'platform', 'priority', 'editcal', 'calpeople'] };

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg',
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

   	  #if ($input{'acceptit'} ne "on") { 
	  #   status("You have not accepted HotDiary agreement, so cannot use the services of HotDiary");
	  #   exit;
          #}  

          #if ($input{'password'} ne $input {'rpassword'}) {
	  #   status("Passwords do not match. Please enter passwords again.\n");
	  #   exit;
	  #}

          if ($input{'invitee'} eq "") {
             status("First name of your invitee is not entered. This is required in order to complete your invitation. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
             exit;
          }

          if (notName(trim $input{'invitee'})) {
             status("Invalid characters in first name. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
             exit;
          }

##### BEGIN CASE
          $logi = "\L$login";
          $logtab{$login}{'login'} = $logi;
          #$logtab{$login}{'login'} = $login;
          $logtab{$login}{'fname'} = $input{invitee};
          $logtab{$login}{'password'} = $logi;
          #$logtab{$login}{'password'} = $login;
          $em = trim $input{'email'};
          $em = "\L$em";
          $logtab{$login}{'email'} = $em;
##### END CASE

          $fchar = substr $login, 0, 1;
          $alphaindex = $fchar . '-index';
 
          #$logtab{$login}{'login'} = $login;
          $logtab{$login}{'fname'} = $input{invitee};
          $logtab{$login}{'password'} = $login;
          $logtab{$login}{'email'} = trim $input{'email'};
          $logtab{$login}{'zone'} = $logtab{$input{mname}}{zone};

          $pidd = $$;
          $acode = rand $pidd;
          $acode = $acode % $pidd;
          $activetab{$login}{login} = $login;
          $activetab{$login}{acode} = $acode;
          $activetab{$login}{verified} = "false";
          tied(%activetab)->sync();

          $msg = "You have successfully prepared an invitation email that will be emailed to your invitee at the email address $email.";

          $emsg = "Dear $logtab{$login}{'fname'},\n";
          $mname = $logtab{$input{mname}}{'fname'} . " " . $logtab{$input{mname}}{'lname'};
          $emsg .= "You have been invited by $mname to join http://www.hotdiary.com! If you would like to contact $mname directly, please send an email to $mname at $logtab{$input{mname}}{'email'}.\n";

          $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
          $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
          $emsg .= "Login: $logtab{$login}{'login'}\n";
          $emsg .= "Password: $logtab{$login}{'password'}\n\n";
          $emsg .= "Regards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Collaborative Internet Organizer\n";

          qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
          qx{/bin/mail -s \"Invitation From $mname\" $logtab{$login}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};
          system "/bin/mkdir -p $ENV{HDREP}/$alphaindex/$login";
	  system "/bin/chmod 755 $ENV{HDREP}/$alphaindex/$login";
          system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphaindex/$login";
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
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
	  system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$login";
          system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login/index.html";
          system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$login";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/calendar_events.txt";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxtab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
 
          status($msg);
   }


#synch the database
   tied(%logtab)->sync();
}

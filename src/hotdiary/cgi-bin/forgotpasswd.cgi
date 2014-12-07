#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: forgotpasswd.cgi
# Purpose: Validate email in records, and send login/passwd by email to user
# 
# Creation Date: 04-11-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Login"); 

   if ($input{"Submit"} eq "Search") {
      $action = "Search";
   }

# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      
 
   if ($action eq "Search") {
      $search = trim $input{'search'};
      if ($search eq "") {
         status("Please enter a non-empty search criteria. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         exit;
      }
      if ($search =~ /\\/) {
         status("Invalid characters found in search expression. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         exit;
      }
      ($firstname, $lastname) = split(" ", $search);
      $firstname = trim $firstname;
      $lastname = trim $lastname;
      if (($firstname eq "") && ($lastname eq "")) {
         status("Please enter \"firstname, lastname\" in search criteria. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         exit;
      }
      $tooshort = "";
      if (((length $firstname) <= 3) && ((length $lastname) <= 3)) {
         $msg .= "The specified search names are too short. A lot of matches were found. However, HotDiary will not display all these members, for protecting user and system security. Will perform an exact name match search to shorten output.<BR>";
         $tooshort = "true";
         $msg .= "<p>\"$firstname\", \"$lastname\" <b>exactly</b> matches the following public members on HotDiary: <BR><DL>";
      } else {
         $msg .= "<p>\"$firstname\", \"$lastname\" matches the following public members on HotDiary: <BR><DL>";
      }

      $cntr = 0;
      foreach $account (sort keys %logtab) {
         $checkid = $logtab{$account}{'checkid'};
         if ($checkid eq "CHECKED") {
            if ((($tooshort eq "") && (nmmatch $logtab{$account}{'fname'}, $firstname) && (nmmatch $logtab{$account}{'lname'}, $lastname)) ||
               (($tooshort eq "true") && ("\U$logtab{$account}{'fname'}" eq "\U$firstname") && ("\U($logtab{$account}{'lname'}" eq "\U$lastname"))) {
               $cntr++;
               $msg .= "<LI>";
               $msg .= $logtab{$account}{'fname'} . " " . $logtab{$account}{'lname'} . "<BR>";
               $msg .= "Member Login: $account <BR>";
               #$msg .= "Member Email: $logtab{$account}{'email'} <BR>";
               $msg .= "</LI><BR>";
            }
         }
      }
      $msg .= "</DL>";
      if ($cntr eq "0") {
         $msg .= "<p>Did not find any matches based on your search criteria.<BR>";
         if (($firstname eq "FirstName") || ($lastname eq "LastName")) {
            $msg .= "<p>Hint: Please replace \"FirstName\" with the actual first name, and \"LastName\" with the actual last name, that you are looking for.<BR>";
         } else {
            if ($tooshort eq "") {
               $msg .= "<p>It is likely that the person you are looking for has decided not to make his/her ID public. So even if he/she exists on HotDiary as a valid member, you will not be able to find him/her.<BR>";
            }
         }
      } else {
         $msg .= "<BR>Found a total of $cntr matches.<BR>";
      }
      status($msg);
      exit;
   }


   $login = trim $input{'login'};
   $login = "\L$login";
   $email = trim $input{'email'};
   $email = "\L$email";
   if ( ($login eq "") && ($email eq "") ) {
      status("Please enter atleast one field (login and/or email). Click <a href=\"forgotpasswd.html\" TARGET=\"_parent\"> here</a> to login.");
      exit;
   } else {
      if ($login eq "") {
         status("We have launched a search for the email address ($email) you have specified. This search should complete in the next 15 minutes, and you should receive an email from us containing your account information, if we are able to find your email address in our database. Your email address would have existed in our database only if you had previously registered with us. Click <a href=\"/\">here</a> to continue.");
         system "nice $ENV{HDCGI}/searchlogin.cgi $email > $ENV{HDHOME}/tmp/lostlogin-$$.txt; /usr/bin/metasend -b -S 800000 -m \"text/plain\" -f $ENV{HDHOME}/tmp/lostlogin-$$.txt -s \"Your Lost Account\" -e \"\" -t \"$email\" -F rhsup\@hotdiary.com 1>/dev/null 2>&1";
         exit;
      }
   }

   if (!exists $logtab{$login})  {
      status("The login you have entered ($login) does not exist. Click <a href=\"forgotpasswd.html\" TARGET=\"_parent\"> here</a> to retry.");
      exit;
   }

   if ($email eq "") {
      status("Please enter a non-empty email. Click <a href=\"forgotpasswd.html\" TARGET=\"_parent\"> here</a> to retry.");
      exit;
   }
   if (exists $activetab{$login}) {
      $acode = $activetab{$login}{acode};
   } else {
      $acode = "Not Applicable";
   }
   #$msg = "Dear Member,\n\nPlease use the information below to sign-in to your HotDiary account.\n\nMember Login: $login\nPassword: $logtab{$login}{'password'}\n\nActivation Code: $acode\n\nRegards,\nHotDiary Inc\n\nHotDiary (http://www.hotdiary.com) - New Generation Internet Organizer.";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/lostpasswd.html";
   $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/lostpasswd-$login.html";
   $prml = strapp $prml, "login=$login";
   $email1 = $logtab{$login}{email};
   $prml = strapp $prml, "email=$email1";
   $password = $logtab{$login}{password};
   $prml = strapp $prml, "password=$password";
   $prml = strapp $prml, "acode=$acode";
   $logo = adjusturl "http://www.hotdiary.com/images/newhdlogo.gif";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "vdomain=www.hotdiary.com";
   $banner = adjusturl "<a href=\"http://www.hotdiary.com\" target=_main><IMG SRC=\"http://www.hotdiary.com/images/dotcombanner.gif\" BORDER=0></a>";
   $prml = strapp $prml, "banner=$banner";
   $prml = strapp $prml, "func=lostpass";
   $title = "HotDiary";
   $prml = strapp $prml, "title=$title";
   $activationmsg = 'Your account activation code is ' . $acode . '. If you are reading this email in a web-enabled browser and are able to click on the link, please click <a href="http://www.hotdiary.com/cgi-bin/execverifyacc.cgi?login=' . $login . '&acode=' . $acode . '">here</a>' . ' if you would like to activate your account. You only need to activate your account once. If you have already activated it previously, you need not click the activate link.' . "\n\n" . 'If you do not have a web-enabled browser, please visit http://www.hotdiary.com/activateacc.shtml to activate your account.';
   $activationmsg = adjusturl $activationmsg;
   $prml = strapp $prml, "activationmsg=$activationmsg";
   parseIt $prml;
   $esubject = "$title Account Information";

   if ($logtab{$login}{email} eq "") {
      status "Our records indicate that there is no email address for this account $login in our database. If you are the owner of this login, and would like to use HotDiary, the only way to retreive your lost account information is to <a href=\"contact_us.html\">contact us</a> and specify your login and email address. We will be happy to record your email address in our database and respond to you with a confirmation. As soon as you receive this confirmation, you can retreive your lost account using this Forgot Password utility.";
      exit;
   }

   if (("\U$logtab{$login}{'email'}" eq "\U$email") ||
       ($logtab{$login}{'email'} eq "")) {
      #qx{echo \"$msg\" > $ENV{HDHOME}/tmp/forgotpasswd$$};
      #qx{mail -s \"Your HotDiary Member Account\" $email < $ENV{HDHOME}/tmp/forgotpasswd$$};
      $email1 = $logtab{$login}{email};
      if (!(notEmailAddress $email1)) {
         system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/lostpasswd-$login.html -s \"$esubject\" -e \"\" -t \"$email1\" -F rhsup\@hotdiary.com";
         status("Your member account information has been mailed to $email1. After you receive the email, click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login. <p><i>Please note, that we do mention the email address as above, if the email address you enter does not match our records. In other words, anyone else who knows your login, cannot retrieve your email address by using this utility.</i>");
      } else {
         status "Your email address in our records is not valid. Please <a href=\"http://www.hotdiary.com/contact_us.html\">contact</a> our customer service to validate your account information.";
         exit;
      }
      #qx{rm -f $ENV{HDHOME}/tmp/forgotpasswd$$};
   } else {
      #qx{echo \"$msg\" > $ENV{HDHOME}/tmp/forgotpasswd$$};
      #qx{mail -s \"Your HotDiary Member Account\" $logtab{$login}{'email'} < $ENV{HDHOME}/tmp/forgotpasswd$$};
      $email1 = $logtab{$login}{email};
      hddebug "esubject = $esubject";
      if (!(notEmailAddress $email1)) {
         hddebug "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/lostpasswd-$login.html -s \"$esubject\" -e \"\" -t \"$email1\" -F rhsup\@hotdiary.com";
         system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/lostpasswd-$login.html -s \"$esubject\" -e \"\" -t \"$email1\" -F rhsup\@hotdiary.com";
         #qx{rm -f $ENV{HDHOME}/tmp/forgotpasswd$$};
         status("Your login ($login), password and activation code have been sent to the email address mentioned in your profile. If you haven't yet activated your account, you may need to <a href=\"/activateacc.shtml\">activate</a> it. If you have already activated your account, click <a href=\"/signin.shtml\" TARGET=\"_parent\">here</a> to login.");
      } else {
         status "Your email address in our records is not valid. Please <a href=\"http://www.hotdiary.com/contact_us.html\">contact</a> our customer service to validate your account information.";
         exit;
      }
   }
}

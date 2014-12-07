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
# FileName: sendpage.cgi 
# Purpose: it sends a pager message.
# Creation Date: 06-10-98
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

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("sendpage.cgi example");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   $to = $input{'to'};
   $pagertype = $input{'pt'};
   if ("\L$pagertype" eq "\LSkytel Pager") {
      if (notSkyTelPin trim $to) {
         status("The $pagertype number you have entered ($to) must be a valid $pagertype pin (7 numeric digits). For instance \"1234567\" is a valid format. Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LAirTouch Pager") {
      if (notAirTouchPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (11 numeric digits). For instance \"1-408-456-1234\" is a valid format. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LPageMart Pager") {
      if (notPageMartPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (either a 7 digit numeric PIN or a 10 digit $pagertype \"Assured Messaging\" phone number which is also the PIN). Note that 7 digit numeric PINs are used for traditional (one-way) paging using $pagertype. For instance either \"408-456-1234\" or \"456-1234\", both are valid formats. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this. <p>If you are trying to page a subscriber and you do not know the recipient's PIN, you must contact that individual to gain access to his or her PIN. $pagertype does not give out subscriber's PINs.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LNextel Pager") {
      if (notNextelPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (10 digit numeric PIN). For instance \"408-456-1234\" is a valid format. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LOther Pager") {
      if (notEmailAddress trim $to) {
         status("The Other Pager type only supports pager email addresses. Please enter a valid email address for your pager, before using this feature. <p>If you are new to this feature, note that Other Pager can be used with any mobile device that is capable of receiving email. For instance, you can use a cellphone, palm device or a pager. <p>You may need to verify if your mobile device supports email with your carrier service representative.");
         exit;
      }
   }
   #print "to = ", $to, "\n";
   #print "pagertype = ", $pagertype, "\n";
   $thispage = $input{'thispage'};
   #print "thispage = ", $thispage, "\n";

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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.");
              exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already timed out. However, all your personal information is completely intact.");
    exit;
   }
   $sesstab{$biscuit}{'time'} = time();

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = "";
   $prml = strapp $prml, "label=HotDiary Send Pager Message";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "to=$to";
   $prml = strapp $prml, "thispage=$thispage";
   $prml = strapp $prml, "pagertype=$pagertype";
   $urlcgi = buildurl("execsendmsg.cgi");
   $prml = strapp $prml, "actioncgi=$urlcgi";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/sendpage.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/sendpage-$$.html";
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/sendpage.html"; 
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/sendpage-$$.html"; 

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

# need to add a counter to keep track of pagers.
   
# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

#!/usr/bin/perl

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

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   hddebug "hdmail";
  
   $logi = $ARGV[0];
   $login = $ARGV[1];
   hddebug "login = $login";
   hddebug "logi = $logi";

   
   #$mailrand = rand 600;
   #if ($mailrand < 300) {
   #   $mailrand = 300; 
   #}

   #$mailrand = 1;
   $rand = 1000 + rand 6000;
   $rand = 300 + $rand % 300;
   hddebug "Sleeping $rand seconds before sending mail to $logtab{$logi}{'email'}";
   qx{sleep $rand};

   $emsg = "Dear $logtab{$logi}{'fname'},\n";
   $mname = $logtab{$login}{'fname'} . " " . $logtab{$login}{'lname'};
   $useremail = $logtab{$login}{'email'};
   $emsg .= "You have been invited by $mname to join http://www.hotdiary.com! If you would like to contact $mname directly, please send an email to $mname at $useremail.\n";

   $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
   $emsg .= "\nName: $logtab{$logi}{'fname'} $logtab{$logi}{'lname'}\n";
   $emsg .= "Login: $logtab{$logi}{'login'}\n";
   $emsg .= "Password: $logtab{$logi}{'password'}\n\n";
   $emsg .= "Regards,\nHotDiary Inc.\n\n";
   $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Collaborative Internet Organizer\n";
   qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/import-$logi-reginviteletter$$};

   $email = $logtab{$logi}{'email'}; 
   hddebug "email = $email";
   qx{/bin/mail -s \"Invitation From $mname\" $email < $ENV{HDHOME}/tmp/import-$logi-reginviteletter$$};
   hddebug "sent mail";
}


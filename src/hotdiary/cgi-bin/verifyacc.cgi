#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: verifyacc.cgi
# Purpose: top html for cal mgmt tools
# This program is invoked by newindex.html file
# Creation Date: 09-10-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

$jp = $input{jp};

$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

$hddomain = $ENV{HDDOMAIN};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


# bind login table vars

   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };


$login = trim $input{login};
$login = "\L$login";
if ($login eq "") {
   status("Please specify a non-empty login name.");
   exit;
}

$acode = trim $input{acode};
$acode = "\L$acode";

if (!exists $logtab{$login}) {
   status "Invalid login ($login). Please click <a href=\"/activateacc.shtml\">here</a> to enter a valid login.";
   exit;
}

$msg = "<p>To purchase a product <a href=/cgi-bin/execlistproducts.cgi?>click here</a>. <p>To download WordIt! <a href=/words>click here</a>. <p>To create a free JiveIt! Cobrand <a href=/jiveitauth.shtml>click here</a>. <p>To create a premium JiveIt! Cobrand <a href=/jiveitprofauth.shtml>click here</a>.";

if (!exists $activetab{$login}) {
   status "$login: This account is already activated. Please click <a href=\"/signin.shtml\">here</a> to login to HotDiary. $msg";
   exit;
}

if ($activetab{$login}{verified} eq "true") {
   status "$login: This account is already activated. <p>Please click <a href=\"/signin.shtml\">here</a> to login to HotDiary. $msg";
   exit;
}

if ($acode eq $activetab{$login}{acode}) {
   $activetab{$login}{verified} = "true";
   $mo = 'US $10';
   #status "$login: Your account has been successfully activated. <p><b>Please click <a href=\"/signin.shtml\">here to login</a> to HotDiary.</b> <p><i>You can win $mo almost instantly. Click <a href=\"$hddomain/links.html\">here</a> to see details!</i>";
   status "$login: Your account has been successfully activated. <p><b>Please click <a href=\"/signin.shtml\">here to login</a> to HotDiary.</b> $msg";
   exit;
} else {
   if ($acode eq $logtab{$login}{password}) {
      $m = "$acode seems to be your password, which will be required once you activate your account.";
   }
   status "$login: The activation code you entered ($acode) is incorrect. The activation code should have been mailed to you at the time of registration to the email address you specified during the registration process. If you registered using DiaryChat, we may not have your email address. In such a case, you need to <a href=\"contact_us.html\">contact us</a> with your login and email address, so we can email your activation code to you. $m Please click <a href=\"/activateacc.shtml\">here</a> and enter a valid activation code. If you have lost your activation code and/or password, please click <a href=\"/forgotpasswd.html\">here</a> to have this information mailed to the email address you specified at the time of your registration. For additional help, please access <a href=\"/accounthelp.html\">account help information</a>.";
   tied(%activetab)->sync();
}

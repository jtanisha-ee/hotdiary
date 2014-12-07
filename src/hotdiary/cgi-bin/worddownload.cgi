#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


&ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = $input{login};
$password = trim $input{password};

if (!exists($logtab{$login})) {
   status("Invalid login ($login). Please enter a valid member login. <b>We encourage you to register with HotDiary. This will help support a number of free community software download initiatives.</b> Note that for downloading WordIt! you do not need to activate your account. If you haven't yet registered with HotDiary, please click <a href=\"/quikregister.html\">here</a> to register. <!-- If you still prefer not registering, you can click <a href=/cgi-bin/execwordnoauthdwnld.cgi>here to download the file</a>. <b>After downloading, we still recommend that you <a href=/quikregister.html>register</a> with HotDiary to make use of all the useful web services it offers for free.</b> --> If you have already registered previously, you should have received an email from HotDiary that contains information about your login and password. If you have lost the information, you can always click on <a href=\"forgotpasswd.html\">forgot password</a> to have your account information emailed to you."); 
   exit;
}

if ("\L$logtab{$login}{password}" ne "$password") {
   status("Invalid password ($password). Please enter the correct password. <b>We encourage you to register with HotDiary. This will help support a number of free community software download initiatives.</b> If you haven't yet registered with HotDiary, please click <a href=\"/register.html\">here</a> to register. <!-- If you still prefer not registering, you can click <a href=/cgi-bin/execwordnoauthdwnld.cgi>here to download the file</a>. <b>After downloading, we still recommend that you <a href=/quikregister.html>register</a> with HotDiary to make use of all the useful web services it offers for free.</b> --> If you have already registered previously, you should have received an email from HotDiary that contains information about your login and password. If you have lost the information, you can always click on <a href=\"forgotpasswd.html\">forgot password</a> to have your account information emailed to you.");
   exit;
}

$copyright = $input{copyright};
if ($copyright eq "") {
   status("Please read the <a href=/words/LICENSE target=_main>LICENSE</a> notice, and then click on the Accept license checkbox. Use the browser back-button now before you proceed.");
   exit;
}

system "mkdir -p $ENV{HTTPHOME}/html/hd/words/key-$$";
system "ln -s $ENV{HDHOME}/yp/WordIt10.zip $ENV{HTTPHOME}/html/hd/words/key-$$";
system "ln -s $ENV{HDHOME}/yp/WordIt10.txt $ENV{HTTPHOME}/html/hd/words/key-$$";

$msg = "<p>Click <a href=\"$ENV{HDDOMAIN}/cgi-bin/execdolistproducts.cgi?login=$login&password=$password&copyright=$copyright\">here to purchase and download</a> the complete WordIt! English Diary that contains a <B>quarter million words</B>, only for " . 'US $5.99.';

system "$ENV{HDEXECCGI}/execcleanproducts $ENV{HTTPHOME}/html/hd/words/key-$$/WordIt10.zip 900";
system "$ENV{HDEXECCGI}/execcleanproducts $ENV{HTTPHOME}/html/hd/words/key-$$/WordIt10.txt 900";

status("$login: Congratulations! HotDiary's WordIt! English Diary is ready. Please click <a href=\"$ENV{HDDOMAIN}/words/key-$$/WordIt10.zip\">here to download diary</a> in WinZip format. The diary contains 105850 words. If your browser does not support the WinZip format, click <a href=\"$ENV{HDDOMAIN}/words/key-$$/WordIt10.txt\">here to download the plain text version</a> of the file. Depending upon the MIME application configuration in your browser, in some cases you may need to explicitly use the SHIFT+LEFTMOUSE combination to invoke the File Save dialog box. You have 15 minutes to download the diary. It will not be available for download at the end of 15 minutes. $msg");   

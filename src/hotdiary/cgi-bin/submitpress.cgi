#!/usr/bin/perl

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
# FileName: submitpress.cgi 
# Purpose: Accept a Press Release
# Creation Date: 10-15-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

# bind login table vars
   tie %newstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/newstab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'login', 'password', 'reldate', 'month', 
	'day', 'title', 'status', 'release', 'phone', 'address'] };

tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = trim $input{login};
if ($login eq "") {
   status "Please enter a non-empty member login. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}
$login = "\L$login";

if (!exists $logtab{$login}) {
   status "Member login $login does not exist. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

$password = "\L$input{password}";
if ($password ne "\L$logtab{$login}{password}") {
   status "Password $password for login $login is incorrect. Please enter a valid password. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

$entryno = "999999" . time();
$newstab{$entryno}{entryno} = $entryno;
$newstab{$entryno}{status} = "pending";
$newstab{$entryno}{login} = $login;
#$newstab{$entryno}{password} = $password;
$newstab{$entryno}{reldate} = $input{reldate};
$newstab{$entryno}{month} = $input{month};
$newstab{$entryno}{day} = $input{day};
$newstab{$entryno}{title} = $input{title};
$date = $input{month} . "/" . $input{day} . "/" . "2000";
$release = "$date -- (NewsDiary) -- Milpitas, CA -- " . $input{release};
$newstab{$entryno}{phone} = $input{phone};
if ($input{phone} ne "") {
   $release = $release . "<p>Company Phone Contact: $input{phone}";
}
$newstab{$entryno}{release} = $release;
$newstab{$entryno}{address} = $input{address};

$email = $logtab{$login}{email};

$msg = "$login: Thank you for submitting a draft of your press release. Your article will be reviewed by our press editors and subsequently published as per your request.<BR>If you have made an error in submitting this release, please use the reference ID $entryno while corresponding with us. All correspondence must be addressed to us along with your reference ID. Please allow atleast 2 hours to review articles submitted for immediate release. <BR>If we have any questions, we will contact you by email at the email address ($email) specified in your records.<BR>Your article may be selected for circulation in our monthly newsletter. <BR>While you wait for your article to show up, this is a good time to check-out all the exciting features that HotDiary has to offer for your personal and business needs. Click <a href=\"/index.html\">here</a> to check out HotDiary.";

system "echo \"$msg\" > $ENV{HDHOME}/tmp/press-$entryno";
system "mail -s \"Press Release Submitted\" rhsup\@hotdiary.com < $ENV{HDHOME}/tmp/press-$entryno";
status $msg; 

tied(%newstab)->sync();

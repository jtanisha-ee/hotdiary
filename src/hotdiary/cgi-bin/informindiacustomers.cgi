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
# FileName: informcustomers.cgi
# Purpose: This script is used to mail newsletters to members
# Creation Date: 04-03-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# Initialize the file name that contains the email message to be sent
# to all the hotdiary members.

$mfile = "$ENV{HDHOME}/letters/someletter";
$ttime = localtime(time());
$subject = "HotDiary Newsletter - $ttime";

if (!(-f $mfile)) {
   print "$mfile does not exist.\n";
   exit;
}

print "WARNING: $mfile will be mailed to thousands of users! Please press CTRL-C to abort!\n";
print "WARNING: Will sleep for 30 seconds before sending mail messages...\n";

qx{sleep 30};

print "...Waking up\n";

$cntr = 0;
foreach $account (sort keys %logtab) {
  $msg = "";
  #$account =~ s/\n//g;
  $account =~ s/\r//g;
  if ($logtab{$account}{'informme'} eq "CHECKED") {
     $email = $logtab{$account}{'email'};
     $country = $logtab{$account}{'country'};
     $country = "\U$country";
     if (!($country =~/INDIA/)) {
        next; 
     }
     if ($email eq "") {
        next;
     }
     $msg = "Dear $logtab{$account}{'fname'},\n\n";
     $msg .= "You recently registered with HotDiary.com. If you have forgotten your password, you can use your login ($logtab{$account}{'login'}) and email ($logtab{$account}{'email'}) to get your password, at our website, by clicking on the lost password link on the main page.\n\n";
     $msg .= "As a token of our appreciation, you will be paid the amount proportional to the number of people you have referred including your own registration, as per the rules mentioned in the initial letter you received. Currently we are facing a huge backlog, but we haven't forgotten you, and you will soon be re-imbursed the amount we have promised.\n\n";
     $msg .= "In the meantime make sure your current address is correct in your profile, by login in to HotDiary and updating your home address.\n\n";
     $msg .= "Note that you can continue referring as many people as you want, and do let us know the email addresses of the people you have referred, and also your own member login, so we know who you are. Everytime you refer a new person, you earn money! And you can tell this to all your friends who do not have internet access, and they may be very happy to hear this!\n\n";
     $msg .= "You have received this email, because you have mentioned your country as India in your profile, and checked the informme box while registering with HotDiary.\n\n";
     $msg .= "Visit us soon at http://www.hotdiary.com. We always have new and exciting features added to our product.\n\n";
     $msg .= "Regards,\n\nBob Palmer,\nCustomer Support,\nHotDiary Inc.\n";
     qx{echo \"$msg\" > /var/tmp/indialetter$$};
     print $msg;
     $cntr += 1;
     print "Sending email to $email...";
     qx{sleep 1};
     system "/bin/mail -s \"$subject\" \"$email\" < /var/tmp/indialetter$$";
     print "...Done.\n";
  } 
}

print "Sent email to $cntr members\n";

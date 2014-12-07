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
# FileName: informcustomers.cgi
# Purpose: This script is used to mail newsletters to members
# Creation Date: 04-03-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
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

$mfile = "$ENV{HDHOME}/letters/newsletter-shockthewave.html";
$subject = "HotDiary.Com and ShockTheWave.Com - May. 2000";

if (!(-f $mfile)) {
   print "$mfile does not exist.\n";
   exit;
}

print "WARNING: $mfile will be mailed to thousands of users! The subject is $subject. Please press CTRL-C to abort!\n";
print "WARNING: Will sleep for 30 seconds before sending mail messages...\n";

qx{sleep 3};

print "...Waking up\n";

$cntr = 0;
foreach $account (sort keys %logtab) {
  #$account =~ s/\n//g;
  $account =~ s/\r//g;
  if ($logtab{$account}{'informme'} eq "CHECKED") {
     $email = $logtab{$account}{'email'};
     if ($email eq "") {
        next;
     }
     $cntr += 1;
     print "Sending shockthewave-newsletter-May-$$-$account.html to $email...";
     qx{sleep 3};
     system "echo \"$email\" >> $mfile.out"; 
     #system "/bin/mail -s \"$subject\" \"$email\" < $mfile";
     $prml = "";
     $prml = strapp $prml, "template=$mfile";
     $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/shockthewave-newsletter-May-$$-$account.html";
     $prml = strapp $prml, "login=$account";
     tie %moneytab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/moneytab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login', 'account', 'comment', 'approved'] };     
     if (exists $moneytab{$account}) {
        $reward = $moneytab{$account}{account};
        if ($reward ne "") {
           $damount = $reward / 100;
           $str = "$damount";
        } else {
           $str = '0.00';
        }       
     } else {
        $str = '0.00';
     }
     $prml = strapp $prml, "reward=$str";
     $mail1 = $logtab{$account}{email};
     $prml = strapp $prml, "email=$mail1";
     parseIt $prml;     
     system "metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/shockthewave-newsletter-May-$$-$account.html -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
     #system "metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
     #system "rm -f $ENV{HDHOME}/tmp/shockthewave-newsletter-May-$$-$account.html";
     print "...Done.\n";
  } 
}

print "Sent email to $cntr members\n";

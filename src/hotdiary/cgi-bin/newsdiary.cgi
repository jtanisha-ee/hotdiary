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


# bind master table vars
   tie %mastertab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['email', 'login', 'password', 'busname', 'suite', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'fax',
        'bphone', 'url', 'contacted', 'category0', 'category1',
        'category2', 'category3', 'category4', 'yearsinbusiness',
        'numemp', 'annualrev', 'held', 'symbol', 'description',
        'companycontact', 'email2', 'areacodes', 'numareacodes' ]};



# Initialize the file name that contains the email message to be sent
# to all the hotdiary members.

$mfile = "$ENV{HDHOME}/letters/newsdiary.html";
$subject = "NewsDiary Article";

if (!(-f $mfile)) {
   print "$mfile does not exist.\n";
   exit;
}

print "WARNING: $mfile will be mailed to thousands of users! The subject is $subject. Please press CTRL-C to abort!\n";
print "WARNING: Will sleep for 30 seconds before sending mail messages...\n";

qx{sleep 3};

print "...Waking up\n";

$cntr = 0;
foreach $email (sort keys %mastertab) {
  $email =~ s/\r//g;
  if ($email eq "") {
     next;
  }
  $email = trim $email;
  if ($mastertab{$email}{contacted} ne "") {
     next;
  }
  $login = $mastertab{$email}{login};
  $cntr += 1;
  print "Sending newsdiary-Apr-$$-$login.html to $email...";
  qx{sleep 3};
  system "echo \"$email\" >> $mfile.out"; 
  $prml = "";
  $prml = strapp $prml, "template=$mfile";
  $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/newsdiary-Apr-$$-$login.html";
  $prml = strapp $prml, "login=$login";
  $password = $mastertab{$email}{password};
  $prml = strapp $prml, "password=$password";
  $url = $mastertab{$email}{url};
  $prml = strapp $prml, "url=$url";
  $comment = $mastertab{$email}{comment};
  $prml = strapp $prml, "comment=$comment";
  parseIt $prml;     
  system "metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/newsdiary-Apr-$$-$login.html -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
  $mastertab{$email}{contacted} = "newsdiary";
  #tied(%mastertab)->sync();
  print "...Done.\n";
}

print "Sent email to $cntr members\n";

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

# bind master table vars
   tie %etab, 'AsciiDB::TagFile',
   DIRECTORY => "/u4/accounts/contacted/etab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['email', 'contacted' ]};

# Initialize the file name that contains the email message to be sent
# to all the hotdiary members.

$mfile = "$ENV{HDHOME}/letters/newspublish.html";
$subject = "NewsDiary Article";

if (!(-f $mfile)) {
   print "$mfile does not exist.\n";
   exit;
}

print "WARNING: $mfile will be mailed to thousands of users! The subject is $subject. Please press CTRL-C to abort!\n";
print "WARNING: Will sleep for 30 seconds before sending mail messages...\n";

qx{sleep 3};

print "...Waking up\n";

$elist = qx{cat /u4/accounts/emix-a.txt};
(@elist) = split '\n', $elist;

$cntr = 0;
foreach $email (@elist) {
  $email =~ s/\r//g;
  if ($email eq "") {
     next;
  }
  $email = trim $email;
  if (!exists $etab{$email}) {
     $etab{$email}{email} = $email; 
  }
  if ($etab{$email}{contacted} ne "") {
     next;
  }
  $cntr += 1;
  print "$cntr: Sending newspublish.html to $email...";
  qx{sleep 1};
  system "echo \"$email\" >> $mfile.out"; 
  $prml = "";
  $prml = strapp $prml, "template=$mfile";
  $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/newspublish-$$.html";
  $prml = strapp $prml, "email=$email";
  parseIt $prml;     
  system "metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/newspublish-$$.html -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
  $etab{$email}{contacted} = "newspublish";
  print "...Done.\n";
}

print "Sent email to $cntr members\n";
tied(%etab)->sync();

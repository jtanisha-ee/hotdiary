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
# FileName: myreward.cgi
# Purpose: increment money in my rewards
# Creation Date: 01-08-2000
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;


# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "myreward.cgi";

   $member = $input{member}; 
   $member =~ s/\"//g;

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
         'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

tie %moneytab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/moneytab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['login', 'account', 'comment', 'approved'] };    

$referer = $ENV{HTTP_REFERER};
$remoteaddr = $ENV{REMOTE_ADDR};
hddebug "HotDiary Banner Clicked ($member at $remoteaddr): $referer";
if ($member ne "") {
   if (!exists $logtab{$member}) {
      status "Please specify a valid member login. $member is not a valid login";
      exit;
   }
}

$fchar = substr $member, 0, 1;
$alphaindex = $fchar . '-index';

if (exists $logtab{$member}) {

   $fchar = substr $member, 0, 1;
   $malphaindex = $fchar . "-index";
   if ( ! -d "$ENV{HDDATA}/$malphaindex/$member/uniquetab" ) {
      system "mkdir -p $ENV{HDDATA}/$malphaindex/$member/uniquetab";
   }

   $moneytab{$member}{'login'} = $member;

   tie %uniquetab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/$malphaindex/$member/uniquetab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['remoteaddr', 'lastupdate'] };    

   ($a, $b, $c, $d) = split '\.', $remoteaddr;
   $remoteaddr = $a . '.' . $b . '.' . $c;
   $currtime = time();
   if (exists $uniquetab{$remoteaddr}) {
      $lastupdate = $uniquetab{$remoteaddr}{'lastupdate'};
      if ( ($currtime - $lastupdate) > ( 86400 * 15 ) ) {
         $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 0.1;
      } else {
         #$moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 0;
         #status "Too many attempts to click banner from the same originating site. This message has been sent to hotdiary.com for further investigation.";
         #exit;
      }
   } else {
      if ($member eq "sergio.panseri") {
         $uniquetab{$remoteaddr}{'remoteaddr'} = $remoteaddr; 
         $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 0.1;
      } else { 
         $uniquetab{$remoteaddr}{'remoteaddr'} = $remoteaddr; 
         $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 0.2;
      }
   }
   $uniquetab{$remoteaddr}{'lastupdate'} = $currtime;
}

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_reward.html";
$prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/reward-$biscuit-$$.html";
$prml = strapp $prml, "redirecturl=http://www.hotdiary.com";       
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDREP}/$alphaindex/$login/reward-$biscuit-$$.html";

## not required
#if ($referer =~ /onlineorganizing/) {
#   print "Location: http://www.hotdiary.com\n\n";
#} else {
#   print "Location: http://www.redbasin.com\n\n";
#}

if (exists $logtab{$member}) {
   tied(%moneytab)->sync();
   tied(%uniquetab)->sync();
}

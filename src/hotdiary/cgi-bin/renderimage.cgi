#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: renderimage.cgi
# Purpose: This program is used for rendering async images
# 
# Creation Date: 04-22-99
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use tp::tp;
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use LWP::UserAgent;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   $member = $input{'member'};

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
   hddebug "$member Reading Newsletter 2003: $referer";
   #if ($member ne "") {
      #if (!exists $logtab{$member}) {
         #status "Please specify a valid member login. $member is not a valid login";
         #exit;
      #}
   #}
 
   $fchar = substr $member, 0, 1;
   $malphaindex = $fchar . '-index';

   if (exists $logtab{$member}) {
      if ( ! -d "$ENV{HDDATA}/$malphaindex/$member/uniquetab" ) {
         system "mkdir -p $ENV{HDDATA}/$malphaindex/$member/uniquetab";
      }
   
      $moneytab{$member}{'login'} = $member;
   
      tie %uniquetab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/$malphaindex/$member/uniquetab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['remoteaddr', 'lastupdate'] };
   
      $remoteaddr = $ENV{REMOTE_ADDR};
      ($a, $b, $c, $d) = split '\.', $remoteaddr;
      $remoteaddr = $a . '.' . $b . '.' . $c;
      $currtime = time();
      if (exists $uniquetab{$remoteaddr}) {
         $lastupdate = $uniquetab{$remoteaddr}{'lastupdate'};
         if ( ($currtime - $lastupdate) > 86400 ) {
            $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 10;
         } else {
            $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 1;
         }
      } else {
         $uniquetab{$remoteaddr}{'remoteaddr'} = $remoteaddr;
         $moneytab{$member}{'account'} = $moneytab{$member}{'account'} + 10;
      }
      $uniquetab{$remoteaddr}{'lastupdate'} = $currtime;
   }

   print "Content-Type: image/gif";
   print "\n\n";
   $ua = LWP::UserAgent->new;
   #$request = HTTP::Request->new(GET => 'http://www.hotdiary.com/images/newhdlogo.gif');
   $request = HTTP::Request->new(GET => 'http://www.hotdiary.com/images/nothing.gif');
   $response = $ua->request($request);
   if ($response->is_success) {
      print $response->content;
   } else {
      status "Bad luck this time";
   }
}

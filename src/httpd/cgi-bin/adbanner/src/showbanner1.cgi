#!/usr/bin/perl

#
# (C) Copyright 2000 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

# FileName: showbanner.cgi
# Purpose: decrement money in customer account and show banner
# Creation Date: 03-26-2000

require "cgi-lib.pl";
#require 'cookie.lib';
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   ##hddebug "showbanner.cgi";

   $member = $input{member}; 
   if ($member eq "") {
      status "This banner is invalid. The member name is missing.";
      exit;
   }
   if ($member eq "hotdiary_shockthewave") {
      $member = "hotdiary";
   }
   $page = $input{page};
   if ($page eq "") {
      status "This banner is invalid. The page number is missing.";
      exit;
   }
   #hddebug "Phase 1";

# bind login table vars
   tie %customers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/customers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'banner', 'account', 
        'impression_cost', 'click_cost', 'policy', 
         'street', 'city', 'state', 'zipcode', 
	'country', 'email', 'url', 'category', 'password'] };

  if (! -d "bannerama/publishers/$member") {
     system "mkdir bannerama/publishers/$member";
  }
  #hddebug "Phase 2";

# bind publisher table vars
  # bind login table vars
   tie %publishers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'click_reward',
             'street', 'city', 'state', 'zipcode',
             'country', 'phone', 'email', 'url', 'category',
             'password', 'pages', 'click_commission'] };

# bind page table vars
   tie %pagetab, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers/$member",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['page', 'referer', 'customer'] };

$referer = $ENV{HTTP_REFERER};

$pagetab{$page}{page} = $page;
$pagetab{$page}{referer} = $referer;

$remoteaddr = $ENV{REMOTE_ADDR};
($a, $b, $c, $d) = split '\.', $remoteaddr;
$remoteaddr = $a . '.' . $b . '.' . $c;

$page = $remoteaddr . $page;

#hddebug "HotDiary Banner Displayed ($member at $remoteaddr): $referer";
  #hddebug "Phase 3";

$pagetab{$page}{page} = $page;
$pagetab{$page}{referer} = $referer;

$banner = "";
#foreach $customer (sort keys %customers) {
(@cust) = sort keys %customers;
  #hddebug "Phase 4";
while (1) {
   $rand = rand ($#cust + 1);
   $rand = $rand % ($#cust + 1); 
   $customer = $cust[$rand];

   $customer = trim $customer;
   #hddebug "publisher's category = $publishers{$member}{category}";
   #hddebug "customer's category = $customers{$customer}{category}";
   #if ($publishers{$member}{category} ne $customers{$customer}{category}) {
   #      hddebug "Phase 5";
   #   next;
   #}
   #hddebug "customer = $customer";
   if ($customers{$customer}{policy} eq "impression") {
      $impression_cost = $customers{$customer}{impression_cost};
      #hddebug "impression_cost = $impression_cost";
      $rate = ($impression_cost * 100) / 1000;
      #hddebug "rate = $rate";
      if ( ($customers{$customer}{account} - $rate) > 0 ) {
	 $account = $customers{$customer}{account};
         $customers{$customer}{account} = $account - $rate;
         $banner = $customers{$customer}{banner};
         #tied(%customers)->sync();
         $pagetab{$page}{customer} = $customer;
         #hddebug "banner = $banner";
         #hddebug "account balance = $customers{$customer}{account}";
         last;
      } else {
         next;
      }
   }
}

if ($banner eq "") {
   $banner = "http://www.hotdiary.com/images/banner9.gif";
}

#print "Content-Type: text/html";
#print "\n\n";
#&SetCookies('customer', $customer);
print "Content-Type: image/gif";
print "\n\n";
$ua = LWP::UserAgent->new;
#hddebug "banner = $banner";
$request = HTTP::Request->new(GET => "$banner");
$response = $ua->request($request);
  #hddebug "Phase 6";
if ($response->is_success) {
   print $response->content;
} else {
   status "Customer's banner is currently not operational.";
}

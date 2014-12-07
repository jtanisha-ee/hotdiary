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

# FileName: showsite.cgi
# Purpose: When visitor clicks on banner, we need to redirect to customer site
# Creation Date: 04-02-2000

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "showsite.cgi";

   #&GetCookies($cookie_name);
   #$value = $cookie_name{customer};
   #hddebug "customer = $value";

   $member = $input{member}; 
   if ($member eq "") {
      status "This banner is invalid. The member name is missing.";
      exit;
   }
   $page = $input{page};
   if ($page eq "") {
      status "This banner is invalid. The page number is missing.";
      exit;
   }

# bind login table vars
   tie %customers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/customers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'banner', 'account', 
        'impression_cost', 'click_cost', 'policy', 
         'street', 'city', 'state', 'zipcode', 
	'country', 'email', 'url', 'category', 'password'] };

# bind publishers table vars
   tie %publishers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'click_reward',
             'street', 'city', 'state', 'zipcode',
             'country', 'phone', 'email', 'url', 'category',
             'password', 'pages', 'click_commission'] };

if ($member eq "hotdiary_shockthewave") {
   $member = "hotdiary";
}


if (! -d "bannerama/publishers/$member") {
   system "mkdir bannerama/publishers/$member";
}

# bind page table vars
   tie %pagetab, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers/$member",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['page', 'referer', 'customer'] };

$remoteaddr = $ENV{REMOTE_ADDR};
($a, $b, $c, $d) = split '\.', $remoteaddr;
$remoteaddr = $a . '.' . $b . '.' . $c;
$pg = $remoteaddr . $page;

if (exists $pagetab{$pg}) {
   $customer = $pagetab{$pg}{customer};
} else {
   $customer = $pagetab{$page}{customer};
}

$page = $pg;

$referer = $ENV{HTTP_REFERER};
#hddebug "HotDiary Banner Clicked ($member at $remoteaddr): $referer";

if (!exists $pagetab{$page}) {
   status "This banner is invalid.";
   exit;
}

if ( ($referer ne "") && ($pagetab{$page}{referer} ne "") && ($pagetab{$page}{referer} ne $referer) && ($page eq $pagetab{$page}{page}) ) {
   status "This banner is invalid. There is a possibility that the same page number is being used on two different pages of the site.";
   exit;
}

$banner = "";

##hddebug "customer = $customer";
#hddebug "member = $member";
$click_commission = $publishers{$member}{click_commission};
#hddebug "click_commission = $click_commission";
$publishers{$member}{click_reward} += $click_commission;
tied(%publishers)->sync();

if ($customer eq "shockthewave") {
   status "This customer has been discontinued. We apologize for the inconvenience. Click <a href=\"http://www.hotdiary.com/\">here</a> to go back to home.";
   exit;
}

if (exists $customers{$customer}) {
   if ($customers{$customer}{policy} eq "click") {
      $customers{$customer}{account} -= $customers{$customer}{click_cost};   
      #hddebug "customer account balance = $customers{$customer}{account}";
      tied(%customers)->sync();
   }
}

if (exists $customers{$customer}) {
   $url = adjusturl $customers{$customer}{url};
} else {
   $url = "http://www.hotdiary.com";
}
print "Location: $url\n\n";

#$prml = "";
#$prml = strapp $prml, "template=templates/redirect_url.html";
#$prml = strapp $prml, "templateout=/tmp/redirect_url-$$.html";
#$prml = strapp $prml, "redirecturl=$url";
#parseIt $prml;

#hddebug "Customer clicked on Bannerama banner for $customer and displaying site $url subsequently.";

#if (-f "/tmp/redirect_url-$$.html") {
#   system "cat templates/content.html";
#   system "cat /tmp/redirect_url-$$.html";
#} else {
#   status "The ad banner could not connect to the sponsor's site. Please try again later. We apologize for the inconvenience this has caused you.";   
#}

#!/usr/bin/perl

require "cgi-lib.pl";
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

use LWP::UserAgent;

&ReadParse(*input);

$member = $input{member};
$url = $input{url};
if ( (!($url =~ /hotdiary/)) && (!($url =~ /mydowntown/)) 
     && (!($url =~ /portalserver/)) && (!($url =~ /hotindia/))
     && (!($url =~ /1800calendar/)) && (!($url =~ /redbasin/))
   ) {
   $member = "hotdiary";
   $url = "http://www.hotdiary.org";
}

tie %linktab, 'AsciiDB::TagFile',
 DIRECTORY => "$ENV{HDDATA}/linktab",
 SUFIX => '.rec',
 SCHEMA => {
 ORDER => ['member', 'clicks', 'url'] };

system "mkdir -p $ENV{HDDATA}/linktab/$member";

tie %refertab, 'AsciiDB::TagFile',
 DIRECTORY => "$ENV{HDDATA}/linktab/$member",
 SUFIX => '.rec',
 SCHEMA => {
 ORDER => ['ip', 'visits'] };

$referer = $ENV{HTTP_REFERER};

$ip = $ENV{REMOTE_ADDR};
$refertab{$ip}{ip} = $ENV{REMOTE_ADDR};
$refertab{$ip}{visits} = $refertab{$ip}{visits} + 1;

hddebug "Sending HotDiary visitor from $referer($ENV{REMOTE_ADDR}) to $url hosted by $member";

$linktab{$member}{member} = $member;
$linktab{$member}{clicks} += 1;
$linktab{$member}{url} = $url;

print "Location: $url\n\n";

tied(%linktab)->sync();
tied(%refertab)->sync();

#if ($url =~ /webmasterportal/) {
#   hddebug "came here";
#   $ua = LWP::UserAgent->new;
   
#   $request = HTTP::Request->new(GET => "$url");
#   $response = $ua->request($request);
#   if ($response->is_success) {
#      print $response->content;
#   } else {
#      status "Bad luck this time";
#   }
#} else {
   #system "cat /var/tmp/adbanner-$rtime-$$";
#}


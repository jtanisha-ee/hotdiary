#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


require "cgi-lib.pl";
use tp::tp;
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
#use LWP::UserAgent;


# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  

&ReadParse(*input);

$site = trim $ENV{HTTP_REFERER};
$site = "\L$site";
$addr = trim $ENV{REMOTE_ADDR};
$uagent = trim $ENV{HTTP_USER_AGENT};
if ( ($site eq "") || ($site =~ /hotdiary/) ) {
   hddebug "HTTP_REFERER disabled or from hotdiary.com ($addr) - $uagent";
} else {
   hddebugtraffic "Redbasin.Com Visitor From $site ($addr) - $uagent";
}

#if ( 
     #( ($site =~ /business/) && (!($site =~ /calendar/)) ) ||
     #($site =~ /b2b/) ||
     #($site =~ /catavault/) ||
     #( ($site =~ /server/) && (!($site =~ /calendar/)) && (!($site =~ /diary/)) ) ||
     #($site =~ /bizware/) ||
     #($site =~ /crm/) ||
     #($site =~ /enterprise/) ||
     #($site =~ /corporate/) ||
     #($site =~ /intranet/) ||
     #($site =~ /middleware/) ||
     #($site =~ /java/) ||
     #($site =~ /jsp/) ||
     #($site =~ /xml/) ||
     #($site =~ /database/) ||
     #($site =~ /network/) ||
     #($site =~ /e-business/) 
   #) {
   #print "Location: http://www.redbasin.com\n\n";
#} else {
   # hdsystemcat "index1.html";
   print "Location: http://www.hotdiary.com:8080/bizware/class103\n\n";
#}

#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;
use LWP::UserAgent;


# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  

&ReadParse(*input);

$site = trim $ENV{HTTP_REFERER};
$addr = trim $ENV{REMOTE_ADDR};
$uagent = trim $ENV{HTTP_USER_AGENT};
if ( ($site eq "") || ($site =~ /hotdiary/) ) {
   hddebug "HTTP_REFERER disabled or from portalserver.net ($addr) - $uagent";
} else {
   hddebugtraffic "PortalServer.Net Visitor From $site ($addr) - $uagent";
}

system "cat $ENV{HDTMPL}/content.html";
system "cat index1.html";

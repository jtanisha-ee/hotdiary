#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: checklogin.cgi
# Purpose: Check for login existence
# 
# Creation Date: 09-24-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

$login = $input{login};
$login = "\L$login";
system "cat $ENV{HDTMPL}/content.html";
if ($login eq "") {
   print "<HTML><BODY>error</BODY></HTML>";
   exit;
}

if (!(exists $logtab{$login})) {
   print "<HTML><BODY>no</BODY></HTML>";
   exit;
}

if (exists $logtab{$login}) {
   print "<HTML><BODY>yes</BODY></HTML>";
   exit;
}

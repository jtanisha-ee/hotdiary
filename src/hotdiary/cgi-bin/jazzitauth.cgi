#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: jazzitauth.cgi
# Purpose: Authenticate Jazzit downloader
# 
# Creation Date: 08-14-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

$jp = $input{jp};

# bind login table vars

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login', 'logo', 'title', 'banner'] };
                                                       
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = $input{login};
if ($login eq "") {
   status("Please specify a non-empty login name");
   exit;
}

if (!exists($logtab{$login})) {
   status("Your $login login does not exist. Please contact us.");
   exit;
}

if (exists($parttab{$login})) {
   $parttab{$login}{title} = adjusturl $input{title};
   $parttab{$login}{logo} = adjusturl $input{logo};
   $parttab{$login}{banner} = adjusturl $input{banner};
   tied(%parttab)->sync();
}


   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };         

   $HDLIC = generateLicense();
   $lictab{$HDLIC}{partner} = $login;
   $lictab{$HDLIC}{IP} = trim $input{ip};
   $lictab{$HDLIC}{vdomain} = trim $input{vdomain};
   $lictab{$HDLIC}{HDLIC} = $HDLIC;
   tied(%lictab)->sync();
   

#$parttab{$login}{topleft} = adjusturl $input{topleft};
#$parttab{$login}{topright} = adjusturl $input{topright};
#$parttab{$login}{middleright} = adjusturl $input{middleright};
#$parttabjivetab{$login}{bottomleft} = adjusturl $input{bottomleft};
#$parttabjivetab{$login}{bottomright} = adjusturl $input{bottomright};
#$parttabjivetab{$login}{account} = 2500;
#$parttab{$login}{url} = adjusturl $input{url};

$rtime = getkeys();
$alphaindex = substr $login, 0, 1;
$alphaindex = $alphaindex . '-index';

system "mkdir -p $ENV{HDREP}/$alphaindex/$login/$rtime";


system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHREP}/$alphaindex/$login/jiveitauth-$rtime-$$.html";




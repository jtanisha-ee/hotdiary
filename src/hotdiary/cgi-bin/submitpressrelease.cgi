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
# FileName: submitpressrelease.cgi 
# Purpose: Accept a Press Release
# Creation Date: 10-15-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

   hddebug "submitpressrelease.cgi";

tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = trim $input{login};
if ($login eq "") {
   status "Please enter a non-empty member login. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}
$login = "\L$login";

if (!exists $logtab{$login}) {
   status "Member login $login does not exist. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

$password = "\L$input{password}";
if ($password ne "\L$logtab{$login}{password}") {
   status "Password $password for login $login is incorrect. Please enter a valid password. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

# bind invoicetab table vars
   tie %invoicetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/invoicetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['counter', 'index' ] };

   $firstname = $logtab{$login}{fname};
   $lastname = $logtab{$login}{lname};
   $street = $logtab{$login}{street};
   $city = $logtab{$login}{city};
   $state = $logtab{$login}{state};
   $zipcode = $logtab{$login}{zipcode};
   $country = $logtab{$login}{country};
   $email = $logtab{$login}{email};

   $invoice = $invoicetab{counter}{index};
   $invoice = $invoice + 1;
   $invoicetab{counter}{index} = $invoice;
   tied(%invoicetab)->sync();

   $logo = "http://www.hotdiary.com/images/newhdlogo.gif";

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }     

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';
   system "mkdir -p $ENV{HDHREP}/$alpha/$login";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/hdcreditcard.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/hdcreditcard-$$.html";    
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "firstname=$firstname";
   $prml = strapp $prml, "lastname=$lastname";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "email=$email";
   $prml = strapp $prml, "invoicenum=$invoice";
   $prml = strapp $prml, "x_description=Press Release To NewsDiary";
   $prml = strapp $prml, "label=Press Release To NewsDiary";
   $prml = strapp $prml, "label1=Submit Press Release To NewsDiary";
   $prml = strapp $prml, "amount=100";
   $prml = strapp $prml, "logo=$logo";
 
   parseIt $prml;  

   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDHREP}/$alpha/$login/hdcreditcard-$$.html";

   tied(%newstab)->sync();

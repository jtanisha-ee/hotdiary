#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

## processadspace.cgi

use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


&ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind invoicetab table vars
   tie %invoicetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/invoicetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['counter', 'index' ] };

$login = $input{login};
$password = $input{password};

if (!exists($logtab{$login})) {
   status("Invalid login. Please enter a valid member login. If you haven't yet registered with HotDiary, please click <a href=\"/register.html\">here</a> to register."); 
   exit;
}

if ("\L$logtab{$login}{password}" ne "$password") {
   status("Invalid password. Please enter the correct password.");
   exit;
}



$prml = "";
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
$prml = strapp $prml, "firstname=$firstname";
$prml = strapp $prml, "login=$login";
$prml = strapp $prml, "lastname=$lastname";
$prml = strapp $prml, "street=$street";
$prml = strapp $prml, "city=$city";
$prml = strapp $prml, "state=$state";
$prml = strapp $prml, "zipcode=$zipcode";
$prml = strapp $prml, "country=$country";
$prml = strapp $prml, "invoicenum=$invoice";
$prml = strapp $prml, "email=$email";
$prml = strapp $prml, "password=$password";


$alphaindex = substr $login, 0, 1;
$alphaindex = $alphaindex . '-index';


$prml = strapp $prml, "template=$ENV{HDTMPL}/processadspace.html";
$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/processadspace-$$.html";

parseIt $prml;

#system "/bin/cat $ENV{HDTMPL}/content.html\n\n";
#system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/processadspace.html";
hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/processadspace-$$.html";



#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

## selectproduct.cgi

## cardprocess.html is being used by processwordit.cgi program.
## please update the program for wordit when you make changes to this file.
## this program calls transact.dll which in turn calls proctrans.cgi to
## process the software purchase on hotdiary.

use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


&ReadParse(*input);


$num = $input{num};

for ($i =1; $i <= $num; $i = $i + 1) {
   $j = "submit" . $i;
   $submit = $input{$j};
   if ($submit ne "") {
	last;
   }
}

$entryno = $i;

# bind prodtab table vars
   tie %prodtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/prodtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'prodtitle', 'prodprice', 'proddesc', 'filelink' ] };

# bind invoicetab table vars
   tie %invoicetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/invoicetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['counter', 'index' ] };

$invoice = $invoicetab{counter}{index};
$invoice = $invoice + 1;
$invoicetab{counter}{index} = $invoice;
tied(%invoicetab)->sync();

$prml = "";

$prml = strapp $prml, "firstname=";
$prml = strapp $prml, "login=";
$prml = strapp $prml, "lastname=";
$prml = strapp $prml, "street=";
$prml = strapp $prml, "city=";
$prml = strapp $prml, "state=";
$prml = strapp $prml, "zipcode=";
$prml = strapp $prml, "country=";
$prml = strapp $prml, "email=";

if (!exists $prodtab{$entryno}) {
   status("$entryno does not exist in product"); 
   exit;
}

$prodprice = $prodtab{$entryno}{prodprice};
$prodtitle = $prodtab{$entryno}{prodtitle};

$prml = strapp $prml, "amount=$prodprice";
$prml = strapp $prml, "x_description=$prodtitle";
#$prml = strapp $prml, "x_Invoice_Num=$invoice";
$prml = strapp $prml, "invoicenum=$invoice";
$custid = "$invoice-$$";
$prml = strapp $prml, "x_Cust_ID=$custid";
$prml = strapp $prml, "product=$prodtitle";

$title = split(" ", $prodtitle);

$prml = strapp $prml, "template=$ENV{HDTMPL}/cardprocess.html";
#$prml = strapp $prml, "templateout=$ENV{HDHDREP}/common/$title-$$.html";
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/$title-$$.html";

parseIt $prml;

system "cat $ENV{HDTMPL}/content.html\n\n";
system "cat $ENV{HDHOME}/tmp/$title-$$.html";

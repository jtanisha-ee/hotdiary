#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

## listproducts.cgi

use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

&ReadParse(*input);

 # bind prodtab table vars
   tie %prodtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/prodtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'prodtitle', 'prodprice', 'proddesc', 'filelink' ] };

#$remoteaddr = $ENV{REMOTE_ADDR};

 tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 
        'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

 # bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };

   
   $login = $input{login};
   $password = trim $input{password};
   $copyright = $input{copyright};

   if (!exists($logtab{$login})) {
      status "The member login ($login) you entered is invalid. If you have not yet registered, please go ahead and register with HotDiary. For your own security we advise you to <a href=/register.html>register</a> with HotDiary before you use your credit card.";
      exit;
   } 

   if ("\L$logtab{$login}{password}" ne "$password") {
      if ($activetab{$login}{acode} ne "$password") {
         status "The password ($password) you entered is invalid. If you have not yet registered, please go ahead and register with HotDiary. For your own security we advise you to <a href=/register.html>register</a> with HotDiary before you use your credit card.";
         exit;
      }
   }

   if ((!exists $activetab{$login}) || ($activetab{$login}{verified} ne "true")) {
      status "Your account is not activated. If you have not yet registered, please go ahead and register with HotDiary. For your own security we advise you to <a href=/register.html>register</a> with HotDiary before you use your credit card. If you have already registered, you need to <a href=/activateacc.shtml>activate</a> your account before you purchase a product.";
       exit;
   }

   if ($copyright eq "") {
      status "You have not checked the Agreement checkbox. Please read the agreement, and then click on the checkbox. <a href=/cgi-bin/execlistproducts.cgi>Try again.</a>";
      exit;
   }

   hddebug "Customer $login has checked the agreement checkbox, and has agreed to the terms in the agreement, by doing so.";

$num = 0;
sub numerically { $a <=> $b; }
foreach $rec (sort numerically keys %prodtab) {
$num = $num + 1;;
#if ( ($num == 8) && ($remoteaddr ne "63.194.208.213") ) {
   #break;
#}
$listproducts .= "<TR>";
$listproducts .= "<TD ALIGN=LEFT>";
$listproducts .= "<B>";
$listproducts .= "<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=2 BGCOLOR=blue WIDTH=\"100%\"><TR><TD><TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 BGCOLOR=white WIDTH=\"100%\"><TR><TD>";
$listproducts .= "<FONT FACE=Verdana SIZE=3 COLOR=f20236>$prodtab{$rec}{prodtitle}</FONT><BR>";
$listproducts .= "<FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>$prodtab{$rec}{proddesc} <BR>Price (USD) $prodtab{$rec}{prodprice}</FONT>";
$listproducts .= "</TD></TR></TABLE></TD></TR></TABLE>";

$listproducts .= "</B>";
$listproducts .= "</TD>";
$listproducts .= "<TD>";
$listproducts .= "<INPUT TYPE=HIDDEN NAME=\"entryno$num\" VALUE=\"$prodtab{$rec}{entryno}\">";
if (($prodtab{$rec}{prodtitle} ne "Home Rental Search/Listing Software") &&
    ($prodtab{$rec}{prodtitle} ne "BizWare E-Business Server")) {
   $listproducts .= "<INPUT TYPE=SUBMIT NAME=\"submit$num\" VALUE=\"Proceed To Purchase\">";
} else {
   $listproducts .= "<a href=http://www.portalserver.net:8080/download>Proceed To Purchase</a>";
}
$listproducts .= "</TD>";
$listproducts .= "</TR>";
 }

$listproducts .= "<INPUT TYPE=HIDDEN NAME=num VALUE=$num>";

$prml = "";
$listproducts = adjusturl $listproducts;
$prml = strapp $prml, "template=$ENV{HDTMPL}/purchaseproducts.html";
$prml = strapp $prml, "listproducts=$listproducts";
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/purchaseproducts-$$.html";

parseIt $prml;
system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHOME}/tmp/purchaseproducts-$$.html";

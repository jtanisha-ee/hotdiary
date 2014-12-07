#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: quadtrafauth.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 05-23-2000
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   hddebug "quadtrafauth.cgi";
# print HTML headers

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 
        'calpublish', 'referer'] };

  $login = trim $input{'login'};
  $login = "\L$login";
  $password = trim $input{'password'};

  if ($login eq "") {
     status "Empty login field. Please enter a valid non-empty login.";
     exit;
  }

  if (!exists $logtab{$login}) {
     status("The login you have entered ($login) is not a valid login. If you have not yet registered with HotDiary, register before you can use JiveIt!");
     exit;
  }

  if ("\L$password" ne "\L$logtab{$login}{'password'}") {
     status("You entered the password ($password) which is incorrect. Please enter the correct password. If you have not yet registered with HotDiary, register before you can use JiveIt!");
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


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ($logo eq "") {
      $logo = "http://www.hotdiary.com/images/newhdlogo.gif";
   } 

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/hdcreditcard.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/hdcreditcard-$$.html";    
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
   $prml = strapp $prml, "x_description=Quadruple Traffic To Your Site";
   $prml = strapp $prml, "label=Quadruple Site Traffic Booster Package";
   $prml = strapp $prml, "label1=6-Month Money Back Guarantee Site Traffic Booster Package";
   $prml = strapp $prml, "amount=500";
   $prml = strapp $prml, "logo=$logo";
 
   parseIt $prml;  

   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/hdcreditcard-$$.html";
 }

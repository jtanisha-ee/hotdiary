#!/usr/bin/perl

#
# (C) Copyright 2000 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

# FileName: showcustomerinfo.cgi
# Purpose:  show customer account
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "showcustomerinfo.cgi";


# bind login table vars
   tie %customers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/customers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'banner', 'account', 
        'impression_cost', 'click_cost', 'policy', 
	'street', 'city', 'state', 'zipcode', 
	'country', 'email', 'url', 'category', 'password'] };

   $password = $input{password};
   $login =  $input{login};

   if (!exists($customers{$login})) {
     status("Login ($login) does not exist. Please enter the correct login .");
     exit;
   }

   if ("\L$password" ne "\L$customers{$login}{password}") {
     status("Password ($password) does not match. Please enter password again.");
     exit;
   }

   $id = trim $login;
   $name = $customers{$id}{name};
   $desc = adjusturl $customers{$id}{desc};
   $banner = adjusturl $customers{$id}{banner}; 
   $account = $customers{$id}{account}; 
   $policy = $customers{$id}{policy}; 
   $street = $customers{$id}{street};
   $city = $customers{$id}{city}; 
   $state = $customers{$id}{state};
   $zipcode = $customers{$id}{zipcode}; 
   $country = $customers{$id}{country};
   $email = $customers{$id}{email};
   $url = $customers{$id}{url}; 
   $category  = $customers{$id}{category}; 
   $password = $customers{$id}{password}; 
 
   #hddebug "desc = $desc, name= $name";
   $prml = ""; 
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "desc=$desc";
   $prml = strapp $prml, "banner=$banner";
   $prml = strapp $prml, "account=$account";
   $prml = strapp $prml, "policy=$policy";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "email=$email";
   $prml = strapp $prml, "url=$url";
   $prml = strapp $prml, "category=$category";
   $prml = strapp $prml, "password=$password";
   $prml = strapp $prml, "rpassword=$password";
   $prml = strapp $prml, "name=$name";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "url=$url";

   ## change the template directory to the appropriate one
   $prml = strapp $prml, "template=$ENV{DOCUMENT_ROOT}/adbanner/showclientinfo.html";
   $prml = strapp $prml, "templateout=/tmp/showclientinfo-$$.html";
   parseIt $prml;

   system "cat templates/content.html";
   system "cat /tmp/showclientinfo-$$.html";

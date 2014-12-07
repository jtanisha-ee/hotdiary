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

# FileName: savecustomerinfo.cgi
# Purpose:  manage and save customer account
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "savecustomerinfo.cgi";


# bind login table vars
   tie %customers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/customers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'banner', 'account', 
        'impression_cost',
        'click_cost', 'policy', 'street', 'city', 'state', 'zipcode', 
	'country', 'email', 'url', 'category', 'password'] };


   $login = $input{login};

   if ($login eq "") {
      status("Please Enter Valid Login.");
      exit;
   } 

   if (!exists($customers{$login}))  {
      status("Please Enter a Valid Login. $login does not exist.");
      exit;
   }
  
   $password = trim $input{password};
   $rpassword = trim $input{rpassword};
   #hddebug "password = $password, rpassword=$rpassword";

   if ("\L$password" ne "\L$rpassword") {
      status "Passwords do not match. Please enter the password again.";
      exit;
   }
 
   $id = $login;
   $desc = $input{desc};
   #hddebug "desc = $desc";
   $customers{$id}{name} = $input{name};
   $customers{$id}{desc} = $input{desc};
   $customers{$id}{banner} = adjusturl $input{banner};
   $customers{$id}{policy} = $input{policy};
   $customers{$id}{street} = $input{street};
   $customers{$id}{city} = $input{city};
   $customers{$id}{state} = $input{state};
   $customers{$id}{zipcode} = $input{zipcode};
   $customers{$id}{country} = $input{country};
   $customers{$id}{email} = $input{email};
   $customers{$id}{url} = adjusturl $input{url};
   $customers{$id}{category} = $input{category};
   $customers{$id}{password} = $input{password};

   tied(%customers)->sync(); 
  
   status("$id: Your account information has been saved.");

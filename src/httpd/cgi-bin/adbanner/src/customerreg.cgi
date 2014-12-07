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

# FileName: customerreg.cgi
# Purpose:  manage and create customer account
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "customerreg.cgi";


# bind login table vars
   tie %customers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/customers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'banner', 'account', 
        'impression_cost',
        'click_cost', 'policy', 'street', 'city', 'state', 'zipcode', 
	'country', 'email', 'url', 'category', 'password', 'approved'] };

   $id =  $input{login};

   if ($id eq "" ) {
     status("Please enter login. Login is empty");
     exit;
   }

   $password = $input{password};
   $rpassword = $input{rpassword};

   if (exists($customers{$id})) {
     status("Please select another login. Login <B>$id</B> is already chosen.");
     exit;
   }
   if ("\L$password" ne "\L$rpassword") {
     status("Passwords do not match. Please enter password again.");
     exit;
   }

   $customers{$id}{name} = $input{name};
   $customers{$id}{desc} = $input{desc};
   $customers{$id}{banner} = $input{banner};
   $customers{$id}{account} = $input{account};
   $customers{$id}{policy} = $input{policy};
   $customers{$id}{street} = $input{street};
   $customers{$id}{city} = $input{city};
   $customers{$id}{state} = $input{state};
   $customers{$id}{zipcode} = $input{zipcode};
   $customers{$id}{country} = $input{country};
   $customers{$id}{email} = $input{email};
   $customers{$id}{url} = $input{url};
   $customers{$id}{category} = $input{category};
   $customers{$id}{password} = "\L$password";
   $customers{$id}{id} = $id;

   #$customers{$id}{impression_cost} = $input{impression_cost};
   #$customers{$id}{click_cost} = $input{click};

   tied(%customers)->sync(); 
  
   status ("$id: Thank you for registering and opening an ad banner account with us. Your Login is <B>$id</B> and password is <B>$password</B>");
   exit; 

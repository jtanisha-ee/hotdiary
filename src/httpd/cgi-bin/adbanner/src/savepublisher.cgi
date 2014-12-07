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

# FileName: savepublisher.cgi
# Purpose:  manage and save publisher account
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "savepublisher.cgi";


# bind publishers table vars
   tie %publishers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'click_reward',
             'street', 'city', 'state', 'zipcode',
             'country', 'phone', 'email', 'url', 'category',
             'password', 'pages', 'click_commission'] };

   $login = $input{login};

   if ($login eq "") {
      status("Please Enter Valid Login.");
      exit;
   } 

   if (!exists($publishers{$login}))  {
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
   $publishers{$id}{name} = $input{name};
   $publishers{$id}{desc} = $input{desc};
   $publishers{$id}{banner} = adjusturl $input{banner};
   $publishers{$id}{policy} = $input{policy};
   $publishers{$id}{street} = $input{street};
   $publishers{$id}{city} = $input{city};
   $publishers{$id}{state} = $input{state};
   $publishers{$id}{zipcode} = $input{zipcode};
   $publishers{$id}{country} = $input{country};
   $publishers{$id}{email} = $input{email};
   $publishers{$id}{url} = adjusturl $input{url};
   $publishers{$id}{category} = $input{category};
   $publishers{$id}{password} = $input{password};
   $publishers{$id}{pages} = $input{pages};

   tied(%publishers)->sync(); 
  
   status("$id: Your account information has been saved.");

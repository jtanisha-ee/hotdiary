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

# FileName: publisherreg.cgi
# Purpose:  create a publisher account
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "publisherreg.cgi";


# bind publisher table vars
  # bind login table vars
   tie %publishers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'click_reward',
             'street', 'city', 'state', 'zipcode',
             'country', 'phone', 'email', 'url', 'category',
             'password', 'pages', 'click_commission'] };


   $id =  $input{login};

   if ($id eq "" ) {
     status("Please enter login. Login is empty");
     exit;
   }

   $password = $input{password};
   $rpassword = $input{rpassword};

   if (exists($publishers{$id})) {
     status("Please select another login. Login <B>$id</B> is already chosen.");
     exit;
   }
   if ("\L$password" ne "\L$rpassword") {
     status("Passwords do not match. Please enter password again.");
     exit;
   }

   $publishers{$id}{name} = $input{name};
   $publishers{$id}{desc} = $input{desc};
   $publishers{$id}{banner} = $input{banner};
   $publishers{$id}{policy} = $input{policy};
   $publishers{$id}{street} = $input{street};
   $publishers{$id}{city} = $input{city};
   $publishers{$id}{state} = $input{state};
   $publishers{$id}{zipcode} = $input{zipcode};
   $publishers{$id}{country} = $input{country};
   $publishers{$id}{email} = $input{email};
   $publishers{$id}{url} = $input{url};
   $publishers{$id}{category} = $input{category};
   $publishers{$id}{password} = "\L$password";
   $publishers{$id}{phone} = $input{phone};
   $publishers{$id}{id} = $id;

   tied(%publishers)->sync(); 
  
   status ("$id: Thank you for registering and opening a publisher banner account with us. Your Login is <B>$id</B> and password is <B>$password</B>. Please copy this snippet of code <BR><pre>&lt;a href=http://www.hotdiary.com/cgi-bin/execshowsite.cgi?member=$id&page=1&gt;<BR>&lt;IMG SRC=http://www.hotdiary.com/cgi-bin/execshowbanner.cgi?member=$id&page=1&gt;&lt;/a&gt;</pre><BR>and paste it on one of the pages of your site. If you need to include this banner in multiple pages of your site, you must change the page=1 tag to point to another unique page number. For instance, your second page can have page=2. Note that you need to replace both instances of the page tag in the above snippet. You can display this banner in as many pages as you wish, as long as the page tag is unique.");

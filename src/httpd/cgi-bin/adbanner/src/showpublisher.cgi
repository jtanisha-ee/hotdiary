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

# FileName: showpublisher.cgi
# Purpose:  show publisher 
# Creation Date: 03-26-2000

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use LWP::UserAgent;

# Read in all the variables set by the form
   &ReadParse(*input);

   #hddebug "showpublisher.cgi";


# bind login table vars
   tie %publishers, 'AsciiDB::TagFile',
   DIRECTORY => "bannerama/publishers",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['id', 'name', 'desc', 'click_reward', 
             'street', 'city', 'state', 'zipcode', 
             'country', 'phone', 'email', 'url', 'category', 
             'password', 'pages'] };


   $password = $input{password};
   $login =  $input{login};

   if (!exists($publishers{$login})) {
     status("Login ($login) does not exist. Please enter the correct login .");
     exit;
   }

   if ("\L$password" ne "\L$publishers{$login}{password}") {
     status("Password ($password) does not match. Please enter password again.");
     exit;
   }

   $id = trim $login;
   $name = $publishers{$id}{name};
   $desc = adjusturl $publishers{$id}{desc};
   $banner = adjusturl $publishers{$id}{banner}; 
   $click_reward = $publishers{$id}{click_reward}; 
   $street = $publishers{$id}{street};
   $city = $publishers{$id}{city}; 
   $state = $publishers{$id}{state};
   $zipcode = $publishers{$id}{zipcode}; 
   $country = $publishers{$id}{country};
   $email = $publishers{$id}{email};
   $url = $publishers{$id}{url}; 
   $category  = $publishers{$id}{category}; 
   $password = $publishers{$id}{password}; 
   $phone = $publishers{$id}{phone}; 
   $pages = $publishers{$id}{pages}; 

   if ($click_reward eq "") {
      $click_reward = "0.00"
   } 
   $prml = ""; 
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "desc=$desc";
   $prml = strapp $prml, "banner=$banner";
   $prml = strapp $prml, "click_reward=$click_reward";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "email=$email";
   $prml = strapp $prml, "category=$category";
   $prml = strapp $prml, "password=$password";
   $prml = strapp $prml, "rpassword=$password";
   $prml = strapp $prml, "name=$name";
   $prml = strapp $prml, "phone=$phone";
   $prml = strapp $prml, "url=$url";
   $prml = strapp $prml, "phone=$phone";
   $prml = strapp $prml, "pages=$pages";

   ## change the template directory to the appropriate one
   $prml = strapp $prml, "template=$ENV{DOCUMENT_ROOT}/adbanner/showpublisherinfo.html";
   $prml = strapp $prml, "templateout=/tmp/showpublisherinfo-$$.html";
   parseIt $prml;

   system "cat templates/content.html";
   system "cat /tmp/showpublisherinfo-$$.html";

   

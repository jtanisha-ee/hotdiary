#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: login.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 10-09-97
# Created by: Smitha Gudur & Manoj Joshi
#


use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

# print HTML headers
# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

  tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
            'topleft', 'topright', 'middleright', 'bottomleft', 
            'bottomright', ' meta'] };
 
  $login = trim $input{'login'};
  $login = "\L$login";
  $password = trim $input{'password'};

  if (!exists $logtab{$login}) {
     status("Please enter the correct login. If you have not yet registered with HotDiary, register before you can use JiveIt!");
     exit;
  }

  if ("\L$password" ne "\L$logtab{$login}{'password'}") {
     status("You entered the password ($password) which is incorrect. Please enter the correct password. If you have not yet registered with HotDiary, register before you can use JiveIt!");
     exit;
  }

  if (exists $jivetab{$login}) {
   status "A JiveIt! account in the name $login already exists. Please <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\">login to the admin page</a> for this account, if you would like to customize or change the configuration.";
   exit;
}


  $alphaindex = substr $login, 0, 1;
  $alphaindex = $alphaindex . '-index';

  system "mkdir -p $ENV{HDHREP}/$alphaindex/$login";

  $prml = "";
  $prml = strapp $prml, "login=$login";
  $prml = strapp $prml, "welcome=Welcome";
  $prml = strapp $prml, "password=$password";
  $prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitauth.html";
  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/jiveitauth.html";
  parseIt $prml;

  #system "/bin/cat $ENV{HDTMPL}/content.html";
  #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/jiveitauth.html";
  hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/jiveitauth.html";
}

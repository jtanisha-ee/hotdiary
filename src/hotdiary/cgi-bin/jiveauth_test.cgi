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
use tp::tp;
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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      
 
  $login = trim $input{'login'};
  $login = "\L$login";
  $password = trim $input{'password'};

  if (!exists $logtab{$login}) {
     status("Please enter the correct login. If you have not yet registered with HotDiary, register before you can use JiveIt!");
     exit;
  }

  if ("\L$password" ne "\L$logtab{$login}{'password'}") {
     status("Please enter the correct password. If you have not yet registered with HotDiary, register before you can use JiveIt!");
     exit;
  }

  $alphaindex = substr $login, 0, 1;
  $alphaindex = $alphaindex . '-index';

  $prml = "";
  $prml = strapp $prml, "login=$login";
  $prml = strapp $prml, "password=$password";
  $prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitauth_test.html";
  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/jiveitauth_test.html";
  parseIt $prml;

  system "/bin/cat $ENV{HDTMPL}/content.html";
  system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/jiveitauth_test.html";
}

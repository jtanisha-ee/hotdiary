#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: addmaster.cgi
# Purpose: it searches info. in hotdiary.
# Creation Date: 04-01-2000
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind master table vars
   tie %mastertab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['email', 'login', 'password', 'busname', 'suite', 'street', 
	'city', 'state', 'zipcode', 'country', 'phone', 'fax', 
	'bphone', 'url', 'contacted', 'category0', 'category1',
        'category2', 'category3', 'category4', 'yearsinbusiness', 
	'numemp', 'annualrev', 'held', 'symbol', 'description',
	'companycontact'] };

   $email = $input{'email'};
   if ($email eq "") {
      status "Please enter non-empty email address.";
      exit;
   }
   $email = "\L$email";
   if (exists $mastertab{$email}) {
      status "Email address already exists.";
      exit;
   }
   $url = $input{url};
   if ($url eq "") {
      status "Please enter non-empty URL address.";
      exit;
   }
   $url = "\L$url";

   ($login, $host) = split '@', $email;
   $login = "\L$login";
   if ( (exists $logtab{$login}) || (notLogin $login) ) {
     $login = $login . $$;
   }
   if ( (exists $logtab{$login}) || (notLogin $login) ) {
     $key1 = substr (getkeys(), 0, 5);
     $login = $login . $key1;
   }
   if (exists $logtab{$login}) {
      status "Could not find a unique member ID for $email";
      exit;
   }
   (@words) = qx{cat $ENV{HDTMPL}/words.db};
   $rand = rand $#words;
   $rand = $rand % $#words;
   hddebug "rand = $rand";
   $password = $words[$rand];
   $password =~ s/\n//g;
   $password = "\L$password"; 

   $busname = $input{busname};
   $category0 = $input{category0};

   $mastertab{$email}{email} = $email;
   $mastertab{$email}{login} = $login;
   $mastertab{$email}{password} = $password;
   $mastertab{$email}{busname} = $busname;
   $mastertab{$email}{category0} = $category0;
   $mastertab{$email}{url} = $url;

   $logtab{$login}{login} = $login;
   $logtab{$login}{password} = $password;
   $logtab{$login}{email} = $email;
   $logtab{$login}{url} = $url;
  
   tied(%mastertab)->sync();
   tied(%logtab)->sync();
}

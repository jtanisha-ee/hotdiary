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
# FileName: addcompany.cgi
# Purpose: it searches info. in hotdiary.
# Creation Date: 04-01-2000
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;


# parse the command line
   &ReadParse(*input); 

   hddebug("addcompany.cgi");
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

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
	'companycontact', 'email2', 'areacodes', 'numareacodes', 'comment' ]};

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };


# bind master table vars
   tie %accounttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab/accounttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login' ] };

   ## categories:
   ## ComputersANDInternet - category 0
   ## Internet - category 1
   ## 

   $email = trim $input{'email'};
   $email =~ s/mailto://g;
   if (notEmail($email)) {
      status "Please enter email address in correct form.";
      exit;
   }

   if ($email eq "") {
      status "Please enter non-empty email address.";
      exit;
   }
   $email = "\L$email";
   if (exists $mastertab{$email}) {
      status "Email address already exists.";
      exit;
   }

   $url = trim $input{url};
   if ($url eq "") {
      status "Please enter non-empty URL address.";
      exit;
   }
   $url =  "\L$url";
   $domain = $url;
   #hddebug "domain = $domain";
   #$domain =~ s/http:\/\///g;
   #hddebug "domain = $domain";
   #($www, $host, $subdomain, $rem) = split /\./,  $domain;
   #hddebug "host = $host";
   $result = qx{grep -i $domain $ENV{HDDATA}/mastertab/*.rec};
   $result =~ s/\n//g;
   $result = trim $result;
   if ($result ne "") {
      hddebug "result = $result";
      status "The URL $url already exists.";
      exit;
   }

   ($user, $host) = split '@', $email;
   ($login, $rest) = split (/\./, $host);
   ## login is acutally hostname. as hostname tends to be unique in 
   ## our case, it makes sense to use this as login
   $login = "\L$login";

   if ( (exists $logtab{$login}) || (notLogin $login) ) {
       $login = $login . $user;
       if ( (exists $logtab{$login}) || (notLogin $login) ) {
         $login = $login . $$;
       }
   }
   if ( (exists $logtab{$login}) || (notLogin $login) ) {
     $key1 = substr (getkeys(), 0, 4);
     $login = $login . $key1;
   }
   if (exists $logtab{$login}) {
      status "Could not find a unique member ID for $email";
      exit;
   }

   #hddebug "login = $login";

   (@words) = qx{cat $ENV{HDTMPL}/words.db};
   $rand = rand $#words;
   $rand = $rand % $#words;
   #hddebug "rand = $rand";
   $password = $words[$rand];
   $password =~ s/\n//g;
   $password = "\L$password"; 

   $busname = $input{busname};
   $category0 = $input{category};

   $mastertab{$email}{email} = $email;
   $mastertab{$email}{login} = $login;
   $mastertab{$email}{password} = $password;
   $mastertab{$email}{busname} = $input{company};
   $mastertab{$email}{category0} = $category0;
   $mastertab{$email}{url} = $url;
   $mastertab{$email}{email2} = $input{email};
   $mastertab{$email}{desc} = $input{desc};
   $mastertab{$email}{city} = $input{city};
   $mastertab{$email}{state} = $input{state};
   $mastertab{$email}{country} = $input{country};
   $mastertab{$email}{bphone} = $input{bphone};
   $mastertab{$email}{fax} = $input{fax};
   $mastertab{$email}{phone} = $input{phone};
   $mastertab{$email}{areacodes} = $input{areacodes};
   $mastertab{$email}{numareacodes} = $input{numareacodes};
   $mastertab{$email}{comment} = adjusturl trim $input{comment};

   $logtab{$login}{login} = $login;
   $logtab{$login}{password} = $password;
   $logtab{$login}{email} = $email;
   $logtab{$login}{url} = $url;

   $surveytab{$login}{login} = $login;

   $accounttab{$login}{login} = $login;
  
   tied(%mastertab)->sync();
   tied(%logtab)->sync();
   tied(%accounttab)->sync();
   tied(%surveytab)->sync();

   status("$login: Your company entry <p><b>$url</b><p> and email <p><b>$email</b><p> have been added to HotDiary Internet directory. Click <a href=\"$hddomain/addcompany.html\"> to add</a> a company.");
   exit;

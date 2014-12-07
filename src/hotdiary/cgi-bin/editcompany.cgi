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
# FileName: editcompany.cgi
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
	'companycontact', 'email2', 'areacodes', 'numareacodes']};

   $password = $input{password};
   $password = "\L$passwword";

   $email = trim $input{'email'};
   if (notEmail($email)){
      status("$email is not a proper email address. Please check the email address again and enter the correct one.");
      exit;
   }

   $email2 = $input{'email2'};

   if (notEmail($email2)){
      status("$email is not a proper email address. Please check the email address again and enter the correct one.");
      exit;
   }

   $email = "\L$email";
   $email2 = "\L$email2";

   if ($email2 eq "") {
      status "Please enter non-empty email address.";
      exit;
   }

   if (!exists $mastertab{$email2}) {
      status "Please enter correct email address before you can edit your company details.";
      exit;
   }

   $url = $input{url};
   if ($url eq "") {
      status "Please enter non-empty URL address.";
      exit;
   }

   $url = "\L$url";
   $login = $input{login};
   $login = "\L$login";

   if ( !exists $logtab{$login})  {
      status "Could not find a directory login. Please contact hotdiary.com";
      exit;
   }

   if (!exists $mastertab{$email})  {
      status "Could not find a directory entry ID for $email. Please contact hotdiary.com";
      exit;
   }

   $password = $input{password};
   hddebug "url = $url";

   $email = $input{email};
   $mastertab{$email}{email2} = $input{email2};
   $mastertab{$email}{login} = $login;
   $mastertab{$email}{busname} = $input{company};
   $mastertab{$email}{password} = $password;
   $mastertab{$email}{category0} = $input{category};
   $mastertab{$email}{url} = $url;
   $mastertab{$email}{suite} = trim $input{suiteno};
   $mastertab{$email}{street} = $input{street};
   $mastertab{$email}{city} = trim $input{city};
   $mastertab{$email}{state} = trim $input{state};
   $mastertab{$email}{zipcode} = trim $input{zipcode};
   $mastertab{$email}{country} = trim $input{country};
   $mastertab{$email}{phone} = trim $input{phone};
   $mastertab{$email}{fax} = trim $input{fax};
   $mastertab{$email}{bphone} = trim $input{bphone};
   $mastertab{$email}{yearsinbusiness} = trim $input{yearsinbusiness};
   $mastertab{$email}{numemp} = trim $input{numemp};
   $mastertab{$email}{annualrev} = trim $input{annualrev};
   $mastertab{$email}{held} = trim $input{held};
   $mastertab{$email}{symbol} = adjusturl trim $input{symbol};
   $mastertab{$email}{description} = adjusturl trim $input{desc};
   $mastertab{$email}{companycontact} = trim $input{companycontact};
   $mastertab{$email}{areacodes} = trim $input{areacodes};
   $mastertab{$email}{numareacodes} = trim $input{numareacodes};

   $logtab{$login}{email} = $email;
   $logtab{$login}{url} = $url;
   $logtab{$login}{password} = $password;

   status("$email: Your changes have been saved and your directory entry will be updated. Your Password is $password and HotDiary Login is $login.");  
   tied(%mastertab)->sync();
   tied(%logtab)->sync();
}

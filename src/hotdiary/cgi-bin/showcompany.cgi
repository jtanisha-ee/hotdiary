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
# FileName: showcompany.cgi
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

  hddebug "showcompany.cgi";

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

   $password = trim $input{password};
   $password = "\L$password";

   $email = $input{'email'};
   hddebug ("email = $email, password = $password");

   if ($email eq "") {
      status "Please enter non-empty email address.";
      exit;
   }

   $email = "\L$email";
   if (!exists $mastertab{$email}) {
	   status "Please enter correct email address ($email) before you can edit your company details.";
	   exit;
   }



   if (!exists $mastertab{$email}) {
	   status "Could not find a directory entry ID for $email. Please contact HotDiary.";
	   exit;
   }

   $login = trim "\L$mastertab{$email}{login}";
   $logpassword = trim "\L$logtab{$login}{password}";

   hddebug "login = $login, logpassword = $logpassword";

   if ($logpassword ne "") {
	   if ($password ne $logpassword) {
		   status("$email: Password does not match");
		   exit;
	   }
   }

   $email2 = $mastertab{$email}{email2}; 
   $login = $mastertab{$email}{login}; 
   $busname = $mastertab{$email}{busname};
   $category = $mastertab{$email}{category0};
   hddebug "category = $category";
   $url = $mastertab{$email}{url}; 
   hddebug "url = $url";
   $suite = $mastertab{$email}{suite};
   $street = $mastertab{$email}{street}; 
   $city = $mastertab{$email}{city};
   $state = $mastertab{$email}{state};
   $zipcode =$mastertab{$email}{zipcode}; 
   $country = $mastertab{$email}{country}; 
   $phone = $mastertab{$email}{phone};
   $fax = $mastertab{$email}{fax};
   $bphone =$mastertab{$email}{bphone};
   $yearsinbusiness = $mastertab{$email}{yearsinbusiness};
   $numemp = $mastertab{$email}{numemp};
   $annualrev = adjusturl $mastertab{$email}{annualrev};
   $held = adjusturl $mastertab{$email}{held};
   $symbol = adjusturl $mastertab{$email}{symbol};
   $description = adjusturl $mastertab{$email}{description}; 
   $companycontact = adjusturl $mastertab{$email}{companycontact};
   $areacodes = adjusturl $mastertab{$email}{areacodes};
   $numareacodes = adjusturl $mastertab{$email}{numareacodes};


   $prml = "";
   $prml = strapp $prml, "companycontact=$companycontact"; 
   $prml = strapp $prml, "desc=$description"; 
   $prml = strapp $prml, "symbol=$symbol"; 
   $prml = strapp $prml, "held=$held"; 
   $prml = strapp $prml, "annualrev=$annualrev"; 
   $prml = strapp $prml, "numemp=$numemp"; 
   $prml = strapp $prml, "yearsinbusiness=$yearsinbusiness"; 
   $prml = strapp $prml, "bphone=$bphone"; 
   $prml = strapp $prml, "fax=$fax"; 
   $prml = strapp $prml, "phone=$phone"; 
   $prml = strapp $prml, "country=$country"; 
   $prml = strapp $prml, "zipcode=$zipcode"; 
   $prml = strapp $prml, "state=$state"; 
   $prml = strapp $prml, "city=$city"; 
   $prml = strapp $prml, "street=$street"; 
   $prml = strapp $prml, "suiteno=$suite"; 
   $prml = strapp $prml, "url=$url"; 
   $prml = strapp $prml, "category=$category"; 
   $prml = strapp $prml, "company=$busname"; 
   $prml = strapp $prml, "login=$login"; 
   $prml = strapp $prml, "email=$email"; 
   $prml = strapp $prml, "email2=$email2"; 
   $prml = strapp $prml, "password=$password"; 
   $prml = strapp $prml, "areacodes=$areacodes"; 
   $prml = strapp $prml, "numareacodes=$numareacodes"; 
   $prml = strapp $prml, "template=$ENV{HDTMPL}/showcompany.html"; 
   $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/showcompany-$$-$login.html"; 
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHOME}/tmp/showcompany-$$-$login.html";


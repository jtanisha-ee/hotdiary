#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: setupdowntown.cgi
# Purpose: Create A Virtual Intranet
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug("setupdowntown.cgi");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
	'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   }

   # bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };                                       

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.\n");
            exit;
	 }
      }
      if (!exists $logtab{$login}) {
         error("Invalid login found in session.");
         exit;
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $sesstab{$biscuit}{'time'} = time();
   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

 
   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle', 'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone', 'fax', 'url', 'email', 'other', 'list',
            'view', 'publish'] };

   if (!(-d "$ENV{HDDATA}/business/business/people/$alphaindex/$login/founded")) {
      system "mkdir -p $ENV{HDDATA}/business/business/people/$alphaindex/$login/founded";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/people/$alphaindex/$login/founded";
      system "chmod 755 $ENV{HDDATA}/business/business/people/$alphaindex/$login/founded";
   }

   tie %founded, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/business/people/$alphaindex/$login/founded",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business'] };


   $rh = $input{rh};
   $password = trim $input{password};
   $rpassword = trim $input{rpassword};
   if ("\L$password" ne "\L$rpassword") {
      status("The two passwords you entered do not match. Please re-enter the password.");
      exit;
   }
   $HDLIC = $input{HDLIC};  

   if (notLogin $business) {
      status("Business name is invalid. Please use alphanumeric characters in your business name.");
      exit;
   }

$prml = "";
$firstname = $logtab{$login}{fname};
$lastname = $logtab{$login}{lname};
$street = $logtab{$login}{street};
$city = $logtab{$login}{city};
$state = $logtab{$login}{state};
$zipcode = $logtab{$login}{zipcode};
$country = $logtab{$login}{country};
$email = $logtab{$login}{email};

# bind invoicetab table vars
   tie %invoicetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/invoicetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['counter', 'index' ] };
                                           
$invoice = $invoicetab{counter}{index};
$invoice = $invoice + 1;
$invoicetab{counter}{index} = $invoice;
tied(%invoicetab)->sync();

$prml = strapp $prml, "firstname=$firstname";
$prml = strapp $prml, "login=$login";
$prml = strapp $prml, "lastname=$lastname";
$prml = strapp $prml, "street=$street";
$prml = strapp $prml, "city=$city";
$prml = strapp $prml, "state=$state";
$prml = strapp $prml, "zipcode=$zipcode";
$prml = strapp $prml, "country=$country";
$prml = strapp $prml, "invoicenum=$invoice";
$prml = strapp $prml, "email=$email";
$prml = strapp $prml, "x_description=My Downtown - B2B Planner";

##### shipping companyfield is business
##### shipping address field is password
##### shipping city field is businesstitle

$amount = "9.99";

   if (-d "$ENV{HDDATA}/moneytab") {
      tie %moneytab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/moneytab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['login', 'account', 'comment', 'approved'] };    

      if (exists($moneytab{$login})) {
         if ($moneytab{$login}{approved} eq "true") {
            $amount = "3.99";
	 }
      }
   }

### check if they have entered rewards comments, if they have
### give discount of $5. otherwise the one time cost of business is $15.

   $prml = strapp $prml, "amount=$amount";

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $rh = $input{rh};
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
   }
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";

   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "x_ship_to_company=";


   $prml = strapp $prml, "template=$ENV{HDTMPL}/setupdowntown.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/setupdowntown-$$.html";

   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html\n\n";
   #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/setupdowntown.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/setupdowntown-$$.html";


   tied(%sesstab)->sync();
   tied(%logsess)->sync();

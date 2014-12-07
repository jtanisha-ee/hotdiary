

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
# FileName: jiveitadmin.cgi
# Purpose: it admin users for jiveit.
# Creation Date: 08-14-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{


# parse the command line
   &ReadParse(*input);

   $login = trim $input{'jp'};
   hddebug "login = $login";
   $login = "\L$login";

   if (notLogin($login)) { 
      status("Invalid characters in login ($login). Make sure there are no spaces in the login name.");
     exit;                                    
   }

   if ($login eq "") {
      status("Your login is empty.");
      exit;
   }
         
   # bind jivetab table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account', 'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };         
   
   if (!exists ($logtab{$login})) {
      status("Your login = $login is invalid. Please register before using JiveIt!.");
      exit; 
   }    

   $url = $input{'url'};
   $logo = $input{'logo'};
   $title = $input{'title'};
   $banner = $input{'bannertxt'};
   $topleft = $input{'topleft'};
   $topright = $input{'topright'};
   $middleright = $input{'middleright'};
   $bottomleft = $input{'bottomleft'};
   $bottomright = $input{'bottomright'};
   #hddebug "url = $url";
   #hddebug "logo = $logo";
   #hddebug "title = $title";
   #hddebug "banner = $banner";

   $jivetab{$login}{'url'} = adjusturl $url;
   $jivetab{$login}{'logo'} = adjusturl $logo;
   $jivetab{$login}{'title'} = adjusturl $title;
   $jivetab{$login}{'banner'} = adjusturl $banner;
   $jivetab{$login}{'topleft'} = adjusturl $topleft;
   $jivetab{$login}{'topright'} = adjusturl $topright;
   $jivetab{$login}{'middleright'} = adjusturl $middleright;
   $jivetab{$login}{'bottomleft'} = adjusturl $bottomleft;
   $jivetab{$login}{'bottomright'} = adjusturl $bottomright;

   #system "/bin/cat $ENV{HDTMPL}/content.html";     
   #system "/bin/cat $ENV{HDTMPL}/jiveit.html";     
   status("Your account has been updated.");
   tied(%jivetab)->sync();   
}

                                   
                         

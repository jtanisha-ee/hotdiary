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
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{


# parse the command line
   &ReadParse(*input);

   $login = trim $input{'jp'};
   $login = "\L$login";

   if (notLogin($login)) { 
      status("Invalid characters in login ($login). Make sure there are no spaces in the login name.");
     exit;                                    
   }

   if ($login eq "") {
      status("Your login=$login is empty");
      exit;
   }
         
   # bind jivetab table vars

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };         

   if (!exists($logtab{$login})) { 
      status("Your login $login is invalid. Please register before you can use JiveIt!"); 
       exit; 
   }

   # bind jivetab table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
	'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright'] };

   $pr = "";    
   $pr = strapp $pr, "jp=$login";
   $jiveitlogo= adjusturl $jivetab{$login}{'logo'};
   $pr = strapp $pr, "jiveitlogo=$jiveitlogo";

   $jiveittitle=adjusturl $jivetab{$login}{'title'};
   $pr = strapp $pr, "jiveittitle=$jiveittitle";

   $topright=adjusturl $jivetab{$login}{'topright'};
   $pr = strapp $pr, "topright=$topright";

   $topleft=adjusturl $jivetab{$login}{'topleft'};
   $pr = strapp $pr, "topleft=$topleft";

   $middleright=adjusturl $jivetab{$login}{'middleright'};
   $pr = strapp $pr, "middleright=$middleright";

   $bottomleft=adjusturl $jivetab{$login}{'bottomleft'};
   $pr = strapp $pr, "bottomleft=$bottomleft";

   $bottomright=adjusturl $jivetab{$login}{'bottomright'};
   $pr = strapp $pr, "bottomright=$bottomright";

   $jiveitbanner=adjusturl $jivetab{$login}{'banner'};
   
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $jp = $login;
   $alphjp = $alphaindex;

   #$alphjp = substr $jp, 0, 1;
   #$alphjp = $alphjp . '-index';

   if ($jp ne "") {
      if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitadmin.html") {
         $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitadmin.html";
      } else {
         $tmpl = "$ENV{HDTMPL}/jiveitadmin.html";
      }
   } else {
      $tmpl = "$ENV{HDTMPL}/jiveitadmin.html";
   }


   system "mkdir -p $ENV{HDREP}/$alphaindex/$login";
   $pr = strapp $pr, "jiveitbanner=$jiveitbanner";

   $pr = strapp $pr, "template=$tmpl";

   #$pr = strapp $pr, "template=$ENV{HDTMPL}/jiveitadmin.html"; 
   $pr = strapp $pr, "templateout=$ENV{HDREP}/$alphaindex/$login/jiveitadmin.html"; 

   parseIt $pr; 
   system "cat \"$ENV{HDTMPL}/content.html\"";   
   system "cat \"$ENV{HDREP}/$alphaindex/$login/jiveitadmin.html\"";   
}

                                   
                         

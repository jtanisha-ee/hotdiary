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
# FileName: privatecalmenu.cgi
# Purpose: Menu for creating HotDiary Private Calendar
# Creation Date: 07-16-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
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

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $HDLIC = $input{HDLIC};


   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $jp = $input{$jp};
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

   $biscuit = $input{'biscuit'};
   if ($biscuit eq "") {
      status("Your login session information is missing. Click <a href=\"http://$vdomain/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
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
      status("You have been logged out automatically. Please relogin.  Click <a href=\"http://$vdomain/index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.\n");
            exit;
         }
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: Your session has already expired. Click <a href=\"http://$vdomain/index.html\" target=\"_parent\"> here</a> to login again.");
      exit;
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['HDLIC', 'partner', 'IP'] };

   tie %parttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/parttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['logo', 'title', 'banner'] };

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers',
        'account', 'topleft', 'topright', 'middleright',
        'bottomleft', 'bottomright', 'meta'] };
 
   $logo = "";

   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $title = $jivetab{$jp}{title};
      $banner = $jivetab{$jp}{banner};
      $label = $title;
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
             $logo = adjusturl $parttab{$partner}{logo};
             $title = $parttab{$partner}{title};
             $banner = adjusturl $parttab{$partner}{banner};
             $label = $title;
         }
      }
   }


   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;

   $cgi = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit";
   $pr = "";
   $pr = strapp $pr, "logo=$logo";
   $pr = strapp $pr, "template=$ENV{HDTMPL}/hdcreateprivategroupcal.html";
   $sgctemp = "$ENV{HDREP}/$alphaindex/$login/sgc-$biscuit-$$.html";
   $pr = strapp $pr, "templateout=$sgctemp";
   $pr = strapp $pr, "biscuit=$biscuit";
   $createcal = adjusturl "$cgi&f=cpc";
   $pr = strapp $pr, "createcal=$createcal";
   $managecal = adjusturl "$cgi&f=mc";
   $pr = strapp $pr, "managecal=$managecal";
   $pr = strapp $pr, "welcome=Welcome";
   $pr = strapp $pr, "login=$login";
   $cgis = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit";
   $pr = strapp $pr, "percal=$cgis";
   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $fref = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }
   $pr = strapp $pr, "home=$fref";
   $pr = strapp $pr, "hiddenvars=$hiddenvars";
   parseIt $pr;

   ## hdcreateprivatecal
   $prs = "";
   $prs = strapp $prs, "logo=$logo";
   if ( ($jp ne "") && 
       (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdcreateprivatecal.html") ) {
       $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdcreateprivatecal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdcreateprivatecal.html";
   }   

   $prs = strapp $prs, "template=$tmpl";
   $cpctemp = "$ENV{HDREP}/$alphaindex/$login/cpc-$biscuit-$$.html";
   $prs = strapp $prs, "templateout=$cpctemp";
   $prs = strapp $prs, "biscuit=$biscuit";
   $searchcal = adjusturl "$cgi&f=sgc";
   $prs = strapp $prs, "searchcal=$searchcal";
   $managecal = adjusturl "$cgi&f=mc";
   $prs = strapp $prs, "managecal=$managecal";
   $prs = strapp $prs, "welcome=Welcome";
   $prs = strapp $prs, "percal=$cgis";
   $prs = strapp $prs, "login=$login";
   $prs = strapp $prs, "home=$fref";
   $prs = strapp $prs, "hiddenvars=$hiddenvars";
   parseIt $prs;

   $prt = "";
   $prt = strapp $prt, "logo=$logo";
   $prt = strapp $prt, "template=$ENV{HDTMPL}/hdmanagecal.html";
   $mctemp = "$ENV{HDREP}/$alphaindex/$login/mc-$biscuit-$$.html";
   $prt = strapp $prt, "templateout=$mctemp";
   $prt = strapp $prt, "biscuit=$biscuit";
   $searchcal = adjusturl "$cgi&f=sgc";
   $prt = strapp $prt, "searchcal=$searchcal";
   $createcal = adjusturl "$cgi&f=cpc";
   $prt = strapp $prt, "createcal=$createcal";
   $prt = strapp $prt, "welcome=Welcome";
   $prt = strapp $prt, "percal=$cgis";
   $prt = strapp $prt, "login=$login";
   $prt = strapp $prt, "home=$fref";
   $prt = strapp $prt, "hiddenvars=$hiddenvars";
   $prt = strapp $prt, "groupmembers=";
   parseIt $prt; 

   system "cat \"$ENV{HDTMPL}/content.html\"";
   if ($f eq "sgc") {
      system "/bin/cat $sgctemp";
   }
   if ($f eq "cpc") {
      system "/bin/cat $cpctemp";
   }
   if ($f eq "mc") {
      system "/bin/cat $mctemp";
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

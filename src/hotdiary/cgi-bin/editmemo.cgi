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
# FileName: editmemo.cgi
# Purpose: Top screen for memo
# Creation Date: 03-04-2000
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
use MIME::Base64;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("editmemo.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
   $g = $input{g};
   hddebug "g = $g";
   $rh = $input{rh};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
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
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();

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
      $logo = adjusturl $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = adjusturl $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   $prml = strapp $prml, "logo=$logo";
   $sc = $input{sc};

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execsavememo =  encurl "execsavememo.cgi";
      $execaddmemo =  encurl "execaddmemo.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execsavememo =   "execsavememo.cgi";
      $execaddmemo =   "execaddmemo.cgi";
   }

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if ($g eq "") {
      hddebug "came here";
      if (! -d "$ENV{HDDATA}/$alpha/$login/todotab") {
         system "mkdir -p $ENV{HDDATA}/$alpha/$login/todotab";
      }
      # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$login/todotab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share',
              'hour', 'banner'] };
   } else {
      if (! -d "$ENV{HDDATA}/listed/groups/$g/todotab") {
         system "mkdir -p $ENV{HDDATA}/listed/groups/$g/todotab";
      }
      # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/todotab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share',
              'hour', 'banner'] };
   }

   $entry = $input{entry};
   if (!exists $todotab{$entry}) {
      status "Invalid memo entry.";
      exit;
   }

   $subject = $todotab{$entry}{subject};
   #$desc = decode_base64 $todotab{$entry}{desc};
   $desc = $todotab{$entry}{desc};
   $desc =~ s/\"/\&quot;/g;
   $desc = adjusturl $desc;
   $todotab{$entry}{desc} = $desc;

   $month = $todotab{$entry}{month};
   $day = $todotab{$entry}{day};
   $year = $todotab{$entry}{year};
   $priority = $todotab{$entry}{priority};
   $status = $todotab{$entry}{status};

   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/editmemo.html") ) {
       $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/editmemo.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/editmemo.html";
   }

   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/editmemo-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execaddmemo=$execaddmemo";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "label1=Memo Manager";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "subject=$subject";
   $prml = strapp $prml, "desc=$desc";
   $prml = strapp $prml, "month=$month";
   $prml = strapp $prml, "day=$day";
   $prml = strapp $prml, "year=$year";
   $prml = strapp $prml, "priority=$priority";
   $prml = strapp $prml, "status=$status";
   $prml = strapp $prml, "label2=Edit Memo";
   $prml = strapp $prml, "g=$g";


   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=13>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavememo\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=year>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=desc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=priority>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=status>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=subject>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=entry>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=edit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=g>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=entry VALUE=$entry>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=edit VALUE=edit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=g VALUE=$g>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=lwptemplate VALUE=http://www.hotdiary.com/rep/$alpha/$login/savememoupload-$$.html>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=lwppress VALUE=save>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";
   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   
   parseIt $prml;

   $prm = "";
   $prm = strapp $prm, "template=$ENV{HDTMPL}/savememoupload.html";
   $prm = strapp $prm, "templateout=$ENV{HDREP}/$alpha/$login/savememoupload-$$.html";
   $prm = strapp $prm, "formenc=$formenc";
   parseIt $prm, 1;


   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alpha/$login/editmemo.html";
   hdsystemcat "$ENV{HDHREP}/$alpha/$login/editmemo-$$.html";

   hddebug "completed editmemo";
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   #tied(%todotab)->sync();

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
# FileName: business.cgi
# Purpose: Top screen for virtual business
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

   hddebug ("business.cgi");
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
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
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com by sending email to support\@$diary, and they will be happy to help you with the license.");
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

   $prml = "";
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
      $execjoinbusiness =  encurl "execjoinbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execleavebusiness = encurl "execleavebusiness.cgi";
      $execviewbusiness = encurl "execviewbusiness.cgi";
      $execdeletebusiness = encurl "execdeletebusiness.cgi";
      $execinvitetobusiness = encurl "execinvitetobusiness.cgi";
      $execbusinesscalendar = encurl "execbusinesscalendar.cgi";
      $execmanagebusiness = encurl "execmanagebusiness.cgi";
      hddebug "execmanagebusiness = $execmanagebusiness";
      $execbusinesslist = encurl "execbusinesslist.cgi";
      $execmeetingstatus = encurl "execmeetingstatus.cgi";
      $execpersonalrsvp = encurl "execpersonalrsvp.cgi";
      $execsetupdowntown = encurl "execsetupdowntown.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execjoinbusiness =  "execjoinbusiness.cgi";
      $execcreatebusiness =  "execcreatebusiness.cgi";
      $execleavebusiness = "execleavebusiness.cgi";
      $execviewbusiness = "execviewbusiness.cgi";
      $execdeletebusiness = "execdeletebusiness.cgi";
      $execinvitetobusiness = "execinvitetobusiness.cgi";
      $execbusinesscalendar = "execbusinesscalendar.cgi";
      $execmanagebusiness = "execmanagebusiness.cgi";
      $execbusinesslist = "execbusinesslist.cgi";
      $execpersonalrsvp = "execpersonalrsvp.cgi";
      $execmeetingstatus = "execmeetingstatus.cgi";
      $execsetupdowntown =  "execsetupdowntown.cgi";
   }
   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';
   $prml = strapp $prml, "template=$ENV{HDTMPL}/business.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/business-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execjoinbusiness=$execjoinbusiness";
   $prml = strapp $prml, "execcreatebusiness=$execcreatebusiness";
   $prml = strapp $prml, "execleavebusiness=$execleavebusiness";
   $prml = strapp $prml, "execviewbusiness=$execviewbusiness";
   $prml = strapp $prml, "execdeletebusiness=$execdeletebusiness";
   $prml = strapp $prml, "execinvitetobusiness=$execinvitetobusiness";
   $prml = strapp $prml, "execbusinesscalendar=$execbusinesscalendar";
   $prml = strapp $prml, "execmanagebusiness=$execmanagebusiness";
   $prml = strapp $prml, "execbusinesslist=$execbusinesslist";

   if ( ($login eq "smitha") || ($login eq "mjoshi") ) {
      $prml = strapp $prml, "execpersonalrsvp=$execpersonalrsvp";
      $prml = strapp $prml, "execmeetingstatus=$execmeetingstatus";
      $prml = strapp $prml, "rsvp=RSVP";
      $prml = strapp $prml, "meeting=Meeting Status";
   } else {
      $prml = strapp $prml, "execpersonalrsvp=";
      $prml = strapp $prml, "rsvp=";
      $prml = strapp $prml, "execmeetingstatus=$execmeetingstatus";
      $prml = strapp $prml, "meeting=";
   }

   $teststr = "<b><FONT FACE=Verdana SIZE=3><a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusinesslist&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=5\">Business Management</a></FONT> </b><BR><FONT FACE=Verdana SIZE=2> Join Biz, Invite Others to Biz, Biz Directory, Biz Calendars, Manage Biz Resources, People, Schedule Biz Meetings, Resources </FONT>";
   $teststr = adjusturl $teststr; 

   if ($login ne "smitha") {
      $prml = strapp $prml, "execschedulemeeting=";
   } else {
      $prml = strapp $prml, "execschedulemeeting=$teststr";
   }
   if ($sc eq "p") {
      $welcome = "Calendar Of";
   } else {
      $welcome = "Welcome";
   }
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   if ($jp ne "") {
      $target = adjusturl "target=_main";
      $prml = strapp $prml, "target=$target";
   } else {
      $prml = strapp $prml, "target=";
   }
   #$prml = strapp $prml, "setup=";
   #$prml = strapp $prml, "execsetupdowntown=";
   #if ( ($login eq "smitha") || ($login eq "mjoshi")) {
      $prml = strapp $prml, "setup=Setup My Downtown";
      $prml = strapp $prml, "execsetupdowntown=$execsetupdowntown";
   #}        
   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alph/$login/business.html";
   hdsystemcat "$ENV{HDHREP}/$alph/$login/business-$$.html";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

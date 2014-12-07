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
# FileName: printgroupdir.cgi 
# Purpose: Create A Virtual Intranet
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("printgroupdir.cgi ");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";
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


   $g = $input{g};

   # bind leditgrouptab table vars
   tie %leditgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/leditgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'jiveit', 'publicedit' ] };

   $publicedit = 0;
   if (exists($leditgrouptab{$g}) ) {
      if ($jp eq "") {
         $jp = $leditgrouptab{$g}{jiveit};
      }
   }

   $sc = $input{sc};
   if ($biscuit eq "") {
      if ( ($g ne "") && (exists $leditgrouptab{$g}) &&
           ($leditgrouptab{$g}{publicedit} eq "CHECKED") ) {
         $publicedit = 1;
      } else {
         hddebug "Came here unfortunately";
         $sc = "p";
      }
   }

   if ($publicedit == 0) {                          
      if ($sc ne "p") {
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
         # reset the timer.
         $sesstab{$biscuit}{'time'} = time();
      }
   }

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
  

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $sc = $input{sc};

 
   if ($os ne "nt") {
      $execaddgroupcontact = encurl "execaddgroupcontact.cgi";
      $execshowgroupcontact = encurl "execshowgroupcontact.cgi";
      $execshowgrouppage = encurl "execshowgrouppage.cgi";
      $execshowgroupfax = encurl "execshowgroupfax.cgi";
      $execgroupcontact = encurl "execgroupcontact.cgi";
      $execprintgroupcontact = encurl "execprintgroupcontact.cgi";
   } else {
      $execaddpgroupcontact = "execaddgroupcontact.cgi";
      $execshowgroupcontact = "execshowgroupcontact.cgi";
      $execshowgrouppage = "execshowgrouppage.cgi";
      $execshowgroupfax = "execshowgroupfax.cgi";
      $execgroupcontact = "execgroupcontact.cgi";
      $execprintgroupcontact = "execprintgroupcontact.cgi";
   }
 
   # bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'group', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };


   if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
         $execgroupcontact = encurl "execgroupcontact.cgi";
   } else {
         $prb = strapp $prb, "formenc=";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execgroupcontact = "execgroupcontact.cgi";
   }

   $msg = "<DIV ALIGN=CENTER><TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";

   $cnt = 0;
   (@sortlist) = sortcontacts("", $g);
   $numcols = 4;
   $numlen = 26;
   foreach $entry (@sortlist) {
      if ( ($cnt % $numcols) == 0) {
         $msg .= "<TR ALIGN=LEFT VALIGN=TOP WIDTH=\"100%\">";
      }
      $msg .= "<TD ALIGN=LEFT VALIGN=TOP WIDTH=\"25%\">";
      $msg .= "<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=2 WIDTH=\"100%\"><TR ALIGN=LEFT VALIGN=TOP WIDTH=\"100%\"><TD ALIGN=LEFT VALIGN=TOP WIDTH=\"100%\">";
      $msg .= "<FONT FACE=Verdana SIZE=1>";
      $fname = $addrtab{$entry}{fname};
      $lname = $addrtab{$entry}{lname};
      if ( ($fname ne "") || ($lname ne "") ) {
         $msg .= "<b>" . (wrapstr "Name: $fname $lname", $numlen) . "</b>";
      }
      $title = $addrtab{$entry}{title};
      if ($title ne "") {
         $msg .= wrapstr "Title: $title", $numlen;
      }
      $busname = $addrtab{$entry}{busname};
      if ($busname ne "") {
         $msg .= "<b>" . (wrapstr "Business Name: $busname", $numlen) . "</b>";
      }
      $aptno = $addrtab{$entry}{aptno};
      if ($aptno ne "") {
         $msg .= wrapstr "No: $aptno", $numlen;
      }
      $street = $addrtab{$entry}{street};
      if ($street ne "") {
         $msg .= wrapstr "Street: $street", $numlen;
      }
      $city = $addrtab{$entry}{city};
      $state = $addrtab{$entry}{state};
      $zipcode = $addrtab{$entry}{zipcode};
      if ( ($city ne "") || ($state ne "") || ($zipcode ne "") ) {
         $msg .= wrapstr "City: $city", $numlen;
         $msg .= wrapstr "State: $state", $numlen;
         $msg .= wrapstr "Zipcode: $zipcode", $numlen;
      }
      $country = $addrtab{$entry}{country};
      if ($country ne "") {
         $msg .= wrapstr "Country: $country", $numlen;
      }
      $phone = $addrtab{$entry}{phone};
      if ($phone ne "") {
         $msg .= "<b>" . (wrapstr "<b>Phone: $phone", $numlen) . "</b>";
      }
      $pager = $addrtab{$entry}{pager};
      if ($pager ne "") {
         $msg .= wrapstr "Pager: $pager", $numlen;
      }
      $fax = $addrtab{$entry}{fax};
      if ($fax ne "") {
         $msg .= wrapstr "Fax: $fax", $numlen;
      }
      $cphone = $addrtab{$entry}{cphone};
      if ($cphone ne "") {
         $msg .= wrapstr "Cell Phone: $cphone", $numlen;
      }
      $bphone = $addrtab{$entry}{bphone};
      if ($bphone ne "") {
         $msg .= "<b>" . (wrapstr "Business Phone: $bphone", $numlen) . "</b>";
      }
      $email = $addrtab{$entry}{email};
      if ($email ne "") {
         $msg .= "<b>" . (wrapstr "Email: $email", $numlen) . "</b>";
      }
      $url = $addrtab{$entry}{url};
      if ($url ne "") {
         $msg .= wrapstr "URL: $url", $numlen;
      }
      $bday = $addrtab{$entry}{bday};
      $bmonth = $addrtab{$entry}{bmonth};
      $byear = $addrtab{$entry}{byear};
      if ( ($bday ne "") && ($bmonth ne "") && ($byear ne "") ) {
         $msg .= wrapstr "Birth Date: $bmonth/$bday/$byear", $numlen;
      }
      $other = wrapstr $addrtab{$entry}{other}, 20;
      $other =~ s/\n/<BR>/g;
      if ($other ne "") {
         $msg .= wrapstr "Other: $other", $numlen;
      }
      $msg .= "</FONT>";
      $msg .= "</TD></TR></TABLE>";
      $msg .= "</TD>";
      if ( ($cnt % $numcols) == ($numcols -1)) {
         $msg .= "</TR>";
      }
      $cnt = $cnt + 1;
   }
   if ( ($cnt % $numcols) == ($numcols-1) ) {
      $msg .= "<TD>&nbsp;</TD>";
   }
   $msg .= "</TABLE></DIV>";
   $msg = adjusturl $msg;

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/printgroupdir.html") ) {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/printgroupdir.html";
   } else {
      $template = "$ENV{HDTMPL}/printgroupdir.html";
   }   

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = "";
   $prml = strapp $prml, "template=$template";
   if ($login eq "") {
      $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/$g-printgroupdir-$$.html";
   } else {
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/printgroupdir-$$.html";
   }
   $prml = strapp $prml, "msg=$msg";
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "cnt=$cnt";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "g=$g";

  if ($biscuit eq "") {
      $prml = strapp $prml, "logout=";
      $prml = strapp $prml, "home=";
      $prml = strapp $prml, "new=";
      $prml = strapp $prml, "features=";
      $prml = strapp $prml, "help=";
   } else {
      $prml = strapp $prml, "logout=Logout";
      $prml = strapp $prml, "home=Home";
      $prml = strapp $prml, "new=What's New";
      $prml = strapp $prml, "features=Features";
      $prml = strapp $prml, "help=Help";
   }

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";

   if ($biscuit eq "") {
      #system "cat $ENV{HDHOME}/tmp/$g-printgroupdir-$$.html";
      hdsystemcat "$ENV{HDHOME}/tmp/$g-printgroupdir-$$.html";
   } else {
      #system "cat $ENV{HDHREP}/$alphaindex/$login/printgroupdir.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/printgroupdir-$$.html";
      tied(%sesstab)->sync();
      tied(%logsess)->sync();
   }



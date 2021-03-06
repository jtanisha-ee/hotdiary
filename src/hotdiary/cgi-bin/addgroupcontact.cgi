#!/usr/local/bin/perl5
#
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
# FileName: addgroupcontact.cgi 
# Purpose:  add a contact to group address book
# Creation Date: 12-01-99
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

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   hddebug ("addgroupcontact.cgi ");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   $g = $input{g};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


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
   hddebug "g = $g, publicedit = $publicedit";
					   		
  
   

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
      }
   }

   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $sesstab{$biscuit}{'time'} = time();
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

   $rh = $input{rh};

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   $prml = "";
   $prml = strapp $prml, "rh=$rh";
   #$prml = strapp $prml, "uname=$uname";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsavegroupcontact = encurl "execsavegroupcontact.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execaddgroupcontact =  encurl "execaddgroupcontact.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execsavegroupcontact = "execsavegroupcontact.cgi";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execaddgroupcontact = "execaddgroupcontact.cgi";
   }

   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/addgroupcontact.html") ) {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/addgroupcontact.html";
   } else {
      $template = "$ENV{HDTMPL}/addgroupcontact.html";
   }   

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

   $prml = strapp $prml, "template=$template";
   if ($login ne "") {
       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/addgroupcontact-$$.html";
   } else {
       $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/$g-addgroupcontact-$$.html";
   }
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "g=$g";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=29>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavegroupcontact\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=entryno>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=fname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=lname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=aptno>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=street>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=city>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=state>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=zipcode>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=country>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=hphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=bphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=cphone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=url>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=pager>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=pagertype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=other>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=fax>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=email>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=newentry>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p23 VALUE=bday>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p24 VALUE=bmonth>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p25 VALUE=byear>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p26 VALUE=busname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p27 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p28 VALUE=g>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=ulogin VALUE=$ulogin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=g VALUE=$g>";

   # this indicates that this is a new entry, entryno is not applicable
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=newentry VALUE=0>";
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
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execaddgroupcontact=$execaddgroupcontact";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "jp=$jp";

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
   if ($login ne "") {
       #system "cat $ENV{HDHREP}/$alph/$login/addgroupcontact.html"; 
       hdsystemcat "$ENV{HDHREP}/$alph/$login/addgroupcontact-$$.html"; 
       tied(%sesstab)->sync();
       tied(%logsess)->sync();
   } else {
       #system "cat $ENV{HDHOME}/tmp/$g-addgroupcontact.html"; 
       hdsystemcat "$ENV{HDHOME}/tmp/$g-addgroupcontact-$$.html"; 
   }

}

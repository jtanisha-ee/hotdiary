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
# FileName: searchgroupcontact.cgi 
# Purpose: Create A Virtual Intranet
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   
use scheduleresolve::scheduleresolve;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("searchgroupcontact.cgi ");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
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

   $g = $input{g};
   $g = "\L$g";
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

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
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


   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=0f0f5f>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff></FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Name (First, Last)</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Business Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Email</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Pager</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Fax</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Bus.Phone</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Directions</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Edit</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;

 
   if ($os ne "nt") {
      $execaddgroupcontact = encurl "execaddgroupcontact.cgi";
      $execshowgroupcontact = encurl "execshowgroupcontact.cgi";
      $execshowgrouppage = encurl "execshowgrouppage.cgi";
      $execshowgroupfax = encurl "execshowgroupfax.cgi";
      $execgroupcontact = encurl "execgroupcontact.cgi";
      $execprintgroupdir = encurl "execprintgroupdir.cgi";
   } else {
      $execaddgroupcontact = "execaddgroupcontact.cgi";
      $execshowgroupcontact = "execshowgroupcontact.cgi";
      $execshowgrouppage = "execshowgrouppage.cgi";
      $execshowgroupfax = "execshowgroupfax.cgi";
      $execgroupcontact = "execgroupcontact.cgi";
      $execprintgroupdir = "execprintgroupdir.cgi";
   }
 
   #$fromstreet = replaceblanks $logtab{$login}{street};
   #$fromcity = replaceblanks $logtab{$login}{city};
   #$fromstate = replaceblanks $logtab{$login}{state};

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';


   # bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'group', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

  
   $cntr = 0; 
   $letter = $input{letter};
   $letter = "\L$letter";
   $all = $input{all};
   if ($all eq "") {
     if ($letter eq "") {
        $letter = "a";
     }
   }
   if ($letter eq "") {
      $letter = "a";
   }
   $chosenletter = $letter;

   $cdir = "";
   $memnum = 0;
   foreach $mem (sort keys %addrtab) {
      $cntr = $cntr +1;
      $msg = "<TR>";
      $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$mem> </FONT></TD>"; 
      $cdir .= $mem;
      $cdir .= " ";

      if ($search eq "First Name OR Last Name") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{fname}") == -1) && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{lname}") == -1) ) {
               next;
          }
      }
      if ($search eq "Street OR City") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{street}") == -1)  && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{city}") == -1) ) {
              next;
         }
      }

      if ($search eq "Country OR City") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{country}") == -1)  && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{city}") == -1) ) {
              next;
         }
      }

      if ($search eq "Zipcode OR State") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{zipcode}") == -1)  && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{state}") == -1) ) {
              next;
         }
      }
      if ($search eq "City OR State") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{city}") == -1)  && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{state}") == -1) ) {
              next;
         }
      }
      if ($search eq "Phone OR Bus.Phone OR Cell Phone") {
         if ( ((index "\Lsearchstr", "\L$addrtab{$mem}{phone}") == -1)  && 
              ((index "\L$searchstr", "\L$addrtab{$mem}{bphone}") == -1) &&
              ((index "\L$searchstr", "\L$addrtab{$mem}{cphone}") == -1) ) {
              next;
         }
      }

      if ($search eq "Email") {
         if ((index "\Lsearchstr", "\L$addrtab{$mem}{email}") == -1)  {
              next;
         }
      }

      if ($search eq "Other") {
         if ((index "\Lsearchstr", "\L$addrtab{$mem}{other}") == -1)  {
              next;
         }
      }

      if ($search eq "Title") {
         if ((index "\Lsearchstr", "\L$addrtab{$mem}{title}") == -1)  {
              next;
         }
      }

      if ($search eq "Pager") {
         if ((index "\Lsearchstr", "\L$addrtab{$mem}{pager}") == -1)  {
              next;
         }
      }




      $memnum = $memnum + 1; 
      $memname = "$addrtab{$mem}{fname} $addrtab{$mem}{lname}";
      $size = length $memname;
      if ($size > 25) {
         $namestr = $memname;
         $memname = substr($namestr, 0, 25);
         $size = $size - 25;
         $memname .= "<BR>";
         $memname .= substr($namestr, 25, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$memname &nbsp;</FONT></TD>";

      $busname = $addrtab{$mem}{busname};
      $size = length $busname;
      if ($size > 25) {
         $busstr = $busname;
         $busname = substr($busstr, 0, 25);
         $size = $size - 25;
         $busname .= "<BR>";
         $busname .= substr($busstr, 25, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$busname &nbsp;</FONT></TD>";

      $email = $addrtab{$mem}{email};
      $size = length $email;
      if ($size > 15) {
         $mail = $email;
	 $email = substr($mail, 0, 15);
	 $size = $size - 15;
	 $email .= "<BR>";
	 $email .= substr($mail, 15, $size);
      } 
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"mailto:$addrtab{$mem}{email}\">$email</a> &nbsp;</FONT></TD>";

      $dbpagertype = replaceblanks $addrtab{$mem}{pagertype};
      $dbpager = replaceblanks $addrtab{$mem}{pager};
      $uname = replaceblanks ($addrtab{$mem}{fname}. " ". $addrtab{$mem}{lname}); 
      ($dbfax = $addrtab{$mem}{'fax'}) =~ s/\n/\n<BR>/g;
      $tostreet = replaceblanks $addrtab{$mem}{street};
      $tocity = replaceblanks $addrtab{$mem}{city};
      $tostate = replaceblanks $addrtab{$mem}{state};

      $pager = $dbpager;
      $to = replaceblanks($to);
      $pt = replaceblanks($pt);
      $thispage = replaceblanks($thispage);
      $thispage = "/rep/$mem/ser$title$biscuit$page_num.html";

      $pageurl = adjusturl("execdogeneric.jsp?pnum=9&p0=$execshowgrouppage&p1=biscuit&p2=thispage&p3=to&p4=pt&p5=uname&p6=dirtype&p7=jp&p8=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbpager&pt=$dbpagertype&uname=$uname&dirtype=groupcontact&jp=$jp&g=$g&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");

      $size = length $pager;
      if ($size > 15) {
         $mempager = $pager;
         $pager = substr($mempager, 0, 15);
         $pager .= "<BR>"; 
         $size = $size - 15;
         $pager .= substr($mempager, 15, $size);
      }

      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$pageurl\">$pager</a>&nbsp;</FONT></TD>";

      $fax = $dbfax;
      $dbfax = getPhoneDigits $dbfax;
      $dbfax = replaceblanks($dbfax);
      $faxurl = adjusturl("execdogeneric.jsp?pnum=8&p0=$execshowgroupfax&p1=biscuit&p2=thispage&p3=to&p4=uname&p5=dirtype&p6=jp&p7=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbfax&uname=$uname&dirtype=groupcontact&jp=$jp&g=$g&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6"); 

      $size = length $fax;
      if ($size > 15) {
         $memfax = $fax;
         $fax = substr($memfax, 0, 15);
         $fax .= "<BR>";
         $size = $size - 15;
         $fax .= substr($memfax, 15, $size);
      }            
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$faxurl\">$fax</a>&nbsp;</FONT></TD>";

      $bphone = $addrtab{$mem}{bphone};
      if ($size > 15) {
         $memphone = $bphone;
         $bphone = substr($memphone, 0, 15);
         $bphone .= "<BR>";
         $size = $size - 15;
         $bphone .= substr($memphone, 15, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$bphone &nbsp;</FONT></TD>";
    
      $directions = adjusturl "http://www.zip2.com/scripts/map.dll?mad1=$fromstreet&mct1=$fromcity&mst1=$fromstate&mad2=$tostreet&mct2=$tocity&mst2=$tostate&type=gis&mwt=350&mht=280&mwt1=350&mht1=280&mwt2=350&mht2=280&mwt3=350&mht3=280&method=d2d&ck=21439101&userid=55724010&userpw=xtv0J_txAwt8tE_FD0C&version=663922&sType=street&adrVer=918629102&ver=d3.0&GetDir.x=Get+Directions";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"$directions\">Directions</a>&nbsp;</FONT></TD>";

      $moreurl = adjusturl("execdogeneric.jsp?pnum=5&p0=$execshowgroupcontact&p1=biscuit&p2=ulogin&p3=jp&p4=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=$mem&jp=$jp&g=$g&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");

      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$moreurl\">Edit</a>&nbsp;</FONT></TD>"; 
 
      $msg .= "</TR>";

      if ((exists $addrtab{$mem})) {
         $smsg .= $msg;
      } else {
         $umsg .= $msg;
      }
   }

   if ($cntr > 0) {
      (@hshcdir) = split " ", $cdir; 
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      $smsg .= "<BR><BR><FONT FACE=\"Verdana\" SIZE=3><INPUT TYPE=submit NAME=Remove VALUE=\"Remove\"></FONT>";
      $smsg = adjusturl $smsg;
   } else {
      $smsg = "";
   }


   $folder = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $folder .= "<TR WIDTH=\"100%\"><TD WIDTH=\"100%\">";

   $folder .= "<TABLE BORDER=0 CELLPADDING=5 CELLSPACING=0 BGCOLOR=ee9900 WIDTH=\"100%\">";
   $folder .= "<TR ALIGN=CENTER WIDTH=\"100%\">";
   for ($i =0; $i <= 25; $i = $i + 1) {
      $letter = chr(65 + $i); 
      $lt = scheduleresolve::scheduleresolve::isaddr($letter, $login, $g); 
      if ($lt == 1) {
         $letterlink = adjusturl("execdogeneric.jsp?pnum=7&p0=$execgroupcontact&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&p6=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&rh=$rh&jp=$jp&g=$g&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=$letter&all=");
         if ("\L$letter" eq "\L$chosenletter") {
            $bgcolor = "BGCOLOR=02994e";
         } else {
            $bgcolor = "";
         }
         if ( ("a" eq "\L$chosenletter") && ($all ne "") ) {
            $bgcolor = "";
         }
         $folder .= "<TD $bgcolor ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</a></FONT></TD>";
     } else {
         $folder .= "<TD ALIGN=CENTER SIZE=1><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</FONT></TD>";
     }
   }

   if ($cntr > 0) {
      $letterlink = adjusturl("execdogeneric.jsp?pnum=7&p0=$execgroupcontact&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&p6=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&jp=$jp&g=$g&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=&all=all");
      if ("$all" ne "") {
         $bgcolor = "BGCOLOR=02994e";
      } else {
         $bgcolor = "";
      }
      $folder .= "<TD $bgcolor ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">All</a></FONT></TD>";
   }

   $folder .= "</TR></TABLE>";
   $folder .= "</TD></TR></TABLE>";
   $folder = adjusturl($folder);
 

      $prb = "";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";

      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
         $execdeletegroupcontact =  encurl "execdeletegroupcontact.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execdeletegroupcontact = "execdeletegroupcontact.cgi";
      }
      
      $prb = strapp $prb, "template=$ENV{HDTMPL}/groupcontact.html";
      if ($biscuit ne "") {
         $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/groupcontact-$$.html";
      } else {
         $prb = strapp $prb, "templateout=$ENV{HDHOME}/tmp/$g-groupcontact$$.html";
      }

      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execdeletegroupcontact\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";

      #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 5;
      $numend = $mcntr;
      $numbegin = $mcntr;

      # this tells from where the parameter for selection starts
      foreach $cn (@hshcdir) {
         $cn = trim $cn;
	 $numend = $numend + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
	 $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $k = $k + 1;
      }
      $numend = $numend - 1;

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
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
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";
      $hiddenvars = adjusturl $hiddenvars;
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "bizdir=$smsg";
      $prb = strapp $prb, "letter=$folder";
      $prb = strapp $prb, "jp=$jp";
      $prb = strapp $prb, "cntr=$memnum contacts";

   $prb = strapp $prb, "status=";
   $bizlabel = "$login $fname $lname - Address Book";
   $prb = strapp $prb, "bizlabel=$bizlabel";
   $prb = strapp $prb, "g=$g";
   $prb = strapp $prb, "execproxylogout=$execproxylogout";
   $prb = strapp $prb, "execdeploypage=$execdeploypage";
   $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
   $prb = strapp $prb, "execaddgroupcontact=$execaddgroupcontact";

   if ($biscuit ne "") {
      $prb = strapp $prb, "home=Home";
      $prb = strapp $prb, "logout=Logout";
      $prb = strapp $prb, "new=What's New";
      $prb = strapp $prb, "features=Features";
      $prb = strapp $prb, "help=Help";
   } else {
      $prb = strapp $prb, "home=";
      $prb = strapp $prb, "logout=";
      $prb = strapp $prb, "new=";
      $prb = strapp $prb, "features=";
      $prb = strapp $prb, "help=";
   }

   parseIt $prb;

   system "cat $ENV{HDTMPL}/content.html";
   if ($biscuit ne "") {
      system "cat $ENV{HDHREP}/$alphaindex/$login/groupcontact-$$.html";
      tied(%sesstab)->sync();
      tied(%logsess)->sync();
   } else {
      system "cat $ENV{HDHOME}/tmp/$g-groupcontact$$.html";
   }
  



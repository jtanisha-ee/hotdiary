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
# FileName: printpersonaldir.cgi 
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

   #print &PrintHeader;
   #print &HtmlTop ("printpersonaldir.cgi ");
   hddebug ("printpersonaldir.cgi ");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 

   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   hddebug "login from cookie = $login";


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


   $cardpattern = $input{cardpattern};

   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=0f0f5f>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;
 
   if ($os ne "nt") {
      $execaddpersonalcontact = encurl "execaddpersonalcontact.cgi";
      $execshowpersonaldir = encurl "execshowpersonaldir.cgi";
      $execshowpersonalpage = encurl "execshowpersonalpage.cgi";
      $execshowpersonalfax = encurl "execshowpersonalfax.cgi";
      $execpersonaldir = encurl "execpersonaldir.cgi";
   } else {
      $execaddpersonalcontact = "execaddpersonalcontact.cgi";
      $execshowpersonaldir = "execshowpersonaldir.cgi";
      $execshowpersonalpage = "execshowpersonalpage.cgi";
      $execshowpersonalfax = "execshowpersonalfax.cgi";
      $execpersonaldir = "execpersonaldir.cgi";
   }
 
   $fromstreet = replaceblanks $logtab{$login}{street};
   $fromcity = replaceblanks $logtab{$login}{city};
   $fromstate = replaceblanks $logtab{$login}{state};

   $g = "";

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   # bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
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

   $cdir = "";
   $memnum = 0;
   foreach $mem (sort keys %addrtab) {
      $cntr = $cntr +1;
      $msg = "<TR>";
      $cdir .= $mem;
      $cdir .= " ";
      $fn = substr $addrtab{$mem}{fname}, 0, 1;
      $ln = substr $addrtab{$mem}{lname}, 0, 1;

      if ($all eq "") {
         if (($letter ne "\L$fn") && ($letter ne "\L$ln")) {
	       next;
         }
      }
      $memnum = $memnum + 1; 
      $memname = "$addrtab{$mem}{fname} $addrtab{$mem}{lname}";
      $email = $addrtab{$mem}{email};
      $dbpager = replaceblanks $addrtab{$mem}{pager};
      ($dbfax = $addrtab{$mem}{'fax'}) =~ s/\n/\n<BR>/g;
      $bphone = $addrtab{$mem}{bphone};

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


   #### this creates the letter link for the top.
   $folder = "<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $folder .= "<TR>";
   for ($i =0; $i <= 25; $i = $i + 1) {
      $letter = chr(65 + $i); 
      $lt = scheduleresolve::scheduleresolve::isaddr($letter, $login, $g); 
      if ($lt == 1) {
         $letterlink = adjusturl("execdogeneric.jsp?pnum=6&p0=$execpersonaldir&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&rh=$rh&jp=$jp&vdomain=$vdomain&hs=$hs&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6&letter=$letter&all=");
         $folder .= "<TD SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</a></FONT></TD>";
     } else {
         $folder .= "<TD SIZE=1><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</FONT></TD>";
     }
   }

   if ($cntr > 0) {
      $letterlink = adjusturl("execdogeneric.jsp?pnum=6&p0=$execpersonaldir&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&jp=$jp&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6&letter=&all=all");
      $folder .= "<TD SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">All</a></FONT></TD>";
   }

   $folder .= "</TR></TABLE>";
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
      $execdeletepersonaldir =  encurl "execdeletepersonaldir.cgi";
   } else {
      $prb = strapp $prb, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeletepersonaldir = "execdeletepersonaldir.cgi";
   }

   $prb = strapp $prb, "template=$ENV{HDTMPL}/printpersonaldir.html";
   $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/printpersonaldir-$$.html";

   $prb = strapp $prb, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prb = strapp $prb, "welcome=$welcome";
   $prb = strapp $prb, "login=$login";
   $prb = strapp $prb, "HDLIC=$HDLIC";
   $prb = strapp $prb, "ip=$ip";
   $prb = strapp $prb, "rh=$rh";
   $prb = strapp $prb, "hs=$hs";
   $prb = strapp $prb, "vdomain=$vdomain";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execdeletepersonaldir\">";
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
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
   $prb = strapp $prb, "execproxylogout=$execproxylogout";
   $prb = strapp $prb, "execdeploypage=$execdeploypage";
   $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
   $prb = strapp $prb, "execaddpersonalcontact=$execaddpersonalcontact";

   parseIt $prb;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/printpersonaldir.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/printpersonaldir-$$.html";
  

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

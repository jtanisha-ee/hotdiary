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
# FileName: showgroupfax.cgi 
# Purpose: it sends a fax message.
# Creation Date: 12-01-98
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

   hddebug "showgroupfax.cgi";

   $biscuit = $input{'biscuit'};
   $jp = $input{jp};

   $vdomain = $input{vdomain};
   $rh = $input{rh};
   $HDLIC = $input{HDLIC};
   $dirtype = $input{dirtype};
   $hs = $input{hs};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   $g = $input{g};
   $g = "\L$g";
   $to = $input{'to'};
   hddebug "to = $to";

   status("Please open a premium account to send faxes. Ask your group master to open a premium account to send faxes.");
   exit;

   $thispage = $input{'thispage'};

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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


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
   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.\n");
              exit;
	   }
        }
   }


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: Your session has already timed out. However, all your personal data is completely intact.");
      exit;
   }

   $sesstab{$biscuit}{'time'} = time();

  }
}
   $uname = $input{uname};
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

   $dirtype = $input{dirtype};

   if ($dirtype eq "groupcontact") {
      $execfile = "execgroupcontact.cgi";
   }
   if ($os ne "nt") {
      $execfile = encurl "$execfile";
   }

   $successpage = "Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execfile&p1=biscuit&p2=jp&p3=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&g=$g&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go back.";

   # bind faxaccttab table vars to maintain the account balance.
   tie %faxaccttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/faxaccttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'faxid', 'balance'] };

   if (!exists $faxaccttab{$login}) {
      status("$login: You do not have a fax account to use fax. Click on the premium services link for more information. <BR>$successpage.");
      exit;
   }

   $rate = 15;
   $balance = $faxaccttab{$login}{'balance'};
   $balance = $balance - ($numpages * $rate);
   if ($balance <= 0) {
      status("$login: You do not have enough balance($balance) in your fax account to send $numpages pages. Click on the premium services link for more information.");
      exit;
   }


   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $prml = "";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "uname=$uname";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsendpersonalfax = encurl "execsendpersonalfax.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";

   } else {
      $prml = strapp $prml, "formenc=";
      $execsendpersonalfax = "execsendpersonalfax.cgi";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$jp/templates/showgroupfax.html") ) {
      $template = "$ENV{HDDATA}/$jp/templates/showgroupfax.html";
   } else {
      $template = "$ENV{HDTMPL}/showgroupfax.html";
   }   

   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/$g-showgroupfax-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=7>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsendgroupfax\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=dirtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=to>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=faxfile>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=message>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=dirtype VALUE=$dirtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=to VALUE=$to>";

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

   #$prml = strapp $prml, "label=$Send Fax Premium Service";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";


   # these lines are uncommented for testing.
   $prml = strapp $prml, "to=$to";
   $prml = strapp $prml, "thispage=$thispage";
   #$urlcgi = buildurl("execsendmsg.cgi");
   #$prml = strapp $prml, "actioncgi=cgi-bin/execsendfaxmsg.cgi";

   #send email to faxsav at number@faxsav.com
   #system "/bin/mail -s \"fax\" $email < $mfile";
   parseIt $prml;

   system "/bin/cat $ENV{HDTMPL}/content.html"; 
   system "/bin/cat $ENV{HDHOME}/tmp/$g-showgroupfax-$$.html"; 

   if ($biscuit ne "") {
      # save the info in db
      tied(%sesstab)->sync();
      tied(%logsess)->sync();
   }

}

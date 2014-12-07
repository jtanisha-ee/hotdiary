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
# FileName: sendpage.cgi 
# Purpose: it sends a pager message.
# Creation Date: 06-10-98
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

   hddebug ("showbusinesspage.cgi");

   $biscuit = $input{'biscuit'};
   $hs = $input{'hs'};
   $jp = $input{'jp'};
   $vdomain = $input{'vdomain'};
   $rh = $input{'rh'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   $to = $input{'to'};
   $rh = $input{'rh'};
   $pagertype = $input{'pt'};
   if ("\L$pagertype" eq "\LSkytel Pager") {
      if (notSkyTelPin trim $to) {
         status("The $pagertype number you have entered ($to) must be a valid $pagertype pin (7 numeric digits). For instance \"1234567\" is a valid format. Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LAirTouch Pager") {
      if (notAirTouchPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (11 numeric digits). For instance \"1-408-456-1234\" is a valid format. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LPageMart Pager") {
      if (notPageMartPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (either a 7 digit numeric PIN or a 10 digit $pagertype \"Assured Messaging\" phone number which is also the PIN). Note that 7 digit numeric PINs are used for traditional (one-way) paging using $pagertype. For instance either \"408-456-1234\" or \"456-1234\", both are valid formats. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this. <p>If you are trying to page a subscriber and you do not know the recipient's PIN, you must contact that individual to gain access to his or her PIN. $pagertype does not give out subscriber's PINs.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LNextel Pager") {
      if (notNextelPin trim $to) {
         if (!(notEmailAddress trim $to)) {
            $msg = "<p>You seem to have entered an email address for your pager. If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pagertype.";
         }
         status("The $pagertype number you have entered ($to) must be a valid $pagertype PIN (10 digit numeric PIN). For instance \"408-456-1234\" is a valid format. $msg <p>Also, you must have $pagertype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pagertype representative to verify this.");
         exit;
      }
   }
   if ("\L$pagertype" eq "\LOther Pager") {
      if (notEmailAddress trim $to) {
         status("The Other Pager type only supports pager email addresses. Please enter a valid email address for your pager, before using this feature. <p>If you are new to this feature, note that Other Pager can be used with any mobile device that is capable of receiving email. For instance, you can use a cellphone, palm device or a pager. <p>You may need to verify if your mobile device supports email with your carrier service representative.");
         exit;
      }
   }
   #print "to = ", $to, "\n";
   #print "pagertype = ", $pagertype, "\n";
   $thispage = $input{'thispage'};
   #print "thispage = ", $thispage, "\n";

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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.");
              exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already timed out. However, all your personal information is completely intact.");
    exit;
   }
   $sesstab{$biscuit}{'time'} = time();


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

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
   $rh = $input{rh};
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
   }

   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $pagertype = replaceblanks($pagertype);
   $to = replaceblanks($to);
   $thispage = replaceblanks($thispage);
   $dirtype = $input{dirtype};


   $prml = "";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "uname=$uname";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsendbusinesspage = encurl "execsendbusinesspage.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execsendbusinesspage = "execsendbusinesspage.cgi";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = strapp $prml, "template=$ENV{HDTMPL}/showbusinesspage.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/showbusinesspage-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $uname = $input{uname};
   $prml = strapp $prml, "uname=$uname";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=8>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsendbusinesspage\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=to>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=thispage>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=pagertype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=message>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=dirtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=to VALUE=$to>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=thispage VALUE=$thispage>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pagertype VALUE=$pagertype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=dirtype VALUE=$dirtype>";
  
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
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
 
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/showbusinesspage.html"; 
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showbusinesspage-$$.html"; 

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

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
# FileName: createbusinesscalendar.cgi 
# Purpose:  add a contact to reseller, customer, or other folders
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

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   hddebug ("createbusinesscalendar.cgi ");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
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

   hddebug "reached near hdlic";
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
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   hddebug "reached near business";
   $business = trim $input{business};
  
   if ($os ne "nt") {
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execbusiness =  encurl "execbusiness.cgi";
   } else {
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execbusiness = "execbusiness.cgi";
   }

   hddebug "before rh";
   $rh = $input{rh};
   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   hddebug "does not exist";
   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   tie %managertab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['login']};

   if ((!exists($managertab{$login})) &&
      ($businesstab{$business}{businessmaster} ne $login)) {
      status("$login: You need to be either a Business Master or Business Manager to create teams. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&re4=os&le4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

   tie %mgraccesstab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother',
                 'invite', 'approve', 'delete', 'edit', 'manage', 'contact', 'teams']};

   if ($businesstab{$business}{businessmaster} ne $login) {
      if ($mgraccesstab{access}{teams} ne "CHECKED") {
         status("$login: You do not have the permission to create a team. Manager Role permissions are not given to create a team. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
         exit;
      }
   }

   
   hddebug "before logo";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   hddebug "before prml = $business";

   $prml = "";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execaddbusinesscalendar = encurl "execaddbusinesscalendar.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";

   } else {
      $prml = strapp $prml, "formenc=";
      $execaddbusinesscalendar = "execaddbusinesscalendar.cgi";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =   "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }
   $prml = strapp $prml, "template=$ENV{HDTMPL}/createbusinesscalendar.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/createbusinesscalendar-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execaddbusinesscalendar\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=teamname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=teamtitle>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=teamdesc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
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
   $prml = strapp $prml, "business=$business";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "label=";
   $prml = strapp $prml, "biscuit=$biscuit";
   $statmsg = "Business Master & Business Managers can create teams.";
   $prml = strapp $prml, "status=$statmsg";

   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDHREP}/$login/createbusinesscalendar-$$.html"; 
   hdsystemcat "$ENV{HDHREP}/$login/createbusinesscalendar-$$.html"; 

# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

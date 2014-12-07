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
# FileName: meetingstatus.cgi
# Purpose: show rsvp meetings that are not confirmed.
# Creation Date: 09-12-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use scheduleresolve::scheduleresolve;   
use calfuncs::meetingfuncs;   


# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "rsvp()";
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
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
    'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };
                                                                              
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

   $alp = substr $login, 0, 1;
   $alp = $alp . '-index';

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
   # bind login table 
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

   $sesstab{$biscuit}{'time'} = time();

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

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
   $business = "iir";

   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
   }

   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   system "mkdir -p $ENV{HDDATA}/business/business/$business/meetingtab";
   system "chmod 755 $ENV{HDDATA}/business/business/$business/meetingtab";

   tie %meetingtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/meetingtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
            'numresources', 'resources', 'teams', 'groups', 'mem',
            'businesses'] };

   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=0f0f5f>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Organizer</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Event</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Date</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Time</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Event Details</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>No.Invitees</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Invitees Confirmed</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Invitees Not Confirmed</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>No.Resources</FONT></TD>";
   $msg .= "<TD WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Resources Reserved</FONT></TD>";

   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;

   $cntr = 0;

   foreach $entryno (sort keys %meetingtab) {
      $cntr = $cntr + 1;
      $msg .= "<TR>";
      $invitees = $meetingtab{$entryno}{invitees};
      (@hshmems) = split (" ", $invitees);
      hddebug "invitees = $invitees";

      $msg .= "<TD><FONT FACE=Verdana SIZE=2>$meetingtab{$entryno}{organizer}&nbsp;</FONT></TD>";
      hddebug "$#hshmems, $hshmems[0], $hshmems[1]";

      $alph = substr $hshmems[$0], 0, 1;
      $alph = $alph . '-index';
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alph/$hshmems[$0]/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
           'hour', 'min', 'meridian', 'dhour', 'dmin',
           'dtype', 'atype', 'desc', 'zone', 'recurtype',
           'share', 'free', 'subject', 'street', 'city', 'state',
           'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
           'confirm', 'id', 'type'] };

      if (exists ($appttab{$entryno})) {
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$appttab{$entryno}{subject} &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$appttab{$entryno}{month}/$appttab{$entryno}{day}/$appttab{$entryno}{year} &nbsp;</FONT></TD>";
	 $min = $appttab{$entryno}{min};
         if ($min eq "") {
	    $min = "00";
         }
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$appttab{$entryno}{hour}:$min &nbsp;$appttab{$entryno}{meridian} $appttab{$entryno}{zone} &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$appttab{$entryno}{desc} &nbsp;</FONT></TD>";
     } else {
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>&nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>&nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>&nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>&nbsp;</FONT></TD>";
     }

      $no = "";
      $yes = "";
      for ($i = 0; $i <= $#hshmems; $i = $i + 1) {
         $alpha = substr $hshmems[$i], 0, 1;
         $alpha = $alpha . '-index';
         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$hshmems[$i]/appttab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'month', 'day', 'year',
              'hour', 'min', 'meridian', 'dhour', 'dmin',
              'dtype', 'atype', 'desc', 'zone', 'recurtype',
              'share', 'free', 'subject', 'street', 'city', 'state',
              'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
              'confirm', 'id', 'type'] };

	 if (exists($appttab{$entryno} )) {
	    if ($appttab{$entryno}{confirm} eq "no") {
	       $no .= $hshmems[$i];
	    } else {
               $yes .= "$logtab{$hshmems[$i]}{fname}$logtab{$hshmems[$i]}{lname}($hshmems[$i]) ";
	    }
         }
      }

      hddebug "yes = $yes, no = $no, entryno = $entryno";
      if (exists ($meetingtab{$entryno}) ) {
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$meetingtab{$entryno}{numinvitees} &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$yes &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$no &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$meetingtab{$entryno}{resources} &nbsp;</FONT></TD>";
         $msg .= "<TD WIDTH=\"10%\"><FONT FACE=Verdana SIZE=2>$meetingtab{$entryno}{numresources} &nbsp;</FONT></TD>";
     }
     $msg .= "</TR>";
     $smsg .= $msg;
      
   }

   if ($cntr == 0) {
      $smsg = "";
      status("$login: There are no meetings to be listed in $business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

   hddebug "$smsg";
   $smsg .= "</TABLE>";
   $umsg .= "</TABLE>";
   $smsg = adjusturl $smsg;

  

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }



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
   } else {
      $prb = strapp $prb, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }

   $prb = strapp $prb, "template=$ENV{HDTMPL}/companyrsvp.html";
   $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/companyrsvp-$$.html";
   $prb = strapp $prb, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prb = strapp $prb, "welcome=$welcome";
   $prb = strapp $prb, "login=$login";
   $prb = strapp $prb, "HDLIC=$HDLIC";
   $prb = strapp $prb, "ip=$ip";
   $prb = strapp $prb, "rh=$rh";
   $prb = strapp $prb, "hs=$hs";
   $prb = strapp $prb, "vdomain=$vdomain";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=1>";
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
   $prb = strapp $prb, "status=";
   $prb = strapp $prb, "execproxylogout=$execproxylogout";
   $prb = strapp $prb, "execdeploypage=$execdeploypage";
   $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
   $prb = strapp $prb, "business=$business";

   parseIt $prb;

   #system "cat $ENV{HDTMPL}/content.html"; 
   #system "cat $ENV{HDHREP}/$alphaindex/$login/companyrsvp.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/companyrsvp-$$.html";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

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
# FileName: showpeopletoteam.cgi 
# Purpose: Create A Virtual Intranet
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

   #print &PrintHeader;
   #print &HtmlTop ("showpeopletoteam.cgi ");
   hddebug ("showpeopletoteam.cgi ");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
               status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
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

   $business = trim $input{business};
   $rh = $input{rh};

   tie %businesstab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/businesstab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

  
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
   }
  
   if ((!exists $businesstab{$business}) || ($business eq "")) {
      if ($os ne "nt") {
         $execcreatebusiness = encurl "execcreatebusiness.cgi";
      } else {
         $execcreatebusiness = "execcreatebusiness.cgi";
      }

      status("$login: Business ($business) does not exist. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3&HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&enu m=4\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

   tie %managertab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['login']};

   if ((!exists($managertab{$login})) && 
      ($businesstab{$business}{businessmaster} ne $login)) {
      status("$login: You do not have the permission to add members to teams. Manager Role can be assigned by only Business Master. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   tie %mgraccesstab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother',
                 'invite', 'approve', 'delete', 'edit', 'manage', 
   		'contact', 'teams']};

   if ($businesstab{$business}{businessmaster} ne $login) {
      if ($mgraccesstab{access}{teams} ne "CHECKED") {
         status("$login: You do not have the permission to add members to a team. As Manager Role permissions are not given to add members to a team. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
         exit;
      }
   }

   if (!-d ( "$ENV{HDDATA}/business/business/$business/teams/teamtab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/teamtab";
      status("$login: You have not created any teams. Please add a team before you can invite members to the team.");
      exit;
   }

   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode',
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] };

   (@hshteams) = sort keys %teamtab;
   if ($#hshteams < 0) {
      status("$login: You have not created any teams. Please add a team before you can invite members to the team.");
      exit;
   }

   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   #$msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Team Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Team Title</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Team Desc</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Change Team Settings</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;
   $cntr = 0;

   if ($os ne "nt") {
      $execeditteamsettings = encurl "execeditteamsettings.cgi";
   } else {
      $execeditteamsettings = "execeditteamsettings.cgi";
   } 
   foreach $mem (sort keys %teamtab) {
       $msg = "<TR>";
       $people .= $mem;
       $people .= " ";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$mem &nbsp;</FONT></TD>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$mem}{'teamtitle'} &nbsp;</FONT></TD>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$mem}{'teamdesc'} &nbsp;</FONT></TD>";
       $editurl = adjusturl("execdogeneric.cgi?pnum=4&p0=$execeditteamsettings&p1=biscuit&p2=business&p3=teamname&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&teamname=$mem&business=$business&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$editurl\">Edit</a>&nbsp;</FONT></TD>";
       $msg .= "</TR>";

       if (exists $teamtab{$mem}) {
          $smsg .= $msg;
       } else {
          $umsg .= $msg;
       }
       $cntr = $cntr +1;
   }

   if ($cntr == 0) {
      status("$login: You do not have any people to ($business). Click here to invite people to ($business)");
      exit; 
   }

   $smsg .= "</TABLE>";
   $umsg .= "</TABLE>";
   $smsg = adjusturl $smsg;

   if ($logo ne "") { 
      $logo = adjusturl $logo;
   }
   $sc = $input{sc};
   


   $prb = "";
   $prb = strapp $prb, "rh=$rh";
   $prb = strapp $prb, "logo=$logo";
   $prb = strapp $prb, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
      $prb = strapp $prb, "formenc=$formenc";
      $execshowteams = encurl "execshowteams.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } else {
      $prb = strapp $prb, "formenc=";
      $execshowteams = "execshowteams.cgi";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   }


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
   $prb = strapp $prb, "template=$ENV{HDTMPL}/showteams.html";
   $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/showteams-$$.html";
   $prb = strapp $prb, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prb = strapp $prb, "welcome=$welcome";
   $prb = strapp $prb, "login=$login";
   $prb = strapp $prb, "HDLIC=$HDLIC";
   $prb = strapp $prb, "ip=$ip";
   $prb = strapp $prb, "rh=$rh";
   $prb = strapp $prb, "hs=$hs";
   $prb = strapp $prb, "vdomain=$vdomain";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execshowteams\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=teamname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=4>";
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>"
   $hiddenvars = adjusturl $hiddenvars;
   $prb = strapp $prb, "hiddenvars=$hiddenvars";
   $prb = strapp $prb, "business=$business";
   $prb = strapp $prb, "members=$smsg";
   $statmsg = "Business Managers & Business Master can edit team settings.";
   $prb = strapp $prb, "status=$statmsg";
   #$prb = strapp $prb, "teams=$teams";
   $prb = strapp $prb, "execproxylogout=$execproxylogout";
   $prb = strapp $prb, "execdeploypage=$execdeploypage";
   $prb = strapp $prb, "execshowtopcal=$execshowtopcal";

   parseIt $prb;
   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/showteams.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showteams-$$.html";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

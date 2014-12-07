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
# FileName: teamconfirm.cgi
# Purpose: checkconflicts
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
use calfuncs::bizfuncs;   


# Read in all the variables set by the form
   &ReadParse(*input);

   #session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "teamconfirm()";

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
      $login = $sesstab{$biscuit}{'login'};
      if ($login eq "") {
         error("Login is an empty string. Possibly invalid session.\n");
         exit;
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
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business home."); 
      exit;        
   }

   $etitle = $input{title};
   hddebug "title = $etitle";
   $edtype = $input{dtype};
   $edesc = $input{desc};
   hddebug "desc = $edesc";
   $emonth = $input{month};
   $eday = $input{day};
   $eyear = $input{year};
   $erecurtype = $input{recurtype};
   $ehour = $input{hour};
   $emin = $input{min};
   $emeridian = $input{meridian};
   $ezone = $input{zone};
   $eshare = $input{share};
   $efree = $input{free};
   $eatype = $input{atype};
   $edhour = $input{dhour};
   $edmin = $input{dmin};

   $econtact = "";
   $group = "";

   $numbegin = $input{numbegin}; 
   $numend = $input{numend}; 
   hddebug "numbegin = $numbegin, numend = $numend";

   $k = 0;

   # add this entry in the personal calendar of this member
   # we should not add this unless they are part of mandatory invitees.
   # it could be that a secretary is arranging such a meeting
   ## these are concatenated with space.

   $numinvitees = 0;
   $numresources = 0;
   $businesses = ""; 
   $checked = 0; 
   for ($i = $numbegin; $i <= $numend; $i= $i + 1) {
      $memberlogin = $input{"box$k"};
      $checkboxval = $input{$memberlogin};
      hddebug "$memberlogin = $checkboxval";
      if ($checkboxval ne "") {
	 $checked = 1;
	 ## business teams "TeamBusnameAAATeamname
	 if ((index "\L$memberlogin", "\LTeam") != -1) {
	    ($rem, $bizteam) = split ("Team", $memberlogin);
	    $bizteams .= "$bizteam ";
	    $bizteamvals .= $checkboxval. "-";
	    ($biz, $rem) = split("AAA", $bizteam);
	    $businesses .= "$biz ";
	 }
	 ## groups GroupGroupname
	 if ((index "\L$memberlogin", "\LGroup") != -1) {
	    ($rem, $group) = split ("Group", $memberlogin);
	    $groups .= "$group ";
	    $groupvals .= $checkboxval. "-";
	 }
	 ## business members BizmemBusnameAAA$mem
	 if ((index "\L$memberlogin", "\LBizmem") != -1) {
	    ($rem, $bizmem) = split ("Bizmem", $memberlogin);
	    $bizmems .= "$bizmem ";
	    
	    $bizmemvals .= $checkboxval . "-";
	    ($biz, $rem) = split("AAA", $bizmem);
	    $businesses .= "$biz ";
	 } 
	 ## business resources, split businessname and resource
	 ## Resource$busnameAAA$res
	 if ((index "\L$memberlogin", "\LResource") != -1) {
	    ($res, $bizres) = split ("Resource", $memberlogin);
	    $bizresources .= "$bizres ";
	    $bizresourcevals .= $checkboxval . "-";
	    $numresources = $numresources + 1;
	    ($biz, $rem) = split("AAA", $bizres);
	    $businesses .= "$biz ";
	 }
	 ## PersonalMemberLogin
	 if ((index "\L$memberlogin", "\LPersonal") != -1) {
	    ($res, $personal) = split ("Personal", $memberlogin);
            $invitees .= "$personal ";
            $inviteesval .= $checkboxval . "-";
            $numinvitees = $numinvitees + 1;
	 }
      }
      $k = $k + 1;
   }

   if ($checked == 1) {
      $bizteams =~ s/AAA/-/g;
      $bizmems =~ s/AAA/-/g;
      $bizresources =~ s/AAA/-/g;

      $businesses = calfuncs::bizfuncs::dupBusinesses($businesses);

      hddebug "teams = $bizteams";
      hddebug "bizteamvals = $bizteamvals";
      hddebug "resources = $bizresources";
      hddebug "bizresourceval = $bizresourcevals";
      hddebug "bizmems = $bizmems";
      hddebug "bizmemvals = $bizmemvals";
      hddebug "groups = $groups";
      hddebug "groupvals = $groupvals";
      hddebug "invitees = $invitees";
      hddebug "inviteesval = $inviteesval";
      hddebug "bizpeople = $bizpeople";
      hddebug "bizpeoplevals = $bizpeoplevals";

      hddebug "businesses = $businesses";
      hddebug "cleanup = $cleanup";

      $entryno = getkeys();
      $entryno = "$entryno$$";


      ## bizpeoplevals, bizpeople are excluded team members these are null.
      $bizpeoplevals = "";
      $bizpeople = "";
      $update = 0;
      $group = "";

      calfuncs::bizfuncs::updateMeetingEvent($invitees, $inviteesval, $bizteamvals, $bizteams, $bizmemvals, $bizmems, $bizresourcevals, $bizresources, $bizpeoplevals, $bizpeople, $groups, $groupvals, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $group, $econtact, $update, $cleanup);
   }

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

   $rurl = $input{back};
   $rurl =  "$ENV{HDHREP}/$alph/$login/$biscuit-$rurl-redirect_url.html";

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $rurl";
   #system "cat $ENV{HDHREP}/$alph/$login/businessmeet$biscuit.html";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();





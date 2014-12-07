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
# FileName: showinvitememberbusiness.cgi 
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
   #print &HtmlTop ("showinvitememberbusiness.cgi ");
   hddebug ("showinvitememberbusiness.cgi ");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
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
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
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

   $business = trim $input{business};
   hddebug "business = $business";
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execinvitebyloginbusiness = encurl "execinvitebyloginbusiness.cgi";
   } else {
      $execbusiness =  "execbusiness.cgi";
      $execinvitebyloginbusiness = "execinvitebyloginbusiness.cgi";
   } 

   $hs = $input{hs};

   if ((!exists $businesstab{$business}) || ($business eq "")) {
      if ($os ne "nt") {
	 $execcreatebusiness = encurl "execcreatebusiness.cgi";
      } else {
	 $execcreatebusiness =  "execcreatebusiness.cgi";
      } 
      status("$login: Business ($business) does not exist. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

  

   if ($input{'invite'} ne "") {
       $action = "invite";
   }
   if ($input{'search'} ne "") {
       $action = "search";
   }

   if ($input{'searchbyname'} ne "") {
       $action = "searchbyname";
   }

   hddebug "action = $action";

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $sc = $input{sc};

   if ($action ne "searchbyname") {
      $memberlogin = trim $input{memberlogin};
      hddebug "memberlogin (showinvitememberbusiness.cgi()) = $memberlogin";

      if ($memberlogin eq "") {
      if ($os ne "nt") {
         $execinvitationbusiness = encurl "execinvitationbusiness.cgi";
      } else {
         $execinvitationbusiness =  "execinvitationbusiness.cgi";
      }    
         status("$login: You have entered empty login. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitationbusiness&p1=biscuit&p2=businesslist&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&businesslist=$business&f=sgc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
         exit;
      }

      if (!exists($logtab{$memberlogin})) {
       	 status("$login: The member login ($memberlogin) is not willing to share his or her ID and cannot receive invitations. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitebyloginbusiness&p1=biscuit&p2=business&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite another member by login.");
         exit;
      }

      if (exists($logtab{$memberlogin})) {
         if ($logtab{$memberlogin}{checkid} eq "") {
         	 status("$login: The member login ($memberlogin) is not willing to share his or her ID and cannot receive invitations. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitebyloginbusiness&p1=biscuit&p2=business&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite another member by login.");
             exit;
         }
   
         tie %surveytab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/surveytab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
		'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority',
		 'editcal', 'calpeople'] };

         if ($surveytab{$memberlogin}{'calinvite'} eq "") {
	    status("$login: The member login ($memberlogin) specified prefers not to receive invitations from others.  <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitebyloginbusiness&p1=biscuit&p2=business&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite another member by login.");
           exit;
         }
      }

   

      $membername = $logtab{$memberlogin}{fname} . " " . $logtab{$memberlogin}{lname};

      if (-d "$ENV{HDDATA}/business/business/$business/peopletab") {
         tie %peopletab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['login', 'business']};

         if (exists($peopletab{$memberlogin})) {
	    status("$login: The ($memberlogin, $membername) is already a member of ($business). <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitebyloginbusiness&p1=biscuit&p2=business&p3=jp&pnum=4&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite another member by login.");
	    exit;
         }
      }

      $alphaindex = substr $login, 0, 1;
      $alphaindex = $alphaindex . '-index';
 
      if ($action eq "invite") { 
         $prml = "";
         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "logo=$logo";
         $prml = strapp $prml, "label=$label";
         if ($os ne "nt") {
            $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
            $prml = strapp $prml, "formenc=$formenc";
	    $execsendmemberinvitebusiness = encurl "execsendmemberinvitebusiness.cgi";
         } else {
            $prml = strapp $prml, "formenc=";
	    $execsendmemberinvitebusiness = "execsendmemberinvitebusiness.cgi";
         }
         $prml = strapp $prml, "template=$ENV{HDTMPL}/invitethismemberbusiness.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/invitethismemberbusiness-$$.html";
         $prml = strapp $prml, "biscuit=$biscuit";
         $welcome = "Welcome";
         $prml = strapp $prml, "welcome=$welcome";
         $prml = strapp $prml, "login=$login";
         $prml = strapp $prml, "HDLIC=$HDLIC";
         $prml = strapp $prml, "ip=$ip";
         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "hs=$hs";
         $prml = strapp $prml, "vdomain=$vdomain";
         $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsendmemberinvitebusiness\">";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=memberlogin>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=businessmanager>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=memberlogin VALUE=$memberlogin>";
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
         $prml = strapp $prml, "memberlogin=$memberlogin";
         $prml = strapp $prml, "membername=$membername";
         parseIt $prml;

         #system "cat $ENV{HDTMPL}/content.html";
         #system "cat $ENV{HDHREP}/$alphaindex/$login/invitethismemberbusiness.html";
         hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/invitethismemberbusiness-$$.html";
      }
   }

   if (($action eq "search") || ($action eq "searchbyname")) {
      $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
      $msg .= "<TR BGCOLOR=dddddd>";
      $msg .= "<TD></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Login</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">First Name</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Last Name</FONT></TD>";
      $msg .= "</TR>";
      $smsg = $msg;
      $umsg = $msg;
      $cntr = 0;

      #it could be any of the data variables.
      if ($action ne "searchbyname") {
         $memlg = trim $input{'memberlogin'};
         $memlg = "\L$memlg";
         hddebug "memberlogin = $memlg";
      } else {
         $firstname = trim $input{'firstname'};
         $firstname = "\L$firstname";
         $lastname = trim $input{'lastname'};
         $lastname = "\L$lastname";
         if (($firstname eq "") || ($lastname eq "")) { 
	    if ($os ne "nt") {
	       $execinvitebynamebusiness = encurl "execinvitebynamebusiness.cgi"; 
            } else {
	       $execinvitebynamebusiness = "execinvitebynamebusiness.cgi"; 
            }
	    status("$login: Either Firstname or Lastname is empty. Enter non empty names. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitebynamebusiness&p1=biscuit&p2=business&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=6\">here</a> to invite a member. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=6\">here</a> to return to business home.");
	    exit;
         }
      }

      #display all results 

      foreach $mem (sort keys %logtab) {
          if ($action ne "searchbyname") {
             if ( ((index "\L$logtab{$mem}{login}", "\L$memlg") != -1) && 
                ($logtab{$mem}{'checkid'} eq  "CHECKED") && 
                ($surveytab{$mem}{'calinvite'} eq "CHECKED") ) { 
                 $cntr = $cntr +1;
                 #hddebug "cntr = $cntr"; 
             } else {
                 next;
             }
          } 

	  if ($action eq "searchbyname") {
             if ( ((index "\L$logtab{$mem}{fname}", $firstname) != -1) || 
                ((index "\L$logtab{$mem}{fname}",  $lastname) != -1) && 
                ($logtab{$mem}{'checkid'} eq  "CHECKED") && 
                ($surveytab{$mem}{'calinvite'} eq "CHECKED")) {
                  $cntr = $cntr +1;
	     } else {
	        next;
	     }
          }

          # display only 5 logins that were most recently accessed at anytime.
          if ($cntr == 6) {
	      last;
          }

          $msg = "<TR>";
          $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=RADIO NAME=memberlogin VALUE=\"$mem\"></FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{login} &nbsp;</FONT></TD>";
          #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$res &nbsp;</FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'fname'} &nbsp;</FONT></TD>";
           #hddebug "showmembersbylogin() login = $mem";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'lname'} &nbsp;</FONT></TD>";
          $msg .= "</TR>";

          if (exists $logtab{$mem}) {
             $smsg .= $msg;
          } else {
             $umsg .= $msg;
          }
      }

      #hddebug "smsg = $smsg";
      if ($cntr == 0) {
         if ($action eq "searchbyname") {
            status("$login: No matches were found with ($firstname, $lastname) or it could be that the  ($firstname, $lastname) has not given permission to receive invitations.");
            exit; 
         } else {
            status("$login: No matches were found with ($memlg) or it could be that the  ($memlg) login has not given permission to receive invitations.");
            exit; 
	 }
      }
  
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      $smsg = adjusturl $smsg;

      $prb = "";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";
      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execshowinvitememberbusiness = encurl "execshowinvitememberbusiness.cgi";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";

      } else {
         $prb = strapp $prb, "formenc=";
         $execshowinvitememberbusiness = "execshowinvitememberbusiness.cgi";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";

      }
      $prb = strapp $prb, "template=$ENV{HDTMPL}/showmembersbylogin.html";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/showmembersbylogin-$$.html";
      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "jp=$jp";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execshowinvitememberbusiness\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=memberlogin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=invite>";
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
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";


      $prb = strapp $prb, "members=$smsg";
      if ($cntr == 5) {
          $stat = adjusturl "<FONT COLOR=ff0000 FACE=\"Verdana\" SIZE=\"2\">We display only first 5 matches at a time for security reasons. The results have been truncated. You can narrow down the search by entering a specific keyword.</FONT><BR><BR>";
      } else {
          $stat = "";
      }
      $prb = strapp $prb, "status=$stat";    

      parseIt $prb;
      #system "cat $ENV{HDTMPL}/content.html";
      #system "cat $ENV{HDHREP}/$alphaindex/$login/showmembersbylogin.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showmembersbylogin-$$.html";
   }


   tied(%sesstab)->sync();
   tied(%logsess)->sync();

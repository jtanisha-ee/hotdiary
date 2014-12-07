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
# FileName: membersdir.cgi 
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
   #print &HtmlTop ("membersdir.cgi ");
   hddebug ("membersdir.cgi ");

   $vdomain = trim $input{'vdomain'};
   
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
   hddebug "biscuit = $biscuit";
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
  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
  
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


   
   tie %peopletab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['login', 'business']};

   if (!exists($peopletab{$login})) {
      status("$login: You do not have permission to view business directory. You have to be a member of ($business) to view business directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

 
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $sc = $input{sc};


   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   #$msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Login</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Email</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Phone</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Pager</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Fax</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Calendar</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Directions</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Edit</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;
   $cntr = 0;

 
   if ($os ne "nt") {
      $execshowcontactlist = encurl "execshowcontactlist.cgi";
      $execaddbusinesscontact = encurl "execaddbusinesscontact.cgi";
   } else {
      $execshowcontactlist = "execshowcontactlist.cgi";
      $execaddbusinesscontact = "execaddbusinesscontact.cgi";
   }
 
   if (!(-d "$ENV{HDDATA}/business/business/$business/directory/emptab"))  {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/directory/emptab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/directory/emptab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/directory/emptab";
      #status ("$login: You currently do not have any contacts in the Members directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitationbusiness&p1=biscuit&p2=businesslist&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite."); 
   #   exit;
   }

   $fromstreet = replaceblanks $logtab{$login}{street};
   $fromcity = replaceblanks $logtab{$login}{city};
   $fromstate = replaceblanks $logtab{$login}{state};

   # bind emptab table vars
   tie %emptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/emptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };
   
   foreach $mem (sort keys %peopletab) {
      $cntr = $cntr +1;
      $msg = "<TR>";
      #$msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$mem></FONT></TD>"; 
      $cdir .= $mem;
      $cdir .= " ";
      if (exists $emptab{$mem}) {
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$emptab{$mem}{'fname'}&nbsp;$emptab{$mem}{'lname'} &nbsp;</FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$mem &nbsp;</FONT></TD>";
          $dbpagertype = $emptab{$mem}{pagertype};
          $email = $emptab{$mem}{email};
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"mailto:$email\">$email</a> &nbsp;</FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$emptab{$mem}{'bphone'}&nbsp;</FONT></TD>";
          $dbpagertype = $emptab{$mem}{pagertype};
          $dbpager = $emptab{$mem}{pager};
          $uname = $emptab{$mem}{fname}. " ". $emptab{$mem}{lname}; 
          ($dbfax = $emptab{$mem}{'fax'}) =~ s/\n/\n<BR>/g;
          $tostreet = replaceblanks $emptab{$mem}{street};
          $tocity = replaceblanks $emptab{$mem}{city};
          $tostate = replaceblanks $emptab{$mem}{state};

      } else {
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'fname'}&nbsp;$logtab{$mem}{'lname'} &nbsp;</FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$mem &nbsp;</FONT></TD>";
          $email = $logtab{$mem}{email};
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"mailto:$email\">$email</a> &nbsp;</FONT></TD>";
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'bphone'}&nbsp;</FONT></TD>";
          $dbpagertype = $logtab{$mem}{pagertype};
          $dbpager = $logtab{$mem}{pager};
          $uname = $logtab{$mem}{fname}. " ". $logtab{$mem}{lname}; 
          ($dbfax = $logtab{$mem}{'fax'}) =~ s/\n/\n<BR>/g;
          $tostreet = $logtab{$mem}{street};
          $tocity = $logtab{$mem}{city};
          $tostate = $logtab{$mem}{state};
      }

      $pager = $dbpager;
      $dbpagertype = replaceblanks($dbpagertype);
      $dbpager = replaceblanks($dbpager);
      $uname = $uname;
      $uname = replaceblanks($uname);
      $to = replaceblanks($to);
      $pt = replaceblanks($pt);
      $thispage = replaceblanks($thispage);
      $thispage = "/rep/$mem/ser$title$biscuit$page_num.html";
      if ($os ne "nt") {
         $execshowbusinesspage = encurl "execshowbusinesspage.cgi";
      } else {
          $execshowbusinesspage = "execshowbusinesspage.cgi";
      }
      $pageurl = adjusturl("execdogeneric.cgi?pnum=8&p0=$execshowbusinesspage&p1=biscuit&p2=thispage&p3=to&p4=pt&p5=uname&p6=business&p7=dirtype&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbpager&pt=$dbpagertype&uname=$uname&business=$business&dirtype=membersdir&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$pageurl\">$pager</a>&nbsp;</FONT></TD>";
      $fax = $dbfax;
      $dbfax = getPhoneDigits $dbfax;
      $dbfax = replaceblanks($dbfax);
      if ($os ne "nt") {
         $execshowbusinessfax = encurl "execshowbusinessfax.cgi";
      } else {
         $execshowbusinessfax = "execshowbusinessfax.cgi";
      }
      $faxurl = adjusturl("execdogeneric.cgi?pnum=7&p0=$execshowbusinessfax&p1=biscuit&p2=thispage&p3=to&p4=uname&p5=business&p6=dirtype&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbfax&uname=$uname&business=$business&dirtype=membersdir&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6"); 
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$faxurl\">$fax</a>&nbsp;</FONT></TD>";
    
      if ($logtab{$mem}{calpublish} eq "CHECKED") { 
         $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/members/$mem\" target=_main>Calendar</a>&nbsp;</FONT></TD>";
      } else {
         $msg .= "<TD>&nbsp;</TD>";
      }
      $directions = adjusturl "http://www.zip2.com/scripts/map.dll?mad1=$fromstreet&mct1=$fromcity&mst1=$fromstate&mad2=$tostreet&mct2=$tocity&mst2=$tostate&type=gis&mwt=350&mht=280&mwt1=350&mht1=280&mwt2=350&mht2=280&mwt3=350&mht3=280&method=d2d&ck=21439101&userid=55724010&userpw=xtv0J_txAwt8tE_FD0C&version=663922&sType=street&adrVer=918629102&ver=d3.0&GetDir.x=Get+Directions";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"$directions\">Directions</a>&nbsp;</FONT></TD>";

      if ($os ne "nt") {
         $execshowbusinessother = encurl "execshowbusinessother.cgi";
      } else {
         $execshowbusinessother = encurl "execshowbusinessother.cgi";
      }
      $moreurl = adjusturl("execdogeneric.cgi?pnum=4&p0=$execshowbusinessother&p1=biscuit&p2=business&p3=ulogin&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=$mem&business=$business&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$moreurl\">Edit</a>&nbsp;</FONT></TD>";
      $msg .= "</TR>";

      if ((exists $logtab{$mem}) || (exists $emptab{$mem})) {
         $smsg .= $msg;
      } else {
         $umsg .= $msg;
      }
   }


   if ($cntr == 0) {
      status ("$login: You currently do not have any contacts in the Members directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execinvitationbusiness&p1=biscuit&p2=businesslist&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to invite."); 
      exit;
   }

   (@hshcdir) = split " ", $cdir; 
   foreach $cn (@hshcdir) {
       $cn = trim $cn;
   }
 
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      $smsg = adjusturl $smsg;

      $prb = "";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";
      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execmembersdir = encurl "execmembersdir.cgi";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execmembersdir = "execmembersdir.cgi";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
      }
      $alphaindex = substr $login, 0, 1;
      $alphaindex = $alphaindex . '-index';

      $prb = strapp $prb, "template=$ENV{HDTMPL}/membersdir.html";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/membersdir-$$.html";
      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execmembersdir\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=numend>";

      #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 6;
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
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
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
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "bizdir=$smsg";
      $prb = strapp $prb, "status=";
      $bizlabel = "$business - Members Directory";
      $prb = strapp $prb, "bizlabel=$bizlabel";
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
      parseIt $prb;

      #system "cat $ENV{HDTMPL}/content.html";
      #system "cat $ENV{HDHREP}/$alphaindex/$login/membersdir.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/membersdir-$$.html";
     

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

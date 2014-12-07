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
# FileName: teamsdir.cgi 
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

   hddebug("teamsdir.cgi ");

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
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
   }
 
   $rh = $input{rh};
   if ($business eq "") {   
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business home."); 
      exit;        
   }


   
   tie %peopletab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['login', 'business']};

   if (!exists($peopletab{$login})) {
      status("$login: You do not have permission to view business directory. You have to be a member of ($business) to view business directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business directory.");
      exit;
   }

 
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $sc = $input{sc};


   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   #$msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Team</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Supervisor</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Project Code</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Location Code</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">No.of People </FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Calendar</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Email</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Phone</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Pager</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Fax</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">More</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;

 
   if ($os ne "nt") {
      $execshowcontactlist = encurl "execshowcontactlist.cgi";
      $execaddbusinesscontact = encurl "execaddbusinesscontact.cgi";
      $execbusinesscalclient = encurl "execbusinesscalclient.cgi";
      $execshowmoreteams = encurl "execshowmoreteams.cgi";
   } else {
      $execshowcontactlist = "execshowcontactlist.cgi";
      $execaddbusinesscontact = "execaddbusinesscontact.cgi";
      $execbusinesscalclient = "execbusinesscalclient.cgi";
      $execshowmoreteams = "execshowmoreteams.cgi";
   }
 
   if (!(-d "$ENV{HDDATA}/business/business/$business/teams/teamtab"))  {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/teamtab";
      status ("$login: You currently do not have any teams in the business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business directory.");
      exit;
   }

   $cntr = 0;
   
   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
	ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode',
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] };

   foreach $team (sort keys %teamtab) {
      $msg = "<TR>";
      $cdir .= $team;
      $cdir .= " ";
      $cntr = $cntr + 1;
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$team}{'teamname'}&nbsp;</FONT></TD>";
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$team}{'supervisor'}&nbsp;</FONT></TD>";
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$team}{'projcode'}&nbsp;</FONT></TD>";
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$team}{'loccode'}&nbsp;</FONT></TD>";

      $numpeople = 0;
      if (-d ("$ENV{HDDATA}/business/business/$business/teams/$team/teampeopletab")) {
         tie %teampeopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/teampeopletab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER => ['login']};

	 hddebug " exists $team";
	 (@hshnumpeople) = (sort keys %teampeopletab); 
	 $numpeople = $#hshnumpeople;
      }

      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$numpeople</FONT></TD>";
      $calurl = adjusturl("execdogeneric.cgi?pnum=4&p0=$execbusinesscalclient&p1=biscuit&p2=teamname&p3=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&teamname=$team&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&enum=5"); 
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"$calurl\">Calendar</a>&nbsp;</FONT></TD>";
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"mailto:$email\">$teamtab{$team}{email}</a> &nbsp;</FONT></TD>";
      $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\">$teamtab{$team}{'bphone'}&nbsp;</FONT></TD>";
      $dbpagertype = $teamtab{$team}{pagertype};
      $dbpager = $teamtab{$team}{pager};
      ($dbfax = $teamtab{$team}{'fax'}) =~ s/\n/\n<BR>/g;
      $pager = $dbpager;
      $dbpagertype = replaceblanks($dbpagertype);
      $dbpager = replaceblanks($dbpager);
      $newlogo = replaceblanks($logo);

      #$pageurl = adjusturl("/cgi-bin/execshowbusinesspage.cgi?thispage=/rep/$mem/ser$title$biscuit$page_num.html&to=$dbpager&biscuit=$biscuit&pt=$dbpagertype&vdomain=$vdomain&rh=$rh&hs=$hs&business=$business&HDLIC=$HDLIC&uname=$uname&logo=$newlogo");
      $thispage = "/rep/$mem/ser$title$biscuit$page_num.html";
      if ($os ne "nt") {
          $execshowbusinesspage = encurl "execshowbusinesspage.cgi";
      } else {
          $execshowbusinesspage = "execshowbusinesspage.cgi";
      }

      $pageurl = adjusturl("execdogeneric.cgi?pnum=8&p0=$execshowbusinesspage&p1=biscuit&p2=thispage&p3=to&p4=pt&p5=uname&p6=business&p7=dirtype&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbpager&pt=$dbpagertype&uname=$uname&business=$business&dirtype=teamdir&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&enum=5");
       $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$pageurl\">$pager</a>&nbsp;</FONT></TD>";


       $fax = $dbfax;
       $dbfax = getPhoneDigits $dbfax;
       $dbfax = replaceblanks($dbfax);
       if ($os ne "nt") {
          $execshowbusinessfax = encurl "execshowbusinessfax.cgi";
       } else {
          $execshowbusinessfax = "execshowbusinessfax.cgi";
       }

       $faxurl = adjusturl("execdogeneric.cgi?pnum=7&p0=$execshowbusinessfax&p1=biscuit&p2=thispage&p3=to&p4=uname&p5=business&p6=dirtype&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbfax&uname=$uname&business=$business&dirtype=teamdir&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&enum=5"); 

       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$faxurl\">$fax</a>&nbsp;</FONT></TD>";

       $contacttype = "Teams";
        
       $moreurl = adjusturl("execdogeneric.cgi?pnum=5&p0=$execshowmoreteams&p1=biscuit&p2=business&p3=entryno&p4=contacttype&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&entryno=$team&contacttype=$contacttype&business=$business&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&enum=5");
       $msg .= "<TD ALIGN=TOP><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$moreurl\">More</a>&nbsp;</FONT></TD>";
       $msg .= "</TR>";

       if (exists $teamtab{$team}) {
          $smsg .= $msg;
       } else {
          $umsg .= $msg;
       }
   }

   if ($cntr == 0) {
      status ("$login: You currently do not have any teams in the teams directory. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execshowcontactlist&p1=biscuit&p2=businesslist&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&businesslist=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to return to business directory.");
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
         $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execteamsdir = encurl "execteamsdir.cgi"; 
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execteamsdir = "execteamsdir.cgi"; 
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
      }

      $alph = substr $login, 0, 1;
      $alph = $alph . '-index';

      $prb = strapp $prb, "template=$ENV{HDTMPL}/teamsdir.html";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alph/$login/teamsdir-$$.html";
      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execteamsdir\">";
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
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=4>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
      $hiddenvars = adjusturl $hiddenvars;
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "bizdir=$smsg";
      $bizlabel = "$business - Teams Rolodex";
      $prb = strapp $prb, "bizlabel=$bizlabel";
      $prb = strapp $prb, "status=";
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
      parseIt $prb;

      #system "cat $ENV{HDTMPL}/content.html";
      #system "cat $ENV{HDHREP}/$alph/$login/teamsdir.html";
      hdsystemcat "$ENV{HDHREP}/$alph/$login/teamsdir-$$.html";
     

   # reset the timer.

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

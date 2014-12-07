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
# FileName: memo.cgi
# Purpose: Top screen for memo
# Creation Date: 03-04-2000
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
use MIME::Base64;

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("memo.cgi");

   $vdomain = trim $input{'vdomain'};

   $hdcookie = $input{'HTTP_COOKIE'};
   $login = getlogin($hdcookie);

   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";
   $rh = $input{rh};
   $g = $input{g};
   hddebug "g = $g";
   $os = $input{os}; 
   $biscuit = $input{'biscuit'};
   $hs = $input{'hs'};
   if ($os ne "nt") {
      $execmemo = encurl "execmemo.cgi";
   } else {
      $execmemo = "execmemo.cgi";
   }
   $show = $input{show};
   $sortby = $input{sortby};
   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                 'listed' ] };
   $memoprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&pnum=5&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\">here</FONT></a>";
   if ( ( $g ne "") && (!exists $lgrouptab{$g}) ) {
      status "Group name ($g) does not exist. Please select a valid group name. Click $memoprog to return to Memo Manager.";
      exit;
   }


   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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

   $fchar = substr $login, 0, 1;
   $alphaindex = $fchar . '-index';

   if (! -d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab") {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
   }

   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
	'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   if (! -d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab") {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
   }

  # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
	'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   if ( ($g ne "") && (!exists $sgrouptab{$g}) && (!exists $fgrouptab{$g}) ) {
      status "You are neither the founder nor the subscriber of the group $g. Please check the group name and try again. Click $memoprog to return to Memo Manager."; 
      exit;
   }
 

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();

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

   if ( (validvdomain($vdomain) eq "1" ) ) {
     $label = "";
     $logo = "";
   }

   if ($jp eq "") {
       $color = "white";
   } else {
       $color = "black";
   }

   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   if ($label ne "") {
      $label = adjusturl $label;
   }

   $prml = strapp $prml, "logo=$logo";
   $sc = $input{sc};

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execeditmemo =  encurl "execeditmemo.cgi";
      $execaddmemo =  encurl "execaddmemo.cgi";
      $execdeletememo =  encurl "execdeletememo.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execeditmemo =  "execeditmemo.cgi";
      $execaddmemo =  "execaddmemo.cgi";
      $execdeletememo =  "execdeletememo.cgi";
   }

   
   if ($g eq "") {
      if (! -d "$ENV{HDDATA}/$alphaindex/$login/todotab") {
         system "mkdir -p $ENV{HDDATA}/$alphaindex/$login/todotab";
         system "chmod 755 $ENV{HDDATA}/$alphaindex/$login/todotab";
      }
      # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/todotab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share',
              'hour', 'banner'] };
   } else {
      if (! -d "$ENV{HDDATA}/listed/groups/$g/todotab") {
         system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$g/todotab";
      }
      # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };

   }

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/memo.html") ) {
      $template = "$ENV{HDDATA}/$alphjp/$jp/templates/memo.html";
   } else {
      $template = "$ENV{HDTMPL}/memo.html";
   }
   $prml = strapp $prml, "template=$template";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/memo-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execaddmemo=$execaddmemo";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "label1=Memo Manager";
   $prml = strapp $prml, "title=$label";

   $sessionheader = getsessionheader($jp);
   $sessionfooter = getsessionfooter($jp);
   $css = getcss($jp);

   $prml = strapp $prml, "css=$css";
   $prml = strapp $prml, "sessionheader=$sessionheader";
   $prml = strapp $prml, "sessionfooter=$sessionfooter";

   $theader = getTheader($jp);
   $tmiddle = getTmiddle($jp);
   $tfooter = getTfooter($jp);
   $prml = strapp $prml, "theader=$theader";
   $prml = strapp $prml, "tmiddle=$tmiddle";
   $prml = strapp $prml, "tfooter=$tfooter";

   $prml = strapp $prml, "g=$g";
   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist < 0) && ($#glist1 < 0) ) {
      $lab100 = adjusturl "<BR><font color=$color size=2>Group Memos</font><BR><FONT SIZE=1>Groups Not Created Or Subscribed</FONT>";
      $prml = strapp $prml, "memotype=$lab100";
   } else {
      #if ($login ne "mjoshi") {
      #   $prml = strapp $prml, "memotype=";
      #} else {
         $memotype = "<BR><font color=$color size=2>Group Memos </font><p><TABLE CELLPADDING=0 CELLSPACING=0 WIDTH=\"30%\" BORDER=0>";
         $memotype .= "<TR><TD>";
         $memotype .= "<FONT SIZE=2><SELECT NAME=selgroup SIZE=2>";
         foreach $grp (keys %fgrouptab) {
            $memotype .= "<OPTION>$grp";
         }
         foreach $grp (keys %sgrouptab) {
            $memotype .= "<OPTION>$grp";
         }
         $memotype .= "</SELECT></FONT>";
         $memotype .= "</TD>";
         $memotype .= "<TD>";
         $memotype .= "&nbsp;<INPUT TYPE=SUBMIT NAME=Go VALUE=Go>";
         $memotype .= "</TD></TR></TABLE>";
         $memotype = adjusturl $memotype;
         $prml = strapp $prml, "memotype=$memotype";
      #}
   }

   $memolist = "";
      $memotitle = "<p>";
      if ($g eq "") {
         $memotitle .= "<font color=$color size=2><b>Personal Memo</b></font><p>";
      } else {
         $memotitle .= "<font color=$color size=2><b>Group Memo ($g) </b></font><p>";
      }
      $memolist .= "<CENTER>$memotitle</CENTER> <TABLE WIDTH=\"100%\" BORDERCOLOR=ee00ee CELLPADDING=5 CELLSPACING=0 BORDER=1>";
   if ($show eq "pending") {
      $memoprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Show<BR>All</FONT></a>";
      $memodateprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=Date&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Sort</FONT></a>";
      $memopriorityprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=Priority&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Sort</FONT></a>";
   } else {
      $memoprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=pending&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Show Undone</FONT></a>";
      $memodateprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=Date&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Sort</FONT></a>";
      $memopriorityprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$g&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=Priority&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>Sort</FONT></a>";
   }
   if ($sortby eq "Date") {
      $datecolor = "BGCOLOR=pink";
      $pcolor = "BGCOLOR=1f1f7f";
   } else {
      $datecolor = "BGCOLOR=1f1f7f";
      $pcolor = "BGCOLOR=pink";
   }
   if ($show eq "pending") {
      $scolor = "BGCOLOR=green";
   }
   if ( ( ($g eq "") && (-d "$ENV{HDDATA}/$alphaindex/$login/todotab") ) ||
        ( ($g ne "") && (-d "$ENV{HDDATA}/listed/groups/$g/todotab") ) ) {
      $memolist .= "<TR BGCOLOR=1f1f7f WIDTH=\"100%\">";
      $memolist .= "<TD WIDTH=\"5%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Sel</FONT></TD>";
      $memolist .= "<TD WIDTH=\"5%\" ALIGN=CENTER $pcolor><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>P</FONT><BR><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>$memopriorityprog</FONT></TD>";
      $memolist .= "<TD WIDTH=\"20%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Subject</FONT></TD>";
      $memolist .= "<TD WIDTH=\"50%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\"  COLOR=ffffff SIZE=2>Memo Description</FONT></TD>";
      $memolist .= "<TD WIDTH=\"10%\" $scolor ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Status</FONT><BR><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1><CENTER>$memoprog</CENTER></FONT></TD>";
      $memolist .= "<TD WIDTH=\"10%\" ALIGN=CENTER $datecolor><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Due Date</FONT><BR><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=1>$memodateprog</FONT></TD>";
      $memolist .= "</TR>";

      $cdir = "";

      #hddebug "came here";
      #hddebug "again g = $g";
      if ($sortby eq "Date") {
         if ($g eq "") {
            (@entrynohsh) = sortmemodate ($login);
         } else {
            (@entrynohsh) = sortgroupmemodate ($g);
         }
      } else {
         if ($g eq "") {
            (@entrynohsh) = sortmemo ($login);
         } else {
            (@entrynohsh) = sortgroupmemo ($g);
         }
      }
      #foreach $item (keys %todotab) {
      $cnt = 0;
      foreach $item (@entrynohsh) {
         #hddebug "item = $item";
         if ($item eq "") {
            next;
         }
         if (!exists($todotab{$item})) {
           next;
         }
         $status = $todotab{$item}{status};
         if ($show eq "pending") {
            if ($status eq "Done") {
               next;
            }
         }
         $cnt = $cnt + 1;
         if ($cnt % 2) {
            $bgcolor = "BGCOLOR=dddddd";
         } else {
            $bgcolor = "BGCOLOR=ffffff";
         }
         $memolist .= "<TR WIDTH=\"100%\" $bgcolor>";
         $entry = $todotab{$item}{entryno};
         #hddebug "entry = $entry";
         $memolist .= "<TD WIDTH=\"5%\" ALIGN=CENTER VALIGN=CENTER><INPUT TYPE=CHECKBOX NAME=$entry></TD>";
         $cdir .= $entry;
         $cdir .= " ";
         
         $priority = $todotab{$item}{priority};
         #hddebug "priority = $priority";
         $memolist .= "<TD WIDTH=\"5%\" ALIGN=CENTER VALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=890382 SIZE=2>$priority</FONT></TD>";
         $subject = $todotab{$item}{subject};
         #hddebug "subject = $subject";
         $subjecturl = adjusturl "execdogeneric.jsp?pnum=5&p0=$execeditmemo&p1=biscuit&p2=entry&p3=jp&p4=g&g=$g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&entry=$entry&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&jp=$jp";
         $memolist .= "<TD WIDTH=\"20%\" ALIGN=CENTER VALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=1029ff SIZE=2><a href=\"http://$vdomain/cgi-bin/$rh/$subjecturl\">$subject</a>&nbsp;</FONT></TD>";
         #$desc = decode_base64 $todotab{$item}{desc};
         $desc = $todotab{$item}{desc};
         $desc =~ s/\n/<BR>/g;
         #hddebug "desc = $desc";
         $memolist .= "<TD WIDTH=\"60%\" ALIGN=LEFT VALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ee01ff SIZE=2>$desc &nbsp;</FONT></TD>";
         #hddebug "status = $status";
         $memolist .= "<TD WIDTH=\"10%\" ALIGN=CENTER VALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=0e1f3d SIZE=2>$status</FONT></TD>";
         $month = $todotab{$item}{month};
         $day = $todotab{$item}{day};
         $year = $todotab{$item}{year};
         $memolist .= "<TD WIDTH=\"10%\" ALIGN=CENTER VALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=2205dd SIZE=2>$month/$day/$year&nbsp;</FONT></TD>";
         $memolist .= "</TR>";
      }
      $memolist .= "</TABLE>";
      $memolist = adjusturl $memolist;
   }

   (@hshcdir) = split " ", $cdir;
   $prml = strapp $prml, "memolist=$memolist";
   if ($g ne "") {
      $pmemo = adjusturl "&nbsp;&nbsp;<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&pnum=5&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">Go To Personal Memo</a>";
      $prml = strapp $prml, "pmemo=$pmemo";
   } else {
      $prml = strapp $prml, "pmemo=";
   }

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execdeletememo\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=Delete>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=Go>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=selgroup>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=group>";

   #values of checkboxes as each parameter
   $k = 0;
   $mcntr = 9;
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=group VALUE=$g>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
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

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/memo.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/memo-$$.html";

   hddebug "completed memo";
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   #tied(%todotab)->sync();

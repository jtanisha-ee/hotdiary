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
# FileName: recheckconflict.cgi
# Purpose: recheckconflicts
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


# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "recheckconflict()";

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
      status("$login: Please specify a non empty business name. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;
   }

   if (!exists $businesstab{$business}) {   
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home."); 
      exit;        
   }

   $res = 0;
   $grp = 0;
   $biz = 0;
   $mem = 0;
   $k = 0;
   for ($i = $selbegin; $i <= $selend; $i= $i + 1) {
      $memberlogin = $input{"box$k"};
      $checkboxval = $input{$memberlogin};
      #hddebug "checkboxval = $checkboxval";

      if ($checkboxval eq "on") {
         #hddebug "action = $action";
	 if (index(memberlogin, "Res-") != -1) {
            ($res, $resname) = split("Res-", $memberlogin);
	    $resources[$res] = $resname;
	    $res = $res + 1;
	 } else {
	    if (index(memberlogin, "Grp-") != -1) {
               ($grp, $grpname) = split("Grp-", $memberlogin);
	       $groups[grp] = $grpname;
	       $grp = $grp + 1;
	    } else {
	       if (index(memberlogin, ":") != -1) {
	          $hshbusteams[$biz] = $memberlogin;
	          $biz = $biz + 1;
	       } else {
                 $hshmembers[$mem] = $memberlogin;
	         $mem = $mem + 1;
	       }
	    }
	 }
      }
      $k = $k + 1;
   }

   if (($hshmembers eq "") && ($groups eq "") && 
      ($hshbusteams eq "") && ($resources eq "")) {
      status("$login: Please select atleast one of the invitees or resources.");
      exit;
   }


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
 
   $chour = $input{chour};
   $cday = $input{cday};
   $cweek = $input{cweek};
   $cmonth = $input{cmonth};

   if (($cmonth == 0 ) && ($cday == 0) && ($cweek == 0) && ($chour == 0)) {
      status("$login: Please specify atleast one(Months, Weeks, Days, Hours) of the Check Availability.");
      exit;
   }

#hddebug "chour = $chour";
#hddebug "cday = $cday";
#hddebug "cweek = $cweek";
#hddebug "cmonth = $cmonth";
$pixsec = 0;

   $images = "$ENV{HDHTML}/images";

   if ($cmonth != 0 ) { 
      $pixsec = 3600 * 24 * 30 * $cmonth;
      if ($cmonth == 1) {
	 $pixsec = 24 * 30 * 3600/400;
         $time .= "<IMG SRC=\"$images/wk1-4.gif\" WIDTH=100 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/wk2-4.gif\" WIDTH=100 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/wk3-4.gif\" WIDTH=100 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/wk4-4.gif\" WIDTH=100 HEIGHT=30>";
      }
      if ($cmonth == 2) {
	 $pixsec = 24 * 30 * 3600/200;
         $time .= "<IMG SRC=\"$images/month1-2.gif\" WIDTH=200 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/month2-2.gif\" WIDTH=200 HEIGHT=30>";
      }
      if ($cmonth == 3) {
	 $pixsec = 24 * 30 * 3600/133;
         $time .= "<IMG SRC=\"$images/month1-3.gif\" WIDTH=133 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/month2-3.gif\" WIDTH=133 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/month3-3.gif\" WIDTH=133 HEIGHT=30>";
      }
      if ($cmonth == 12) {
	 $pixsec = 24 * 30 * 3600/33;
         $time .= "<IMG SRC=\"$images/s1-2.gif\" WIDTH=200 HEIGHT=30>";
         $time .= "<IMG SRC=\"$images/s2-2.gif\" WIDTH=200 HEIGHT=30>";
      }
   } else  {
      if ($cweek != 0) {
	$pixsec = 3600 * 24 * 7 * $cweek;
	if ($cweek == 1) {
	  $pixsec = 3600 * 24; 
	  $pixsec = $pixsec/57; 
          $time .= "<IMG SRC=\"$images/monday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/tuesday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/wednesday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/thursday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/friday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/saturday.gif\" WIDTH=57 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/sunday.gif\" WIDTH=57 HEIGHT=30>";
        }
	if ($cweek == 2) {
	  $pixsec = 3600 * 24 * 7/200;
          $time .= "<IMG SRC=\"$images/wk1-2.gif\" WIDTH=200 HEIGHT=30 BORDER=0>";
          $time .= "<IMG SRC=\"$images/wk2-2.gif\" WIDTH=200 HEIGHT=30 BORDER=0>";
	}
	if ($cweek == 3) {
	  $pixsec = 3600 * 24 * 7/133; 
          $time .= "<IMG SRC=\"$images/wk1-3.gif\" WIDTH=133 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/wk2-3.gif\" WIDTH=133 HEIGHT=30>";
          $time .= "<IMG SRC=\"$images/wk3-3.gif\" WIDTH=133 HEIGHT=30>";
	}
	if ($cweek == 4) {
	   $pixsec = 24 * 3600 * 7/100;
           $time .= "<IMG SRC=\"$images/wk1-4.gif\" WIDTH=100 HEIGHT=30>";
           $time .= "<IMG SRC=\"$images/wk2-4.gif\" WIDTH=100 HEIGHT=30>";
           $time .= "<IMG SRC=\"$images/wk3-4.gif\" WIDTH=100 HEIGHT=30>";
           $time .= "<IMG SRC=\"$images/wk4-4.gif\" WIDTH=100 HEIGHT=30>";
	}
      } else  {
         if ($cday != 0) {
   	    $pixsec = 3600 * 24/400;
	    if ($cday == 1) {
               $time .= "<IMG SRC=\"$images/6am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/7am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/8am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/9am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/10am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/11am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/12am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/1pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/2pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/3pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/4pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/5pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/6pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/7pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/8pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/9pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/10pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/11pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/12pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/1am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/2am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/3am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/4am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/5am.gif\" WIDTH=16 HEIGHT=30>";
            }
         } else {
	    if ($chour != 0) {
   	       $pixsec = 3600 * 24/400; 
               $time .= "<IMG SRC=\"$images/6am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/7am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/8am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/9am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/10am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/11am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/12am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/1pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/2pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/3pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/4pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/5pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/6pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/7pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/8pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/9pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/10pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/11pm.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/12am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/1am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/2am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/3am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/4am.gif\" WIDTH=16 HEIGHT=30>";
               $time .= "<IMG SRC=\"$images/5am.gif\" WIDTH=16 HEIGHT=30>";
	    }
	 }
      }
   }

   if ($pixsec == 0) {
      $pixsec = 60;
   }
   #$pixsec = 60;
   
   $min = $input{min};
   $hour = $input{hour};
   $day = $input{day};
   $month = $input{month};
   $meridian = $input{meridian};
   $year = $input{year};
   $zone = $input{zone};

   $appttime = etimetosec(0, $min, $hour, $day, $month, $year, "", "", "", $zone);
 
   $daysinmonth = $cmonth * 30;
   $cweekdays = $cweek * 7; 
    
   $tdays = $cweekdays + $cday + $daysinmonth + $mdays;
   $daysec = $tdays * 24 * 3600;
   $hrsec = $chour * 3600;
   $chktime = $daysec + $hrsec;

   $upperrange = $appttime + $chktime;
   #hddebug "upperrange = $upperrange, appttime = $appttime";
   if ($appttime == $upperrange) {
      status ("$login: Specify check available time by selecting one or more of months, weeks, days, hours.");
return;
   }

   $k = 0;
 
   $k = 0;    
   $l = 0;    

   $checkbox .=  "<TR BGCOLOR=dddddd FGCOLOR=ffffff>";
   $checkbox .=  "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=CHECKBOX NAME=checkbox></FONT> </TD>";

   $login_exists = 0;
   for ($i = 0; $i <= $#hshmembers; $i = $i + 1) {
      ($mem, $rem) = split(":", $hshmembers[$i]);
      hddebug "members = $mem";
      $mem = trim $mem;
      if ($mem eq $login) {
	 $login_exists = 1;
      }
   }

   hddebug "login_exists = $login_exists";
   if ($login_exists == 0) {
      $hshmembers[$#hshmembers + 1] = $login;
   }

   for ($g = 0; $g <= $#hshmembers; $g = $g+1) {
     ($mem, $rem) = split(":", $hshmembers[$g]);
     $mem = trim $mem;

     if (!exists($logtab{$mem})) {
	next;
     } 

     $alpmem = substr $mem, 0, 1;
     $alpmem = $alpmem . '-index';
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$alpmem/$mem/appttab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
                'hour', 'min', 'meridian', 'dhour', 'dmin',
                'dtype', 'atype', 'desc', 'zone', 'recurtype',
                'share', 'free', 'subject'] };
     foreach $record (sort keys % appttab) {
        $meridian = $appttab{$record}{meridian};
        $appthour = $appttab{$record}{hour};
        $apptzone = $appttab{$record}{zone};
        $apptzone = adjustzone($apptzone);
  
        if ( ($meridian eq "PM") && ($appthour ne "12")) {
           $appthour += 12;
        }
        if (($meridian eq "AM") && ($appthour eq "12")){
           $appthour = 0;
        }
        $etime = etimetosec("", $appttab{$record}{min}, $appthour, $appttab{$record}{day}, $appttab{$record}{month}, $appttab{$record}{year}, "", "", "", $apptzone);
        $dhour = $appttab{$record}{dhour} * 3600;
        $dmin = $appttab{$record}{min} * 60;
        $durtime = $dhour + $dmin + $etime;
        system "echo \"$etime $record $durtime\" >> $ENV{HDHOME}/tmp/$mem-etime$$";
     }
     $systemcat = "cat $ENV{HDHOME}/tmp/$mem-etime$$";
     $sortcmd =  "sort -n \"+0.0\"";
     $pipecmd =  "|";
     $outputfile =  "> $ENV{HDHOME}/tmp/$mem-etimeout$$";
     system "echo '#!/bin/ksh' > /var/tmp/ksh$mem$$";
     system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$mem$$";
     system "/bin/chmod 755 /var/tmp/ksh$mem$$";
     system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$mem$$\"";
     system "/bin/cp $ENV{HDHOME}/tmp/$mem-etimeout$$ /var/tmp/$mem-etimeout$$";
     $td .= $checkbox;
     $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$mem</FONT></TD>";
     $td .= "<TD>";
     $tfile = "/var/tmp/$mem-etimeout$$";
     $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
     $td .= "</TR>";
   }

   $z = 0;
   for ($q = 0; $q < $#hshbusteams; $q = $q + 1) {  
      ($busname, $teaminfo, $mem) = split(":", $hshbusteams[$q]);
      ($teamname, $mem) = split(":", $teaminfo);
      if ($teamname eq "AllTeams") {
	 $teamnames[$z] = "AllTeams";
	 $busnames[$z] = $busname;
	 $mems[$z] = $mem;
	 $z = $z + 1; 
      } else {
	$alreadyexists = 0;
	for ($b = 0; $b <= $z; $b = $b + 1 ) {
	   if ($busnames[$b] == $busname) {
	       $alreadyexists = 1;
           }
        }
	if ($alreadyexists == 0) {
	   $teamnames[$z] = $teamname;
	   $busnames[$z] = $busname;
	   $mems[$z] = $mem;
	   $z = $z + 1;
	}
      }
   }
  
   hddebug "busnames = $z"; 
   for ($q = 0; $q < $z; $q = $q + 1) {  

      $teamname = $teamnames[$q];
      $busname = $busnames[$q];
      $mem = $mems[$q];
      hddebug "teamname = $teamname, busname = $busname, mem = $mem";
	
  
      if ($teamname eq "AllTeams") {
         # bind teamtab table vars
         tie %teamtab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
         SUFIX => '.rec',
         SCHEMA => {
             ORDER => ['teamname', 'teamtitle', 'teamdesc', 'password',
                       'cpublish' ] };

         foreach $tmname (sort keys % teamtab) { 
            # takes care of team calendars
	    $td = scheduleresolve::scheduleresolve::createTeamSchedule($tmname, $busname, $td, $checkbox);

            # bind manager table vars
            tie %teampeopletab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/business/business/$busname/teams/$tmname/teampeopletab",
            SUFIX => '.rec',
            SCHEMA => {
                ORDER => ['login']};

 	    foreach $mem (sort keys %teampeopletab) {
	       if ($mem eq $login) {
	          next;
	       }
	       for ($r = 0; $r <= $#hshmembers; $r = $r + 1) {
		  ($bizmem, $rem) = split(":", $hshmembers[$r]);
	          if ($bizmem eq $mem) {
		     next;
		  }
	       }

               $alpmem = substr $mem, 0, 1;
               $alpmem = $alpmem . '-index';
               # check for each members personal calendar appt.
               # bind personal appointment table vars
               tie %appttab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/$alpmem/$mem/appttab",
               SUFIX => '.rec',
               SCHEMA => {
                 ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject'] };
               foreach $record (sort keys % appttab) {
                   $meridian = $appttab{$record}{meridian};
                   $appthour = $appttab{$record}{hour};
                   $apptzone = $appttab{$record}{zone};
                   $apptzone = adjustzone($apptzone);
    
                   if ( ($meridian eq "PM") && ($appthour ne "12")) {
                      $appthour += 12;
                   }
                   if (($meridian eq "AM") && ($appthour eq "12")){
                      $appthour = 0;
                   }
                   $etime = etimetosec("", $appttab{$record}{min}, $appthour, $appttab{$record}{day}, $appttab{$record}{month}, $appttab{$record}{year}, "", "", "", $apptzone);
	           $dhour = $appttab{$record}{dhour} * 3600;
	           $dmin = $appttab{$record}{min} * 60;
                   $durtime = $dhour + $dmin + $etime;
                   system "echo \"$etime $record $durtime\" >> $ENV{HDHOME}/tmp/$mem-etime$$"; 
               }
               $systemcat = "cat $ENV{HDHOME}/tmp/$mem-etime$$";
	       $sortcmd =  "sort -n \"+0.0\"";
	       $pipecmd =  "|";
	       $outputfile =  "> $ENV{HDHOME}/tmp/$mem-etimeout$$";

	       system "echo '#!/bin/ksh' > /var/tmp/ksh$mem$$";
	       system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$mem$$";
	       system "/bin/chmod 755 /var/tmp/ksh$mem$$";
	       system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$mem$$\"";
	       system "/bin/cp $ENV{HDHOME}/tmp/$mem-etimeout$$ /var/tmp/$mem-etimeout$$";
               $td .= $checkbox;
	       $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$mem</FONT></TD>";
	       $td .= "<TD>";
	       $pdurtime = 0;
               $tfile = "/var/tmp/$mem-etimeout$$";
	       hddebug "tfile = $tfile";
               $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
	       $td .= "</TR>";
	    }
	 }
      } else {
	 $td = scheduleresolve::scheduleresolve::createTeamSchedule($teamname, $busname, $td, $checkbox);
      } 
   }

   foreach $grpname (@groups) {
      $grpname = trim $grpname;
      if (-d("$ENV{HDDATA}/listed/groups/$grpname/appttab")) {
         tie %grouptab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/listed/groups/$grpname/appttab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'month', 'day', 'year',
              'hour', 'min', 'meridian', 'dhour', 'dmin',
              'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
              'subject'] };

	 foreach $record (sort keys %appttab) {
            $meridian = $appttab{$record}{meridian};
            $appthour = $appttab{$record}{hour};
            $apptzone = $appttab{$record}{zone};
            $apptzone = adjustzone($apptzone);

            if ( ($meridian eq "PM") && ($appthour ne "12")) {
               $appthour += 12;
            }
            if (($meridian eq "AM") && ($appthour eq "12")){
               $appthour = 0;
            }
            $bdhour = $appttab{$record}{'dhour'};
            $bdmin = $appttab{$record}{'dmin'};
            $bdhour = $bdhour * 3600;
            $bdmin = $bdmin * 60;

            $etime = etimetosec("", $appttab{$record}{min}, $appthour, $appttab{$record}{day}, $appttab{$record}{month}, $appttab{$record}{year}, "", "", "", $apptzone);
            $durtime = $bdhour + $bdmin + $etime;
	    system "echo \"$etime $record $durtime\" >> $ENV{HDHOME}/tmp/$grpname-etime$$";
         }
         $systemcat = "cat $ENV{HDHOME}/tmp/$grpname-etime$$";
         $sortcmd =  "sort -n \"+0.0\"";
         $pipecmd =  "|";
         $outputfile =  "> $ENV{HDHOME}/tmp/$grpname-etimeout$$";

         system "echo '#!/bin/ksh' > /var/tmp/ksh$grpname$$";
         system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$grpname$$";
         system "/bin/chmod 755 /var/tmp/ksh$grpname$$";
         system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$grpname$$\"";
         system "/bin/cp $ENV{HDHOME}/tmp/$grpname-etimeout$$ /var/tmp/$grpname-etimeout$$";
         $td .= $checkbox;
         $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$grpname</FONT></TD>";
         $td .= "<TD>";
         $pdurtime = 0;
         $tfile = "/var/tmp/$grpname-etimeout$$";
         hddebug "tfile = $tfile";
         $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
         $td = "</TR>";
      }
   }

   foreach $res (@resources) {
      $res = trim $res;
      if (-d("$ENV{HDDATA}/business/business/$business/restab")) {
         tie %restab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/restab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER =>  ['type', 'name', 'bldg', 'zipcode', 'country', 'tz'] };

         foreach $resname (sort keys %restab) {
            tie %appttab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/business/business/$business/resources/$resname/appttab",
            SUFIX => '.rec',
            SCHEMA => {
               ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject'] };

            foreach $record (sort keys % appttab) {
               $meridian = $appttab{$record}{meridian};
               $appthour = $appttab{$record}{hour};
               $apptzone = $appttab{$record}{zone};
               $apptzone = adjustzone($apptzone);

               if ( ($meridian eq "PM") && ($appthour ne "12")) {
                  $appthour += 12;
               }
               if (($meridian eq "AM") && ($appthour eq "12")){
                  $appthour = 0;
               }
               $etime = etimetosec("", $appttab{$record}{min}, $appthour, $appttab{$record}{day}, $appttab{$record}{month}, $appttab{$record}{year}, "", "", "", $apptzone);
               $dhour = $appttab{$record}{dhour} * 3600;
               $dmin = $appttab{$record}{min} * 60;
               $durtime = $dhour + $dmin + $etime;
	
               system "echo \"$etime $record $durtime\" >> $ENV{HDHOME}/tmp/$resname-etime$$";
	    }
  	    $systemcat = "cat $ENV{HDHOME}/tmp/$resname-etime$$";
            $sortcmd =  "sort -n \"+0.0\"";
            $pipecmd =  "|";
            $outputfile =  "> $ENV{HDHOME}/tmp/$resname-etimeout$$";

            system "echo '#!/bin/ksh' > /var/tmp/ksh$resname$$";
            system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$resname$$";
            system "/bin/chmod 755 /var/tmp/ksh$resname$$";
            system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$resname$$\"";
            system "/bin/cp $ENV{HDHOME}/tmp/$resname-etimeout$$ /var/tmp/$resname-etimeout$$";
            $td .= $checkbox;
            $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$resname</FONT></TD>";
            $td .= "<TD>";
            $pdurtime = 0;
            $tfile = "/var/tmp/$resname-etimeout$$";
            hddebug "tfile = $tfile";
            $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
            $td .= "</TR>";
	 }
      }
   } 


   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $rh = $input{rh};
   #$prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";

   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }

   $prml = strapp $prml, "template=$ENV{HDTMPL}/hdshowcalconflicts.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/hdshowcalconflicts-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "business=$business";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=11>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=members>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=groups>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=teams>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=resources>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=hour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=week>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=\"$execgetmembersforconflict\">";

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
   $prml = strapp $prml, "members=$hshmembers";
   $prml = strapp $prml, "groups=$groups";
   $prml = strapp $prml, "teams=$teams";
   $prml = strapp $prml, "resources=$resources";
   $prml = strapp $prml, "hour=0";
   $prml = strapp $prml, "day=0";
   $prml = strapp $prml, "week=0";
   $prml = strapp $prml, "month=0";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $td = adjusturl $td;
   $prml = strapp $prml, "td=$td";
   $time = adjusturl $time;
   $prml = strapp $prml, "time=$time";
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$alphaindex/$login/hdshowcalconflicts-$$.html";

   # reset the timer.

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

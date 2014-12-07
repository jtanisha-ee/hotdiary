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
# FileName: checkconflict.cgi
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


# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "checkconflict()";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
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

   # from personal address book
   $members = $input{pmembers};
   $groups = $input{pgroups};
   $teams = $input{pteams};
   $resources = $input{presources};
   $bizmembers = $input{bizmembers};
   hddebug "Teams = $teams";


   if (($bizmembers eq "") && ($groups eq "") && 
      ($teams eq "") && ($resources eq "")  &&
      ($members eq "")) {
      status("$login: Please select atleast one of the invitees or resources.");
      exit;
   }

   $timedur = $input{timedur};
   if ($timedur eq "1 Week") {
      $cweek = 1;	
   } 
   if ($timedur eq "2 Weeks") {
      $cweek = 2;	
   }
   if ($timedur eq "3 Weeks") {
      $cweek = 3;	
   }
   if ($timedur eq "4 Weeks") {
      $cweek = 4;	
   }
   if ($timedur eq "1 Month") {
      $cmonth = 1;	
   }
   if ($timedur eq "2 Months") {
      $cmonth = 2;	
   }
   if ($timedur eq "3 Months") {
      $cmonth = 3;	
   }
   if ($timedur eq "12 Months") {
      $cmonth = 12;	
   }
   if ($timedur eq "1 Day") {
      $cday = 1;	
   }


   #$chour = $input{chour};
   #$cday = $input{cday};
   #$cweek = $input{cweek};
   #$cmonth = $input{cmonth};


   #if (($cmonth == 0 ) && ($cday == 0) && ($cweek == 0) && ($chour == 0)) {
   #   status("$login: Please specify atleast one(Months, Weeks, Days, Hours) of the Check Availability.");
   #   exit;
   #}

$pixsec = 0;

   $hour = $input{hour};
   $meridian = $input{meridian};

   $images = "http://www.hotdiary.com/images";

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
      } else {
	 if ($cday == 1) {
   	    $pixsec = 3600 * 24/400;
	    $k = $hour;
            $dt = "\L$meridian";
	    for ($i = $hour; $i <= $hour + 24;  $i = $i + 1) { 
	        if ($i == 13 ) {
	           $k = 1;
		   if (($hour eq "12") && ($meridian eq "AM")) {
		      $dt = "am";
		   } else {
  	              if ($meridian eq "AM") {
		         $dt = "pm";
		      }
		      if ($meridian eq "PM") {
		         $dt = "am";
		      }
		   }
		}  
	        if ($k == 13 ) {
		   $k = 1;
		   if ($oldmer eq "am") {
		      $dt = "pm";
		   }
		   if ($oldmer eq "pm") {
		       $dt = "am";
		   }
		}	
	        $gifnm = "$k$dt.gif"; 		
                $time .= "<IMG SRC=\"$images/$gifnm\" WIDTH=16 HEIGHT=30>";
	        $k = $k + 1;
		$oldmer = $dt;
	    }
	 }
      }
   }

   if ($pixsec == 0) {
      $pixsec = 60;
   }
   #$pixsec = 60;
   
   $min = $input{min};
   $day = $input{day};
   $month = $input{month};
   $year = $input{year};
   $zone = $input{zone};
   $zone = adjustzone($zone);
   #hddebug "meridian = $meridian";

   if (($meridian eq "PM") && ($hour ne "12")) {
      $hour += 12;
   } 
   if (($meridian eq "AM") && ($hour eq "12")) {
      $hour = 0;
   }
    
   $appttime = etimetosec(0, $min, $hour, $day, $month, $year, "", "", "", $zone);
 
   $daysinmonth = $cmonth * 30;
   $cweekdays = $cweek * 7; 
    
   $tdays = $cweekdays + $cday + $daysinmonth + $mdays;
   $daysec = $tdays * 24 * 3600;
   #$hrsec = $chour * 3600;
   #$chktime = $daysec + $hrsec;
   $chktime = $daysec;

   $upperrange = $appttime + $chktime;
   #hddebug "upperrange = $upperrange, appttime = $appttime";
   if ($appttime == $upperrange) {
      status ("$login: Specify check available time by selecting one or more of months, weeks, days, hours.");
      return;
   }

   $k = 0;

   (@hshbizmembers) = split(" ", $bizmembers);
   $hshmembers = "";
   for ($i = 0; $i <= $#hshbizmembers; $i = $i + 1) {
       ($rem, $hshmembers[$i]) = split("-", $hshbizmembers[$i]);
   }
  
   (@hshpersonal) = split(" ", $members);
   (@hshbusteams) = split(" ", $teams);
   $k = 0;    
   $l = 0;    

   #### check for duplicate users in bizmembers and personal address book
   #### if there are no duplicate entries add them to bizmembers (hshmembers).
 
   $j = $#hshmembers + 1;
   for ($i = 0; $i <= $#hshpersonal; $i = $i + 1) {
      for ($m = 0; $m <= $#hshmembers; $m = $m + 1) {
	 if ($hshmembers[$m] eq $hshpersonal[$i]) {
	    $exists = 1;
	 }
      }
      if ($exists == 0) {
   	 $hshmembers[$j] = $hshpersonal[$i];
	 $j = $j + 1;
      }
   }

   $login_exists = 0;
   for ($i = 0; $i <= $#hshmembers; $i = $i + 1) {
      ($mem, $rem) = split("-", $hshmembers[$i]);
      $mem = trim $mem;
      if ($mem eq $login) {
	 $login_exists = 1;
      }
   }

   if ($login_exists == 0) {
      $hshmembers[$#hshmembers + 1] = $login;
   }


   $checkbox = "<TR BGCOLOR=dddddd FGCOLOR=ffffff>";
   $td = "";
   $numpersonal = $#hshpersonal;
   for ($g = 0; $g <= $numpersonal; $g = $g+1) {
      ($mem, $rem) = split("-", $hshpersonal[$g]);
      $mem = trim $mem;

      if (!exists($logtab{$mem})) {
     	 next;
      } 
      $bk = "Personal" . $mem;
      $td .=  "$checkbox <TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=man></FONT> </TD>";
      $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=rsvp></FONT></TD>";

      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
                'hour', 'min', 'meridian', 'dhour', 'dmin',
                'dtype', 'atype', 'desc', 'zone', 'recurtype',
                'share', 'free', 'subject', 'street', 'city', 'state', 
		'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
		 'confirm', 'id', 'type'] };

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
      $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$mem</FONT></TD><TD>";
      if (-e "$ENV{HDHOME}/tmp/$mem-etime$$") {
         $systemcat = "cat $ENV{HDHOME}/tmp/$mem-etime$$";
         $sortcmd =  "sort -n \"+0.0\"";
         $pipecmd =  "|";
         $outputfile =  "> $ENV{HDHOME}/tmp/$mem-etimeout$$";
         system "echo '#!/bin/ksh' > /var/tmp/ksh$mem$$";

         system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$mem$$";
         system "/bin/chmod 755 /var/tmp/ksh$mem$$";
         system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$mem$$\"";
         system "/bin/cp $ENV{HDHOME}/tmp/$mem-etimeout$$ /var/tmp/$mem-etimeout$$";
         $people .= "$bk ";
         #$td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$mem</FONT></TD><TD>";
         $tfile = "/var/tmp/$mem-etimeout$$";
         $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
         $td .= "</TR>";
      } else {
	 $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
      }
   }

   $biznum = $#hshbizmembers;
   ## bizmembers is $businessname-$memberlogin
   for ($i = 0; $i <= $biznum; $i = $i + 1) {
      ($biz, $mem) = split("-", $hshbizmembers[$i]);
      $mem = trim $mem;
      if (!exists($logtab{$mem})) {
     	 next;
      } 
      #hddebug "biz = $biz";
      $bk = "Bizmem" . $biz . "AAA" . $mem;
      $td .=  "$checkbox <TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=man></FONT> </TD>";
      $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=rsvp></FONT></TD>";

      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
                'hour', 'min', 'meridian', 'dhour', 'dmin',
                'dtype', 'atype', 'desc', 'zone', 'recurtype',
                'share', 'free', 'subject', 'street', 'city', 'state', 
		'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
		 'confirm', 'id', 'type'] };

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
      $td .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$mem</FONT></TD><TD>";
      if (-e "$ENV{HDHOME}/tmp/$mem-etime$$") {
         $systemcat = "cat $ENV{HDHOME}/tmp/$mem-etime$$";
         $sortcmd =  "sort -n \"+0.0\"";
         $pipecmd =  "|";
         $outputfile =  "> $ENV{HDHOME}/tmp/$mem-etimeout$$";
         system "echo '#!/bin/ksh' > /var/tmp/ksh$mem$$";

         system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$mem$$";
         system "/bin/chmod 755 /var/tmp/ksh$mem$$";
         system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$mem$$\"";
         system "/bin/cp $ENV{HDHOME}/tmp/$mem-etimeout$$ /var/tmp/$mem-etimeout$$";
         $people .= "$bk ";
         $tfile = "/var/tmp/$mem-etimeout$$";
         $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
         $td .= "</TR>";
      } else {
	 $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
      }
   }


   $z = 0;
   $numbusteams = $#hshbusteams;
   hddebug "numbusteams = $numbusteams";
   for ($q = 0; $q <= $numbusteams; $q = $q + 1) {  
      ($busname, $teaminfo, $mem) = split(":", $hshbusteams[$q]);
      #hddebug "busname= $busname, teaminfo  = $teaminfo";
      ($teamname, $mem) = split(":", $teaminfo);
      #hddebug "teamname  = $teamname";
      if (($teamname eq "AllTeams") || ($teamname eq "NoTeams")) {
	 $teamnames[$z] = "AllTeams";
	 $busnames[$z] = $busname;
	 $mems[$z] = $mem;
	 $z = $z + 1; 
      } else {
	$alreadyexists = 0;
	for ($b = 0; $b <= $z; $b = $b + 1 ) {
	   if ($busnames[$b] eq $busname) {
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
 
 # initialze totalteammem 
 $kh = 0; 
 $#totalteammem = -1;
 if ($z > 0) { 
   for ($q = 0; $q < $z; $q = $q + 1) {  
      #($busname, $teaminfo, $mem) = split(":", $hshbusteams[$q]);
      #($teamname, $mem) = split(":", $teaminfo);

      $teamname = $teamnames[$q];
      $busname = $busnames[$q];
      $mem = $mems[$q];
      hddebug "teamname = $teamname, busname = $busname, mem = $mem";
	
  
      if ($teamname eq "AllTeams") {
         # bind teamtab table vars
	 if (-d("$ENV{HDDATA}/business/business/$busname/teams/teamtab")) {
            tie %teamtab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/business/business/$busname/teams/teamtab",
            SUFIX => '.rec',
            SCHEMA => {
                ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode', 
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] };

            foreach $tmname (sort keys % teamtab) { 
               # takes care of team calendars
	       $bk = "Team" . $busname . "AAA" . $tmname;
	       $people .= "$bk ";
	       $td = scheduleresolve::scheduleresolve::createTeamSchedule($tmname, $busname, $td, $upperrange, $appttime, $pixsec);

     	       if (-d ("$ENV{HDDATA}/business/business/$busname/teams/$tmname/teampeopletab")) {

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

		     $mem_exists = 0;
		     $nummems = $#hshmembers;
	             for ($r = 0; $r <= $nummems; $r = $r + 1) {
		        ($bizmem, $rem) = split(":", $hshmembers[$r]);
			#hddebug "bizmem = $hshmembers[$r]";
		        ($bizmem, $rem) = split("-", $bizmem);
	                if ($bizmem eq $mem) {
		           $mem_exists = 1;
			   last;
		        }
	             }

		     if ($mem_exists == 1) {
			next;
		     }

		     $teammem_exists = 0;
		     # remove duplicate members in different teams
	             for ($r = 0; $r <= $#totalteammem; $r = $r + 1) {
		        if ($totalteammem[$r] eq $mem) {
			   $teammem_exists = 1;
			   #hddebug "teammem_exists = $teammem_exists";
			   last;
			}
		     }
		     if ($teammem_exists == 1) {
		        #hddebug "exists";
			next;
		     }
		     #hddebug "mem = $mem";
   
                     # check for each members personal calendar appt.
                     # bind personal appointment table vars
                     tie %appttab, 'AsciiDB::TagFile',
                     DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
                     SUFIX => '.rec',
                     SCHEMA => {
                          ORDER => ['entryno', 'login', 'month', 'day', 'year',
                       'hour', 'min', 'meridian', 'dhour', 'dmin',
                       'dtype', 'atype', 'desc', 'zone', 'recurtype',
                       'share', 'free', 'subject', 'street', 'city', 
		       'state', 'zipcode', 'country', 'venue', 'person', 
		       'phone', 'banner', 'confirm', 'id'] };

	             $records = 0;
		     $totalteammem[$kh] = $mem;
		     #hddebug "totalteammem[$kh] = $totalteammem[$kh]";
		     $kbp = "Bizmem" . $busname . "AAA" . $mem;
                     $td .=  "$checkbox <TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$kbp VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$kbp VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>$tmname-$mem</FONT></TD><TD>";
		     $kh = $kh + 1;

                     foreach $record (sort keys % appttab) {
			 $records = 1;
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
	             if ($records == 1) {
                        $systemcat = "cat $ENV{HDHOME}/tmp/$mem-etime$$";
	                $sortcmd =  "sort -n \"+0.0\"";
	                $pipecmd =  "|";
	                $outputfile =  "> $ENV{HDHOME}/tmp/$mem-etimeout$$";

	                system "echo '#!/bin/ksh' > /var/tmp/ksh$mem$$";
	                system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$mem$$";
	                system "/bin/chmod 755 /var/tmp/ksh$mem$$";
	                system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$mem$$\"";
	                system "/bin/cp $ENV{HDHOME}/tmp/$mem-etimeout$$ /var/tmp/$mem-etimeout$$";
                        $people .= "$kbp ";
	                $pdurtime = 0;
                        $tfile = "/var/tmp/$mem-etimeout$$";
	                #hddebug "tfile = $tfile";
                        $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
	                $td .= "</TR>";
		     } else {
	                $td .= "<TD><IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
		     }
	          }
	       }
	    }
	 }   
      } else {
	 hddebug "busname = $busname came to else part";
	 $bk = "Team" . $busname . "AAA" . $teamname;
	 $people .= "$bk ";
	 $td = scheduleresolve::scheduleresolve::createTeamSchedule($teamname, $busname, $td, $upperrange, $appttime, $pixsec);
      } 
   }
 }

   #hddebug "groupname = $groups";
   (@hshgroups) = split(" ", $groups);
   #hddebug "numgroups, $#hshgroups, group0 = $hshgroups[0]";

   foreach $grpname (@hshgroups) {
      #hddebug "groupname = $grpname";
      $grpname = trim $grpname;
      $bk = "Group" . $grpname;
      $people .= "$bk ";
      $td .=  "$checkbox <TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>Group-$grpname</FONT></TD><TD>";

      if (-d("$ENV{HDDATA}/listed/groups/$grpname/appttab")) {
         tie %grouptab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/listed/groups/$grpname/appttab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'month', 'day', 'year',
              'hour', 'min', 'meridian', 'dhour', 'dmin',
              'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
              'subject', 'street', 'city', 'state', 'zipcode', 'country',
              'venue', 'person', 'phone', 'banner', 'confirm', 'id'] };

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
      }
      if (-e "$ENV{HDHOME}/tmp/$grpname-etime$$") {
         $systemcat = "cat $ENV{HDHOME}/tmp/$grpname-etime$$";
         $sortcmd =  "sort -n \"+0.0\"";
         $pipecmd =  "|";
         $outputfile =  "> $ENV{HDHOME}/tmp/$grpname-etimeout$$";

         system "echo '#!/bin/ksh' > /var/tmp/ksh$grpname$$";
         system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$grpname$$";
         system "/bin/chmod 755 /var/tmp/ksh$grpname$$";
         system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$grpname$$\"";
         system "/bin/cp $ENV{HDHOME}/tmp/$grpname-etimeout$$ /var/tmp/$grpname-etimeout$$";
         $pdurtime = 0;
         $tfile = "/var/tmp/$grpname-etimeout$$";
         #hddebug "tfile = $tfile";
         $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
         $td .= "</TR>";
	 system "rm $ENV{HDHOME}/tmp/$grpname-etimeout$$";
	 system "rm $ENV{HDHOME}/tmp/$grpname-etime$$";
      } else {
	 $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
      }
      hddebug "td = $td";
   }
   


   (@hshres) = split(",", $resources);
   foreach $res (@hshres) {
      $res = trim $res;
      ($biz, $resname) = split(":", $res);
      if (-d("$ENV{HDDATA}/business/business/$biz/restab")) {
         tie %restab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$biz/restab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER =>  ['type', 'name', 'bldg', 'zipcode', 'country', 'tz'] };

	 $bk = "Resource" . $biz . "AAA" . $res;
	 $people .= "$bk ";
         $td .=  "$checkbox <TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=1>Resource-$biz-$res</FONT></TD><TD>";

	 if (-d("$ENV{HDDATA}/business/business/$biz/resources/$resname")) {
            tie %appttab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/business/business/$biz/resources/$resname/appttab",
            SUFIX => '.rec',
            SCHEMA => {
               ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
		 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
		 'confirm', 'id'] };

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
	    if (-e "$ENV{HDHOME}/tmp/$resname-etime$$") {
    	       $systemcat = "cat $ENV{HDHOME}/tmp/$resname-etime$$";
               $sortcmd =  "sort -n \"+0.0\"";
               $pipecmd =  "|";
               $outputfile =  "> $ENV{HDHOME}/tmp/$resname-etimeout$$";

               system "echo '#!/bin/ksh' > /var/tmp/ksh$resname$$";
               system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$resname$$";
               system "/bin/chmod 755 /var/tmp/ksh$resname$$";
               system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$resname$$\"";
               system "/bin/cp $ENV{HDHOME}/tmp/$resname-etimeout$$ /var/tmp/$resname-etimeout$$";
               $pdurtime = 0;
               $tfile = "/var/tmp/$resname-etimeout$$";
               #hddebug "tfile = $tfile";
               $td = scheduleresolve::scheduleresolve::createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
               $td .= "</TR>";
	       system "rm $ENV{HDHOME}/tmp/$resname-etime$$";
	       system "rm $ENV{HDHOME}/tmp/$resname-etimeout$$";
	    } else {
	        $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
	    }
	 } else {
	    $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
	 }
      }
   } 

   hddebug "people = $people";
   (@hshpeople) = split(" ", $people);
   hddebug "people = $hshpeople[0]";
   foreach $cn (@hshpeople) {
      $cn = trim $cn;
   }

   #foreach $busname (sort keys %businesstab) {
   #   if (-d("$ENV{HDDATA}/business/business/$busname/peopletab")) {
   #      tie %peopletab, 'AsciiDB::TagFile',
   #      DIRECTORY => "$ENV{HDDATA}/business/business/$busname/peopletab",
   #      SUFIX => '.rec',
   #      SCHEMA => {
   #      ORDER => ['business']};
   #      if (exists($peopletab{$login})) {
   #          $businesses .= "$busname ";
#	 }
#      }
#   }
#   $businesses = replaceblanks($businesses);

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
      $execteamconfirm =  encurl "execteamconfirm.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execteamconfirm =  "execteamconfirm.cgi";
   }


   $prml = strapp $prml, "template=$ENV{HDTMPL}/hdshowcalconflicts.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/hdshowcalconflicts-$$.html";
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execteamconfirm>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=back>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=dtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=desc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=year>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=recurtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=hour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=min>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=meridian>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=share>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=free>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=atype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=dhour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=dmin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=businesses>";

   #values of checkboxes as each parameter
   $k = 0;
   $mcntr = 23;
   $numend = $mcntr;
   $numbegin = $mcntr;
   # this tells from where the parameter for selection starts
   foreach $cn (@hshpeople) {
      $cn = trim $cn;
      #$cn = goodwebstr $cn;
      #hddebug "cn = $cn";
      $numend = $numend + 1;
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
      $mcntr = $mcntr + 1;
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
      $mcntr = $mcntr + 1;
      $k = $k + 1;
   }
   $numend = $numend - 1;

   $back = $input{rurl};
   ($dir, $re, $bi, $id) = split ("-", $back);

   $businesses = "";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=businesses VALUE=$businesses>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=back VALUE=$id>";
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

   $title = $input{subject};
   $title = replaceblanks($title);
   $dtype = $input{dtype};
   $desc = $input{desc};
   $desc = replaceblanks($desc);
   $month = $input{month};
   $day = $input{day};
   $year = $input{year};
   $recurtype = $input{recurtype};
   $hour = $input{hour};
   $min = $input{min};
   $meridian = $input{meridian};
   $zone = $input{zone};
   $share = $input{share};
   $free = $input{free};
   $atype = $input{atype};
   $dhour = $input{dhour};
   $dmin = $input{dmin};

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=title VALUE=$title>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=dtype VALUE=$dtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=desc VALUE=$desc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=month VALUE=$month>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=day VALUE=$day>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=year VALUE=$year>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=recurtype VALUE=$recurtype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=hour VALUE=$hour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=min VALUE=$min>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=meridian VALUE=$meridian>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=zone VALUE=$zone>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=share VALUE=$share>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=free VALUE=$free>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=atype VALUE=$atype>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=dhour VALUE=$dhour>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=dmin VALUE=$dmin>";

   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $td = adjusturl $td;
   $prml = strapp $prml, "td=$td";
   $time = adjusturl $time;
   $prml = strapp $prml, "time=$time";
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$login/hdshowcalconflicts-$$.html";

   # reset the timer.

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

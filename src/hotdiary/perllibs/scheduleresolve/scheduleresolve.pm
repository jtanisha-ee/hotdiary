package scheduleresolve::scheduleresolve;
require Exporter;
require "flush.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;

@ISA = qw(Exporter);
@EXPORT = qw(createImageSchedule createTeamSchedule removeDuplicates getmimetype);


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
# FileName: scheduleresolve.cgi
# Purpose: checkconflicts
# Creation Date: 09-12-99
# Created by: Smitha Gudur
#

sub removeDuplicates {

   my($tfile) = @_;

   #hddebug "removeduplicates()";
   open thandle, "+<$tfile";

   $i = 0;
   while (<thandle>) {
      chop;
      $onekey = $_;
      #hddebug "onekey from file = $onekey";

      ($etime, $entryno, $durtime) = split(" ", $onekey);
      if ($i != 0) {
	 #hddebug "i = $i $etimearray[$i - 1], $etime";
	 #hddebug "i = $i $durtimearray[$i - 1], $durtime";
	 
         if ($etimearray[$i - 1] == $etime) {
	    if ($durtimearray[$i - 1] <= $durtime) {
		$i = $i - 1;
		#hddebug "$etime, $durtime, i =$i";
	    } 
	 } 
      }
      $etimearray[$i] = $etime;
      $entrynoarray[$i] = $entryno;
      $durtimearray[$i] = $durtime;
      $i = $i + 1;
   }

   #hddebug "i came here = $i";
   $mfile = "/var/tmp/cleanup$i-$$";
   for ($k = 0; $k <= $i; $k = $k + 1) {
      #hddebug "$etimearray[$k], $entrynoarray[$k] $durtimearray[$k]";
      system "echo \"$etimearray[$k] $entrynoarray[$k] $durtimearray[$k]\" >> $mfile";
   }
   return $mfile;

}


sub createImageSchedule {

   my($kfile, $appttime, $upperrange, $td, $pixsec, $uzone) = @_;

   hddebug "createImageSchedule, upperrange = $upperrange";

   $tfile = removeDuplicates($kfile);

   open thandle, "+<$tfile";
   #hddebug "pixsec= $pixsec";

   $free = 0;
   $full = 0;

   $images = "http://www.hotdiary.com/images";

   $usedwidth = 0;
   $pdurtime = 0;
   while (<thandle>) {
      #hddebug "inside while() loop";
      chop;
      $onekey = $_;
      $overlap = 0;
      $free = 0;

      #hddebug "onekey from file = $onekey";

      ($etime, $entryno, $durtime) = split(" ", $onekey);	   
      

      #($entryno, $durtime) = split("-", $info);	   
      #hddebug "etime = $etime, entryno=$entryno, durtime=$durtime";
      #hddebug "pixsec = $pixsec";

      if ($pdurtime > 0 ) {
         if (($etime >= $appttime) && ($etime <= $upperrange)) {
            if ($etime > $pdurtime) {
               $freetime = $etime - $pdurtime;
	     
	       if ($freetime > $pixsec) {
                  $freetime = int $freetime / $pixsec;
		  # we want to put the redmark at the end of the right window bar
		  # example. appttime = 6.am upperrange = 6.am next day
		  # etime 6.00 am next day.
		  if ($etime == $upperrange) { 
  		     $freetime = $freetime - 16;
		     $usedwidth = 400;
		  } else {
		     if ($usedwidth == 0) {
      		       $freetime = $freetime - 16;
		     }
	          }
	       } else {
		  $freetime = 1;
	       }
	       if ($freetime > 400) {
	          $freetime = 400 - $usedwidth;
	       }
               #hddebug  "user is free for freetime = $freetime, pdurtime=$pdurtime, etime = $etime";
	       $usedwidth = $usedwidth + $freetime;
	       #$utime = getuserstime($etime, $uzone);
               $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=$freetime HEIGHT=30>";
            }
         }
      }
      # etime = 7.30 am    appttime = 6.30 am
      # durtime = 9.30 am  upperrange = 7.30 am
      if (($etime >= $appttime) && ($etime <= $upperrange)) {
         if (($durtime >= $appttime) && ($durtime >= $upperrange)) {
             #hddebug "upperrange = $upperrange, appttime = $appttime, etime = $etime, durtime = $durtime, upperrange = $upperrange, usedwidth = $usedwidth";	
             #hddebug "$entryno for window1";
	     if ($etime == $upperrange) {
		$overlap = 16; 
		$usedwidth = 400;
	     } else {
		if ($durtime == $upperrange) {
		   $overlap = $durtime - $etime; 
                   $full = $full + $overlap;
		} else {
                   $overlap = $etime - $appttime;
                   $full = $full + $overlap;
                   #hddebug "$entryno for overlap = $overlap";
		}
	        if ($overlap > $pixsec) {
                   $overlap = int $overlap / $pixsec;
	        } else {
	           $overlap = 1;
	        }
	     }
             #hddebug "usedwidth = $usedwidth, overlap = $overlap";
	     if ($usedwidth == 0 ) {
	        if ($etime > $appttime) {
	          $usedwidth = $etime - $appttime;
	          $usedwidth = int $usedwidth/$pixsec;
	          $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=$usedwidth HEIGHT=30>";
	        } 
	     }
             #hddebug "pixsec = $pixsec, full = $full, overlap = $overlap for window1, usedwidth = $usedwidth";
	     $usedwidth = $usedwidth + $overlap;
             $td .= "<IMG SRC=\"$images/oneredpixel.gif\" WIDTH=$overlap HEIGHT=30>";
        }
        # etime = 7.30 am    apptime = 6.30am
	# durtime = 7.45am   upperrange = 7.30am
        if (($durtime >= $appttime) && ($durtime < $upperrange)){
           #hddebug "$entryno for window2";
           $overlap = $durtime - $etime;
           #hddebug "overlap = $overlap, durtime = $durtime";
	   #assume the duration of this appointment is minimal.
	   if ($overlap == 0) {
	      $overlap = 1;
	   }
	   $full = $full + $overlap;
	   if ($overlap > $pixsec) {
              $overlap = int $overlap / $pixsec;
	   } else  {
	      $overlap = 1;
           }
           #hddebug "$entryno etime= $etime, appttime = $appttime pixsec = $pixsec"; 
	   if ($usedwidth == 0 ) {
	      if ($etime > $appttime) {
	        $usedwidth = $etime - $appttime;
	        $usedwidth = int $usedwidth/$pixsec;
		#hddebug "usedwidth = $usedwidth";
	        $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=$usedwidth HEIGHT=30>";
	      } 
	   }
           #hddebug "$entryno conflicts overlap = $overlap, usedwith = $usedwidth";
	   $usedwidth = $usedwidth + $overlap;
	   $td .= "<IMG SRC=\"$images/oneredpixel.gif\" WIDTH=$overlap HEIGHT=30>";
	} 
     }
     # etime = 6.00 am      appttime = 6.30 am
     # durtime = 7.00 am    upperrange = 7.30 am
     if ($etime < $appttime)  {
    	if (($durtime >= $appttime) && ($durtime < $upperrange)){
            #hddebug "$entryno for window3";
            $overlap = $durtime - $appttime;
	    $full = $full + $overlap;
	    if ($overlap > $pixsec) {
               $overlap = int $overlap / $pixsec;
	    } else {
	       $overlap = 1;
	    }
	    #if ($usedwidth == 0) {
	    #    $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=$usedwidth HEIGHT=30>";
	    #}
            #hddebug "$entryno conflicts overlap = $overlap";
	    $usedwidth = $usedwidth + $overlap;
	    $td .= "<IMG SRC=\"$images/oneredpixel.gif\" WIDTH=$overlap HEIGHT=30>";
        }
        # etime = 6.00 am      appttime = 6.30 am
        # durtime = 8.00 am    upperrange = 7.30 am
        if (($durtime >= $appttime) && ($durtime >= $upperrange)) {
           #hddebug "$entryno for window4";
           $overlap = $upperrange - $appttime;
           $full = $full + $overlap;
           #hddebug "$entryno conflicts overlap = $overlap";
	   if ($overlap > $pixsec) {
              $overlap = int $overlap / $pixsec;
	   } else {
	      $overlap = 1;
	   }
           #hddebug "$entryno conflicts overlap = $overlap";
	   $usedwidth = $usedwidth + $overlap;
	   $td .= "<IMG SRC=\"$images/oneredpixel.gif\" WIDTH=$overlap HEIGHT=30>";
	} 
     }
     if ($overlap == 0 ) {
        if (($etime <= $upperrange) && 
           ($durtime <= $upperrange)) {
           if ($durtime > $appttime) {
              $busytime = $durtime - $etime;
              $full = $full + $busytime;
	      if ($busytime >= $pixsec) {
                $busytime = int $busytime / $pixsec;
	      } else {
		 $busytime = 1;
	      }
	      $usedwidth = $usedwidth + $busytime;
	      $overlap = 1;
              $green = "<IMG SRC=\"$images/onegreenpixel.gif\" WIDTH=$busytime HEIGHT=30>";
              $green = adjusturl $green;
              $td .= $green;
           }
        }
     }
     if ($overlap != 0) {
        $free = 1;
     }  

     if (($durtime >= $appttime) && ($durtime <= $upperrange)) {
        $pdurtime = $durtime;
     } else {
        $pdurtime = 0;
     }
   }         
   close thandle;
   $freetime = $upperrange - $appttime;
   if ($free == 0) {
       if ($usedwidth == 0) {
         $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30>"; 
      }
   }

   #hddebug "usedwidth = $usedwidth, full = $full freetime = $freetime";
   if ($usedwidth != 0) {  
      if ($full != 0) {
         #hddebug "full = $full, freetime = $freetime";
         $freetime = $freetime - $full;
         #hddebug "full freetime = $freetime, usedwidth = $usedwidth";
	 if ($freetime > $pixsec) {
            $freetime = int $freetime / $pixsec;
	 } else {
	    $freetime = 400 - $usedwidth;
	 }
	 $freetime = 400 - $usedwidth;
	 if (($freetime < 1) && ($freetime > 0 ) ) {
	    $freetime = 1;
	 }
	 if ($freetime > 0 ) {
            $td .= "<IMG SRC=\"$images/onebluepixel.gif\" WIDTH=$freetime HEIGHT=30>";
	 }
      }
   }
	     
   $td .= "</TD>";
   #hddebug "td = $td";
   return $td;

}

sub createTeamSchedule {

   my($tmname, $busname, $td, $upperrange, $appttime, $pixsec) = @_;

   $images = "http://www.hotdiary.com/images";
   $records = 0;
   $bk = "Team" . $busname . "AAA" . $tmname;
   # check in the team calendar appointments
   $td .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$bk VALUE=rsvp><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=1>Team-$busname-$tmname</FONT></TD>";

   if (-d("$ENV{HDDATA}/business/business/$busname/teams/$tmname/busappttab")) {
      tie %busappttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$busname/teams/$tmname/busappttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share',
                 'free', 'subject', 'street', 'city', 'state', 'zipcode',
                 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };

      #hddebug "tmname = $tmname";
      foreach $record (sort keys %busappttab) {
	 $records = 1;
	 #hddebug "record = $record";
         if (exists($busappttab{$record})) {
            $byear = $busappttab{$record}{'year'};
            $bmonth = $busappttab{$record}{'month'};
            $bday = $busappttab{$record}{'day'};
            $bhour = $busappttab{$record}{'hour'};
            $bmin = $busappttab{$record}{'min'};
            $bzone = $busappttab{$record}{'zone'};
            $bmeridian = $busappttab{$record}{'meridian'};
            $bdhour = $busappttab{$record}{'dhour'};
            $bdmin = $busappttab{$record}{'dmin'};
            $bdhour = $bdhour * 3600;
            $bdmin = $bdmin * 60;
            if (($bmeridian eq "PM") && ($bhour ne "12")) {
               $bhour += 12;
            }
            if (($bmeridian eq "AM") && ($bhour eq "12")){
               $bhour = 0;
            }

	    #hddebug "bhour = $bhour";
            $bzone = adjustzone($bzone);

            #gmtime in seconds
            $etime = etimetosec("", $bmin, $bhour, $bday, $bmonth, $byear, "", "", "", $bzone);
            $durtime = $bdhour + $bdmin + $etime;
            system "echo \"$etime $record $durtime\" >> $ENV{HDHOME}/tmp/$busname-$tmname-etime$$";
          }
       }
       if ($records == 1) {
          $systemcat = "cat $ENV{HDHOME}/tmp/$busname-$tmname-etime$$";
          $sortcmd =  "sort -n \"+0.0\"";
          $pipecmd =  "|";
          $outputfile =  "> $ENV{HDHOME}/tmp/$busname-$tmname-etimeout$$";

          system "echo '#!/bin/ksh' > /var/tmp/ksh$busname-$tmname$$";
          system "echo \"$systemcat $pipecmd $sortcmd $outputfile\" >> /var/tmp/ksh$busname-$tmname$$";
          system "/bin/chmod 755 /var/tmp/ksh$busname-$tmname$$";
          system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/ksh$busname-$tmname$$\"";
          system "/bin/cp $ENV{HDHOME}/tmp/$busname-$tmname-etimeout$$ /var/tmp/$busname-$tmname-etimeout$$";
         $td .= "<TD>";
         $pdurtime = 0;
         $tfile = "/var/tmp/$busname-$tmname-etimeout$$";
         #hddebug "file for $tmname = $tfile";
         $td = createImageSchedule($tfile, $appttime, $upperrange, $td, $pixsec);
         $td .= "</TR>";
      } 
   }
   #hddebug "records = $records";
   if ($records == 0 ) {
      $td .= "<TD><IMG SRC=\"$images/onebluepixel.gif\" WIDTH=400 HEIGHT=30></TD></TR>";
   }
   return $td;
	
}


sub isaddr {

   my($letter, $login, $g) = @_;

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';
   if ($g eq "") {
      # bind address table vars
      tie %addrtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alph/$login/addrtab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
           'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
           'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
           'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };
  } else {
     tie %addrtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/addrtab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };             
  }

   foreach $mem (sort keys %addrtab) {
      $fn = substr $addrtab{$mem}{fname}, 0, 1;
      $ln = substr $addrtab{$mem}{lname}, 0, 1;
      if (("\L$letter" eq "\L$fn") || ("\L$letter" eq "\L$ln")) {
         return (1);
      }
   }
   return 0;
}

sub getmimetype {

  my($ftype) = @_;

  if (("\L$ftype" eq "html") || ("\L$ftype" eq "plain") || ("\L$ftype" eq "rtf") ||
     ("\L$ftype" eq "htm") ) { 
     return("text/$ftype");
  }
  if ("\L$ftype" eq "txt")  {
     return("text/plain");
  }
  if (("\L$ftype" eq "gif") || ("\L$ftype" eq "jpg")) {
     return("image/$ftype");
  } 
  if (("\L$ftype" eq "pdf") || ("\L$ftype" eq "x-troff-man") ) {
     return("application/$ftype");
  }
    
  if (("\L$ftype" eq "x-troff") || ("\L$ftype" eq "t") || ("\L$ftype" eq "tr") ||
     ("\L$ftype" eq "roff") ) { 
     return("application/x-troff");
  } 

  if (("\L$ftype" eq "x-sgi-movie") || ("\L$ftype" eq "movie")) { 
     return("video/$ftype");
  } 
  if (("\L$ftype" eq "x-pn-realaudio-plugin") || ("\L$ftype" eq "rpm")) { 
     return("movie/$ftype");
  }
  if (("\L$ftype" eq "ram") || ("\L$ftype" eq "ra") || ("\L$ftype" eq "rm") ) {
     return("audio/x-pn-realaudio");
  }  

  if (("\L$ftype" eq "mp2") || ("\L$ftype" eq "mpega") || ("\L$ftype" eq "abs") ||
     ("\L$ftype" eq "mpa")) {
     return("audio/x-mpeg");
  }  

  if (("\L$ftype" eq "aif") || ("\L$ftype" eq "aiff") || ("\L$ftype" eq "aifc") ) { 
     return("audio/x-aiff");
  }

  if (("\L$ftype" eq "au") || ("\L$ftype" eq "snd") ) { 
     return("audio/basic");
  }

  if ("\L$ftype" eq "wav") {
     return("audio/x-wav");
  }
 
  if (("\L$ftype" eq "wpd") || ("\L$ftype" eq "wp6") ) {
     return("application/wordperfect5.1");
  }  
  if ("\L$ftype" eq "scm") {
     return("application/vnd.lotus-screencam");
  }  
  if (("\L$ftype" eq "or3") || ("\L$ftype" eq "or2") || ("\L$ftype" eq "org") ) {
     return("application/vnd.lotus-organizer");
  }  
  if (("\L$ftype" eq "wk4") || ("\L$ftype" eq "wk3") || ("\L$ftype" eq "wk1") ||
	("\L$ftype" eq "123") ) {
     return("application/vnd.lotus-1-2-3");
  }  
  if (("\L$ftype" eq "wp") || ("\L$ftype" eq "sam")) {
     return("application/vnd.lotus-wordpro");
  }
  ## MS powerpoint
  if (("\L$ftype" eq "pot") || ("\L$ftype" eq "ppt") || ("\L$ftype" eq "pps") ||
     ("\L$ftype" eq "pwz") || ("\L$ftype" eq "ppa")) {
     return("application/vnd.ms-powerpoint");
  }
  
  if (("\L$ftype" eq "mdb") || ("\L$ftype" eq "mda") || ("\L$ftype" eq "mde")) { 
     return("application/vnd.ms-access");
  }

  if (("\L$ftype" eq "xls") || ("\L$ftype" eq "xlt") || ("\L$ftype" eq "xlm") ||
     ("\L$ftype" eq "xld") || ("\L$ftype" eq "xla") || ("\L$ftype" eq "xlc") ||
     ("\L$ftype" eq "xlw") || ("\L$ftype" eq "xll")) { 
     return("application/vnd.ms-excel");
  }

  if (("\L$ftype" eq "jpeg") || ("\L$ftype" eq "jpg") || ("\L$ftype" eq "jpe") ||
     ("\L$ftype" eq "jfif") || ("\L$ftype" eq "pjpeg") || ("\L$ftype" eq "pjp")) { 
     return("image/jpeg");
  }

  if (("\L$ftype" eq "doc") || ("\L$ftype" eq "dot")) {
     return("application/msword");
  }
  
  if (("\L$ftype" eq "jsc") || ("\L$ftype" eq "js") || ("\L$ftype" eq "mocha")) {
     return("application/x-javascript-config");
  }  

  if ("\L$ftype" eq "pl") {
     return("application/x-perl");
  }  

  if (("\L$ftype" eq "tar") || ("\L$ftype" eq "bin")) {
     return("application/x-tar");
  }  
  return("text/plain");


}

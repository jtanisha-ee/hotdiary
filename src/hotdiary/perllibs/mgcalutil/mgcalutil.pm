package mgcalutil::mgcalutil;
require Exporter;
use Time::Local;
use tparser::tparser;
use utils::utils;
use calfuncs::mgcalfuncs;

@ISA = qw(Exporter);
@EXPORT = qw(createCalendar nextMonth yrOfNextMonth prevMonth getweekendday yrOfPrevMonth getDateNumSuffix getmonth getday isDayInWeek getWeekDayIndex isdsttime getdaystr);

sub nextMonth {
   my($mo, $yr) = @_;
   return 1 if ($mo == 12);
   return ($mo+1);
}

sub yrOfNextMonth {
   my($mo, $yr) = @_;
   return ($yr+1) if ($mo == 12);
   return $yr;
}

sub prevMonth {
   my($mo, $yr) = @_;
   return 12 if ($mo == 1);
   return ($mo-1);
}

sub yrOfPrevMonth {
   my($mo, $yr) = @_;
   return ($yr-1) if ($mo == 1);
   return $yr;
}

# Appends "nd", "st", "rd", "th" as appropriate for numbers
sub getDateNumSuffix {
   my($dy) = @_;
   $len = length $dy;
   #status("dy = $dy");
   $digit = substr $dy, ($len-1), 1;
   #status("digit = $digit");
   return ($dy . "th") if (($digit == 0) || (($digit >= 4) && ($digit <= 9)) || (($dy >= 10) && ($dy <= 20)));
   return ($dy . "st") if ($digit == 1);
   return ($dy . "nd") if ($digit == 2);
   return ($dy . "rd") if ($digit == 3);
}

# Returns the nearest "legal" day
sub getAdjustedDay {
   my($dy, $mo, $yr) = @_;
   return ($dy-1) if (($mo == 2) && ($dy == 29) && (($yr % 4) != 0));
   return ($dy-2) if (($mo == 2) && ($dy == 30) && (($yr % 4) != 0));
   return ($dy-3) if (($mo == 2) && ($dy == 31) && (($yr % 4) != 0));
   return ($dy-1) if (($mo == 2) && ($dy == 30) && (($yr % 4) == 0));
   return ($dy-2) if (($mo == 2) && ($dy == 31) && (($yr % 4) == 0));
   return ($dy-1) if ((($mo == 4) || ($mo == 6) || ($mo == 9) || ($mo == 11)) && ($dy == 31));
   return $dy;
}

# Takes Jan..Dec and returns 0..11
sub getmonth {
   my($mo) = @_;
   $i = 1;
   (@mstr) = split " ", "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec";
   foreach $m (@mstr) {
      $mlist{$m} = $i;
      $i = $i + 1;
   }
   return $mlist{$mo};
}

# Takes Sun..Sat and returns 0..6
sub getday {
   my($mo) = @_;
   $i = 0;
   (@mstr) = split " ", "Sun Mon Tue Wed Thu Fri Sat";
   foreach $m (@mstr) {
      $mlist{$m} = $i;
      $i = $i + 1;
   }
   return $mlist{$mo};
}

# Takes 0..6 and returns Sun..Sat
sub getdaystr {
   my($index) = @_;
   return "Sun" if ($index == 0);
   return "Mon" if ($index == 1);
   return "Tue" if ($index == 2);
   return "Wed" if ($index == 3);
   return "Thu" if ($index == 4);
   return "Fri" if ($index == 5);
   return "Sat" if ($index == 6);
}


# Given a date, return the date on Sunday of the week within which
# this date falls.
sub getweekstartday {
   my($dy, $mo, $yr) = @_;
   $mstr = getmonthstr $mo;
   $wday = qx{date --date '$dy $mstr $yr' +%w};
   $wday =~ s/\n//g;
   $ctm = timelocal("0", "0", "5", $dy, ($mo-1), ($yr-1900));
   $ctm -= (3600 * 24 * $wday);
   ($sec, $min, $hour, $mday, $mon, $year) = localtime $ctm;
   $monstr = getmonthstr(++$mon);
   $year += 1900;
   $wstartday = "$monstr $mday, $year";
   return $wstartday;
}

# Given a date, return the date on Sat of the week within which
# this date falls.
sub getweekendday {
   my($dy, $mo, $yr) = @_;
   $mstr = getmonthstr $mo;
   $wday = qx{date --date '$dy $mstr $yr' +%w};
   $wday =~ s/\n//g;
   $ctm = timelocal("0", "0", "5", $dy, ($mo-1), ($yr-1900));
   $ctm += (3600 * 24 * (7 - $wday - 1));
   ($sec, $min, $hour, $mday, $mon, $year) = localtime $ctm;
   $monstr = getmonthstr(++$mon);
   $year += 1900;
   $wstartday = "$monstr $mday, $year";
   return $wstartday;
}

sub getDayOfWeek {
   my($dy, $mo, $yr, $wkdy) = @_;
   $mstr = getmonthstr $mo;
   $wday = qx{date --date '$dy $mstr $yr' +%w};
   $wday =~ s/\n//g;
   $ctm = timelocal("0", "0", "5", $dy, ($mo-1), ($yr-1900));
   $day = getday $wkdy;
   $ctm -= (3600 * 24 * ($wday-$day));
   ($sec, $min, $hour, $mday, $mon, $year) = localtime $ctm;
   $monstr = getmonthstr(++$mon);
   $year += 1900;
   $wday = "$monstr $mday, $year";
   return $wday;
}

# Given a date, return the weekday index 0..6 (Sun..Sat)
sub getWeekDayIndex {
   my($dy, $mo, $yr) = @_;
   $mstr = getmonthstr $mo;
   $wday = qx{date --date '$dy $mstr $yr' +%w};
   $wday =~ s/\n//g;
   return $wday;
}

# Determine if a certain day ($aptdy, $aptmo, $aptyr) falls in
# a week that contains the day ($dy, $mo, $yr)
sub isDayInWeek {
   my($aptdy, $aptmo, $aptyr, $dy, $mo, $yr) = @_;

   $aptmstr = getmonthstr $aptmo;
   $aptwday = qx{date --date '$dy $aptmstr $yr' +%w};
   $apttm = timelocal("0", "0", "5", $aptdy, ($aptmo-1), ($aptyr-1900));

   $startday = getDayOfWeek $dy, $mo, $yr, "Sun";
   $startday =~ s/,//g;
   ($startmonstr, $startmday, $startyear) = split " ", $startday;
   $startmon = getmonth $startmonstr;
   $starttm = timelocal("0", "0", "5", $startmday, ($startmon-1), ($startyear-1900));

   $endday = getDayOfWeek $dy, $mo, $yr, "Sat";
   $endday =~ s/,//g;
   ($endmonstr, $endmday, $endyear) = split " ", $endday;
   $endmon = getmonth $endmonstr;

   $endtm = timelocal("0", "0", "5", $endmday, ($endmon-1), ($endyear-1900));
   return 1 if (($apttm >= $starttm) && ($apttm <= $endtm));
   return 0;
}


sub getMonOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Mon";
}

sub getTueOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Tue";
}

sub getWedOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Wed";
}

sub getThuOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Thu";
}

sub getFriOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Fri";
}

sub getSatOfWeek {
   my($dy, $mo, $yr) = @_;
   return getDayOfWeek $dy, $mo, $yr, "Sat";
}

# This function takes current month and year as input and generates a monthly
# HTML calendar dataplate from template hdcal*.html. The dataplate is 
# copied to file $dp

sub createCalendar {
   my($dy, $mo, $yr, $dp, $login, $biscuit, $vw, $f, $a, $h, $m, $tz, $en, $sc, $jvw, $g, $calp, $rh, $logo, $title, $banner, $vdomain, $hs, $jp, $os) = @_;

   #hddebug "yr = $yr";

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

# Make sure prml is init
   $prml = "";

# substitute HTTPSUBDIR
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hiddenvars=";

   ## required for carry-on to indicate whether this should be in a frame
   ## or not.
   if ( ($vdomain eq "www.hotdiary.com") || ($vdomain eq "hotdiary.com")) {
      $prml = strapp $prml, "flg=";
   } else {
      $prml = strapp $prml, "flg=1";
   }

# form encoding ideosyncracies for NT v/s UNIX
   if ($os eq "nt") {
      $prml = strapp $prml, "formenc=";
      $execfilebrowser = "execfilebrowser.cgi";
   } else {
      $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execfilebrowser = encurl "execfilebrowser.cgi";
   }
   $prml = strapp $prml, "execfilebrowser=$execfilebrowser";

# compute today
   $tod = qx{date};
   $tod =~ s/\n//g;
   (@trex) = split ' ', $tod;
   $cmo = getmonth $trex[1];
   $cdy = $trex[2];
   $cyr = $trex[5]; 

#  Set defaults, if required to TODAY's date
#  Month and Year should always be set, if not, this must be the first time
#  we displayed calendar in this session for this user
   #if (($mo eq "") && ($yr eq "")) {
      #hddebug "dy = $dy, mo = $mo, yr = $yr";
      if (notDate $dy, $mo, $yr) {
         $dy = $cdy;
         #hddebug "mo4 = $mo";
         $mo = $cmo;
         #hddebug "before yr = $yr";
         $yr = $cyr;
      }
      if ($mo eq "") {
         $mo = $cmo;
      }
      #hddebug "yr = $yr";
      if ($yr eq "") {
         $yr = $cyr;
      }
      if ($dy eq "") {
         $dy = $cdy;
      }
      if (($vw eq "") || (($vw ne "d") && ($vw ne "m") && ($vw ne "w") && ($vw ne "y") && ($vw ne "i") && ($vw ne "n"))) {
         if ($sc ne "p") {
            $vw = "d";
         } else {
            $vw = "m";
         }
      }
# f is function, it can be e (event), t (todo), j (journal), h (home)
      if (($f eq "") || (($f ne "e") && ($f ne "t") && ($f ne "h"))) {
         $f = "e";
      }
# no action means just display
# d (display), 
      if (($a eq "") || (($a ne "d") && ($a ne "da") && ($a ne "de") && ($a ne "a") && ($a ne "e") && ($a ne "r"))) {
         $a = "d";
      }
   #}

# Call the cal utility and store records from output of cal
   $calout = qx{cal $mo $yr};
   (@records) = split '\n', $calout;

# Get the first row which contains the month label
   $records[0] =~ s/\n//g;


# Init Today
   $cdate = "$trex[1] $cdy, $cyr";
   $prml = strapp $prml, "today=$cdate"; 

# Get the month and year
   ($monthlbl, $yrlbl) = split " ", $records[0];

# Init the month label
   $prml = strapp $prml, "monthlbl=$monthlbl"; 

# Init the year label
   $prml = strapp $prml, "yrlbl=$yrlbl"; 

# Init the base CGI url

   if ($biscuit eq "") {
       $cgiscript = adjusturl "execmgcalclient.cgi?sc=$sc&l=$login&g=$g&jp=$jp";
   } else {
       $cgiscript = adjusturl "execmgcalclient.cgi?biscuit=$biscuit&g=$g&jp=$jp";
   }
   #$cgis = "/cgi-bin/$cgiscript";
   $cgis = "$cgiscript";

# Init JazzIt link

   if (("\L$vdomain" eq "\Lwww.hotdiary.com") || (("\L$vdomain" ne "\L1800calendar.com") && ("\L$vdomain" ne "\Lwww.1800calendar.com"))) {
      $jcgi = adjusturl "http://www.hotdiary.com/cgi-bin/execdogeneric.cgi?biscuit=$biscuit&vdomain=$vdomain";
   } else {
      $jcgi = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?biscuit=$biscuit&vdomain=$vdomain";
   }
   $prml = strapp $prml, "jazzit=$jcgi";

# Init JiveIt Partner
   $prml = strapp $prml, "jp=$jp";

# Init today ref
   $todayref = adjusturl "$cgis&mo=$cmo&dy=$cdy&yr=$cyr&vw=d&f=$f&a=d";
   $prml = strapp $prml, "todayref=$todayref";

   # bind portaltab table vars
   tie %portaltab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/portaltab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'calcolor', 'photo', 'title', 'logo',
                'tbanner', 'bbanner', 'but1', 'but2', 'but3', 'but4',
                'audio'] };                                       

   $prml = strapp $prml, "pubcolor=ffffff"; 
   $prml = strapp $prml, "calcolor="; 
   $prml = strapp $prml, "calphoto="; 
   $prml = strapp $prml, "tbanner="; 
   $prml = strapp $prml, "bbanner="; 
   $prml = strapp $prml, "but1="; 
   $prml = strapp $prml, "but2="; 
   $prml = strapp $prml, "but3="; 
   $prml = strapp $prml, "but4="; 
   $prml = strapp $prml, "audio="; 

   tie %hdtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/hdtab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['title', 'logo' ] };

 
   if ($sc eq "p") {
      $publish = "Published";
   }
 
   if ($title eq "") {
      if (exists $hdtab{$login}) {
         $title = adjusturl $hdtab{$login}{title};
      } else {
         $title = "HotDiary $publish Merged Calendars";
      }
   }
   # bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'listed',
		'groups', 'logins' ] };

# Init the page header
   $prml = strapp $prml, "login=$g"; 
   if ($g ne "") {

      if ($lmergetab{$g}{'password'} eq "") {
         if (-d "$ENV{HTTPHOME}/html/hd/merged/$g") {
            if ($lmergetab{$g}{cpublish} eq "on") {
            if ($hs eq "") {
               $gurl = "<BR></b></FONT><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Merged Calendar Website (http://$vdomain/merged/$g)</FONT>";
            } else {
               $gurl = "<BR></b></FONT><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Merged Calendar Website (http://$vdomain/$hs/merged/$g)</FONT>";
            }
            }
         }
         $label = adjusturl "$title $gurl";
      } else {
         if (-d "$ENV{HTTPHOME}/html/hd/merged/$g") {
            if ($lmergetab{$g}{cpublish} eq "on") {
            #if ($hs eq "") {
               $gurl = "<BR></b></FONT><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Secure Website (http://www.hotdiary.com/merged/$g)</FONT>";
            #} else {
               $gurl = "<BR></b></FONT><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Secure Website (http://$vdomain/$hs/merged/$g)</FONT>";
            #}
            }
         }
         $label = adjusturl "$title (Secure) $gurl";
      }
   } 

   $prml = strapp $prml, "label=$label";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "banner=$banner";

   $dref = adjusturl "<a href=\"$cgis&mo=$mo&yr=$yr&dy=$dy&vw=d&f=$f&a=d\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Day</FONT></a>";
   $wref = adjusturl "<a href=\"$cgis&mo=$mo&yr=$yr&dy=$dy&vw=w&f=$f&a=d\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Week</FONT></a>";
   $mref = adjusturl "<a href=\"$cgis&mo=$mo&yr=$yr&dy=$dy&vw=m&f=$f&a=d\"><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=\"34e69c\">Month</FONT></a>";
   #$yref = adjusturl "<a href=\"$cgis&mo=$mo&yr=$yr&dy=$dy&vw=y&f=$f&a=d\">Year</a>";
   $label1 = "Browse by $dref, $wref, $mref";
   $prml = strapp $prml, "label1=$label1"; 
   $label2 = "Use Events, To-Dos, and Journal";
   $prml = strapp $prml, "label2=$label2"; 
   if ($sc eq "p") {
      $prml = strapp $prml, "welcome=Merged Calendar"; 
      $prml = strapp $prml, "carryon="; 
   } else {
      $prml = strapp $prml, "welcome=Merged Calendar"; 
      $prml = strapp $prml, "carryon=My Carry-On"; 
   }

   $list = "";
   if ($lmergetab{$g}{groups} ne "") {
      $list = "(Groups - $lmergetab{$g}{groups})";
   }

   if ($lmergetab{$g}{logins} ne "") {
      $list .= " (Logins - $lmergetab{$g}{logins})";
   }
   $list = adjusturl $list;

   if ($g ne "") {
      $prml = strapp $prml, "group= [includes $list]"; 
   }

   if ( (($g ne "") && ($biscuit ne "")) || 
	($sc ne "p") ) {
      $prml = strapp $prml, "help=Help"; 
   } else { 
      $prml = strapp $prml, "help="; 
   }

# Init group cal link
       if ($g eq "") {
          if ($rh ne "") {
             $cgirh = "$rh";
          }
          #$grpcal = adjusturl "<a href=\"/cgi-bin/$cgirh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os\">Group Calendars</a> - ";
          $prml = strapp $prml, "groupcal=";
          $prml = strapp $prml, "calline=$calline";
       } else {
          if ($rh ne "") {
             $cgirh = "$rh";
          }
          #$grpcal = adjusturl "<a href=\"/cgi-bin/$cgirh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os\">Group Calendars</a> - ";
          $prml = strapp $prml, "groupcal=";
          $calline = adjusturl "<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=2 WIDTH=\"90%\"><TR><TD><TABLE BGCOLOR=\"0f0f5f\" CELLPADDING=0 CELLSPACING=0 WIDTH=\"100%\" BORDER=0><TR><TD WIDTH=\"25%\"><FONT FACE=\"Verdana\" COLOR=ffffff SIZE=\"2\">$lmergetab{$g}{'ctype'}&nbsp;</FONT></TD><TD ALIGN=\"CENTER\" WIDTH=\"50%\"><FONT COLOR=ffffff FACE=\"Verdana\" SIZE=\"2\">$lmergetab{$g}{'grouptitle'}&nbsp;</FONT></TD><TD WIDTH=\"25%\"><FONT COLOR=ffffff FACE=\"Verdana\" SIZE=\"2\">$lmergetab{$g}{'corg'}&nbsp;</FONT></TD></TR></TABLE></TD></TR></TABLE>";
          $prml = strapp $prml, "calline=$calline";
       }
    
# Init master template vars

   $caltop = "$ENV{HDTMPL}/mgcalviewtop.html";
   $calbot = "$ENV{HDTMPL}/hdcalviewbottom.html";
   $caldaily = "$ENV{HDTMPL}/mgcaldailyview.html";
   $calyearly = "$ENV{HDTMPL}/hdcalyearlyview.html";
   $calyearlytop = "$ENV{HDTMPL}/hdcalyearlyviewtop.html";
   $calyearlybot = "$ENV{HDTMPL}/hdcalyearlyviewbot.html";
   $calyearly = "$ENV{HDTMPL}/hdcalyearlyview.html";
   $calmonthly = "$ENV{HDTMPL}/hdcalmonthlyview.html";
   $calweekly = "$ENV{HDTMPL}/hdcalweeklyview.html";
   $calevent = "$ENV{HDTMPL}/hdcaleventview.html";
   $caltodo = "$ENV{HDTMPL}/hdcaltodoview.html";

   if ($sc eq "p") {
      $calevent = "$ENV{HDTMPL}/showevent.html";
      $caltodo = "$ENV{HDTMPL}/showevent.html";
   }

# Set the CGI script
   $prml = strapp $prml, "rh=$rh";

# Init the rep directory

   $hdhrep = "$ENV{HDHREP}/$alphaindex/$login";

# Make sure link to current month is set
   $mnturl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=m&f=$f&a=d";
   $prml = strapp $prml, "mntref=$mnturl"; 

# Make sure link to current year is set
   $yrurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=y&f=$f&a=d";
   $prml = strapp $prml, "yrref=$yrurl"; 

# Make sure link to next month is set
   #hddebug "mo = $mo, yr = $yr";
   $nmn = nextMonth $mo, $yr;
   #hddebug "nmn = $nmn, yr = $yr";
   $yonm = yrOfNextMonth $mo, $yr;
   $dya = getAdjustedDay $dy, $nmn, $yonm;
   if (($vw eq "n") || ($vw eq "i")) {
      $vew = "d";
   } else {
      $vew = $vw;
   }
   $nmnurl = adjusturl "$cgis&mo=$nmn&yr=$yonm&dy=$dya&vw=$vew&f=$f&a=d";
   #status "nmnurl = $nmnurl";
   $prml = strapp $prml, "nmn=$nmnurl"; 

# Make sure link to prev month is set
   $pmn = prevMonth $mo, $yr;
   $yopm = yrOfPrevMonth $mo, $yr;
   $dya = getAdjustedDay $dy, $pmn, $yopm;
   if (($vw eq "n") || ($vw eq "i")) {
      $vew = "d";
   } else {
      $vew = $vw;
   }
   $pmnurl = adjusturl "$cgis&mo=$pmn&yr=$yopm&dy=$dya&vw=$vew&f=$f&a=d";
   $prml = strapp $prml, "pmn=$pmnurl"; 

# Make sure link to next year is set
   $nyr = $yr + 1;
   if (($vw eq "n") || ($vw eq "i")) {
      $vew = "d";
   } else {
      $vew = $vw;
   }
   $nyrurl = adjusturl "$cgis&mo=$mo&yr=$nyr&dy=$dy&vw=$vew&f=$f&a=d";
   $prml = strapp $prml, "nyr=$nyrurl"; 

# Make sure link to prev year is set
   $pyr = $yr - 1;
   if (($vw eq "n") || ($vw eq "i")) {
      $vew = "d";
   } else {
      $vew = $vw;
   }
   $pyrurl = adjusturl "$cgis&mo=$mo&yr=$pyr&dy=$dy&vw=$vew&f=$f&a=d";
   $prml = strapp $prml, "pyr=$pyrurl"; 

# Store the previous view
   if ($a eq "d") {
      $jvw = $vw;
   } 

# Init the hidden fields for Form processing
   $prml = strapp $prml, "biscuit=$biscuit"; 
   $prml = strapp $prml, "dy=$dy"; 
   $prml = strapp $prml, "mo=$mo"; 
   $prml = strapp $prml, "yr=$yr"; 
   $prml = strapp $prml, "f=$f"; 
   $prml = strapp $prml, "jvw=$jvw";
   $prml = strapp $prml, "g=$g";
   if ($a eq "da") {
      $prml = strapp $prml, "a=a"; 
   } 
   if ($a eq "de") {
      $prml = strapp $prml, "a=e"; 
      if ($sc eq "p") {
        $prml = mgcalfuncs::mgcalfuncs::displayDetails($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $g);
      }
   } 
   $prml = strapp $prml, "en=$en"; 
   $prml = strapp $prml, "vw=$vw"; 
   $prml = strapp $prml, "h=$h"; 
   $prml = strapp $prml, "m=$m"; 
   if (($a eq "da") || ($a eq "de")) {
# this is redirect url, will be invoked when Save button is pressed
      #hddebug "just before rh = $rh";
      if ($rh ne "") {
         $cgirh = "/cgi-bin/$rh/";
      }
      $rurl = adjusturl "$cgirh$cgis&vw=w&mo=$mo&dy=$dy&yr=$yr&f=$f&a=d&jvw=$jvw";
      #$rurl = adjusturl "$cgis&vw=$vw&mo=$mo&dy=$dy&yr=$yr&f=$f&a=d";
      $prm = "";
      $prm = strapp $prm, "redirecturl=$rurl";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prm = strapp $prm, "templateout=$ENV{HDHREP}/$alphaindex/$login/$biscuit-$$-redirect_url.html";
      if ($sc eq "p") {
         $prm = strapp $prm, "carryon="; 
         $prm = strapp $prm, "homestr="; 
         $prm = strapp $prm, "home="; 
      }
      $prm = strapp $prm, "login=$g"; 
      parseIt $prm;
      $prml = strapp $prml, "rurl=$ENV{HDHREP}/$alphaindex/$login/$biscuit-$$-redirect_url.html";
   }

# Initialize Functions
   if (($vw eq "n") || ($vw eq "i")) {
      $vew = "d";
   } else {
      $vew = $vw;
   }
   $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=e&a=d";
   $prml = strapp $prml, "events=$fref"; 
   $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=t&a=d";
   $prml = strapp $prml, "todo=$fref"; 
   $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=j&a=d";
   $prml = strapp $prml, "jour=$fref"; 
   if ( ($login ne "") && ($sc ne "p") && (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") ) {
      $fref = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }
   $prml = strapp $prml, "home=$fref"; 

   #$repht = adjusturl "<a href=\"$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=r&a=d\"><FONT FACE=\"Verdana\" SIZE=\"3\">Report</FONT></a><BR><BR>";
   #$prml = strapp $prml, "rep=$repht";

   $prml = strapp $prml, "rep=";

   if ( ("\L$vdomain" eq "\Lwww.hotdiary.com") ||
        ("\L$vdomain" eq "\Lhotdiary.com") ) {
      $prml = strapp $prml, "homestr=Home";
      $target = adjusturl "target=_parent";
      $prml = strapp $prml, "target=$target";
 
   } else {
      $prml = strapp $prml, "homestr=Home";
      $prml = strapp $prml, "target=$target";
   }

   #if ($login eq "mjoshi") {
   #   $pcalcgi = adjusturl "<a href=\"/cgi-bin/execprivatecalmenu.cgi?biscuit=$biscuit&l=$login\">Secure Group Calendar</a><BR><BR>";
   #   $prml = strapp $prml, "pcal=$pcalcgi";
   #} else {
   #   $prml = strapp $prml, "pcal=";
   #}


# Initialize func
   if (($vw eq "d") || ($vw eq "m") || ($vw eq "w")) {
      if ($f eq "e") {
         $prml = strapp $prml, "func=Events";
      }
      if ($f eq "t") {
         $prml = strapp $prml, "func=To-Do";
      }
      if ($f eq "j") {
         $prml = strapp $prml, "func=Journal";
      }
   }
   if ($vw eq "y") {
      $prml = strapp $prml, "func=";
   }

# Build the month
   $dayurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=d&f=$f&a=d";
   for ($ind = 2; $ind < $#records; $ind = $ind + 1) {
       $row = $ind - 2;
       $records[$ind] =~ s/\n//g;
       (@days) = split ' ', $records[$ind];
       $wkurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=w&f=$f&a=d&dy=$days[0]";
       $prml = strapp $prml, "jwk$row=$wkurl";
       for ($col = 6; $col >= (6 - $#days); $col = $col - 1) {
           $today = $days[$col - (6 - $#days)];
           $prml = strapp $prml, "c$row$col=$today"; 
           $turl = adjusturl "$dayurl&dy=$today";
           $prml = strapp $prml, "rep$row$col=$turl"; 
       }
# first week of the month has leading blanks
       if ($row == 0) {
          for ($col = 0; $col < (6 - $#days); $col = $col + 1) {
              $prml = strapp $prml, "c$row$col="; 
          }
       }
   }
# last week of the month, has trailing blanks
   $ind = $#records;
   $row = $ind - 2;
   $records[$ind] =~ s/\n//g;
   (@days) = split ' ', $records[$ind];
   $wkurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=w&f=$f&a=$a&dy=$days[0]";
   $prml = strapp $prml, "jwk$row=$wkurl";
   for ($col = 0; $col <= $#days; $col = $col + 1) {
       $today = $days[$col];
       $prml = strapp $prml, "c$row$col=$today"; 
       $todayurl = adjusturl "$dayurl&dy=$today";
       $prml = strapp $prml, "rep$row$col=$todayurl"; 
   }
   for ($col = $#days+1; $col < 7; $col = $col + 1) {
       $prml = strapp $prml, "c$row$col="; 
   }

# some months have less than 6 weeks
   if ($#records == 6) {
      (@days) = split ' ', $records[$#records];
      $wkurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=w&f=$f&a=$a&dy=$days[0]";
      $prml = strapp $prml, "jwk5=$wkurl"; 
      for ($col = 0; $col < 7; $col = $col + 1) {
          $prml = strapp $prml, "c5$col="; 
      }
   }
   if ($#records == 5) {
      (@days) = split ' ', $records[$#records];
      $wkurl = adjusturl "$cgis&mo=$mo&yr=$yr&vw=w&f=$f&a=$a&dy=$days[0]";
      $prml = strapp $prml, "jwk4=$wkurl"; 
      $prml = strapp $prml, "jwk5=$wkurl"; 
      for ($i = 4; $i <= 5; $i = $i + 1) {
         for ($col = 0; $col < 7; $col = $col + 1) {
             $prml = strapp $prml, "c$i$col="; 
         }
      }
   }
   #hddebug "mo1 = $mo";

# depending on type of view use different template
# daily view
   if ($vw eq "d") {

# Init the day label

      if ($dy eq "") {
         $dy = 1;
      }
      $dy = getAdjustedDay $dy, $mo, $yr;
      $dystr = getDateNumSuffix($dy);
    
      $prml = strapp $prml, "day=$dystr,$records[0]"; 
      $tpartial = "$hdhrep/hdcaldailyview-$biscuit.html";
      qx{cat $caltop $caldaily $calbot > $tpartial};


      $prml = strapp $prml, "template=$tpartial"; 
      #status ("f = $f");
      if (($f eq "e") || ($f eq "t")) {
         $h = "5";
         $m = "AM";
         for ($i = 0; $i <= 18; $i++) {
            $h++;
            if ($h eq "12") {
               $m = "PM"
            }
            if ($h eq "13") {
               $h = "1";
            }
            if ($i eq "17") {
               $h = "11";
            }
            if ($i eq "18") {
               $h = "5";
               $m = "AM";
            }
            $timeref = adjusturl "$cgiscript&mo=$mo&dy=$dy&yr=$yr&vw=n&f=$f&a=da&h=$h&m=$m";
            $prml = strapp $prml, "twin$i=$timeref"; 
         }
      }
   }

# new item view
   if (($vw eq "n") || ($vw eq "i")) {
      if ($vw eq "i") {
         $vw = "d";
      }
      if (($f eq "e") && ($a eq "da")) {
         $tpartial = "$hdhrep/hdcaleventview-$biscuit.html";
         qx{cat $caltop $calevent $calbot > $tpartial};
         $prml = strapp $prml, "template=$tpartial";
         $prml = strapp $prml, "subject=";
         $prml = strapp $prml, "desc=";
         $mostr = getmonthstr $mo;
         $prml = strapp $prml, "month=$mostr";
         $prml = strapp $prml, "monthnum=$mo";
         $prml = strapp $prml, "day=$dy";
         $prml = strapp $prml, "year=$yr";
         $prml = strapp $prml, "recurtype=Once";
         $prml = strapp $prml, "hour=$h";
         $prml = strapp $prml, "min=0";
         $prml = strapp $prml, "meridian=$m";
         $zonestr = getzonestr $tz;
         $prml = strapp $prml, "zonestr=$zonestr";
         $prml = strapp $prml, "zone=$tz";
         $prml = strapp $prml, "share=Public";
         $prml = strapp $prml, "free=Free";
         $prml = strapp $prml, "atype=Email";
         $prml = strapp $prml, "dtype=Holiday";
         $prml = strapp $prml, "dhour=1";
         $prml = strapp $prml, "dmin=0";
         $prml = strapp $prml, "contact=";
         $prml = strapp $prml, "pinvited=";
         $prml = strapp $prml, "people=";
         $prml = strapp $prml, "bizpeople=";
         $prml = strapp $prml, "groups=";
         $prml = strapp $prml, "bizresource=";
         $prml = strapp $prml, "bizmem=";
         $prml = strapp $prml, "bizteams=";
         $prml = strapp $prml, "businesses=";
         $prml = strapp $prml, "type=";
         $prml = strapp $prml, "evtbanner=";
         $prml = strapp $prml, "filelist=";
         $prml = strapp $prml, "evenue=";
      }
      if (($f eq "e") && ($a eq "de")) {
         $tpartial = "$hdhrep/hdcaleventview-$biscuit.html";
         qx{cat $caltop $calevent $calbot > $tpartial};
         $prml = strapp $prml, "template=$tpartial";
      }
      if (($f eq "t") && ($a eq "da")) {
         $tpartial = "$hdhrep/hdcaltodoview-$biscuit.html";
         qx{cat $caltop $caltodo $calbot > $tpartial};
         $prml = strapp $prml, "template=$tpartial";
         $prml = strapp $prml, "subject=";
         $prml = strapp $prml, "desc=";
         $mostr = getmonthstr $mo;
         $prml = strapp $prml, "month=$mostr";
         $prml = strapp $prml, "monthnum=$mo";
         $prml = strapp $prml, "day=$dy";
         $prml = strapp $prml, "year=$yr";
         $prml = strapp $prml, "priority=3";
         $prml = strapp $prml, "meridian=$m";
         $prml = strapp $prml, "hour=$h";
         $prml = strapp $prml, "status=Undone";
         $prml = strapp $prml, "share=Public";
         $prml = strapp $prml, "pinvited=";
         $prml = strapp $prml, "people=";
         $prml = strapp $prml, "bizpeople=";
         $prml = strapp $prml, "groups=";
         $prml = strapp $prml, "bizresource=";
         $prml = strapp $prml, "bizmem=";
         $prml = strapp $prml, "bizteams=";
         $prml = strapp $prml, "businesses=";
         $prml = strapp $prml, "type=";
         $prml = strapp $prml, "evtbanner=";
         $prml = strapp $prml, "filelist=";
         $prml = strapp $prml, "evenue=";
      }
      if (($f eq "t") && ($a eq "de")) {
         $tpartial = "$hdhrep/hdcaltodoview-$biscuit.html";
         qx{cat $caltop $caltodo $calbot > $tpartial};
         $prml = strapp $prml, "template=$tpartial";
      }
   }

# monthly view
   if ($vw eq "m") {

      $tpartial = "$hdhrep/hdcalmonthlyview-$biscuit.html";
      qx{cat $caltop $calmonthly $calbot > $tpartial};


      $prml = strapp $prml, "template=$tpartial"; 
      $calout = qx{cal $mo $yr};
      (@crecords) = split '\n', $calout;
#################
      for ($ind = 2; $ind < $#crecords; $ind = $ind + 1) {
             $row = $ind - 2;
             $crecords[$ind] =~ s/\n//g;
             (@days) = split ' ', $crecords[$ind];
             for ($col = 6; $col >= (6 - $#days); $col = $col - 1) {
                 $today = $days[$col - (6 - $#days)];
                 #$todaylink = ':$day' . $today . ':' . ' ' . ':$img' . $today . ':';
                 $todaylink = ':$day' . $today . ':';
                 $prml = strapp $prml, "mc$row$col$mnt=$todaylink";
#                 $todayref = adjusturl "<a href=\"http://www.hotdiary.com/$cgis&mo=$mo&dy=$today&yr=$yr&vw=d&f=$f&a=d\">$today</a>";
                 $todayref = adjusturl "<a href=\"$cgis&mo=$mo&dy=$today&yr=$yr&vw=d&f=$f&a=d\">$today</a>";
                 $prml = strapp $prml, "dnum$row$col=$todayref";
             }
# first week of the month has leading blanks
             if ($row == 0) {
                for ($col = 0; $col < (6 - $#days); $col = $col + 1) {
                    $prml = strapp $prml, "mc$row$col$mnt=";
                    $prml = strapp $prml, "dnum$row$col=";
                }
             }
         }
# last week of the month, has trailing blanks
         $ind = $#crecords;
         $row = $ind - 2;
         $crecords[$ind] =~ s/\n//g;
         (@days) = split ' ', $crecords[$ind];
         for ($col = 0; $col <= $#days; $col = $col + 1) {
             $today = $days[$col];
             #$todaylink = ':$day' . $today . ':' . ' ' . ':$img' . $today . ':';
             $todaylink = ':$day' . $today . ':';
             $prml = strapp $prml, "mc$row$col$mnt=$todaylink";
             $todayref = adjusturl "<a href=\"$cgis&mo=$mo&dy=$today&yr=$yr&vw=d&f=$f&a=d\">$today</a>";
             $prml = strapp $prml, "dnum$row$col=$todayref";
         }
         for ($col = $#days+1; $col < 7; $col = $col + 1) {
             $prml = strapp $prml, "mc$row$col$mnt=";
             $prml = strapp $prml, "dnum$row$col=";
         }
# some months have less than 6 weeks
# in case of 5 week months
         if ($#crecords == 6) {
            for ($col = 0; $col < 7; $col = $col + 1) {
                $prml = strapp $prml, "mc5$col$mnt=";
                $prml = strapp $prml, "dnum5$col=";
            }
         }
# in case of 4 week months (eg. Feb 2009 is a 4 week month)
         if ($#crecords == 5) {
            for ($i = 4; $i <= 5; $i = $i + 1) {
                for ($col = 0; $col < 7; $col = $col + 1) {
                    $prml = strapp $prml, "mc$i$col$mnt=";
                    $prml = strapp $prml, "dnum$i$col=";
                }
            }
         }
         $tpartialout = $tpartial . ".out";
         $prml = strapp $prml, "templateout=$tpartialout"; 
         if ($sc eq "p") {
            $prml = strapp $prml, "carryon="; 
            $prml = strapp $prml, "homestr="; 
            $prml = strapp $prml, "home="; 
         }
         $prml= strapp $prml, "login=$g"; 
         parseIt $prml;
         $prml = "";
         $prml = strapp $prml, "template=$tpartialout"; 


#################

   }

# yearly view
   if ($vw eq "y") {

   #hddebug "yr = $yr";
   if (($yr >= 1996) && ($yr <= 2008)) {
      #hddebug "came here";
      $tpartial = "$hdhrep/hdcalyearlyview-$biscuit.html";
      qx{cat $caltop $ENV{HDTMPL}/y$yr.html $calbot > $tpartial};
      $prml = strapp $prml, "year=$yr"; 
      $prml = strapp $prml, "template=$tpartial"; 
   } else {

      $tpartial = "$hdhrep/hdcalyearlyview-$biscuit.html";
      qx{cat $caltop $calyearly $calbot > $tpartial};
      qx{cat $caltop > $tpartial};
      qx{cat $calyearlytop >> $tpartial};
      qx{cal $yr | egrep -v "$yr" >> $tpartial};
      qx{cat $calyearlybot >> $tpartial};
      qx{cat $calbot >> $tpartial};
      $prml = strapp $prml, "template=$tpartial"; 
      #$yearcal = adjusturl qx{cal $yr};
      #$prml = strapp $prml, "yearcal=$yearcal";

# Call the cal utility and store records from output of cal
      #for ($mnt = 0; $mnt < 12; $mnt = $mnt + 1) {
         #$mnth = $mnt + 1;
         #$calout = qx{cal $mnth $yr};
         #(@crecords) = split '\n', $calout;
##########
         #for ($ind = 2; $ind < $#crecords; $ind = $ind + 1) {
             #$row = $ind - 2;
             #$crecords[$ind] =~ s/\n//g;
             #(@days) = split ' ', $crecords[$ind];
             #for ($col = 6; $col >= (6 - $#days); $col = $col - 1) {
                 #$today = $days[$col - (6 - $#days)];
                 #$prml = strapp $prml, "c$row$col$mnt=$today"; 
             #}
# first week of the month has leading blanks
             #if ($row == 0) {
                #for ($col = 0; $col < (6 - $#days); $col = $col + 1) {
                    #$prml = strapp $prml, "c$row$col$mnt="; 
                #}
             #}
         #}
# last week of the month, has trailing blanks
         #$ind = $#crecords;
         #$row = $ind - 2;
         #$crecords[$ind] =~ s/\n//g;
         #(@days) = split ' ', $crecords[$ind];
         #for ($col = 0; $col <= $#days; $col = $col + 1) {
             #$today = $days[$col];
             #$prml = strapp $prml, "c$row$col$mnt=$today"; 
         #}
         #for ($col = $#days+1; $col < 7; $col = $col + 1) {
             #$prml = strapp $prml, "c$row$col$mnt="; 
         #}
## some months have less than 6 weeks
## in case of 5 week months
         #if ($#crecords == 6) {
            #for ($col = 0; $col < 7; $col = $col + 1) {
                #$prml = strapp $prml, "c5$col$mnt="; 
            #}
         #}
## in case of 4 week months (eg. Feb 2009 is a 4 week month)
         #if ($#crecords == 5) {
            #for ($i = 4; $i <= 5; $i = $i + 1) {
                #for ($col = 0; $col < 7; $col = $col + 1) {
                    #$prml = strapp $prml, "c$i$col$mnt="; 
                #}
            #}
         #}
#########
      #}
   

      $prml = strapp $prml, "year=$yr"; 
   }
   }

# weekly view
   if ($vw eq "w") {
      $tpartial = "$hdhrep/hdcalweeklyview-$biscuit.html";
      qx{cat $caltop $calweekly $calbot > $tpartial};
      $weekstart = getweekstartday $dy, $mo, $yr;
      $weekend = getweekendday $dy, $mo, $yr;
      $prml = strapp $prml, "day1=$weekstart"; 
      $wday = getMonOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day2=$wday"; 
      $wday = getTueOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day3=$wday"; 
      $wday = getWedOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day4=$wday"; 
      $wday = getThuOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day5=$wday"; 
      $wday = getFriOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day6=$wday"; 
      $wday = getSatOfWeek $dy, $mo, $yr;
      $prml = strapp $prml, "day7=$wday"; 
      $prml = strapp $prml, "weekstart=$weekstart"; 
      $prml = strapp $prml, "weekend=$weekend"; 
      $prml = strapp $prml, "template=$tpartial"; 
      for ($k2 = 0; $k2 <= 6; $k2 = $k2 + 1) {
         $daystr = getdaystr($k2);
         $dpig = getDayOfWeek($dy, $mo, $yr, $daystr);
         $dpig =~ s/,//g;
         ($kmonth, $kday, $kyear) = split(" ", $dpig); 
         $kmonth = getmonth $kmonth;
         #print "kday = $kday <BR>";
         $timeref = adjusturl "$cgiscript&mo=$kmonth&dy=$kday&yr=$kyear&vw=d&f=$f&a=d";
         $prml = strapp $prml, "twin$k2=$timeref"; 
      }
   }

# destination template does not change, and is a parameter!
   if ($a eq "da") {
      $en = "";
   }
   $url = $cgis;
   if (($a ne "") && ($vw ne "y") && ($a ne "da")) {
      $prml = dispatch $prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $g;
   }

   if ($sc eq "p") {
      $prml = strapp $prml, "carryon="; 
      $prml = strapp $prml, "homestr="; 
      $prml = strapp $prml, "home="; 
   }

   $prml = strapp $prml, "templateout=$dp"; 
   $prml = strapp $prml, "login=$g"; 
   parseIt $prml;
}


sub isdsttime {
   # first Sunday in April, clocks are set ahead one hour at 2:00 a.m.
   # local standard # On the last Sunday in October, clocks are set
   # back one hour at 2:00 a.m. local daylight time, which becomes 
   # 1:00 a.m. local standard time .

   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());      
   if (($mon >= 4 ) && ($mon <= 10)) {
      if (($mon == 4) || ($mon == 10)) {
         if ($mon == 4) {
	    $d = 1;
         } else {
	    $d = 31;
         }
         $dstmon = 0;
         while ($dstmon != $mon) { 
	    (@dstval)  = getweekstartday($d, $mon, $year);
            ($dstmon, $dstday, $dstyear) = (@dstval);
	    if ($mon == 4) {
	       $d = $d + 1; 
	    } else {
	       $d = $d - 1; 
	    }
         }
         # check for dst day. 
         if ($mon == 10 ) {
	    if ($mday > $dstday) {
	       return 0;
	    }
	    # last sunday of october
            if ($mday == $dstday) {
	       if ($hour < 14) {
	          return 0;
	       }
            }
         } 
         if ($mon == 4) {
	    if ($mday < $dstday) {
	       return 0;
	    }
	    # Ist sunday of April 
            if ($mday == $dstday) {
	       if ($hour < 14) {
	          return 0;
	       }
            }
         }
      } 
      return 1;
   } 
   return 0;
}


1;

__END__

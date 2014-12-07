package tdatautils;

require Exporter;
use Time::Local;

@ISA = qw(Exporter);
@EXPORT = qw(gmtimediff gettimezone getgmtimediff gettz gettmtz gethhmmtz getymd getpymd getFirstOfMon getFirstOfPrevMon padIt trim getmmddyy getmmddyyyy gettm getYesterday getToday);

use Time::Local;

# All of these time calls are cached internally in perl, so do not
# worry about calling them repeatedly in terms of performance

# Return the time difference between current zone and gm zone in hours
# The goal is to find out what the current zone is. But this is the first
# step towards that. For instance the time difference between GM and PST
# is -8 hours, and the time diff bet. GM and EST is -5 hours. So that's
# how it works.
sub gmtimediff {
  ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time()); 
  $gtm = timegm($sec, $min, $hour, $mday, $mon, $year);
  $ltm = timelocal($sec, $min, $hour, $mday, $mon, $year);
  return (($gtm - $ltm)/3600);
}

# This function takes as input the gmtimediff() above and returns a
# time zone string like PST, EST, CST etc.. Note only American 
# and some prominent time zones are supported. So if our data center is
# in one of the unsupported time zones, this code will have to be
# modified
sub gettimezone {
   my($tdiff) = @_;
   return "EST" if ($tdiff == -5);
   return "PST" if ($tdiff == -8);
   return "CST" if ($tdiff == -6);
   return "MST" if ($tdiff == -7);
   return "GMT" if ($tdiff == 0);
   return "Alaska" if ($tdiff == -9);
   return "Hawaii" if ($tdiff == -10);
   return "W.Europe" if ($tdiff == 1);
   return "Taiwan" if ($tdiff == 8);
   return "E.Australia" if ($tdiff == 10);
   return "New Zealand" if ($tdiff == 12);

   return "";
}

# This function takes a time zone string as input and returns the
# number of hours of difference from gm time
sub getgmtimediff {
   my($tz) = @_;
   return -5 if ($tz eq "EST");
   return -8 if ($tz eq "PST");
   return -6 if ($tz eq "CST");
   return -7 if ($tz eq "MST");
   return 0 if ($tz eq "GMT");
   return -9 if ($tdiff eq "Alaska");
   return -10 if ($tdiff eq "Hawaii");
   return 1 if ($tdiff eq "W.Europe");
   return 8 if ($tdiff eq "Taiwan");
   return 10 if ($tdiff eq "E.Australia");
   return 12 if ($tdiff eq "New Zealand");
   return 0;
}

# This function returns the current time zone as a string like
# "PST", "EST" etc, using gettimezone()
sub gettz {
   $tdiff = gmtimediff();
   return gettimezone $tdiff;
}

# This function returns the current time in seconds since epoch for 
# a given time zone
sub gettmtz {
   my($tz) = @_;
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time());
   $gtm1 = timegm($sec, $min, $hour, $mday, $mon, $year);
   $tdiff = getgmtimediff($tz);
   $toffset = 8 + $tdiff;
   $gtm1 += (3600*$toffset);
}

# Returns the formatted hhmm time for a given time zone
sub gethhmmtz {
   my($tz) = @_;
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(gettmtz($tz));
   if ( ($hour > 0) && ($hour < 10) ) {
	  $hour = '0' . $hour;
   }
   if ( ($min > 0) && ($min < 10) ) {
	  $min = '0' . $min;
   }
   return ($hour . $min);
}

# Get the current months's year, month and day
sub getymd {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   if ($mon < 10) {
	  $mon = '0' . $mon;
   }
   if ($mday < 10) {
	  $mday = '0' . $mday;
   }
   return ($year . $mon . $mday);
}

# Get the current month, day, year in mmddyyyy format
sub getmmddyyyy {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   if ($mon < 10) {
	  $mon = '0' . $mon;
   }
   if ($mday < 10) {
	  $mday = '0' . $mday;
   }
   return ($mon . $mday . $year);
}

# Get the current month, day, year in mmddyy format
sub getmmddyy {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   #$year = $year + 1900;
# Normalize the year to a two-digit value that will work is the year is
# post-2000 or pre-2000
   if ( ($year >= 100) && ($year <= 136) ) {
	  $year = substr $year, 1, 2; 
   } else {
	  if ( ($year >= 2000) && ($year <= 2036) ) {
         $year = substr $year, 2, 2;		 
	  }
   }
   $mon = $mon + 1;
   if ($mon < 10) {
	  $mon = '0' . $mon;
   }
   if ($mday < 10) {
	  $mday = '0' . $mday;
   }
   return ($mon . $mday . $year);
}


# Get the current hh, mm
sub gettm {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   return ($hour . $min);
}

sub getYesterday {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time()-86400);
   $year = $year + 1900;
   $mon = $mon + 1;
   if ($mon < 10) {
	  $mon = '0' . $mon;
   }
   return ($mon . '/' . $mday . '/' . $year);
}

sub getToday {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   if ($mon < 10) {
	  $mon = '0' . $mon;
   }
   return ($mon . '/' . $mday . '/' . $year);
}

# Gets the last day of the prev. month
sub lastDayOfPrevMonth {
   ($year, $mon) = @_;
   if ($mon == 1) {
	  $ryear = $year - 1;
	  $rmon = 12;
   } else {
	  $rmon = $mon - 1;
	  $ryear = $year;
   }
   (@days) = split " ", "31 28 31 30 31 30 31 31 30 31 30 31";
   if ( ($year % 4) == 0 ) {
	  if ($rmon == 1) {
	     $d = $days[$rmon-1] + 1;
	  } else {
		 $d = $days[$rmon-1];
	  }
   }
   if ($rmon < 10) {
	  $rmon = '0' . $rmon;
   }
   return ($ryear . $rmon . $d);
}

# Get the last day of previous month in teradata format
sub getpymd {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   return lastDayOfPrevMonth($year, $mon);
}

# Get the date at start of first day of current month in datetime format
sub getFirstOfMon {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   return ($mon . '/' . '1' . '/' . $year);
}

# Gets the first day of the prev. month in datetime format
sub firstDayOfPrevMonthDate {
   ($year, $mon) = @_;
   if ($mon == 1) {
      $ryear = $year - 1;
      $rmon = 12;
   } else {
      $rmon = $mon - 1;
      $ryear = $year;
   }
   return ($rmon . '/' . '1' . '/' . $ryear);
}


# Get the first day of previous month in date format
sub getFirstOfPrevMon {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $year = $year + 1900;
   $mon = $mon + 1;
   return firstDayOfPrevMonthDate($year, $mon);
}

sub tmin {
   ($x, $y) = @_;
   return ($x < $y) ? $x : $y;
}

# Pad with blanks
sub padIt {
   my($str, $len) = @_;
   $lenn = tmin(length $str, $len);
   $mystr = substr $str, 0, $lenn;
   if ($lenn < $len) {
	  for ($i = 0; $i < ($len-$lenn); $i++) {
		  $mystr .= " ";
	  }
   }
   return $mystr;
}

1;

__END__


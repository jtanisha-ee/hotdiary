use Time::Local;

{
 $sec = 0;
 $min  = 50;
 $hour = 11;
 $day = 12;
 $month = 11;
 $year = 1998;
 $tz = 5.5;
  
 #($sec, $min, $hour, $day, $month, $year, $wday, $yday, $isdst, $tz) = @_;
  $etime = timegm($sec, $min, $hour, $day, ($month - 1), ($year - 1900));
  $etime = $etime - ($tz * 3600);

 print "etime = $etime \n";


 ($sec1,$min1,$hour1,$mday1,$mon1,$year1,$wday1,$yday1,$isdst1) 
		= localtime(time());
   $ctm = timegm($sec1, $min1, $hour1, $mday1, $mon1, $year1);
   $ctm = $ctm + ( 8 * 3600);
 print "ctm = $ctm \n";

}

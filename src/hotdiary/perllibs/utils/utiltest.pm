
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



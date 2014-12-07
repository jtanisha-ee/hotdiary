use Time::Local;

{
  # assume ist input to timegm.. 
  #  11:10 AM Sept 15 1999
  # sunday(0), monday(1), tue(2), wed(3), thu(4), fri(5), sat(6)
  # timegm  sec, min, hour, day, month-1, year -1900
  $sec = timegm(0,10,11,15,8,99); 
  ($s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst) = gmtime($sec);
  print "$wday \n";


  # 10:00 PM Dec 25, 1999
  # weekday that is printed ranges from 0 - 6 ie. sunday - saturday
  # sunday(0), monday(1), tue(2), wed(3), thu(4), fri(5), sat(6)
  $sec = timegm(0,0,22,25,11,99); 
  ($s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst) = gmtime($sec);
  print "$wday \n";


  # testing with timezone
  # 2:00 AM DEC 1, 1999  india time
  # assume timezone as india time ie. tz = 5.5
  $tz = 5.5;
  $etime = timegm(0,0,2,1,11,99); 
  $etime = $etime - ($tz * 3600); 
  ($s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst) = gmtime($etime);
  print "$wday \n";
   
  

  #print "$s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst \n";
  #print "sec = $sec \n";

  #current time in gm time
  $sec1 =  gmtime(time());
  #print "sec1 = $sec1 \n";
 # ($s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst) =gmtime($sec1);
 # print "current time in gmtime \n";
 # print "$s, $m, $h, $mday, $mon, $year, $wday, $yday, $isdst \n";

  #$sec = timegm(0,50,22,11,11,98); 
  #print "time(10:50pm) = $sec \n";
}



package companycalutil::companycalfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use companycalutil::companycalutil;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch eventDispatch isCurrentDay isCurrentMonth isCurrentYear  setEventDisplayRec getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink setEventEditRec setDailyPrml deleteEvent addEvent updateEvent setMonthlyPrml setWeeklyPrml createWeeklyImageLink createDailyImageLink displayTodo createTodoLink createTodoWeeklyImageLink createTodoDailyImageLink editTodo updateTodo addTodo deleteTodo todoDispatch setTodoDailyPrml setTodoMonthlyPrml setTodoWeeklyPrml createDtypeImg addCalendarPref publishTodo publishEvent isCalPublic addBusEventToMyCal displayEventsAndTodos displayDetails );

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $business) = @_;

   if ($f eq "e") {
      $prml = eventDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc);
   }

   if ($f eq "t") {
      $prml = todoDispatch($prml, $vw, $mo, $dy, $yr, $h,$m, $login, $url, $a, $en, $f, $jvw, $business, $sc);
   }

   if ($f eq "j") {
      $prml = journalDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc);
   }
   return $prml;
}

sub todoDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc) = @_;     
   if ($a eq "d") {
      return(displayTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc ));
   }

   if ($a eq "de") {
      return(editTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $business));
   }                                                                           
   return $prml;
}

sub eventDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc) = @_;

   if ($a eq "d") {
      return (displayEventsAndTodos($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc));
      #return(setEventDisplayRec($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc));
   }
   if ($a eq "de") {
      return(setEventEditRec($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $jvw, $business, $sc));
   } 
   return $prml;
}

sub isCurrentDay {
   my($uday, $cday) = @_;
   return 1 if ($uday == $cday);
   return 0;
}
                             
sub isCurrentMonth {
   my($umonth, $cmonth) = @_;
   return 1 if ($umonth == $cmonth);
   return 0;
}

sub isCurrentYear {
   my($uyear, $cyear) = @_;
   return 1 if ($uyear == $cyear);
   return 0;
}

sub isCurrentMeridian {
   my($umer, $cmer) = @_;
   return 1 if ($umer == $cmer);
   return 0;
}


# assumption is meridian AM
sub getDailyAMEventNumber {

    my($hour) = @_;

    return 0 if (($hour >= 6) && ($hour < 7));
    return 1 if (($hour >= 7) && ($hour < 8)); 
    return 2 if (($hour >= 8) && ($hour < 9));
    return 3 if (($hour >= 9) && ($hour < 10));
    return 4 if (($hour >= 10) && $hour < 11);
    return 5 if (($hour >= 11) && ($hour < 12));
    return 18 if (($hour >= 12) || ($hour < 6));
}

# assumption is meridian PM
sub getDailyPMEventNumber {

    my($hour) = @_;
    return 6 if (($hour >= 12) || ($hour < 1));
    return 7 if (($hour >= 1) && ($hour < 2));
    return 8 if (($hour >= 2) && ($hour < 3));
    return 9 if (($hour >= 3) && ($hour < 4));
    return 10 if (($hour >= 4) && ($hour < 5));
    return 11 if (($hour >= 5) && ($hour < 6));
    return 12 if (($hour >= 6) && ($hour < 7));
    return 13 if (($hour >= 7) && ($hour < 8));
    return 14 if (($hour >= 8) && ($hour < 9));
    return 15 if (($hour >= 9) && ($hour < 10));
    return 16 if (($hour >= 10) && ($hour < 11));
    return 17 if (($hour >= 11) && ($hour < 12));
}


sub getDailyEventNum {

   my($year, $month, $day, $hour, $min, $meridian) = @_;

   if ($meridian eq "AM") {
      return(getDailyAMEventNumber($hour));
   }

   if ($meridian eq "PM") { 
       return(getDailyPMEventNumber($hour));
   }
}   

sub createDtypeImg {
   my($dtype) = @_; 

   $hdnm = $ENV{HDDOMAIN};

   if ($dtype eq "Birthday") {
      $dimg = "<IMG SRC=\"$hdnm/images/bday.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"birthday\">";
      return $dimg;
   } 
   
   if ($dtype eq "SendEmail") {
      $dimg = "<IMG SRC=\"$hdnm/images/sendemail.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\", ALT=\"sendemail\">";
      return $dimg;
   }

   if ($dtype eq "PhoneCall") {
      $dimg = "<IMG SRC=\"$hdnm/images/phone.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"phone call\">";
      return $dimg;
   }

   if ($dtype eq "TV Program") {
      $dimg = "<IMG SRC=\"$hdnm/images/tv.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"tv program\">";
      return $dimg;
   }

   if ($dtype eq "Graduation") {
      $dimg = "<IMG SRC=\"$hdnm/images/graduation.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"graduation\">";
      return $dimg;
   }

   if ($dtype eq "Games") {
      $dimg = "<IMG SRC=\"$hdnm/images/baseball.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"games\">";
      return $dimg;
   }

   if ($dtype eq "Festival") {
      $dimg = "<IMG SRC=\"$hdnm/images/festival.jpg\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"festival\">";
      return $dimg;
   }

   if ($dtype eq "Holiday") {
      $dimg = "<IMG SRC=\"$hdnm/images/vacation1.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"holiday\">";
      return $dimg;
   }

   if ($dtype eq "Concerts") {
      $dimg = "<IMG SRC=\"$hdnm/images/guitar.jpg\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"concerts\">";
      return $dimg;
   }

   if ($dtype eq "Chat") {
      $dimg = "<IMG SRC=\"$hdnm/images/chat.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"chat\">";
      return $dimg;
   }

   if ($dtype eq "Picnic") {
      $dimg = "<IMG SRC=\"$hdnm/images/chat.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"picnic\">";
      return $dimg;
   }

   if ($dtype eq "Party") {
      $dimg = "<IMG SRC=\"$hdnm/images/chat.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"party\">";
      return $dimg;
   }

   if ($dtype eq "Parental") {
      $dimg = "<IMG SRC=\"$hdnm/images/newsman.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"parental\">";
      return $dimg;
   }

   if ($dtype eq "Conference") {
      $dimg = "<IMG SRC=\"$hdnm/images/meeting.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"conference\">";
      return $dimg;
   }

   if ($dtype eq "Meeting") {
      $dimg = "<IMG SRC=\"$hdnm/images/meeting.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"meeting\">";
      return $dimg;
   }

   if ($dtype eq "Reunion") {
      $dimg = "<IMG SRC=\"$hdnm/images/meeting.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"reunion\">";
      return $dimg;
   }


   if ($dtype eq "BBQ") {
      $dimg = "<IMG SRC=\"$hdnm/images/bbq.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"bbq\">";
      return $dimg;
   }

   if ($dtype eq "Movie") {
      $dimg = "<IMG SRC=\"$hdnm/images/reelrite.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"movie\">";
      return $dimg;
   }

   if ($dtype eq "Other") {
      $dimg = "<IMG SRC=\"$hdnm/images/other.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"other\">";
      return $dimg;
   }

   if ($dtype eq "Interview") {
      $dimg = "<IMG SRC=\"$hdnm/images/interview.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"interview\">";
      return $dimg;
   }

   if ($dtype eq "Doctor") {
      $dimg = "<IMG SRC=\"$hdnm/images/doctor.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"doctor\">";
      return $dimg;
   }

   if ($dtype eq "Anniversary") {
      $dimg = "<IMG SRC=\"$hdnm/images/shopping.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"anniversary\">";
      return $dimg;
   }

   if ($dtype eq "SendRequest") {
      $dimg = "<IMG SRC=\"$hdnm/images/sendrequest.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"sendrequest\">";
      return $dimg;
   }

   if ($dtype eq "Pay Bills") {
      $dimg = "<IMG SRC=\"$hdnm/images/1dollar.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"sendrequest\">";
      return $dimg;
   }

   if ($dtype eq "Shopping") {
      $dimg = "<IMG SRC=\"$hdnm/images/shopping.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"shopping\">";
      return $dimg;
   }

   if ($dtype eq "MailLetter") {
      $dimg = "<IMG SRC=\"$hdnm/images/letter.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"  ALT=\"letter\">";
      return $dimg;
   }


   return("");
}

# vw = view week, view day, view month, view year, new item(n), exist item(i) 
# mo = month  dy=day yr=year vw=view en=entrynumber  a=action f=function
# functions event(e), todo(t), journal(j)
# actions   display(d), edit(e), remove(r)
#
sub createSubjectLink {

   my($dtype, $en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $subject, $jvw, $business, $login, $desc, $delete) = @_; 
   $burl = $url; 
   $e = "de";

   $burl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=e&vw=i&jvw=$jvw");
   $hr = "<HR>";

   $hdnm = $ENV{HDDOMAIN};

   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
      $showbusy = "";
   }
   $dimg = createDtypeImg($dtype);

   if ($delete == 1) {
      $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a>");
   } else {
      $imgurl = adjusturl ("$dimg $showbusy");
   }


   if ($subject ne "") {
      $etitle = $subject;
   } else { 
      $etitle = $dtype;
   }

   $hourlen = length($hour);
   if ($hourlen eq "1") {
       $hour = "&nbsp;$hour";
   }

  
   if ($delete == 1) { 
      $addeventtop = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=u\"><IMG SRC=\"$hdnm/images/addevent.gif\" BORDER=\"0\" ALT=\"Add Event To My Personal Calendar\"></a>");
     $burlhref1 = "<CENTER><a href=\"$burl\">$etitle</a> <BR>$desc <BR> $hour $min $meridian <BR> $imgurl $addeventtop </CENTER> $hr";
   } else {
     $addeventtop = ""; 
     $burlhref1 = "<CENTER>($login) $etitle <BR>$desc <BR> $hour $min $meridian <BR> $imgurl $addeventtop </CENTER> $hr";
   }

   $burlhref = adjusturl($burlhref1);
   return $burlhref;

}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $delete) = @_;

   $dimg = createDtypeImg($dtype);
   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
       $showbusy = "";
   }

   if ($delete == 1) {
      $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a><BR><BR>");
   } else {
      $imgurl = adjusturl ("$dimg $showbusy");
   }

   return $imgurl;
}


sub createWeeklyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $delete) = @_;

   $dimg = createDtypeImg($dtype);

   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
      $showbusy = "";
   }

   #$imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a><BR><BR>");

   if ($delete == 1) {
       $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a><BR>");
   } else {
	$imgurl = adjusturl ("$dimg $showbusy");
   }
   return $imgurl;

}


sub initializeEvents {
   my($numevents) = @_;
   for ($z = 0; $z <= $numevents; $z = $z+1) {
      $events[$z] = "";
   }
   return($events); 
}

sub initializeImageList {
   my($numevents) = @_;
   for ($r = 0; $r <= $numevents; $r = $r+1) {
      $imglist[$r] = "";
   }
   return($imglist); 
}

sub setEventDisplayRec {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc) = @_;

   if ($sc eq "p") { 
      #if ((isCalPublic($businessme)) != 1) {
      #   return $prml;
      #}
   } 

  if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
   }

   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
         'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   
   if ($vwtype eq "d") {
      $numevents = 19;
   } else {
     if ($vwtype eq "w") {
         $numevents = 8;
     } else {
       if ($vwtype eq "m") {
          $numevents = 42;
       }
     }
   }                      


   $events = initializeEvents($numevents);
   $imglist = initializeImageList($numevents);

   (@records) = sort keys %appttab;


   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];                              
      if ($onekey ne "")  {
         if (exists $appttab{$onekey}) {
	    if ($sc eq "p") {
               if ($appttab{$onekey}{'share'} eq "Private") {
                   next;
	       }
	    }	
            $year = $appttab{$onekey}{'year'};
            $month = $appttab{$onekey}{'month'};
            $day = $appttab{$onekey}{'day'};
    

            # isCurrentYear and isCurrentMonth are relevant checks 
            # for all view types.

            if ((isCurrentYear($year, $cyear)) != 1) {      
	       next;
	    }

            if (($vwtype eq "d") || ($vwtype eq "m")) {
               if ((isCurrentMonth($month, $cmonth)) != 1) {
	          next;
	       }
            }      

            if ($vwtype eq "d") {
	       if ((isCurrentDay($day, $cday)) != 1) {
                  next;
               }
            }

            if ($vwtype eq "w") {
	       if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                  next;
               }
            }

            $year = $appttab{$onekey}{'year'};
            $month = $appttab{$onekey}{'month'};
            $day = $appttab{$onekey}{'day'};
            $hour = $appttab{$onekey}{'hour'};
            $min = $appttab{$onekey}{'min'};
            $meridian = $appttab{$onekey}{'meridian'};
            $free = $appttab{$onekey}{'free'};

            if (($sc eq "p") && ($appttab{$onekey}{'share'} eq "Showasbusy")) {
                $subject = "Busy";
            } else {
                $subject = $appttab{$onekey}{'subject'};
	    }

            $dtype = $appttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
	       if ($vwtype eq "m") {
	          $eventnum = $day - 1;
	       } else {
	          if ($vwtype eq "w") {
	             $eventnum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
                  }
	       }
            } 

	    # append the events for this eventnum.
	    $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $appttab{$onekey}{desc}, 1);

            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, 1);
            }
         }
      }    
   }

   if ($vwtype eq "d") {
      $prml = setDailyPrml($prml, $events, $numevents, $imglist);
   }  

   if ($vwtype eq "m") { 
      $prml = setMonthlyPrml($prml, $events, $numevents);
   }

   if ($vwtype eq "w") {
      $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);
   }

   return $prml;
}

sub setDailyPrml {
   my($prml, $events, $numevents, $imglist) = @_;
   for ($i = 0; $i <= $numevents; $i = $i + 1) {
      if ($events[$i] ne "") {
         $prml = strapp $prml, "evtlist$i=$events[$i]";
         #$prml = strapp $prml, "imglist$i=$imglist[$i]";
      } else {
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "evtlist$i=$space";
         #$space = adjusturl("&nbsp;<BR><BR>");
         #$prml = strapp $prml, "imglist$i=$space";
      }
   }
   return $prml;
}

sub setTodoDailyPrml {

   my($prml, $todos, $numtodo, $timglist) = @_;

   for ($s = 0; $s <= $numtodo; $s = $s + 1) {
      if ($todos[$s] ne "") {
         $prml = strapp $prml, "evtlist$s=$todos[$s]";
         #$prml = strapp $prml, "imglist$s=$timglist[$s]";
      } else {
         #status ("else todolist[$s] = $todos[$s]");
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "evtlist$s=$space";
         #$space = adjusturl("&nbsp;<BR><BR>");
         #$prml = strapp $prml, "imglist$s=$space";
      }
   }
   return $prml;
}         
            
sub setWeeklyPrml {
   my($prml, $events, $numevents, $imglist) = @_;

   #print "numevents = $numevents \n";
   $q = 1;
   for ($k = 0; $k < $numevents; $k = $k + 1) {
      if ($events[$k] ne "") {
         $prml = strapp $prml, "evtlist$q=$events[$k]";
         #$prml = strapp $prml, "imglist$q=$imglist[$k]";
      } else {
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "evtlist$q=$space";
         #$space = adjusturl("&nbsp;");
         #$prml = strapp $prml, "imglist$q=$space";
      }
      $q = $q + 1;
   }
   return $prml;
}


sub setTodoWeeklyPrml {

   my($prml, $todos, $numtodo, $timglist) = @_;

   $u = 1;
   for ($v = 0; $v < $numtodo; $v = $v + 1) {
      if ($todos[$v] ne "") {
         $prml = strapp $prml, "evtlist$u=$todos[$v]";
         #$prml = strapp $prml, "imglist$u=$timglist[$v]";
      } else {
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "evtlist$u=$space";
         #$space = adjusturl("&nbsp;<BR><BR>");
         #$prml = strapp $prml, "imglist$u=$space";
      }
      $u = $u + 1;
   }
   return $prml;
}


sub setMonthlyPrml {
   my($prml, $events, $numevents) = @_;

   #print "numevents = $numevents \n";
   $n = 1;
   for ($m = 0; $m < $numevents; $m = $m + 1) {
      if ($events[$m] ne "") {
         $prml = strapp $prml, "day$n=$events[$m]";
      } else {
         $space = adjusturl("&nbsp;");
         $prml = strapp $prml, "day$n=$space";
	 #print "day = day$n \n";
      }
      $n = $n + 1;
   }
   return $prml;
}

sub setTodoMonthlyPrml {
   my($prml, $todos, $numtodo) = @_;

   $w = 1;
   for ($x = 0; $x < $numtodo; $x = $x + 1) {
      if ($todos[$x] ne "") {
         $prml = strapp $prml, "day$w=$todos[$x]";
      } else {
         $space = adjusturl("&nbsp;");
         $prml = strapp $prml, "day$w=$space";
      }
      $w = $w + 1;
   }
   return $prml;
}


sub setEventEditRec {
  
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw, $business, $sc) = @_;


  hddebug "companycalutil::setEventEditRec()";

  if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
   }

   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
         'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   $onekey = $ceno;
   if (exists $appttab{$onekey}) {
      $prml = strapp $prml, "year=$appttab{$onekey}{'year'}";
      ($monthstr = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $prml = strapp $prml, "meridian=$appttab{$onekey}{'meridian'}";
      $prml = strapp $prml, "month=$monthstr"; 
      $prml = strapp $prml, "monthnum=$appttab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$appttab{$onekey}{'day'}";

      $recurtype = $appttab{$onekey}{'recurtype'};
      if ($recurtype eq "") {
         $recurtype = "Daily";
      }

      $prml = strapp $prml, "recurtype=$recurtype";
      $prml = strapp $prml, "hour=$appttab{$onekey}{'hour'}";
      if ($appttab{$onekey}{'min'} eq "00") {
         $min = 0;
      } else {
         $min = $appttab{$onekey}{'min'};
      }
      $prml = strapp $prml, "min=$min";
      $prml = strapp $prml, "sec=$appttab{$onekey}{'sec'}";
                  $prml = strapp $prml, "zone=$appttab{$onekey}{'zone'}";
                  $zone = getzonestr($appttab{$onekey}{'zone'});
                  $prml = strapp $prml, "zonestr=$zone";

                  $share = $appttab{$onekey}{'share'};
                  if ($share eq "") {
	             $share = "Public";
                  }
                  $prml = strapp $prml, "share=$share";

                  $free = $appttab{$onekey}{'free'};
                  if ($free eq "") {
	             $free = "Free";
                  }
                  $prml = strapp $prml, "free=$free";
                  $prml = strapp $prml, "atype=$appttab{$onekey}{'atype'}";
                  $prml = strapp $prml, "dtype=$appttab{$onekey}{'dtype'}";
                  if (($appttab{$onekey}{'share'} eq "Showasbusy") && ($sc eq "p")) {
                     $prml = strapp $prml, "subject=BUSY";
                     $prml = strapp $prml, "desc=BUSY";
                  } else {
		     $subject = adjusturl($appttab{$onekey}{'subject'});
                     $prml = strapp $prml, "subject=$subject";
		     $desc = adjusturl($appttab{$onekey}{'desc'});
                     $prml = strapp $prml, "desc=$desc";
                  }
		  $prml = strapp $prml, "dhour=$appttab{$onekey}{'dhour'}";
                  $dmin = $appttab{$onekey}{'dmin'};
                  if (($dmin eq "00") || ($dmin eq "")) {
                     $dmin = 0;
                  } 
                  $prml = strapp $prml, "dmin=$dmin";
                  $prml = strapp $prml, "contact=";
     } else {
	##display the details of user's calendar.
        $prml = empEventDetails($onekey, $business, $prml);
     }
     return $prml;
}

sub empEventDetails {

   my ($onekey, $business, $prml) = @_;

   if (!-d "$ENV{HDDATA}/business/business/$business/peopletab") {
      return $prml;
   }

   $app_tab = 0;
   $todo_tab = 0;

   tie %peopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
   SUFIX => '.rec',
     SCHEMA => {
      ORDER => ['login', 'business']};

   foreach $mem (sort keys %peopletab) { 
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
              'hour', 'min', 'meridian', 'dhour', 'dmin',
             'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
             'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type']};

      if (exists($appttab{$onekey})) {
         ($monthstr = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $appttab{$onekey}{'day'} $appttab{$onekey}{'year'} $appttab{$onekey}{'meridian'} <BR> Free/Busy: $appttab{$onekey}{free}<BR>";
         if ($appttab{$onekey}{'share'} eq "Private") {
            $subject = "Details: Private<BR>";
            $subject .= "User: $mem <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            #hddebug "subject1 = $subject";
            return $prml;
         }
         $subject = "Details: $appttab{$onekey}{'subject'}<BR> Description: $appttab{$onekey}{'desc'}<BR>";
         $subject .= "User: $mem <BR> $subject_d";
         $subject = adjusturl $subject;
         $prml = strapp $prml, "subdetails=$subject";
         #hddebug "subject1 = $subject";
         return $prml;
      }

      if (-d "$ENV{HDDATA}/$mem/todotab") {
         # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$mem/todotab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
             'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

         if (exists($todotab{$onekey})) {
	    $todo_tab == 1;
            ($monthstr = getmonthstr($todotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
            $subject_d .= "Date: $monthstr $todotab{$onekey}{'day'} $todotab{$onekey}{'year'} $todotab{$onekey}{'meridian'} <BR> Priority: $todotab{$onekey}{'priority'} <BR> Status: $todotab{$onekey}{'status'}";
            if ($todotab{$onekey}{'share'} eq "Private") {
               $subject = "Event & To-do Details: Private<BR>";
               $subject .= "User: $mem <BR> $subject_d";
               $subject = adjusturl $subject;
               $prml = strapp $prml, "subdetails=$subject";
               return $prml;
	    }
         }
      }
   }

   return $prml;
}
                        
sub deleteEvent {

   my($ceno, $lg, $business) = @_;
   hddebug "companycalfuncs::deleteEvent";

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
       return $prml;
   }

   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
         'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   if (exists($appttab{$ceno})) {
      delete $appttab{$ceno};
      tied(%appttab)->sync();   
   }
   return $prml;
}

sub addEvent {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact) = @_; 
 
  hddebug "companycalfuncs::addEvent";

  if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
   }

   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
         'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   $entryno = getkeys();
   $appttab{$entryno}{'login'} = trim $lg;
   $appttab{$entryno}{'month'} = trim $emonth;
   $appttab{$entryno}{'day'} = trim $eday;
   $appttab{$entryno}{'year'} = trim $eyear;
   $appttab{$entryno}{'hour'} = trim $ehour;
   $appttab{$entryno}{'min'} = trim $emin;
   $appttab{$entryno}{'meridian'} = trim $emeridian;
   $appttab{$entryno}{'dhour'} = trim $edhour;
   $appttab{$entryno}{'dmin'} = trim $edmin;
   $appttab{$entryno}{'dtype'} = trim $edtype;
   $appttab{$entryno}{'atype'} = trim $eatype;
   $appttab{$entryno}{'desc'} = $edesc;
   $appttab{$entryno}{'zone'} = trim $ezone;
   $appttab{$entryno}{'recurtype'} = trim $erecurtype;
   $appttab{$entryno}{'share'} = trim $eshare;
   $appttab{$entryno}{'free'} = trim $efree;
   $appttab{$entryno}{'subject'} = trim $etitle;
   $appttab{$entryno}{'entryno'} = trim $entryno;
   if ($econtact ne "") {
      $eventdetails .= "Event: $etitle \n";
      $eventdetails .= "Event Type: $edtype \n";
      $eventdetails .= "Date:  $emonth-$eday-$eyear \n";
      $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
      $eventdetails .= "Description: $edesc \n";
      $eventdetails .= "Frequency: $erecurtype \n";
      #$appttab{$entryno}{'contact'} = trim $econtact;
   }

   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno);
   }
   tied(%appttab)->sync();
   #return $prml;
}

sub updateEvent  {

   my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact) = @_; 

  hddebug "companycalutil::updateEvent()";

  if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
       return $prml;
   }

   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
         'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   if (exists $appttab{$entryno}) {
      $appttab{$entryno}{'login'} = trim $lg;
      $appttab{$entryno}{'month'} = trim $emonth;
      $appttab{$entryno}{'day'} = trim $eday;
      $appttab{$entryno}{'year'} = trim $eyear;
      $appttab{$entryno}{'hour'} = trim $ehour;
      $appttab{$entryno}{'min'} = trim $emin;
      $appttab{$entryno}{'meridian'} = trim $emeridian;
      $appttab{$entryno}{'dhour'} = trim $edhour;
      $appttab{$entryno}{'dmin'} = trim $edmin;
      $appttab{$entryno}{'dtype'} = trim $edtype;
      $appttab{$entryno}{'atype'} = trim $eatype;
      $appttab{$entryno}{'desc'} = $edesc;
      $appttab{$entryno}{'zone'} = trim $ezone;
      $appttab{$entryno}{'recurtype'} = trim $erecurtype;
      $appttab{$entryno}{'share'} = trim $eshare;
      $appttab{$entryno}{'free'} = trim $efree;
      $appttab{$entryno}{'subject'} = trim $etitle;
      $appttab{$entryno}{'entryno'} = trim $entryno;
      if ($econtact ne "") {
         $eventdetails .= "Event: $etitle \n";
         $eventdetails .= "Event Type: $edtype \n";
         $eventdetails .= "Date: $emonth-$eday-$eyear \n";
         $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
         $eventdetails .= "Description: $edesc \n";
         $eventdetails .= "Frequency: $erecurtype \n";
      }
   }                                                                                                  
   tied(%appttab)->sync();
   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno);
   }
   return $prml;

}

sub displayTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc) = @_;

   if ($sc eq "p") {
      if ((isCalPublic($business)) != 1) {
         return $prml;
      }
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
   }

   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

   if ($vwtype eq "d") {
      $numtodo = 19;
   } else {
     if ($vwtype eq "w") {
         $numtodo= 8;
     } else {
       if ($vwtype eq "m") {
          $numtodo = 42;
       }
     }
   }

   $todomntcnt = 0;
   $todos = initializeEvents($numtodo);
   $timglist = initializeImageList($numtodo);

   (@records) = sort keys %todotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {
         $onekey = $records[$g]; 
         if (!exists($todotab{$onekey})) {
            next; 
         }
	 if ($sc eq "p") {
            if ($todotab{$onekey}{'share'} eq "Private") {
	       next; 
	    }
	 }
         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};

         #status ("calday = $cday <BR>");
         #status ("month = $month <BR>");
         #status ("day = $day <BR>");
         # isCurrentYear and isCurrentMonth are relevant checks
         # for all view types.

         if ((isCurrentYear($year, $cyear)) != 1) {
             next;
          }

         if (($vwtype eq "d") || ($vwtype eq "m")) {
            if ((isCurrentMonth($month, $cmonth)) != 1) {
               next;
            }
         }

         if ($vwtype eq "d") {
            if ((isCurrentDay($day, $cday)) != 1) {
                next;
            }
            #status(" day =$day <BR>");
         }

         if ($vwtype eq "w") {
            if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};
         $hour = $todotab{$onekey}{'hour'};
         $meridian = $todotab{$onekey}{'meridian'};
         $subject = $todotab{$onekey}{'subject'};
         $priority = $todotab{$onekey}{'priority'};

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum 
         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, 1);

         if ($vwtype ne "m") {
            $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, 1);
         }
      }
   }


   if ($vwtype eq "d") {
      $prml = setTodoDailyPrml($prml, $todos, $numtodo, $timglist);
   }

   if ($vwtype eq "m") {
      $prml = setTodoMonthlyPrml($prml, $todos, $numtodo);
   }

   if ($vwtype eq "w") {
      $prml = setTodoWeeklyPrml($prml, $todos, $numtodo, $timglist);
   }

   return $prml;
}


sub createTodoLink {

   my($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $subject, $todomntcnt, $priority, $desc, $delete) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $todourl = $url;
   $e = "de";

   $todourl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=t&vw=i");

   $hr = "<HR>";

   if ($delete == 1) {
      $todoimgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a>");
   } else {
      $todoimgurl = "";
   }

   $pri = " Priority ";
   if ($subject ne "") {
     $todotitle = "Todo $subject$pri$priority";
   } else {
     $todotitle = "Todo$pri$priority";
   }

   if ($delete == 1) {
      $burlhref1 = "<CENTER><a href=\"$todourl\"><FONT COLOR=03c503>$todotitle</FONT></a> <BR><FONT COLOR=03c503>$desc <BR> $hour $meridian </FONT><BR> $todoimgurl </CENTER> $hr";
   } else {
      $burlhref1 = "<CENTER>($login)<FONT COLOR=03c503>$todotitle</FONT><BR><FONT COLOR=03c503>$desc <BR> $hour $meridian </FONT><BR> $todoimgurl </CENTER> $hr";
   }
   $burlhref = adjusturl($burlhref1);
   #status ("href = $burlhref");
   return $burlhref;

}

sub createTodoWeeklyImageLink {

   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw) = @_;

   $hdnm = $ENV{HDDOMAIN};

   if ($delete == 1) { 
      $imgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a><BR><BR>");
   } else {
      return $url;
   }
   return $imgurl;

}


sub createTodoDailyImageLink {
   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $delete ) = @_;

   $hdnm = $ENV{HDDOMAIN};
   if ($delete == 1) {
      $timgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a><BR><BR>");
   } else {
       return $url;
   }

   return $timgurl;
}


sub editTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $business) = @_;


   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };


   $onekey = $ceno;
   if (exists($todotab{$onekey})) {
      $prml = strapp $prml, "subject=$todotab{$onekey}{'subject'}";
      $prml = strapp $prml, "desc=$todotab{$onekey}{'desc'}";
      ($monthstr = getmonthstr($todotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $prml = strapp $prml, "month=$monthstr";
      $prml = strapp $prml, "monthnum=$todotab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$todotab{$onekey}{'day'}";                   
      $prml = strapp $prml, "year=$todotab{$onekey}{'year'}";
      $prml = strapp $prml, "meridian=$todotab{$onekey}{'meridian'}";
      $prml = strapp $prml, "priority=$todotab{$onekey}{'priority'}";
      $prml = strapp $prml, "status=$todotab{$onekey}{'status'}";
      $prml = strapp $prml, "share=$todotab{$onekey}{'share'}";
      $prml = strapp $prml, "hour=$todotab{$onekey}{'hour'}";
   }
   return $prml;


}

sub deleteTodo {
   my($ceno, $lg, $business) = @_; 

   hddebug "companycalfuncs::deleteTodo";

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
       return $prml;
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

   if (exists($todotab{$ceno})) {
      delete $todotab{$ceno};
      tied(%todotab)->sync();   
   }
   return $prml;
}

sub addTodo {

   my($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $business) = @_; 
  
  hddebug "companycalfuncs::addTodo";


   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };


   $entryno = getkeys();
   $todotab{$entryno}{'login'} = trim $lg;      
   $todotab{$entryno}{'subject'} = trim $ttitle;      
   $todotab{$entryno}{'desc'} = trim $tdesc; 
        
   $todotab{$entryno}{'month'} = trim $tmonth;      
   $todotab{$entryno}{'day'} = trim $tday;      
   $todotab{$entryno}{'year'} = trim $tyear;      
   $todotab{$entryno}{'hour'} = trim $thour;      
   $todotab{$entryno}{'meridian'} = trim $tmeridian;      
   $todotab{$entryno}{'share'} = trim $tshare;      
   $todotab{$entryno}{'entryno'} = trim $entryno;      
   $todotab{$entryno}{'hour'} = trim $thour;      
   $todotab{$entryno}{'priority'} = trim $tpriority;      
   $todotab{$entryno}{'status'} = trim $tstatus;      
   $todotab{$entryno}{'$entryno'} = trim $$entryno;      

   tied(%todotab)->sync(); 
   return $prml;
}

sub updateTodo {
    my($entryno, $etitle,  $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $lg, $business) = @_; 


   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
       return $prml;
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

    if (exists($todotab{$entryno})) {
       $todotab{$entryno}{'login'} = trim $lg;
       $todotab{$entryno}{'subject'} = trim $etitle;
       $todotab{$entryno}{'desc'} = trim $edesc;

       $todotab{$entryno}{'month'} = trim $emonth;
       $todotab{$entryno}{'day'} = trim $eday;
       $todotab{$entryno}{'year'} = trim $eyear;
       $todotab{$entryno}{'hour'} = trim $ehour;
       $todotab{$entryno}{'meridian'} = trim $emeridian;
       $todotab{$entryno}{'share'} = trim $eshare;
       $todotab{$entryno}{'priority'} = trim $epriority;
       $todotab{$entryno}{'status'} = trim $estatus;
       $todotab{$entryno}{'entryno'} = trim $entryno;
       tied(%todotab)->sync();
    }
}


sub publishEvent {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $business ) = @_;

   hddebug "companycalfuncs::publishEvent";

   if ((isCalPublic($business)) != 1) {
      return $prml;
   };

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
   }

   # bind appttab appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   if ($vwtype eq "d") {
      $numevents = 19;
   } else {
     if ($vwtype eq "w") {
         $numevents = 8;
     } else {
       if ($vwtype eq "m") {
          $numevents = 42;
       }
     }
   }


   $events = initializeEvents($numevents);
   $imglist = initializeImageList($numevents);

   #if (exists($appttab{$lg} )) {
      (@records) = sort keys %appttab;
      if ($#records >= 0) {
         for ($g = 0; $g <= $#records; $g = $g+1) {
            $onekey = $records[$g];
            if (exists($appttab{$onekey})) {
               if ($appttab{$onekey}{'share'} eq "Public") {
                  $month = $appttab{$onekey}{'month'};
                  $day=$appttab{$onekey}{'day'};
                  $year=$appttab{$onekey}{'year'};

                  # isCurrentYear and isCurrentMonth are relevant checks
                  # for all view types.
                  if ((isCurrentYear($year, $cyear)) != 1) {
                     next;
                 }

                 if (($vwtype eq "d") || ($vwtype eq "m")) {
                    if ((isCurrentMonth($month, $cmonth)) != 1) {
                       next;
                    }
                 }

                 if ($vwtype eq "d") {
                    if ((isCurrentDay($day, $cday)) != 1) {
                       next;
                    }
                 }

                 if ($vwtype eq "w") {
                    if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                       next;
                    }
                 }

                 $year = $appttab{$onekey}{'year'};
                 $month = $appttab{$onekey}{'month'};
                 $day = $appttab{$onekey}{'day'};
                 $hour = $appttab{$onekey}{'hour'};
                 $min = $appttab{$onekey}{'min'};
                 $meridian = $appttab{$onekey}{'meridian'};
                 $free = $appttab{$onekey}{'free'};
                 $subject = $appttab{$onekey}{'subject'};
                 $dtype = $appttab{$onekey}{'dtype'};

                 if ($vwtype eq "d") {
                    $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
                 } else {
                    if ($vwtype eq "m") {
                       $eventnum = $day - 1;
                    } else {
                       if ($vwtype eq "w") {
                          $eventnum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
                       }
                    }
                 }

                 # append the events for this eventnum.
                 $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $appttab{$onekey}{desc}, 0);

                  if ($vwtype ne "m") {
                     $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, 0);
                  }
               }
            }
         }
      }
   #}


   if ($vwtype eq "d") {
      $prml = setDailyPrml($prml, $events, $numevents, $imglist);
   }

   if ($vwtype eq "m") {
      $prml = setMonthlyPrml($prml, $events, $numevents);
   }

   if ($vwtype eq "w") {
      $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);
   }

   return $prml;
}



sub publishTodo {

   my($prml, $vwtype, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $a, $en, $f, $sc, $business) = @_;

   if ((isCalPublic($business)) != 1) {
       return $prml;
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };




   if ($vwtype eq "d") {
      $numtodo = 19;
   } else {
     if ($vwtype eq "w") {
         $numtodo= 8;
     } else {
       if ($vwtype eq "m") {
          $numtodo = 42;
       }
     }
   }

   $todomntcnt = 0;
   $todos = initializeEvents($numtodo);
   $timglist = initializeImageList($numtodo);

   (@records) = sort keys %$todotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {

         $onekey = $records[$g];
         if (!exists($todotab{$onekey})) {  
            next; 
         }

         if ($todotab{$onekey}{'share'} eq "Private") { 
	    next;
         }

         #status ("entryno = $onekey <BR>");
         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};

         #status ("calmonth = $cmonth <BR>");
         #status ("calday = $cday <BR>");
         #status ("month = $month <BR>");
         #status ("day = $day <BR>");
         # isCurrentYear and isCurrentMonth are relevant checks
         # for all view types.

         if ((isCurrentYear($year, $cyear)) != 1) {
             next;
          }

         if (($vwtype eq "d") || ($vwtype eq "m")) {
            if ((isCurrentMonth($month, $cmonth)) != 1) {
               next;
            }
         }

         if ($vwtype eq "d") {
            if ((isCurrentDay($day, $cday)) != 1) {
                next;
            }
            #status(" day =$day <BR>");
         }

         if ($vwtype eq "w") {
            if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};
         $hour = $todotab{$onekey}{'hour'};
         $meridian = $todotab{$onekey}{'meridian'};
         $subject = $todotab{$onekey}{'subject'};
         $priority = $todotab{$onekey}{'priority'};

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum

         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, 0);

         if ($vwtype ne "m") {
            $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, 0);
         }
      }
   }


   if ($vwtype eq "d") {
      $prml = setTodoDailyPrml($prml, $todos, $numtodo, $timglist);
   }

   if ($vwtype eq "m") {
      $prml = setTodoMonthlyPrml($prml, $todos, $numtodo);
   }

   if ($vwtype eq "w") {
      $prml = setTodoWeeklyPrml($prml, $todos, $numtodo, $timglist);
   }

   return $prml;
}


sub isCalPublic {

   my($business) = @_;

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle', 'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone', 'fax', 'url', 'email', 'other', 'list', 'view', 'publish' ] };

   if (exists($businesstab{$business})) {
     if ($businesstab{$business}{publish} eq "CHECKED") {
        return 1;
     }
   }

   return 0;
}

sub regEmailContacts {

   my($contacts, $mname, $eventdetails, $entryno) = @_;

   $contacts = trim $contacts;
   $contacts = "\L$contacts";
   (@hshemail) = split ",", $contacts;
  
    
   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
      'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

    $cntr = 0;
    foreach $cn (@hshemail) {
       if (notEmailAddress($cn)) {	    
          next;
       }
       $cntr = $cntr + 1;
       $cn = "\L$cn";
       $cn = trim $cn;
       if ("\L$logtab{$mname}{email}" eq $cn) {
	  next;
       }
  
       if ($cn eq "") {
          next;
       }
       # bind surveytab table vars
       tie %surveytab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/surveytab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite'] };

       if (exists ($logtab{$cn} ) ) {
          if ($surveytab{$cn}{calinvite} ne "CHECKED") {
             next;
          }
          $login = $cn;
          $cn = $logtab{$cn}{email};
          $eemail = 1;          
          $oldlogin = $login;
       } else {
          ($login, $domain) = split '@', $cn;
          $login = trim $login;
          $eemail = 0;          
       }

       if ($login =~ /\&/) {
          next;
       }
       if ( (!(notLogin $login)) || (exists ($logtab{$login} )) ) {
          if ($eemail ne "1") {
	     $oldlogin = $login;
             if (exists($logtab{$login} )) {
      	        $login = "l$login$$-$cntr";
             }
	  }
       }
       if ($eemail ne "1") {
          $logtab{$login}{'login'} = $login;
          $logtab{$login}{'fname'} = $login;
          $logtab{$login}{'password'} = $login;
          $logtab{$login}{'email'} = $cn;
          $logtab{$login}{'zone'} = $logtab{$mname}{zone};
          $surveytab{$login}{'login'} = $login;
          $surveytab{$login}{'hearaboutus'} = "Friend";
          $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
          tied(%surveytab)->sync();
       }


       $emsg = "Dear $logtab{$oldlogin}{fname}, \n \n";
       $uname = $logtab{$mname}{'fname'} . " " . $logtab{$mname}{'lname'};
       $emsg .= "You have been invited by $uname to an event. \n \n";
       $emsg .= "Event Details: \n";
       $emsg .=  $eventdetails;
       $emsg .=  "\n\n";
       $emsg .= "If you would like to contact $uname directly, please send an email to $uname at $logtab{$mname}{'email'}. $uname's member login ID on HotDiary is \"$mname\".\n";

       if ($eemail ne "1") {
           $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
           $emsg .= "Login: $login \n";
           $emsg .= "Password: $logtab{$login}{'password'}\n\n";
           $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
       }

       $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
       $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Internet Products and Services\n";

       qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
       qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};

       if ($eemail ne "1") {
          system "mkdir -p $ENV{HDREP}/$login";
          system "chmod 755 $ENV{HDREP}/$login";
          system "mkdir -p $ENV{HDHOME}/rep/$login";
          system "mkdir -p $ENV{HDDATA}/$login";
          system "chmod 755 $ENV{HDDATA}/$login";
          system "touch $ENV{HDDATA}/$login/addrentrytab";
          system "chmod 755 $ENV{HDDATA}/$login/addrentrytab";
          system "mkdir -p $ENV{HDDATA}/$login/addrtab";
          system "chmod 755 $ENV{HDDATA}/$login/addrtab";
          system "touch $ENV{HDDATA}/$login/apptentrytab";
          system "chmod 660 $ENV{HDDATA}/$login/apptentrytab";
          system "mkdir -p $ENV{HDDATA}/$login/appttab";
          system "chmod 770 $ENV{HDDATA}/$login/appttab";
          system "mkdir -p $ENV{HDDATA}/groups/$login/personal/pgrouptab";
          system "mkdir -p $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
          system "mkdir -p $ENV{HDDATA}/groups/$login/founded/fgrouptab";
          system "chmod -R 770 $ENV{HDDATA}/groups/$login";
          system "cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";
          system "cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$login";
          system "chmod 775 $ENV{HDDATA}/$login/calendar_events.txt";

          system "mkdir -p $ENV{HDDATA}/$login/faxtab";
          system "chmod 755 $ENV{HDDATA}/$login/faxtab";

          system "mkdir -p $ENV{HDDATA}/$login/faxdeptab";
          system "chmod 755 $ENV{HDDATA}/$login/faxdeptab";
      }

      if ( (($eemail eq "1") && ($logtab{$login}{checkid} eq "CHECKED") ) || ($eemail ne "1") ) {
         system "/bin/cp $ENV{HDDATA}/$mname/appttab/$entryno.rec $ENV{HDDATA}/$login/appttab/$entryno.rec";
         # bind remind index table vars
         tie %remindtab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login'] };
         $remindtab{$login}{login} = $login;
         tied(%remindtab)->sync();
         system "chmod 777 $ENV{HDDATA}/aux/remindtab/$login.rec";

         #add the entry in the apptentrytab
         $tfile = "$ENV{HDDATA}/$login/apptentrytab";
         open thandle, ">>$tfile";
         printf thandle "%s\n", $entryno;
         close thandle;

         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$login/appttab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
                 'subject', 'street', 'city', 'state', 'zipcode', 'country',
                 'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

          $appttab{$entryno}{login} = $login;
          tied(%appttab)->sync();
       }
   }

#synch the database
   tied(%logtab)->sync();
 
}

sub addBusEventToMyCal {

   my($busen, $login, $business) = @_;

   hddebug "companycalfuncs::addBusEventToMyCal";
   hddebug("addbuseventtomycal busen = $busen, business = $business, login = $login");

   if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
       return $prml;
   }


   # bind todo table vars
   tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

   if (!exists $appttab{$busen}) { 
       return 0;
   }

   # bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$login/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'street', 'city', 'state', 
	'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
	 'confirm', 'id', 'type'] };                    

   # bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };
   $remindtab{$login}{login} = $login;
   tied(%remindtab)->sync();
   system "chmod 777 $ENV{HDDATA}/aux/remindtab/$login.rec";
  
   $entryno = getkeys(); 
   $appttab{$entryno}{'login'} = trim $login;
   $appttab{$entryno}{'month'} = $appttab{$busen}{month};
   $appttab{$entryno}{'day'} = $appttab{$busen}{day};   
   $appttab{$entryno}{'year'} = $appttab{$busen}{year};   
   $appttab{$entryno}{'hour'} = $appttab{$busen}{hour};   
   $appttab{$entryno}{'min'} = $appttab{$busen}{min};   
   $appttab{$entryno}{'meridian'} = $appttab{$busen}{meridian};   
   $appttab{$entryno}{'dhour'} = $appttab{$busen}{dhour};   
   $appttab{$entryno}{'dmin'} = $appttab{$busen}{dmin};   
   $appttab{$entryno}{'dtype'} = $appttab{$busen}{dtype};   
   $appttab{$entryno}{'atype'} = $appttab{$busen}{atype};   
   $appttab{$entryno}{'desc'} = $appttab{$busen}{desc};   
   $appttab{$entryno}{'zone'} = $appttab{$busen}{zone};  
   $appttab{$entryno}{'recurtype'} = $appttab{$busen}{recurtype};   
   $appttab{$entryno}{'share'} = $appttab{$busen}{share};   
   $appttab{$entryno}{'free'} = $appttab{$busen}{free};   
   $appttab{$entryno}{'subject'} = $appttab{$busen}{subject};   
   $appttab{$entryno}{'entryno'} = $entryno;
   
   #add the entry in the apptentrytab
   $tfile = "$ENV{HDDATA}/$login/apptentrytab";
   open thandle, ">>$tfile";
   printf thandle "%s\n", $entryno;
   close thandle;

   tied(%appttab)->sync();              
   return 1;
}


sub displayEventsAndTodos {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc) = @_;

   hddebug "companycalfuncs::displayEventsAndTodos, business=$business";

   if ($sc eq "p") {
      if ((isCalPublic($business)) != 1) {
         return $prml;
      }
   }


   if ($vwtype eq "d") {
      $numevents = 19;
   } else {
     if ($vwtype eq "w") {
         $numevents = 8;
     } else {
       if ($vwtype eq "m") {
          $numevents = 42;
       }
     }
   }
   $events = initializeEvents($numevents);
   $imglist = initializeImageList($numevents);
   $todomntcnt = 0;


   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle', 'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone', 'fax', 'url', 'email', 'other', 'list', 'view', 'publish' ] };

   hddebug "$businesstab{$business}{view}";
   ## onlycalendarview

   if (!exists($businesstab{$business})) {
      return $prml;
   }

   if ($businesstab{$business}{view} ne "cview") {
      $prml = mergedviewEmps($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc, $businesstab{$business}{view});
      return $prml;
   }
   
   if ($businesstab{$business}{view} eq "cview") {

      if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
         (!(-d "$ENV{HDDATA}/business/business/$business/calendar/appttab"))) {
          system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
          system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
          system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/appttab";
          system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/appttab";
      }

     hddebug "appttab exists";
      # bind appttab appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

      if ((!(-d "$ENV{HDDATA}/business/business/$business/calendar")) ||
         (!(-d "$ENV{HDDATA}/business/business/$business/calendar/todotab"))) {
          system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar";
          system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar";
          system "mkdir -p $ENV{HDDATA}/business/business/$business/calendar/todotab";
          system "chmod 755 $ENV{HDDATA}/business/business/$business/calendar/todotab";
      }
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

      $prml = setuplist($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, %appttab, %todotab, $events, $imglist, $todomntcnt);
   }

   return $prml;

}

sub mergedviewEmps {

   hddebug "companycalfuncs::mergedviewEmps, business=$business";
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc, $view) = @_;

   if ($sc eq "p") {
      if ((isCalPublic($business)) != 1) {
         return $prml;
      }
   }

   if ($vwtype eq "d") {
      $numevents = 19;
   } else {
     if ($vwtype eq "w") {
         $numevents = 8;
     } else {
       if ($vwtype eq "m") {
          $numevents = 42;
       }
     }
   }
   $events = initializeEvents($numevents);
   $imglist = initializeImageList($numevents);
   $todomntcnt = 0;

   if (!-d "$ENV{HDDATA}/business/business/$business/peopletab") {
      return $prml;
   }
   tie %peopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
   SUFIX => '.rec',
     SCHEMA => {
      ORDER => ['login', 'business']};
   foreach $mem (sort keys %peopletab) {
	$records = 0;
	hddebug "mem = $mem";
	$mem = trim $mem;
	if ($mem ne "bank") {
	   next;
	}
        %appttab = "";
        %todotab = "";
        if (-d "$ENV{HDDATA}/$mem/appttab") {
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
            (@records) = (sort keys %appttab);
        $num = $#records;
	hddebug "apppttab records = $num $mem";
         }

         if (-d "$ENV{HDDATA}/$mem/todotab") {
            # bind todo table vars
            tie %todotab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/$mem/todotab",
            SUFIX => '.rec',
            SCHEMA => {
                 ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
                  'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };
	}

        $num = $#records;
	hddebug "apppttab records = $num $mem";
        for ($y = 0; $y <= $num; $y = $y+1) {
          $onekey = $records[$y];
          if ($onekey ne "")  {
             if (exists $appttab{$onekey}) {
	       hddebug "appttab $mem";
                $year = $appttab{$onekey}{'year'};
                $month = $appttab{$onekey}{'month'};
                $day = $appttab{$onekey}{'day'};

                # isCurrentYear and isCurrentMonth are relevant checks
                # for all view types.

                if ((isCurrentYear($year, $cyear)) != 1) {
                   next;
                }

                if (($vwtype eq "d") || ($vwtype eq "m")) {
                   if ((isCurrentMonth($month, $cmonth)) != 1) {
                       next;
	           }
                }

               if ($vwtype eq "d") {
                  if ((isCurrentDay($day, $cday)) != 1) {
                     next;
                  }
               }

               if ($vwtype eq "w") {
                  if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                     next;
                  }
               }

               $year = $appttab{$onekey}{'year'};
               $month = $appttab{$onekey}{'month'};
               $day = $appttab{$onekey}{'day'};
               $hour = $appttab{$onekey}{'hour'};
               $min = $appttab{$onekey}{'min'};
               $meridian = $appttab{$onekey}{'meridian'};
               $free = $appttab{$onekey}{'free'};

               if (($sc eq "p") && ($appttab{$onekey}{'share'} eq "Showasbusy")) {
                   $subject = "Busy";
               } else {
                   if ($appttab{$onekey}{'share'} eq "Private") {
                       $subject = "Private";
                   } else {
                      $subject = $appttab{$onekey}{'subject'};
                   }
               }
               $dtype = $appttab{$onekey}{'dtype'};
               if ($vwtype eq "d") {
                  $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
               } else {
                  if ($vwtype eq "m") {
                     $eventnum = $day - 1;
                  } else {
                     if ($vwtype eq "w") {
                        $eventnum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
                     }
                  }
               }
	       hddebug "current $mem";
               # append the events for this eventnum.
               $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $mem, $appttab{$onekey}{desc}, 0);

               if ($vwtype ne "m") {
                  $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, 0);
               }
            }
         }
      }
      hddebug "came here before todotab";

      $records = (sort keys %todotab); 
      if ($#records >= 0) {
         for ($g = 0; $g <= $#records; $g = $g+1) {
            $onekey = $records[$g];
            if (!exists($todotab{$onekey})) {
               next;
            }
            $year = $todotab{$onekey}{'year'};
            $month = $todotab{$onekey}{'month'};
            $day = $todotab{$onekey}{'day'};

            #status ("calday = $cday <BR>");
            #status ("month = $month <BR>");
            #status ("day = $day <BR>");
            # isCurrentYear and isCurrentMonth are relevant checks
            # for all view types.

            if ((isCurrentYear($year, $cyear)) != 1) {
                next;
            }
            if (($vwtype eq "d") || ($vwtype eq "m")) {
               if ((isCurrentMonth($month, $cmonth)) != 1) {
                  next;
	       }
            }
            if ($vwtype eq "d") {
               if ((isCurrentDay($day, $cday)) != 1) {
                    next;
                }
            }

            if ($vwtype eq "w") {
                if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                    next;
               }
            }

            $year = $todotab{$onekey}{'year'};
            $month = $todotab{$onekey}{'month'};
            $day = $todotab{$onekey}{'day'};
            $hour = $todotab{$onekey}{'hour'};
            $meridian = $todotab{$onekey}{'meridian'};
            if ($todotab{$onekey}{'share'} eq "Private") {
               $subject = "Private";
            } else {
               $subject = $todotab{$onekey}{'subject'};
            }
            $priority = $todotab{$onekey}{'priority'};
	    if ($vwtype eq "d") {
               $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
            } else {
              if ($vwtype eq "m") {
                 $todonum = $day - 1;
                 $todomntcnt = $todmntcnt + 1;
              } else {
                 if ($vwtype eq "w") {
                    $todonum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
                 }
              }
            } 

            # append the todos for this todonum
            $events[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, 0);

            if ($vwtype ne "m") {
               $imglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, 0);
            }
         }
      }
   }

   ##companycalendar events also:
   if ($view eq "mcview") {
        tie %appttab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
        SUFIX => '.rec',
        SCHEMA => {
              ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

         # bind todo table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
         SUFIX => '.rec',
         SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

        $prml = setuplist($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, %appttab, %todotab, $events, $imglist, $todomntcnt);
	return $prml;
   }

   ## if it not mcview but only mview continue with this.
   if ($vwtype eq "d") {
      $prml = setDailyPrml($prml, $events, $numevents, $imglist);
   }

   if ($vwtype eq "m") {
      $prml = setMonthlyPrml($prml, $events, $numevents);
   }

   if ($vwtype eq "w") {
      $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);

   }
   return $prml;
}

sub setuplist {
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, %appttab, %todotab, $events, $imglist, $todomntcnt) = @_;

   hddebug "setuplist ()";

   (@records) = sort keys %appttab;
   hddebug "records = $#records";

   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];
      if ($onekey ne "")  {
         if (exists $appttab{$onekey}) {
            $year = $appttab{$onekey}{'year'};
            $month = $appttab{$onekey}{'month'};
            $day = $appttab{$onekey}{'day'};

            # isCurrentYear and isCurrentMonth are relevant checks
            # for all view types.

            if ((isCurrentYear($year, $cyear)) != 1) {
               next;
            }

            if (($vwtype eq "d") || ($vwtype eq "m")) {
               if ((isCurrentMonth($month, $cmonth)) != 1) {
                  next;
               }
            }

            if ($vwtype eq "d") {
               if ((isCurrentDay($day, $cday)) != 1) {
                  next;
               }
            }

            if ($vwtype eq "w") {
               if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                  next;
               }
            }

            $year = $appttab{$onekey}{'year'};
            $month = $appttab{$onekey}{'month'};
            $day = $appttab{$onekey}{'day'};
            $hour = $appttab{$onekey}{'hour'};
            $min = $appttab{$onekey}{'min'};
            $meridian = $appttab{$onekey}{'meridian'};
            $free = $appttab{$onekey}{'free'};

            if (($sc eq "p") && ($appttab{$onekey}{'share'} eq "Showasbusy")) {
                $subject = "Busy";
            } else {
                if ($appttab{$onekey}{'share'} eq "Private") {
                    $subject = "Private";
		} else {
                   $subject = $appttab{$onekey}{'subject'};
	        }
            }

            $dtype = $appttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
               if ($vwtype eq "m") {
                  $eventnum = $day - 1;
               } else {
                  if ($vwtype eq "w") {
                     $eventnum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
                  }
               }
            }

            # append the events for this eventnum.
            $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $appttab{$onekey}{desc}, 1);

            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, 1);
            }
         }
      }
   }


   (@records) = sort keys %todotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {
         $onekey = $records[$g];
         if (!exists($todotab{$onekey})) {
            next;
         }
         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};

         #status ("calday = $cday <BR>");
         #status ("month = $month <BR>");
         #status ("day = $day <BR>");
         # isCurrentYear and isCurrentMonth are relevant checks
         # for all view types.

         if ((isCurrentYear($year, $cyear)) != 1) {
             next;
          }

         if (($vwtype eq "d") || ($vwtype eq "m")) {
            if ((isCurrentMonth($month, $cmonth)) != 1) {
               next;
            }
         }

         if ($vwtype eq "d") {
            if ((isCurrentDay($day, $cday)) != 1) {
                next;
            }
            #status(" day =$day <BR>");
         }

         if ($vwtype eq "w") {
            if ((companycalutil::companycalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};
         $hour = $todotab{$onekey}{'hour'};
         $meridian = $todotab{$onekey}{'meridian'};
         if ($todotab{$onekey}{'share'} eq "Private") {
            $subject = "Private";
         } else {
            $subject = $todotab{$onekey}{'subject'};
	 }
         $priority = $todotab{$onekey}{'priority'};
         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = companycalutil::companycalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum
         $events[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, 1);

         if ($vwtype ne "m") {
            $imglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, 1);
         }
      }
   }

   if ($vwtype eq "d") {
      $prml = setDailyPrml($prml, $events, $numevents, $imglist);
   }

   if ($vwtype eq "m") {
      $prml = setMonthlyPrml($prml, $events, $numevents);
   }

   if ($vwtype eq "w") {
      $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);

   }
   return $prml;

}


sub displayDetails {
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $business) = @_;

   hddebug "companycalutil::displayDetails";

   $onekey = $ceno;
   $prml = strapp $prml, "subdetails=";
   $app_tab = 0;
   $todo_tab = 0;

   if (-d ("$ENV{HDDATA}/business/business/$business/calendar/todotab") ) {
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/todotab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };
     $todo_tab = 1;
   }

   if (-d ("$ENV{HDDATA}/business/business/$business/calendar/appttab") ) {
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/calendar/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
               'hour', 'min', 'meridian', 'dhour', 'dmin',
               'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
              'subject', 'street', 'city', 'state', 'zipcode', 'country',
              'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
      $app_tab = 1;
   }

   if ($todo_tab == 1) {
      if (exists($todotab{$onekey})) {
         ($monthstr = getmonthstr($todotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $todotab{$onekey}{'day'} $todotab{$onekey}{'year'} $todotab{$onekey}{'meridian'} <BR> Priority: $todotab{$onekey}{'priority'} <BR> Status: $todotab{$onekey}{'status'}";
         if ($todotab{$onekey}{'share'} eq "Private") {
            $subject = "Event & To-do Details: Private<BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            return $prml;
         }
         $subject = "Details: $todotab{$onekey}{'subject'}<BR> Description: $todotab{$onekey}{'desc'}<BR>";
         #$subject .= "$todotab{$onekey}{'desc'}";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         #hddebug "subject = $subject";
         $prml = strapp $prml, "subdetails=$subject";
         return $prml;
      }
   }
   if ($app_tab == 1)  {
      #hddebug "came here";
      if (exists($appttab{$onekey})) {
         ($monthstr = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $appttab{$onekey}{'day'} $appttab{$onekey}{'year'} $appttab{$onekey}{'meridian'} <BR> Free/Busy: $appttab{$onekey}{free}<BR>";
         if ($appttab{$onekey}{'share'} eq "Private") {
            $subject = "Details: Private<BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            #hddebug "subject1 = $subject";
            return $prml;
         }
         $subject = "Details: $appttab{$onekey}{'subject'}<BR> Description: $appttab{$onekey}{'desc'}<BR>";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         $prml = strapp $prml, "subdetails=$subject";
         #hddebug "subject1 = $subject";
         return $prml;
      }  
      $subject = "Details: $appttab{$onekey}{'subject'}<BR> Description: $appttab{$onekey}{'desc'}<BR>";
      $subject .= "User: $lg <BR> $subject_d";
      $subject = adjusturl $subject;
      #hddebug "subject = $subject";
      $prml = strapp $prml, "subdetails=$subject";
   }
   return $prml;
}

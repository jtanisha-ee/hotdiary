package calfuncs::businesscalfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use businesscalutil::businesscalutil;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch eventDispatch isCurrentDay isCurrentMonth isCurrentYear  setEventDisplayRec getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink setEventEditRec setDailyPrml deleteEvent addEvent updateEvent setMonthlyPrml setWeeklyPrml createWeeklyImageLink createDailyImageLink displayTodo createTodoLink createTodoWeeklyImageLink createTodoDailyImageLink editTodo updateTodo addTodo deleteTodo todoDispatch setTodoDailyPrml setTodoMonthlyPrml setTodoWeeklyPrml createDtypeImg addCalendarPref publishTodo publishEvent isCalPublic addBusEventToMyCal getmembers getresources getgroups getbusinessdir addMeeting deleteMeeting updateMeeting displayEventsAndTodos displayDetails );

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $business, $teamname) = @_;

   ## pc indicates add this event it to team members personal calendars
   if ($f eq "e") {
      $prml = eventDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc, $teamname);
   }

   if ($f eq "t") {
      $prml = todoDispatch($prml, $vw, $mo, $dy, $yr, $h,$m, $login, $url, $a, $en, $f, $jvw, $business, $sc, $teamname);
   }

   if ($f eq "j") {
      $prml = journalDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc, $teamname);
   }
   return $prml;
}

sub todoDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc, $teamname) = @_;     
   if ($a eq "d") {
      return(displayTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc, $teamname));
   }

   if ($a eq "de") {
      return(editTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $business, $teamname));
   }                                                                           
   return $prml;
}

sub eventDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $business, $sc, $teamname) = @_;

   if ($a eq "d") {
      return(setEventDisplayRec($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc, $teamname));
   }
   if ($a eq "de") {
      return(setEventEditRec($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $jvw, $business, $sc, $teamname));
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

   my($dtype, $en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $subject, $jvw, $business, $login, $teamname, $desc) = @_; 
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

   $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a>");

   if ($subject ne "") {
      $etitle = $subject;
   } else { 
      $etitle = $dtype;
   }

   $hourlen = length($hour);
   if ($hourlen eq "1") {
       $hour = "&nbsp;$hour";
   }

   $addeventtop = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=u\"><IMG SRC=\"$hdnm/images/addevent.gif\" BORDER=\"0\" ALT=\"Add Event To My Personal Calendar\"></a>");

   $burlhref1 = "<CENTER><a href=\"$burl\">$etitle</a> <BR>$desc <BR> $hour $min $meridian <BR> $imgurl $addeventtop </CENTER> $hr";

   $burlhref = adjusturl($burlhref1);
   return $burlhref;

}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype) = @_;

   $dimg = createDtypeImg($dtype);
   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
       $showbusy = "";
   }


   $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a><BR><BR>");

   return $imgurl;
}


sub createWeeklyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype) = @_;

   $dimg = createDtypeImg($dtype);

   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
      $showbusy = "";
   }

   #$imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a><BR><BR>");

   $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a><BR>");

   #$prml = strapp $prml, "imglist$row1=$imgurl";
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

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc, $teamname) = @_;

   if ($sc eq "p") { 
      if ((isCalPublic($business, $teamname)) != 1) {
         return $prml;
      }
   }    

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) || 
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
   }

   # bind personal appt table vars
   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
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

   (@records) = sort keys %busappttab;


   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];                              
      if ($onekey ne "")  {
         if (exists $busappttab{$onekey}) {
	    if ($sc eq "p") {
               if ($busappttab{$onekey}{'share'} eq "Private") {
                   next;
	       }
	    }	
            $year = $busappttab{$onekey}{'year'};
            $month = $busappttab{$onekey}{'month'};
            $day = $busappttab{$onekey}{'day'};

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
	       if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                  next;
               }
            }

            $year = $busappttab{$onekey}{'year'};
            $month = $busappttab{$onekey}{'month'};
            $day = $busappttab{$onekey}{'day'};
            $hour = $busappttab{$onekey}{'hour'};
            $min = $busappttab{$onekey}{'min'};
            $meridian = $busappttab{$onekey}{'meridian'};
            $free = $busappttab{$onekey}{'free'};

            if (($sc eq "p") && ($busappttab{$onekey}{'share'} eq "Showasbusy")) {
                $subject = "Busy";
            } else {
                $subject = $busappttab{$onekey}{'subject'};
	    }

            $dtype = $busappttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
	       if ($vwtype eq "m") {
	          $eventnum = $day - 1;
	       } else {
	          if ($vwtype eq "w") {
	             $eventnum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
                  }
	       }
            } 

	    # append the events for this eventnum.
	    $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $teamname, $busappttab{$onekey}{desc});

            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
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
  
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw, $business, $sc, $teamname) = @_;


   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
   }

   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free', 
	 'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

   $onekey = $ceno;
   if (exists $busappttab{$onekey}) {
      $banner = adjusturl $busappttab{$onekey}{banner};
      $prml = strapp $prml, "year=$busappttab{$onekey}{'year'}";
      ($monthstr = getmonthstr($busappttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $prml = strapp $prml, "meridian=$busappttab{$onekey}{'meridian'}";
      $prml = strapp $prml, "month=$monthstr"; 
      $prml = strapp $prml, "monthnum=$busappttab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$busappttab{$onekey}{'day'}";
      $prml = strapp $prml, "evtbanner=$banner";

      $recurtype = $busappttab{$onekey}{'recurtype'};
      if ($recurtype eq "") {
         $recurtype = "Daily";
      }

      $prml = strapp $prml, "recurtype=$recurtype";
      $prml = strapp $prml, "hour=$busappttab{$onekey}{'hour'}";
      if ($busappttab{$onekey}{'min'} eq "00") {
         $min = 0;
      } else {
         $min = $busappttab{$onekey}{'min'};
      }
      $prml = strapp $prml, "min=$min";
      $prml = strapp $prml, "sec=$busappttab{$onekey}{'sec'}";
      $prml = strapp $prml, "zone=$busappttab{$onekey}{'zone'}";
      $zone = getzonestr($busappttab{$onekey}{'zone'});
      $prml = strapp $prml, "zonestr=$zone";

      $share = $busappttab{$onekey}{'share'};
      if ($share eq "") {
         $share = "Public";
      }
      $prml = strapp $prml, "share=$share";

      $free = $busappttab{$onekey}{'free'};
      if ($free eq "") {
         $free = "Free";
      }
      $prml = strapp $prml, "free=$free";
      $prml = strapp $prml, "atype=$busappttab{$onekey}{'atype'}";
      $prml = strapp $prml, "dtype=$busappttab{$onekey}{'dtype'}";
      if (($busappttab{$onekey}{'share'} eq "Showasbusy") && ($sc eq "p")) {
        $prml = strapp $prml, "subject=BUSY";
        $prml = strapp $prml, "desc=BUSY";
      } else {
        $subject = adjusturl($busappttab{$onekey}{'subject'});
        $prml = strapp $prml, "subject=$subject";
        $desc = adjusturl($busappttab{$onekey}{'desc'});
                     $prml = strapp $prml, "desc=$desc";
                  }
		  $prml = strapp $prml, "dhour=$busappttab{$onekey}{'dhour'}";
                  $dmin = $busappttab{$onekey}{'dmin'};
                  if (($dmin eq "00") || ($dmin eq "")) {
                     $dmin = 0;
                  } 
                  $prml = strapp $prml, "dmin=$dmin";
                  $prml = strapp $prml, "contact=";
	       }
     return $prml;
}
                        
sub deleteEvent {

   my($ceno, $lg, $business, $teamname) = @_;
   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) || 
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) { 
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       return $prml;
   }
 
   #bind teamname appt table vars
   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
   SUFIX => '.rec',
   SCHEMA => {
       ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   if (exists($busappttab{$ceno})) {
      delete $busappttab{$ceno};
      tied(%busappttab)->sync();   
   }
   deleteEventFromPc($business, $teamname, $ceno);
   return $prml;
}

sub addEvent {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact, $teamname, $pc, $banner) = @_; 

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
   }


   tie %busappttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };


   $entryno = getkeys();
   $entryno .= $business;
   $entryno .= $teamname;
   $busappttab{$entryno}{'login'} = trim $lg;
   $busappttab{$entryno}{'month'} = trim $emonth;
   $busappttab{$entryno}{'day'} = trim $eday;
   $busappttab{$entryno}{'year'} = trim $eyear;
   $busappttab{$entryno}{'hour'} = trim $ehour;
   $busappttab{$entryno}{'min'} = trim $emin;
   $busappttab{$entryno}{'meridian'} = trim $emeridian;
   $busappttab{$entryno}{'dhour'} = trim $edhour;
   $busappttab{$entryno}{'dmin'} = trim $edmin;
   $busappttab{$entryno}{'dtype'} = trim $edtype;
   $busappttab{$entryno}{'atype'} = trim $eatype;
   $busappttab{$entryno}{'desc'} = $edesc;
   $busappttab{$entryno}{'zone'} = trim $ezone;
   $busappttab{$entryno}{'recurtype'} = trim $erecurtype;
   $busappttab{$entryno}{'share'} = trim $eshare;
   $busappttab{$entryno}{'free'} = trim $efree;
   $busappttab{$entryno}{'subject'} = trim $etitle;
   $busappttab{$entryno}{'entryno'} = trim $entryno;
   $busappttab{$entryno}{'person'} = trim $lg;
   $busappttab{$entryno}{'banner'} = $banner;
   if ($econtact ne "") {
      $eventdetails .= "Event: $etitle \n";
      $eventdetails .= "Event Type: $edtype \n";
      $eventdetails .= "Date:  $emonth-$eday-$eyear \n";
      $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
      $eventdetails .= "Description: $edesc \n";
      $eventdetails .= "Frequency: $erecurtype \n";
      #$busappttab{$entryno}{'contact'} = trim $econtact;
   }

   ## save event to personal calendars of team members
   if ($pc ne "") {
     saveEventToPc($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact, $teamname, $entryno, $banner); 
   }

   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno);
   }

   tied(%busappttab)->sync();
}

sub saveEventToPc {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact, $teamname, $entryno, $banner) = @_;


   if (!-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab")) {
      return;
   }

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['login']};

   foreach $mem (sort keys %teampeopletab) {
      $mem = trim $mem;
      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';

      if (!-d "$ENV{HDDATA}/$alpha/$mem/appttab") {
	 next;
      }

      # bind personal appointment table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
           'hour', 'min', 'meridian', 'dhour', 'dmin',
           'dtype', 'atype', 'desc', 'zone', 'recurtype',
           'share', 'free', 'subject', 'street', 'city', 'state',
           'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
           'confirm', 'id', 'type'] };

     
      $appttab{$entryno}{'login'} = trim $mem;
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
      $appttab{$entryno}{'person'} = trim $lg;
      $appttab{$entryno}{'banner'} = $banner;
      tied(%appttab)->sync();

      # bind remind index table vars
      tie %remindtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['login'] };
      $remindtab{$login}{login} = $login;
      tied(%remindtab)->sync();
      system "chmod 777 $ENV{HDDATA}/aux/remindtab/$login.rec";
   }
}


sub saveTodoInPc {

   my($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $business, $teamname, $banner, $entryno) = @_; 

   if (!-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab")) {
      return;
   }

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['login']};

   foreach $mem (sort keys %teampeopletab) {
      $mem = trim $mem;
      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';

      if (!-d "$ENV{HDDATA}/$alpha/$mem/todotab") {
         next;
      }

      # bind personal todo table vars
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };

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
      $todotab{$entryno}{'$entryno'} = trim $entryno;
      $todotab{$entryno}{'$banner'} = $banner;
      tied(%appttab)->sync();
   }
}


sub deleteEventFromPc {

   my($business, $teamname, $ceno) = @_;

   if (!-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab")) {
      return;
   }

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['login']};

   foreach $mem (sort keys %teampeopletab) {
      $mem = trim $mem;
      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';
      if (!-d "$ENV{HDDATA}/$alpha/$mem/appttab") {
         next;
      }

      # bind personal appointment table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
           'hour', 'min', 'meridian', 'dhour', 'dmin',
           'dtype', 'atype', 'desc', 'zone', 'recurtype',
           'share', 'free', 'subject', 'street', 'city', 'state',
           'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
           'confirm', 'id', 'type'] };
      if (exists($appttab{$ceno}) ) {
         delete($appttab{$ceno});
         tied(%appttab)->sync();
      }
   }
}

sub deleteTodoFromPc {

   my($business, $teamname, $ceno) = @_;

   if (!-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab")) {
      return;
   }

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['login']};

   foreach $mem (sort keys %teampeopletab) {
      $mem = trim $mem;
      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';
      if (!-d "$ENV{HDDATA}/$alpha/$mem/todotab") {
         next;
      }

      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };

      if (exists($todotab{$ceno}) ) {
         delete($todotab{$ceno});
         tied(%todotab)->sync();
      }
   }
}

sub updateEvent  {

   my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact, $teamname, $pc, $banner) = @_; 

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       return $prml;
   }

   tie %busappttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
                  'hour', 'min', 'meridian', 'dhour', 'dmin',
                  'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share',
		  'free', 'subject',  'street', 'city', 'state', 'zipcode',
	 	  'country', 'venue', 'person', 'phone', 'banner', 
		  'confirm', 'id', 'type'] };


   if (exists $busappttab{$entryno}) {
      $busappttab{$entryno}{'login'} = trim $lg;
      $busappttab{$entryno}{'month'} = trim $emonth;
      $busappttab{$entryno}{'day'} = trim $eday;
      $busappttab{$entryno}{'year'} = trim $eyear;
      $busappttab{$entryno}{'hour'} = trim $ehour;
      $busappttab{$entryno}{'min'} = trim $emin;
      $busappttab{$entryno}{'meridian'} = trim $emeridian;
      $busappttab{$entryno}{'dhour'} = trim $edhour;
      $busappttab{$entryno}{'dmin'} = trim $edmin;
      $busappttab{$entryno}{'dtype'} = trim $edtype;
      $busappttab{$entryno}{'atype'} = trim $eatype;
      $busappttab{$entryno}{'desc'} = $edesc;
      $busappttab{$entryno}{'zone'} = trim $ezone;
      $busappttab{$entryno}{'recurtype'} = trim $erecurtype;
      $busappttab{$entryno}{'share'} = trim $eshare;
      $busappttab{$entryno}{'free'} = trim $efree;
      $busappttab{$entryno}{'subject'} = trim $etitle;
      $busappttab{$entryno}{'entryno'} = trim $entryno;
      $busappttab{$entryno}{'banner'} = $banner;
      if ($econtact ne "") {
         $eventdetails .= "Event: $etitle \n";
         $eventdetails .= "Event Type: $edtype \n";
         $eventdetails .= "Date: $emonth-$eday-$eyear \n";
         $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
         $eventdetails .= "Description: $edesc \n";
         $eventdetails .= "Frequency: $erecurtype \n";
      }

      if ($pc ne "") {
         saveEventToPc($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $business, $econtact, $teamname, $entryno, $banner);
      }
   }                                                                                                  
   tied(%busappttab)->sync();
   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno);
   }
   return $prml;

}

sub displayTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc, $teamname) = @_;

   if ($sc eq "p") {
      if ((isCalPublic($business, $teamname)) != 1) {
         return $prml;
      }
   }
   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
   }

   # bind todo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };

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

   (@records) = sort keys %bustodotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {
         $onekey = $records[$g]; 
         if (!exists($bustodotab{$onekey})) {
            next; 
         }
	 if ($sc eq "p") {
            if ($bustodotab{$onekey}{'share'} eq "Private") {
	       next; 
	    }
	 }
         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};

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
            if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};
         $hour = $bustodotab{$onekey}{'hour'};
         $meridian = $bustodotab{$onekey}{'meridian'};
         $subject = $bustodotab{$onekey}{'subject'};
         $priority = $bustodotab{$onekey}{'priority'};

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum 
         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $bustodotab{$onekey}{desc});

         if ($vwtype ne "m") {
            $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
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

   my($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $subject, $todomntcnt, $priority, $desc) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $todourl = $url;
   $e = "de";

   $todourl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=t&vw=i");

   $hr = "<HR>";

   $todoimgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a>");

   $pri = " Priority ";
   if ($subject ne "") {
     $todotitle = "Todo $subject$pri$priority";
   } else {
     $todotitle = "Todo$pri$priority";
   }

   
   $burlhref1 = "<CENTER><a href=\"$todourl\"><FONT COLOR=03c503>$todotitle</FONT></a> <BR><FONT COLOR=03c503>$desc <BR> $hour $meridian </FONT><BR> $todoimgurl </CENTER> $hr";
   $burlhref = adjusturl($burlhref1);
   #status ("href = $burlhref");
   return $burlhref;

}

sub createTodoWeeklyImageLink {

   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $imgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a><BR><BR>");

   #$prml = strapp $prml, "imglist$row1=$imgurl";
   return $imgurl;

}


sub createTodoDailyImageLink {
   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw ) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $timgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a><BR><BR>");

   return $timgurl;
}


sub editTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $business, $teamname) = @_;


  if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
   }


   # bind todo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };

   $onekey = $ceno;
   if (exists($bustodotab{$onekey})) {
      $prml = strapp $prml, "subject=$bustodotab{$onekey}{'subject'}";
      $prml = strapp $prml, "desc=$bustodotab{$onekey}{'desc'}";
      ($monthstr = getmonthstr($bustodotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $prml = strapp $prml, "month=$monthstr";
      $prml = strapp $prml, "monthnum=$bustodotab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$bustodotab{$onekey}{'day'}";                   
      $prml = strapp $prml, "year=$bustodotab{$onekey}{'year'}";
      $prml = strapp $prml, "meridian=$bustodotab{$onekey}{'meridian'}";
      $prml = strapp $prml, "priority=$bustodotab{$onekey}{'priority'}";
      $prml = strapp $prml, "status=$bustodotab{$onekey}{'status'}";
      $prml = strapp $prml, "share=$bustodotab{$onekey}{'share'}";
      $prml = strapp $prml, "hour=$bustodotab{$onekey}{'hour'}";
      $prml = strapp $prml, "evtbanner=$bustodotab{$onekey}{'banner'}";
   }
   return $prml;


}

sub deleteTodo {
   my($ceno, $lg, $business, $teamname) = @_; 

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       return $prml;
   }

   # bind bustodo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] }; 

   if (exists($bustodotab{$ceno})) {
      delete $bustodotab{$ceno};
      tied(%bustodotab)->sync();   
      deleteTodoFromPc($business,$teamname, $ceno);
   }
   return $prml;
}

sub addTodo {

   my($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $business, $teamname, $pc, $banner) = @_; 
  

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
   }

   # bind todo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
       SUFIX => '.rec',
       SCHEMA => {
            ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
            'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };


   $entryno = getkeys();
   $entryno = "$entryno . $business . $teamname";
   $bustodotab{$entryno}{'login'} = trim $lg;      
   $bustodotab{$entryno}{'subject'} = trim $ttitle;      
   $bustodotab{$entryno}{'desc'} = trim $tdesc; 
        
   $bustodotab{$entryno}{'month'} = trim $tmonth;      
   $bustodotab{$entryno}{'day'} = trim $tday;      
   $bustodotab{$entryno}{'year'} = trim $tyear;      
   $bustodotab{$entryno}{'hour'} = trim $thour;      
   $bustodotab{$entryno}{'meridian'} = trim $tmeridian;      
   $bustodotab{$entryno}{'share'} = trim $tshare;      
   $bustodotab{$entryno}{'entryno'} = trim $entryno;      
   $bustodotab{$entryno}{'hour'} = trim $thour;      
   $bustodotab{$entryno}{'priority'} = trim $tpriority;      
   $bustodotab{$entryno}{'status'} = trim $tstatus;      
   $bustodotab{$entryno}{'$entryno'} = trim $entryno;      
   $bustodotab{$entryno}{'$banner'} = $banner;      

   if ($pc ne "") {
      saveTodoInPc($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $business, $teamname,$banner, $entryno); 
   } 

   tied(%bustodotab)->sync(); 
   return $prml;
}

sub updateTodo {
    my($entryno, $etitle,  $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $lg, $business, $teamname, $pc, $banner) = @_; 


    if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       return $prml;
    }

    # bind todo table vars
    tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };

    if (exists($bustodotab{$entryno})) {
       $bustodotab{$entryno}{'login'} = trim $lg;
       $bustodotab{$entryno}{'subject'} = trim $etitle;
       $bustodotab{$entryno}{'desc'} = trim $edesc;

       $bustodotab{$entryno}{'month'} = trim $emonth;
       $bustodotab{$entryno}{'day'} = trim $eday;
       $bustodotab{$entryno}{'year'} = trim $eyear;
       $bustodotab{$entryno}{'hour'} = trim $ehour;
       $bustodotab{$entryno}{'meridian'} = trim $emeridian;
       $bustodotab{$entryno}{'share'} = trim $eshare;
       $bustodotab{$entryno}{'priority'} = trim $epriority;
       $bustodotab{$entryno}{'status'} = trim $estatus;
       $bustodotab{$entryno}{'entryno'} = trim $entryno;
       $bustodotab{$entryno}{'banner'} = trim $banner;
       tied(%bustodotab)->sync();
       if ($pc ne "") {
          saveTodoInPc($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $business, $teamname,$banner, $entryno); 
       }
   }
}


sub publishEvent {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $business, $teamname) = @_;

   if ((isCalPublic($business, $teamname)) != 1) {
      return $prml;
   };


   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
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

   #if (exists($busappttab{$lg} )) {
      (@records) = sort keys %busappttab;
      if ($#records >= 0) {
         for ($g = 0; $g <= $#records; $g = $g+1) {
            $onekey = $records[$g];
            if (exists($busappttab{$onekey})) {
               if ($busappttab{$onekey}{'share'} eq "Private") {
                  $month = $busappttab{$onekey}{'month'};
                  $day=$busappttab{$onekey}{'day'};
                  $year=$busappttab{$onekey}{'year'};

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
                    if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                       next;
                    }
                 }

                 $year = $busappttab{$onekey}{'year'};
                 $month = $busappttab{$onekey}{'month'};
                 $day = $busappttab{$onekey}{'day'};
                 $hour = $busappttab{$onekey}{'hour'};
                 $min = $busappttab{$onekey}{'min'};
                 $meridian = $busappttab{$onekey}{'meridian'};
                 $free = $busappttab{$onekey}{'free'};
                 $subject = $busappttab{$onekey}{'subject'};
                 $dtype = $busappttab{$onekey}{'dtype'};

                 if ($vwtype eq "d") {
                    $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
                 } else {
                    if ($vwtype eq "m") {
                       $eventnum = $day - 1;
                    } else {
                       if ($vwtype eq "w") {
                          $eventnum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
                       }
                    }
                 }

                 # append the events for this eventnum.
                 $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $teamname, $busappttab{$onekey}{desc});

                  if ($vwtype ne "m") {
                     $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
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

   my($prml, $vwtype, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $a, $en, $f, $sc, $business, $teamname) = @_;

   if ((isCalPublic($business, $teamname)) != 1) {
       return $prml;
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
   }


   # bind todo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };


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

   (@records) = sort keys %$bustodotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {

         $onekey = $records[$g];
         if (!exists($bustodotab{$onekey})) {  
            next; 
         }

         if ($bustodotab{$onekey}{'share'} eq "Private") { 
	    next;
         }

         #status ("entryno = $onekey <BR>");
         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};

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
            if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};
         $hour = $bustodotab{$onekey}{'hour'};
         $meridian = $bustodotab{$onekey}{'meridian'};
         $subject = $bustodotab{$onekey}{'subject'};
         $priority = $bustodotab{$onekey}{'priority'};

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum

         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $bustodotab{$onekey}{desc});

         if ($vwtype ne "m") {
            $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
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

   my($business, $teamname) = @_;

   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc', 'password',
                'cpublish' ] };               

   if (($teamtab{$teamname}{'calpublish'}) eq "CHECKED") {
       return 1;
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
       $emsg = "Dear $oldlogin, \n \n";
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

     ### DONOT SEND INVITATION LETTER ######
       #qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
       #qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};

       if ($eemail ne "1") {
          $alpha = substr $login, 0, 1;
          $alpha = $alpha . '-index';
          system "mkdir -p $ENV{HDREP}/$alpha/$login";
          system "chmod 755 $ENV{HDREP}/$alpha/$login";
          system "mkdir -p $ENV{HDHOME}/rep/$alpha/$login";
          system "mkdir -p $ENV{HDDATA}/$alpha/$login";
          system "chmod 755 $ENV{HDDATA}/$alpha/$login";
          system "touch $ENV{HDDATA}/$alpha/$login/addrentrytab";
          system "chmod 755 $ENV{HDDATA}/$alpha/$login/addrentrytab";
          system "mkdir -p $ENV{HDDATA}/$alpha/$login/addrtab";
          system "chmod 755 $ENV{HDDATA}/$alpha/$login/addrtab";
          system "touch $ENV{HDDATA}/$alpha/$login/apptentrytab";
          system "chmod 660 $ENV{HDDATA}/$alpha/$login/apptentrytab";
          system "mkdir -p $ENV{HDDATA}/$alpha/$login/appttab";
          system "chmod 770 $ENV{HDDATA}/$alpha/$login/appttab";
          system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";
          system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
          system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
          system "chmod -R 770 $ENV{HDDATA}/groups/$alpha/$login";
          system "cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alpha/$login/index.html";
          system "cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alpha/$login";
          system "chmod 775 $ENV{HDDATA}/$alpha/$login/calendar_events.txt";

          system "mkdir -p $ENV{HDDATA}/$alpha/$login/faxtab";
          system "chmod 755 $ENV{HDDATA}/$alpha/$login/faxtab";

          system "mkdir -p $ENV{HDDATA}/$alpha/$login/faxdeptab";
          system "chmod 755 $ENV{HDDATA}/$alpha/$login/faxdeptab";
     } 

      if ( (($eemail eq "1") && ($logtab{$login}{checkid} eq "CHECKED") ) || ($eemail ne "1") ) {
         $malpha = substr $mname, 0, 1;
         $malpha = $malpha . '-index';
         system "/bin/cp $ENV{HDDATA}/$malpha/$mname/appttab/$entryno.rec $ENV{HDDATA}/$alpha/$login/appttab/$entryno.rec";
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
         $tfile = "$ENV{HDDATA}/$alpha/$login/apptentrytab";
         open thandle, ">>$tfile";
         printf thandle "%s\n", $entryno;
         close thandle;

         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$login/appttab",
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

   my($busen, $login, $business, $teamname) = @_;

   hddebug("addbuseventtomycal busen = $busen, business = $business, teamname= $teamname, login = $login");

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       return $prml;
   }

   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['entryno', 'login', 'month', 'day', 'year',        
                'hour', 'min', 'meridian', 'dhour', 'dmin',
                'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 
	        'free', 'subject', 'street', 'city', 'state', 'zipcode', 
		'country', 'venue', 'person', 'phone', 'banner', 
		'confirm', 'id', 'type'] };

   if (!exists $busappttab{$busen}) { 
       return 0;
   }

   # bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alpha/$login/appttab",
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
   $appttab{$entryno}{'month'} = $busappttab{$busen}{month};
   $appttab{$entryno}{'day'} = $busappttab{$busen}{day};   
   $appttab{$entryno}{'year'} = $busappttab{$busen}{year};   
   $appttab{$entryno}{'hour'} = $busappttab{$busen}{hour};   
   $appttab{$entryno}{'min'} = $busappttab{$busen}{min};   
   $appttab{$entryno}{'meridian'} = $busappttab{$busen}{meridian};   
   $appttab{$entryno}{'dhour'} = $busappttab{$busen}{dhour};   
   $appttab{$entryno}{'dmin'} = $busappttab{$busen}{dmin};   
   $appttab{$entryno}{'dtype'} = $busappttab{$busen}{dtype};   
   $appttab{$entryno}{'atype'} = $busappttab{$busen}{atype};   
   $appttab{$entryno}{'desc'} = $busappttab{$busen}{desc};   
   $appttab{$entryno}{'zone'} = $busappttab{$busen}{zone};  
   $appttab{$entryno}{'recurtype'} = $busappttab{$busen}{recurtype};   
   $appttab{$entryno}{'share'} = $busappttab{$busen}{share};   
   $appttab{$entryno}{'free'} = $busappttab{$busen}{free};   
   $appttab{$entryno}{'subject'} = $busappttab{$busen}{subject};   
   $appttab{$entryno}{'entryno'} = $entryno;
   
   #add the entry in the apptentrytab
   $tfile = "$ENV{HDDATA}/$alpha/$login/apptentrytab";
   open thandle, ">>$tfile";
   printf thandle "%s\n", $entryno;
   close thandle;

   tied(%appttab)->sync();              
   return 1;
}

sub getmembers {

   my($login) = @_;
   hddebug "getmembers";

   $members = "";
   $space = " ";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';
   
   if (-d ("$ENV{HDDATA}/$alpha/$login/addrtab")) {
      # bind address table vars
      tie %addrtab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/$alpha/$login/addrtab",
        SUFIX => '.rec',
        SCHEMA => {
           ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
           'city', 'state', 'zipcode', 'country', 'phone', 'pager',
           'pagertype', 'fax', 'cphone', 'bphone','email', 'url', 'id',
           'other', 'aptno', 'busname', 'bday', 'bmonth', 'byear'] };

      foreach $contact (sort keys %addrtab) {
         if ($addrtab{$contact}{id} ne "") {
            $id = $addrtab{$contact}{id}; 
	    
            if ($logtab{$id}{checkid} eq "CHECKED") {
               $addr = trim "\L$id-\L$logtab{$id}{fname}-$logtab{$id}{lname}-$logtab{$id}{email}";
               $members .= "\<OPTION\>$addr<\/OPTION\>";
	    }
         }
      }
   }
   return $members;
}

sub getresources {

   my($login, $busname) = @_;

   hddebug "getresources";

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

   foreach $busname (sort keys %businesstab) {
      $busname = trim $busname;
      if (-d("$ENV{HDDATA}/business/business/$busname/peopletab")) {
         tie %peopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$busname/peopletab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'business']};

	 if (exists($peopletab{$login})) {
            if (-d("$ENV{HDDATA}/business/business/$busname/restab")) {
               tie %restab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/business/business/$busname/restab",
               SUFIX => '.rec',
               SCHEMA => {
                  ORDER =>  ['type', 'name', 'bldg', 'zipcode',
                                'country', 'tz'] };

               foreach $res (sort keys %restab) {
                  if (exists($restab{$res})) {
	             $res = trim $res;
                     $resources .= "\<OPTION\>$busname:$res\<\/OPTION\>"
                  }
	       }
            }
         }
      }
   }
   return ($resources);
}

sub getgroups {
   my($login) = @_;

   hddebug "getgroups login =$login";
   $groups = "";

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if (-d("$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
     # bind subscribed group table vars
     tie %sgrouptab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
         'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

     foreach $group (sort keys %sgrouptab) {
        if (exists($sgrouptab{$group})) {
	   $group = trim $group;
           $groups .= "\<OPTION\>$group\<\/OPTION\>";
        }
     }
   }

   if (-d("$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
      # bind founded group table vars
      tie %fgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

      foreach $group (sort keys %fgrouptab) {
         if (exists($fgrouptab{$group})) {
	    $group = trim $group;
            $groups .= "\<OPTION\>$group\<\/OPTION\>";
         }
      }
   }
   return $groups;
}

sub getteams {

   my($login, $busname) = @_;
   hddebug "getteams";
   $teams = "";

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

   foreach $busname (sort keys %businesstab) {
      $busname = trim $busname;
      if (-d("$ENV{HDDATA}/business/business/$busname/peopletab")) {
         tie %peopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$busname/peopletab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['business']};
         if (exists($peopletab{$login})) {
            if (!-d("$ENV{HDDATA}/business/business/$busname/teams/teamtab")) {
                $teams .= "\<OPTION\>$busname:NoTeams\<\/OPTION\>";
	    } 
            if (-d("$ENV{HDDATA}/business/business/$busname/teams/teamtab")) {
	       #hddebug "busname = $busname";
               # bind teamtab table vars
               tie %teamtab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/business/business/$busname/teams/teamtab",
               SUFIX => '.rec',
               SCHEMA => {
                  ORDER => ['teamname', 'teamtitle', 'teamdesc',
                        'password', 'cpublish' ] };
	       (@numteams) = (sort keys %teamtab);

	       if ($#numteams < 0) {
	           $teams .= "\<OPTION\>$busname:NoTeams\<\/OPTION\>";
	       } else {
	           $teams .= "\<OPTION\>$busname:AllTeams\<\/OPTION\>";
	       }

	       #hddebug "numteams = $#numteams";
               foreach $team (sort keys %teamtab) {
                  if (exists($teamtab{$team})) {
	             $team = trim $team;
                     $teams .= "\<OPTION\>$busname:$team\<\/OPTION\>";
                  }
               }
            } 
         }
      }
   }
   return ($teams);
}


sub getbusinessdir {

   my($business, $login) = @_;
   hddebug "getbusinessdir()";

   tie %peopletab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['business']};

   if (!exists($peopletab{$login})) {
      return "";
   }

   $members = "";
   $not_exists = 0;
   if (-d("$ENV{HDDATA}/business/business/$business/directory/emptab")) {
      # bind emptab table vars
      tie %emptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/directory/emptab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['login', 'fname', 'lname', 'street',
           'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
           'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
           'aptno', 'busname', 'bday', 'bmonth', 'byear'] };
   } else {
      $not_exists = 1;
   }

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner',
	 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   foreach $mem (sort keys %peopletab) {
      #hddebug "mem = $mem";
      if (exists($logtab{$mem}) ) {
         $logmem = "\<OPTION\>$business-$mem-$logtab{$mem}{'fname'}-$logtab{$mem}{'lname'}-$logtab{$mem}{email}\<\/OPTION\>";
      }
      if ($not_exists == 0) {
         if (exists $emptab{$mem}) {
 	    $logmem = "\<OPTION\>$business-$mem-$emptab{$mem}{'fname'}-$emptab{$mem}{'lname'}-$logtab{$mem}{email}\<\/OPTION\>";
         } 
      }
      $members .= $logmem;
   }

   #hddebug "getbusinessdir() members = $members";
   return ($members);
}



                        
sub deleteMeeting {

   #my($ceno, $lg) = @_;
   my($ceno, $lg, $group) = @_;

   if ($group ne "") {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

       -d "$ENV{HDDATA}/listed/groups/$group/appttab or return $prml";
      delete $appttab{$ceno};
      tied(%appttab)->sync();
      return $prml;
   }
                                   

   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';

   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

  
   $tfile = "$ENV{HDDATA}/$alpha/$lg/apptentrytab";
   (-e "$ENV{HDDATA}/$alpha/$lg/appttab" and -d "$ENV{HDDATA}/$alpha/$lg/appttab") or return $prml;

   #print "ceno = $ceno \n";
   open thandle, "+<$tfile";

   
   $b = 0;
   while (<thandle>) {
      chop;
      $onekey = $_;
      if ($onekey ne "")  {
         if ($onekey ne $ceno) {
            $num_array[$b] = $onekey;
            $b = $b + 1;
	    #print "onekey = $onekey \n";
         }
      }
   }
   close thandle;

   # intialize the file
   system "/bin/echo >$ENV{HDDATA}/$alpha/$lg/apptentrytab";

   $tfile = "$ENV{HDDATA}/$alpha/$lg/apptentrytab";
   open thandle, "+<$tfile";

   for ($c = 0; $c < $b; $c = $c + 1)  {
      $get_entryno = $num_array[$c];
      printf thandle "%s\n", $get_entryno;
   }
   close thandle;
   delete $appttab{$ceno};
   tied(%appttab)->sync();   
   return $prml;
}

sub addMeeting {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $banner) = @_; 

#hddebug "econtact in addevent = $econtact";
   if ($group ne "") {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id'. 'type'] };

       -d "$ENV{HDDATA}/listed/groups/$group/appttab or return $prml";
   }                                        
   else {
     # bind personal appt table vars
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/appttab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   }

   $entryno = getkeys();
   #hddebug "group = $group \n";
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
   $appttab{$entryno}{'banner'} = trim $banner;
   if ($econtact ne "") {
      $eventdetails .= "Event: $etitle \n";
      $eventdetails .= "Event Type: $edtype \n";
      $eventdetails .= "Date:  $emonth-$eday-$eyear \n";
      $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
      $eventdetails .= "Description: $edesc \n";
      $eventdetails .= "Frequency: $erecurtype \n";
      #hddebug("addEvent, eventdetails  $eventdetails");
      #$appttab{$entryno}{'contact'} = trim $econtact;
   }

   if ($group eq "") { 
     #add the entry in the apptentrytab
     $tfile = "$ENV{HDDATA}/$alpha/$lg/apptentrytab";
     open thandle, ">>$tfile";
     printf thandle "%s\n", $entryno;
     close thandle;                                    
   }
   
   tied(%appttab)->sync();
   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
   return $prml;
}

sub updateMeeting  {

   my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $banner) = @_; 

   if ($group ne "") {
      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

       -d "$ENV{HDDATA}/listed/groups/$group/appttab or return $prml";
  } else {
     # bind personal appt table vars
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/appttab",
     SUFIX => '.rec',
     SCHEMA => {
          ORDER => ['entryno', 'login', 'month', 'day', 'year',
          'hour', 'min', 'meridian', 'dhour', 'dmin',
          'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
          'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   }


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
      $appttab{$entryno}{'banner'} = trim $banner;
      if ($econtact ne "") {
         $eventdetails .= "Event: $etitle \n";
         $eventdetails .= "Event Type: $edtype \n";
         $eventdetails .= "Date: $emonth-$eday-$eyear \n";
         $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
         $eventdetails .= "Description: $edesc \n";
         $eventdetails .= "Frequency: $erecurtype \n";
         #hddebug("updateMeeting, eventdetails = $eventdetails");
         #$appttab{$entryno}{'contact'} = trim $econtact;
      }
   }                                                                                                  
   tied(%appttab)->sync();
   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
   return $prml;

}


sub displayEventsAndTodos {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $business, $sc, $teamname) = @_;

   hddebug "displayEventsAndTodos";

   if ($sc eq "p") {
      if ((isCalPublic($business, $teamname)) != 1) {
         return $prml;
      }
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
  }

   # bind personal appt table vars
   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
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

   (@records) = sort keys %busappttab;


   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];
      if ($onekey ne "")  {
         if (exists $busappttab{$onekey}) {
            $year = $busappttab{$onekey}{'year'};
            $month = $busappttab{$onekey}{'month'};
            $day = $busappttab{$onekey}{'day'};

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
               if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                  next;
               }
            }

            $year = $busappttab{$onekey}{'year'};
            $month = $busappttab{$onekey}{'month'};
            $day = $busappttab{$onekey}{'day'};
            $hour = $busappttab{$onekey}{'hour'};
            $min = $busappttab{$onekey}{'min'};
            $meridian = $busappttab{$onekey}{'meridian'};
            $free = $busappttab{$onekey}{'free'};

            if (($sc eq "p") && ($busappttab{$onekey}{'share'} eq "Showasbusy")) {
                $subject = "Busy";
            } else {
                if ($busappttab{$onekey}{'share'} eq "Private") {
                    $subject = "Private";
		} else {
                   $subject = $busappttab{$onekey}{'subject'};
	        }
            }

            $dtype = $busappttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
               if ($vwtype eq "m") {
                  $eventnum = $day - 1;
               } else {
                  if ($vwtype eq "w") {
                     $eventnum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
                  }
               }
            }

	    #hddebug "eventnum = $eventnum";
            # append the events for this eventnum.
            $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $teamname, $busappttab{$onekey}{desc});

            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
            }
         }
      }
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab";
   }

   # bind todo table vars
   tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };


   $todomntcnt = 0;
   (@records) = sort keys %bustodotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {
         $onekey = $records[$g];
         if (!exists($bustodotab{$onekey})) {
            next;
         }
         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};

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
            if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
                next;
            }
         }

         $year = $bustodotab{$onekey}{'year'};
         $month = $bustodotab{$onekey}{'month'};
         $day = $bustodotab{$onekey}{'day'};
         $hour = $bustodotab{$onekey}{'hour'};
         $meridian = $bustodotab{$onekey}{'meridian'};
         if ($bustodotab{$onekey}{'share'} eq "Private") {
            $subject = "Private";
         } else {
            $subject = $bustodotab{$onekey}{'subject'};
	 }
         $priority = $bustodotab{$onekey}{'priority'};
         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum
         $events[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $bustodotab{$onekey}{desc});

         if ($vwtype ne "m") {
            $imglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
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
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $business, $teamname) = @_;

   hddebug "displaydetails";
   $onekey = $ceno;
   $prml = strapp $prml, "subdetails=";
   $app_tab = 0;
   $todo_tab = 0;

   if (-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab") ) {
      tie %bustodotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/bustodotab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour', 'banner'] };
     $todo_tab = 1;
   }

   if (-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab") ) {
      tie %busappttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab",
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
      if (exists($bustodotab{$onekey})) {
         ($monthstr = getmonthstr($bustodotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $bustodotab{$onekey}{'day'} $bustodotab{$onekey}{'year'} $bustodotab{$onekey}{'meridian'} <BR> Priority: $bustodotab{$onekey}{'priority'} <BR> Status: $bustodotab{$onekey}{'status'}";
	 $banner = adjusturl $bustodotab{$onekey}{banner};
         if ($bustodotab{$onekey}{'share'} eq "Private") {
            $subject = "Event & To-do Details: Private<BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            $prml = strapp $prml, "evtbanner=$banner";
            return $prml;
         }
         $subject = "Details: $bustodotab{$onekey}{'subject'}<BR> Description: $bustodotab{$onekey}{'desc'}<BR>";
         #$subject .= "$bustodotab{$onekey}{'desc'}";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         #hddebug "subject = $subject";
         $prml = strapp $prml, "subdetails=$subject";
         $prml = strapp $prml, "evtbanner=$banner";
         return $prml;
      }
   }
   if ($app_tab == 1)  {
      #hddebug "came here";
      if (exists($busappttab{$onekey})) {
         ($monthstr = getmonthstr($busappttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $busappttab{$onekey}{'day'} $busappttab{$onekey}{'year'} $busappttab{$onekey}{'meridian'} <BR> Free/Busy: $busappttab{$onekey}{free}<BR>";
         $banner = adjusturl $busappttab{$onekey}{banner};
         if ($busappttab{$onekey}{'share'} eq "Private") {
            $subject = "Details: Private<BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            $prml = strapp $prml, "evtbanner=$banner";
            #hddebug "subject1 = $subject";
            return $prml;
         }
         $subject = "Details: $busappttab{$onekey}{'subject'}<BR> Description: $busappttab{$onekey}{'desc'}<BR>";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         $prml = strapp $prml, "subdetails=$subject";
         $prml = strapp $prml, "evtbanner=$banner";
         #hddebug "subject1 = $subject";
         return $prml;
      }  
      $subject = "Details: $busappttab{$onekey}{'subject'}<BR> Description: $busappttab{$onekey}{'desc'}<BR>";
      $subject .= "User: $lg <BR> $subject_d";
      $subject = adjusturl $subject;
      #hddebug "subject = $subject";
      $prml = strapp $prml, "subdetails=$subject";
      $prml = strapp $prml, "evtbanner=$banner";
      return $prml;
   }
}

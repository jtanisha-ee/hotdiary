package calfuncs::mergedviewfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use businesscalutil::teammergedcalutil;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch isCurrentDay isCurrentMonth isCurrentYear  setEventDisplayRec getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink setEventEditRec setDailyPrml setMonthlyPrml setWeeklyPrml createDailyImageLink displayTodo createTodoLink createTodoDailyImageLink setTodoDailyPrml setTodoMonthlyPrml setTodoWeeklyPrml createDtypeImg publishTodo publishEvent isCalPublic, addBusEventToMyCal, displayDetails);

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $business, $teamname) = @_;


   $prml = setEventDisplayRec($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $business, $sc, $teamname);
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

   my($dtype, $en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $subject, $jvw, $business, $login, $teamname, $mem, $desc) = @_; 
   $burl = $url; 
   $e = "de";

   $burl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=$f&vw=i&jvw=$jvw");

   $hr = "<HR>";

   $hdnm = $ENV{HDDOMAIN};

   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
      $showbusy = "";
   }
   $dimg = createDtypeImg($dtype);

   #$imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a>");

   $imgurl = adjusturl ("$dimg $showbusy");

   if ($subject ne "") {
      $etitle = "$mem $subject";
   } else { 
      $etitle = "$mem $dtype";
   }

   $hourlen = length($hour);
   if ($hourlen eq "1") {
       $hour = "&nbsp;$hour";
   }

   $burlhref1 = "<CENTER><a href=\"$burl\">$etitle</a><BR>$desc<BR>$hour $min $meridian <BR> $imgurl </CENTER>$hr";
   $burlhref = adjusturl($burlhref1);
   return $burlhref;
}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype) = @_;

   $dimg = createDtypeImg($dtype);
   #$noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");
 
   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
       $showbusy = "";
   }


   #$imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete Event\"></a><BR><BR>");
   $imgurl = adjusturl ("$dimg $showbusy");

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

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) || 
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab";
   }


   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']};

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

   (@hshpeople) = (sort keys %teampeopletab);
   
   #hddebug "mem = $#hshpeople";
    
   foreach $mem (sort keys %teampeopletab) {
      #hddebug "mem = $mem";
      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';

      # bind personal appt table vars
      if (!-d("$ENV{HDDATA}/$alpha/$mem/appttab")) {
	 next;
      }
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
           'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
 
      (@records) = sort keys %appttab;

      for ($y = 0; $y <= $#records; $y = $y+1) {
         $onekey = $records[$y];                              
         if ($onekey ne "")  {
            if (exists $appttab{$onekey}) {
	       #if ($sc eq "p") {
               #   if ($appttab{$onekey}{'share'} eq "Private") {
               #       next;
	       #   }
	       #}	
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
	          if ((businesscalutil::businesscalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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

               if ($appttab{$onekey}{'share'} eq "Private") {
                   $subject = "Private";
	       }

               $dtype = $appttab{$onekey}{'dtype'};
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
	       $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $business, $lg, $teamname, $mem, $appttab{$onekey}{desc});

               if ($vwtype ne "m") {
                   $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
               }
            }
         }    
      }
   }


   $todomntcnt = 0;

   foreach $mem (sort keys %teampeopletab) {
      #hddebug "mem in teampeopletab = $mem";
      if ($mem eq "") {
         next;
      }
      if (!-d("$ENV{HDDATA}/$alpha/$mem/todotab")) {
         next;
      }
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };

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
                     $todonum = businesscalutil::businesscalutil::getWeekDayIndex($day, $month, $year);
                  }
               }
            }

            # append the todos for this todonum
            $events[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $mem, $todotab{$onekey}{desc});
	    
            if ($vwtype ne "m") {
               $imglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
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
         $prml = strapp $prml, "imglist$s=$timglist[$s]";
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
         $prml = strapp $prml, "imglist$u=$timglist[$v]";
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
         'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type' ] };

   $onekey = $ceno;
   if (exists $busappttab{$onekey}) {
      $prml = strapp $prml, "year=$busappttab{$onekey}{'year'}";
      ($monthstr = getmonthstr($busappttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $prml = strapp $prml, "meridian=$busappttab{$onekey}{'meridian'}";
      $prml = strapp $prml, "month=$monthstr"; 
      $prml = strapp $prml, "monthnum=$busappttab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$busappttab{$onekey}{'day'}";

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

sub createTodoLink {

   my($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $subject, $todomntcnt, $priority, $jvw, $mem, $desc) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $todourl = $url;
   $e = "de";

   $todourl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=$f&vw=i");
   $hr = "<HR>";

   #$todoimgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a>");

   if (($vw eq "w") || ($vw eq "d")) {
      $todobr = "<BR>";
   } else {
     $todobr = "";
   }

   $pri = " Priority ";
   if ($subject ne "") {
      $todotitle = "$mem Todo $subject $pri$priority";
   } else {
      $todotitle = "$mem Todo $pri$priority";
   }

   #$noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");
   
   $burlhref1 = "<CENTER><FONT COLOR=03c503><a href=\"$todourl\"><FONT COLOR=03c503>$todotitle</FONT></a>$desc $hour $meridian </FONT> <BR> $todobr $todoimgurl </CENTER>$hr";
   $burlhref = adjusturl($burlhref1);
   return $burlhref;
}

sub createTodoDailyImageLink {
   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw ) = @_;

   $hdnm = $ENV{HDDOMAIN};
   #$noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");

   #$timgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"Delete\"></a><BR><BR>");

   return $url;
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
      (@records) = sort keys %appttab;
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

         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $mem, $bustodotab{$onekey}{desc});

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


sub addBusEventToMyCal {

   my($busen, $login, $business, $teamname) = @_;

   #hddebug("addbuseventtomycal busen = $busen, business = $business, teamname= $teamname, login = $login");

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
    		  'free', 'subject', 'street', 'city', 'state', 'country',
                  'venue', 'person', 'phone', 'banner', 'confirm', 'id',
                  'type'] };

   if (!exists $busappttab{$busen}) { 
       return 0;
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   # bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'street', 'city', 'state',
        'zipcode', 'country', 'venue', 'person', 'phone',
        'banner', 'confirm', 'id', 'type'] };                    

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
   $tfile = "$ENV{HDDATA}/$alphaindex/$login/apptentrytab";
   open thandle, ">>$tfile";
   printf thandle "%s\n", $entryno;
   close thandle;

   tied(%appttab)->sync();              
   return 1;
}


sub displayDetails {
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $business, $teamname) = @_;

   #hddebug "displayDetails";

   $onekey = $ceno;
 
   if (!-d ("$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab" )) {
      $prml = strapp $prml, "subdetails=No Details are available";
      return $prml;
   }
   $prml = strapp $prml, "subdetails=";

   # bind manager table vars
   tie %teampeopletab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$teamname/teampeopletab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']};
 
   foreach $mem (sort keys %teampeopletab) {

      $app_tab = 0;
      $todo_tab = 0;

      $alpha = substr $mem, 0, 1;
      $alpha = $alpha . '-index';

      # bind todo table vars
      if (-d ("$ENV{HDDATA}/$alpha/$mem/todotab") ) {
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/todotab",
         SUFIX => '.rec',
         SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour'] };
	  $todo_tab = 1;
      } 

      if (-d ("$ENV{HDDATA}/$alpha/$mem/appttab") ) {
         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$mem/appttab",
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
            $subject .= "User: $mem <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
 	    return $prml;
         }
         $subject = "Details: $todotab{$onekey}{'subject'}<BR> Description: $todotab{$onekey}{'desc'}<BR>";
         #$subject .= "$todotab{$onekey}{'desc'}";
         $subject .= "User: $mem <BR> $subject_d";
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
               $subject .= "User: $mem <BR> $subject_d";
               $subject = adjusturl $subject;
               $prml = strapp $prml, "subdetails=$subject";
               #hddebug "subject1 = $subject";
               return $prml;
            }
            $subject = "Details: $appttab{$onekey}{'subject'}<BR> Description: $appttab{$onekey}{'desc'}<BR>";
            $subject .= "User: $mem <BR> $subject_d";
            $subject = adjusturl $subject;
            #hddebug "subject = $subject";
            $prml = strapp $prml, "subdetails=$subject";
            return $prml;
	 }
      } 

   }   
}

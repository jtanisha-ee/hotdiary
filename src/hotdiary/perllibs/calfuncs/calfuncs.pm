package calfuncs::calfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use calutil::calutil;
use calfuncs::bizfuncs;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch eventDispatch isCurrentDay isCurrentMonth isCurrentYear  setEventDisplayRec getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink setEventEditRec setDailyPrml deleteEvent addEvent updateEvent setMonthlyPrml setWeeklyPrml createWeeklyImageLink createDailyImageLink displayTodo createTodoLink createTodoWeeklyImageLink createTodoDailyImageLink editTodo updateTodo addTodo deleteTodo todoDispatch setTodoDailyPrml setTodoMonthlyPrml setTodoWeeklyPrml createDtypeImg addCalendarPref publishTodo publishEvent isCalPublic addGroupEventToMyCal displayEventsAndTodos displayDetails getinvitedpeople deleteAllCal getaddresses sendEventInvitations getEmailContacts);

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $group) = @_;

   #hddebug "dispatch, sc = $sc";

   ##publishEvent() applies only for personal calendar.
   ## publishing for groups is handled by setEventDisplayRec()
   if ($f eq "e") {
      if ($sc eq "p") {
         if ($a eq "d") {
	    if ($group eq "") {
                return(publishEvent($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $sc, $group));  
	    }
         } 
      }
      $prml = eventDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $group, $sc);
   }

   if ($f eq "t") {
      if ($sc eq "p") {
         if ($a eq "d") {
           $prml = return(publishTodo($prml, $vw, $mo, $dy, $yr, $h,$m, $login, $url, $a, $en, $f, $sc, $group));
         } 
      }
      #   if ($a eq "de") {
      #      return (editTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $group));
      #   }
      $prml = todoDispatch($prml, $vw, $mo, $dy, $yr, $h,$m, $login, $url, $a, $en, $f, $jvw, $group, $sc);
   }

   if ($f eq "j") {
      $prml = journalDispatch($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $group, $sc);
   }
   
   return $prml;
}

sub todoDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $group, $sc) = @_;     
   if ($a eq "d") {
      return(displayTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $group, $sc ));
   }

   if ($a eq "de") {
      return(editTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $group));
   }                                                                           
   return $prml;
}

sub eventDispatch {

   my($prml, $vw, $mo, $dy, $yr, $h, $m, $login, $url, $a, $en, $f, $jvw, $group, $sc) = @_;

   if ($a eq "d") {
      return(setEventDisplayRec($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $group, $sc ));
   }
   if ($a eq "de") {
      return(setEventEditRec($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $jvw, $group, $sc));
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

   my($dtype, $en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $subject, $jvw, $group, $login, $desc, $sc) = @_;

   #hddebug "createSubjectLink ";
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
   if ($sc eq "p") {
      $imgurl = "";
   } else {
      $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"delete\"></a>");
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

   #bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed' ] };
   # bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

    #hddebug("group = $group");
   if ( ($group ne "") && (exists $lgrouptab{$group}) && ($lgrouptab{$group}{ctype} eq "Community") ) {
      #hddebug("came here");
      if ($login eq "") {
         $addeventtop = "";
      } else {
         $addeventtop = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=u\"><IMG SRC=\"$hdnm/images/addevent.gif\" BORDER=\"0\" ALT=\"Add Event To My Personal Calendar\"></a>");
      }
      if ($lgrouptab{$group}{ctype} eq "Community") {
         $imgurl = "";
      }

      #if ($vw eq "w") {
      #   $burlhref1 = "<a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$en&login=$login\">$etitle</a> $hour $min $meridian $imgurl $addeventtop $hr";
      #} else {

      $burlhref1 = "<CENTER><a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$en&login=$login\">$etitle</a> <BR>$desc <BR>$hour $min $meridian <BR> $imgurl $addeventtop </CENTER> $hr";
      #}

   } else {

      #if ($vw eq "w") {
      #   $burlhref1 = "<a href=\"$burl\">$etitle</a> $hour $min $meridian $imgurl $hr";
      #} else {

      $burlhref1 = "<CENTER><a href=\"$burl\">$etitle</a> <BR>$desc <BR>$hour $min $meridian <BR> $imgurl </CENTER> $hr";
         #hddebug("not weekly came here burlhref1 = $burlhref1");
      #}
   }
   $burlhref = adjusturl($burlhref1);

   #if ($vw eq "w") {
   #   $burlhref .=  createWeeklyImageLink($en, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vw, $free, $dtype, $group);
   #}

   return $burlhref;

}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $group, $sc) = @_;

   #bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed' ] };

   if (($group ne "") && (exists $lgrouptab{$group}) && ($lgrouptab{$group}{ctype} eq "Community") ) {
      $showbusy = "";
      $delimg = "";
      $dimg = "";
   } else {
      if ($free ne "Free") {
        $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
      } else {
       $showbusy = "";
      }
      $dimg = createDtypeImg($dtype);
      if ($sc eq "p") {
         $delimg = "";
      } else {
         $delimg = "<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a>";
      }
   }

   $imgurl = adjusturl ("$dimg $showbusy $delimg<BR><BR>");

   return $imgurl;
}


sub createWeeklyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $group) = @_;


   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed' ] };

   if (($group ne "") && (exists $lgrouptab{$group}) && ($lgrouptab{$group}{ctype} eq "Community") ) {
      $showbusy = "";
      $delimg = "";
      $dimg = "";
   } else {
      if ($free ne "Free") {
         $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
      } else {
         $showbusy = "";
      }
      $dimg = createDtypeImg($dtype);
      $delimg = "<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a>";
   }

   $imgurl = adjusturl ("$dimg $showbusy $delimg<BR>");
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

## this does not display event meetings that are not confirmed. i.e confirm=no
sub setEventDisplayRec {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $group, $sc) = @_;
   #hddebug "setEventDisplayRec group = $group";

   if ($group eq "") {

      #if ($sc eq "p") { 
      #   if ((isCalPublic($lg)) != 1) {
      #      return $prml;
          # }
      #}    

      $alpha = substr $lg, 0, 1;
      $alpha = $alpha . '-index';

      system "mkdir -p $ENV{HDDATA}/$alpha/$lg/appttab";
      system "chmod 755 $ENV{HDDATA}/$alpha/$lg/appttab";
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

      (-e "$ENV{HDDATA}/$alpha/$lg/appttab" and -d "$ENV{HDDATA}/$alpha/$lg/appttab") or return $prml;
   }


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

   (@records) = sort keys %appttab;

   #hddebug("numevents = $numevents");
   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];                              
      if ($onekey ne "")  {
         if (exists $appttab{$onekey}) {
            if ($group eq "") {
	       if ($sc eq "p") {
                  if ($appttab{$onekey}{'share'} eq "Private") {
                      next;
	          }
	       }	
            }
	    # donot display meetings that are not yet confirmed
	    if ($appttab{$onekey}{'confirm'} eq "no") {
	       next;
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
	       if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
            $venue = $appttab{$onekey}{'venue'};

            if (($sc eq "p") && ($appttab{$onekey}{'share'} eq "Showasbusy")) {
                $subject = "Busy";
            } else {
                $subject = $appttab{$onekey}{'subject'};
	    } 
	    if ($appttab{$onekey}{type} eq "meeting") {
		$subject .= " Meeting - $subject";
		#$url = adjusturl("$url&type=meeting");
            }
            $dtype = $appttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
	       if ($vwtype eq "m") {
	          $eventnum = $day - 1;
	       } else {
	          if ($vwtype eq "w") {
	             $eventnum = calutil::calutil::getWeekDayIndex($day, $month, $year);
                  }
	       }
            } 

            $desc = "$appttab{$onekey}{desc} <BR> $appttab{$onekey}{venue}";
	   
	    # append the events for this eventnum.
	    $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $group, $lg, $desc, $sc);

            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, $group, $sc);
            }
         }
      }    
   }

   #hddebug ("numevents = $numevents");
   if ($vwtype eq "d") {
      $prml = setDailyPrml($prml, $events, $numevents, $imglist);
   }  

   if ($vwtype eq "m") { 
      $prml = setMonthlyPrml($prml, $events, $numevents);
   }

   if ($vwtype eq "w") {
      $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);
   }

   $prml = strapp $prml, "pinvited=";
   $prml = strapp $prml, "people=";
   $prml = strapp $prml, "bizpeople=";
   $prml = strapp $prml, "businesses=";
   $prml = strapp $prml, "groups=";
   $prml = strapp $prml, "bizresource=";
   $prml = strapp $prml, "bizmem=";
   $prml = strapp $prml, "bizteams=";
  
   return $prml;
}

sub setDailyPrml {
   my($prml, $events, $numevents, $imglist) = @_;
   #hddebug ("numevents = $numevents");
   for ($i = 0; $i <= $numevents; $i = $i + 1) {
      if ($events[$i] ne "") {
         $prml = strapp $prml, "evtlist$i=$events[$i]";
         $prml = strapp $prml, "imglist$i=$imglist[$i]";
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
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "imglist$s=$space";
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
         #$space = adjusturl("&nbsp;");
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
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "imglist$u=$space";
      }
      $u = $u + 1;
   }
   return $prml;
}


sub setMonthlyPrml {
   my($prml, $events, $numevents) = @_;

   #hddebug "monthly numevents = $numevents \n";
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
   #hddebug "prml = $prml";
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
  
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw, $group, $sc) = @_;
   hddebug "setEventEditRec login = $lg";

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
   } else {

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
   }

   $onekey = $ceno;
   if (exists $appttab{$onekey}) {
      $prml = strapp $prml, "year=$appttab{$onekey}{'year'}";
      ($monthstr = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
      $evtbanner= adjusturl $appttab{$onekey}{'banner'};
      $prml = strapp $prml, "meridian=$appttab{$onekey}{'meridian'}";
      $prml = strapp $prml, "month=$monthstr"; 
      $prml = strapp $prml, "monthnum=$appttab{$onekey}{'month'}";
      $prml = strapp $prml, "day=$appttab{$onekey}{'day'}";
      $prml = strapp $prml, "evtbanner=$evtbanner";

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

      $venue = $appttab{$onekey}{venue};
      # $person = $appttab{$onekey}{person};
      $addresses = getaddresses($lg);

      $prml = strapp $prml, "dmin=$dmin";
      $prml = strapp $prml, "contact=";
      $prml = strapp $prml, "pinvited=";
      $prml = strapp $prml, "people=";
      $prml = strapp $prml, "bizpeople=";
      $prml = strapp $prml, "groups=";
      $prml = strapp $prml, "bizresource=";
      $prml = strapp $prml, "bizmem=";
      $prml = strapp $prml, "bizteams=";
      $prml = strapp $prml, "businesses=";
      $prml = strapp $prml, "evenue=$venue";
      # $prml = strapp $prml, "contact=$person";
      $prml = strapp $prml, "people=$addresses";

      ## people value is being used in the meeting. so it will replaced
      if (($lg eq "smitha") || ($lg eq "mjoshi") || ($lg eq "buddie")) {
        if ($appttab{$onekey}{'type'} eq "meeting") {
	    #$url =  adjusturl("$url&type=meeting");
  	    $prml = getinvitedpeople($onekey, $appttab{$onekey}{id}, $lg, $prml);
            $prml = strapp $prml, "type=meeting";
        }
      } 
   } 
   ## when we actually use it for people for people we need to check this
   ## piece of code.
   return $prml;
}
                        
sub deleteEvent {

   #my($ceno, $lg) = @_;
   my($ceno, $lg, $group) = @_;

   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';

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
      if (!exists($appttab{$ceno})) {
	  return $prml;
      }
      if ($appttab{$ceno}{type} eq "meeting") {
	 calfuncs::bizfuncs::cleanupmeetingtab($ceno, $appttab{$ceno}{id});
      }
      delete $appttab{$ceno};
      tied(%appttab)->sync();
      return $prml;
   }
                                   

   
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

   if (!exists($appttab{$ceno})) {
       return $prml;
   }
   if ($appttab{$ceno}{type} eq "meeting") {
      calfuncs::bizfuncs::cleanupmeetingtab($ceno, $appttab{$ceno}{id});
   }
  
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

   # bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };
   (@aptsno) = keys %appttab;
   if ($#aptsno < 0) {
      if (exists $remindtab{$lg}) {
         delete $remindtab{$lg};
         tied(%remindtab)->sync();
      }
   }
   return $prml;
}

sub addEvent {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $banner, $venue) = @_; 

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
   }                                        
   else {

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
   }

   $entryno = getkeys();
   #hddebug "group = $group \n";
   # bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };
   $remindtab{$lg}{'login'} = $lg;
   tied(%remindtab)->sync();
   system "chmod 777 $ENV{HDDATA}/aux/remindtab/$lg.rec";
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
   $appttab{$entryno}{'banner'} = adjusturl $banner;
   $appttab{$entryno}{'venue'} = adjusturl $venue;
   # $appttab{$entryno}{'person'} = adjusturl $econtact;
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
   
   if ($econtact ne "") {
       #hddebug "distribution list invitees list = $econtact";
      regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
   tied(%appttab)->sync();
   return $prml;
}

sub updateEvent  {

   #my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $econtact) = @_; 

   my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $banner, $venue) = @_; 

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
      $appttab{$entryno}{'banner'} = adjusturl $banner;
      $appttab{$entryno}{'venue'} = adjusturl $venue;
      $appttab{$entryno}{'person'} = adjusturl $econtact;
      if ($econtact ne "") {
         $eventdetails .= "Event: $etitle \n";
         $eventdetails .= "Event Type: $edtype \n";
         $eventdetails .= "Date: $emonth-$eday-$eyear \n";
         $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
         $eventdetails .= "Description: $edesc \n";
         $eventdetails .= "Frequency: $erecurtype \n";
         #hddebug("updateEvent, eventdetails = $eventdetails");
         #$appttab{$entryno}{'contact'} = trim $econtact;
      }
   }                                                                                                  
   tied(%appttab)->sync();
   if ($econtact ne "") {
       #hddebug "updateevent()distribution list invitees list = $econtact";
      regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
   return $prml;

}

sub displayTodo {

   #my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw) = @_;
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $group, $sc) = @_;

   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';

   if ($group eq "") {
      if ($sc eq "p") {
         if ((isCalPublic($lg)) != 1) {
            return $prml;
	 }
      }
      system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$lg/todotab";
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

      (-e "$ENV{HDDATA}/$alpha/$lg/todotab" and -d "$ENV{HDDATA}/$alpha/$lg/todotab") or return; 
   } else {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";

      # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

       -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";
   }                                                                           

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
         #hddebug "onekey = $onekey";
         if (!exists($todotab{$onekey})) {
            #hddebug "does not exist"; 
            next; 
         }
         #hddebug "group = $group";
         if ($group eq "") {
	    if ($sc eq "p") {
               if ($todotab{$onekey}{'share'} eq "Private") {
	          next; 
	       }
	    }
         }
         #status ("entryno = $onekey <BR>");
         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};

         #hddebug ("calmonth = $cmonth" );
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
            if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
         #hddebug "subject = $subject";

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = calutil::calutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum 
         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, $sc);

         #if ($vwtype ne "m") {
         #   $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
         #}
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

   my($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $subject, $todomntcnt, $priority, $desc, $sc) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $todourl = $url;
   $e = "de";

   $todourl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=t&vw=i");

   $hr = "<HR>";

   if ($sc eq "p") {
      $todoimgurl = "";
   } else {
      $todoimgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"delete\"></a>");
   }

   $pri = " Priority ";
   if ($subject ne "") {
      $todotitle = "$subject$pri$priority";
   } else {
      $todotitle = "Todo$pri$priority";
   }

   
   $burlhref1 = "<CENTER><a href=\"$todourl\">$todotitle</a> <BR>$desc <BR>$hour $meridian <BR> $todoimgurl <BR></CENTER> $hr";
   $burlhref = adjusturl($burlhref1);
   return $burlhref;

}

sub createTodoWeeklyImageLink {

   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $imgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"delete\"></a><BR><BR>");

   #$prml = strapp $prml, "imglist$row1=$imgurl";
   return $imgurl;

}


sub createTodoDailyImageLink {
   my ($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw ) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $timgurl = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=t&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"delete\"></a><BR><BR>");

   return $timgurl;
}


sub editTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $group) = @_;
   #print "entryno = $ceno \n";             

   if ($group eq "") {

      $alpha = substr $lg, 0, 1;
      $alpha = $alpha . '-index';

      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };
   } else {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";

      # bind group todotab table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

      -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";                
   }

   #hddebug "entryno = $ceno";
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
      $evtbanner = adjusturl $todotab{$onekey}{banner};
      $prml = strapp $prml, "evtbanner=$evtbanner";
   }
   return $prml;


}

sub deleteTodo {
   my($ceno, $lg, $group) = @_; 

   #hddebug "group = $group";
   if ($group eq "") {
      $alpha = substr $lg, 0, 1;
      $alpha = $alpha . '-index';

      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] }; 
   }  else {

      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";
      # bind group todotab table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] }; 

      -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";
   }

   #hddebug "ceno = $ceno";
   if (!exists($todotab{$ceno})) {
      return $prml;
   }
   delete $todotab{$ceno};
   tied(%todotab)->sync();   
   return $prml;
}

sub addTodo {
    my($ttitle, $tdesc, $tmonth, $tday, $tyear, $thour, $tmeridian, $tshare, $tpriority, $tstatus, $lg, $group, $banner) = @_; 

    if ($group eq "") {

       $alpha = substr $lg, 0, 1;
       $alpha = $alpha . '-index';

       # bind todo table vars
       tie %todotab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
       SUFIX => '.rec',
       SCHEMA => {
            ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
            'day', 'year', 'meridian', 'priority', 'status', 'share', 
            'hour', 'banner'] };
    } else {

       system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";

       # bind group todotab table vars
       tie %todotab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
       SUFIX => '.rec',
       SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] }; 

        -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";
   }

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
   $todotab{$entryno}{'banner'} = adjusturl $banner;      

   tied(%todotab)->sync(); 
   return $prml;
}

sub updateTodo {
    my($entryno, $etitle,  $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $lg, $group, $banner) = @_; 

   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';

   if ($group eq "") { 
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };
   } else {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";
      # bind group todotab table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] }; 

       -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";
   }
 
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
       $todotab{$entryno}{'banner'} = adjusturl $banner;
       tied(%todotab)->sync();
    }
    return $prml;
}


sub publishEvent {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $group) = @_;

   #hddebug "came here";
   if ((isCalPublic($lg)) != 1) {
   #hddebug "came here2";
      return $prml;
   };


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
      hddebug "records = $#records";
      if ($#records >= 0) {
         for ($g = 0; $g <= $#records; $g = $g+1) {
            $onekey = $records[$g];
            if (exists($appttab{$onekey})) {
               if ($appttab{$onekey}{'share'} ne "Private") {
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
                    if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
                 $venue = $appttab{$onekey}{'venue'};
		 if ($appttab{$onekey}{type} eq "meeting") {
		    $subject .= " Meeting - $subject";
	            #$url =  adjusturl("$url&type=meeting");
		 }


                 if ($vwtype eq "d") {
                    $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
                 } else {
                    if ($vwtype eq "m") {
                       $eventnum = $day - 1;
                    } else {
                       if ($vwtype eq "w") {
                          $eventnum = calutil::calutil::getWeekDayIndex($day, $month, $year);
                       }
                    }
                 }

                 $desc = "$appttab{$onekey}{desc}<BR>$appttab{$onekey}{venue}";
                 # append the events for this eventnum.
                 $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $group, $lg, $desc, $sc);

                  if ($vwtype ne "m") {
                     $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, $group, $sc);
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

   my($prml, $vwtype, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $a, $en, $f, $sc, $group) = @_;

   #my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f) = @_;
   #status("publishTodo $lg = $lg <BR>");


   if ($group eq "") {
      if ((isCalPublic($lg)) != 1) {
         return $prml;
      }
      $alpha = substr $lg, 0, 1;
      $alpha = $alpha . '-index';

      system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$lg/todotab";
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

      (-e "$ENV{HDDATA}/$alpha/$lg/todotab" and -d "$ENV{HDDATA}/$alpha/$lg/todotab") or return;
   } else {
   }

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

         if ($todotab{$onekey}{'share'} ne "Private") { 
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
            if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
                  $todonum = calutil::calutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum

         $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, $sc);

         #if ($vwtype ne "m") {
         #   $timglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
         #}
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

   my($login) = @_;

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };                          

    if (exists($logtab{$login} )) {
       if (($logtab{$login}{'calpublish'}) eq "CHECKED") {
          return 1;
       }
    }

    return 0;
}

sub regEmailContacts {

   my($contacts, $mname, $eventdetails, $entryno, $g) = @_;

   $contacts = trim $contacts;
   $contacts = "\L$contacts";

   #(@hashemail) = split " ", $contacts;
   #if ($#hashemail >= 1) {
   #   $contacts =~ s/ /,/g;
   #   hddebug "contacts = $contacts";
   #}
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
    $acode = "";
    foreach $cn (@hshemail) {
       if ( (notEmailAddress($cn)) && (!exists $logtab{$cn}) ) {
          hddebug "none here";
	  next;
       } 
       $cntr = $cntr + 1;
       $cn = "\L$cn";
       $cn = trim $cn;
       hddebug "cn = $cn";
       hddebug "mname = $mname";
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
             hddebug "$cn not invited, as per calinvite flag";
             next;
          }
          $login = $cn;
          $cn = $logtab{$cn}{email};
          $eemail = 1;          
          $oldlogin = $login;
       } else {
	  ## Not a hotdiary login or user.
	  if (notEmailAddress($cn)) { 
	      next;
	  }
          ($login, $domain) = split '@', $cn;
          $login = trim $login;
          $eemail = 0;          
       }

       if ($login =~ /\&/) {
          next;
       }
       if ( (notLogin $login) || (exists ($logtab{$login} )) ) {
          if ($eemail ne "1") {
	     $oldlogin = $login;
             if (exists($logtab{$login} )) {
      	        $login = "$login$$" . "$cntr";
             }
	  }
       }

       ### this is an old one statement that was commented out longback.
       #if (!exists ($logtab{$login} )) {

	  ### Not REQUIRED to add new user
	  ### we are not adding users anymore when we send events.
	  ### so logtab and activetab and surveytab information is commented

          if ($eemail ne "1") {
             $logtab{$login}{'login'} = $login;
             $logtab{$login}{'fname'} = $login;
             $logtab{$login}{'password'} = $login;
             $logtab{$login}{'email'} = $cn;
             $logtab{$login}{'zone'} = $logtab{$mname}{zone};
             # bind active table vars
             tie %activetab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/aux/activetab",
             SUFIX => '.rec',
             SCHEMA => {
                  ORDER => ['login', 'acode', 'verified' ] };
             $pidd = $$;
             $acode = rand $pidd;
             $acode = $acode % $pidd;
	 
             $activetab{$login}{login} = $login;
             $activetab{$login}{acode} = $acode;
             $activetab{$login}{verified} = "false";
             tied(%activetab)->sync();

             $surveytab{$login}{'login'} = $login;
             $surveytab{$login}{'hearaboutus'} = "Friend";
             $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
             tied(%surveytab)->sync();
          }

          
          hddebug "oldlogin = $oldlogin";
          hddebug "eemail = $eemail";
         
          if (exists $logtab{$oldlogin}) {
             $fnam = $logtab{$oldlogin}{fname};
          } else {
             $fnam = "Friend";
          }
          $emsg = "Dear $fnam, \n \n";
          $uname = $logtab{$mname}{'fname'} . " " . $logtab{$mname}{'lname'};
          $emsg .= "You have been invited by $uname to an event. \n \n";
          $emsg .= "Event Details: \n";
          $emsg .=  $eventdetails;
          $emsg .=  "\n\n";
          $emsg .= "If you would like to contact $uname directly, please send an email to $uname at $logtab{$mname}{'email'}. Member login ID of $uname on HotDiary is \"$mname\".\n";

          if ($eemail ne "1") {
             $emsg .= "Your Hotdiary Account information: \nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
             $emsg .= "Login: $login \n";
             $emsg .= "Password: $logtab{$login}{'password'}\n\n";
             $emsg .= "Activation Code: $acode\n\n";
             #$emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
          }

          $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Internet Products and Services\n";

          qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
          #qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};

	  ## creating new user, so don't use $logtab{$login}{email}
          qx{metasend -b -S 800000 -m \"text/plain\" -f $ENV{HDHOME}/tmp/reginviteletter$$ -s \"Invitation From $uname\" -e \"\" -t \"$logtab{$login}{email}\" -F \"$uname <$logtab{$mname}{'email'}>\"};

          $alpha = substr $login, 0, 1;
          $alpha = $alpha . '-index';

	  ###  REQUIRED to add new user
          if ($eemail ne "1") {
             system "/bin/mkdir -p $ENV{HDREP}/$alpha/$login";
             system "/bin/chmod 755 $ENV{HDREP}/$alpha/$login";
             system "/bin/mkdir -p $ENV{HDHOME}/rep/$alpha/$login";
             system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login";
             system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login";
             system "/bin/touch $ENV{HDDATA}/$alpha/$login/addrentrytab";
             system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/addrentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/addrtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/addrtab";
             system "/bin/touch $ENV{HDDATA}/$alpha/$login/apptentrytab";
             system "/bin/chmod 660 $ENV{HDDATA}/$alpha/$login/apptentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/appttab";
             system "/bin/chmod 770 $ENV{HDDATA}/$alpha/$login/appttab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
             system "/bin/chmod -R 770 $ENV{HDDATA}/groups/$alpha/$login";
             system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alpha/$login/index.html";
             system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alpha/$login";
             system "/bin/chmod 775 $ENV{HDDATA}/$alpha/$login/calendar_events.txt";

             system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/faxtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/faxtab";

             system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/faxdeptab";
             system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/faxdeptab";
          }

          hddebug "entryno = $entryno";

	  ### REQUIRED for new user to add an appttab entry
	  if ( (($eemail eq "1") && ($logtab{$login}{checkid} eq "CHECKED") ) || ($eemail ne "1") ) {
             if ($g eq "") {
	         $malpha = substr $mname, 0, 1;
                 $malpha = $malpha . '-index';
                 system "/bin/cp $ENV{HDDATA}/$malpha/$mname/appttab/$entryno.rec $ENV{HDDATA}/$alpha/$login/appttab/$entryno.rec";

                 #add the entry in the apptentrytab
                 $tfile = "$ENV{HDDATA}/$alpha/$login/apptentrytab";
                 open thandle, ">>$tfile";
                 printf thandle "%s\n", $entryno;
                 close thandle;
             } else {
                 system "/bin/cp $ENV{HDDATA}/listed/groups/$g/appttab/$entryno.rec $ENV{HDDATA}/$alpha/$login/appttab/$entryno.rec";
             }
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
      #}
   }

#synch the database
   tied(%logtab)->sync();
}

sub addGroupEventToMyCal {

   my($en, $login, $group) = @_;

   if ($group ne "") {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";

      # bind group appt table vars
      tie %grouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject'] };

      -d "$ENV{HDDATA}/listed/groups/$group/appttab or return $prml";
   }   


  $alpha = substr $login, 0, 1;
  $alpha = $alpha . '-index';
   if ($login ne "") {
     # bind personal appt table vars
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$alpha/$login/appttab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   }

   $entryno = getkeys(); 
   # bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };
   $remindtab{$login}{login} = $login;
   tied(%remindtab)->sync();
   system "chmod 777 $ENV{HDDATA}/aux/remindtab/$login.rec";
   $appttab{$entryno}{'login'} = trim $login;
   $appttab{$entryno}{'month'} = $grouptab{$en}{month};
   $appttab{$entryno}{'day'} = $grouptab{$en}{day};
   $appttab{$entryno}{'year'} = $grouptab{$en}{year};
   $appttab{$entryno}{'hour'} = $grouptab{$en}{hour};
   $appttab{$entryno}{'min'} = $grouptab{$en}{min};
   $appttab{$entryno}{'meridian'} = $grouptab{$en}{meridian};
   $appttab{$entryno}{'dhour'} = $grouptab{$en}{dhour};
   $appttab{$entryno}{'dmin'} = $grouptab{$en}{dmin};
   $appttab{$entryno}{'dtype'} = $grouptab{$en}{dtype};
   $appttab{$entryno}{'atype'} = $grouptab{$en}{atype};
   $appttab{$entryno}{'desc'} = $grouptab{$en}{desc};
   $appttab{$entryno}{'zone'} = $grouptab{$en}{zone};
   $appttab{$entryno}{'recurtype'} = $grouptab{$en}{recurtype};
   $appttab{$entryno}{'share'} = $grouptab{$en}{share};
   $appttab{$entryno}{'free'} = $grouptab{$en}{free};
   $appttab{$entryno}{'subject'} = $grouptab{$en}{subject};
   $appttab{$entryno}{'entryno'} = $entryno;

   #add the entry in the apptentrytab
   $tfile = "$ENV{HDDATA}/$alpha/$login/apptentrytab";
   open thandle, ">>$tfile";
   printf thandle "%s\n", $entryno;
   close thandle;

   tied(%appttab)->sync();
   return 1;

} 

sub displayEventsAndTodos {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $group, $sc) = @_;

   if ($group eq "") {

      if ($sc eq "p") {
         if ((isCalPublic($lg)) != 1) {
            return $prml;
         }
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

      (-e "$ENV{HDDATA}/$alpha/$lg/appttab" and -d "$ENV{HDDATA}/$alpha/$lg/appttab") or return $prml;
   }


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

   (@records) = sort keys %appttab;

   #hddebug("numevents = $numevents");
   for ($y = 0; $y <= $#records; $y = $y+1) {
      $onekey = $records[$y];
      if ($onekey ne "")  {
         if (exists $appttab{$onekey}) {
            if ($group eq "") {
               if ($sc eq "p") {
                  if ($appttab{$onekey}{'share'} eq "Private") {
                      next;
                  }
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
               if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
   	    if ($appttab{$onekey}{type} eq "meeting") {
	        $subject .= " Meeting - $subject";
		#$url = adjusturl("$url&type=meeting");
	    }

            $dtype = $appttab{$onekey}{'dtype'};


            if ($vwtype eq "d") {
               $eventnum = getDailyEventNum($year, $month, $day, $hour, $min, $meridian);
            } else {
               if ($vwtype eq "m") {
                  $eventnum = $day - 1;
               } else {
                  if ($vwtype eq "w") {
                     $eventnum = calutil::calutil::getWeekDayIndex($day, $month, $year);
                  }
               }
            }

            $desc = "$appttab{$onekey}{desc} <BR> $appttab{$onekey}{venue}";
            # append the events for this eventnum.
            $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $group, $lg, $desc, $sc);
            if ($vwtype ne "m") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype, $group, $sc);
            }
         }
      }
   }

   if ($group eq "") { 
      system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$lg/todotab";
      # bind todo table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

      (-e "$ENV{HDDATA}/$alpha/$lg/todotab" and -d "$ENV{HDDATA}/$alpha/$lg/todotab") or return;
   } else {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/todotab";

      # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

       -d "$ENV{HDDATA}/listed/groups/$group/todotab or return $prml";
   }


   $todomntcnt = 0;
   (@records) = sort keys %todotab;

   if ($#records >= 0) {
      for ($g = 0; $g <= $#records; $g = $g+1) {
         $onekey = $records[$g];
         #hddebug "onekey = $onekey";
         if (!exists($todotab{$onekey})) {
            #hddebug "does not exist";
            next;
         }
         #hddebug "group = $group";
         if ($group eq "") {
            if ($sc eq "p") {
               if ($todotab{$onekey}{'share'} eq "Private") {
                  next;
               }
            }
         }
         #status ("entryno = $onekey <BR>");
         $year = $todotab{$onekey}{'year'};
         $month = $todotab{$onekey}{'month'};
         $day = $todotab{$onekey}{'day'};

         #hddebug ("calmonth = $cmonth" );
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
            if ((calutil::calutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
         #hddebug "subject = $subject";

         if ($vwtype eq "d") {
            $todonum = getDailyEventNum($year, $month, $day, $hour, "", $meridian);
         } else {
            if ($vwtype eq "m") {
               $todonum = $day - 1;
               $todomntcnt = $todmntcnt + 1;
            } else {
               if ($vwtype eq "w") {
                  $todonum = calutil::calutil::getWeekDayIndex($day, $month, $year);
               }
            }
         }

         # append the todos for this todonum
         $events[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, $sc);

         #if ($vwtype ne "m") {
         #   $imglist[$todonum] .=  createTodoDailyImageLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype );
         #}
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

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $group) = @_;

   hddebug "displayDetails";
   $onekey = $ceno;


   $prml = strapp $prml, "subdetails=$subject";
   $app_tab = 0;
   $todo_tab = 0;
   # bind todo table vars

   if ($group ne "") {
      if (-d ("$ENV{HDDATA}/listed/groups/$group/appttab")) { 
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

         $app_tab = 1;
      }
   } else {
      $alpha = substr $lg, 0, 1;
      $alpha = $alpha . '-index';

      if (-d ("$ENV{HDDATA}/$alpha/$lg/appttab") ) {
         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/appttab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER => ['entryno', 'login', 'month', 'day', 'year',
               'hour', 'min', 'meridian', 'dhour', 'dmin',
               'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
               'subject', 'street', 'city', 'state', 'zipcode', 'country',
               'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

         $app_tab = 1;
      }
   }

  
   if ($group ne "") {
      if (-d ("$ENV{HDDATA}/listed/groups/$group/todotab")) {
         # bind group appt table vars
         tie %todotab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
            'day', 'year', 'meridian', 'priority', 'status', 'share', 
            'hour', 'banner'] };
         $todo_tab = 1;
       }
    } else {
       if (-d ("$ENV{HDDATA}/$alpha/$lg/todotab") ) {
          tie %todotab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
                 'day', 'year', 'meridian', 'priority', 'status', 'share', 'hour',
		 'banner'] };
          $todo_tab = 1;
       }
    }

   if ($todo_tab == 1) {
      if (exists($todotab{$onekey})) {
         ($monthstr = getmonthstr($todotab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $todotab{$onekey}{'day'} $todotab{$onekey}{'year'} $todotab{$onekey}{'meridian'} <BR> Priority: $todotab{$onekey}{'priority'} <BR> Status: $todotab{$onekey}{'status'}";
         $evtbanner = adjusturl $todotab{$onekey}{banner};
         if ($todotab{$onekey}{'share'} eq "Private") {
            $subject = "Event & To-do Details: Private<BR><BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            $prml = strapp $prml, "evtbanner=$evtbanner";
            return $prml;
         }
         $subject = "Details: $todotab{$onekey}{'subject'}<BR><BR> Description: $todotab{$onekey}{'desc'}<BR><BR>";
         #$subject .= "$todotab{$onekey}{'desc'}";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         hddebug "subject = $subject";
         $prml = strapp $prml, "subdetails=$subject";
         return $prml;
      }
   }

   if ($app_tab == 1)  {
      if (exists($appttab{$onekey})) {
         ($monthstr = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
         $subject_d .= "Date: $monthstr $appttab{$onekey}{'day'} $appttab{$onekey}{'year'} $appttab{$onekey}{hour} $appttab{$onekey}{min} $appttab{$onekey}{'meridian'} <BR> Free/Busy: $appttab{$onekey}{free}<BR>";
         $evtbanner = adjusturl $appttab{$onekey}{banner};
         if ($appttab{$onekey}{'share'} eq "Private") {
            $subject = "Details: Private<BR><BR>";
            $subject .= "User: $lg <BR> $subject_d";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            $prml = strapp $prml, "evtbanner=$evtbanner";
            #hddebug "subject1 = $subject";
            return $prml;
         }
         $subject = "Details: $appttab{$onekey}{'subject'}<BR> <BR> Description: $appttab{$onekey}{'desc'}<BR><BR>";
         $subject .= $subject_d;
         $subject = adjusturl $subject;
         #hddebug "subject = $subject";
         $prml = strapp $prml, "subdetails=$subject";
         $prml = strapp $prml, "evtbanner=$evtbanner";
         return $prml;
      }
   }

   return $prml;
}


sub getinvitedpeople {

   my($en, $bbusiness, $login, $prml) = @_;

   hddebug "getinvitedpeople()";
   hddebug "en = $en, business=$bbusiness, login=$login";
   ($business, $rem) = split(" ", $bbusiness);
   hddebug "business=$business";


   if (($en eq "") || ($business eq "") || ($login eq "")) {
       return $prml;
   }
   $business = trim $business;

   if (!-d ("$ENV{HDDATA}/business/business/$business/meetingtab")) {
      return $prml;
   }

   $people = "";
   $bizpeople = "";
   $groups = "";
   $bizresource = "";
   $bizmem = "";
   $bizteams = "";
   $businesses = "";

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner',
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   
   tie %meetingtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/meetingtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
          'numresources', 'resources', 'teams', 'groups', 'mem', 'businesses'] };

   if (!exists($meetingtab{$en})) {
     return $prml;
   }

   (@hshmems) = split(" ", $meetingtab{$en}{invitees});
   $invitees = "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"75\"><TR><TD>";

   ## top table
   $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=fffff>Select Mandatory Invitees</TD><TD WIDTH=\"10%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=fffff>Select RSVP Invitees</TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Attendees (login-Firstname-LastName-EmailAddress)</FONT></TD></TR></TABLE>";

   $invitees .= "<TR><TD><TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\">";

   $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT COLOR=0f0f5f FACE=Verdana SIZE=2>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=04c8dd>Invited Members/Groups/Teams</FONT></TD></TR>";

   for ($i =0; $i <= $#hshmems; $i = $i + 1) { 
      $people .= "$hshmems[$i] ";
      $invitees .= "<TR WIDTH=\"100%\" BGCOLOR=dddddd FGCOLOR=ffffff><TD WIDTH=\"15%\" ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$hshmems[$i] VALUE=man CHECKED></TD><TD WIDTH=\"10%\" ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$hshmems[$i] VALUE=rsvp></TD><TD WIDTH=\"75%\"><FONT FACE=Verdana SIZE=2>$hshmems[$i]-</FONT></TD></TR>";
   }
   $peoplecntr = $#hshmems;


   (@hshgroups) = split (" ", $meetingtab{$en}{groups});
   $groupcntr = $#hshmems;

   ## groups 
   for ($i = 0; $i <= $#hshgroups; $i = $i + 1) {
      $groups .= "Group-$hshgroups[$i] ";
      $invitees .= "<TR WIDTH=\"100%\" BGCOLOR=dddddd FGCOLOR=ffffff><TD WIDTH=\"15%\" ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Group-$hshgroups[$i] VALUE=man CHECKED></FONT></TD><TD WIDTH=\"10%\" ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Group-$hshgroups[$i] VALUE=rsvp></TD><TD WIDTH=\"75%\"><FONT FACE=Verdana SIZE=2>Group-$hshgroups[$i]</FONT></TD></TR>";
   }

   ## we should avoid duplicates from this list of personal invitees.
   ## remove duplicates
   (@hshbizmems) = split(" ", $meetingtab{$en}{mem});

   ##invited biz-members
   for ($i =0; $i <= $#hshbizmems; $i = $i + 1) {
      ($tm, $mem) = split("-", $hshbizmems[$i]); 
      $mem = trim $mem;
      ## this means it is not a duplicate entry
      if ((index "\L$people", "\L$mem") == -1) {
         if (exists $logtab{$mem}) {
           $people .= "$mem "; 
           $addr = $tm . "-". $mem . "-" . $logtab{$mem}{fname} . "-" . $logtab{$mem}{lname}. "-". $logtab{$mem}{email};
	   
           $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$mem VALUE=man CHECKED></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$mem VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$addr</FONT></TD></TR>";
         }
      }
   }


   (@hshbizresources) = split(" ", $meetingtab{$en}{resources});
   for ($i =0; $i <= $#hshbizresources; $i = $i + 1) {
       $bizresource .= "$hshbizresources[$i] ";
       $invitees .=  "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Resource-$hshbizresources[$i] VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Resource-$hshbizresources[$i] VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>Resource-$hshbizresources[$i]</FONT></TD></TR>";
   }


   ## teams in the form of business-teamname
   (@hshteams) = split (" ", $meetingtab{$en}{teams});
   $teamcntr = $#hshteams;
   for ($i = 0; $i <= $#hshteams; $i = $i + 1) {
       $bizteams .= "$hshteams[$i] ";
       $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff>";   
       $invitees .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$hshteams[$i] VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$hshteams[$i]</FONT></TD></TR><TR><TD>";
   
       $invitees .= "<TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT COLOR=0f0f5f SIZE=2 FACE=Verdana>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=f20236>Exclude Members From Business Team $hshteams[$i]</FONT></TD></TR>";
       ($biz, $teamname) = split("-", $hshteams[$i]);
       if (-d ("$ENV{HDDATA}/business/business/$biz/teams/$teamname/teampeopletab")) {
         # bind manager table vars
         tie %teampeopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$biz/teams/$teamname/teampeopletab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login']};
           
         foreach $mem (sort keys %teampeopletab) {
            $bizpeople .= "$biz-$teamname-$mem ";
           #$invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD FONT FACE=Verdana SIZE=3><B>Teams</B></TD></TR>";   
            
            $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff>";   
            $invitees .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$biz-$teamname-$mem VALUE=man></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$teamname-$mem</FONT></TD></TR>";
	 }
      }
   }

   $invitees .= "</TABLE>";


   $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT FACE=Verdana COLOR=0f0f5f SIZE=2>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Personal Address Book</FONT></TD></TR>";

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   ## personal addressbook
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
               $people .= "$id ";
               $addr = trim "\L$id-\L$logtab{$id}{fname}-$logtab{$id}{lname}-$logtab{$id}{email}";
               $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$id VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$id VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$addr</FONT></TD></TR>";
            }
         }
      }
   }
   $invitees .= "</TABLE>";

   #resources
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

	 #hddebug "busname  = $busname";

         if (exists($peopletab{$login})) {
	    #hddebug "busname peopletab  = $busname";
            if (-d("$ENV{HDDATA}/business/business/$busname/restab")) {

               $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT COLOR=0f0f5f SIZE=2 FACE=Verdana>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Resources of $busname</FONT></TD></TR>";

               tie %restab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/business/business/$busname/restab",
               SUFIX => '.rec',
               SCHEMA => {
                  ORDER =>  ['type', 'name', 'bldg', 'zipcode',
                                'country', 'tz'] };

	       #hddebug "busname restab  = $busname";
               foreach $res (sort keys %restab) {
                  if (exists($restab{$res})) {
                     $res = trim $res;
                     $bizresource .= "Resource-$busname-$res ";
	             $invitees .=  "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Resource-$busname-$res VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Resource-$busname-$res VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>Resource-$res</FONT></TD></TR>";
                  } else {
		     next;
	 	  }
               }
               $invitees .= "</TABLE>";
            }
         } else {
	     next;
	 } 
      }
   }

   ## businessdirectory
   $invitees .= "<TR><TD>";
   foreach $busname (sort keys %businesstab) {
      if (-d("$ENV{HDDATA}/business/business/$busname/peopletab")) {
         tie %peopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$busname/peopletab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'business']};

         if (exists($peopletab{$login})) {
            $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT COLOR=0f0f5f SIZE=2 FACE=Verdana>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Biz Addresses of employees in $busname</FONT></TD></TR>";
	    $members = "";
            $not_exists = " ";
            foreach $mem (sort keys %peopletab) {
               #hddebug "mem = $mem";
               if (exists($logtab{$mem}) ) {
	          $bizmem .= "$busname-$mem "; 
                  $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$mem VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$mem VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$mem-$logtab{$mem}{'fname'}-$logtab{$mem}{'lname'}-$logtab{$mem}{email}</FONT></TD></TR>";
               }
               if ($not_exists == 0) {
                  if (exists $emptab{$mem}) {
	             $bizmem .= "$busname-$mem "; 
                     $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$mem VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$mem VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$mem-$emptab{$mem}{'fname'}-$emptab{$mem}{'lname'}-$logtab{$mem}{email}</FONT></TD></TR>";
                  }
               }
	    }
	    $invitees .= "</TABLE>";
	 }
      }
   }


### teams
   foreach $busname (sort keys %businesstab) {
      $busname = trim $busname;
      if (-d("$ENV{HDDATA}/business/business/$busname/peopletab")) {
         tie %peopletab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$busname/peopletab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['business']};
         if (exists($peopletab{$login})) {
	     $businesses .= "$busname ";
	     $bizteams .= "$busname-AllTeams "; 
            $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT COLOR=0f0f5f SIZE=2 FACE=Verdana>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Biz Teams in $busname</FONT></TD></TR>";
            $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-AllTeams VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-AllTeams VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$busname-AllTeams</FONT></TD></TR>";
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
	       #hddebug "numteams = $#numteams";
               foreach $team (sort keys %teamtab) {
                  if (exists($teamtab{$team})) {
	             $team = trim $team;
	             $bizteams .= "$busname-$team "; 
                     $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$team VALUE=man></FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$team VALUE=rsvp></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$busname-$team</FONT></TD></TR>";
                     if (-d ("$ENV{HDDATA}/business/business/$busname/teams/$team/teampeopletab")) {
	                $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>&nbsp;</FONT></TD><TD ALIGN=CENTER>&nbsp;</FONT></TD><TD ALIGN=CENTER><FONT FACE=Verdana COLOR=f20236 SIZE=2>Exclude Members from $busname-$team</FONT></TD></TR>";
		         # bind manager table vars
 		        tie %teampeopletab, 'AsciiDB::TagFile',
	                DIRECTORY => "$ENV{HDDATA}/business/business/$busname/teams/$team/teampeopletab",
            	        SUFIX => '.rec',
		        SCHEMA => {
		        ORDER => ['login']};

	                foreach $mem (sort keys %teampeopletab) {
	                   $bizpeople .= "$busname-$team-$mem ";
	                   $invitees .= "<TR BGCOLOR=dddddd FGCOLOR=ffffff>";
	                   $invitees .= "<TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=$busname-$team-$mem VALUE=man></FONT></TD><TD>&nbsp;</TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$team-$mem</FONT></TD></TR>";
         		}
      		     }
                  }
               }
            } 
            $invitees .= "</TABLE>";
         }
      }
   }

## all groups

   $invitees .= "<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=1 WIDTH=\"100%\"><TR WIDTH=\"100%\" FGCOLOR=ffffff><TD WIDTH=\"15%\" BGCOLOR=0f0f5f ><FONT FACE=Verdana SIZE=2 COLOR=0f0f5f>Select Mandatory Invitees</FONT></TD><TD  WIDTH=\"10%\" BGCOLOR=0f0f5f><FONT SIZE=2 COLOR=0f0f5f FACE=Verdana>Select RSVP Invitees</FONT></TD><TD WIDTH=\"75%\" BGCOLOR=0f0f5f HEIGHT=\"100%\"><FONT FACE=Verdana SIZE=2 COLOR=ffffff>Groups (Subscribed/Founded)</FONT></TD></TR>";

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
            $groups .= "Group-$group ";
            $invitees .= "<TR WIDTH=\"100%\"><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Group-$group VALUE=man></TD><TD>&nbsp;</TD></FONT></TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$group</FONT></TD></TR>";
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
            $groups .= "Group-$group ";
            $invitees .= "<TR WIDTH=\"100%\"><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2><INPUT TYPE=RADIO NAME=Group-$group VALUE=man></FONT></TD><TD>&nbsp;</TD><TD ALIGN=CENTER> <FONT FACE=Verdana SIZE=2>$group</FONT></TD></TR>";
         }
      }
   }
   $invitees .= "</TABELE>";

 

   $invitees .= "</TD></TR>";

   $invitees .= "</TD></TR></TABLE>";
   $invitees .= "</TD></TR></TABLE>";


   $people = adjusturl $people;
   $bizteams = adjusturl $bizteams;
   $bizmem = adjusturl $bizmem;
   $bizresource = adjusturl $bizresource;
   $groups = adjusturl $groups;
   $bizpeople = adjusturl $bizpeople;

   #$teams = adjusturl $teams;
   #$contacts = adjusturl $contacts;

   $prml = strapp $prml, "people=$people";
   $invitees = adjusturl $invitees;
   $prml = strapp $prml, "pinvited=$invitees";
   $prml = strapp $prml, "bizteams=$bizteams";
   $prml = strapp $prml, "bizmem=$bizmem";
   $prml = strapp $prml, "bizresource=$bizresource";
   $prml = strapp $prml, "groups=$groups";
   $prml = strapp $prml, "bizpeople=$bizpeople";
   $prml = strapp $prml, "teams=";
   $prml = strapp $prml, "contacts=";
   $prml = strapp $prml, "businesses=$businesses";
   $prml = strapp $prml, "type=";

   return $prml;
   
}

sub deleteAllCal {

   my($lg) = @_;

   if ($lg eq "") {
      return;
   }

   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';

   (-e "$ENV{HDDATA}/$alpha/$lg/appttab" and -d "$ENV{HDDATA}/$alpha/$lg/appttab") or return;

   $tfile = "$ENV{HDDATA}/$alpha/$lg/apptentrytab";
   system "rm $tfile";
   system "touch $tfile";

   system "rm -f $ENV{HDDATA}/$alpha/$lg/appttab/*.rec";

   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };

   (@aptsno) = keys %appttab;

   if ($#aptsno < 0) {
      if (exists $remindtab{$lg}) {
         delete $remindtab{$lg};
         tied(%remindtab)->sync();
      }
   }

   (-e "$ENV{HDDATA}/$alpha/$lg/todotab" and -d "$ENV{HDDATA}/$alpha/$lg/todotab") or return; 
   system "rm -f $ENV{HDDATA}/$alpha/$lg/todotab/*.rec";

}

sub publishEventNew {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $group) = @_;

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

   
}


sub getaddresses {

   my($login) = @_;
   hddebug "getaddresses";

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

      foreach $id (sort keys %addrtab) {
            $addr = trim "\L$addrtab{$id}{fname} $space $addrtab{$id}{lname}-$addrtab{$id}{email}";
            $members .= "\<OPTION\>$addr<\/OPTION\>";
      }
   }
   $members = adjusturl $members;
   return $members;
}

sub getEmailContacts {

   my($contacts, $mname) = @_;

   $contacts = trim $contacts;
   $contacts = "\L$contacts";

   (@hshemail) = split ",", $contacts;
   #hddebug "contacts = $contacts, $#hshemail";

   ## we don't want to send invitations to the existing users. 
   ## as they already have their own appts added to their appt table.
   ## 
   foreach $cn (@hshemail) {

       # hddebug "cn = $cn, cnt = $cnt, total count $#hshemail";
       # bind login table vars
       tie %logtab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/logtab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner',
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] }; 	

       ## not a user with valid email address, skip it
       if (!notEmailAddress($cn)) {
          #hddebug "none here";
          next;
       }
       $cntr = $cntr + 1;
       $cn = "\L$cn";
       $cn = trim $cn;

       ## valid existing user who created this appt, skip it
       if ("\L$logtab{$mname}{email}" eq $cn) {
          next;
       }
       ## already a user, skip it.
       if ("\L$logtab{$cn}" eq $cn) {
          next; 
       }
       if ($cn eq "") {
          next;
       }
       $newcontacts .= $cn;
       $newcontacts .= ",";
    }
    # hddebug "newcontacts = $newcontacts";
    return $newcontacts;
}

sub sendEventInvitations {

   ## login includes name
   my($login, $g, $subject, $dtype, $desc, $appthour, $aptmin, $meridian, $recurtype, $zone, $share, $busy, $banner, $venue, $invitees, $edhour, $edmin, $email) = @_;     
   
   $duration = $dhour . "Hrs" . " " . $dmin . "Mins";  
   $zonestr = getzonestr $zone; 

   if ($appthour >= 13) {
      $apthr = $appthour - 12;
   } else {
      if ($appthour eq "0") {
          $apthr = $appthour + 12;
      } else {
          $apthr = $appthour;
      }
   }                                    

   hddebug "desc = $desc, dtype =$dtype, share = $share, busy=$busy, time=$apthr, $aptmin, $meridian";
   $banner = adjusturl $banner;
   $pra = "";
   $pra = strapp $pra, "template=$ENV{HDTMPL}/eventinvitation.html";
   $pra = strapp $pra, "templateout=$ENV{HDHOME}/tmp/evt-$$.html";
   $pra = strapp $pra, "name=$login";
   $pra = strapp $pra, "subject=$subject";
   $pra = strapp $pra, "eventtype=$dtype";
   $pra = strapp $pra, "description=$desc";
   $pra = strapp $pra, "time=$apthr:$aptmin $meridian";
   $pra = strapp $pra, "frequency=$recurtype";
   $pra = strapp $pra, "zone=$zonestr";
   $pra = strapp $pra, "duration=$duration";
   $pra = strapp $pra, "share=$share";
   $pra = strapp $pra, "busy=$busy";
   $pra = strapp $pra, "evenue=$venue";
   $pra = strapp $pra, "banner=$banner";
   $pra = strapp $pra, "loginemail=$email";
   $pra = strapp $pra, "login=$login";
   parseIt $pra;

   (@hshinvitees) = split(" ", $invitees);

   ##
   ##"\L$addrtab{$id}{fname}  $addrtab{$id}{lname}-$addrtab{$id}{email}";   
   ##

   
   foreach $invitee (@hshinvitees) {
      hddebug "invitee = $invitee";
      ($rem, $invemail) = split("-", $invitee);
      hddebug "invemail = $invemail";
      if (!notEmailAddress($invemail)) {
         #system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/evt-$$.html -s \"$subject\" -e \"\" -t \"$invemail\" -F cronuser\@hotdiary.com";
      }
   }

}
			 

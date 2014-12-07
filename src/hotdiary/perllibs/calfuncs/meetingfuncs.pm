package calfuncs::meetingfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use calutil::calutil;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch eventDispatch isCurrentDay isCurrentMonth isCurrentYear  showMeetings getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink setMeetingEditRec setDailyPrml deleteEvent addMeeting updateMeeting setMonthlyPrml setWeeklyPrml createWeeklyImageLink createDailyImageLink createDtypeImg addCalendarPref publishEvent isCalPublic bookResource);

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $group) = @_;

   if ($a eq "d") {
      return(showMeetings($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $group, $sc ));
   }

   if ($a eq "de") {
      return(setMeetingEditRec($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $jvw, $group, $sc));
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

   my($dtype, $en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $subject, $jvw, $group, $login) = @_; 
   #hddebug "createSubjectLink ";
   $burl = $url; 
   $e = "de";

   $burl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=$f&vw=i&jvw=$jvw");

   $hr = "";
   if ($vw eq "m") {
      $hr = "<HR>";
   } 

   $hdnm = $ENV{HDDOMAIN};
   if ($vw eq "m") {

      if ($free ne "Free") {
         $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
      } else {
         $showbusy = "";
      }
      $dimg = createDtypeImg($dtype);

      $imgurl = adjusturl ("$dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"delete\"></a>");

   } else {
     $imgurl = "";
   }

   #if (($vw eq "w") || ($vw eq "d")) {
   if ($vw eq "d") {
      $br = "<BR>";
   } else {
     $br = ""; 
   } 
   
   if ($subject ne "") {
      $sublen = length($subject);
      if ($sublen > 8) {
        $etitle = substr($subject, 0, 8); 
      } else {
        $etitle = $subject;
      }
   } else { 
        $etitle = $dtype;
   }

   $hourlen = length($hour);
   if ($hourlen eq "1") {
       $hour = "&nbsp;$hour";
   }
   $noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");

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
         $addeventtop = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=u\"><IMG SRC=\"$hdnm/images/addevent.gif\" BORDER=\"0\" ALT=\"Add Event To My Personal Calendar\"></a>");  
      }
 
      if ($vw eq "w") {
         #$mybiscuit = $logsess{$login}{'biscuit'};
          
         $burlhref1 = "<a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$en&login=$login\">$etitle</a> $hour $min $meridian $noimg $imgurl $addeventtop $hr";
      } else {
         $burlhref1 = "<a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$en&login=$login\">$etitle</a> $hour $min $meridian $noimg <BR> $imgurl $addeventtop $hr";
      }
   } else {

      if ($vw eq "w") { 
         $burlhref1 = "<a href=\"$burl\">$etitle</a> $hour $min $meridian $noimg $imgurl $hr";
      } else { 
         $burlhref1 = "<a href=\"$burl\">$etitle</a> $hour $min $meridian $noimg <BR> $br $imgurl $hr";
         #hddebug("not weekly came here burlhref1 = $burlhref1");
      }
   }
   $burlhref = adjusturl($burlhref1);

   if ($vw eq "w") {
      #$imglist[$eventnum] .=  createWeeklyImageLink($en, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vw, $free, $dtype);
      $burlhref .=  createWeeklyImageLink($en, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vw, $free, $dtype);
   }

   #if ($vw eq "d") {
      #$imglist[$eventnum] .=  createDailyImageLink($en, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vw, $free, $dtype);
   #   $burlhref .=  createDailyImageLink($en, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vw, $free, $dtype);
   #}
   return $burlhref;

}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype) = @_;

   $dimg = createDtypeImg($dtype);
   $noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");
 
   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
       $showbusy = "";
   }


   $imgurl = adjusturl ("$noimg $dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a><BR><BR>");

   return $imgurl;
}


sub createWeeklyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype) = @_;

   $dimg = createDtypeImg($dtype);
   $noimg = adjusturl("<IMG SRC=\"$hdnm/images/nothing.gif\" BORDER=\"0\" WIDTH=\"30\" HEIGHT=\"30\">");

   if ($free ne "Free") {
      $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
   } else {
      $showbusy = "";
   }

   #$imgurl = adjusturl ("$noimg $dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a><BR><BR>");

   $imgurl = adjusturl ("$noimg $dimg $showbusy <a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=$f&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a><BR>");

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

sub showMeetings {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $group, $sc) = @_;

   #hddebug "showMeeting"; 

   if ($sc eq "p") { 
      if ((isCalPublic($lg)) != 1) {
         return $prml;
      }
   }    

   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
   SUFIX => '.rec',
   SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free', 
	   'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

   (-e "$ENV{HDDATA}/$lg/appttab" and -d "$ENV{HDDATA}/$lg/appttab") or return $prml;

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

	    # append the events for this eventnum.
	    $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $group, $lg);

            #if ($vwtype eq "w") {
            #   $imglist[$eventnum] .=  createWeeklyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
            #}
            if ($vwtype eq "d") {
               $imglist[$eventnum] .=  createDailyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
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
         $space = adjusturl("&nbsp;");
         $prml = strapp $prml, "evtlist$i=$space";
         $space = adjusturl("&nbsp;<BR><BR>");
         $prml = strapp $prml, "imglist$i=$space";
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

sub setMeetingEditRec {
  
   #my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw) = @_;
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw, $group, $sc) = @_;

   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
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
	       }
     return $prml;
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
                                   

   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

  
   $tfile = "$ENV{HDDATA}/$lg/apptentrytab";
   (-e "$ENV{HDDATA}/$lg/appttab" and -d "$ENV{HDDATA}/$lg/appttab") or return $prml;

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
   system "/bin/echo >$ENV{HDDATA}/$lg/apptentrytab";

   $tfile = "$ENV{HDDATA}/$lg/apptentrytab";
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

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $confirm, $id, $entryno) = @_; 

   hddebug "addMeeting, entryno = $entryno";
   if ($entryno eq "") {
      return;
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

       -d "$ENV{HDDATA}/listed/groups/$group/appttab or return";
   } else {
     # bind personal appt table vars
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   }

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
   $appttab{$entryno}{'confirm'} = $confirm;
   $appttab{$entryno}{'entryno'} = trim $entryno;
   $appttab{$entryno}{'id'} = $id;
   $appttab{$entryno}{'type'} = "meeting";

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

   tied(%appttab)->sync();

   if ($econtact ne "") {
      regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
}

sub updateMeeting  {

   #my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $econtact) = @_; 

   my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $confirm, $id) = @_; 

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
     DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
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
      $appttab{$entryno}{'confirm'} = $confirm;
      $appttab{$entryno}{'entryno'} = trim $entryno;
      $appttab{$entryno}{'confirm'} = trim $confirm;
      $appttab{$entryno}{'id'} = $id;
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


sub publishEvent {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $group) = @_;

   if ((isCalPublic($lg)) != 1) {
      return $prml;
   };
   #status("publish calendar ");


   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
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
               if ($appttab{$onekey}{'share'} eq "Private") {
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

                 # append the events for this eventnum.
                 $events[$eventnum] .= createSubjectLink($dtype, $onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $subject, $jvw, $group, $lg);

                 if ($vwtype eq "w") {
                    $imglist[$eventnum] .=  createWeeklyImageLink($onekey, $url, $hour, $min, $meridian, $day, $month, $year, $f, $vwtype, $free, $dtype);
                  }
                  if ($vwtype eq "d") {
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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remotead
dr', 'informme', 'cserver', 'zone', 'calpublish'] };

    $cntr = 0;
    foreach $cn (@hshemail) {
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
             hddebug "login = $login";
	  }
       }
       #if (!exists ($logtab{$login} )) {
          if ($eemail ne "1") {
             $logtab{$login}{'login'} = $login;
             $logtab{$login}{'fname'} = $login;
             $logtab{$login}{'password'} = $login;
             $logtab{$login}{'email'} = $cn;
             $logtab{$login}{'zone'} = $logtab{$mname}{zone};
             # bind surveytab table vars
            # tie %surveytab, 'AsciiDB::TagFile',
            #   DIRECTORY => "$ENV{HDDATA}/surveytab",
            #   SUFIX => '.rec',
            #   SCHEMA => {
            #   ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite'] };
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

          qx{echo \"$emsg\" > /var/tmp/reginviteletter$$};
          qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login}{email} < /var/tmp/reginviteletter$$};

          if ($eemail ne "1") {
             system "/bin/mkdir -p $ENV{HDREP}/$login";
             system "/bin/chmod 755 $ENV{HDREP}/$login";
             system "/bin/mkdir -p $ENV{HDHOME}/rep/$login";
             system "/bin/mkdir -p $ENV{HDDATA}/$login";
             system "/bin/chmod 755 $ENV{HDDATA}/$login";
             system "/bin/touch $ENV{HDDATA}/$login/addrentrytab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/addrentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$login/addrtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/addrtab";
             system "/bin/touch $ENV{HDDATA}/$login/apptentrytab";
             system "/bin/chmod 660 $ENV{HDDATA}/$login/apptentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$login/appttab";
             system "/bin/chmod 770 $ENV{HDDATA}/$login/appttab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/personal/pgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/founded/fgrouptab";
             system "/bin/chmod -R 770 $ENV{HDDATA}/groups/$login";
             system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";
             system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$login";
             system "/bin/chmod 775 $ENV{HDDATA}/$login/calendar_events.txt";

             system "/bin/mkdir -p $ENV{HDDATA}/$login/faxtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/faxtab";

             system "/bin/mkdir -p $ENV{HDDATA}/$login/faxdeptab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/faxdeptab";
          }

          hddebug "entryno = $entryno";
	  if ( (($eemail eq "1") && ($logtab{$login}{checkid} eq "CHECKED") ) || ($eemail ne "1") ) {
             if ($g eq "") {
                 system "/bin/cp $ENV{HDDATA}/$mname/appttab/$entryno.rec $ENV{HDDATA}/$login/appttab/$entryno.rec";

                 #add the entry in the apptentrytab
                 $tfile = "$ENV{HDDATA}/$login/apptentrytab";
                 open thandle, ">>$tfile";
                 printf thandle "%s\n", $entryno;
                 close thandle;
             } else {
                 system "/bin/cp $ENV{HDDATA}/listed/groups/$g/appttab/$entryno.rec $ENV{HDDATA}/$login/appttab/$entryno.rec";
             }
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
      #}
   }

#synch the database
   tied(%logtab)->sync();
}

sub addGroupEventToMyCal {

   my($en, $login, $group) = @_;

   if ($login ne "") {
     # bind personal appt table vars
     tie %appttab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$login/appttab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject',  'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
   }

   $entryno = getkeys(); 
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
   $tfile = "$ENV{HDDATA}/$login/apptentrytab";
   open thandle, ">>$tfile";
   printf thandle "%s\n", $entryno;
   close thandle;

   tied(%appttab)->sync();
   return 1;

} 

sub bookResource {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $bizres, $organizer, $entryno, $business) = @_;

   ($prefix, $resinfo) = split("Resource-", $bizres);
   ($biz, $resname) = split(":", $resinfo);

   if (-d("$ENV{HDDATA}/business/business/$biz/restab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$biz/resources/$resname";
      system "chmod 755 $ENV{HDDATA}/business/business/$biz/resources/$resname";

      if (-d("$ENV{HDDATA}/business/business/$biz/resources/$resname")) {
         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$biz/resources/$resname/appttab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
                 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };

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
        $appttab{$entryno}{'entryno'} = trim $entryno;
        $appttab{$entryno}{'id'} = $business;
        $appttab{$entryno}{'person'} = $organizer;

        tied(%appttab)->sync();
      }
   }
}


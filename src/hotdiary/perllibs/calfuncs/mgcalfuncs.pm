package calfuncs::mgcalfuncs;
require Exporter;
require "flush.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use mgcalutil::mgcalutil;


@ISA = qw(Exporter);
@EXPORT = qw(dispatch isCurrentDay isCurrentMonth isCurrentYear  showEvents getEventDate getEventZone getDailyAMEventNumber getDailyPMEventNumber getDailyEventNum createSubjectLink showOneEvent setDailyPrml setMonthlyPrml setWeeklyPrml createWeeklyImageLink createDailyImageLink showTodos createTodoLink createTodoWeeklyImageLink createTodoDailyImageLink setTodoDailyPrml setTodoMonthlyPrml setTodoWeeklyPrml createDtypeImg isCalPublic addGroupEventToMyCal displayDetails showOneTodo);

sub dispatch {

   my($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $m, $login, $url, $en, $jvw, $sc, $group) = @_;

   #hddebug "mgcalfuncs::dispatch";
   if ($f eq "t") {
      if ($a eq "d") {
         return(showTodos($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $group, $sc));
      }
      if ($a eq "de") {
        return(showOneTodo($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $group));   }
   }

   if ($f eq "e") {
      if ($a eq "d") {
         return(showEvents($prml, $dy, $mo, $yr, $login, $url, $vw, $f, $jvw, $group, $sc ));
      }
      if ($a eq "de") {
         return(showOneEvent($prml, $dy, $mo, $yr, $login, $url, $vw, $en, $f, $jvw, $group, $sc));
      } 
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
   $imgurl = "";


   if ($subject ne "") {
     $etitle = $subject;
   } else {
     $etitle = $dtype;
   }

   $hourlen = length($hour);
   if ($hourlen eq "1") {
       $hour = "&nbsp;$hour";
   }

   #bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed', 'groups', 'logins' ] };

   if ( ($group ne "") && (exists $lmergetab{$group}) && ($lmergetab{$group}{ctype} eq "Community") ) {
      if ($login eq "") {
         $addeventtop = "";
      } else {
         $addeventtop = adjusturl ("<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=u\"><IMG SRC=\"$hdnm/images/addevent.gif\" BORDER=\"0\" ALT=\"Add Event To My Personal Calendar\"></a>");
      }
      if ($lmergetab{$group}{ctype} eq "Community") {
         $imgurl = "";
      }
      $burlhref1 = "<CENTER><a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$en&login=$login\">$login $group $etitle</a> <BR>$desc <BR>$hour $min $meridian <BR> $imgurl $addeventtop </CENTER> $hr";
   }  else {
   
      if ($login ne "") {
         $login = "<B>Login $login</B>";
      } else {
         $group = "<B>Group $group</B>";
      }   
      $burlhref1 = "<CENTER>$login $group<BR>$etitle <BR>$desc <BR>$hour $min $meridian <BR> $imgurl </CENTER> $hr";
   }
   $burlhref = adjusturl($burlhref1);

   return $burlhref;
}


sub createDailyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $group, $sc) = @_;

   if (($group ne "") && (exists $lmergetab{$group}) && ($lmergetab{$group}{ctype} eq "Community") ) {
      $showbusy = "";
      $delimg = "";
      $dimg = "";
   } 
   else {
      if ($free ne "Free") {
        $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
      } else {
       $showbusy = "";
      }
   }

   ### donot show delete images
   #   $dimg = createDtypeImg($dtype);
   #   if ($sc eq "p") {
   #      $delimg = "";
   #   } else {
   #      $delimg = "<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a>";
   #   }

   $imgurl = adjusturl ("$dimg $showbusy $delimg<BR><BR>");
   return $imgurl;
}


sub createWeeklyImageLink {

   my($en, $url, $hour, $min, $meridian, $day, $month, $year,$f, $vw, $free, $dtype, $group) = @_;


   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed', 'groups', 'logins' ] };

   if (($group ne "") && (exists $lmergetab{$group}) && ($lmergetab{$group}{ctype} eq "Community") ) {
      $showbusy = "";
      $delimg = "";
      $dimg = "";
   } else {
      if ($free ne "Free") {
         $showbusy = "<IMG SRC=\"$hdnm/images/showbusy.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\" ALT=\"show busy\">";
      } else {
         $showbusy = "";
      }
   }
  
   #   $dimg = createDtypeImg($dtype);
   #   $delimg = "<a href=\"$url&vw=$vw&dy=$day&mo=$month&yr=$year&h=$hour&m=$meridian&en=$en&f=e&a=r\"><IMG SRC=\"$hdnm/images/delevt.gif\" BORDER=\"0\" WIDTH=\"20\" HEIGHT=\"20\"></a>";
   

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
sub showEvents {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $g, $sc) = @_;
  
   #hddebug "mgcalfuncs::showEvents"; 
   #hddebug "$sc, $g"; 

   $events = initializeEvents($numevents);
   $imglist = initializeImageList($numevents);

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

   #bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed', 'groups', 'logins'] };

   if ($sc eq "p") {
      if (isCalPublic($g) != 1) {
         return $prml;
      }
   }

   #hddebug "logins = $lmergetab{$g}{logins}";
   if (exists($lmergetab{$g})) {
      $prml = setEventGroupDisplays($prml, $cday, $cmonth, $cyear, $url, $vwtype, $f, $jvw, $lmergetab{$g}{groups}, $sc, $newgroups); 

      $prml = setEventLoginDisplays($prml, $cday, $cmonth, $cyear, $url, $vwtype, $f, $jvw, $lmergetab{$g}{logins}, $sc); 
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

sub setEventLoginDisplays {

   my($prml, $cday, $cmonth, $cyear, $url, $vwtype, $f, $jvw, $logins, $sc) = @_;

   #hddebug "mgcalclient::setEventLogins, logins=$logins, $cday, $cmonth, $cyear";

   $group = "";
   if ($logins ne "") {
      (@hshlogins) = split(" ", $logins);
   } else {
      return $prml;
   }


   foreach $lg (@hshlogins) {
     $alpha = substr $lg, 0, 1;
     $alpha = $alpha . '-index';
     if ($lg ne "") { 
      if (!-d "$ENV{HDDATA}/$alpha/$lg/appttab") {
          next;
      } 
      # bind login appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/appttab",
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
	          if ((mgcalutil::mgcalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
	                $eventnum = mgcalutil::mgcalutil::getWeekDayIndex($day, $month, $year);
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

      if ($vwtype eq "d") {
         $prml = setDailyPrml($prml, $events, $numevents, $imglist);
      }  

      if ($vwtype eq "m") { 
         $prml = setMonthlyPrml($prml, $events, $numevents);
      }

      if ($vwtype eq "w") {
         $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);
      }
    }
  }
  return $prml;
}


sub setEventGroupDisplays {
   my($prml, $cday, $cmonth, $cyear, $url, $vwtype, $f, $jvw, $groups, $sc) = @_;

   if ($groups ne "") {
      (@hshgroups) = split(" ", $groups);
   } else {
      return $prml;
   }

   $lg = "";
   $newgroups = "";
   foreach $group (@hshgroups) {
     if ($group ne "") { 
      if (!-d "$ENV{HDDATA}/listed/groups/$group/appttab") {
          next;
      } 
      $newgroups .= "$group ";	
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
                                                                  
     (@records) = sort keys %appttab;
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
	          if ((mgcalutil::mgcalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
	                $eventnum = mgcalutil::mgcalutil::getWeekDayIndex($day, $month, $year);
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

      if ($vwtype eq "d") {
         $prml = setDailyPrml($prml, $events, $numevents, $imglist);
      }  

      if ($vwtype eq "m") { 
         $prml = setMonthlyPrml($prml, $events, $numevents);
      }

      if ($vwtype eq "w") {
         $prml = setWeeklyPrml($prml, $events, $numevents, $imglist);
      }
    }
  }
  return $prml;
}

sub setDailyPrml {
   my($prml, $events, $numevents, $imglist) = @_;
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


sub showOneEvent {
  
   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $jvw, $group, $sc) = @_;

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
                        
sub showTodos {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $f, $jvw, $group, $sc) = @_;
   
   #hddebug "group = $group";

   #bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed', 'groups', 'logins'] };

   if (!exists($lmergetab{$group})) {
      return $prml;
   }

   if ($sc eq "p") {
      if (isCalPublic($group) != 1) {
	 #hddebug "came here";
         return $prml;
      }
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

   $prml = displayTodoLogins($prml, $cday, $cmonth, $cyear, $lmergetab{$group}{logins}, $url, $vwtype, $f, $jvw, $sc); 
   $prml = displayTodoGroups($prml, $cday, $cmonth, $cyear, $lmergetab{$group}{groups}, $url, $vwtype, $f, $jvw, $sc); 

}


sub displayTodoLogins {

   my($prml, $cday, $cmonth, $cyear, $logins, $url, $vwtype, $f, $jvw, $sc) = @_;

   if ($logins eq "") {
       return $prml;
   }
   (@hshlogins) = split(" ", $logins);
   
   foreach $lg (@hshlogins) {
       $alpha = substr $lg, 0, 1;
       $alpha = $alpha . '-index';

       if (!-d "$ENV{HDDATA}/$alpha/$lg/todotab") { 
           next;
       }
       # bind todo table vars
       tie %todotab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/$alpha/$lg/todotab",
       SUFIX => '.rec',
       SCHEMA => {
            ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
              'day', 'year', 'meridian', 'priority', 'status', 'share', 
              'hour', 'banner'] };
      

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
                if ((mgcalutil::mgcalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
                      $todonum = mgcalutil::mgcalutil::getWeekDayIndex($day, $month, $year);
                   }
                }
             }

	
             # append the todos for this todonum 
             $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, $sc, "", $lg);
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

sub displayTodoGroups {

   my($prml, $cday, $cmonth, $cyear, $groups, $url, $vwtype, $f, $jvw, $sc) = @_;

   if ($groups eq "") {
       return $prml;
   }
   (@hshgroups) = split(" ", $groups);

   foreach $group (@hshgroups) {
      if ( !-d "$ENV{HDDATA}/listed/groups/$group/todotab") {
         next;
      }
      # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share', 
           'hour', 'banner'] };

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
                if ((mgcalutil::mgcalutil::isDayInWeek($day, $month, $year, $cday, $cmonth, $cyear)) != 1) {
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
                      $todonum = mgcalutil::mgcalutil::getWeekDayIndex($day, $month, $year);
                   }
                }
             }

             # append the todos for this todonum 
             $todos[$todonum] .= createTodoLink($onekey, $url, $hour, $meridian, $day, $month, $year, $f, $vwtype, $subject, $todmntcnt, $priority, $todotab{$onekey}{desc}, $sc, $group, "");
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

   my($en, $url, $hour, $meridian, $day, $month, $year, $f, $vw, $subject, $todomntcnt, $priority, $desc, $sc, $group, $login) = @_;

   $hdnm = $ENV{HDDOMAIN};

   $todourl = $url;
   $e = "de";

   $todourl = adjusturl("$url&en=$en&a=$e&dy=$day&mo=$month&yr=$year&f=t&vw=i");

   $hr = "<HR>";

   $todoimgurl = "";

   $pri = " Priority ";
   if ($subject ne "") {
      $todotitle = "$subject$pri$priority";
   } else {
      $todotitle = "Todo$pri$priority";
   }

   if ($login ne "") {
     $login = "<B>Login $login</B>";
   }
   if ($group ne "") {
     $group = "<B>Group $group</B>";
   }
   $burlhref1 = "<CENTER>$login $group <BR> $todotitle <BR>$desc <BR>$hour $meridian <BR> $todoimgurl <BR></CENTER> $hr";
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


sub showOneTodo {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $group) = @_;
   #print "entryno = $ceno \n";             

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

sub isCalPublic {

   my($mgroup) = @_;

   #bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
              'listed', 'groups', 'logins' ] };

   $mgroup = trim $mgroup;
   if (exists($lmergetab{$mgroup})) {
      if ($lmergetab{$mgroup}{cpublish} eq "on") {
         return 1;
      } 
   }
   return 0;
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


   if ($login ne "") {
      $alpha = substr $login, 0, 1;
      $alpha = $alpha . '-index';

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

sub displayDetails {

   my($prml, $cday, $cmonth, $cyear, $lg, $url, $vwtype, $ceno, $f, $group) = @_;

   #hddebug "displayDetails";
   $onekey = $ceno;

   $prml = strapp $prml, "subdetails=$subject";
   $app_tab = 0;
   $todo_tab = 0;

   # bind todo table vars
   $alpha = substr $lg, 0, 1;
   $alpha = $alpha . '-index';


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
         $subject = "Details: $todotab{$onekey}{'subject'}<BR><BR> Description: $todotab{$onekey}{'desc'}<BR><BR> $todotab{$onekey}{venue}";
         #$subject .= "$todotab{$onekey}{'desc'}";
         $subject .= "User: $lg <BR> $subject_d";
         $subject = adjusturl $subject;
         #hddebug "subject = $subject";
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
            $subject .= "Venue: <BR>$appttab{$onekey}{venue}";
            $subject = adjusturl $subject;
            $prml = strapp $prml, "subdetails=$subject";
            $prml = strapp $prml, "evtbanner=$evtbanner";
            return $prml;
         }

         $subject = "Details: $appttab{$onekey}{'subject'}<BR><BR> Description: $appttab{$onekey}{'desc'}<BR><BR> Venue: $appttab{$onekey}{venue}";

         $subject = adjusturl $subject;
         $prml = strapp $prml, "subdetails=$subject";
         $prml = strapp $prml, "evtbanner=$evtbanner";
         return $prml;
      }
   }

   return $prml;
}


			 

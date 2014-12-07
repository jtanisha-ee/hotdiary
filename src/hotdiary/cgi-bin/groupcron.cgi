#!/usr/bin/perl
#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: groupcron.cgi
# Purpose: it searches for appointments and sends out email/fax/pager 
# from cron.      
# Creation Date: 02-04-98 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{

# bind personal appointment table vars
#   tie %appttab, 'AsciiDB::TagFile',
#   DIRECTORY => "$ENV{HDDATA}/appttab",
#   SUFIX => '.rec', 
#   SCHEMA => { 
#   	ORDER => ['entryno', 'login', 'month', 'day', 'year', 
#	'hour', 'min', 'sec', 'meridian', 'dhour', 'dmin',
#        'dtype', 'atype', 'desc', 'zone', 'recurtype'] };


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

## bind cntrtab table vars
   #tie %cntrtab, 'AsciiDB::TagFile',
   #DIRECTORY => "$ENV{HDDATA}/cntrtab",
   #SUFIX => '.rec',
   #SCHEMA => {
        #ORDER => ['counter'] };



    # get the login name of each hotdiary user.
    # open the user's login apptentrytab. 
    # check in their apptentrytab if there are any entry numbers
    # search for each entry in the appointment entry tab
    # look for the entry numbers that are current or relevant   

    # bind lgrouptab table vars
    tie %lgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc' , 'password', 'ctype', 'cpublish', 'corg',
                  'listed' ] };      

    $blocklist = qx{cat $ENV{HDDATA}/blocktab/blocktab.rec};

    foreach $gname (keys %lgrouptab) {
      $gname = trim $gname;

      if ($lgrouptab{$gname}{ctype} eq "Community") {
         next;
      }
     (-e "$ENV{HDDATA}/listed/groups/$gname/appttab" and -d "$ENV{HDDATA}/listed/groups/$gname/appttab") or next;
      
      # bind group appointment table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$gname/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'sec', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',  'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id',
         'type'] };

      (@records) = sort keys %appttab;
      for ($y = 0; $y <= $#records; $y = $y+1) {
         $onekey = $records[$y];
         if ($onekey ne "")  {
	    if (exists $appttab{$onekey}) { 
	       if ($appttab{$onekey}{atype} ne "DontSendMeReminder") {

               $apptmonth = $appttab{$onekey}{'month'};
               $apptday = $appttab{$onekey}{'day'};
               $apptyear = $appttab{$onekey}{'year'};
               $apptmin = $appttab{$onekey}{'min'};
               $apptsec = $appttab{$onekey}{'sec'};
               $appthour = $appttab{$onekey}{'hour'};
               $meridian = $appttab{$onekey}{'meridian'};
               $apptzone = $appttab{$onekey}{'zone'};
	       $apptzone = adjustzone($apptzone);
	       $recurtype = $appttab{$onekey}{'recurtype'};
               if ( ($meridian eq "PM") && ($appthour ne "12")) {
                   $appthour += 12;
               }
               if (($meridian eq "AM") && ($appthour eq "12")){
                   $appthour = 0;
               }

               $ctime = ctimetosec();
               $etime = 0;

               # check if current year is less than appt year
               # then we don't send reminder for daily, weekly, annually 

               # scenario 2
               # check if current year is same as appt year
               # if the year is same, check if current month is
               # same or greater than the apptmonth.
               # if the current month is same as apptmonth, check
               # if the current day is greater than apptday.
               # if all the above conditions are met, then send the reminder
               # for daily.
               
               # scenario 3
               # check if the current year is greater than appt year
               # then send the reminder for daily.

               # take current month, current year, current day, 
               # take user's time, user's zone for etimetosec(); 

               if ($appttab{$onekey}{'recurtype'} eq "Once") {
                   #print "entered once\n";
                   $etime = etimetosec($apptsec, $apptmin, $appthour, $apptday, $apptmonth, $apptyear, "", "", "", $apptzone); 
               }


               # comparisons are always in GMT
               if ($appttab{$onekey}{'recurtype'} ne "Once") {

                   #print "recurtype = $appttab{$onekey}{'recurtype'} \n";

                   #print "apptsec = $apptsec\n";
                   #print "apptmin = $apptmin\n";
                   #print "appthour = $appthour\n";
                   #print "apptday = $apptday\n";
                   #print "apptmonth = $apptmonth\n";
                   #print "apptyear = $apptyear\n";
                   #print "apptzone = $apptzone\n";
                   $chktime = etimetosec($apptsec, $apptmin, $appthour, $apptday, $apptmonth, $apptyear, "", "", "", $apptzone); 

                   #print "checktime = $chktime \n";

                   (@values) = getMoYrDy($chktime);
                   ($gmapt_mon, $gmapt_year, $gmapt_day, $gmapt_wk) = (@values); 

                   ($gmcur_mon, $gmcur_year, $gmcur_day, $gmcur_wk) = getMoYrDy($ctime);

                   #print "appt month =  $gmapt_mon \n";
                   #print "appt year =  $gmapt_year \n";
                   #print "appt day = $gmapt_day \n";
                   #print "appt wk =  $gmapt_wk \n";
                   #print "cur year = $gmcur_year \n";
                   #print "cur day =  $gmcur_day \n";
                   #print "cur wk =  $gmcur_wk \n";
                  #
                   # if the current year is less than appointment year
                   # if the current year is less than appointment year
                   if ($gmcur_year < $gmapt_year) {
                      next;
                   }

                   # if the appt is in the same year, but the current month
                   # is less than the appt month. 
                   if (($gmcur_year == $gmapt_year) &&
                       ($gmcur_mon < $gmapt_mon)) {
                      next;
                   }
               }

               if ($appttab{$onekey}{'recurtype'} eq "Daily") {

                   # for daily, if current year is >= to appt year.
                   # if current year is equal to appt year, check if month
                   # is >= than appt month and current day is greater than apt day.
                   if ($gmcur_year == $gmapt_year) {
                      if ($gmcur_mon == $gmapt_mon) {
                         if ($gmcur_day < $gmapt_day) {
                            next;
                         }
                      } else {
                         if ($gmcur_mon < $gmapt_mon) {
                            next;
                         }
                      }
                   } else {
                      if ($gmcur_year < $gmapt_year) {
                         next;
                      }
                   }
                   #if (($gmcur_year == $gmapt_year) &&
                      #($gmcur_mon == $gmapt_mon) && 
                      #($gmcur_day < $gmapt_day)) {
                      #next;
                   #}
                   #print "entered daily \n";

                   $etime = getdailyEtime($apptsec, $apptmin, $appthour, $apptzone);
                   #print "etime = $etime\n";
               }

            
               if ($appttab{$onekey}{'recurtype'} eq "Weekly") {
                 #print "entered weekly\n";
                 if ($gmcur_year == $gmapt_year) {
                    if ($gmcur_mon == $gmapt_mon) {
                       if ($gmcur_day >= $gmapt_day) {
                          if ($gmcur_wk != $gmapt_wk) {
                             next;
                          }
                       } else {
                          next;
                       }
                    } else {
                       if ($gmcur_mon > $gmapt_mon) {
                          if ($gmcur_wk != $gmapt_wk) {
                             next;
                          }
                       } else {
                          next;
                       }
                    }
                 } else {
                    if ($gmcur_year > $gmapt_year) {
                       if ($gmcur_wk != $gmapt_wk) {
                          next;
                       }
                    } else {
                       next;
                    }
                 }

                 #if (($gmcur_year >= $gmapt_year) &&
                    #($gmcur_mon >= $gmapt_mon) &&
                    #($gmcur_wk != $gmapt_wk)) {
                    #next;
                 #}

                 $etime = getdailyEtime($apptsec, $apptmin, $appthour, $apptzone);
                 #print "etime = $etime\n";
               }
 

               # for monthly, current year can be >= to appt year
               # If current year is greater than appt year, current day must be
               # equal to appt day.
               # if current year is equal to appt year, current month should be
               # greater than appt month and current day must be equal to appt day.
               #
               if ($appttab{$onekey}{'recurtype'} eq "Monthly") {
                 #print "entered monthly\n";
                 if ($gmcur_year == $gmapt_year) {
                    if ($gmcur_mon >= $gmapt_mon) {
                       if ($gmcur_day != $gmapt_day) {
                          next;
                       }
                    } else {
                       next;
                    }
                 } else {
                    if ($gmcur_year > $gmapt_year) {
                       if ($gmcur_day != $gmapt_day) {
                          next;
                       }
                    } else {
                       next;
                    }
                 }
                 #if (($gmcur_year == $gmapt_year) &&
                 #   ($gmcur_mon >= $gmapt_mon) && 
                 #   ($gmcur_day != $gmapt_day)) {
                 #   next;
                 #}

                 $etime = getdailyEtime($apptsec, $apptmin, $appthour, $apptzone);
                 #print "etime = $etime\n";
               }

               # for annually, current year should be greater than appt year.
               # current month should be same as appt month
               # current day should be same as appt day
               if ($appttab{$onekey}{'recurtype'} eq "Yearly") {
                 #print "entered Yearly\n";
                 if ($gmcur_year == $gmapt_year) {
                    if ($gmcur_mon == $gmapt_mon) {
                       if ($gmcur_day != $gmapt_day) {
                          next;
                       }
                    } else {
                       next;
                    }
                 } else {
                    if ($gmcur_year > $gmapt_year) {
                       if ($gmcur_mon != $gmapt_mon) {
                          next;
                       } else {
                          if ($gmcur_day != $gmapt_day) {
                             next;
                          }
                       }
                    } else {
                       next;
                    }
                 }
                 #if (($gmcur_year > $gmapt_year) &&
                    #($gmcur_mon != $gmapt_mon)) { 
                    #next;
                 #}
#
                 #if (($gmcur_year > $gmapt_year) &&
                    #($gmcur_mon == $gmapt_mon) &&
                    #($gmcur_day != $gmapt_day)) { 
                    #next;
                 #}

                 $etime = getdailyEtime($apptsec, $apptmin, $appthour, $apptzone);
                 #print "etime = $etime\n";
               }
           
               # we need to check for "Onlyonce", "everyday", 
               # "weekly", monthly,annually 
               # calculate day of the appt. and get the matching day of the week.
               # monthly, just calculate the number of hours 
               if (isaptcurrent($ctime, $etime)) { 
                  $dtype = $appttab{$onekey}{'dtype'}; 
                  $dtype =~ s/\n/\n<BR>/g;
                  $atype = $appttab{$onekey}{'atype'}; 
                  $atype =~ s/\n/\n<BR>/g;

                  $recurtype = $appttab{$onekey}{'recurtype'}; 
                  $recurtype =~ s/\n/\n<BR>/g;

                  $desc = $appttab{$onekey}{'desc'};
                  
                  ($mfile = "$ENV{HDHOME}/tmp/grouptcron$$.txt") =~ s/\n/\n<BR>/g;
                  #printf mhandle "Date: $apptmonth-$apptday-$apptyear\n";
                  if ($appthour >= 13) {
                     $apthr = $appthour - 12;
                  } else {
                     if ($appthour eq "0") {
                       $apthr = $appthour + 12;
                     } else {
                       $apthr = $appthour;

                     }
                  }
                  $founder = $lgrouptab{$gname}{'groupfounder'};
                  $n = 0; 
                  print "Group Name: $gname\n";
                  print "Group Founder: $founder\n";

                  # bind founded group table vars
                  tie %usertab, 'AsciiDB::TagFile',
                  DIRECTORY => "$ENV{HDDATA}/listed/groups/$gname/usertab",
                  SUFIX => '.rec',
                  SCHEMA => {
                  ORDER => ['login'] };     

		  foreach $t (keys %usertab) {
                     $t = trim $t;
                     (-e "$ENV{HDDATA}/logtab/$t.rec" and -d "$ENV{HDDATA}/logtab") or next;
	             $records[$n] = $t;
                     $n = $n + 1;
                  } 
                  $records[$n] = $founder;
                  for ($z = 0; $z <= $n; $z = $z + 1) {
                     $uname = $records[$z];     
		     print "-----Group Member: $uname \n";
                     print "-----Entry Number: $onekey \n";
		     print "-----Group Reminder Event: Date: $apptmonth-$apptday-$apptyear \n";
                     print "-----Group Reminder Event: Time: $apthr:$apptmin $meridian\n";
                  if (!exists $logtab{$uname}) {
	             next;
                  }
                  #$toname = $logtab{$uname}{'fname'};
                  #if ($toname eq "") {
                     #$toname = "HotDiary Member";
                  #}
                  #system "rm -f $ENV{HDHOME}/tmp/grouptcron$$.txt";
                  #open mhandle, ">$mfile";
                  #printf mhandle "Dear $toname,\n\n";
                  ##printf mhandle "Your appointment is due. Please read the notes below for details.\n\n";
                  ##printf mhandle "Regards\n";
                  ##printf mhandle "HotDiary Inc.\n\n";
                  #printf mhandle "Your Group Reminder Follows:\n\n";
                  #printf mhandle "Date: $apptmonth-$apptday-$apptyear\n";
                  #printf mhandle "Time: $apthr:$apptmin $meridian\n";
                  #printf mhandle "Reminder Type: $dtype \n";
                  #printf mhandle "Description: %s\n", $desc;
                  #printf mhandle "Frequency: %s\n", $recurtype;
                  #printf mhandle "\nHotDiary - New Generation Internet Organizer, http://www.hotdiary.com";
                  #&flush(mhandle);

                  $busy = $appttab{$onekey}{'free'};
                  $zone = $appttab{$onekey}{'zone'};
                  $zone = getzonestr $zone;
                  $duration = $appttab{$onekey}{'dhour'} . "Hrs";
                  $dmin = $appttab{$onekey}{'dmin'};
                  if ($dmin eq "") {
                     $dmin = "0";
                  }
                  $duration .= " " . $dmin . "Mins";
                  $share = $appttab{$onekey}{'share'};
                  $banner = adjusturl $appttab{$onekey}{'banner'};
                  $prml = "";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/groupreminder.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/groupreminder-$uname$$.html";
                  $prml = strapp $prml, "group=$gname";
                  $prml = strapp $prml, "founder=$founder";
                  $femail = $logtab{$founder}{email};
                  $members = "";
		  foreach $t1 (keys %usertab) {
                    $members .= $t1 . ' ';
                  }
                  $prml = strapp $prml, "members=$members";
                  $prml = strapp $prml, "login=$uname";
                  $prml = strapp $prml, "email=$email";
                  $esubject = $appttab{$onekey}{subject};
                  $prml = strapp $prml, "subject=$esubject";
                  $dtype = $appttab{$onekey}{dtype};
                  $prml = strapp $prml, "eventtype=$dtype";
                  $desc = $appttab{$onekey}{desc};
                  $prml = strapp $prml, "description=$desc";
                  $prml = strapp $prml, "time=$apthr:$apptmin $meridian";
                  $prml = strapp $prml, "frequency=$recurtype";
                  $prml = strapp $prml, "zone=$zone";
                  $prml = strapp $prml, "duration=$duration";
                  $prml = strapp $prml, "share=$share";
                  $prml = strapp $prml, "busy=$busy";
                  $prml = strapp $prml, "banner=$banner";
                  parseIt $prml;
                  #$counter = $cntrtab{'apptcounter'}{'counter'} + 1;
                  #if (($counter % $ENV{'USE_APPT_WINNER_FREQ'}) == 0) { 
                     #$login = $uname;
                     #$email = $logtab{$login}{'email'};
                     #system "cat $ENV{'HDHOME'}/letters/apptwinner > $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     #system "echo \"Entry Number  $onekey\" >> $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     #if ($email ne "") {
                        #system "/bin/mail -s \"Did you just win a Prize!\" $email < $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     #}
                  #}
                  #$cntrtab{'apptcounter'}{'counter'} = $counter;
                  #tied(%cntrtab)->sync();
                  #
                  # send email to user
                  #
                  if ($atype eq "Email") {
                    $login = $uname;
		    #print "login =", $login, "\n";
                    if (exists $logtab{$login}) {
		      #print "entered login exists \n";
                      $email = $logtab{$login}{'email'};
                      #print "$login email = ",  $email, "\n";
                      if ($email ne "") {
                         #system "/bin/mail -s \"$dtype\" $email < $mfile";
                         #system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/groupreminder-$login$$.html -s \"$esubject\" -e \"\" -t \"$email\" -F cronuser\@hotdiary.com";
                         if ($femail eq "") {
                            $femail = "rhsup\@hotdiary.com";
                         }
                         if (!($blocklist =~ /$email/)) {
                            system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/groupreminder-$login$$.html -s \"$esubject\" -e \"\" -t \"$email\" -F $femail";
                         }
                      }
                    } #else
                  } else {
                    if ($atype eq "Pager") {
                       $login = $uname;
                       if (exists $logtab{$login}) {
                          #print "Entered Pager type"; 
                          $pager = $logtab{$login}{'pager'}; 
                          $from = $logtab{$login}{'fname'};
			  $pagertype = $logtab{$login}{'pagertype'};
                          $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                          $pagerfile = "$ENV{HDHOME}/tmp/$login$$";
                          qx{echo \"$message\" > $pagerfile};
			  if ("\U$pagertype" eq "\USkyTel Pager") {
                            system "java COM.hotdiary.main.SendPage \"$pager\" \"$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
	                  } else {
                               $pager = getPhoneDigits $pager;
			       if ("\U$pagertype" eq "\UAirTouch Pager") {
				  $email = "$pager\@airtouch.net"; 
                                  if (!($blocklist =~ /$email/)) {
                                     system "/bin/mail -s \"$from\" $email < $pagerfile";
                                  }
			       } else {
                                    if ("\U$pagertype" eq "\UNextel Pager") {
                                       $email = "$pager\@page.nextel.com"; 
                                       if (!($blocklist =~ /$email/)) {
                                          system "/bin/mail -s \"$from\" $email < $pagerfile";
                                       }
                                    } else {
                                       if ("\U$pagertype" eq "\UPageMart Pager") {
                                          $email = "$pager\@pagemart.net"; 
                                          if (!($blocklist =~ /$email/)) {
                                             system "/bin/mail -s \"$from\" $email < $pagerfile";
                                          }
                                       } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
       $message = trim $message;
       $message =~ s/\s/\+/g;
       $url = "http://www.metrocall.com/cgi-bin/rbox/default.cgi?TO=$pager&Message=\"$message\"";
       system "java COM.hotdiary.main.ExecCGIURL \"$url\"";
    } else {
    if ("\U$pagertype" eq "\UOther Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
       $otherpagerfile = "$ENV{HDHOME}/tmp/$login$otherpager$$";
       qx{echo \"$message\" > $otherpagerfile};
       ($user, $domain) = split "\@", $pager;
       if ((trim($user) ne "") && (trim($domain) ne "")) {
          $email = "$pager"; 
       } else {
            qx{echo \"For Other Pager type, your pager field must contain a valid email address. Could not deliver message to your pager. Sending an email message instead.\" >> $otherpagerfile};
            $email = $logtab{$login}{'email'};
       }
       if (!($blocklist =~ /$email/)) {
          system "/bin/mail -s \"$from\" $email < $otherpagerfile";
       }
    }
    }
    } 
                                       }
                                    }
			       }
                          }
                       }
                    }
                  }
                }
	       } #dontremindme 
	      }
           }
        }
   }


# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   #tied(%appttab)->sync();
   #tied(%logtab)->sync();
   #print "end of appt cron cgi file \n";
}

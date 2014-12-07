#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: apptcron.cgi
# Purpose: it searches for appointments and sends out email/fax/pager 
# from cron.      
# Creation Date: 02-04-98 
# Created by: Smitha Gudur
# 

#!/usr/local/bin/perl5

require "cgi-lib.pl";
#require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;
#use calutil::calutil;
require "flush.pl";

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

# bind cntrtab table vars
   tie %cntrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/cntrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['counter'] };



    # get the login name of each hotdiary user.
    # open the user's login apptentrytab. 
    # check in their apptentrytab if there are any entry numbers
    # search for each entry in the appointment entry tab
    # look for the entry numbers that are current or relevant   

    #print "this is appt cron cgi file \n";
    #print "$ENV{HDDATA}/logtab \n"; 
    #%dirlistt = dirlist "$ENV{HDDATA}/logtab";
      
    #foreach $fl (%dirlistt) {
    $mycnt = 0;
    #system "echo \"*******************************\" >> $ENV{HDHOME}/tmp/crontest";
    #system "echo \"*******************************\" >> $ENV{HDHOME}/tmp/crontest";
    #system "echo \"Invoked cron reminder, PID = $$\" >> $ENV{HDHOME}/tmp/crontest";
    $lult = localtime(time());
    #system "echo \"Current Time = $lult\" >> $ENV{HDHOME}/tmp/crontest";
    foreach $fl (keys %logtab) {
      $mycnt += 1;
      #print "entered for each loop fl = $fl\n";
      ($lg, $sf) = split(/\./, $fl);
      #if ($lg eq "manoj") {
      #   system "echo \"User = $lg\" >> $ENV{HDHOME}/tmp/crontest";
      #}
      #$tfile = "$ENV{HDDATA}/$lg/apptentrytab";
      #-e $tfile or next;
      (-e "$ENV{HDDATA}/$lg/appttab" and -d "$ENV{HDDATA}/$lg/appttab") or next;
      
      # bind personal appointment table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$lg/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'sec', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject'] };

      #print "open the file handle \n";
      #open thandle, "<$tfile";
      #print "After open thandle\n";
      #while (<thandle>) {
	#hddebug "entered while loop \n";
         #chop;
         #$onekey = $_;
      foreach $onekey (sort keys %appttab) {
         if ($onekey ne "")  {
	    #print "onekey = ", $onekey, "\n";
	    if (exists $appttab{$onekey}) { 
	       #print "entered exists condition \n";
            $apptmonth = $appttab{$onekey}{'month'};
            $apptday = $appttab{$onekey}{'day'};
            $apptyear = $appttab{$onekey}{'year'};
            $apptmin = $appttab{$onekey}{'min'};
            $apptsec = $appttab{$onekey}{'sec'};
            $appthour = $appttab{$onekey}{'hour'};
            $meridian = $appttab{$onekey}{'meridian'};
            #if ($lg eq "manoj") {
               #system "echo \"($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
            #}
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
            #if ($lg eq "manoj")  {
               #system "echo \"ctime:$ctime\" >> $ENV{HDHOME}/tmp/crontest";
            #}
            $etime = 0;
	    #print "ctime = $ctime \n";

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

            #print "checking etime\n";
            if ($appttab{$onekey}{'recurtype'} eq "Once") {
                #print "entered once\n";
                $etime = etimetosec($apptsec, $apptmin, $appthour, $apptday, $apptmonth, $apptyear, "", "", "", $apptzone); 
	        if (isstd($apptzone)) {
                   #system "echo \"isstd, zone :$apptzone\" >> $ENV{HDHOME}/tmp/crontest";
	           if (isdsttime) {
                      #system "echo \"current time is DST\" >> $ENV{HDHOME}/tmp/crontest";
	               $etime = $etime + 3600;
                   }
                } 
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
              
                #if ($lg eq "manoj") {
               
                #system "echo \"recurtype:$recurtype\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"onekey:$onekey\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmcur_mon, $gmcur_mon\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmcur_year, $gmcur_year\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmcur_wk, $gmcur_wk\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmcur_day, $gmcur_day\" >> $ENV{HDHOME}/tmp/crontest";

                #system "echo \"gmapt_day, $gmapt_day\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmapt_year, $gmapt_year\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmapt_mon, $gmapt_mon\" >> $ENV{HDHOME}/tmp/crontest";
                #system "echo \"gmapt_wk, $gmapt_wk\" >> $ENV{HDHOME}/tmp/crontest";
                #}

                #print "appt month =  $gmapt_mon \n";
                #print "appt year =  $gmapt_year \n";
                #print "appt day = $gmapt_day \n";
                #print "appt wk =  $gmapt_wk \n";
#
                #print "cur month = $gmcur_mon \n";
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

                #if ($lg eq "manoj") {
                   #system "echo \"recurtype DAILY ($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
                #}
                #hddebug "$onekey is Daily";
                # for daily, if current year is >= to appt year.
                # if current year is equal to appt year, check if month
                # is >= than appt month and current day is greater than apt day.
                if ($gmcur_year == $gmapt_year) {
                   if ($gmcur_mon == $gmapt_mon) {
                      if ($gmcur_day < $gmapt_day) {
                         #if ($lg eq "manoj") {
                            #system "echo \"gmcur_day($gmcur_day) < gmapt_day($gmapt_day) ($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
                         #}
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
                
                #$etime = getdailyEtime($apptsec, $apptmin, $appthour, $apptzone);
                $ctime1 = $ctime + (3600 * $apptzone);  
                ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = gmtime($ctime1); 
                $mon = $mon + 1;
                $year = $year + 1900;   
                $etime = etimetosec("", $apptmin, $appthour, $day, $mon, $year, "", "", "", $apptzone);

	        if (isstd($apptzone)) {
                   #system "echo \"isstd, zone :$apptzone\" >> $ENV{HDHOME}/tmp/crontest";
	           if (isdsttime) {
                      #system "echo \"current time is DST\" >> $ENV{HDHOME}/tmp/crontest";
	               $etime = $etime + 3600;
                   }
                } 
                                      
                if (isaptcurrent $ctime, $etime) {
                   #hddebug "APT CURRENT: login $lg, appthour $appthour, apptmin $apptmin, apptday $apptday, apptmonth $apptmonth, apptyear $apptyear, apptzone $apptzone, gmapt_day $gmapt_day, gmapt_mon $gmapt_mon, gmapt_year $gmapt_year";
                }
                #if ($lg eq "manoj")  {
                #   system "echo \"etime:$etime\" >> $ENV{HDHOME}/tmp/crontest";
                #}
                #print "etime = $etime\n";
                #if ($lg eq "manoj") {
                   #system "echo \"DAILY APPT ($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
                #}
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
              #if ($lg eq "manoj") {
                 #system "echo \"WEEKLY APPT ($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
              #}
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
           

            #print "ctime = $ctime\n";
            #print "etime = $etime\n";
            # we need to check for "Onlyonce", "everyday", 
            # "weekly", monthly,annually 
            # calculate day of the appt. and get the matching day of the week.
            # monthly, just calculate the number of hours 
            if (isaptcurrent($ctime, $etime)) { 
                  #if ($lg eq "manoj") {
                     #system "echo \"APT CURRENT ($onekey): $lg, $appthour:$apptmin $meridian, $apptday:$apptmonth:$apptyear\" >> $ENV{HDHOME}/tmp/crontest";
                  #}
                  #hddebug "appt is current"; 
                  $dtype = $appttab{$onekey}{'dtype'}; 
                  $dtype =~ s/\n/\n<BR>/g;
                  $atype = $appttab{$onekey}{'atype'}; 
                  $atype =~ s/\n/\n<BR>/g;

                  $recurtype = $appttab{$onekey}{'recurtype'}; 
                  $recurtype =~ s/\n/\n<BR>/g;

                  $desc = $appttab{$onekey}{'desc'};
                  
                  ($mfile = "$ENV{HDHOME}/tmp/apptcron-$lg-$onekey-$$.txt") =~ s/\n/\n<BR>/g;
                  open mhandle, ">$mfile";
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
                  print "Member Login: $appttab{$onekey}{'login'} \n";
                  print "Time Zone: $appttab{$onekey}{'zone'} \n";
                  #hddebug "Member Login: $appttab{$onekey}{'login'} \n";
                  print "Entry Number: $onekey \n";
		  print "Appt Event: Date: $apptmonth-$apptday-$apptyear \n";
                  print "Appt Event: Time: $apthr:$apptmin $meridian\n";
                  $toname = $logtab{$appttab{$onekey}{'login'}}{'fname'};
                  if ($toname eq "") {
                     $toname = "HotDiary Member";
                  }
                  printf mhandle "Dear $toname,\n\n";
                  printf mhandle "Member Login: $appttab{$onekey}{'login'}\n\n";
                  #printf mhandle "Your appointment is due. Please read the notes below for details.\n\n";
                  #printf mhandle "Regards\n";
                  #printf mhandle "HotDiary Inc.\n\n";
                  printf mhandle "Your Reminder Follows:\n\n";
                  printf mhandle "Date: $apptmonth-$apptday-$apptyear\n";
                  printf mhandle "Time: $apthr:$apptmin $meridian\n";
                  printf mhandle "Reminder Type: $dtype \n";
                  printf mhandle "Description: %s\n", $desc;
                  printf mhandle "Frequency: %s\n", $recurtype;
                  printf mhandle "\nHotDiary - New Generation Internet Organizerr, http://www.hotdiary.com";
                  &flush(mhandle);

                  $counter = $cntrtab{'apptcounter'}{'counter'} + 1;
                  if (($counter % $ENV{'USE_APPT_WINNER_FREQ'}) == 0) { 
                     $login = $appttab{$onekey}{'login'};
                     $email = $logtab{$login}{'email'};
                     system "cat $ENV{'HDHOME'}/letters/apptwinner > $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     system "echo \"Entry Number  $onekey\" >> $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     if ($email ne "") {
                        system "/bin/mail -s \"Did you just win a Prize!\" $email < $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                     }
                  }
                  $cntrtab{'apptcounter'}{'counter'} = $counter;
                  tied(%cntrtab)->sync();
                  #
                  # send email to user
                  #
                  if ($atype eq "Email") {
		    #print "entered email current \n";
                    $login = $appttab{$onekey}{'login'};
		    #print "login =", $login, "\n";
                    if (exists $logtab{$login}) {
		      #print "entered login exists \n";
                      $email = $logtab{$login}{'email'};
                      #print "$login email = ",  $email, "\n";
                      if ($email ne "") {
                         $esubject = $appttab{$onekey}{'subject'};
                         if ($esubject eq "") {
                            $esubject = $appttab{$onekey}{'dtype'};
                         }
                         system "/bin/mail -s \"$esubject\" $email < $mfile";
                      }
                    } #else
                  } else {
                    if ($atype eq "Pager") {
                       $login = $appttab{$onekey}{'login'};
                       if (exists $logtab{$login}) {
                          #print "Entered Pager type"; 
                          $pager = $logtab{$login}{'pager'}; 
                          $from = $logtab{$login}{'fname'};
			  $pagertype = $logtab{$login}{'pagertype'};
                          $subject = $appttab{$onekey}{'subject'};
                          if ($subject ne "") {
                             $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc $subject";
                          } else {
                             $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                          }
                          $pagerfile = "$ENV{HDHOME}/tmp/$login$$";
                          qx{echo \"$message\" > $pagerfile};
                          $pager = getPhoneDigits $pager;
			  if ("\U$pagertype" eq "\USkyTel Pager") {
                            system "java COM.hotdiary.main.SendPage \"$pager\" \"$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc $subject\" \"$from\"";
	                  } else {
			       if ("\U$pagertype" eq "\UAirTouch Pager") {
                                  if ($pager ne "") {
				     $email = "$pager\@airtouch.net"; 
                                     system "/bin/mail -s \"$from\" $email < $pagerfile";
                                  } 
			       } else {
                                    if ("\U$pagertype" eq "\UNextel Pager") {
                                       $email = "$pager\@page.nextel.com"; 
                                       system "/bin/mail -s \"$from\" $email < $pagerfile";
                                    } else {
                                       if ("\U$pagertype" eq "\UPageMart Pager") {
                                          $email = "$pager\@pagemart.net"; 
                                          system "/bin/mail -s \"$from\" $email < $pagerfile";
                                       } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
       $message = trim $message;
       $message =~ s/\s/\+/g;
       $url = "http://www.metrocall.com/cgi-bin/rbox/default.cgi?TO=$pager&Message=\"$message\"";
       system "java COM.hotdiary.main.ExecCGIURL \"$url\"";
    } else {
    if ("\U$pagertype" eq "\UOther Pager") {
       $subject = $appttab{$onekey}{'subject'};
       $recurtype = $appttab{$onekey}{'recurtype'};
       $message = "$subject $desc $dtype $apthr:$apptmin $meridian $recurtype";
       $otherpagerfile = "$ENV{HDHOME}/tmp/$login$otherpager$$";
       qx{echo \"$message\" > $otherpagerfile};
       ($user, $domain) = split "\@", $pager;
       if ((trim($user) ne "") && (trim($domain) ne "")) {
          $email = "$pager"; 
       } else {
            qx{echo \"For Other Pager type, your pager field must contain a valid email address. Could not deliver message to your pager. Sending an email message instead.\" >> $otherpagerfile};
            $email = $logtab{$login}{'email'};
       }
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
        }
      close thandle;
   }

   #system "echo \"total logins processed = $mycnt\" >> $ENV{HDHOME}/tmp/crontest";


# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   #tied(%appttab)->sync();
   #tied(%logtab)->sync();
   #print "end of appt cron cgi file \n";
}

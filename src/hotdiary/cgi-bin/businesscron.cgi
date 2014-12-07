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
# FileName: businesscron.cgi
# Purpose: it searches for appointments and sends out email/fax/pager 
# from cron.      
# Creation Date: 10-02-99 
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

   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 
	'businesstitle', 'street', 'suite', 'city', 
	'state', 'zipcode', 'country', 'phone', 'fax', 
	'url', 'email', 'other', 'list'] };

   foreach $business (keys %businesstab) {

   -d "$ENV{HDDATA}/business/business/$business/teams/teamtab" or next;
   # bind teamtab table vars 
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode', 
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] };


    foreach $team (keys %teamtab) {
      $team = trim $team;

     (-e "$ENV{HDDATA}/business/business/$business/teams/teamtab" and -d "$ENV{HDDATA}/business/business/$business/teams/teamtab" and -d "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab") or next;
      
      tie %busappttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['entryno', 'login', 'month', 'day', 'year',
          'hour', 'min', 'meridian', 'dhour', 'dmin',
          'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free', 
          'subject', 'street', 'city', 'state', 'zipcode', 'country',
          'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

      (@records) = sort keys %busappttab;
      for ($y = 0; $y <= $#records; $y = $y+1) {
         $onekey = $records[$y];
         if ($onekey ne "")  {
	    if (exists $busappttab{$onekey}) { 
               $apptmonth = $busappttab{$onekey}{'month'};
               $apptday = $busappttab{$onekey}{'day'};
               $apptyear = $busappttab{$onekey}{'year'};
               $apptmin = $busappttab{$onekey}{'min'};
               $apptsec = $busappttab{$onekey}{'sec'};
               $appthour = $busappttab{$onekey}{'hour'};
               $meridian = $busappttab{$onekey}{'meridian'};
               $apptzone = $busappttab{$onekey}{'zone'};
	       $apptzone = adjustzone($apptzone);
	       $recurtype = $busappttab{$onekey}{'recurtype'};
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

               if ($busappttab{$onekey}{'recurtype'} eq "Once") {
                   #print "entered once\n";
                   $etime = etimetosec($apptsec, $apptmin, $appthour, $apptday, $apptmonth, $apptyear, "", "", "", $apptzone); 
               }


               # comparisons are always in GMT
               if ($busappttab{$onekey}{'recurtype'} ne "Once") {

                   #print "recurtype = $busappttab{$onekey}{'recurtype'} \n";

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

               if ($busappttab{$onekey}{'recurtype'} eq "Daily") {

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

            
               if ($busappttab{$onekey}{'recurtype'} eq "Weekly") {
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
               if ($busappttab{$onekey}{'recurtype'} eq "Monthly") {
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
               if ($busappttab{$onekey}{'recurtype'} eq "Yearly") {
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
                  $dtype = $busappttab{$onekey}{'dtype'}; 
                  $dtype =~ s/\n/\n<BR>/g;
                  $atype = $busappttab{$onekey}{'atype'}; 
                  $atype =~ s/\n/\n<BR>/g;

                  $recurtype = $busappttab{$onekey}{'recurtype'}; 
                  $recurtype =~ s/\n/\n<BR>/g;

                  $desc = $busappttab{$onekey}{'desc'};
                  
                  ($mfile = "$ENV{HDHOME}/tmp/businesscron$$.txt") =~ s/\n/\n<BR>/g;
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
                  $n = 0; 
                  print "Team Name: $team\n";

                  # bind manager table vars
                  tie %teampeopletab, 'AsciiDB::TagFile',
                    DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/teampeopletab",
                    SUFIX => '.rec',
                    SCHEMA => {
                    ORDER => ['login']};

		  foreach $t (keys %teampeopletab) {
                     $esubject = $busappttab{$onekey}{'subject'};
		     $uname = trim $t;	
                     if (!exists $logtab{$uname}) {
	                next;
                     }
		     $login = $uname;	
                     $email = $logtab{$login}{'email'};
                     print "-----Team Member: $uname \n";
                     print "-----Entry Number: $onekey \n";
                     print "-----Business Team Reminder Event: Date: $apptmonth-
$apptday-$apptyear \n";
                     print "-----Business Team Reminder Event: Time: $apthr:$app
tmin $meridian\n";                                                
                     if ($esubject eq "") {
                         $esubject = $busappttab{$onekey}{'dtype'};
                     }
                     $busy = $busappttab{$onekey}{'free'};
                     $zone = $busappttab{$onekey}{'zone'};
		     $zone = getzonestr $zone;
                     $duration = $busappttab{$onekey}{'dhour'} . "Hrs";
		     $dmin = $busappttab{$onekey}{'dmin'};
		     if ($dmin eq "") {
		        $dmin = "0";
		     }
                     $duration .= " " . $dmin . "Mins";
                     $share = $busappttab{$onekey}{'share'};
                     $banner = adjusturl $busappttab{$onekey}{'banner'};
                     $prml = "";
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/teamreminder.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/teamreminder-$login$$.html";
                     $prml = strapp $prml, "login=$login";
		     $teamname = $teamtab{$team}{teamname};
                     $prml = strapp $prml, "teamname=$teamname";
                     $prml = strapp $prml, "busname=$business";
                     $prml = strapp $prml, "email=$email";
                     $prml = strapp $prml, "subject=$esubject";
                     $prml = strapp $prml, "eventtype=$dtype";
                     $prml = strapp $prml, "description=$desc";
                     $prml = strapp $prml, "time=$apthr:$apptmin $meridian";
                     $prml = strapp $prml, "frequency=$recurtype";
                     $prml = strapp $prml, "zone=$zone";
                     $prml = strapp $prml, "duration=$duration";
                     $prml = strapp $prml, "share=$share";
                     $prml = strapp $prml, "busy=$busy";
                     $prml = strapp $prml, "banner=$banner";
                     parseIt $prml;

                     #tie %moneytab, 'AsciiDB::TagFile',
                     #DIRECTORY => "$ENV{HDDATA}/moneytab",
                     #SUFIX => '.rec',
                     #SCHEMA => {
                     #  ORDER => ['login', 'account', 'comment', 'approved'] };

                     #$str = "";
                     #if (exists $moneytab{$login}) {
                     #   $reward = $moneytab{$login}{account};
                     ##   if ($reward ne "") {
                     #      $damount = $reward / 100;
                     #      $str = 'US $' . "$damount";
                     #   } else {
                     #      $str = 'US $' . '0.00';
                     #   }
                     #} else {
                     #   $str = 'US $' . '0.00';
                     #}

                    $counter = $cntrtab{'apptcounter'}{'counter'} + 1;
                    if (($counter % $ENV{'USE_APPT_WINNER_FREQ'}) == 0) { 
                       $login = $uname;
                       system "cat $ENV{'HDHOME'}/letters/apptwinner > $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                       system "echo \"Entry Number  $onekey\" >> $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                       if ($email ne "") {
                          system "/bin/mail -s \"Did you just win a Prize!\" $email < $ENV{HDHOME}/tmp/apptwinner$onekey$$";
                       }
                    }
                    $cntrtab{'apptcounter'}{'counter'} = $counter;
                    tied(%cntrtab)->sync();
                    # send email to user
                    if ($atype eq "Email") {
                      $login = $uname;
                      if (exists $logtab{$login}) {
                        if ($email ne "") {
 	                   system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/teamreminder-$login$$.html -s \"$esubject\" -e \"\" -t \"$email\" -F cronuser\@hotdiary.com";
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
                                  system "/bin/mail -s \"$from\" $email < $pagerfile";
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
        }
   }
   }


# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 
}

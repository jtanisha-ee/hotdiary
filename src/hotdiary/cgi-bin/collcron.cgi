#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: collcron.cgi
# Purpose: it searches for collabrum and sends out email/fax/pager 
# from cron.      
# Creation Date: 02-09-98 
# Created by: Smitha Gudur
# 

#!/usr/local/bin/perl5

require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{

# bind collabrum table vars
   tie %colltab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/colltab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'subject', 'distribution', 'colledit',
        'zone'] };


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };




    # get the login name of each hotdiary user.
    # open the user's login collentrytab. 
    # check in their collentrytab if there are any entry numbers
    # search for each entry in the appointment entry tab
    # look for the entry numbers that are current or relevant   

      $ctime = ctimetosec();
      $tfile = "$ENV{HDDATA}/collentrytab";
      open thandle, "<$tfile";
      while (<thandle>) {
	#print "entered while loop \n";
         chop;
         $onekey = $_;
         if ($onekey ne "")  {
	    #print "onekey = ", $onekey, "\n";
	    if (exists $colltab{$onekey}) { 
		#print "entered exists condition \n";
            $apptmonth = $colltab{$onekey}{'month'};
            $apptday = $colltab{$onekey}{'day'};
            $apptyear = $colltab{$onekey}{'year'};
            $apptmin = $colltab{$onekey}{'min'};
            $apptsec = $colltab{$onekey}{'sec'};
            $appthour = $colltab{$onekey}{'hour'};
            $meridian = $colltab{$onekey}{'meridian'};
            $apptzone = $colltab{$onekey}{'zone'};
            $subject = $colltab{$onekey}{'subject'};
	    $apptzone = adjustzone($apptzone);

            #
            #  if it is 12.00pm we should not add 12 hours to this.
            #
            if (($meridian eq "PM") && ($appthour ne "12")) {
                $appthour += 12;
            }

            if (($meridian eq "AM") && ($appthour eq "12")){
                $appthour = 0;
            }
  
            $etime = etimetosec($apptsec, $apptmin, $appthour, $apptday, $apptmonth, $apptyear, "", "", "", $apptzone); 
	    #print "etime = $etime \n";

	    #print "ctime = $ctime \n";
            if (isaptcurrent($ctime, $etime))  {
		#print "entered appt current \n";
                  $dtype = $colltab{$onekey}{'dtype'}; 
                  $dtype =~ s/\n/\n<BR>/g;
                  $atype = $colltab{$onekey}{'atype'}; 
                  $atype =~ s/\n/\n<BR>/g;
		  $subject = $colltab{$onekey}{'subject'};
                  $desc = $colltab{$onekey}{'desc'};
                  
                  if ($appthour >= 13) {
                     $apthr = $appthour - 12;
                  } else {
                     if ($appthour eq "0") {
                       $apthr = $appthour + 12;
                     } else {
                       $apthr = $appthour;

                     }
                  }
                  #
                  # send email to user(s) i.e in distribution 
                  #
		  $ts = $colltab{$onekey}{'distribution'};
                  @hsh = split(" ", $ts);
                  #print $#hsh;
                  #print @hsh[0];
                  $ts = "";
                  #@hsh[0] = "\b@hsh[0]";

                 $login = $colltab{$onekey}{'login'};
                 print "HotDiary Collabrum:\n\n";  
                 print "Entry Number: $onekey\n";  
                 print "Owner: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";  
                 print "Owner ID: $login\n";  
                 print "Invitees: $colltab{$onekey}{'distribution'}\n";  
                 print "Date: $apptmonth-$apptday-$apptyear\n";  
                 print "Time: $apthr:$apptmin $meridian\n";
                 print "Reminder Type: $dtype\n";
                 print "Description: $desc\n";
                 print "Subject: $subject\n";
                
                 ($mfile = "$ENV{HDHOME}/tmp/colladd$$.txt") =~ s/\n/\n<BR>/g;
                 open mhandle, ">$mfile";

                 printf mhandle "Dear HotDiary Member,\n\n";
                 printf mhandle "Your collaborative appointment is now due. Please read the notes below for details.\n\n";
                 #printf mhandle "Regards\n";
                 #printf mhandle "HotDiary Inc.\n\n";
                 printf mhandle "Your Collabrum Reminder Follows:\n\n";
                 printf mhandle "Entry number to search for your collabrum appointment is %s\n", $onekey;
                 printf mhandle "(Please keep the above number carefully. You will need it to access your appointment)\n\n";
                 #printf mhandle "Owner: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
                 printf mhandle "Owner ID: $login\n";
                 printf mhandle "Invitees: $colltab{$onekey}{'distribution'}\n";
                 printf mhandle "Date: $apptmonth-$apptday-$apptyear\n";
                 printf mhandle "Time: $apthr:$apptmin $meridian\n";
                 printf mhandle "Reminder Type: $dtype \n";
                 printf mhandle "Description: %s\n", $desc;
                 printf mhandle "Subject: %s\n", $subject;
                 printf mhandle "\n HotDiary - New Generation Internet Organizer, http://www.hotdiary.com.";
                 #printf mhandle "%s\n", $desc;
                 &flush(mhandle);

                 if ($atype eq "Email") {
                 # send email to distribution
                    foreach $i (@hsh) {
                      #print "i=", $i, "\n";
                      if (exists $logtab{$i}) {
                         $email = $logtab{$i}{'email'};
                         #print "$i email = ",  $email, "\n";
                         system "/bin/mail -s \"$subject\" $email < $mfile";
                      } else {
                         # bind lgrouptab table vars
                         tie %lgrouptab, 'AsciiDB::TagFile',
                         DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                         SUFIX => '.rec',
                         SCHEMA => {
                         ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                         if (exists $lgrouptab{$i}) {
                            if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                               tie %usertab, 'AsciiDB::TagFile',
                               DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                               SUFIX => '.rec',
                               SCHEMA => {
                               ORDER => ['login'] };
                               (@records) = sort keys %usertab; 
                               if ($#records >= 0) {
                                  for ($k = 0; $k <= $#records; $k++) {
                                      if (exists $logtab{$records[$k]}) {
                                         $email = $logtab{$records[$k]}{'email'};
                                         if ($email ne "") {
                                            system "/bin/mail -s \"$subject\" $email < $mfile";
                                         }
                                      }
                                  }
                               } 
                            }
                         } else {
                            tie %plgrouptab, 'AsciiDB::TagFile',
                            DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
                            SUFIX => '.rec',
                            SCHEMA => {
                            ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc' ] };
                            if (exists $plgrouptab{$i}) {
                               $groupfounder = $plgrouptab{$i}{'groupfounder'};
                               if ($groupfounder ne "") {
			          $alphaindex = substr $groupfounder, 0, 1;
				  $alphaindex = $alphaindex . '-index';                              if (-d "$ENV{HDDATA}/groups/$alphaindex/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$groupfounder/personal/$i/gmembertab",
                                     SUFIX => '.rec',
                                     SCHEMA => {
                                     ORDER => ['login'] };
                                     (@records) = sort keys %gmembertab;
                                     if ($#records >= 0) {
                                        for ($k = 0; $k <= $#records; $k++) {
                                           ($user, $domain) = split "\@", $records[$k];
                                           if (exists $logtab{$records[$k]}) {
                                              $email = $logtab{$records[$k]}{'email'};
                                              if ($email ne "") {
                                                 system "/bin/mail -s \"$subject\" $email < $mfile";
                                              }

                                           } else {
   if (((trim $user) ne "") && ((trim $domain) ne "")) {
      system "/bin/mail -s \"$subject\" $records[$k] < $mfile";
   }
                                           }
                                        }
                                     }
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $email = $logtab{$groupfounder}{'email'};
                                     if ($email ne "") {
                                        system "/bin/mail -s \"$subject\" $email < $mfile";
                                     }
                                  }
                               }
                            }
                         }
                      }
                    }
                 } else {
                 # send pager to distribution
                    $login = $colltab{$onekey}{'login'};
                    foreach $i (@hsh) {
                      if (exists $logtab{$i}) {
                         $pager = $logtab{$i}{'pager'};
                         $toname = $logtab{$i}{'fname'};
			 $pagertype = $logtab{$i}{'pagertype'};
                         $from = $logtab{$login}{'fname'};
                         $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                         $pagerfile = "$ENV{HDHOME}/tmp/$i$$";
                         qx{echo \"$message\" > $pagerfile};
                         if ($pager ne "") {
                           #print "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"\n";
			   if ("\U$pagertype" eq "\USkyTel Pager") {
                              $pager = getPhoneDigits $pager;
                              system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
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
                      } else {
###############################
                   # bind lgrouptab table vars
                         tie %lgrouptab, 'AsciiDB::TagFile',
                         DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                         SUFIX => '.rec',
                         SCHEMA => {
                         ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed'  ] };
                         if (exists $lgrouptab{$i}) {
                            if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                               tie %usertab, 'AsciiDB::TagFile',
                               DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                               SUFIX => '.rec',
                               SCHEMA => {
                               ORDER => ['login'] };
                               (@records) = sort keys %usertab;
                               if ($#records >= 0) {
                                  for ($k = 0; $k <= $#records; $k++) {
                                      if (exists $logtab{$records[$k]}) {
                                         $pager = $logtab{$records[$k]}{'pager'};
			                 $pagertype = $logtab{$k}{'pagertype'};
                                         $toname = $logtab{$records[$k]}{'fname'};
                                         $from = $logtab{$login}{'fname'};
                                         #print "k = $k\n";
                                         #print "login = $records[$k]\n";
                                         #print "toname = $toname\n";
                                         $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                                         $pagerfile = "$ENV{HDHOME}/tmp/$login$$";
                                         qx{echo \"$message\" > $pagerfile};
                                         if ($pager ne "") {
                                            #print "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"\n";
			                    if ("\U$pagertype" eq "\USkyTel Pager") {
                                               $pager = getPhoneDigits $pager;
                                               system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
                                            } else {
   if ("\U$pagertype" eq "\UAirTouch Pager") {
      $pager = getPhoneDigits $pager;
      $email = "$pager\@airtouch.net"; 
      system "/bin/mail -s \"$from\" $email < $pagerfile";
   } else {
       if ("\U$pagertype" eq "\UNextel Pager") {
          $pager = getPhoneDigits $pager;
          $email = "$pager\@page.nextel.com"; 
          system "/bin/mail -s \"$from\" $email < $pagerfile";
       } else {
          if ("\U$pagertype" eq "\UPageMart Pager") {
             $pager = getPhoneDigits $pager;
             $email = "$pager\@pagemart.net"; 
             system "/bin/mail -s \"$from\" $email < $pagerfile";
          } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
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
                     $email = $logtab{$records[$k]}{'email'};
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
                         } else {
                            tie %plgrouptab, 'AsciiDB::TagFile',
                            DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
                            SUFIX => '.rec',
                            SCHEMA => {
                            ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc' ] };
                            if (exists $plgrouptab{$i}) {
                               $groupfounder = $plgrouptab{$i}{'groupfounder'};
                               if ($groupfounder ne "") {
				  $alphaindex = substr $groupfounder, 0, 1;
		                  $alphaindex = $alphaindex . '-index';                          if (-d "$ENV{HDDATA}/groups/$alphaindex/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$groupfounder/personal/$i/gmembertab",
                                     SUFIX => '.rec',
                                     SCHEMA => {
                                     ORDER => ['login'] };
                                     (@records) = sort keys %gmembertab;
                                     if ($#records >= 0) {
                                        for ($k = 0; $k <= $#records; $k++) {
                                           if (exists $logtab{$records[$k]}) {
                                              $pager = $logtab{$records[$k]}{'pager'};
			                      $pagertype = $logtab{$records[$k]}{'pagertype'};
                                              $toname = $logtab{$records[$k]}{'fname'};
                                              $from = $logtab{$login}{'fname'};
                                              $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                                              $pagerfile = "$ENV{HDHOME}/tmp/$records[$k]$$";
                                              qx{echo \"$message\" > $pagerfile};
                                              if ($pager ne "") {
                                                 #print "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"\n";
   if ("\U$pagertype" eq "\USkyTel Pager") {
      $pager = getPhoneDigits $pager;
      system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
   } else {
        if ("\U$pagertype" eq "\UAirTouch Pager") {
           $pager = getPhoneDigits $pager;
           $email = "$pager\@airtouch.net"; 
           system "/bin/mail -s \"$from\" $email < $pagerfile";
        } else {
            if ("\U$pagertype" eq "\UNextel Pager") {
               $pager = getPhoneDigits $pager;
               $email = "$pager\@page.nextel.com"; 
               system "/bin/mail -s \"$from\" $email < $pagerfile";
            } else {
               if ("\U$pagertype" eq "\UPageMart Pager") {
                  $pager = getPhoneDigits $pager;
                  $email = "$pager\@pagemart.net"; 
                  system "/bin/mail -s \"$from\" $email < $pagerfile";
               } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
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
                     $email = $logtab{$records[k]}{'email'};
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
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $pager = $logtab{$groupfounder}{'pager'};
                                     $toname = $logtab{$groupfounder}{'fname'};
			             $pagertype = $logtab{$groupfounder}{'pagertype'};
                                     $from = $logtab{$groupfounder}{'fname'};
                                     $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                                     $pagerfile = "$ENV{HDHOME}/tmp/$groupfounder$$";
                                     qx{echo \"$message\" > $pagerfile};
                                     if ($pager ne "") {
                                        #print "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"\n";
    if ("\U$pagertype" eq "\USkyTel Pager") {
       $pager = getPhoneDigits $pager;
       system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
    } else {
         if ("\U$pagertype" eq "\UAirTouch Pager") {
            $pager = getPhoneDigits $pager;
            $email = "$pager\@airtouch.net"; 
            system "/bin/mail -s \"$from\" $email < $pagerfile";
         } else {
             if ("\U$pagertype" eq "\UNextel Pager") {
                $pager = getPhoneDigits $pager;
                $email = "$pager\@page.nextel.com"; 
                system "/bin/mail -s \"$from\" $email < $pagerfile";
             } else {
                if ("\U$pagertype" eq "\UPageMart Pager") {
                   $pager = getPhoneDigits $pager;
                   $email = "$pager\@pagemart.net"; 
                   system "/bin/mail -s \"$from\" $email < $pagerfile";
                } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
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
                     $email = $logtab{$groupfounder}{'email'};
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

###############################
                      }
                    }

                 }
 
                  # send email to owner.
                  #
                  if ($atype eq "Email") {
		    #print "entered email current \n";
                    $login = $colltab{$onekey}{'login'};
		    #print "login =", $login, "\n";
                    if (exists $logtab{$login}) {
		      #print "entered login exists \n";
                      $email = $logtab{$login}{'email'};
                      #print "$login email = ",  $email, "\n";
                      system "/bin/mail -s \"$subject\" $email < $mfile";
                    } #else
                  }  else {
                     if ($atype eq "Pager") {
                       $login = $colltab{$onekey}{'login'};
                       if (exists $logtab{$login}) {
                          #print "Entered Pager type";
                          $pager = $logtab{$login}{'pager'};
			  $pagertype = $logtab{$login}{'pagertype'};
                          $from = $logtab{$login}{'fname'};
                          $toname = $logtab{$login}{'fname'};
                          $message = "$apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc";
                          $pagerfile = "$ENV{HDHOME}/tmp/$login$$";
                          qx{echo \"$message\" > $pagerfile};
                          #print "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"\n";
      if ("\U$pagertype" eq "\USkyTel Pager") {
         $pager = getPhoneDigits $pager;
         system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $onekey $apptmonth-$apptday-$apptyear $apthr:$apptmin $meridian $dtype $desc\" \"$from\"";
      } else {
           if ("\U$pagertype" eq "\UAirTouch Pager") {
              $pager = getPhoneDigits $pager;
              $email = "$pager\@airtouch.net"; 
              system "/bin/mail -s \"$from\" $email < $pagerfile";
           } else {
               if ("\U$pagertype" eq "\UNextel Pager") {
                  $pager = getPhoneDigits $pager;
                  $email = "$pager\@page.nextel.com"; 
                  system "/bin/mail -s \"$from\" $email < $pagerfile";
               } else {
                  if ("\U$pagertype" eq "\UPageMart Pager") {
                     $pager = getPhoneDigits $pager;
                     $email = "$pager\@pagemart.net"; 
                     system "/bin/mail -s \"$from\" $email < $pagerfile";
                  } else {
    if ("\U$pagertype" eq "\UMetrocall Pager") {
       $message = "$desc $dtype $apthr:$apptmin $meridian";
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
      close thandle;


# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   tied(%colltab)->sync();
   #tied(%logtab)->sync();
  #print "end of collbrum cron cgi file \n";
}

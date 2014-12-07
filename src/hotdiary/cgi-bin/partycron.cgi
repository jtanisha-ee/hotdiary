#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: partycron.cgi
# Purpose: it searches for partycron and sends out email/fax/pager 
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

# bind partytab table vars
   tie %partytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'subject', 'distribution', 'partyedit',
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

      #$tfile = "$ENV{HDDATA}/collentrytab";
      #open thandle, "<$tfile";
      #while (<thandle>) {
	#print "entered while loop \n";
         #chop;
         #$onekey = $_;
      foreach $onekey (sort keys %partytab) {
         if ($onekey ne "")  {
	    if (exists $partytab{$onekey}) { 
            $apptmonth = $partytab{$onekey}{'month'};
            $apptday = $partytab{$onekey}{'day'};
            $apptyear = $partytab{$onekey}{'year'};
            $apptmin = $partytab{$onekey}{'min'};
            $apptsec = $partytab{$onekey}{'sec'};
            $appthour = $partytab{$onekey}{'hour'};
            $meridian = $partytab{$onekey}{'meridian'};
            $apptzone = $partytab{$onekey}{'zone'};
            $subject = $partytab{$onekey}{'subject'};
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
                  $dtype = $partytab{$onekey}{'dtype'}; 
                  $dtype =~ s/\n/\n<BR>/g;
                  $atype = $partytab{$onekey}{'atype'}; 
                  $atype =~ s/\n/\n<BR>/g;
		  $subject = $partytab{$onekey}{'subject'};
                  $desc = $partytab{$onekey}{'desc'};
                  
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
		  $ts = $partytab{$onekey}{'distribution'};
                  (@hsh) = split(" ", $ts);
                  #print $#hsh;
                  #print @hsh[0];
                  $ts = "";
                  #@hsh[0] = "\b@hsh[0]";


                 $login = $partytab{$onekey}{'login'};
                 print "HotDiary Party Invitation: <BR><BR>";  
                 print "Party Organizer: $logtab{$login}{'fname'} $logtab{$login}{'lname'}<BR><BR>";  
                 print "Party Organizer ID: $login<BR><BR>";  
                 print "Party Invitees: $partytab{$onekey}{'distribution'}<BR>";  
                 print "Date: $apptmonth-$apptday-$apptyear<BR>";  
                 print "Time: $apthr:$apptmin $meridian<BR>";
                 print "Reminder Type: $dtype<BR>";
                 print "Description: $desc<BR><BR>";
                 print "Subject: $subject<BR><BR>";
                
                 ($mfile = "$ENV{HDHOME}/tmp/partyadd$$.html") =~ s/\n/\n<BR>/g;
                 open mhandle, ">$mfile";

		 ## party message in html format
                 $partymsg = "<HTML><BODY BGCOLOR=\"ffffff\"><FONT FACE=\"Verdana\"><TABLE><TR><TD>";
                 $partymsg .= "<IMG SRC=\"http://www.hotdiary.com/images/balloon6.gif\" WIDTH=\"60\" HEIGHT=\"100\"></TD><TD><H3>HotDiary Party Invitation</h3></TD></TR></TABLE>";
                 $partymsg .= "<p align=\"justify\">";
                 $partyendmsg = "</p><p><a href=\"http://www.hotdiary.com\">http://www.hotdiary.com</a></p>";
                 $partyendmsg .= "</FONT></BODY></HTML>";

		 printf mhandle "$partymsg<BR>";
                 printf mhandle "Dear HotDiary Member,<BR><BR>";
                 printf mhandle "Your party event reminder is now due. Please read the details below.";
                 printf mhandle "Your party event details:<BR><BR>";
                 printf mhandle "Party Event: %s<BR>", $subject;
                 printf mhandle "Details of Party: %s<BR>", $desc;
                 printf mhandle "Party Organizer ID: $login<BR>";
                 printf mhandle "Party Invitees: $partytab{$onekey}{'distribution'}<BR>";
                 printf mhandle "Date of Party : $apptmonth-$apptday-$apptyear<BR>";
                 printf mhandle "Time of Party : $apthr:$apptmin $meridian<BR>";
                 printf mhandle "Party Reminder Type: $dtype <BR>";
                 printf mhandle "\n HotDiary - New Generation Internet Organizer, http://www.hotdiary.com.<BR>";
		 printf mhandle "$partyendmsg";
                 &flush(mhandle);

                 if ($atype eq "Email") {
                 # send email to distribution
                    foreach $i (@hsh) {
                      #print "i=", $i, "\n";
                      if (exists $logtab{$i}) {
                         $email = $logtab{$i}{'email'};
                         #print "$i email = ",  $email, "\n";
                         #system "/bin/mail -s \"$subject\" $email < $mfile";
			 system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
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
                                            #system "/bin/mail -s \"$subject\" $email < $mfile";
                      			    system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
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
                               $alp = substr $groupfounder, 0, 1;
                               $alp = $alp . '-index';
                               if ($groupfounder ne "") {
                                  if (-d "$ENV{HDDATA}/groups/$alp/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alp/$groupfounder/personal/$i/gmembertab",
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
                                                 #system "/bin/mail -s \"$subject\" $email < $mfile";
			 		         system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
                                              }

                                           } else {
   if (((trim $user) ne "") && ((trim $domain) ne "")) {
      #system "/bin/mail -s \"$subject\" $records[$k] < $mfile";
      system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$records[$k]\" -F noreply\@hotdiary.com";
   }
                                           }
                                        }
                                     }
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $email = $logtab{$groupfounder}{'email'};
                                     if ($email ne "") {
                                        #system "/bin/mail -s \"$subject\" $email < $mfile";
                                        system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
                                     }
                                  }
                               }
                            }
                         }
                      }
                    }
                 } else {
                 # send pager to distribution
                    $login = $partytab{$onekey}{'login'};
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
                               $alpgf = substr $groupfounder, 0, 1;
                               $alpgf = $alpgf . '-index';
                               if ($groupfounder ne "") {
                                  if (-d "$ENV{HDDATA}/groups/$alpgf/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alpgf/$groupfounder/personal/$i/gmembertab",
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
                    $login = $partytab{$onekey}{'login'};
		    #print "login =", $login, "\n";
                    if (exists $logtab{$login}) {
		      #print "entered login exists \n";
                      $email = $logtab{$login}{'email'};
                      #print "$login email = ",  $email, "\n";
                      #system "/bin/mail -s \"$subject\" $email < $mfile";
                      system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $mfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";

                    } #else
                  }  else {
                     if ($atype eq "Pager") {
                       $login = $partytab{$onekey}{'login'};
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
   system "rm -f $ENV{HDHOME}/tmp/partyadd$$.html";

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   #tied(%logtab)->sync();
  #print "end of collbrum cron cgi file \n";
}

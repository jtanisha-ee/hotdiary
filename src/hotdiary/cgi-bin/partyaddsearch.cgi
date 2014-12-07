#!/usr/local/bin/perl5

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: partyaddsearch.cgi
# Purpose: it adds and searches the party appointments.
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXDESC = 4096;

# parse the command line
   &ReadParse(*input); 

   hddebug "partyaddsearch.cgi";
   $action = $input{search};
   #hddebug "action = $action";

   $vdomain = trim $input{'vdomain'};
   $rh = trim $input{'rh'};
   $jp = $input{jp};
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers',
        'account', 'topleft', 'topright', 'middleright',
        'bottomleft', 'bottomright', 'meta'] };

   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   if ($biscuit eq "") {
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
              exit;
            }
         }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   }



# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['biscuit', 'login', 'time'] };


# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };
   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
            }
         }
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.\n");
            exit;
	 }
      }
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
               exit;
            }
         }
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();


   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }


   tie %parttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/partners/parttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['logo', 'title', 'banner'] };


   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

  ## party message in html format
  $partymsg = "<HTML><BODY BGCOLOR=\"ffffff\"><FONT FACE=\"Verdana\"><TABLE><TR><TD>";
  $partymsg .= "<IMG SRC=\"http://www.hotdiary.com/images/balloon6.gif\" WIDTH=\"60\" HEIGHT=\"100\"></TD><TD><H3>HotDiary Party Invitation</h3></TD></TR></TABLE>"; 
  $partymsg .= "<p align=\"justify\">";
  $partyendmsg = "</p><p><a href=\"http://www.hotdiary.com\">http://www.hotdiary.com</a></p>";
  $partyendmsg .= "</FONT></BODY></HTML>";



   if ($input{'add'} ne "") {
      $action = "Add";
   }
 
   if ($input{'search'} ne "") {
      $action = "Search";
   }


   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        $login = $sesstab{$biscuit}{'login'};
        if ($login eq "") {
      		error("Login  is an empty string.\n");
                exit;
        }
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
   #    error("Intrusion detected. Access denied.\n");
   #    exit;
   #}


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
     if (exists $sesstab{$biscuit}) {
        delete $sesstab{$biscuit};
     }
     if (exists $logsess{$login}) {
        delete $logsess{$login};
     }
     status("$login: Your session has timed out. Please relogin. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.");
     exit;
   }

   $sesstab{$biscuit}{'time'} = time(); 


   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }                           

# bind party table vars
   tie %partytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partytab",
   SUFIX => '.rec', 
   SCHEMA => { 
   	ORDER => ['entryno', 'login', 'month', 'day', 'year', 
	'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'subject', 'distribution', 'partyedit',
	'zone'] };

   # get entry number
   $entryno = getkeys();
   $pagenum = 0;
   $nextpage = 0;
   $prevpage = 0;

   if ($action eq "Add") {
       #add a new party 
       $partytab{$entryno}{'entryno'} = $entryno;
       $partytab{$entryno}{'login'} = $login;

       
       $mo = trim $input{'month'};
       #hddebug "mo = $mo";
       $da = trim $input{'day'};
       $yr = trim $input{'year'};


       
       $ezone = trim $input{'zone'};
       $ehour = trim $input{'hour'};
       $meridian = trim $input{'meridian'};
       if (trim $input{'min'} eq "0") {
          $emin = '00';
       } else {
          $emin= trim $input{'min'};
       }

       $event_zone = adjustzone($ezone);
       if ( ($meridian eq "PM") && ($ehour ne "12")) {
            $ehour += 12;
       }
       if (($meridian eq "AM") && ($ehour eq "12")){
            $ehour = 0;
       }


       $etime = etimetosec("", $emin, $ehour, $da, $mo, $yr, "", "", "", $event_zone);
       $ctime = ctimetosec();

       if ($input{sendnow} ne "on") {
          if ((($etime - $ctime) < 0) || (($etime - $ctime) < 1200)) {
             status("$login: You can only set reminders which are due in the future, atleast 20 minutes past current time. If you would like to send this party invitation now, check on SendNow.");
             exit;
	  }
       }


       #if (notDate($da, $mo, $yr)) {
       #   error("$da $mo $yr: invalid date\n");
       #   return;
       #}

       #if (notHour(trim $input{'hour'})) {
       #   error("$input{'hour'}: invalid hour\n");
       #   return;
       #}
 
       #if (notMinSec(trim $input{'min'})) { 
       #   error("$input{'min'}: invalid minute\n");
       #   return;
       #}

       #if (notMinSec(trim $input{'sec'})) {
       #   error("$input{'sec'}:  invalid second\n"); 
       #  return;
       #}
   
       #if (notMeridian(trim $input{'meridian'})) {
       #   error("$input{'meridian'}: invalid. It can be only AM or PM \n");
       #   return;
       #}

       #if (notHour(trim $input{'dhour'})) {	
       #   error("$input{'dhour'}: invalid hour\n");
       #   return;
       #} 

       #if (notMinSec(trim $input{'dmin'})) {
       #  error("$input{'dmin'}: invalid minute\n");
       #   return;
       #}

       if (notDesc($input{'desc'})) { 
          status("$login: Invalid characters in Description ($input{'desc'}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
	  exit;
       }

       if (length(trim $input{'desc'}) > $MAXDESC) {
	  status("$login: Limit the length of description to $MAXDESC");
	  exit;
       } 

       if (notName($input{'distribution'})) {
          status("$login: Invalid characters in Distribution. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
	  exit;
       }
 
       if (notDesc($input{'subject'})) {
         status("$login: Invalid characters in Subject. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
	  exit;
       }
 

       # we currently do not support Pager/Fax/VoiceMail.
       # give appropriate error message.
       #if ($input{'atype'} eq "Pager") {
       #   error("Currently VoiceMail/Pager/Fax are not supported.\n");
       #   return;
       #}

       if ($input{'atype'} eq "Fax") {
          status("$login: We have not been able to verify your premium account. Click on the premium services link for more information. <p>We require a US Dollar 15.00 fee to setup your premium membership. In addition you need to add a minimum deposit of US Dollar 15.00 to activate your fax account. This allows you to send faxes. <p>Mail all payments (minimum US Dollar 30.00 by valid bank check) to P.O. Box 360404, Milpitas, CA 95036-0404. USA. Mention your hotdiary member login on the check. <p>To activate your premium service your email address in your member profile must be valid.  Your account will be activated after we receive your check. \n");
          exit;
       }

       if ($input{'atype'} eq "VoiceMail") {
          status("$login: PartyPlanner/Reminder/Calendar Voice service is coming soon.\n");
          exit;
       }


       depositmoney $login;
       $partytab{$entryno}{'dtype'} = trim $input{'dtype'};
       $partytab{$entryno}{'atype'} = trim $input{'atype'};
  
       $partytab{$entryno}{'desc'} = trim $input{'desc'};

       $partytab{$entryno}{'subject'} = trim $input{'subject'};
       $partytab{$entryno}{'zone'} = trim $input{'zone'};

       if (trim $input{'partyedit'} eq "on") {
       		$partytab{$entryno}{'partyedit'} = "CHECKED"; 
       } else {
       		$partytab{$entryno}{'partyedit'} = trim $input{'partyedit'};
       }
       # add the entry in the database.
       $partytab{$entryno}{'month'} = $mo;
       $partytab{$entryno}{'day'} =  $da;
       $partytab{$entryno}{'year'} = $yr;
       $partytab{$entryno}{'hour'} = trim $input{'hour'};
       if (trim $input{'min'} eq "0") {
         $partytab{$entryno}{'min'} = '00';
       } else {
         $partytab{$entryno}{'min'} = trim $input{'min'};
       }
       #$partytab{$entryno}{'sec'} = trim $input{'sec'};    
       $partytab{$entryno}{'meridian'} = trim $input{'meridian'};    
       $partytab{$entryno}{'dhour'} = trim $input{'dhour'};    
       if (trim $input{'dmin'} eq "0") {
         $partytab{$entryno}{'dmin'} = '00';
       } else {
         $partytab{$entryno}{'dmin'} = trim $input{'dmin'};
       }
 
       # send mail to  distribution list and also to the owner.
       $ts = trim $input{'distribution'};

       $pgroups = trim $input{pgroups};
       #hddebug "pgroups = $pgroups";

       $pgroups .= " ";
       $ts = $ts . " " . $pgroups;
       $ts =~ s/No Group//g;
       $ts = trim $ts;

       #if ((length $ts) eq "0") {
       #   status("$login: There are no members specified in the party invitees field, other than yourself. Please enter valid member logins or groups in the party invitees field. <p>Note: If you are not planning to invite any member or group to this Party, you can use Reminders instead. Reminders are personal appointments.");
       #   exit;
       #}

       $distr = $ts;
       $partytab{$entryno}{'distribution'} = $distr;
       if ($input{sendnow} ne "on") {
          tied(%partytab)->sync();
       }
	
       @hsh = split(" ", $ts);
       #print $#hsh;
       #print @hsh[0];
       $ts = "";
       #@hsh[0] = "\b@hsh[0]";
       $desc = trim $input{'desc'};
       $hour = trim $input{'hour'};
       $min = trim $input{'min'};
       #$sec = trim $input{'sec'};
       $meridian = trim $input{'meridian'};
       $dtype = trim $input{'dtype'};
       #print "desc = ", $desc, "\n";

       ($mfile = "$ENV{HDHOME}/tmp/partyadd$$.html") =~ s/\n/\n<BR>/g;
       open thandle, ">$mfile";
       printf thandle "$partymsg";
       printf thandle "Dear HotDiary Member,<BR><BR>";
       if ($input{sendnow} ne "on") {
          printf thandle "Your Party Reminder Follows:<BR>";
       } else {
          printf thandle "You have received an invitation for a party from $login ($logtab{$login}{fname} $logtab{$login}{lname}):<BR><BR>";
       }
       printf thandle "Party Details: $desc<BR>";
       printf thandle "Party Organizer ID: $login<BR>";
       printf thandle "Party Invitees: $distr<BR>";
       printf thandle "Date Of Party: $mo/$da/$yr<BR>";
       if ($min eq "0") {
          $min = "00";
       }
       printf thandle "Time Of Party: $hour:$min $meridian <BR>";
       printf thandle "Party Reminder Type: $dtype <BR>";
       if ($input{sendnow} ne "on") {
           printf thandle "Entry number to search for your party reminder is %s\n", $entryno;
           printf thandle "(Please keep the above number carefully. You will need it to access your appointment)<BR>";
       } 
       printf thandle "HotDiary - New Generation Internet Organizer, http://www.hotdiary.com.<BR>";
       printf thandle "$partyendmsg";
       &flush(thandle);         

       $kfile = "$ENV{HDHOME}/tmp/partyadd$$.html";
       
       $subject = trim $input{'subject'};

       $atype = $input{'atype'};
       if ($atype eq "Email") {
       # send email to distribution 
          foreach $i (@hsh) {
	     #print "i=", $i, "\n";
             #bind lgrouptab table vars
             tie %lgrouptab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
               SUFIX => '.rec',
               SCHEMA => {
                    ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
             tie %plgrouptab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
               SUFIX => '.rec',
               SCHEMA => {
                    ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

             if ((!exists $logtab{$i}) && (!exists $lgrouptab{$i}) && (!exists $plgrouptab{$i})) {
	        status("$i: is not valid login or group in $p2");
	        exit;
	     } else {
                if (exists $logtab{$i}) {
	           $email = $logtab{$i}{'email'};
                   if ($email ne "") {
		       #hddebug "came to metasend";
                      #system "/bin/mail -s \"$subject\" $email < $mfile";
system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
			

                      $alphi = substr $i, 0, 1;
                      $alphi = $alphi . '-index';
                      if ($input{sendnow} ne "on") {
                         system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/$alphi/$i/appttab";
                         system "echo $entryno >> $ENV{HDDATA}/$alphi/$i/apptentrytab";
                         # bind remind index table vars
                         tie %remindtab, 'AsciiDB::TagFile',
                         DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
                         SUFIX => '.rec',
                         SCHEMA => {
                              ORDER => ['login'] };
                         $remindtab{$i}{login} = $i;
                         tied(%remindtab)->sync();
                         system "chmod 777 $ENV{HDDATA}/aux/remindtab/$i.rec";
                      }
                   }
                } else {
##########################
                   # bind lgrouptab table vars
                         tie %lgrouptab, 'AsciiDB::TagFile',
                         DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                         SUFIX => '.rec',
                         SCHEMA => {
                         ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                         if (exists $lgrouptab{$i}) {
                            system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/listed/groups/$i/appttab";
                            # bind remind index table vars
                            tie %remindtab, 'AsciiDB::TagFile',
                            DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
                            SUFIX => '.rec',
                            SCHEMA => {
                                 ORDER => ['login'] };
                            $remindtab{$i}{login} = $i;
                            tied(%remindtab)->sync();
                            system "chmod 777 $ENV{HDDATA}/aux/remindtab/$i.rec";

                            if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                               tie %usertab, 'AsciiDB::TagFile',
                               DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                               SUFIX => '.rec',
                               SCHEMA => {
                               ORDER => ['login'] };
                               (@records) = sort keys %usertab;
                               if ($#records >= 0) {
                                  for ($q = 0; $q <= $#records; $q = $q+1) {
                                      if (exists $logtab{$records[$q]}) {
                                         $email = $logtab{$records[$q]}{'email'};
                                         if ($email ne "") {
                                            #system "/bin/mail -s \"$subject\" $email < $mfile";
				            system "metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";

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
                                  $alphgf = substr $groupfounder, 0, 1;
                                  $alphgf = $alphgf . '-index';
                                  if (-d "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab",
                                     SUFIX => '.rec',
                                     SCHEMA => {
                                     ORDER => ['login'] };
                                     (@records) = sort keys %gmembertab;
                                     if ($#records >= 0) {
                                        for ($q = 0; $q <= $#records; $q = $q + 1) {
                                           ($user, $domain) = split "\@", $records[$q];
                                           if (exists $logtab{$records[$q]}) {
                                              $email = $logtab{$records[$q]}{'email'};
                                              if ($email ne "") {
                                                 #system "/bin/mail -s \"$subject\" $email < $mfile";
				                 system "metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
                                              }

                                           } else {
    if ( ((trim $user) ne "") && ((trim $domain) ne "") ) {
       #system "/bin/mail -s \"$subject\" $records[$q] < $mfile";
       system "metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$records[$q]\" -F noreply\@hotdiary.com";
    }
                                           }
                                        }
                                     }
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $email = $logtab{$groupfounder}{'email'};
                                     if ($email ne "") {
                                        #system "/bin/mail -s \"$subject\" $email < $mfile";
       	                                system "metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
                                     }
                                  }
                               }
                            }
                         }
##########################
                }
	     }
          }
       } else {
       # send pager to distribution 
          foreach $i (@hsh) {
             tie %lgrouptab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
               SUFIX => '.rec',
               SCHEMA => {
                    ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
             tie %plgrouptab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
               SUFIX => '.rec',
               SCHEMA => {
                    ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

             if ((!exists $logtab{$i}) && (!exists $lgrouptab{$i}) && (!exists $plgrouptab{$i})) {
	        error("$login: $i is not valid login or group in $p2");
	        exit;
	     } else {
                if (exists $logtab{$i}) {
	           $pager = $logtab{$i}{'pager'};
                   $toname = $logtab{$i}{'fname'};
                   $from = $logtab{$login}{'fname'};
                   if ($input{sendnow} ne "on") {
                      $alphi = substr $i, 0, 1;
                      $alphi = $alphi . '-index';
                      system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/$alphi/$i/appttab";
                      system "echo $entryno >> $ENV{HDDATA}/$alphi/$i/apptentrytab";
                      # bind remind index table vars
                      tie %remindtab, 'AsciiDB::TagFile',
                      DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
                      SUFIX => '.rec',
                      SCHEMA => {
                           ORDER => ['login'] };
                      $remindtab{$i}{login} = $i;
                      tied(%remindtab)->sync();
                      system "chmod 777 $ENV{HDDATA}/aux/remindtab/$i.rec";
                   }
                   if ($pager ne "") {
                      system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                   }
                } else {
##########################
                   # bind lgrouptab table vars
                         tie %lgrouptab, 'AsciiDB::TagFile',
                         DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                         SUFIX => '.rec',
                         SCHEMA => {
                         ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                                        'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                         if (exists $lgrouptab{$i}) {
                            system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/listed/groups/$i/appttab";
                            if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                               tie %usertab, 'AsciiDB::TagFile',
                               DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                               SUFIX => '.rec',
                               SCHEMA => {
                               ORDER => ['login'] };
                               (@records) = sort keys %usertab;
                               if ($#records >= 0) {
                                  for ($q = 0; $q <= $#records; $q = $q+1) {
                                      if (exists $logtab{$records[$q]}) {
	                                 $pager = $logtab{$records[$q]}{'pager'};
                                         $toname = $logtab{$records[$q]}{'fname'};
                                         $from = $logtab{$login}{'fname'};
                                         if ($pager ne "") {
                                            system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
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
                               $alphgf = substr $groupfounder, 0, 1;
                               $alphgf = $alphgf . '-index';
                               if ($groupfounder ne "") {
                                  if (-d "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab",
                                     SUFIX => '.rec',
                                     SCHEMA => {
                                     ORDER => ['login'] };
                                     (@records) = sort keys %gmembertab;
                                     if ($#records >= 0) {
                                        for ($q = 0; $q <= $#records; $q = $q+1) {
	 				   $smail = $records[$q];
                                           if ((index ($smail, '@')) == -1) {
                                             if (exists $logtab{$records[$q]}) {
	                                      $pager = $logtab{$records[$q]}{'pager'};
                                              $toname = $logtab{$records[$q]}{'fname'};
                                              $from = $logtab{$login}{'fname'};
                                              if ($pager ne "") {
                                                 system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                                              }
                                             }
                                           }
                                        }
                                     }
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $pager = $logtab{$groupfounder}{'pager'};
                                     $toname = $logtab{$groupfounder}{'fname'};
                                     $from = $logtab{$groupfounder}{'fname'};
                                     if ($pager ne "") {
                                        system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                                     }
                                  }
                               }
                            }
                         }

##########################
                }
	     }
          }
     
       }
       #send email to the owner also
       #print "login = ", $login, "\n";
       if (!exists $logtab{$login}) {
	  error("$login: $login is not a valid login in $p2.");
	  exit;
       } else { 
            if ($atype eq "Email") {
	      $email = $logtab{$login}{'email'};
              if ($email ne "") {
                 #system "/bin/mail -s \"$subject\" $email < $mfile";
                 system "metasend -b -S 800000 -m \"text/html\" -f $kfile -s \"$subject\" -e \"\" -t \"$email\" -F noreply\@hotdiary.com";
              }
            } else {
              if ($atype eq "Pager") {
	        $pager = $logtab{$login}{'pager'};
                $from = $logtab{$login}{'fname'};
                $toname = $logtab{$login}{'fname'};
                if ($pager ne "") {
                   system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                }
              }
            }
       }
 
       if ($input{sendnow} eq "on") {
          status("$login: Party invitation has been sent to invitees. ($partytab{$entryno}{'distribution'}).\n");   
       } else {
          status("$login: Party event has been added.\n");   
       }
   }

# save the info in db
   if ($input{sendnow} ne "on") {
      tied(%partytab)->sync();
   }

   if ($action eq "Search") {
      $dist_flag = 0;
      $owner_flag = 0;

      if ($os ne "nt") {
         $execshowpartyentry =  encurl "execshowpartyentry.cgi";
         $execsavepartyentry =  encurl "execsavepartyentry.cgi";
      } else {
         $execshowpartyentry =  "execshowpartyentry.cgi";
         $execsavepartyentry =  "execsavepartyentry.cgi";
      }

      $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
      $msg .= "<TR BGCOLOR=dddddd>";
      $msg .= "<TD></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Party Organizer</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Date Of Party</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Time Of Party</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Duration Of Party</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Party Details</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">More</FONT></TD>";
      $msg .= "</TR>";
      $smsg = $msg;
      $umsg = $msg;
      $cntr = 0;

      $title = time();
      $found_counter = 0;
      $mo = trim $input{'month'};
      $yr = trim $input{'year'};

      #$tfile = "$ENV{HDDATA}/partyentrytab";
      #open thandle, "+<$tfile";
      #while (<thandle>) {
      #   chop;
      #   $onekey = $_;
      
      foreach $onekey (sort keys %partytab) {
         $collmatch = "";
         $dist_flag = 0;
         if ($onekey ne "")  {
            if (exists $partytab{$onekey}) {
               $collmatch = "true";
            }
            # check for entryno entered by the user.
            # check for login and compare it with distribution list.
            # if it matches in the distribution list or it is the owner
            # then proceed or give an error.
            #if (($collmatch eq "") || ($collmatch eq "true")) {
               #if ((($collmatch eq "") || ($collmatch eq "true")) {
	          if ($partytab{$onekey}{'login'} ne $login) {
		     $owner_flag = 0;

		     $ts = $partytab{$onekey}{'distribution'};
                     @hsh = split(" ", $ts);
                     #print $#hsh;
                     #print @hsh[0];
                     $ts = ""; 
                     #@hsh[0] = "\b@hsh[0]";
                     foreach $i (@hsh) {
                        if ($ts eq "") {
                           $ts = "$i"; 
                        } else {
                          $ts = "$ts $i";
		        }
		        #print "i = ", $i, "\n";
		        #found the distributor
		        if ($i eq $login) {
			   $dist_flag = 1;
			   #print "set dist flag \n";
		        } else {
                           tie %lgrouptab, 'AsciiDB::TagFile',
                             DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                             SUFIX => '.rec',
                             SCHEMA => {
                               ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                           if (exists $lgrouptab{$i}) {
                              if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                                 tie %usertab, 'AsciiDB::TagFile',
                                   DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                                   SUFIX => '.rec',
                                   SCHEMA => {
                                   ORDER => ['login'] };
                                 if (exists $usertab{$login}) {
                                    $dist_flag = 1;
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
                                    $alphgf = substr $groupfounder, 0, 1;
                                    $alphgf = $alphgf . '-index';
                                    if (-d "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab") {
                                       tie %gmembertab, 'AsciiDB::TagFile',
                                       DIRECTORY => "$ENV{HDDATA}/groups/$alphgf/$groupfounder/personal/$i/gmembertab",
                                       SUFIX => '.rec',
                                       SCHEMA => {
                                       ORDER => ['login'] };
                                    }
                                    if (exists $gmembertab{$login}) {
                                       $dist_flag = 1;
                                    } else {
    if (exists $gmembertab{$logtab{$login}{'email'}}) {
       $dist_flag = 1;
    }
                                    }
                                  }
                               }
                           }
                        }
		     }
	          } else {
		     $owner_flag = 1;
	             #hddebug "set owner flag";
	          }
	
                  if ($owner_flag == 0) {
		     if ($dist_flag == 0) {
                        if ($collmatch eq "") {
		           status("$login: You do not have the permission to access this party reminder.");
		           exit;
                        } else {
                             next;
                        }
                     }
	          }
	          #hddebug "onekey = $onekey";
	          $cntr = $cntr +1;
	          $msg = "<TR>";
	          $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$onekey></FONT></TD>";
	          $cdir .= $onekey;
	          $cdir .= " ";
		  $organizer = $partytab{$onekey}{login};
	          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$organizer}{'fname'}&nbsp;$logtab{$organizer}{'lname'} &nbsp;($organizer)</FONT></TD>";
		  
	          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$partytab{$onekey}{'month'}/$partytab{$onekey}{'day'}/$partytab{$onekey}{year}&nbsp;</FONT></TD>";
	          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$partytab{$onekey}{'hour'}:$partytab{$onekey}{'min'}$partytab{$onekey}{meridian}&nbsp;</FONT></TD>";
	          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$partytab{$onekey}{'dhour'}:$partytab{$onekey}{'dmin'}&nbsp;</FONT></TD>";
	          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$partytab{$onekey}{'subject'}-$partytab{$onekey}{atype}&nbsp;</FONT></TD>";
                  $moreurl = adjusturl("execdogeneric.cgi?pnum=4&p0=$execshowpartyentry&p1=biscuit&p2=entryno&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&entryno=$onekey&rh=$rh&jp=$jp&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6");
                  $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$moreurl\">More</a>&nbsp;</FONT></TD>";
	          $msg .= "</TR>";

	 	  if (exists $partytab{$onekey}) { 
		      $smsg .= $msg;
		  } else {
	              $umsg .= $msg;
                  }
                #}
	     #}
          }
        }
   }

   if ($action eq "Search") {
      if ($cntr == 0) {
         status ("$login: You currently do not have any parties planned in party organizer."); 
         exit;
      }

      (@hshcdir) = split " ", $cdir;
      foreach $cn (@hshcdir) {
          $cn = trim $cn;
      }

 
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      $smsg = adjusturl $smsg;

      $prb = "";
      if ($logo ne "") {
            $logo = adjusturl $logo;
      }
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";
      $prb = strapp $prb, "label1=Party Planner/Party Reminder/Calendar";
      $prb = strapp $prb, "label2=Use More Link to edit and save the party details.";
      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execmembersdir = encurl "execmembersdir.cgi";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
         $execpartyaddsearch =  encurl "execpartyaddsearch.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execmembersdir = "execmembersdir.cgi";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execpartyaddsearch =  "execpartyaddsearch.cgi";
      }

      if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/partydir.html") ) {
         $template = "$ENV{HDDATA}/$alphjp/$jp/templates/partydir.html";
      } else {
         $template = "$ENV{HDTMPL}/partydir.html";
      }  
      $prb = strapp $prb, "template=$template";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/partydir-$$.html";
      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "jp=$jp";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavepartyentry\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=delete>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=jp>";

      #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 6;
      $numend = $mcntr;
      $numbegin = $mcntr;
      # this tells from where the parameter for selection starts
      foreach $cn (@hshcdir) {
         $cn = trim $cn;
         $numend = $numend + 1;

 	 #hddebug "p$mcntr, box$k, $cn";
         #$bizdir .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
         #$bizdir .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
         #$bizdir .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";

         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $k = $k + 1;
      }
      $numend = $numend - 1;

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";
      $hiddenvars = adjusturl $hiddenvars;
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "bizdir=$smsg";
      $prb = strapp $prb, "status=";
      $bizlabel = "$login - Party Planner";
      $prb = strapp $prb, "bizlabel=$bizlabel";
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
      $prb = strapp $prb, "status=Click checkboxes to delete the party events.";
      parseIt $prb;

      #system "cat $ENV{HDTMPL}/content.html";
      #system "cat $ENV{HDHREP}/$alphaindex/$login/partydir.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/partydir-$$.html";
   }

   if ($action eq "Add") {
      system "rm $ENV{HDHOME}/tmp/partyadd$$.html";
   }


   tied(%sesstab)->sync();
   tied(%logsess)->sync();

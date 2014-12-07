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
# FileName: savepartyentry.cgi
# Purpose: displays partyentry details
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

   hddebug "savepartyentry.cgi";

   $vdomain = trim $input{'vdomain'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $rh = trim $input{'rh'};
   $jp = $input{jp};
   hddebug "jp = $jp";
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};

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


   if ($os ne "nt") {
      $execpartyaddsearch = encurl "execpartyaddsearch.cgi";
   } else {
      $execpartyaddsearch = "execpartyaddsearch.cgi";
   }
   $search = "Search";

   $k = 0;
   if ($input{delete} ne "") {
      $numbegin = $input{numbegin}; 
      $numend = $input{numend}; 
      for ($i = $numbegin; $i <= $numend; $i= $i + 1) {
         $entryno = $input{"box$k"};
	 hddebug "entryno = $entryno";
         $checkboxval = $input{$entryno};
         if ($checkboxval eq "on") {
             delete $partytab{$entryno};
         }
         $k = $k + 1;
       }
       tied(%sesstab)->sync();
       tied(%logsess)->sync();
       tied(%partytab)->sync();
       status("$login: Party event(s) have been deleted. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execpartyaddsearch&p1=biscuit&p2=search&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&search=$search&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to party events list.");
       exit;
   }

   $entryno = $input{entryno};

   $pagenum = 0;
   $nextpage = 0;
   $prevpage = 0;

   #save party event
   #$partytab{$entryno}{'entryno'} = $entryno;
   $partytab{$entryno}{'login'} = $login;

       
   $mo = trim $input{'month'};
   $da = trim $input{'day'};
   $yr = trim $input{'year'};
   hddebug "mo = $mo";
   hddebug "da = $da";
   hddebug "yr = $yr";

       
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

       $subject = $input{subject};
       hddebug "subject = $subject"; 
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

       $partyedit = $input{partyedit};
       hddebug "partyedit = $partyedit";
       if (trim $input{'partyedit'} eq "on") {
       		$partytab{$entryno}{'partyedit'} = "CHECKED"; 
       } else {
       		$partytab{$entryno}{'partyedit'} = trim $input{'partyedit'};
       }
       # add the entry in the database.
       $partytab{$entryno}{'month'} = $mo;
       $partytab{$entryno}{'day'} =  $da;
       $partytab{$entryno}{'year'} = $yr;
       $hour = $input{hour};
       hddebug "hour = $hour";

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
       $pgroups = multselkeys $input, "pgroups";
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

       $mimetype = "text/html";
       $partymsg = "<HTML> <BODY> <FONT FACE=\"Verdana\"><TABLE><TR><TD>";
       $partymsg .= "<IMG SRC=\"http://www.hotdiary.com/images/balloon6.gif\" WIDTH=\"60\" HEIGHT=\"100\"></TD><TD><H3>HotDiary Party Invitation</h3></TD></TR></TABLE>";

       $partymsg .= "<p align=\"justify\">";
       $partyendmsg = "</p><p><a href=\"http://www.hotdiary.com\">http://www.hotdiary.com</a>";
       $partyendmsg .= "</FONT></BODY></HTML>";

       ($mfile = "$ENV{HDHOME}/tmp/partyadd$$.html") =~ s/\n/\n<BR>/g;
       open thandle, ">$mfile";
       printf thandle "$partymsg<BR>";
       printf thandle "Dear HotDiary Member<BR><BR>";
       if ($input{sendnow} ne "on") {
          printf thandle "Your Party Reminder Follows:<BR>";
       } else {
	  $partylogin = $partytab{$entryno}{login};
          printf thandle "You have received an invitation for a party from $logtab{$partylogin}{fname} $logtab{$partylogin}{lname} ($partylogin):<BR><BR>";
 
       }
       printf thandle "Description: $desc <BR>";
       printf thandle "Owner ID: $login <BR>";
       printf thandle "Invitees: $distr <BR>";
       printf thandle "Date: $mo/$da/$yr <BR>";
       if ($min eq "0") {
          $min = "00";
       }
       printf thandle "Time: $hour:$min $meridian <BR>";
       printf thandle "Reminder Type: $dtype <BR>";

       #if ($input{sendnow} ne "on") {
       #    printf thandle "Entry number to search for your party reminder is %s\n", $entryno;
       #    printf thandle "(Please keep the above number carefully. You will need it to access your appointment)\n\n";
       #} 
       #printf thandle "Description: $desc\n";


       printf thandle "HotDiary - New Generation Internet Organizer, http://www.hotdiary.com.";
       printf thandle "$partyendmsg";
       &flush(thandle);         
       
       $subject = trim $input{'subject'};
       #print "subject = ", $subject, "\n";

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
                      system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $email -F $vdomain\@$vdomain.com";
                      $alp = substr $i, 0, 1;
                      $alp = $alp . '-index';
                      if ($input{sendnow} ne "on") {
                         system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/$alp/$i/appttab";
                         system "echo $entryno >> $ENV{HDDATA}/$alp/$i/apptentrytab";
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
					    system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $email -F $vdomain\@$vdomain.com";
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
                               $alpgf = $alpgf, 0, 1;
                               if ($groupfounder ne "") {
                                  if (-d "$ENV{HDDATA}/groups/$alpgf/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$alpgf/$groupfounder/personal/$i/gmembertab",
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
					         system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $email -F $vdomain\@$vdomain.com";
                                              }

                                           } else {
    if ( ((trim $user) ne "") && ((trim $domain) ne "") ) {
       #system "/bin/mail -s \"$subject\" $records[$q] < $mfile";
       system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $records[$q] -F $vdomain\@$vdomain.com";
    }
                                           }
                                        }
                                     }
# The groupfounder is not included in gmembertab, so we explictly send this.
                                     $email = $logtab{$groupfounder}{'email'};
                                     if ($email ne "") {
                                        #system "/bin/mail -s \"$subject\" $email < $mfile";
				        system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $email -F $vdomain\@$vdomain.com";
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
                   $alpi = substr $i, 0, 1;
                   $alpi = $alpi . '-index';
                   if ($input{sendnow} ne "on") {
                      system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/$alpi/$i/appttab";
                      system "echo $entryno >> $ENV{HDDATA}/$alpi/$i/apptentrytab";
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
                 system "metasend -b -S 800000 -m $mimetype -f $mfile -s \"$subject\" -e \"\" -t $email -F $vdomain\@$vdomain.com";
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
      status("$login: Party message has been sent to $partytab{$entryno}{'distribution'}.\n");   
   } else {
      status("$login: Party event has been saved. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execpartyaddsearch&p1=biscuit&p2=search&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&search=$search&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to party events list.");   
   }

# save the info in db
   if ($input{sendnow} ne "on") {
      tied(%partytab)->sync();
   }

   system "rm $ENV{HDHOME}/tmp/partyadd$$.html"; 
   tied(%sesstab)->sync();
   tied(%logsess)->sync();


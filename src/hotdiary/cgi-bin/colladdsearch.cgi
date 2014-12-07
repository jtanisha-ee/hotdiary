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
# FileName: colladdsearch.cgi
# Purpose: it adds and searches the collabrum appointments.
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXDESC = 4096;

# parse the command line
   &ReadParse(*input); 

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Add Collabrum"); 
   #print &PrintVariables(*input);
   #local (*in) = @_ if @_ == 1;
   #local (%in) = @_ if @_ > 1;
   #local ($out, $key, $output);
#
   #$output =  "\n<dl compact>\n";
   #foreach $key (sort keys(%input)) {
   #  if ((index $key, "pgroups") == 0) {
   #     foreach (split("\0", $input{$key})) {
   #       ($out = $_) =~ s/\n/<br>\n/g;
   #       $output .=  "<dt><b>$key</b>\n <dd>:<i>$out</i>:<br>\n";
   #     }
   #  }
   #}
   #$output .=  "</dl>\n";
   #print $output;
   #exit;


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


   $biscuit = trim $input{'biscuit'};

   if ($input{'add.x'} ne "") {
      $action = "Add";
   } else {
      if ($input{'search.x'} ne "") {
        $action = "Search";
      }
   }
   hddebug "action = $action";

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
      		error("Login  is an empty string.\n");
                exit;
           }
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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


#
# bind collabrum entry number table vars
#   tie %apptnotab, 'AsciiDB::TagFile',
#   DIRECTORY => "$ENV{HDDATA}/apptnotab",
#   SUFIX => '.rec', 
#   SCHEMA => { 
#	ORDER => ['entryno'] };
#
# biscuit generation
#   @allkeys = keys %apptnotab;
#   $oldentryno = $allkeys[0];
#
#   if ($oldentryno eq '9999999') {
#      $entryno = '9999';
#   } else {
#      $entryno = $oldentryno + 1;
#   }
#   $apptnotab{$entryno}{'entryno'} = $entryno;
#   delete $apptnotab{$oldentryno};

   # get entry number
   $entryno = getkeys();

   if ($action eq "Add") {
       #add a new collarbum 
       $colltab{$entryno}{'entryno'} = $entryno;
       $colltab{$entryno}{'login'} = $login;

       
       $mo = trim $input{'month'};
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
             status("$login: You can only set reminders which are due in the future, atleast 20 minutes past current time.");
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
          status("$login: Collaborative Voice service is coming soon.\n");
          exit;
       }


       depositmoney $login;
       $colltab{$entryno}{'dtype'} = trim $input{'dtype'};
       $colltab{$entryno}{'atype'} = trim $input{'atype'};
  
       $colltab{$entryno}{'desc'} = trim $input{'desc'};

       $colltab{$entryno}{'subject'} = trim $input{'subject'};
       $colltab{$entryno}{'zone'} = trim $input{'zone'};

       if (trim $input{'colledit'} eq "on") {
       		$colltab{$entryno}{'colledit'} = "CHECKED"; 
       } else {
       		$colltab{$entryno}{'colledit'} = trim $input{'colledit'};
       }
       # add the entry in the database.
       $colltab{$entryno}{'month'} = $mo;
       $colltab{$entryno}{'day'} =  $da;
       $colltab{$entryno}{'year'} = $yr;
       $colltab{$entryno}{'hour'} = trim $input{'hour'};
       if (trim $input{'min'} eq "0") {
         $colltab{$entryno}{'min'} = '00';
       } else {
         $colltab{$entryno}{'min'} = trim $input{'min'};
       }
       #$colltab{$entryno}{'sec'} = trim $input{'sec'};    
       $colltab{$entryno}{'meridian'} = trim $input{'meridian'};    
       $colltab{$entryno}{'dhour'} = trim $input{'dhour'};    
       if (trim $input{'dmin'} eq "0") {
         $colltab{$entryno}{'dmin'} = '00';
       } else {
         $colltab{$entryno}{'dmin'} = trim $input{'dmin'};
       }
       #$colltab{$entryno}{'sec'} = trim $input{'sec'};    
       if ($input{sendnow} ne "on") {
          # add the entry in the collentrytab/$login.
          $tfile = "$ENV{HDDATA}/collentrytab";
          open thandle, ">>$tfile";
          printf thandle "%s\n", $entryno;
          close thandle;
       }
 
       # send mail to  distribution list and also to the owner.
       $ts = trim $input{'distribution'};
       $pgroups = multselkeys $input, "pgroups";
       $pgroups .= " ";
       $ts = $ts . " " . $pgroups;
       $ts =~ s/No Group//g;
       $ts = trim $ts;
       if ((length $ts) eq "0") {
          status("$login: There are no members specified in the distribution field, other than yourself. Please enter valid member logins or groups in the distribution field. <p>Note: If you are not planning to invite any member or group to this Collabrum, you can use Reminders instead. Reminders are personal appointments.");
          exit;
       }
       $distr = $ts;
       $colltab{$entryno}{'distribution'} = $distr;
       if ($input{sendnow} ne "on") {
          tied(%colltab)->sync();
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

       ($mfile = "/tmp/colladd$$.txt") =~ s/\n/\n<BR>/g;
       open thandle, ">$mfile";
       printf thandle "Dear HotDiary Member,\n\n";
       #printf thandle "You have been invited to a collaborative appointment.  Please read the notes below for details.\n\n";
       #printf thandle "Regards\n";
       #printf thandle "HotDiary Inc.\n\n";
       if ($input{sendnow} ne "on") {
          printf thandle "Your Collabrum Reminder Follows:\n\n";
       } else {
          printf thandle "You have received a group broadcast message:\n\n";
       }
       #printf thandle "Entry number to search for your collabrum appointment is %s\n", $entryno;
       #printf thandle "(Please keep the above number carefully. You will need it to access your appointment)\n\n";
       #printf thandle "Owner: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
       printf thandle "From: $login\n";
       printf thandle "Description: $desc\n";
       printf thandle "Owner ID: $login\n";
       printf thandle "Invitees: $distr\n";
       printf thandle "Date: $mo/$da/$yr \n";
       if ($min eq "0") {
          $min = "00";
       }
       printf thandle "Time: $hour:$min $meridian \n";
       printf thandle "Reminder Type: $dtype \n";
       if ($input{sendnow} ne "on") {
           printf thandle "Entry number to search for your collabrum reminder is %s\n", $entryno;
           printf thandle "(Please keep the above number carefully. You will need it to access your appointment)\n\n";
       } 
       #printf thandle "Description: $desc\n";
       printf thandle "\nHotDiary - New Generation Internet Organizer, http://www.hotdiary.com.";
       #printf thandle "%s\n", $desc; 
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
                      system "/bin/mail -s \"$subject\" $email < $mfile";
                      if ($input{sendnow} ne "on") {
                         system "cp $ENV{HDDATA}/colltab/$entryno.rec $ENV{HDDATA}/$i/appttab";
                         system "echo $entryno >> $ENV{HDDATA}/$i/apptentrytab";
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
                            system "cp $ENV{HDDATA}/colltab/$entryno.rec $ENV{HDDATA}/listed/groups/$i/appttab";
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
                                  if (-d "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab",
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
                                                 system "/bin/mail -s \"$subject\" $email < $mfile";
                                              }

                                           } else {
    if ( ((trim $user) ne "") && ((trim $domain) ne "") ) {
       system "/bin/mail -s \"$subject\" $records[$q] < $mfile";
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
                      system "cp $ENV{HDDATA}/colltab/$entryno.rec $ENV{HDDATA}/$i/appttab";
                      system "echo $entryno >> $ENV{HDDATA}/$i/apptentrytab";
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
                            system "cp $ENV{HDDATA}/colltab/$entryno.rec $ENV{HDDATA}/listed/groups/$i/appttab";
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
                               if ($groupfounder ne "") {
                                  if (-d "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab") {
                                     tie %gmembertab, 'AsciiDB::TagFile',
                                     DIRECTORY => "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab",
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
                 system "/bin/mail -s \"$subject\" $email < $mfile";
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
          status("$login: Collabrum message has been sent to $colltab{$entryno}{'distribution'}.\n");   
       } else {
          status("$login: Collabrum entry has been added.\n");   
       }
   }

#intialize the flags for distributor 
   $dist_flag = 0;
   $owner_flag = 0;

   if ($action eq "Search") {
    
      system "/bin/rm -f $ENV{HDREP}/$login/ser*.html"; 
      $title = time();
      $entryno = trim $input{'entryno'};
      #print "entryno = ", $entryno, "\n";
      #$month = trim $input{'month'};
      $found_counter = 0;
      $page_entries = 0;
      $page_num = 0;
      $prevpage = "";
      $nextpage = "";
      $mo = trim $input{'month'};
      $yr = trim $input{'year'};
      $collmatch = "";
      $collentry = "";

#      #go through each entry in the collabrum table.
#      # @allkeys = keys %colltab;

      $tfile = "$ENV{HDDATA}/collentrytab";
      open thandle, "+<$tfile";
      while (<thandle>) {
         chop;
         $onekey = $_;
         $dist_flag = 0;

         if ($onekey ne "")  {

            #print if collabrum  record exists with firstname.
            #print "month ", $month;
	    #print "onekey = $onekey<BR>";
	    #if (exists $colltab{$onekey}) {
		#print "colltab:month =", $colltab{$onekey}{'month'};
	    #}
            $collmatch = "";
            if ($entryno eq "") {
               if (exists $colltab{$onekey}) {
                  #print "$colltab{$onekey}{'month'} $colltab{$onekey}{'year'}<BR>";
                  if (($mo eq $colltab{$onekey}{'month'}) && ($yr eq $colltab{$onekey}{'year'})) {
                     $collmatch = "true";
                     $collentry = $colltab{$onekey}{'entryno'};
                  }
               }
            } else {
               $collmatch = "";
               $collentry = $entryno;
            }

            # check for entryno entered by the user.
            # check for login and compare it with distribution list.
            # if it matches in the distribution list or it is the owner
            # then proceed or give an error.

            if ((($onekey eq $entryno) && ($collmatch eq "")) || ($collmatch eq "true")) {

               #print "came here";
               if ((($colltab{$onekey}{'entryno'} eq $entryno) && ($collmatch eq "")) ||
                   ($collmatch eq "true")) {

	          if ($colltab{$onekey}{'login'} ne $login) {
		     $owner_flag = 0;

		     $ts = $colltab{$onekey}{'distribution'};
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
                                    if (-d "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab") {
                                       tie %gmembertab, 'AsciiDB::TagFile',
                                       DIRECTORY => "$ENV{HDDATA}/groups/$groupfounder/personal/$i/gmembertab",
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
	             #print "set owner flag \n";
	          }
	

                  if ($owner_flag == 0) {
		     if ($dist_flag == 0) {
                        if ($collmatch eq "") {
		           status("$login: You do not have the permission to access this collabrum appointment.");
		           exit;
                        } else {
                             next;
                        }
                     }
	          }

                  $found_counter= $found_counter + 1;
                  $page_entries = $page_entries + 1;
                  if ($page_entries eq 1) {
                     $page_num = $page_num + 1;
                  }
                  #print "page_num = ", $page_num, "\n";
                  if ($page_num eq 1) {
                     $prevpage = "rep/$login/ser$title$biscuit$page_num.html";
                  } else {
                     $pageno = $page_num - 1;
                     $prevpage = "rep/$login/ser$title$biscuit$pageno.html";
                  }
                  $pageno = $page_num + 1;
                  if ($page_num eq 1) {
                     $nextpage = "rep/$login/ser$title$biscuit$pageno.html";
                  } else {
                     $nextpage = "rep/$login/ser$title$biscuit$pageno.html";
                  }
                  #print "nextpage = ", $nextpage, "\n";
                  #print "prevpage = ", $prevpage, "\n";

                  # this is commented out on april 10th.
                  #($entryno = $colltab{$onekey}{'entryno'}) =~ s/\n/\n<BR>/g;
                  #print "Entryno = ", $entryno, "\n";
	          $prml = "";
                  #$prml = strapp $prml, "entrynfield=entryn$found_counter";
                  $prml = strapp $prml, "entrynfield=entryn$page_entries";
                  $prml = strapp $prml, "entryno=$onekey";

	          $prml = strapp $prml, "checkboxfield=checkbox$onekey";

                  ($outfield = $colltab{$onekey}{'month'}) =~ s/\n/\n<BR>/g;
                  #print "Month Num = ", $outfield, "\n";
                  $prml = strapp $prml, "monthnum=$outfield";
                  $prml = strapp $prml, "montnumfield=montnum$onekey";

                  ($outfield = getmonthstr($colltab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
                  #print "Month = ", $outfield, "\n";
                  $prml = strapp $prml, "month=$outfield";
                  $prml = strapp $prml, "montfield=mont$onekey";


                  #($outfield = $colltab{$onekey}{'month'}) =~ s/\n/\n<BR>/g;
                  ##print "Month = ", $outfield, "\n";
	          #$prml = strapp $prml, "month=$outfield";
                  #$prml = strapp $prml, "montfield=mont$onekey";

                  ($outfield = $colltab{$onekey}{'day'}) =~ s/\n/\n<BR>/g;
	          $prml = strapp $prml, "day=$outfield";
	          $prml = strapp $prml, "dafield=da$onekey";

                  ($outfield = $colltab{$onekey}{'year'}) =~ s/\n/\n<BR>/g;
                  #print "Year = ", $outfield, "\n";
	          $prml = strapp $prml, "year=$outfield";
	          $prml = strapp $prml, "yeafield=yea$onekey";

                  ($outfield = $colltab{$onekey}{'hour'}) =~ s/\n/\n<BR>/g;
                  #print "Hour = ", $outfield, "\n";
	          $prml = strapp $prml, "hour=$outfield";
	          $prml = strapp $prml, "houfield=hou$onekey";

                  ($outfield = $colltab{$onekey}{'min'}) =~ s/\n/\n<BR>/g;
		  if ($outfield eq '00') {
                      $outfield = '0';
                  }
                  #print "Minutes = ", $outfield, "\n";
	          $prml = strapp $prml, "min=$outfield";
	          $prml = strapp $prml, "mifield=mi$onekey";

                  #($outfield = $colltab{$onekey}{'sec'}) =~ s/\n/\n<BR>/g;
                  #print "Seconds = ", $outfield, "\n";
	          #$prml = strapp $prml, "sec=$outfield";
	          #$prml = strapp $prml, "sefield=se$onekey";

                  ($outfield = $colltab{$onekey}{'meridian'}) =~ s/\n/\n<BR>/g;
                  #print "Meridian = ", $outfield, "\n";
	          $prml = strapp $prml, "meridian=$outfield";
	          $prml = strapp $prml, "meridiafield=meridia$onekey";

                  ($outfield = $colltab{$onekey}{'dhour'}) =~ s/\n/\n<BR>/g;
                  #print "Duration Hour = ", $outfield, "\n";
	          $prml = strapp $prml, "dhour=$outfield";
	          $prml = strapp $prml, "dhoufield=dhou$onekey";

                  ($outfield = $colltab{$onekey}{'dmin'}) =~ s/\n/\n<BR>/g;
		  if ($outfield eq '00') {
                     $outfield = '0';
                  }
                  #print "Duration Minutes = ", $outfield, "\n";
      	          $prml = strapp $prml, "dmin=$outfield";
	          $prml = strapp $prml, "dmifield=dmi$onekey";

                  ($outfield = $colltab{$onekey}{'dtype'}) =~ s/\n/\n<BR>/g;
                  #print "Reminder Type = ", $outfield, "\n";
	          $prml = strapp $prml, "dtype=$outfield";
	          $prml = strapp $prml, "dtypfield=dtyp$onekey";

                  ($outfield = $colltab{$onekey}{'atype'}) =~ s/\n/\n<BR>/g;
                  #print "Alarm Type = ", $outfield, "\n";
	          $prml = strapp $prml, "atype=$outfield";
	          $prml = strapp $prml, "atypfield=atyp$onekey";

                  #($outfield = $colltab{$onekey}{'desc'}) =~ s/\n/\n<BR>/g;
                  $outfield = $colltab{$onekey}{'desc'};
	          $outfield = adjusturl($outfield);
                  #print "Description = ", $outfield, "\n";
	          $prml = strapp $prml, "desc=$outfield";
	          $prml = strapp $prml, "desfield=des$onekey";
 
                  $outfield = $colltab{$onekey}{'distribution'};
                  #print "Description = ", $outfield, "\n";
                  $prml = strapp $prml, "distribution=$outfield";
                  $prml = strapp $prml, "distributiofield=distributio$onekey";

                  $outfield = $colltab{$onekey}{'zone'};
                  #print "Zone = ", $outfield, "\n";
                  $prml = strapp $prml, "zone=$outfield";
                  $prml = strapp $prml, "zonfield=zon$onekey";

	          ($outfield = getzonestr($colltab{$onekey}{'zone'})) =~ s/\n/\n<BR>/g;
                  #print "Zone String = ", $outfield, "\n";
                  $prml = strapp $prml, "zonestr=$outfield";
                  $prml = strapp $prml, "zonstrfield=zonstr$onekey";

                  $outfield = $colltab{$onekey}{'subject'};
                  #print "subject = ", $outfield, "\n";
                  $prml = strapp $prml, "subject=$outfield";
                  $prml = strapp $prml, "subjecfield=subjec$onekey";

                  $outfield = $colltab{$onekey}{'colledit'};
                  $prml = strapp $prml, "colledit=$outfield";
                  $prml = strapp $prml, "colledifield=colledi$onekey";

	          $prml = strapp $prml, "template=$ENV{HDTMPL}/searchcolltblentry.html";
	          $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/searchcolltblentry.html";
                  parseIt $prml, 1;
                  $prml = "";

                  if ($page_entries eq 1) {
#                     if ($page_num eq 1 ) {
#                        system "/bin/cat $ENV{HDTMPL}/content.html > $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
#                     }
                     # Generate Search Page Header
                     $prml = strapp $prml, "biscuit=$biscuit";
		     #$expiry = localtime(time() + 5);
                     #$expiry = "\:$expiry";
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/searchpghdr.html";
		     #$prml = strapp $prml, "expiry=$expiry";
		     $prml = strapp $prml, "expiry=";
                     $urlcgi = buildurl("execcollupddel.cgi");
                     $prml = strapp $prml, "actioncgi=$urlcgi";
                     $prml = strapp $prml, "label=$p2 Multi-Group Reminder Search Results";
                     $prml = strapp $prml, "label1=";
                     parseIt $prml, 1;
                     $prml = "";
                     if ($page_num eq 1) {
                       system "/bin/cat $ENV{HDHREP}/$login/searchpghdr.html > $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
                     } else {
                       system "/bin/cat $ENV{HDHREP}/$login/searchpghdr.html > $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
                     }

                     # Generate Standard Table Header
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/stdtblhdr.html";
                     parseIt $prml, 1;
                     $prml = "";
                     system "/bin/cat $ENV{HDHREP}/$login/stdtblhdr.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
	          }

                  system "/bin/cat $ENV{HDHREP}/$login/searchcolltblentry.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
 
                  if ($page_entries eq 2) {
# this is the last time we will use page_entries in this iteration,
# so we can reset it now to 0
                     # Generate Standard Table Footer
                     $prml = strapp $prml, "numentries=$page_entries";
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/stdtblftr.html";
                     $prml = strapp $prml, "nextpage=$nextpage";
                     $prml = strapp $prml, "prevpage=$prevpage";
                     parseIt $prml, 1;
                     $prml = "";
                     system "/bin/cat $ENV{HDHREP}/$login/stdtblftr.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";

                     # Generate Search Page Footer
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/searchpgftr.html";
                     parseIt $prml, 1;
                     $prml = "";
                     system "/bin/cat $ENV{HDHREP}/$login/searchpgftr.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
                  }
                  if ($page_entries eq 2) {
                     $page_entries = 0;
                  }
                }
	     }
          }
        }
         close thandle;

         # deal with cases when the $found_counter are odd numbered
         $rem = $found_counter % 2;
         if ($rem != 0) {
            # Generate Standard Table Footer
            $prml = strapp $prml, "numentries=$page_entries";
            $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/stdtblftr.html";
            $prml = strapp $prml, "nextpage=$nextpage";
            $prml = strapp $prml, "prevpage=$prevpage";
            parseIt $prml, 1;
            $prml = "";
            system "/bin/cat $ENV{HDHREP}/$login/stdtblftr.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";

            # Generate Search Page Footer
            $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/searchpgftr.html";
            parseIt $prml, 1;
            $prml = "";
            system "/bin/cat $ENV{HDHREP}/$login/searchpgftr.html >> $ENV{HDREP}/$login/ser$title$biscuit$page_num.html";
         }


         # overwrite nextpage with lastpage
         $prml = strapp $prml, "template=$ENV{HDTMPL}/lastpage.html";
         $prml = strapp $prml,
                        "prevpage=rep/$login/ser$title$biscuit$page_num.html";
         $pageno = $page_num + 1;
         $prml = strapp $prml, "templateout=$ENV{HDREP}/$login/ser$title$biscuit$pageno.html";
         parseIt $prml, 1;
         $prml = "";
         system "cp $ENV{HDREP}/$login/$biscuit.html $ENV{HDREP}/$login/ser$title$biscuit$pageno.html";

         if ($found_counter eq 0) {
            status("$login: No collabrum appointments were found. You can also search for all collabrum appointments in a specified month, by leaving the entry number field blank.");
	    exit;
         } else {
            #system "/bin/cat $ENV{HDTMPL}/content.html"; 
	    $pagenum = "1";
            #system "/bin/cat $ENV{HDREP}/$login/ser$title$biscuit$pagenum.html";
            hdsystemcat "$ENV{HDREP}/$login/ser$title$biscuit$pagenum.html";
         }
    }

# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 


# save the info in db
   if ($input{sendnow} ne "on") {
      tied(%colltab)->sync();
   }
   tied(%sesstab)->sync();

}

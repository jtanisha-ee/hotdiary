#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: partyupddel.cgi
# Purpose: it updates and deletes the party appointments.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

# parse the command line
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXDESC = 4096;

   $biscuit = $input{'biscuit'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp};
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

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


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

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


   $numentries = $input{'numentries'};
   
   if ($input{'update'} ne "") {
      $action = "Update";
   } else {
   if ($input{'delete'} ne "") {
      $action = "Delete";
   }}

   hddebug "action = $action";

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
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: Your session has already expired.\n");
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

# bind personal party table vars
   tie %partytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min',  'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'subject', 'distribution', 'partyedit',
	'zone'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


#   #initialize the counter
   $num = 1;

   #from the array of entry numbers that are to be deleted.
   for ($i = 0; $i < $numentries; $i = $i + 1) {

        #how do we define an array
        $entry_array[$i] = "entryn$num";
        #print "entry_array =", $entry_array[$i];
        #print "\n";
        $num = $num + 1;
   }

   #initialize the counter
   $found_counter = 0;
   $checknum = 0; 
   $owner_flag = 0;
   $dist_flag = 0;

   for ($l = 0; $l < $numentries; $l = $l + 1) {
       $one_entryno = $entry_array[$l];
       $entryno = $input{$one_entryno};
       #print "entryno = ", $entryno;
       #print "one_entryno = ", $one_entryno;

       # check if checkbox is on.
       $checkbox_e = "checkbox$entryno";
       $checkbox = $input{$checkbox_e};
       #print "cbeckbox = ", $checkbox;

       if ($checkbox eq "on") {
          #print "checkbox is on";
          $checknum = $checknum + 1;

          # check if party record exists.
          if (!exists $partytab{$entryno}) {
             #print "Party record does not exist.\n";
             if ($action eq "Delete") {
                $msg = "$login: Could not find a match for party entry $entryno";
             }
          } else {

              # check if this user is the owner or non-owner. 
              # donot allow the non-owner to update the
              # atype, dtype, cedit, distribution fields. 

              #print "login = ", $login, "\n";
              if ($partytab{$entryno}{'login'} eq $login) {
                  $owner_flag = 1;
		  #print "owner_flag has been set \n";
              } else {
                  #check if this in one of the distributions
                  $ts = $partytab{$entryno}{'distribution'};
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

                     tie %lgrouptab, 'AsciiDB::TagFile',
                       DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                       SUFIX => '.rec',
                       SCHEMA => {
                            ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                     tie %plgrouptab, 'AsciiDB::TagFile',
                       DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
                       SUFIX => '.rec',
                       SCHEMA => {
                            ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
  
                     if (exists $logtab{$i}) {
                        if ($i eq $login) {
                           $dist_flag = 1;
                           #print "set dist flag \n";
                        }
                     } else {
                         if (exists $lgrouptab{$i}) {
# bind subscribed group table vars
                            if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab")) {
                               system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
                               system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
                            }
                            tie %sgrouptab, 'AsciiDB::TagFile',
                            DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
                            SUFIX => '.rec',
                            SCHEMA => {
                                 ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

# bind founded group table vars
                            if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab")) {
                               system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
                               system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
                            }
                            tie %fgrouptab, 'AsciiDB::TagFile',
                            DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
                            SUFIX => '.rec',
                            SCHEMA => {
                                 ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };
                            if (exists $sgrouptab{$i}) {
                               $dist_flag = 1;
                            } else {
                                 if (exists $fgrouptab{$i}) {
                                    $dist_flag = 1;
                                 }
                            }
                         } else {
                              if (exists $plgrouptab{$i}) {
                                 $founder = $plgrouptab{$i}{'groupfounder'};
                                 $alphf = substr $founder, 0, 1;
                                 $alphf = $alphf . '-index';
                                # bind personal group table vars
                                 tie %gmembertab, 'AsciiDB::TagFile',
                                 DIRECTORY => "$ENV{HDDATA}/groups/$alphf/$founder/personal/$i/gmembertab",
                                 SUFIX => '.rec',
                                 SCHEMA => {
                                      ORDER => ['login' ] };
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

              if ($action eq "Update") {

                 #increment the counter
                 $found_counter = $found_counter + 1;
                 #print "entered the update ";

                 #modify/edit an existing party
                 $month_e = "mont$entryno";
                 $mo = trim $input{$month_e};

                 $day_e = "da$entryno";
                 $da = trim $input{$day_e};

                 $year_e = "yea$entryno";
                 $yr = trim $input{$year_e};


                 $zone_e = "zon$entryno";
                 $ezone = trim $input{$zone_e};
                 $event_zone = adjustzone($ezone);

                 $hour_e = "hou$entryno";
                 $ehour = trim $input{$hour_e};

                 $min_e = "mi$entryno";
                 if (trim $input{$min_e} eq "0") {
                    $emin = '00';
                 } else {
                    $emin= trim $input{$min_e};
                 }

                 $meridian_e = "meridia$entryno"; 
                 $meridian = trim $input{$meridian_e};
                 if ( ($meridian eq "PM") && ($ehour ne "12")) {
                      $ehour += 12;
                 }

                 if (($meridian eq "AM") && ($ehour eq "12")){
                      $ehour = 0;
                 }


                 $etime = etimetosec("", $emin, $ehour, $da, $mo, $yr, "", "", "", $event_zone);
                 $ctime = ctimetosec();

                 if ((($etime - $ctime) < 0) || (($etime - $ctime) < 1200)) {
                    status("$login: Set Multi-Group Reminders a minimum of 20 minutes in advance of current time.");
                    exit;
                 }

                 #if (notDate($da, $mo, $yr)) {
                 #   error("$da $mo $yr: invalid date\n");
                 #   return;
                 #} 

                 # we currently do not support Pager/Fax/VoiceMail.
                 # give appropriate error message.
		 $atype_e = "atyp$entryno";
                 #if ($input{$atype_e} eq "Pager") {
                 #   error("Currently VoiceMail/Pager/Fax are not supported.\n");
                 #   return;
                 #}

                 if ($input{$atype_e} eq "Fax") {
                    status("$login: We have not been able to verify your premium account. Click on the premium services link for more information. <p>We require a US Dollar 15.00 fee to setup your premium membership. In addition you need to add a minimum deposit of US Dollar 15.00 to activate your fax account. This allows you to send faxes. <p>Mail all payments (minimum US Dollar 30.00 by valid bank check) to P.O. Box 360404, Milpitas, CA 95036-0404. USA. Mention your hotdiary member login on the check. <p>To activate your premium service your email address in your member profile must be valid.  Your account will be activated after we receive your check. \n");
                    exit;
                 }

                 if ($input{$atype_e} eq "VoiceMail") {
                    status("$login: Party Voice Planner service is coming soon!.\n");
                    exit;
                 }


                 $hour_e = "hou$entryno";
		 #if (notHour(trim $input{$hour_e})) {
		 #   error ("$input{$hour_e}: invalid hour actual hour \n");
		 #   exit;
 		 #} 
	
                 $min_e = "mi$entryno";
	         #if (notMinSec(trim $input{$min_e})) {
		 #   error ("$input{$min_e}: invalid minute \n");
		 #   return;
		 #} 

                 $sec_e = "se$entryno";
		 #if (notMinSec(trim $input{$sec_e})) {
	         #   error("$input{$sec_e}: invalid seconds \n");	
                 #   return;	
 		 #}
 
                 $dhour_e = "dhou$entryno";
		 #if (notHour(trim $input{$dhour_e})) {
		 #   error("$input{$dhour_e}: invalid hour \n");
		 #   return;
		 #}

                 $dmin_e = "dmi$entryno";
		 #if (notMinSec(trim $input{$dmin_e})) {
		 #   error("$input{$dmin_e}: invalid minutes \n");
		 #   return;
		 #}

                 $meridian_e = "meridia$entryno";
		 #if (notMeridian(trim $input{$meridian_e})) {
		 #  error("$input{$meridian_e}: invalid. It can be only AM or PM \n");	
		 #  return;
		 #}
		
                 $desc_e = "des$entryno";
	         if (notDesc($input{$desc_e})) {
		   status("$login: Invalid characters in Description ($input{$desc_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
		   exit;
		 }

	         if (length($input{$desc_e}) > $MAXDESC) {
                   status("$login: Limit the length of Description to $MAXDESC");
		    exit;
		 } 
                 $subject_e = "subjec$entryno";
	         if (notName($input{$subject_e})) {
		   status("$login: Invalid characters in Subject. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
		   exit;
		 }

                 $distribution_e = "distributio$entryno";
	         if (notName($input{$distribution_e})) {
                    status("$login: Invalid characters in Distribution. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
		   exit;
		 }

                 $subject_e = "subjec$entryno";
                 #print "subject = ", $input{$subject_e};
                 $partytab{$entryno}{'subject'} = $input{$subject_e};

                 #allow only owner to update these fields.
	         # for non-owners donot update these fields and ignore them.
                 if (($partytab{$entryno}{'partyedit'} ne "CHECKED") &&
			 ($owner_flag != 1)) {
		    status("$login: You are not authorized to make changes to this entry");
		    exit;
		 }
		
		 #print "update these other fields as i am the owner\n";
                 $dtype_e = "dtyp$entryno";
                 $partytab{$entryno}{'dtype'} = $input{$dtype_e};
                 #print "appt type = ", $input{$dtype_e};

                 $atype_e = "atyp$entryno";
                 $partytab{$entryno}{'atype'} = $input{$atype_e};
                 #print "alarmtype = ", $input{$atype_e};

                 $distribution_e = "distributio$entryno";
                 #print "distribution = ", $input{$distribution_e};
                 $partytab{$entryno}{'distribution'} = $input{$distribution_e};
                 $zone_e = "zon$entryno";
                 #print "zone = ", $input{$zone_e};
                 $partytab{$entryno}{'zone'} = $input{$zone_e};

                 $partyedit_e = "partyedi$entryno";
	         if ($input{$partyedit_e} eq "on") {
                     $partytab{$entryno}{'partyedit'} = "CHECKED";
	         } else {
                     $partytab{$entryno}{'partyedit'} = $input{$partyedit_e};
		 }
                 #print "partyedit = ", $input{$partyedit_e};

                 $desc_e = "des$entryno";
               	 #($partytab{$entryno}{'desc'} = trim $input{$desc_e}) =~ s/\n//g;;
               	 ($partytab{$entryno}{'desc'} = trim $input{$desc_e});
                 #$partytab{$entryno}{'desc'} = $input{$desc_e};
                 $partytab{$entryno}{'month'} = $mo;
                 $partytab{$entryno}{'day'} = $da;
                 $partytab{$entryno}{'year'} = $yr;
                 $partytab{$entryno}{'hour'} = trim $input{$hour_e};
                 #$partytab{$entryno}{'min'} = trim $input{$min_e};
		 if (trim $input{$min_e} eq "0") {
	            $partytab{$entryno}{'min'} = '00';
                 } else {
                   $partytab{$entryno}{'min'} = trim $input{$min_e};
                 }
                 #$partytab{$entryno}{'sec'} = trim $input{$sec_e};
                 $partytab{$entryno}{'dhour'} = trim $input{$dhour_e};
                 #$partytab{$entryno}{'dmin'} = trim $input{$dmin_e};
		 if (trim $input{$dmin_e} eq "0") {
	            $partytab{$entryno}{'dmin'} = '00';
                 } else {
                   $partytab{$entryno}{'dmin'} = trim $input{$dmin_e};
                 }
                 $partytab{$entryno}{'meridian'} = trim $input{$meridian_e};

                 $desc = $partytab{$entryno}{'desc'};
                 $subject = $partytab{$entryno}{'subject'}; 
                 $hour = trim $input{$hour_e};
                 $min = trim $input{$min_e};
                 #$sec = trim $input{$sec_e};
                 $meridian = trim $input{$meridian_e};
                 $dtype =  $input{$dtype_e};

                 ($mfile = "/tmp/partyupd$$.txt") =~ s/\n/\n<BR>/g; 
                 open thandle, ">$mfile";
                 printf thandle "Dear HotDiary Member,\n\n";
                 printf thandle "Your party reminder with other HotDiary members has been recently updated. Please read the party details below.\n\n";
                 printf thandle "Regards\n";
                 printf thandle "HotDiary Inc.\n\n";
                 printf thandle "Your Party Reminder Follows:\n\n";
                 printf thandle "Entry number to search for your party reminder is %s\n", $entryno;
                 printf thandle "(Please keep the above number carefully. You will need it access your appointment)\n\n";
                
                 printf thandle "From: $login\n";
                 printf thandle "Owner ID: $partytab{$entryno}{'login'}\n";
                 printf thandle "Invitees: $partytab{$entryno}{'distribution'}\n";
                 printf thandle "Date: $mo/$da/$yr \n";
                 if ($min eq "0") {
                    $min = "00";
                 }
                 printf thandle "Time: $hour:$min $meridian \n";
                 printf thandle "Reminder Type: $dtype\n";
                 printf thandle "Description: $desc\n\n";     
                 printf thandle "HotDiary - New Generation Internet Organizer, http://www.hotdiary.com.";
                 &flush(thandle);
                 

                 $ts = $partytab{$entryno}{'distribution'};
                 @hsh = split(" ", $ts);
                 $ts = ""; 
                 # send email to distribution
                 foreach $i (@hsh) {
                    if ($ts eq "") {
                        $ts = "$i";
                    } else {
                        $ts = "$ts $i";
                    }
		   #print "i =", $i, "\n";
	           $i = trim $i;
                   tie %lgrouptab, 'AsciiDB::TagFile',
                     DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                     SUFIX => '.rec',
                     SCHEMA => {
                          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                        'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed' ] };
                   tie %plgrouptab, 'AsciiDB::TagFile',
                     DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
                     SUFIX => '.rec',
                     SCHEMA => {
                          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };


                   if ((!exists $logtab{$i}) && (!exists $lgrouptab{$i}) && (!exists $plgrouptab{$i})) {
			$altmsg = "$altmsg\n $i: is not valid login or group in $p2.";
		   } else { 
                     $atype = $input{$atype_e};
                     if ($atype eq "Email") { 
                        if (exists $logtab{$i}) {
                           $email = $logtab{$i}{'email'};
                           if ($email ne "") {
                              system "/bin/mail -s \"$subject\" $email < $mfile";
                              $alphi = substr $i, 0, 1;
                              $alphi = $alphi . '-index';
                              system "cp $ENV{HDDATA}/partytab/$entryno.rec $ENV{HDDATA}/$alphi/$i/appttab";
                              system "echo $entryno >> $ENV{HDDATA}/$alphi/$i/apptentrytab";
                           }
                        } else {
                           tie %lgrouptab, 'AsciiDB::TagFile',
                             DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                             SUFIX => '.rec',
                             SCHEMA => {
                               ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg', 'listed' ] }; 
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
                                    for ($l = 0; $l <= $#records; $l++) {
                                        if (exists $logtab{$records[$l]}) {
                                           $email = $logtab{$records[$l]}{'email'};
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
                                          for ($l = 0; $l <= $#records; $l++) {
                                             if (exists $logtab{$records[$l]}) {
                                                $email = $logtab{$records[$l]}{'email'};
                                                if ($email ne "") {
                                                   system "/bin/mail -s \"$subject\" $email < $mfile";
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
                              } else {
    ($user, $domain) = split "\@", $i;
    if (((trim $user) ne "") && ((trim $domain) ne "")) {
       system "/bin/mail -s \"$subject\" $i < $mfile";
        
    }
                              }
                           }
                        }
                     } else {
                        if ($atype eq "Pager") {
                           if (exists $logtab{$i}) {
                              $pager = $logtab{$i}{'pager'}; 
                              $toname = $logtab{$i}{'fname'};
                              $owner = $partytab{$entryno}{'login'};
                              $from = $logtab{$owner}{'fname'};
                              if ($pager ne "") {
                                 system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                              }
                           } else {
                              tie %lgrouptab, 'AsciiDB::TagFile',
                                DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
                                SUFIX => '.rec',
                                SCHEMA => {
                                ORDER => ['groupname', 'groupfounder', 
				'grouptype', 'grouptitle', 'groupdesc',
				 'password', 'ctype', 'cpublish', 'corg', 'listed'] };

                              if (exists $lgrouptab{$i}) {
                                 if (-d "$ENV{HDDATA}/listed/groups/$i/usertab") {
                                    tie %usertab, 'AsciiDB::TagFile',
                                    DIRECTORY => "$ENV{HDDATA}/listed/groups/$i/usertab",
                                    SUFIX => '.rec',
                                    SCHEMA => {
                                    ORDER => ['login'] };
                                    (@records) = sort keys %usertab;
                                    if ($#records >= 0) {
                                       for ($l = 0; $l <= $#records; $l++) {
                                           if (exists $logtab{$records[$l]}) {
                                              $pager = $logtab{$records[$1]}{'pager'};
                                              $toname = $logtab{$records[$1]}{'fname'};
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
                                               for ($l = 0; $l <= $#records; $l++) {
                                                  if (exists $logtab{$records[$l]}) {
                                                     $pager = $logtab{$records[$1]}{'pager'};
                                                     $toname = $logtab{$records[$1]}{'fname'};
                                                     $from = $logtab{$login}{'fname'};
                                                     if ($pager ne "") {
                                                        system "java COM.hotdiary.main.SendPage \"$pager\" \"$toname $entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
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
                           }
                        }
                     }
                   }
                 }

                 #send email to the owner also
                 $owner = $partytab{$entryno}{'login'};
                 #print "owner = ", $owner, "\n";

                 if (!exists $logtab{$owner}) {
		     $altmsg = "$altmsg\n $owner: does not have account in $p2.";
		 } else {
                     $atype = $input{$atype_e};     
                     if ($atype eq "Email") {
                        $email = $logtab{$owner}{'email'};
                        #print "owner email = ",  $email, "\n";
                        if ($email ne "") {
                           system "/bin/mail -s \"$subject\" $email < $mfile";
                        }
                     } else {
                        if ($atype eq "Pager") {
                           $pager = $logtab{$owner}{'pager'};
                           $from = $logtab{$owner}{'fname'};
                           if ($pager ne "") {
                              system "java COM.hotdiary.main.SendPage \"$pager\" \"$entryno $mo-$da-$yr $hour:$min $meridian $dtype $desc\" \"$from\"";
                           }
                           
                        }
                     }
                 }

                 $msg = "$login: Party details have been updated. $altmsg";
	      }

              if ($action eq "Delete")
              {
		 if ($owner_flag == 0)
	         {
	            status("$login: You have to be the owner to delete this party reminder.");
		    exit;
	         }

                 $found_counter = $found_counter + 1;

                 $tfile = "$ENV{HDDATA}/partyentrytab";
                 open thandle, "+<$tfile";

                 $i = 0;

                 while (<thandle>) {
                    chop;
                    $onekey = $_;
                    #print "entryno in the file ", $onekey;
                    if ($onekey ne $entryno) {
                       $num_array[$i] = $onekey;
                       #print "num_array =", $num_array[$i];
                       $i = $i + 1;
                    }
                 }
                 close thandle;

                 # intialize the file
                 system "/bin/echo >$ENV{HDDATA}/partyentrytab";

                 $tfile = "$ENV{HDDATA}/partyentrytab";
                 open thandle, "+<$tfile";

                 for ($k = 0; $k < $i; $k = $k + 1)  {
                    $get_entryno = $num_array[$k];
                    printf thandle "%s\n", $get_entryno;
                 }
                 close thandle;
                 if (exists $partytab{$entryno}) {
                    delete $partytab{$entryno};
                    $msg = "$login: Party details has been deleted.";
                    withdrawmoney $login;
                 } else {
                    $msg = "$login: Did not find a match for party entry $entryno";
                 }

                 # delete entrynumber from the partyentrytab
                 # lookup the entrynumber in the partyentrytab and
                 # remove it.
    #status("$login: Party details have been deleted.");
	      }
           }
        }
   }

   if ($checknum == 0) {
      status("$login: Please select or click atleast one checkbox.");
      exit;
   }
  
   status("$msg");
   

# save the info in db
   tied(%partytab)->sync();
   tied(%sesstab)->sync();


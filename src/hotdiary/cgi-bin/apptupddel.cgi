#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: apptupddel.cgi
# Purpose: appointment updates and deletes.                  
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


#!/usr/local/bin/perl5

require "cgi-lib.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use utils::utils;
$cgi_lib'maxdata = 500000;

MAIN:
{


# parse the command line
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXDESC = 4096;

# print HTML headers

   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Update/Delete Appointment");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   #print "biscuit =", $biscuit;

   $numentries = $input{'numentries'};
   #print "numentries =", $numentries;
 
   if ($input{'update.x'} ne "") {     
      $action = "Update";
   } else {
   if ($input{'delete.x'} ne "") {
      $action = "Delete";
   }}
   hddebug "action = $action";

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['login', 'password', 'fname', 'lname', 'street',
	'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


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
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
             error("Login  is an empty string.\n");
             exit;
           }
        }
   }
   $alp = substr $login, 0, 1;
   $alp = $alp . '-index';

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
   #    error("Intrusion detected. Access denied.\n");
   #    exit;
   #}


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: Your session has already expired.\n");
      exit;
   }

   $sesstab{$biscuit}{'time'} = time();

# bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alp/$login/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'street', 'city', 'state',
        'zipcode', 'country', 'venue', 'person', 'phone',
        'banner', 'confirm', 'id', 'type'] };

# bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };


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

   for ($l = 0; $l < $numentries; $l = $l + 1) {
       $one_entryno = $entry_array[$l];
       $entryno = $input{$one_entryno};
       #print "entryno = ", $entryno;
       #print "one_entryno = ", $one_entryno;

       # check if checkbox is on.
       $checkbox_e = "checkbox$entryno";
       $checkbox = $input{$checkbox_e};
       #print "cbeckbox = ", $checkbox;

       #if ($checkbox eq "on") {
          #print "checkbox is on";
       #   $checknum = $checknum + 1;

          # check if appointment record exists.
          if (!exists $appttab{$entryno}) {
	     $msg = "Reminder record does not exist.";
          } else {
              if ($action eq "Update") {
                 #increment the counter
                 $found_counter = $found_counter + 1;
                 #print "entered the update ";

                 #modify/edit an existing appointments
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
                    #status("$login: Please set reminders a minimum of 20 minutes in advance of current time. Change the date to make it current.");
                    #exit;
	         }


                 # check if the user has selected Pager/Fax/VoiceMail.
                 # give an appropriate error message until we support this
                 # feature.
                 $atype_e = "atyp$entryno";
                 #if ($input{$atype_e} eq "Pager") {
          	 #   error("Currently VoiceMail/Pager/Fax are not supported.\n");
          	 #   return;
		 #}
                 #if (($input{$atype_e} eq "Pager") && ($logtab{$login}{'pagertype'} eq "Other Pager")) {
                 #   status("$login: Reminder pager notification for pager type \"Other Pager\" is not supported."); 
                 #   exit;
                 #}
                 if ($input{$atype_e} eq "VoiceMail") {
          	    status("$login: Reminder Voice service is coming soon!\n");
          	    exit;
		 }
                 if ($input{$atype_e} eq "Fax") {
          	    status("$login: We have not been able to verify your premium account. Click on the premium services link for more information. <p>We require a US Dollar 15.00 fee to setup your premium membership. In addition you need to add a minimum deposit of US Dollar 15.00 to activate your fax account. This allows you to send faxes. <p>Mail all payments (minimum US Dollar 30.00 by valid bank check) to P.O. Box 360404, Milpitas, CA 95036-0404. USA. Mention your hotdiary member login on the check. <p>To activate your premium service your email address in your member profile must be valid.  Your account will be activated after we receive your check. \n");

          	    exit;
		 }

                 #if (notDate($da, $mo, $yr)) {
                 #   error("$da $mo $yr: invalid date\n");
                 #   return;
                 #} else {

                    $appttab{$entryno}{'month'} = $mo; 
                    $appttab{$entryno}{'day'} = $da;
                    $appttab{$entryno}{'year'} = $yr;

	         #}

                 $hour_e = "hou$entryno";
                 #if (notHour(trim $input{$hour_e})) { 
		 #   error ("$input{$hour_e}: invalid hour actual hour \n");
		 #   return;
		 #} 

                 $min_e = "mi$entryno";
	         #if (notMinSec(trim $input{$min_e})) {
		 #   error ("$input{$min_e}: invalid minute \n");
	         #   return;
	         #}
  
                 #$sec_e = "se$entryno";
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
		 #   error("$input{$meridian_e}: invalid. It can be only AM or PM \n");	
                 #}

                 $desc_e = "des$entryno";
	         if (notDesc($input{$desc_e})) {
		   status("$login: Invalid characters in description. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
		   exit; 
                 }

	         if (length(trim $input{$desc_e}) > $MAXDESC) {
		     status("$login: Limit the length of description to $MAXDESC");
		     exit;
	         }
#########################
if ($emsg eq "") {
$pgtype = $logtab{$login}{'pagertype'};
$pager = getPhoneDigits trim $logtab{$login}{'pager'};
       if (("\L$pgtype" eq "\LSkyTel Pager") && ($input{$atype_e} eq "Pager") && ((notSkyTelPin $pager) || (!(notEmailAddress $pager)) )) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. You need to specify only a numeric PIN of 7 digits in your pager number. Non-numeric digits and email addresses are not supported. If you would like to use an email address for your $pgtype, please use the Other Pager feature in Profile (even if you have a $pgtype), and enter an email address.";
       }
       if (("\L$pgtype" eq "\LAirTouch Pager") && ($input{$atype_e} eq "Pager") && ( (notAirTouchPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (11 numeric digits). Also it cannot be an email address. For instance \"1-408-456-1234\" is a valid format.<p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype. <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this. <p>If you would like to use an email address for your $pgtype, please use the Other Pager feature in Profile (even if you have a $pgtype), and enter an email address.";
       }
       if (("\L$pgtype" eq "\LNextel Pager") && ($input{$atype_e} eq "Pager") && ( (notNextelPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>$login: Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (10 digit numeric PIN). Also it cannot be an email address. For instance \"408-456-1234\" is a valid format. <p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype.  <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this.";
       }
       if (("\L$pgtype" eq "\LPageMart Pager") && ($input{$atype_e} eq "Pager") && ( (notPageMartPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (either a 7 digit numeric PIN or a 10 digit $pgtype \"Assured Messaging\" phone number which is also the PIN). Also it cannot be an email address. Note that 7 digit numeric PINs are used for traditional (one-way) paging using $pgtype. For instance either \"408-456-1234\" or \"456-1234\", both are valid formats. <p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype. <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this. <p>If you are trying to page a subscriber and you do not know the recipient's PIN, you must contact that individual to gain access to his or her PIN. $pgtype does not give out subscriber's PINs.";
       }
       if (($input{$atype_e} eq "Pager") && ($pagertype eq "Other Pager") && (notEmailAddress $pager) ) {
          $emsg = "<p>Warning! Since you have selected an Other Pager type, and not entered a valid internet pager email address in the Pager field of your Profile menu you may not receive this reminder. Numeric pager numbers which are not internet pager email addresses will not be supported.";
       }
}
#########################

                 $hour_e = "hou$entryno";
                 $appttab{$entryno}{'hour'} = trim $input{$hour_e};

                 $min_e = "mi$entryno";
                 #$appttab{$entryno}{'min'} = trim $input{$min_e};
		 #print "min = ", trim $input{$min_e}, "\n";
		 #print "fieldname min = ", $min_e, "\n";
		 $temp = trim $input{$min_e};
		 if ($temp == 0) {
		     $appttab{$entryno}{'min'} = '00';
                 } else {
                    $appttab{$entryno}{'min'} = $temp;
                 }

                 #$sec_e = "se$entryno";
                 #$appttab{$entryno}{'sec'} = trim $input{$sec_e};

                 $dhour_e = "dhou$entryno";
                 $appttab{$entryno}{'dhour'} = trim $input{$dhour_e};

                 $dmin_e = "dmi$entryno";
                 #$appttab{$entryno}{'dmin'} = trim $input{$dmin_e};
		 if (trim $input{$dmin_e} eq "0") {
                     $appttab{$entryno}{'dmin'} = '00';
                 } else {
                    $appttab{$entryno}{'dmin'} = trim $input{$dmin_e};
                 }


                 $meridian_e = "meridia$entryno";
                 $appttab{$entryno}{'meridian'} = trim $input{$meridian_e};

                 $dtype_e = "dtyp$entryno";
                 $appttab{$entryno}{'dtype'} = $input{$dtype_e};
                 #print "appt type = ", $input{$dtype_e};

                 $recurtype_e = "recurtyp$entryno";
                 $appttab{$entryno}{'recurtype'} = $input{$recurtype_e};

                 $atype_e = "atyp$entryno";
                 $appttab{$entryno}{'atype'} = $input{$atype_e};
                 #print "alarmtype = ", $input{$atype_e};

                 $desc_e = "des$entryno";
                 #($appttab{$entryno}{'desc'} = $input{$desc_e}) =~ s/\n/\n<BR>/g;
                 $appttab{$entryno}{'desc'} = $input{$desc_e};
                 $zone_e = "zon$entryno";
                 ($appttab{$entryno}{'zone'} = $input{$zone_e}) =~ s/\n/\n<BR>/g;
                 #$appttab{$entryno}{'desc'} = $input{$desc_e};
                 $msg = "$login: Reminder entries have been updated.";
	      }

              if (($action eq "Delete") && ($checkbox eq "on")) {
                 $found_counter = $found_counter + 1;
                 $checknum = $checknum + 1;  

                 $tfile = "$ENV{HDDATA}/$alp/$login/apptentrytab";
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
                 system "/bin/echo >$ENV{HDDATA}/$alp/$login/apptentrytab";

                 $tfile = "$ENV{HDDATA}/$alp/$login/apptentrytab";
                 open thandle, "+<$tfile";

                 for ($k = 0; $k < $i; $k = $k + 1)  {
                    $get_entryno = $num_array[$k];
                    printf thandle "%s\n", $get_entryno;
                 }
                 close thandle;
                 delete $appttab{$entryno};
                 withdrawmoney $login;

                 # delete entrynumber from the apptentrytab
                 # lookup the entrynumber in the apptentrytab and
                 # remove it.
    #status("$login: Appointment entries have been deleted.");
                 $msg = "$login: Reminder entries have been deleted.";
	      }
           }
       # }
   }

   if (($checknum == 0) && ($action eq "Delete")) {
      status("$login: Please select or click atleast one checkbox.");
      exit;
   }

   
   status("$msg $emsg");

   #reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   

# save the info in db
   if ($action eq "Delete") {
      (@aptsno) = keys %appttab;
      if ($#aptsno < 0) {
         if (exists $remindtab{$login}) {
            delete $remindtab{$login};
            tied(%remindtab)->sync();
         }
      }
   }
   tied(%appttab)->sync();
   tied(%sesstab)->sync();

}

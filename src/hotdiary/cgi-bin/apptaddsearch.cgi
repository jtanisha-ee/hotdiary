#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: apptaddsearch.cgi
# Purpose: it adds and searches the appointments.                  
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
#$cgi_lib'maxdata = 500000;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

#max length in the description
   $MAXDESC = 4096;

# parse the command line
   &ReadParse(*input); 

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Add Appointment"); 

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
     status("$login: Your session has timed out. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.");
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
                        

  $alph = substr $login, 0, 1;
  $alph = $alph . '-index';

# bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alph/$login/appttab",
   SUFIX => '.rec', 
   SCHEMA => { 
   	ORDER => ['entryno', 'login', 'month', 'day', 'year', 
	'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'street', 'city', 'state',
        'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
        'confirm', 'id', 'type'] };

# bind remind index table vars
   tie %remindtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   	ORDER => ['login'] };

#
# bind personal appointment entry number table vars
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
       #add a new appointment 

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

       if ((($etime - $ctime) < 0) || (($etime - $ctime) < 1200)) {
	  #status("$login: You can only set reminders which are due in the future, atleast 20 minutes past current time.");
	  #exit;
       } 

       #if (notDate($da, $mo, $yr)) {
       #  error("$da $mo $yr: invalid date\n");
       #  return;
       #} 

       #if (notHour(trim $input{'hour'})) {
       #  error("$input{'hour'}: invalid hour\n");
       #  return;
       #}
      
       #if (notMinSec(trim $input{'min'})) {
	#  error("$input{'min'}: invalid minute\n");
	#  return;
       #}
       
       #if (notMinSec(trim $input{'sec'})) {  
	#  error("$input{'sec'}:  invalid second\n");
	#  return;
       #}
      
       #if (notMeridian(trim $input{'meridian'})) { 
#	  error("$input{'meridian'}: invalid. It can be only AM or PM \n");
#	  return;
#       }
      
       #if (notHour(trim $input{'dhour'})) {
#	  error("$input{'dhour'}: invalid hour\n");
#	  return;
#       }
    
#       if (notMinSec(trim $input{'dmin'})) {
#	  error("$input{'dmin'}: invalid minute\n");
#	  return;
#       } 

       if (notDesc($input{'desc'})) {
          status("$login: Invalid characters in Description ($input{'desc'}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
	  exit;
       }

       $pgtype = $logtab{$login}{'pagertype'};
       if ( ("\U$pgtype" eq "\UMetrocall Pager") && (notAlphaNumeric ($input{'desc'})) ) {
          status("$login: You can specify only alphanumeric characters (a-z A-Z 0-9) and spaces (space or blank characters) in your Metrocall Pager message");
          exit;
       }

       if ($input{'atype'} eq "VoiceMail") {
	  status("$login: Reminder Voice service is coming soon!.\n");
	  exit;
       } 
       #if ($input{'atype'} eq "Pager") {
	  #error("Currently VoiceMail/Pager/Fax are not supported.\n");
	  #exit;
       #}
       #if (($input{'atype'} eq "Pager") && ($logtab{$login}{'pagertype'} eq "Other Pager")) {
       #   status("$login: Reminder pager notification for pager type \"Other Pager\" is not supported."); 
       #   exit;
       #}
       if ($input{'atype'} eq "Fax") {
	  status("$login: We have not been able to verify your premium account. Click on the premium services link for more information. <p>We require a US Dollar 15.00 fee to setup your premium membership. In addition you need to add a minimum deposit of US Dollar 15.00 to activate your fax account. This allows you to send faxes. <p>Mail all payments (minimum US Dollar 30.00 by valid bank check) to P.O. Box 360404, Milpitas, CA 95036-0404. USA. Mention your hotdiary member login on the check. <p>To activate your premium service your email address in your member profile must be valid.  Your account will be activated after we receive your check. \n");
	  exit;
       }

       # check if the alarm type is pager, voicemail or fax
       # we need to give an error until we support premium services.
    
# after all validation, we save the the changes at one shot.

       depositmoney $login;
       $appttab{$entryno}{'entryno'} = $entryno;
       $appttab{$entryno}{'login'} = $login;
       $appttab{$entryno}{'dtype'} = trim $input{'dtype'};
       $appttab{$entryno}{'atype'} = trim $input{'atype'};
       $appttab{$entryno}{'recurtype'} = trim $input{'recurtype'};
       $remindtab{$login}{'login'} = $login;
       
       if (length($input{'desc'}) > $MAXDESC) {
	  status("$login: Limit the length of description to $MAXDESC");
	  exit;
       } else { 
          $appttab{$entryno}{'desc'} = $input{'desc'};
       }
       $appttab{$entryno}{'zone'} = trim $input{'zone'};
       $appttab{$entryno}{'month'} = $mo;
       $appttab{$entryno}{'day'} = $da;
       $appttab{$entryno}{'year'} = $yr;
       $appttab{$entryno}{'hour'} = trim $input{'hour'};
       if (trim $input{'min'} eq "0") {
         $appttab{$entryno}{'min'} = '00'; 
       } else {
         $appttab{$entryno}{'min'} = trim $input{'min'};    
       }
       #$appttab{$entryno}{'sec'} = trim $input{'sec'};    
       $appttab{$entryno}{'meridian'} = trim $input{'meridian'};    
       $appttab{$entryno}{'dhour'} = trim $input{'dhour'};    
       if (trim $input{'dmin'} eq "0") {
         $appttab{$entryno}{'dmin'} = '00'; 
       } else {
          $appttab{$entryno}{'dmin'} = trim $input{'dmin'};    
       }

       # add the entry in the apptentrytab/$login.
       $tfile = "$ENV{HDDATA}/$alph/$login/apptentrytab";
       open thandle, ">>$tfile";
       printf thandle "%s\n", $entryno;
       close thandle;
       $pager = getPhoneDigits trim $logtab{$login}{'pager'};
       if (("\L$pgtype" eq "\LSkyTel Pager") && ($input{'atype'} eq "Pager") && ((notSkyTelPin $pager) || (!(notEmailAddress $pager)) )) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. You need to specify only a numeric PIN of 7 digits in your pager number. Non-numeric digits and email addresses are not supported. If you would like to use an email address for your $pgtype, please use the Other Pager feature in Profile (even if you have a $pgtype), and enter an email address.";
       }
       if (("\L$pgtype" eq "\LAirTouch Pager") && ($input{'atype'} eq "Pager") && ( (notAirTouchPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (11 numeric digits). Also it cannot be an email address. For instance \"1-408-456-1234\" is a valid format.<p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype. <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this. <p>If you would like to use an email address for your $pgtype, please use the Other Pager feature in Profile (even if you have a $pgtype), and enter an email address.";
       }
       if (("\L$pgtype" eq "\LNextel Pager") && ($input{'atype'} eq "Pager") && ( (notNextelPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>$login: Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (10 digit numeric PIN). Also it cannot be an email address. For instance \"408-456-1234\" is a valid format. <p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype.  <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this.";
       }
       if (("\L$pgtype" eq "\LPageMart Pager") && ($input{'atype'} eq "Pager") && ( (notPageMartPin $pager) || (!(notEmailAddress $pager)) ) ) {
          $emsg .= "<p>Warning! We have checked your Profile, and determined that you may not receive your reminder. The $pgtype number you have entered ($pager) must be a valid $pgtype PIN (either a 7 digit numeric PIN or a 10 digit $pgtype \"Assured Messaging\" phone number which is also the PIN). Also it cannot be an email address. Note that 7 digit numeric PINs are used for traditional (one-way) paging using $pgtype. For instance either \"408-456-1234\" or \"456-1234\", both are valid formats. <p>If your pager's email address is of type PIN\@domain.com, you only need to enter your PIN. If you would still like to use your pager's email address, try the Other Pager option. This option can be used even though you have a $pgtype. <p>Also, you must have $pgtype internet paging service option enabled. If you are not sure you have this option enabled, please call a $pgtype representative to verify this. <p>If you are trying to page a subscriber and you do not know the recipient's PIN, you must contact that individual to gain access to his or her PIN. $pgtype does not give out subscriber's PINs.";
       }
       if (($input{'atype'} eq "Pager") && ($logtab{$login}{'pagertype'} eq "Other Pager") && (notEmailAddress $pager) ) {
          $emsg = "<p>Warning! Since you have selected an Other Pager type, and not entered a valid internet pager email address in the Pager field of your Profile menu you may not receive this reminder. Numeric pager numbers which are not internet pager email addresses will not be supported.";
       }
       #if (($input{'atype'} eq "Pager") && ($logtab{$login}{'pagertype'} ne "Other Pager")) {
          #($user, $domain) = split '@', $logtab{$login}{'pager'};
          #$pager1 = $logtab{$login}{'pager'};
          #if ($pager1 =~ /\@/) {
          #if (((trim $user) ne "") || ((trim $domain) eq "")) {
          #   $emsg .= "<p>Warning! The Pager field in your Profile menu contains an email address. In case of pager type $logtab{$login}{'pagertype'}, you only need to provide the pager PIN or numeric digits that normally precede the '\@' sign in the email address. $p2 takes care of sending message to the $logtab{$login}{'pagertype'} carrier automatically by constructing the corresponding email address.<p>If you would still like to use an explicit email address of your pager, specify the pager type as Other Pager in your Profile menu.<p>You can now update your Profile menu. You do not need to update your reminder after you update the Profile menu.";
          #}
       #}
       if ($input{'atype'} eq "Email") {
	  $fmsg = "<p>Make sure you have entered a valid email address. Otherwise you will not receive the reminder.";
           $mal = $logtab{$login}{'email'};
           if ((index ($mal, '@')) == -1) {
              $fmsg .= "<p>Your email address is not valid. It needs to be in the format user\@domain.com. Please fix the email address.";
           }
       } 
       $freqmsg = "<p>Please note that you have set a $appttab{$entryno}{'recurtype'} reminder. If you would like to change this, you can click on Reminder in left frame, select the appropriate month in the right frame, and press the Search button. This will show you all the reminders for the month you selected. Then you can browse through this list, and change the Frequency field in the reminder of interest. Press the checkbox for this reminder entry. Use the Update button to update the reminder.";
       if ($input{'atype'} eq "Pager") {
           $gmsg = "<p>Please make sure you have subcribed to an Internet based paging service before you use this feature. You can call your $pgtype representative to get more information on the type of service your pager supports.";
       }
       status("$login: Reminder entry has been added for $mo-$da-$yr. $emsg $fmsg $freqmsg $gmsg");   
   }

   if ($action eq "Search") {

      system "/bin/rm -f $ENV{HDREP}/$alph/$login/ser*.html";
      $month = trim $input{'month'};
      $yr = trim $input{'year'};
      $found_counter = 0;
      $page_entries = 0;
      $page_num = 0;
      $prevpage = "";
      $nextpage = "";
      $title = time();

#      #go through each entry in the appointment table.
#      # @allkeys = keys %appttab;

      $tfile = "$ENV{HDDATA}/$alph/$login/apptentrytab";
      open thandle, "+<$tfile";
      while (<thandle>) {
         chop;
         $onekey = $_;
         if ($onekey ne "")  {

            #print if appointment  record exists with firstname.
          #  print "month ", $month;
	  #  print "onekey", $onekey;
	    #if (exists $appttab{$onekey}) {
	#	print "appttab:month =", $appttab{$onekey}{'month'};
	#    }

           if (!exists $appttab{$onekey}) {
		next;
           } 
            if (($appttab{$onekey}{'month'} eq $month) && ($appttab{$onekey}{'year'} eq $yr)) {

               $found_counter= $found_counter + 1;
               $page_entries = $page_entries + 1;
               if ($page_entries eq 1) {
                  $page_num = $page_num + 1;
               }
               #print "page_num = ", $page_num, "\n";
               if ($page_num eq 1) {
                  $prevpage = "rep/$alph/$login/ser$biscuit$title$page_num.html";
               } else {
                  $pageno = $page_num - 1;
                  $prevpage = "rep/$alph/$login/ser$biscuit$title$pageno.html";
               }
               $pageno = $page_num + 1;
               if ($page_num eq 1) {
                  $nextpage = "rep/$alph/$login/ser$biscuit$title$pageno.html";
               } else {
                  $nextpage = "rep/$alph/$login/ser$biscuit$title$pageno.html";
               }
               #print "nextpage = ", $nextpage, "\n";
               #print "prevpage = ", $prevpage, "\n";


               ($entryno = $appttab{$onekey}{'entryno'}) =~ s/\n/\n<BR>/g;
               #print "Entryno = ", $entryno, "\n";
	       $prml = "";
              #$prml = strapp $prml, "entrynfield=entryn$found_counter";
               $prml = strapp $prml, "entrynfield=entryn$page_entries";
               $prml = strapp $prml, "entryno=$entryno";

	       $prml = strapp $prml, "checkboxfield=checkbox$entryno";


               ($outfield = $appttab{$onekey}{'month'}) =~ s/\n/\n<BR>/g;
               #print "Month Num = ", $outfield, "\n";
               $prml = strapp $prml, "monthnum=$outfield";
               $prml = strapp $prml, "montnumfield=montnum$entryno";


	      ($outfield = getmonthstr($appttab{$onekey}{'month'})) =~ s/\n/\n<BR>/g;
               #print "Month = ", $outfield, "\n";
	       $prml = strapp $prml, "month=$outfield";
               $prml = strapp $prml, "montfield=mont$entryno";

               ($outfield = $appttab{$onekey}{'day'}) =~ s/\n/\n<BR>/g;
	       $prml = strapp $prml, "day=$outfield";
	       $prml = strapp $prml, "dafield=da$entryno";


               ($outfield = $appttab{$onekey}{'year'}) =~ s/\n/\n<BR>/g;
               #print "Year = ", $outfield, "\n";
	       $prml = strapp $prml, "year=$outfield";
	       $prml = strapp $prml, "yeafield=yea$entryno";

               ($outfield = $appttab{$onekey}{'hour'}) =~ s/\n/\n<BR>/g;
               #print "Hour = ", $outfield, "\n";
	       $prml = strapp $prml, "hour=$outfield";
	       $prml = strapp $prml, "houfield=hou$entryno";

               ($outfield = $appttab{$onekey}{'min'}) =~ s/\n/\n<BR>/g;
	       if ($outfield eq '00') {
		  $outfield = '0';
               }	
               #print "Minutes = ", $outfield, "\n";
	       $prml = strapp $prml, "min=$outfield";
	       $prml = strapp $prml, "mifield=mi$entryno";

               #($outfield = $appttab{$onekey}{'sec'}) =~ s/\n/\n<BR>/g;
               ##print "Seconds = ", $outfield, "\n";
	       #$prml = strapp $prml, "sec=$outfield";
	       #$prml = strapp $prml, "sefield=se$entryno";

               ($outfield = $appttab{$onekey}{'meridian'}) =~ s/\n/\n<BR>/g;
               #print "Meridian = ", $outfield, "\n";
	       $prml = strapp $prml, "meridian=$outfield";
	       $prml = strapp $prml, "meridiafield=meridia$entryno";

               ($outfield = $appttab{$onekey}{'dhour'}) =~ s/\n/\n<BR>/g;
               #print "Duration Hour = ", $outfield, "\n";
	       $prml = strapp $prml, "dhour=$outfield";
	       $prml = strapp $prml, "dhoufield=dhou$entryno";

               ($outfield = $appttab{$onekey}{'dmin'}) =~ s/\n/\n<BR>/g;
	       if ($outfield eq '00') {
		  $outfield = '0';
	       }
               #print "Duration Minutes = ", $outfield, "\n";
	       $prml = strapp $prml, "dmin=$outfield";
	       $prml = strapp $prml, "dmifield=dmi$entryno";

               ($outfield = $appttab{$onekey}{'dtype'}) =~ s/\n/\n<BR>/g;
               #print "Reminder Type = ", $outfield, "\n";
	       $prml = strapp $prml, "dtype=$outfield";
	       $prml = strapp $prml, "dtypfield=dtyp$entryno";

               if (trim($appttab{$onekey}{'recurtype'}) eq "") {
		  $appttab{$onekey}{'recurtype'} = "Once";
               }
               ($outfield = $appttab{$onekey}{'recurtype'}) =~ s/\n/\n<BR>/g;
               #print "Recurring Type = ", $outfield, "\n";
	       $prml = strapp $prml, "recurtype=$outfield";
	       $prml = strapp $prml, "recurtypfield=recurtyp$entryno";

               ($outfield = $appttab{$onekey}{'atype'}) =~ s/\n/\n<BR>/g;
               #print "Alarm Type = ", $outfield, "\n";
	       $prml = strapp $prml, "atype=$outfield";
	       $prml = strapp $prml, "atypfield=atyp$entryno";

               #($outfield = $appttab{$onekey}{'desc'}) =~ s/\n/\n<BR>/g;
               $outfield = $appttab{$onekey}{'desc'};
               $outfield = adjusturl($outfield);
               #print "Description = ", $outfield, "\n";
	       $prml = strapp $prml, "desc=$outfield";
	       $prml = strapp $prml, "desfield=des$entryno";

               ($outfield = getzonestr($appttab{$onekey}{'zone'})) =~ s/\n/\n<BR>/g;
               #print "Zone String = ", $outfield, "\n";
	       $prml = strapp $prml, "zonestr=$outfield";
	       $prml = strapp $prml, "zonstrfield=zonstr$entryno";

               ($outfield = $appttab{$onekey}{'zone'}) =~ s/\n/\n<BR>/g;
               #print "Zone = ", $outfield, "\n";
	       $prml = strapp $prml, "zone=$outfield";
	       $prml = strapp $prml, "zonfield=zon$entryno";

	       $prml = strapp $prml, "template=$ENV{HDTMPL}/searchappttblentry.html";
	       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/searchappttblentry.html";
               parseIt $prml;
               $prml = "";

               if ($page_entries eq 1) {
#                  if ($page_num eq 1 ) {
#                     system "/bin/cat $ENV{HDTMPL}/content.html > $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
#                  }
                  # Generate Search Page Header
                  $prml = strapp $prml, "biscuit=$biscuit";
                  #$title = time();
		  #$expiry = localtime(time() + 5);
                  #$expiry = "\:$expiry";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/searchpghdr.html";
                  $prml = strapp $prml, "pagenumber=Page: $page_num <BR>";
		  #$prml = strapp $prml, "expiry=$expiry";
		  $prml = strapp $prml, "expiry=";
                  $urlcgi = buildurl("execapptupddel.cgi");
                  $prml = strapp $prml, "actioncgi=$urlcgi";
	          $monthstr = getmonthstr($month);
                  $prml = strapp $prml, "label=$p2 Reminder Search results for $monthstr";
                  $prml = strapp $prml, "label1=To receive reminders you must have correct Email, Pager, or Fax information specified in your Profile";
                  parseIt $prml;
                  $prml = "";
                  if ($page_num eq 1) {
                    system "/bin/cat $ENV{HDHREP}/$alph/$login/searchpghdr.html > $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
                  } else {
                    system "/bin/cat $ENV{HDHREP}/$alph/$login/searchpghdr.html > $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
                  }

                  # Generate Standard Table Header
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/stdtblhdr.html"; 
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alph/$login/stdtblhdr.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
	       }

               system "/bin/cat $ENV{HDHREP}/$alph/$login/searchappttblentry.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
 
               if ($page_entries eq 2) {
# this is the last time we will use page_entries in this iteration,
# so we can reset it now to 0
                  # Generate Standard Table Footer
                  $prml = strapp $prml, "numentries=$page_entries";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/stdtblftr.html";
                  $prml = strapp $prml, "nextpage=$nextpage";
                  $prml = strapp $prml, "prevpage=$prevpage";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alph/$login/stdtblftr.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";

                  # Generate Search Page Footer
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/searchpgftr.html";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alph/$login/searchpgftr.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
               }
               if ($page_entries eq 2) {
                  $page_entries = 0;
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
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/stdtblftr.html";
         $prml = strapp $prml, "nextpage=$nextpage";
         $prml = strapp $prml, "prevpage=$prevpage";
         parseIt $prml;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alph/$login/stdtblftr.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";

         # Generate Search Page Footer
         $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alph/$login/searchpgftr.html";
         parseIt $prml;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alph/$login/searchpgftr.html >> $ENV{HDREP}/$alph/$login/ser$biscuit$title$page_num.html";
      }


      # overwrite nextpage with lastpage
      #$title = time();
      #$expiry = localtime(time() + 5);
      #$expiry = "\:$expiry";
      #$prml = strapp $prml, "expiry=$expiry";
      $prml = strapp $prml, "expiry=";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/lastpage.html";
      $prml = strapp $prml, "prevpage=rep/$alph/$login/ser$biscuit$title$page_num.html";
      $pageno = $page_num + 1;
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alph/$login/ser$biscuit$title$pageno.html";
      parseIt $prml;
      $prml = "";
      system "cp $ENV{HDREP}/$alph/$login/$biscuit.html $ENV{HDREP}/$alph/$login/ser$biscuit$title$pageno.html";

      if ($found_counter eq 0) {
         status("$login: No reminders set in " . getmonthstr($month) . ". If you have received a reminder message recently that you are looking for, check the month when the reminder was set in the message, and then search by selecting appropriate month. For a more visual experience, press the Calendar button in the left frame, and it will allow you to browse by monthly view.");
      } else {
         #system "/bin/cat $ENV{HDTMPL}/content.html";  
	 $pagenum = "1";
         #system "/bin/cat $ENV{HDREP}/$alph/$login/ser$biscuit$title$pagenum.html";
         hdsystemcat "$ENV{HDREP}/$alph/$login/ser$biscuit$title$pagenum.html";
         }
    }

# close the document cleanly
   #print &HtmlBot;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 


# save the info in db
   tied(%appttab)->sync();
   tied(%remindtab)->sync();
   system "chmod 777 $ENV{HDDATA}/aux/remindtab/*.rec";
   tied(%sesstab)->sync();
}

#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#


#
# FileName: sendfaxmsg.cgi
# Purpose: it sends appropriate fax messages from the address book.
# Creation Date: 07-01-98
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXMESSAGE = 256000;
   $FIRSTPAGE = 3000;
   #$NEXTPAGE = 3400;

   #print &PrintHeader;
   #print &HtmlTop ("sendfaxmsg.cgi example");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagerytpe',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind faxaccttab table vars to maintain the account balance.
   tie %faxaccttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/faxaccttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'faxid', 'balance'] };

# bind areacodetab table vars to maintain the account balance.
   tie %areacodetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/areacodes/us/areacodetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['areacode'] };


   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.");
              exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already timed out. However, all your personal information is completely intact.");
    exit;
   }


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if (! (-d "$ENV{HDDATA}/$alphaindex/$login/faxtab")) {
	system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxtab";
        system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxtab";
   }

   if (! (-d "$ENV{HDDATA}/$alphaindex/$login/faxdeptab")) {
	system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
        system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
   }

# bind faxtab table vars
   tie %faxtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/faxtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'fax', 'numpages', 'date'] };




   if ($input{'send.x'} ne "") {
      $action = "Send";
   }

   #if ($login ne "smitha") {
#	status("This service is coming soon!");
#	exit;
#   }

   if (notPhone(trim $input{'to'})) {
      status("$login: Invalid characters in Phone.  Click <a href=\"validation.html\"> here</a> for valid input.");
      exit;
   } else { 
      $to = trim $input{'to'};
   }

   #print "to = ", $to, "\n";
    
   if (!exists $faxaccttab{$login}) {
      status("$login: We have not been able to verify your premium account. Click on the premium services link for more information. <p>We require a US Dollar 15.00 fee to setup your premium membership. In addition you need to add a minimum deposit of US Dollar 15.00  to activate your fax account. This allows you to send faxes. <p>Mail all payments (minimum US Dollar 30.00 by valid bank check) to P.O. Box 360404, Milpitas, CA 95036-0404. USA. Mention your hotdiary member login on the check. <p>To activate your premium service your email address in your member profile must be valid.  Your account will be activated after we receive your check.");
      exit;
   }

   $faxdigits = getPhoneDigits($to);
   if ((length($faxdigits) ne "10") &&  (length($faxdigits) ne "11")) {
       status("$login: If you enter a complete phone number including area code, its length may not exceed 10 digits. If it is prefixed with 1, it's length may not exceed 11. Otherwise if you are trying to send international fax, this service is coming soon."); 
       exit;
   }

   if (length($faxdigits) eq "11") {
	$fd = substr($faxdigits, 0, 1);
        if ($fd ne "1") {
	    status("$login: The only supported prefix for your phone number is \"1\". Please enter 1 followed by the areacode and the phone number.");
            exit;
        }
   }


   $areacode = getAreaCode($faxdigits); 
   if ($areacode eq "011") {
	status("$login: Support for international faxes is coming soon!");
	exit;
   }

   if (exists $areacodetab{$areacode}) {
      $faxto = getFaxSavUSPhoneDigits($faxdigits);
   } else {
      status("$login: Support for this area code for fax is coming soon!");
      exit;
   } 
   
   $successpage = $input{'thispage'};
   #print "successpage = ", $successpage, "\n";


   # get entry number
   $entryno = getkeys();

   $sesstab{$biscuit}{'time'} = time();
   $from = $logtab{$login}{'fname'};
   $numpages = 1;

 # create email to send fax. append the faxsav id number at the end of
 # email.

   $emailto = "$faxto\@faxsav.com";

 # check if this message is a file or typed text.
 # if it a typed text 

   $balance = "";
   $rate = "";
   if ($input{'faxfile'} ne "") {
      $mime_type = $input{'fmttype'};
      if ($mime_type eq "text/plain") {
	  $encode_bit = "7bit";
      }
      $faxfile = $input{'faxfile'};
      $filelen = length($faxfile);
      #print "filelen = $filelen";
      if ($filelen > $FIRSTPAGE) {
	 $numpages = int $filelen / $FIRSTPAGE;
         $numpages = $numpages + 1; 
      }

      #print "numpages = $numpages"; 
# shall we currently assume 15cents per page for US.
# get the rate from a rate file in future.
     $rate = 15;
     $balance = $faxaccttab{$login}{'balance'}; 
     $balance = $balance - ($numpages * $rate);
     #print "balance = $balance";
     if ($balance <= 0) {
        status("$login: You do not have enough balance($balance) in your account to send $numpages pages. Click on the premium services link for more information.");
        exit;
     }
 
      ($afile = "/tmp/att$$.txt") =~ s/\n/\n<BR>/g;
      open thandle, ">$afile";
      printf thandle "%s", $input{'faxfile'};
      printf thandle "AAA000";
      &flush(thandle);
      close thandle;
      if ($action = "Send") { 
           $mailcmd = "/usr/bin/metasend -b -S 800000 -m $mime_type -f $afile -s \"$faxto\" -e $encode_bit -t $emailto -F noreply\@hotdiary.com";

           system "echo '#!/bin/ksh' > /var/tmp/sendfax$$";  
           #$mailcmd = "/bin/mail -s \"fax\" $emailto < $mfile";
           system "echo \"$mailcmd\" >> /var/tmp/sendfax$$";
           system "chmod 777 /var/tmp/sendfax$$";
           system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/sendfax$$\"";
           system "/bin/cat $ENV{HDTMPL}/content.html"; 
           system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage";
      }

   } else {

# text area message.
     $message = $input{'message'};
     ($mfile = "/tmp/fax$$.txt") =~ s/\n/\n<BR>/g;
     open mhandle, ">$mfile";
     printf mhandle "$message\n";
     printf mhandle "AAA000";
     &flush(mhandle);
     #print "email = ", $emailto;

     $textlen = length($mfile);
     if ($textlen > $FIRSTPAGE) {
       $numpages = int $textlen/$FIRSTPAGE;
       $numpages = $numpages + 1; 
     }

# shall we currently assume 15cents per page for US.
# get the rate from a rate file in future.
     $rate = 15;
     $balance = $faxaccttab{$login}{'balance'}; 
     $balance = $balance - ($numpages * $rate);
     if ($balance <= 0) {
        status("$login: You do not have enough balance in your account. Click on the premium services link for more information.");
        exit;
     }

     if ($action = "Send") { 
        system "/bin/cat $ENV{HDTMPL}/content.html"; 
        #send email to faxsav at number@faxsav.com
        system "echo '#!/bin/ksh' > /var/tmp/sendfax$$"; 
	$mailcmd = "/bin/mail -s \"$faxto\" $emailto < $mfile";
        system "echo \"$mailcmd\" >> /var/tmp/sendfax$$";
        system "chmod 777 /var/tmp/sendfax$$";
        system "/usr/local/admin/bin/promote \"su - hotdiary -c /var/tmp/sendfax$$\"";
        system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage";
     }
   }

   # check the number of pages sent by this user and maintain
   # the balance.
   if ($action = "Send") {

	$faxtab{$entryno}{'fax'} = $faxto;
	$faxtab{$entryno}{'numpages'} = $numpages;

	# get date 
	$faxtab{$entryno}{'date'} = localtime();

	# get the balance and reduce the balance amount.
        # in future have the faxid.
	$faxaccttab{$login}{'login'} = $login;
     
	# update the balance with the deposit amount from depfaxadd
        $rate = 15;
	$faxaccttab{$login}{'balance'} = $balance; 
   }
   depositmoney $login;

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   
# save the info in db
   tied(%sesstab)->sync();
   tied(%faxaccttab)->sync();
   tied(%faxtab)->sync();
   tied(%logsess)->sync();
}

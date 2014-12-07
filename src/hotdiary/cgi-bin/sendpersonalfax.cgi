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
# FileName: sendpersonalfax.cgi
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
   hddebug "sendpersonalfax.cgi";

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXMESSAGE = 256000;
   $FIRSTPAGE = 1100;

   $biscuit = $input{'biscuit'};
   $hs = $input{'hs'};
   $rh = $input{'rh'};
   $jp = $input{jp};

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


   if ($biscuit eq "") {
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
              exit;
            }
         }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   }


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
   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $sesstab{$biscuit}{'time'} = time();

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

   
   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }
    

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $HDLIC = $input{'HDLIC'};
      # bind login table vars
      tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

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

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers',
        'account', 'topleft', 'topright', 'middleright',
        'bottomleft', 'bottomright', 'meta'] };

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


   $fchar = substr $login, 0, 1;
    $alphaindex = $fchar . '-index';
   $rh = $input{rh};
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

   if (notPhone(trim $input{'to'})) {
      status("$login: Invalid characters in Phone.  Click <a href=\"validation.html\"> here</a> for valid input.");
      exit;
   } else { 
      $to = trim $input{'to'};
   }

   hddebug "to = $to";
    
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

   $faxfile = $input{faxfile};

   if ($input{'faxfile'} ne "") {
      $mime_type = $input{'fmttype'};
      $suffix = "txt";
      if ($mime_type eq "text/plain") {
	  $encode_bit = "7bit";
	  $suffix = "txt";
      }
      if ($mime_type eq "image/jpg") {
         $encode_bit = "base64";
         $suffix = "jpg";
      }
      $faxfile = $input{'faxfile'};
      $filelen = length($faxfile);
      
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
 
      ($afile = "$ENV{HDHOME}/tmp/att$$.$suffix") =~ s/\n/\n<BR>/g;

     
      open thandle, ">$afile";
      printf thandle "%s", $input{'faxfile'};
      printf thandle "%s", "AAA000";
      &flush(thandle);
      close thandle;
      $mailcmd = "/usr/bin/metasend -b -S 800000 -m $mime_type -f $afile -s \"$faxto\" -e $encode_bit -t $emailto -F noreply\@hotdiary.com";

      system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/sendfax$$";  
      system "echo \"$mailcmd\" >> $ENV{HDHOME}/tmp/sendfax$$";
      system "chmod 777 $ENV{HDHOME}/tmp/sendfax$$";
      system "/usr/local/admin/bin/promote \"su - hotdiary -c $ENV{HDHOME}/tmp/sendfax$$\"";

     $dirtype = $input{dirtype};

     if ($dirtype eq "personaldir") {
        $execfile = "execpersonaldir.cgi";
     }
     if ($os ne "nt") {
        $execfile = encurl "$execfile";
     }
     $successpage = "$login: ($ulogin) does not exist. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execpersonaldir&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to personal address book.";   
     #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage";
     status ("$login: Fax has been sent");
   } else {

# text area message.
     $message = $input{'message'};
     ($mfile = "$ENV{HDHOME}/tmp/fax$$.txt") =~ s/\n/\n<BR>/g;
     open mhandle, ">$mfile";
     printf mhandle "%s", "$message\n";
     printf mhandle "%s", "AAA000";
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
        system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/sendfax$$"; 
	$mailcmd = "/bin/mail -s \"$faxto\" $emailto < $mfile";
        system "echo \"$mailcmd\" >> $ENV{HDHOME}/tmp/sendfax$$";
        system "chmod 777 $ENV{HDHOME}/tmp/sendfax$$";
        system "/usr/local/admin/bin/promote \"su - hotdiary -c $ENV{HDHOME}/tmp/sendfax$$\"";
        #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage";
        status "$login: Fax has been sent.";
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

# reset the timer.
   
# save the info in db
   tied(%sesstab)->sync();
   tied(%faxaccttab)->sync();
   tied(%faxtab)->sync();
   tied(%logsess)->sync();
}

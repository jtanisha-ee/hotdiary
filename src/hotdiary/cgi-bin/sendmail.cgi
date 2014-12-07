#!/usr/bin/perl

# Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: sendmail.cgi
# Purpose: Top screen for hotdiary carryon 
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;
use scheduleresolve::scheduleresolve;


# parse the command line
   &ReadParse(*input);
   hddebug "sendmail.cgi";

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp};
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
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
    'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};

   if ( ($framedomain ne "www.hotdiary.com") && ($framedomain ne "hotdiary.com")) {
      $flg = 2;
   } else {
      $flg = "";
   }

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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
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
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
               exit;
            }
         }
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $HDLIC = $input{'HDLIC'};
   # bind login table
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

   $sesstab{$biscuit}{'time'} = time();

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


   $basedir = trim $input{basedir};
   $filename = trim $input{filename};

   if ( ($filename =~ /\.\./) || ($filename =~ /\~/) ) {
     status("$login: Invalid filename specification. HotDiary Security Alert.");
     exit;
   }

   if ( ($basedir =~ /\.\./) || ($basedir =~ /\~/) ) {
     status("$login: Invalid directory specification. HotDiary Security Alert.");
     exit;
   }

   if (notCarryOnFile($basedir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) $msg.");
      exit;
   }

   if (notCarryOnName($filename)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) $msg.");
      exit;
   }

   $subject = trim $input{subject};
   ($tx, $ext) = split('\.', $filename);
   $emails =  multselkeys $input, "memail";
   hddebug "emails = $emails";
   (@hsh) = split(" ", $emails);
    $cc = trim $input{cc};
   (@tohsh) = split(",", $cc);

   $type =scheduleresolve::scheduleresolve::getmimetype($ext);

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $kfile = "$ENV{HDCARRYON}/aux/carryon/$login/$basedir/$filename";
   hddebug "filename = $filename, ext=$ext, basedir=$basedir, type =$type, cc=$cc, emails = $emails, kfile = $kfile";

   if (($emails eq "") && ($cc eq "")) {
      status("$login: Select an email address from contact manager list or enter email address(es) to send this file. Click <a href=\"/cgi-bin/execcarryonmail.cgi?framedomain=$framedomain&flg=$flg&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&basedir=$basedir&l=$login&biscuit=$biscuit&filename=$filename\">here</a> to enter email address.");
     exit;
   }


   $sender = $logtab{$login}{email}; 
   $cntr = 0;
   foreach $i (@hsh) {
      #($rem, $email) = split("-", $i);
      $email = $i;
      $email =~ s/%40/\@/g;
      hddebug "email = $email";
      if (!notEmailAddress($email))  {
         hddebug "metasend -b -S 800000 -m \"$type\" -f $kfile -s \"$subject\" -e \"base64\" -t \"$email\" -F noreply\@hotdiary.com";
         system "metasend -b -S 800000 -m \"$type\" -f $kfile -s \"$subject\" -e \"base64\" -t \"$email\" -F $sender";
	 $cntr = $cntr + 1;
      }
   }

   
   foreach $i (@tohsh) {
      hddebug "cc email = $i";
      if (!notEmailAddress($i))  {
         hddebug "metasend -b -S 800000 -m \"$type\" -f $kfile -s \"$subject\" -e \"base64\" -t \"$i\" -F noreply\@hotdiary.com";
         system "metasend -b -S 800000 -m \"$type\" -f $kfile -s \"$subject\" -e \"base64\" -t \"$i\" -F $sender";
	 $cntr = $cntr + 1;
      }
   }

   if ($cntr == 0) {
      status("$login: The names that you have selected do not have email address. Click <a href=\"/cgi-bin/execcarryonmail.cgi?framedomain=$framedomain&flg=$flg&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&basedir=$basedir&l=$login&biscuit=$biscuit&filename=$filename\">here</a> to enter email address or select names that have email addresses to send this file..");
      exit;
   }

   status("$login: File has been sent. Click <a href=\"/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file attache'.");

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

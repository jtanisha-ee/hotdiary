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
# FileName: delfile.cgi
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


# parse the command line
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   hddebug "delfile.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $vdomain = trim $input{'vdomain'};
   $rh = trim $input{'rh'};
   $jp = $input{jp};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
    'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};

   $framedomain = $input{framedomain};
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


   $dir = $input{dir};
   $dirpath = $input{dirpath};
   $dirname = $input{dirname};
   $filename = $input{filename};

   if (notCarryOnFile($filename)) {
      status("$login: You can only have alphabets(A-Z)(a-z), underscore(_), hyphen(-), forwardslash(/), single dot(.) and numerals(0-9) in your filename.");
      exit;
   }
   if (notCarryOnFile($dirpath)) {
      status("$login: You can only have alphabets(A-Z)(a-z), underscore(_), hyphen(-) and numerals(0-9) in your filename.");
      exit;
   }
   if (notCarryOnFile($dir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), underscore(_), hyphen(-) and numerals(0-9) in your filename.");
      exit;
   }
   if (notCarryOnFile($dirname)) {
    status("$login: You can only have alphabets(A-Z)(a-z) and numerals(0-9), underscore(_), hyphen(-) in your filename.");
      exit;
   }

   if ( ($dirpath =~ /\.\./) || ($dirpath =~ /\~/) ) {  
    status("$login: Invalid directory specification. HotDiary Security Alert.");
     exit;
   }
   if ( ($dirname =~ /\.\./) || ($dirname =~ /\~/) ) {  
    status("$login: Invalid directory specification. HotDiary Security Alert.");
      exit;
   }

   if ( ($dir =~ /\.\./) || ($dir =~ /\~/) ) {  
    status("$login: Invalid directory specification. HotDiary Security Alert.");
    exit;
   }  

   if ( ($filename =~ /\.\./) || ($filename =~ /\~/) ) {  
    status("$login: Invalid directory specification. HotDiary Security Alert.");
    exit;
   }  

   if (!-e ("$ENV{HDCARRYON}/aux/carryon/$login/permittab")) {
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/permittab";
   }
 
   # bind logsess table vars
   tie %permittab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDCARRYON}/aux/carryon/$login/permittab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['entryno', 'fn', 'permit', 'list', 'publish']};

   $msg = "Click <a href=\"http://www.hotdiary.com/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file attache'.";


   if ($dir eq "file") {
      if (($dirpath eq "") || ($filename eq "")) {
	 status("$login: Please specify a filename or a directory. Either filename or directory is empty. $msg");
	 exit;
      }
      if (-e "$ENV{HDCARRYON}/aux/carryon/$login/$dirpath/$filename") {
         system "rm $ENV{HDCARRYON}/aux/carryon/$login/$dirpath/$filename"; 
         foreach $entryno (sort keys %permittab) {
            if ("\L$permittab{$entryno}{fn}" eq "\L$filename") {
   	       delete $permittab{$entryno};
	    }
         }
	 status("$login: $filename file has been deleted. $msg");
      } else {
	 status("$login: No such file $filename exists in your folder. $msg");
	 exit;
      }
   } else {
      hddebug "came here1";
      if ($dir eq "dir") {
         if (($dirpath eq "") || ($dirname eq "")) {
	    status("$login: Please specify directory and directory path. Either directory or directory path is empty. $msg");
	    exit;
         }
 
         if (-d "$ENV{HDCARRYON}/aux/carryon/$login/$dirpath/$dirname") {
            system "rm -rf $ENV{HDCARRYON}/aux/carryon/$login/$dirpath/$dirname"; 
            foreach $entryno (sort keys %permittab) {
               if ("\L$permittab{$entryno}{fn}" eq "\L$dirname") {
                  delete $permittab{$entryno};
	       }
	    }
         }
	 status("$login: $dirname directory has been deleted. $msg");
      } else {
	 status("$login: No such file $filename exists in your folder. $msg");
	 exit;
      }
   }

   
   tied(%sesstab)->sync();
   tied(%logsess)->sync();


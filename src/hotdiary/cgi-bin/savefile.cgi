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
# FileName: savefile.cgi
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

   hddebug "savefile.cgi";
   $hddomain = $ENV{HDDOMAIN};
   $hotdiary = $ENV{HOTDIARY};
   $diary = $ENV{DIARY};

   $vdomain = trim $input{'vdomain'};
   hddebug "vdomain = $vdomain";
   $rh = trim $input{'rh'};
   $jp = $input{jp};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
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

   $framedomain = $input{framedomain};
   hddebug "framedomain = $framedomain";
   if ( ($framedomain ne "$hotdiary") && ($framedomain ne "$diary")) {
      $flg = 2;
   } else {
      $flg = "";
   }

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
   hddebug "HDLIC = $HDLIC";

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

   #$alphaindex = substr $login, 0, 1;
   #$alphaindex = $alphaindex . '-index';

   $filename = $input{filename};
   $basedir = $input{basedir};
   $newfilename = trim $input{newfilename};
   $entryno = $input{en}; 
   hddebug "entryno = $entryno, newfilename = $newfilename, filename=$filename, basedir=$basedir";

   if ( ($basedir =~ /\.\./) || ($basedir =~ /\~/) ) {
      status("$login: Invalid directory specification. HotDiary Security Alert.");
      exit;
   }

   if ( ($filename =~ /\.\./) || ($filename =~ /\~/) ) {
      status("$login: Invalid filename specification. HotDiary Security Alert.");
      exit;
   }

   if ( ($newfilename =~ /\.\./) || ($newfilename =~ /\~/) ) {
      status("$login: Invalid new filename specification. HotDiary Security Alert.");
      exit;
   }



   if (notCarryOnName($filename)) {
      status("$login: You can only have alphabets(a-z)(A-Z), numerals(0-9), underscore(_), hyphen(-), dot (.) in the specfied name. Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to My Carry-On '.");
      exit;
   }

   if (notCarryOnFile($basedir)) {
      status("$login: You can only have alphabets(a-z)(A-Z), numerals(0-9), underscore(_), hyphen(-), forward slash (/), dot (.). Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to My Carry-On'.");
      exit;
   }

   if (notCarryOnName($newfilename)) {
      status("$login: You can only have alphabets(a-z)(A-Z), numerals(0-9), underscore(_), hyphen(-), dot (.) in the specified name. Click <a href=\"/cgi-bin/execeditfile.cgi?framedomain=$framedomain&flg=$flg&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&login=$login&biscuit=$biscuit&en=$entryno&filename=$filename&basedir=$basedir\">here</a> to make changes to this file or directory.");
      exit;
   }

   #if ( (index $newfilename, '.') != -1 ) {
   #   (@compo) = split '\.', $newfilename;
   #   if ($#compo > 1) {
   #      status "Invalid file name suffix. Please enter file of the form \"myfile.doc\".";
   #      exit;
   #   }
   #   if ( ($compo[0] eq "") || ($compo[1] eq "") ) {
   #      status "Invalid file name. Please enter file of the form \"myfile.doc\" or simply myfile.";
   #      exit;
   #   }
   #}

   if (isHiddenFile($newfilename)) {
      status("$login: The file name ($newfilename) cannot begin with a '.', $msg");
      exit;
   }

   if (!-e ("$ENV{HDCARRYON}/aux/carryon/$login/permittab")) {
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/permittab";
   }

   # bind permittab table vars
   tie %permittab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDCARRYON}/aux/carryon/$login/permittab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['entryno', 'fn', 'permit', 'list', 'publish'] };


   $list = $input{list};
   $publish = $input{publish};
   $radio1 = $input{radio1};
   hddebug "list = $list, publish=$publish, permission=$radio1";
   if ($radio1 eq "") {
       $radio1 = "personal";
   }

 
   $exists = 0; 
   if ($newfilename eq $filename ) {
      status("$login: New filename or directory must be different from the existing file or directory."); 
      exit;
   }
 
   $basedir = substr $basedir, 2, length($basedir); 
   if (($newfilename ne "") && ($newfilename ne $filename)) {
      if (exists($permittab{$entryno})) {
         if ("\L$permittab{$entryno}{fn}" eq "\L$filename") {
            $exists = 1;
            $permittab{$entryno}{'permit'} = $radio1;
            hddebug "radio1 = $permittab{$entryno}{'permit'}";
            $permittab{$entryno}{'list'} = $list;
            $permittab{$entryno}{'fn'} = $newfilename;
            if ($basedir ne "") {
               if (-d "$ENV{HDCARRYON}/aux/carryon/$login/$basedir") {
	          system "chmod +x $ENV{HDCARRYON}/aux/carryon/$login/$basedir";
                  system "mv $ENV{HDCARRYON}/aux/carryon/$login/$basedir/$filename $ENV{HDCARRYON}/aux/carryon/$login/$basedir/$newfilename";
               } else {
                   system "mv $ENV{HDCARRYON}/aux/carryon/$login/permittab/$filename $ENV{HDCARRYON}/aux/carryon/$login/permittab/$newfilename";
	       }
            }
            if ($publish eq "on") {
               $permittab{$entryno}{publish} = "CHECKED";
            }
            tied(%permittab)->sync();
         }
      }
   }

   ## create a new entry in the permittab for this file
   if ($exists == 0) { 
      $entryno = getkeys();
      $permittab{$entryno}{entryno} = $entryno;      
      if ($input{publish} eq "on") {
         $permittab{$entryno}{publish} = "CHECKED";
      }
      $permittab{$entryno}{'permit'} = $radio1;
      $permittab{$entryno}{'list'} = $list;
      $permittab{$entryno}{'fn'} = $newfilename;
      tied(%permittab)->sync();
      if ($basedir ne "") {
         if (-d "$ENV{HDCARRYON}/aux/carryon/$login/$basedir") {
             if ($basedir ne "") {
		 system "chmod +x $ENV{HDCARRYON}/aux/carryon/$login/$basedir";
                 system "mv $ENV{HDCARRYON}/aux/carryon/$login/$basedir/$filename $ENV{HDCARRYON}/aux/carryon/$login/$basedir/$newfilename";
              } else {
                  system "mv $ENV{HDCARRYON}/aux/carryon/$login/permittab/$filename $ENV{HDCARRYON}/aux/carryon/$login/permittab/$newfilename";
              }
          }
      }
    }

   hddebug "HDLIC = $HDLIC, flg = $flg";
   status("$login: File has been updated. Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?framedomain=$framedomain&flg=$flg&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file Carry-On'.");

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

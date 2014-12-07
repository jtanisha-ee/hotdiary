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
# FileName: uploadfile.cgi
# Purpose: Top screen for hotdiary carryon
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;


# parse the command line
   &ReadParse(*input);
   hddebug("uploadfile.cgi");

   #print &PrintHeader;
   #print "Hello World\n";
   #print &PrintVariables(*input);
   #exit;

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $hddomain = $ENV{HDDOMAIN};
   $hotdiary = $ENV{HOTDIARY};
   $diary = $ENV{DIARY};

   $vdomain = trim $input{'vdomain'};
   $rh = trim $input{'rh'};
   $jp = $input{jp};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   }
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $os = $input{os};

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
    'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   $uploadfile = $input{uploadfile};
   $len = length $uploadfile;

   hddebug "biscuit = $biscuit, hs = $hs, jp=$jp, length = $len";
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
               status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
               exit;
            }
         }
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   $HDLIC = $input{'HDLIC'};
   #hddebug "hdlic = $HDLIC";

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

   $msg = "Click <a href=\"$ENV{HDDOMAIN}/cgi-bin/execfilebrowser.cgi?jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&currdir=MyFolder&basedir=.&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file attache'.";

   $msize = qx{du -s $ENV{HDCARRYON}/aux/carryon/$login};
   $msize =~ s/\n//g;
   ($msize, $rem) = split(" ", $msize);
   hddebug "file size = $msize";
   if ( ($msize > 20000) && ($login ne "mjoshi") && ($login ne "manoj") && ($login ne "smitha") ) {
      status("$login: You have exceeded your initial stage quota of 20 MB.<p> You can apply for an extension to a total free quota of 50 MB after you make a 2 year deposit of $10 by mail, which will be returned after you are done using CarryOn or at the end of 2 years, whichever comes first.<p> If you wish to take advantage of this offer please mail a US Dollar bank check of $10 made payable to Manoj Joshi, 3653 Santa Croce Ct, San Jose, CA 95148.<p> Any storage beyond a period of 2 years is not free, and if you wish to continue storing your data on our system beyond 2 years, we will apply your deposit towards the payment required to continue using our Carryon system. If you wish, you can upgrade your carryon storage quota to 100 MB for USD 9.99/year. $msg");
      exit;
   }

   #$startdir = $input{'startdir'};
   $jumpdir = $input{'jumpdir'};
   $currdir = $input{currdir};
   $basedir = $input{basedir};
   $uploadname = trim $input{'uploadname'};
   $directory = trim $input{'directory'};
   if (notCarryOnFile($jumpdir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) ($jumpdir) $msg.");
      exit;
   }
   if (notCarryOnFile($currdir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) in current directory ($currdir) $msg.");
      exit;
   }
   if (notCarryOnFile($basedir)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-), forwardslash(/), and a single dot(.) in directory ($basedir) $msg.");
      exit;
   }
   if (notCarryOnName($uploadname)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-) and a single dot(.) in a filename ($uploadname) $msg.");
      exit;
   }
   if (notCarryOnName($directory)) {
      status("$login: You can only have alphabets(A-Z)(a-z), numerals(0-9), underscore(_), hyphen(-) and a single dot(.) in a directory ($directory) $msg.");
      exit;
   }
   if (isHiddenFile($directory)) {
      status("$login: The directory name ($directory) cannot begin with a '.', $msg");
      exit;
   }
   if (isHiddenFile($uploadname)) {
      status("$login: The file name ($uploadname) cannot begin with a '.', $msg");
      exit;
   }

   if ( ($jumpdir =~ /\.\./) || ($jumpdir =~ /\~/) ) {
    status("$login: Invalid directory specification ($jumpdir). HotDiary Security Alert.");
    exit;
   }    
   if ( ($directory =~ /\.\./) || ($directory =~ /\~/) ) {
    status("$login: Invalid directory specification ($directory). HotDiary Security Alert.");
    exit;
   }    
   if ( ($basedir =~ /\.\./) || ($basedir =~ /\~/) ) {
    status("$login: Invalid directory specification ($basedir). HotDiary Security Alert.");
    exit;
   }    
   if ( ($uploadname =~ /\.\./) || ($uploadname =~ /\~/) ) {
    status("$login: Invalid directory specification ($uploadname). HotDiary Security Alert.");
    exit;
   }    
   if ( ($currdir =~ /\.\./) || ($currdir =~ /\~/) ) {
    status("$login: Invalid directory specification ($currdir). HotDiary Security Alert.");
    exit;
   }    
   #if ( (index $uploadname, '.') != -1 ) {
   #   (@compo) = split '\.', $uploadname;
   #   if ($#compo > 1) {
   #      status "Invalid file name suffix. Please enter file of the form \"myfile.doc\" or simply myfile.";
   #      exit;
   #   }
   #   if ( ($compo[0] eq "") || ($compo[1] eq "") ) {
   #      status "Invalid file name. Please enter file of the form \"myfile.doc\".";
   #      exit;
   #   }
   #}

   #hddebug "jumpdir = $jumpdir, currdir = $currdir";
   $startdir = "$ENV{HDCARRYON}/aux/carryon/$login";
   if ((index "\L$startdir", "\L$ENV{HDCARRYON}/aux/carryon/$login") != -1) {
	$startdir = "$ENV{HDCARRYON}/aux/carryon/$login";
   } 

   $newdir = $startdir;
   if ($basedir ne "") {
      $newdir = "$newdir/$basedir";
   }
   if ($currdir ne "") {
      $newdir = "$newdir/$currdir";
   }


   if ($newdir eq "$ENV{HDCARRYON}/aux/carryon/$login") {
      status("$login: You cannot upload files in this directory. Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&basedir=.&currdir=MyFolder&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file attache'.");
      exit;
   }

   $action = $input{CreateDirectory};
   if ($action eq "CreateDirectory") {
      $directory = trim $input{directory};
      #($directory =~ /[^a-zA-Z\d\s]+/);
      if ($directory =~ /[^a-zA-Z\-\_\d]+/) {
	 status ("$login: Please enter a directory name that has [a-z][A-Z][0-9][-_] characters only.  Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file attache'.");
	 exit;
      }  

      if ($directory ne "") {
         $mydir = qx{basename $newdir};
         $mydir =~ s/\n//g;
         if (-d "$newdir/$directory") {
            status "$login: Directory $directory already exists. Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?rh=&hs=&vdomain=$diary&jp=&HDLIC=JE6M-E3JH-TEP6-7389&biscuit=$biscuit&basedir=&jumpdir=$mydir&currdir=$mydir\">here</a> to specify another directory.";
            exit;
         }
         system "mkdir -p $newdir/$directory";
         system "chmod 755 $newdir/$directory";
	 status("$login: Directory $directory has been created. Click <a href=\"$hddomain/cgi-bin/execfilebrowser.cgi?rh=&hs=&vdomain=$diary&jp=&HDLIC=JE6M-E3JH-TEP6-7389&biscuit=$biscuit&basedir=&jumpdir=$mydir&currdir=$mydir\">here</a> to view it.");
	 exit;
      }
   }

   $uploadname = trim $input{'uploadname'};
   hddebug "uploadname = $uploadname";
   $contents = $input{'uploadfile'};
   $len = length $contents;
   hddebug "len = $len, uploadname = $uploadname";
   
   if ((length $contents) eq "0") {
      status ("$login: You have not entered any file or directory on HotDiary carry-on. Please enter a filename or directory you would like to upload.");
      exit;
   }

   #$contents =~ s/\r//g;
   #print &PrintVariables(*input);
   if ($input{'uploadname'} eq "") {
      status ("$login: Please enter file name for upload.");
      exit;
   }

   $uploadname = $input{'uploadname'};
   #$contents =~ s/\"/\\\"/g;
   open thandle, ">$newdir/$uploadname";
   printf thandle "%s", $contents;
   close thandle;
   system "chmod -x $newdir/$uploadname";
   $sbhalla = qx{file $newdir/$uploadname};
   if ($login ne "mjoshi") {
   if ( (index $sbhalla, "executable") != -1) {
      status("You cannot load this file, as it happens to be an executable.");
      if ( ($newdir ne "") && ($uploadname ne "") ) {
         system "rm -f $newdir/$uploadname";
      }
      exit; 
   }
   }

   $outr = qx{file $uploadname};
   hddebug "startdir = $startdir, jumpdir = $jumpdir";
   open thandle, ">$newdir/$uploadname";
   printf thandle "%s", $contents;
   close thandle;

   # fixed the bug of chmod -x which was creating drw- permissions in
   # some folders for user.

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
         ORDER => ['entryno', 'fn', 'permit', 'list', 'publish'] };

   $entryno = getkeys();
   $permittab{$entryno}{fn} = trim $input{uploadname};
   $permittab{$entryno}{entryno} = $entryno;

   $framedomain = $input{framedomain};
   hddebug "framedomain = $framedomain";
   if ( ($framedomain ne "$hotdiary") && ($framedomain ne "$diary")) {
      $flg = 2;
   } else {
      $flg = "";
   }

   status ("$login: Your specified file $input{'uploadname'} has been successfully uploaded and it occupies $len bytes of space. Click <a href=\"$ENV{HDDOMAIN}/cgi-bin/execfilebrowser.cgi?p1=biscuit&p2=f&flg=$flg&framedomain=$framedomain&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to browse the files.");


   tied(%permittab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();


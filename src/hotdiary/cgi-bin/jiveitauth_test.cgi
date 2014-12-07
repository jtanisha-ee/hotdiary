#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: jiveitauth.cgi
# Purpose: Authenticate JiveIt downloader
# 
# Creation Date: 08-14-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input); 

$jp = $input{jp};

# bind login table vars

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
	   'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = $input{login};
if ($login eq "") {
   status("Please specify a non-empty login name");
   exit;
}

if (!(exists $logtab{$login})) {
   #status("Member login $login does not exist.");
   #exit;
}


#$password = $input{password};
#if ("\L$password" ne "\L$logtab{$login}{password}") {
   #status("The password you have specified for $login is invalid.");
#   exit;
#}

$jivetab{$login}{url} = adjusturl $input{url};
$jivetab{$login}{title} = adjusturl $input{title};
$jivetab{$login}{logo} = adjusturl $input{logo};
$jivetab{$login}{banner} = adjusturl $input{banner};

if ($input{url} eq "") {
   status("Please enter your homepage.");
   exit;
}

if ($input{title} eq "") {
   $title = "JiveIt! Calendars";
}

if ($input{logo} eq "") {
   $logo = "http://www.hotdiary.com/images/memocalendar_new.gif";
}


$ftpsel = $input{ftpsite};
$memlogin = $input{memlogin};

if ($ftpsel eq "Tripod") {
    $ftpsite = "ftp.tripod.com";
    $homesite = "http://members.tripod.com/$memlogin";
}

if ($ftpsel eq "Other") {
    $ftpsite = $input{rhost}; 
    $homesite = $url;
}

if ($ftpsel eq "Xoom") {
    $ftpsite = "ftp.xoom.com";
    $homesite = "http://members.xoom.com/$memlogin";
}

if ($ftpsel eq "GeoCities") {
    $ftpsite = "ftp.geocities.com";
    $homesite = $input{url};
}

$ftpfilename = $input{ftpfilename};
$mempassword = $input{mempassword};
$update = $input{update};
$overwrite = $input{overwrite};

hddebug "overwrite = $overwrite";
hddebug "ftpfilename = $ftpfilename";
hddebug "memlogin = $memlogin";
hddebug "mempassword = $mempassword";
hddebug "update = $update";
hddebug "ftpsite = $ftpsite";

$rtime = getkeys();
system "mkdir -p $ENV{HDREP}/$login/$rtime";

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitindex.html";
$prml = strapp $prml, "templateout=$ENV{HDREP}/$login/$rtime/myindex.html";
$prml = strapp $prml, "home=$jivetab{$login}{url}";
$prml = strapp $prml, "jp=$login";
parseIt $prml;

#$prml = "";
#$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitleftframe.html";
#$prml = strapp $prml, "templateout=$ENV{HDREP}/$login/$rtime/leftFrame.html";
#$prml = strapp $prml, "jp=$login";
#parseIt $prml;

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/redirect.html";
$prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/jiveitauth-$rtime-$$.html";
$prml = strapp $prml, "redirecturl=$ENV{HDDOMAIN}/rep/$login/$rtime";
parseIt $prml;

system "cp $ENV{HDTMPL}/jiveitreadme $ENV{HDREP}/$login/$rtime/README";
system "chown -R nobody:nobody $ENV{HDREP}/$login/$rtime";
system "chmod -R 755 $ENV{HDREP}/$login/$rtime";


if ($update eq "on") {

   $lsout = "/tmp/lsout$login$$";
   $lserror = "/tmp/lserror$login$$";
   $putout = "/tmp/putout$login$$";
   $puterror = "/tmp/puterror$login$$";
   hddebug "lsout = $lsout";
   hddebug "lserror = $lserror";
   hddebug "putout = $putout";
   hddebug "puterror = $puterror";

   system "echo '#!/bin/ksh' > /var/tmp/hdftpclientcmd-$login$$";
   $ftplscmd = "/usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword ls $lsout $lserror";
   system "echo \"$ftplscmd\" >> /var/tmp/hdftpclientcmd-$login$$";
   system "chmod 777 /var/tmp/hdftpclientcmd-$login$$";
   system "/usr/local/admin/bin/promote \"su - gubri -c /var/tmp/hdftpclientcmd-$login$$\"";

   #system "/usr/local/admin/bin/promote \"su - gubri -c /usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword ls $lsout $lserror\"";

   $fncount = 0;
   $errorcount = 0;

   if (-e $lserror)  {
      if ((-s $lserror) == 0) {
         if (-e $lsout)  {
            #$fncount = qx {/usr/bin/grep --count -i $ftpfilename $lsout}; 
            $fncount = qx {cat $lsout | grep -i $ftpfilename | wc -l}; 
	 }
      }
   }

   hddebug "fncount = $fncount";
   $ftpputcmd = "\"put $ENV{HDREP}/$login/$rtime/myindex.html $ftpfilename\"";
   system "echo '#!/bin/ksh' > /var/tmp/hdftpputcmd-$login$$";
   $ftpputcmd = "/usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword \'$ftpputcmd\' $putout $puterror";
   system "echo \"$ftpputcmd\" >> /var/tmp/hdftpputcmd-$login$$";
   system "chmod 777 /var/tmp/hdftpputcmd-$login$$";
   system "/usr/local/admin/bin/promote \"su - gubri -c /var/tmp/hdftpputcmd-$login$$\"";
              
   if ($fncount > 0 ) {
      if ($overwrite eq "on") {
         system "/usr/local/admin/bin/promote \"su - gubri -c /var/tmp/hdftpputcmd-$login$$\"";

         #system "/usr/local/admin/bin/promote \"su - gubri -c /usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword $ftpputcmd $putout $puterror\"";
        
         if (-e $puterror) {
           if ((-s $puterror) == 0 ) {
              if (-e $putout) {
	         status("File $ftpfilename has been successfully placed on your $ftpsite. Click <a href=\"$homesite/$ftpfilename\">here</a> to view your JiveIt! Website");
                 system "/bin/cat $putout";
                 exit;
              }
            }
         }
      } else {
	 status("Remote File with $ftpfilename already exists and is not overwritten, as you have chosen not to overwrite remote file. You can either manually download the file or decide to select Overwrite Remote File to overwrite the file. If you choose to manually download the file, you can read the instructions on how to download the file by clicking on: <a href=\"$ENV{HDDOMAIN}/rep/$login/$rtime\">Download File And Instructions Area</a><p>If you choose to Overwrite Remote File, use the browser Back button now, to change the option.");
	 exit;
      }
   } else {
         system "/usr/local/admin/bin/promote \"su - gubri -c /var/tmp/hdftpputcmd-$login$$\"";
      #system "/usr/local/admin/bin/promote \"su - gubri -c /usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword $ftpputcmd $putout $puterror\"";
      if (-e $puterror) {
         if ((-s $puterror) == 0) {
            if (-e $putout) {
                status("File $ftpfilename has been successfully placed on $ftpsite.Click <a href=\"$homesite/$ftpfilename\">here</a> to view your JiveIt! Website");
                system "/bin/cat $putout";
               exit;
	    }
         }
      }
   }
}


system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHREP}/$login/jiveitauth-$rtime-$$.html";



tied(%jivetab)->sync();

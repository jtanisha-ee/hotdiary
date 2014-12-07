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
	    'topleft', 'topright', 'middleright', 'bottomleft', 
            'bottomright', 'meta'] };

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

if (exists $jivetab{$jp}) {
   status "A JiveIt! account in the name $jp already exists. Please <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$jp\">login to the admin page</a> for this account, if you would like to customize or change the configuration.";
   exit;
}


#$password = $input{password};
#if ("\L$password" ne "\L$logtab{$login}{password}") {
   #status("The password you have specified for $login is invalid.");
#   exit;
#}

$login = "\L$login";

$alphaindex = substr $login, 0, 1;
$alphaindex = $alphaindex . '-index';

$jivetab{$login}{url} = adjusturl $input{url};
$jivetab{$login}{title} = adjusturl $input{title};
$jivetab{$login}{logo} = adjusturl $input{logo};
$jivetab{$login}{banner} = adjusturl $input{banner};
$jivetab{$login}{topleft} = adjusturl $input{topleft};
$jivetab{$login}{topright} = adjusturl $input{topright};
$jivetab{$login}{middleright} = adjusturl $input{middleright};
$jivetab{$login}{bottomleft} = adjusturl $input{bottomleft};
$jivetab{$login}{bottomright} = adjusturl $input{bottomright};
$jivetab{$login}{account} = 0;
$title = trim $jivetab{$login}{title};
if ($title eq "") {
   $title = "My Portal";
}

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
system "mkdir -p $ENV{HDREP}/$alphaindex/$login/$rtime";

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitindex.html";
$prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/$rtime/myindex.html";
$prml = strapp $prml, "home=$jivetab{$login}{url}";
$prml = strapp $prml, "title=$title";
$prml = strapp $prml, "jp=$login";
parseIt $prml;

#qx{cp $ENV{HTTPHOME}/html/hd/portaltemplate.txt $ENV{HDREP}/$alphaindex/$login/$rtime};
qx{cp $ENV{HDREP}/$alphaindex/$login/$rtime/myindex.html $ENV{HDREP}/$alphaindex/$login/$rtime/myindex.txt};

#$prml = "";
#$prml = strapp $prml, "template=$ENV{HDTMPL}/jiveitleftframe.html";
#$prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/$rtime/leftFrame.html";
#$prml = strapp $prml, "jp=$login";
#parseIt $prml;

#$prml = "";
#$prml = strapp $prml, "template=$ENV{HDTMPL}/redirect.html";
#$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/jiveitauth-$rtime-$$.html";
#$prml = strapp $prml, "redirecturl=$ENV{HDDOMAIN}/rep/$alphaindex/$login/$rtime";
#parseIt $prml;

#system "cp $ENV{HDTMPL}/jiveitreadme $ENV{HDREP}/$alphaindex/$login/$rtime/README";
#system "chown -R nobody:nobody $ENV{HDREP}/$alphaindex/$login/$rtime";
#system "chmod -R 755 $ENV{HDREP}/$alphaindex/$login/$rtime";


if ($update eq "on") {

   $lsout = "$ENV{HDHOME}/tmp/lsout$login$$";
   $lserror = "$ENV{HDHOME}/tmp/lserror$login$$";
   $putout = "$ENV{HDHOME}/tmp/putout$login$$";
   $puterror = "$ENV{HDHOME}/tmp/puterror$login$$";
   hddebug "lsout = $lsout";
   hddebug "lserror = $lserror";
   hddebug "putout = $putout";
   hddebug "puterror = $puterror";

   system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/hdftpclientcmd-$login$$";
   $ftplscmd = "/usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword ls $lsout $lserror";
   system "echo \"$ftplscmd\" >> $ENV{HDHOME}/tmp/hdftpclientcmd-$login$$";
   system "chmod 777 $ENV{HDHOME}/tmp/hdftpclientcmd-$login$$";
   #system "/usr/local/admin/bin/promote \"su - gubri -c $ENV{HDHOME}/tmp/hdftpclientcmd-$login$$\"";
   system "$ENV{HDHOME}/tmp/hdftpclientcmd-$login$$";

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
   $ftpputcmd = "\"put $ENV{HDREP}/$alphaindex/$login/$rtime/myindex.html $ftpfilename\"";
   system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/hdftpputcmd-$login$$";
   $ftpputcmd = "/usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword \'$ftpputcmd\' $putout $puterror";
   system "echo \"$ftpputcmd\" >> $ENV{HDHOME}/tmp/hdftpputcmd-$login$$";
   system "chmod 777 $ENV{HDHOME}/tmp/hdftpputcmd-$login$$";
   #system "/usr/local/admin/bin/promote \"su - gubri -c $ENV{HDHOME}/tmp/hdftpputcmd-$login$$\"";
   system "$ENV{HDHOME}/tmp/hdftpputcmd-$login$$";
              
   if ($fncount > 0 ) {
      if ($overwrite eq "on") {
         #system "/usr/local/admin/bin/promote \"su - gubri -c $ENV{HDHOME}/tmp/hdftpputcmd-$login$$\"";
         system "$ENV{HDHOME}/tmp/hdftpputcmd-$login$$";

         #system "/usr/local/admin/bin/promote \"su - gubri -c /usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword $ftpputcmd $putout $puterror\"";
        
         if (-e $puterror) {
           if ((-s $puterror) == 0 ) {
              if (-e $putout) {
	         #status("File $ftpfilename has been successfully placed on $ftpsite in your member directory. Click <a href=\"$homesite/$ftpfilename\">here</a> to view your JiveIt! Website");
	         status("<h3>Please Take A Print-Out Of This Page</h3>File $ftpfilename has been successfully placed on $ftpsite in your member directory. <p>Congratulations! You have successfully opened a JiveIt! account.<p>Your JiveIt! Admin ID is $login and is the same as your HotDiary member ID.<p>Please click <a href=\"http://www.1800calendar.com/index.cgi?jp=$login\" target=_main>http://www.1800calendar.com/index.cgi?jp=$login</a> to proceed to view a copy of your JiveIt! page.<p>If you would like to customize portal templates for JiveIt! click <a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>JiveIt! Portal Templates</a><p>You can click <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\" target=_main>http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login</a> if you would like to administer your JiveIt! site at any time.<p>If you would like to start all over again, please click <a href=\"http://www.hotdiary.com/jiveitauth.shtml\">http://www.hotdiary.com/jiveitauth.shtml</a>");
                 system "/bin/cat $putout";
                 exit;
              }
            }
         }
      } else {
	 #status("<FONT COLOR=ff0000>Remote File with $ftpfilename already exists</FONT> and is not overwritten, as you have chosen not to overwrite remote file. You can either manually download the file or decide to select Overwrite Remote File to overwrite the file. If you choose to manually download the file, you can read the instructions on how to download the file by clicking on: <a href=\"$ENV{HDDOMAIN}/rep/$alphaindex/$login/$rtime\"><p>Download File And Instructions Area</a><p>If you choose to Overwrite Remote File, <FONT COLOR=0000ff>use the browser Back button now</FONT>, to change the option.");
	 status("<h3>Please Take A Print-Out Of This Page</h3> <FONT COLOR=ff0000>Remote File with $ftpfilename already exists</FONT> and is not overwritten, as you have chosen not to overwrite remote file. You can either manually download the file or decide to select Overwrite Remote File to overwrite the file.  <p>If you choose to Overwrite Remote File, <FONT COLOR=0000ff>use the browser Back button now</FONT>, to change the option. <p>Congratulations! You have successfully opened a JiveIt! account.<p>Your JiveIt! Admin ID is $login and is the same as your HotDiary member ID.<p>Please click <a href=\"http://www.1800calendar.com/index.cgi?jp=$login\" target=_main>http://www.1800calendar.com/index.cgi?jp=$login</a> to proceed to see a copy of your JiveIt! page. <p>Please click <a href=\"http://www.hotdiary.com/rep/$alphaindex/$login/$rtime/myindex.txt\">here</a> to download an example frame based HTML document that you may use as a starting point to launch JiveIt! on your site. <p>If you would like to customize JiveIt! portal templates click <a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>http://www.hotdiary.com/downloadtemplates.html</a><p>You can click <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\" target=_main>http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login</a> if you would like to administer your JiveIt! site at any time.<p>If you would like to start all over again, please click <a href=\"http://www.hotdiary.com/jiveitauth.shtml\">http://www.hotdiary.com/jiveitauth.shtml</a>.");
	 exit;
      }
   } else {
         #system "/usr/local/admin/bin/promote \"su - gubri -c $ENV{HDHOME}/tmp/hdftpputcmd-$login$$\"";
         system "$ENV{HDHOME}/tmp/hdftpputcmd-$login$$";
      #system "/usr/local/admin/bin/promote \"su - gubri -c /usr/local/hotdiary/cgi-bin/hdftpclient $ftpsite $memlogin $mempassword $ftpputcmd $putout $puterror\"";
      if (-e $puterror) {
         if ((-s $puterror) == 0) {
            if (-e $putout) {
                #status("File $ftpfilename has been successfully placed on $ftpsite in your member directory. Click <a href=\"$homesite/$ftpfilename\">here</a> to view your JiveIt! Website");
                status("<h3>Please Take A Print-Out Of This Page</h3>File $ftpfilename has been successfully placed on $ftpsite in your member directory.<p>Congratulations! You have successfully opened a JiveIt! account.<p>Your JiveIt! Admin ID is $login and is the same as your HotDiary member ID.<p>Please click <a href=\"http://www.1800calendar.com/index.cgi?jp=$login\" target=_main>http://www.1800calendar.com/index.cgi?jp=$login</a> to proceed to see a copy of your JiveIt! page. <p>Please click <a href=\"http://www.hotdiary.com/rep/$alphaindex/$login/$rtime/myindex.txt\">here</a> to download an example frame based HTML document that you may use as a starting point to launch JiveIt! on your site. <p>If you would like to customize JiveIt! portal templates click <a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>http://www.hotdiary.com/downloadtemplates.html</a><p>You can click <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\" target=_main>http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login</a> if you would like to administer your JiveIt! site at any time.<p>If you would like to start all over again, please click <a href=\"http://www.hotdiary.com/jiveitauth.shtml\">http://www.hotdiary.com/jiveitauth.shtml</a>");
               #system "/bin/cat $putout";
               exit;
	    }
         } else {
             $myerror = qx{cat $puterror $putout};
	     #status("<h3>Please Take A Print-Out Of This Page</h3> FTP failed. The following error occurred when we tried to transport your file $ftpfilename to $homesite:<BR><CENTER>$myerror</CENTER><BR>.Make sure the hostname($ftpsite), login($memlogin), and password($mempassword) are correct. <BR>You must have a ftp member login created on $homesite and your website at $homesite must exist, before you use JiveIt! JiveIt! does not create a member login on $homesite. It only allows you to upload files to an existing ftp site like $homesite.<BR>If you would like to upload the website manually, you can click <a href=\"$ENV{HDDOMAIN}/rep/$alphaindex/$login/$rtime\">here</a> to download it manually");
	     status("<h3>Please Take A Print-Out Of This Page</h3> FTP failed. The following error occurred when we tried to transport your file $ftpfilename to $homesite:<BR><CENTER>$myerror</CENTER><BR>.Make sure the hostname($ftpsite), login($memlogin), and password($mempassword) are correct. <BR>You must have a ftp member login created on $homesite and your website at $homesite must exist, before you use JiveIt! JiveIt! does not create a member login on $homesite. It only allows you to upload files to an existing ftp site like $homesite. <p>Congratulations! You have successfully opened a JiveIt! account.<p>Your JiveIt! Admin ID is $login and is the same as your HotDiary member ID.<p>Please click <a href=\"http://www.1800calendar.com/index.cgi?jp=$login\" target=_main>http://www.1800calendar.com/index.cgi?jp=$login</a> to proceed to your JiveIt! page. <p>Please click <a href=\"http://www.hotdiary.com/rep/$alphaindex/$login/$rtime/myindex.txt\">here</a> to download an example frame based HTML document that you may use as a starting point to launch JiveIt! on your site.<p>If you would like to customize JiveIt! portal templates click <a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>http://www.hotdiary.com/downloadtemplates.html</a><p>You can click <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\" target=_main>http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login</a> if you would like to administer your JiveIt! site at any time.<p>If you would like to start all over again, please click <a href=\"http://www.hotdiary.com/jiveitauth.shtml\">http://www.hotdiary.com/jiveitauth.shtml</a> ");
	     exit;
         }
      }
   }
}


#system "cat $ENV{HDTMPL}/content.html";
#system "cat $ENV{HDHREP}/$alphaindex/$login/jiveitauth-$rtime-$$.html";

status "<h3>Please Take A Print-Out Of This Page</h3>Congratulations! You have successfully opened a JiveIt! account.<p>Your JiveIt! Admin ID is $login and is the same as your HotDiary member ID.<p>Please click <a href=\"http://www.1800calendar.com/index.cgi?jp=$login\" target=_main>http://www.1800calendar.com/index.cgi?jp=$login</a> to proceed to your JiveIt! page. <p>Please click <a href=\"http://www.hotdiary.com/rep/$alphaindex/$login/$rtime/myindex.txt\">here</a> to download an example frame based HTML document that you may use as a starting point to launch JiveIt! on your site.<p>If you would like to customize JiveIt! portal templates click <a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>http://www.hotdiary.com/downloadtemplates.html</a><p>You can click <a href=\"http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login\" target=_main>http://www.1800calendar.com/cgi-bin/execjiveitadmin.cgi?jp=$login</a> if you would like to administer your JiveIt! site at any time.<p>If you would like to start all over again, please click <a href=\"http://www.hotdiary.com/jiveitauth.shtml\">http://www.hotdiary.com/jiveitauth.shtml</a>";

tied(%jivetab)->sync();

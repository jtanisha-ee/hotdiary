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
# FileName: jiveitupload.cgi
# Purpose: templateupload program for custom files download 
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
   hddebug("templatedownload.cgi");


   $jp = $input{login};
   $login = $jp;

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   #system "mkdir -p "$ENV{FTPHOME}/

   $uploadname = trim $input{'uploadname'};
   $contents = $input{'uploadfile'};
   $len = length $contents;
   hddebug "len = $len, uploadname = $uploadname";
   $os = $input{os};
   $vdomain = $input{vdomain};
   $rh = $input{rh};
   $hs = $input{hs};


   $msg = adjusturl "Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitfile.cgi?p1=login&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=2&le3=HDLIC&HDLIC=$HDLIC&login=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to upload files.";

   $msg1 = adjusturl "Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitdisplay.cgi?p1=jp&p2=file&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=3&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&file=file&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to manage JiveIt! account.";
   
   if ((length $contents) eq "0") {
      status ("$login: You have not selected any file to upload. Please select a file. <BR> $msg <BR>$msg1");
      exit;
   }

   if ($input{'uploadname'} eq "") {
      status ("$login: Please enter filename for upload. <BR> $msg<BR> $msg1");
      exit;
   }


   $fchar = substr $jp, 0, 1;
   $alphaindex = $fchar . '-index';

   if (!-e ("$ENV{HDDATA}/$alphaindex/$jp/templates")) {
      system "mkdir -p $ENV{HDDATA}/$alphaindex/$jp/templates";
      system "chmod 755 $ENV{HDDATA}/$alphaindex/$jp/templates";
      system "chown nobody:nobody $ENV{HDDATA}/$alphaindex/$jp/templates";
   }

   $dir = "$ENV{HDDATA}/$alphaindex/$jp/templates";

   #open thandle, ">$dir/$uploadname";
   #printf thandle "%s", $contents;
   #close thandle;

   #system "chmod -x $dir/$uploadname";
   #$sbhalla = qx{file $dir/$uploadname};
   #if ( (index $sbhalla, "executable") != -1) {
   #   status("You cannot load this file, as it happens to be an executable.");
   #   if ( ($dir ne "") && ($uploadname ne "") ) {
   #      system "rm -f $dir/$uploadname";
   #   }
   #   exit; 
   #}

   if ($uploadname eq "PortalTemplate") {
      $uploadname = "topcal.html";
   } else {
   if ($uploadname eq "JiveIt") {
      $uploadname = "jiveit.html";
   } else {
   if ($uploadname eq "DailyCalendar") {
      $uploadname = "dailycalendar.html";
   } else {
   if ($uploadname eq "WeeklyCalendar") {
      $uploadname = "weeklycalendar.html";
   } else {
   if ($uploadname eq "MonthlyCalendar") {
      $uploadname = "monthlycalendar.html";
   } else {
   if ($uploadname eq "Memo") {
      $uploadname = "memo.html";
   } else {
   if ($uploadname eq "EditMemo") {
      $uploadname = "editmemo.html";
   } else {
   if ($uploadname eq "DiaryPad") {
      $uploadname = "notes.html";
   } else {
   if ($uploadname eq "EditDiaryPad") {
      $uploadname = "editnotes.html";
   } else { 
   if ($uploadname eq "ContactManager") {
      $uploadname = "personaldir.html";
   } else {
   if ($uploadname eq "Admin") {
      $uploadname = "jiveitadmin.html";
   } else {
   if ($uploadname eq "AddContact") {
      $uploadname = "addpersonalcontact.html";
   } else {
   if ($uploadname eq "EditContact") {
      $uploadname = "showpersonal.html";
   } else {
   if ($uploadname eq "PrintContacts") {
      $uploadname = "printcontacts.html";
   } else {
   if ($uploadname eq "SendFaxToContact") {
      $uploadname = "showpersonalfax.html";
   } else {
   if ($uploadname eq "Help") {
      $uploadname = "jhelp.html";
   } else {
   if ($uploadname eq "Features") {
      $uploadname = "jfeatures.html";
   } else {
   if ($uploadname eq "WhatsNew") {
      $uploadname = "jwhatsnew.html";
   } else {
   if ($uploadname eq "ManagersCalendar") {
      $uploadname = "othercalendar.html";
   } else {
   if ($uploadname eq "CalendarReport") {
      $uploadname = "hddisplayreportcal.html";
   } else {
   if ($uploadname eq "Register") {
      $uploadname = "jiveitregister.html";
   } else {
   if ($uploadname eq "JiveItAccount") {
      $uploadname = "jiveitaccount.html";
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }
   }

   $outr = qx{file $uploadname};
   open thandle, ">$dir/$uploadname";
   printf thandle "%s", $contents;
   close thandle;

   status ("$jp: Your specified file has been successfully uploaded. <BR> Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitdisplay.cgi?p1=jp&p2=file&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=3&le3=HDLIC&HDLIC=$HDLIC&file=file&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to manage JiveIt! account.");


   tied(%permittab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();


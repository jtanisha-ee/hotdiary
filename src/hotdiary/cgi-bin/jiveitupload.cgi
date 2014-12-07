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
# Purpose: jiveitupload program for custom files upload 
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
   hddebug("uploadfiles.cgi");


   $jp = $input{login};
   $login = $jp;
   $password = $input{password};

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


   $uploadname = trim $input{'uploadname'};
   $contents = $input{'uploadfile'};
   $len = length $contents;
   hddebug "len = $len, uploadname = $uploadname";
   $os = $input{os};
   $vdomain = $input{vdomain};
   $rh = $input{rh};
   $hs = $input{hs};


   $msg = adjusturl "Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitfile.cgi?p1=login&p2=password&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=3&password=$password&le3=HDLIC&HDLIC=$HDLIC&login=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to upload files.";

   $msg1 = adjusturl "Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitdisplay.cgi?p1=jp&p2=file&p3=password&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&file=file&password=$password&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to manage JiveIt! account.";
   
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

   $twarning = "false";
   $luploadname = $uploadname;

   #if ($jp eq "mjoshi") {
   if ($contents =~ /TEMPLATECODE /) {
      open touthandle, ">$ENV{HDHOME}/tmp/templateout-$jp-$$";
      printf touthandle "%s", $contents;
      close touthandle;
      $coline = qx{grep "TEMPLATECODE " $ENV{HDHOME}/tmp/templateout-$jp-$$};
      qx{rm -f $ENV{HDHOME}/tmp/templateout-$jp-$$};
      $coline =~ s/\\n//g;
      $coline =~ s/\r//g;
      $numtoks = qx{echo "$coline" | wc -l};
      $numtoks =~ s/\n//g;
      $numtoks =~ s/\r//g;
      ($cod, $ttype) = split " ", $coline;
      $luploadname = "\L$uploadname";
      $lcontents = "\L$contents";
      if ( (!($lcontents =~ /templatecode $luploadname/)) && ($numtoks == 2) ) {
         status("Please select the correct template type. You selected in the dropdown options to upload a template of type <b>$uploadname</b> but it's contents indicate that you are actually trying to upload a template of type <b>$ttype</b>. If you examine the source template file on your local system that you are trying to upload, you will observe that your template contains a line that looks like<BR><BR><CENTER>TEMPLATECODE $ttype</CENTER><BR><BR>. If it does, then please select the appropriate template type, or if you believe this is an error, change the line above in your local file to indicate what the right <b>TEMPLATECODE</b> needs to be. For instance, if you really did mean to upload a template of type <b>$uploadname</b>, then the line in your file must look like:<BR><BR><CENTER>TEMPLATECODE $uploadname</CENTER></BR></BR>.Note that this line is case-insensitive, which means that the characters in this line can be either in upper case or lower case, or mixed case. <p>If you are not sure, what TEMPLATECODE you need to use, please refer to our <a href=\"http://www.hotdiary.com/downloadtemplates.html\">portal templates</a> list.<p>Note that you can always remove this line if you are not sure what it means, and this will prevent our software from checking it's contents. However, we are giving this message on purpose, so it will prevent you from overwriting your own templates accidentally. <p>It is possible that you have a word called TEMPLATECODE somewhere in your template but you obviously did not intend to use it to tell us about the TEMPLATECODE of your template. Rather it was used for a different purpose just to serve up the content of your page. If this is the case, please <a href=\"http://www.hotdiary.com/contact_us.html\">contact customer service</a> and we will be happy to help you.<p>Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitdisplay.cgi?p1=jp&p2=file&p3=password&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&password=$password&le3=HDLIC&HDLIC=$HDLIC&file=file&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to continue managing your JiveIt! account."); 
         exit;
      }
   } else {
      $twarning = "true"; 
   }
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
   if ($uploadname eq "MyDowntown") {
      $uploadname = "business.html";
   } else {
   if ($uploadname eq "MyRewards") {
      $uploadname = "reward.html";
   } else {
   if ($uploadname eq "MyProfile") {
      $uploadname = "profile.html";
   } else {
   if ($uploadname eq "MyCalendarSettings") {
      $uploadname = "calpreferences.html";
   } else {
   if ($uploadname eq "PremiumChannel") {
      $uploadname = "commerceportal.html";
   } else {
   if ($uploadname eq "PartyPlanner") {
      $uploadname = "menupartytbl.html";
   } else {
   if ($uploadname eq "ShowPartyPlanner") {
      $uploadname = "showpartyentry.html";
   } else {
   if ($uploadname eq "EditPartyPlanner") {
      $uploadname = "partydir.html";
   } else {
   if ($uploadname eq "SetCalColor") {
      $uploadname = "hdshowbizbg.html";
   } else {
   if ($uploadname eq "CreateGroups") {
      $uploadname = "hdcreateprivatecal.html";
   } else {
   if ($uploadname eq "ManageGroups") {
      $uploadname = "hdmanagegroupcal.html";
   } else {
   if ($uploadname eq "SearchGroups") {
      $uploadname = "hdsearchgroupcal.html";
   } else {
   if ($uploadname eq "EditManageGroups") {
      $uploadname = "hdmanagecal.html";
   } else {
   if ($uploadname eq "EditCreateGroups") {
      $uploadname = "hdeditprivatecal.html";
   } else {
   if ($uploadname eq "SubscribeGroups") {
      $uploadname = "hdsubscribeprivatecal.html";
   } else {
   if ($uploadname eq "DisplayGroups") {
      $uploadname = "hddisplaygroupcal.html";
   } else {
   if ($uploadname eq "MyGroups") {
      $uploadname = "mygroups.html";
   } else {
   if ($uploadname eq "CreateMerged") {
      $uploadname = "hdcreatemergedcal.html";
   } else {
   if ($uploadname eq "SearchMerged") {
      $uploadname = "hdsearchmergedcal.html";
   } else {
   if ($uploadname eq "ManageMerged") {
      $uploadname = "managemergedcal.html";
   } else {
   if ($uploadname eq "DisplayMerged") {
      $uploadname = "hdviewmergedcal.html";
   } else {
   if ($uploadname eq "DisplayManageMerged") {
      $uploadname = "hdmanagemergedcal.html";
   } else {
   if ($uploadname eq "SubscribeMerged") {
      $uploadname = "hddisplaymergedcal.html";
   } else {
   if ($uploadname eq "JiveItRegister") {
      $uploadname = "jiveitregister.html";
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
   if ($uploadname eq "Admin") {
      $uploadname = "jiveitadmin.html";
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
   }
   }
   }

   $outr = qx{file $uploadname};
   open thandle, ">$dir/$uploadname";
   printf thandle "%s", $contents;
   close thandle;

   if ($jp eq "mjoshi") {
   if ($twarning eq "true") {
      $tmsg = "<p>Did you know that you can setup your templates so that you do not accidentally overwrite a destination template of a different type with your source template? If you would like to take advantage of this funtionality please add the code word<br><br><CENTER>TEMPLATECODE $luploadname</CENTER><br><br> to your template <b>within an HTML comment block</b>. For examples of how we do this, you can always check out <a href=\"http://www.hotdiary.com/downloadtemplates.html\">our templates</a> and check for the code word TEMPLATECODE in the beginning of the file. Do not forget to add the HTML comment block.";
   }
   }

   hddebug "uploadname = $uploadname";
   status ("$jp: Your specified file has been successfully uploaded as $uploadname in your (or $jp 's) JiveIt! portal template configuration directory. $tmsg <BR> Click <a href=\"http://www.hotdiary.com/cgi-bin/execjiveitdisplay.cgi?p1=jp&p2=file&p3=password&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&password=$password&le3=HDLIC&HDLIC=$HDLIC&file=file&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">here</a> to continue managing your JiveIt! account.");


   #tied(%permittab)->sync();
   #tied(%sesstab)->sync();
   #tied(%logsess)->sync();


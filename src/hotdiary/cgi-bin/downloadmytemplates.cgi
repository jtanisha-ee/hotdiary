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
# FileName: templatedownload.cgi
# Purpose: templatedownload program for custom files download 
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
   hddebug("downloadmytemplates.cgi");

   $jp = $input{login};
   $login = $jp;

   hddebug "jp = $jp";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

 
   $alpha = substr $jp, 0, 1;
   $alpha = $alpha . '-index';
   system "mkdir -p $ENV{HDREP}/$alpha/$jp/templates";
   system "chown nobody:nobody $ENV{HDREP}/$alpha/$jp/templates";
   system "chmod 755 $ENV{HDREP}/$alpha/$jp/templates";

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/topcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/topcal.html  $ENV{HDREP}/$alpha/$jp/templates/portaltemplate.txt";
      $apphome = adjusturl "<a href=\"/rep/$alpha/$jp/templates/portaltemplate.txt\">Application Home</a>";
   } else {
      $apphome = "Application Home <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/jiveit.html") {
       system "cp $ENV{HDDATA}/$alpha/$jp/templates/jiveit.html  $ENV{HDREP}/$alpha/$jp/templates/jiveit.txt";
      $jiveit = adjusturl "<a href=\"/rep/$alpha/$jp/templates/jiveit.txt\">JiveIt Home</a>";
   } else {
      $jiveit = "JiveIt Home <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/dailycalendar.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/dailycalendar.html  $ENV{HDREP}/$alpha/$jp/templates/dailycalendar.txt";
      $dailycalendar = adjusturl "<a href=\"/rep/$alpha/$jp/templates/dailycalendar.txt\">Daily Calendar</a>";
   } else {
      $dailycalendar = "Daily Calendar <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/weeklycalendar.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/weeklycalendar.html  $ENV{HDREP}/$alpha/$jp/templates/weeklycalendar.txt";
      $weeklycalendar = adjusturl "<a href=\"/rep/$alpha/$jp/templates/weeklycalendar.txt\">Weekly Calendar</a>";
   } else {
      $weeklycalendar = "Weekly Calendar <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/monthlycalendar.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/monthlycalendar.html  $ENV{HDREP}/$alpha/$jp/templates/monthlycalendar.txt";
      $monthlycalendar = adjusturl "<a href=\"/rep/$alpha/$jp/templates/monthlycalendar.txt\">Monthly Calendar</a>";
   } else {
      $monthlycalendar = "Monthly Calendar <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/memo.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/memo.html  $ENV{HDREP}/$alpha/$jp/templates/memo.txt";
      $memo = adjusturl "<a href=\"/rep/$alpha/$jp/templates/memo.txt\">Memo Manager</a>";
   } else {
      $memo = "Memo <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/editmemo.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/editmemo.html  $ENV{HDREP}/$alpha/$jp/templates/editmemo.txt";
      $editmemo = adjusturl "<a href=\"/rep/$alpha/$jp/templates/editmemo.txt\">Edit Memo</a>";
   } else {
      $editmemo = "Edit Memo <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/notes.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/notes.html  $ENV{HDREP}/$alpha/$jp/templates/diarypad.txt";
      $diarypad = adjusturl "<a href=\"/rep/$alpha/$jp/templates/diarypad.txt\">Edit Diary Pad</a>";
   } else {
      $diarypad = "Diary Pad <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/editnotes.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/editnotes.html  $ENV{HDREP}/$alpha/$jp/templates/editdiarypad.txt";
      $editdiarypad = adjusturl "<a href=\"/rep/$alpha/$jp/templates/editdiarypad.txt\">Edit Diary Pad</a>";
   } else {
      $editdiarypad = "Edit Diary Pad <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/personaldir.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/personaldir.html  $ENV{HDREP}/$alpha/$jp/templates/contactmanager.txt";
      $contactmanager = adjusturl "<a href=\"/rep/$alpha/$jp/templates/contactmanager.txt\">Contact Manager</a>";
   } else {
      $contactmanager = "Contact Manager <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/addpersonalcontact.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/addpersonalcontact.html  $ENV{HDREP}/$alpha/$jp/templates/addcontact.txt";
      $addcontact = adjusturl "<a href=\"/rep/$alpha/$jp/templates/addcontact.txt\">Add A Contact</a>";
   } else {
      $addcontact = "Add A Contact <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/editcontact.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/showpersonal.html  $ENV{HDREP}/$alpha/$jp/templates/editcontact.txt";
      $editcontact = adjusturl "<a href=\"/rep/$alpha/$jp/templates/editcontact.txt\">Edit A Contact</a>";
   } else {
      $editcontact = "Edit A Contact <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/printcontacts.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/printcontacts.html  $ENV{HDREP}/$alpha/$jp/templates/printcontacts.txt";
      $printcontacts = adjusturl "<a href=\"/rep/$alpha/$jp/templates/printcontacts.txt\">Print All Contacts</a>";
   } else {
      $printcontacts = "Print All Contacts <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/showpersonalfax.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/showpersonalfax.html  $ENV{HDREP}/$alpha/$jp/templates/sendcontactfax.txt";
      $sendcontactfax = adjusturl "<a href=\"/rep/$alpha/$jp/templates/sendcontactfax.txt\">Send Fax To Contacts</a>";
   } else {
      $sendcontactfax = "Send Fax To Contacts <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/business.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/business.html  $ENV{HDREP}/$alpha/$jp/templates/mydowntown.txt";
      $mydowntown = adjusturl "<a href=\"/rep/$alpha/$jp/templates/mydowntown.txt\">My Downtown</a>";
   } else {
      $mydowntown = "My Downtown <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/reward.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/reward.html  $ENV{HDREP}/$alpha/$jp/templates/reward.txt";
      $myrewards = adjusturl "<a href=\"/rep/$alpha/$jp/templates/reward.txt\">My Rewards</a>";
   } else {
      $myrewards = "My Rewards <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/profile.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/profile.html  $ENV{HDREP}/$alpha/$jp/templates/profile.txt";
      $myprofile = adjusturl "<a href=\"/rep/$alpha/$jp/templates/profile.txt\">My Profile</a>";
   } else {
      $myprofile = "My Profile <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/calpreferences.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/calpreferences.html  $ENV{HDREP}/$alpha/$jp/templates/calpreferences.txt";
      $mycalsettings = adjusturl "<a href=\"/rep/$alpha/$jp/templates/calpreferences.txt\">My Calendar Settings</a>";
   } else {
      $mycalsettings = "My Calendar Settings <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/commerceportal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/commerceportal.html  $ENV{HDREP}/$alpha/$jp/templates/premiumchannel.txt";
      $premiumchannel = adjusturl "<a href=\"/rep/$alpha/$jp/templates/premiumchannel.txt\">Premium Channel</a>";
   } else {
      $premiumchannel = "Premium Channel <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/menupartytbl.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/menupartytbl.html  $ENV{HDREP}/$alpha/$jp/templates/partyplanner.txt";
      $partyplanner = adjusturl "<a href=\"/rep/$alpha/$jp/templates/partyplanner.txt\">Party Planner</a>";
   } else {
      $partyplanner = "Party Planner <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/showpartyentry.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/showpartyentry.html  $ENV{HDREP}/$alpha/$jp/templates/showpartyentry.txt";
      $showpartyplanner = adjusturl "<a href=\"/rep/$alpha/$jp/templates/showpartyentry.txt\">Show Party Planner</a>";
   } else {
      $showpartyplanner = "Show Party Planner <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/partydir.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/partydir.html  $ENV{HDREP}/$alpha/$jp/templates/partydir.txt";
      $editpartyplanner = adjusturl "<a href=\"/rep/$alpha/$jp/templates/partydir.txt\">Edit Party Planner</a>";
   } else {
      $editpartyplanner = "Edit Party Planner <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdshowbizbg.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdshowbizbg.html  $ENV{HDREP}/$alpha/$jp/templates/setcalcolor.txt";
      $pcalcolor = adjusturl "<a href=\"/rep/$alpha/$jp/templates/setcalcolor.txt\">Set Calendar Color</a>";
   } else {
      $pcalcolor = "Set Calendar Color <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdcreateprivatecal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdcreateprivatecal.html  $ENV{HDREP}/$alpha/$jp/templates/creategroups.txt";
      $creategroup = adjusturl "<a href=\"/rep/$alpha/$jp/templates/creategroups.txt\">Create Groups</a>";
   } else {
      $creategroup = "Create Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdmanagegroupcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdmanagegroupcal.html  $ENV{HDREP}/$alpha/$jp/templates/managegroups.txt";
      $managegroup = adjusturl "<a href=\"/rep/$alpha/$jp/templates/managegroups.txt\">Manage Groups</a>";
   } else {
      $managegroup = "Manage Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdsearchgroupcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdsearchgroupcal.html  $ENV{HDREP}/$alpha/$jp/templates/searchgroups.txt";
      $searchgroup = adjusturl "<a href=\"/rep/$alpha/$jp/templates/searchgroups.txt\">Search Groups</a>";
   } else {
      $searchgroup = "Search Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdmanagecal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdmanagecal.html  $ENV{HDREP}/$alpha/$jp/templates/editmanagegroups.txt";
      $editmanagegroups = adjusturl "<a href=\"/rep/$alpha/$jp/templates/editmanagegroups.txt\">Edit Manage Groups</a>";
   } else {
      $editmanagegroups = "Edit Manage Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdeditprivatecal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdeditprivatecal.html  $ENV{HDREP}/$alpha/$jp/templates/editcreategroups.txt";
      $editcreategroups = adjusturl "<a href=\"/rep/$alpha/$jp/templates/editcreategroups.txt\">Edit Created Groups</a>";
   } else {
      $editcreategroups = "Edit Created Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdsubscribeprivatecal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdsubscribeprivatecal.html  $ENV{HDREP}/$alpha/$jp/templates/subscribegroups.txt";
      $subscribegroups = adjusturl "<a href=\"/rep/$alpha/$jp/templates/subscribegroups.txt\">Subscribe Groups</a>";
   } else {
      $subscribegroups = "Subscribe Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hddisplaygroupcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hddisplaygroupcal.html  $ENV{HDREP}/$alpha/$jp/templates/displaygroups.txt";
      $displaygroups = adjusturl "<a href=\"/rep/$alpha/$jp/templates/displaygroups.txt\">Display Groups</a>";
   } else {
      $displaygroups = "Display Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/mygroups.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/mygroups.html  $ENV{HDREP}/$alpha/$jp/templates/mygroups.txt";
      $mygroups = adjusturl "<a href=\"/rep/$alpha/$jp/templates/mygroups.txt\">My Groups</a>";
   } else {
      $mygroups = "My Groups <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdcreatemergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdcreatemergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/createmerged.txt";
      $createmerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/createmerged.txt\">Create Merged</a>";
   } else {
      $createmerged = "Create Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdsearchmergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdsearchmergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/searchmerged.txt";
      $searchmerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/searchmerged.txt\">Search Merged</a>";
   } else {
      $searchmerged = "Search Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/managemergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/managemergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/managemerged.txt";
      $managemerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/managemerged.txt\">Manage Merged</a>";
   } else {
      $managemerged = "Manage Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdviewmergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdviewmergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/displaymerged.txt";
      $displaymerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/displaymerged.txt\">Display Merged</a>";
   } else {
      $displaymerged = "Display Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hdmanagemergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hdmanagemergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/displaymgmerged.txt";
      $displaymgmerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/displaymgmerged.txt\">Display Manage Merged</a>";
   } else {
      $displaymgmerged = "Display Manage Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/hddisplaymergedcal.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/hddisplaymergedcal.html  $ENV{HDREP}/$alpha/$jp/templates/subscribemerged.txt";
      $subscribemerged = adjusturl "<a href=\"/rep/$alpha/$jp/templates/subscribemerged.txt\">Subscribe Merged</a>";
   } else {
      $subscribemerged = "Subscribe Merged <BR> No User Template";
   }

   if (-e "$ENV{HDDATA}/$alpha/$jp/templates/jiveitregister.html") {
      system "cp $ENV{HDDATA}/$alpha/$jp/templates/jiveitregister.html  $ENV{HDREP}/$alpha/$jp/templates/jiveitregister.txt";
      $register = adjusturl "<a href=\"/rep/$alpha/$jp/templates/jiveitregister.txt\">JiveItRegister</a>";
   } else {
      $register = "Register <BR> No User Template";
   }


      # bind jivetab table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
             'topleft', 'topright', 'middleright', 'bottomleft',
              'bottomright'] };

   $url=$jivetab{$login}{'url'};
   $url= adjusturl($url);
   $logo= adjusturl "$jivetab{$login}{'logo'}";
   $title= adjusturl "$jivetab{$login}{'title'}";
  

   $prml = "";
   $prml= strapp $prml, "logo=$logo";
   $prml= strapp $prml, "sendcontactfax=$sendcontactfax";
   $prml= strapp $prml, "printcontacts=$printcontacts";
   $prml= strapp $prml, "editcontact=$editcontact";
   $prml= strapp $prml, "addcontact=$addcontact";
   $prml= strapp $prml, "contactmanager=$contactmanager";
   $prml= strapp $prml, "editdiarypad=$editdiarypad";
   $prml= strapp $prml, "diarypad=$diarypad";
   $prml= strapp $prml, "editmemo=$editmemo";
   $prml= strapp $prml, "memo=$memo";
   $prml= strapp $prml, "dailycalendar=$dailycalendar";
   $prml= strapp $prml, "weeklycalendar=$weeklycalendar";
   $prml= strapp $prml, "monthlycalendar=$monthlycalendar";
   $prml= strapp $prml, "apphome=$apphome";
   $prml= strapp $prml, "jiveit=$jiveit";
   $prml= strapp $prml, "mydowntown=$mydowntown";
   $prml= strapp $prml, "premiumchannel=$premiumchannel";
   $prml= strapp $prml, "mycalsettings=$mycalsettings";
   $prml= strapp $prml, "myrewards=$myrewards";
   $prml= strapp $prml, "myprofile=$myprofile";
   $prml= strapp $prml, "partyplanner=$partyplanner";
   $prml= strapp $prml, "editpartyplanner=$editpartyplanner";
   $prml= strapp $prml, "showpartyplanner=$showpartyplanner";
   $prml= strapp $prml, "pcalcolor=$pcalcolor";
   $prml= strapp $prml, "creategroup=$creategroup";
   $prml= strapp $prml, "searchgroup=$searchgroup";
   $prml= strapp $prml, "managegroup=$managegroup";
   $prml= strapp $prml, "editmanagegroups=$editmanagegroups";
   $prml= strapp $prml, "editcreategroups=$editcreategroups";
   $prml= strapp $prml, "subscribegroups=$subscribegroups";
   $prml= strapp $prml, "displaygroups=$displaygroups";
   $prml= strapp $prml, "mygroups=$mygroups";
   $prml= strapp $prml, "createmerged=$createmerged";
   $prml= strapp $prml, "managemerged=$managemerged";
   $prml= strapp $prml, "searchmerged=$searchmerged";
   $prml= strapp $prml, "displaymerged=$displaymerged";
   $prml= strapp $prml, "displaymgmerged=$displaymgmerged";
   $prml= strapp $prml, "subscribemerged=$subscribemerged";
   $prml= strapp $prml, "register=$register";

   $prml= strapp $prml, "hiddenvars=$hiddenvars";
   $prml= strapp $prml, "title=$title";
   $prml= strapp $prml, "label=$title";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/downloadmytemplates.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha/$jp/templates/downloadmytemplates-$$.html";
   parseIt $prml;
 
   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDREP}/$alpha/$jp/templates/downloadmytemplates.html";
   hdsystemcat "$ENV{HDREP}/$alpha/$jp/templates/downloadmytemplates-$$.html";
  




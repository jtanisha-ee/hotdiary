#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: groupaddsearch.cgi
# Purpose: it adds and searches the groups.                  
# Creation Date: 03-09-99 
# Created by: Smitha Gudur & Manoj Joshi
# 


#!/usr/local/bin/perl5

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("groupaddsearch.cgi example");    

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'add.x'} ne "") {
      $action = "Add"; 
   } else {
   if ($input{'search.x'} ne "") { 
      $action = "Search";
   }}
 

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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

   # check if session record exists. 
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      #return;
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

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       ##return;
       #exit;
   #}
        
  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired. Click <a href=\"index.html\" target=\"_parent\"> here</a> to login again.");
    #return;
    exit;
   }

  $alpha = substr $login, 0, 1;
  $alpha = $alpha . '-index';


  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";
  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                 'listed' ] };

# bind personal group table vars
   tie %pgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that 
# the groupname is unique amoung all Listed as well as personal groups
   tie %plgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

# bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   $entryno = getkeys();

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

   if (notLogin($input{'groupname'})) {
      status("$login: Invalid characters in Group Name(s) ($input{groupname}). Hint: Make sure there are no spaces in group name. It should be a single word. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
      exit;
   }
   $groupname = trim $input{'groupname'};
##### CASE BEGIN
   $groupname = "\L$groupname";
##### CASE END

   if (notDesc($input{'grouptitle'})) {
      status("$login: Invalid characters in Group Title.  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   if (notDesc($input{'groupdesc'})) {
      status("$login: Invalid characters in Group Description.  Click <a href=\"validation.html\"> here</a> for valid input.\n");
      exit;
   }

   $grouptype = trim $input{'grouptype'};
   $groupfounder = $login;
   $groupdesc = trim $input{'groupdesc'};
   $grouptitle = trim $input{'grouptitle'};
   hddebug "groupname = $groupname";
   hddebug "action = $action";

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }

#  add a new group, 
   if ($action eq "Add") { 
      if ($groupname eq "NoGroup") {
         status("$login: The group $groupname is a reserved group name. It cannot be added to $p2. Please choose another name.");
         exit;
      }
      if ($groupname eq "") {
         $pgroupname = $input{'pgroups'};
         if (($pgroupname eq "") || ($pgroupname eq "No Group")) {
            status("$login: Please enter a non-empty group name.");
            exit;
         }
         $title = time();
         $prml = "";
         $prml = strapp $prml, "biscuit=$biscuit";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html"; 
	 $prml = strapp $prml, "pagenumber=";
         $prml = strapp $prml, "expiry=";
         $prml = strapp $prml, "pagefield=";

         $urlcgi = buildurl("execmemberadddel.cgi");
         $prml = strapp $prml, "actioncgi=$urlcgi";
         $prml = strapp $prml, "label=Members of Personal Group <i>$pgroupname</i>";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html > $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
       
         $prml = "";
         $prml = strapp $prml, "groupname=$pgroupname"; 
         $prml = strapp $prml, "template=$ENV{HDTMPL}/addmember.html"; 
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/addmember.html";
         $prml = strapp $prml, "login=";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/addmember.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";

         $prml = "";
         # Generate Standard Table Header
         $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html"; 
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblhdr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";

         # bind personal group table vars
         tie %gmembertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/$pgroupname/gmembertab",
           SUFIX => '.rec', 
           SCHEMA => { 
           ORDER => ['login'] };
         (@records) = sort keys %gmembertab;

         if ($#records >= 0) {
            for ($l = 0; $l <= $#records; $l++) {
                if ($logtab{$records[$l]}{'checkid'} ne "CHECKED") {
                   delete $gmembertab{$records[$l]};
                   next;
                }
                $prml = "";
                $prml = strapp $prml, "template=$ENV{HDTMPL}/managegrouptblentry.html"; 
                $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/managegrouptblentry.html";
                $prml = strapp $prml, "checkboxfield=checkbox$l"; 
                $prml = strapp $prml, "groupmemberfield=groupmember$l";
                $prml = strapp $prml, "groupmember=$records[$l]";
                $prml = strapp $prml, "login=$records[$l]";
                parseIt $prml, 1;
                system "/bin/cat $ENV{HDHREP}/$alpha/$login/managegrouptblentry.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
            }
         }
         
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/amembertblftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/amembertblftr.html";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/amembertblftr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
 
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/amembersearchpgftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/amembersearchpgftr.html";
         $prml = strapp $prml, "numentries=$#records";
         parseIt $prml, 1;
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/amembersearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html";
         
         #system "/bin/cat $ENV{HDTMPL}/content.html\n\n"; 
         #system "/bin/cat $ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html"; 
         hdsystemcat "$ENV{HDREP}/$alpha/$login/gamem$title$biscuit.html"; 
         exit;
      }

      if (exists $logtab{$groupname}) {
         status("$login: A member login by the same name ($groupname) already exists. Try using another name, like $groupname$$.<p>Hint: When you send invitations to individuals or groups, the group names should not conflict with member login names. This way you can include the group names and member login names unambiguously in your invitation lists.");
         exit;
      }
# check if the group exists in list of all groups and list of all personal groups
      if (exists $plgrouptab{$groupname}) {
         status("$login: Group name $groupname already exists and is a personal group. Try using another name, like $groupname$$.");
         exit;
      }
      if (exists $lgrouptab{$groupname}) {
         status("$login: Group name $groupname already exists and is a public group. Try using another name, like $groupname$$.");
         exit;
      }
# The grouptype is misleading here when we Add a group. As far as Add is concerned, there are only two 
# types of groups, the public groups (Subscribed, Unsubscribed, Founded) and personal groups (Personal)
      if (($grouptype eq "Subscribed") || ($grouptype eq "Unsubscribed") || ($grouptype eq "Founded")) {
# add the group to the grand group list
         $lgrouptab{$groupname}{'groupname'} = $groupname;
         $lgrouptab{$groupname}{'grouptype'} = $grouptype;
         $lgrouptab{$groupname}{'groupfounder'} = $groupfounder;
         $lgrouptab{$groupname}{'grouptitle'} = $grouptitle;
         $lgrouptab{$groupname}{'groupdesc'} = $groupdesc;
# add the founded group to the user
         $fgrouptab{$groupname}{'groupname'} = $groupname;
         $fgrouptab{$groupname}{'grouptype'} = $grouptype;
         $fgrouptab{$groupname}{'groupfounder'} = $groupfounder;
         $fgrouptab{$groupname}{'grouptitle'} = $grouptitle;
         $fgrouptab{$groupname}{'groupdesc'} = $groupdesc;
         system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$groupname/usertab";
         system "/bin/chmod -R 775 $ENV{HDDATA}/listed/groups/$groupname";
# Add the calendar events file for this group
         system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/listed/groups/$groupname";
         system "/bin/chmod 775 $ENV{HDDATA}/listed/groups/$groupname/calendar_events.txt";
         depositmoney $login;

# bind founded group table vars
         tie %usertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/listed/groups/$groupname/usertab",
           SUFIX => '.rec', 
           SCHEMA => { 
           ORDER => ['login'] };
         $usertab{$login}{'login'} = $login;
      } else {
# add the personal group to the user
         $pgrouptab{$groupname}{'groupname'} = $groupname;
         $pgrouptab{$groupname}{'grouptype'} = $grouptype;
         $pgrouptab{$groupname}{'groupfounder'} = $groupfounder;
         $pgrouptab{$groupname}{'grouptitle'} = $grouptitle;
         $pgrouptab{$groupname}{'groupdesc'} = $groupdesc;
# create member directory for personal groups
         system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/$groupname/gmembertab";
         system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alpha/$login/personal/$groupname";
# add the group to list of personal groups
         $plgrouptab{$groupname}{'groupname'} = $groupname;
         $plgrouptab{$groupname}{'grouptype'} = $grouptype;
         $plgrouptab{$groupname}{'groupfounder'} = $groupfounder;
         $plgrouptab{$groupname}{'grouptitle'} = $grouptitle;
         $plgrouptab{$groupname}{'groupdesc'} = $groupdesc;
      }
      if (($grouptype eq "Founded") || ($grouptype eq "Subscribed") || ($grouptype eq "Unsubscribed")) {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/groups/$groupname";
         system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/groups/$groupname";
         system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/groups/$groupname";
         $msg .= "<p>$p2 has successfully created a group website for $groupname. You can start using the calendar $groupname which supports TelTalk service. Your group calendar website URL is <BR><STRONG>http://www.hotdiary.com/groups/$groupname.</STRONG>";
      }
      if ($grouptype eq "Personal") {
         $msg .= "<p>You have created a personal group. <p>No calendar is created for Personal groups. If you would like to use a private calendar, press the Calendar button, and then press the Secure Calendars link. You can then create a secure private calendar with a password.<p>No other user can see your group on $p2, or subscribe to it. However, you can add the email addresses and/or $p2 member logins of your friends, co-workers, relatives and others to this group. <p>When you search for this group, make sure you select Group Type in the main menu as \"Personal\". If you would like to add members to this group, select the Group Type as Personal and search for it by keyword or first alphabet. When you find a matching entry, select the group using the checkbox, and use the Manage button to add or delete members to this group.<p>Since you are the founder of this group, you are automatically subscribed to this group.";
      }
      $msg .= "<p>To reap the benefits of the group you just created, you can use $p2 Collabrum service to send broadcast messages and invitations to all the members of this group.";
      if (($grouptype eq "Unsubscribed") || ($grouptype eq "Subscribed") ||
          ($grouptype eq "Founded")) {
         $msg .= "<p>You have created a public group. Since you are the founder of this group, you are automatically subscribed to this group.";
         
      }
      $msg = "$login : Group $groupname has been added. <STRONG>To search for $groupname, you must select the Group Type as Founded (or Personal as appropriate) before pressing the Search button.</STRONG>" . $msg; 
      if ($grouptype ne "Personal") {
         $msg .= "<p>We have created a group calendar for $groupname. To access this calendar, press on Calendar button in left frame, and then press Secure Calendars link in your personal calendar. Here you can use Search or Manage features. To edit, simply Search for your calendar, and use the Edit button in the search results page.";
      }
      $msg .= "<p>Did you know that you can use Collabrum to send instant messages to $groupname? You could also send instant messages to multiple groups that you have subcribed to or founded yourself!";
      status($msg);
   }

	   if ($action eq "Search") { 

	      if (($groupname eq "") && ($grouptype eq "Unsubscribed")) {
		 status("$login: Enter a non-empty keyword or group to search when you are searching for all unsubscribed groups.");
		 exit;
	      }

	      system "/bin/rm -f $ENV{HDREP}/$alpha/$login/gser*.html";      
	      $title = time();
	      $found_counter = 0;
	      $page_entries = 0;
	      $page_num = 0;
	      $prevpage = "";
	      $nextpage = "";

	      
	      (@records) = ();
	      if (($grouptype eq "Subscribed") || ($grouptype eq "Unsubscribed")) {
		 (@records) = sort keys %lgrouptab;
	      } else {
		 if ($grouptype eq "Founded") {
		    (@records) = sort keys %fgrouptab;
		 }
		 if ($grouptype eq "Personal") {
		    (@records) = sort keys %pgrouptab;
		 }
	      }
	      for ($i = 0; $i <= $#records; $i++) {
		 $onekey = $records[$i];

		 $nomatch = "true";
                 if (exists $lgrouptab{$onekey}) {
                    if ($lgrouptab{$onekey}{'listed'} eq "on") {
                       next;
                    }
                 }
		 if ($onekey ne "")  {
		    #if (nmmatch $onekey, $groupname) {
		    if ( ((index "\L$groupname", "\L$onekey") != -1) ||
			 ((exists $plgrouptab{$onekey}) && ((index "\L$plgrouptab{$onekey}{'grouptitle'}", "\L$groupname") != -1)) || 
			 ((exists $plgrouptab{$onekey}) && ((index "\L$plgrouptab{$onekey}{'groupdesc'}", "\L$groupname") != -1)) ||
			 ((exists $lgrouptab{$onekey}) && ((index "\L$lgrouptab{$onekey}{'grouptitle'}", "\L$groupname") != -1)) || 
			 ((exists $lgrouptab{$onekey}) && ((index "\L$lgrouptab{$onekey}{'ctype'}", "\L$groupname") != -1)) ||
			 ((exists $lgrouptab{$onekey}) && ((index "\L$lgrouptab{$onekey}{'groupdesc'}", "\L$groupname") != -1) )) {
		       #print "grouptype = $grouptype, groupname = $onekey<BR>";
		       if (($grouptype eq "Subscribed") && (!exists $sgrouptab{$onekey}) && (!exists $fgrouptab{$onekey})) {
			  next;
		       }
		       if (($grouptype eq "Unsubscribed") && ((exists $sgrouptab{$onekey}) || (exists $fgrouptab{$onekey}))) {
			  #print "groupname = $onekey, skipping group<BR>";
			  next;
		       }
		       if (($grouptype eq "Founded") && (!exists $fgrouptab{$onekey})) {
			  next;
		       }
	# if this is a public group it must be in lgrouptab, although it could be in other places too
		       if (($grouptype eq "Subscribed") || ($grouptype eq "Unsubscribed") || ($grouptype eq "Founded")) {
	# kick out secure groups/calendars, we will handle this separately
			  if ($lgrouptab{$onekey}{'password'} ne "") {
			     next;
			  } 
			  $groupfounder = $lgrouptab{$onekey}{'groupfounder'};
			  $grouptitle = $lgrouptab{$onekey}{'grouptitle'};
			  $groupdesc = $lgrouptab{$onekey}{'groupdesc'};
		       } else {
	# if this is a personal group it must be in pgrouptab, although it is also in plgrouptab
			  $groupfounder = $pgrouptab{$onekey}{'groupfounder'};
			  $grouptitle = $pgrouptab{$onekey}{'grouptitle'};
			  $groupdesc = $pgrouptab{$onekey}{'groupdesc'};
		       }
		       $found_counter= $found_counter + 1;
		       $page_entries = $page_entries + 1;
		       if ($page_entries eq 1) {
			  $page_num = $page_num + 1;
		       }
		       if ($page_num eq 1) {
			  $prevpage = "rep/$alpha/$login/gser$title$biscuit$page_num.html";
		       } else {
			  $pageno = $page_num - 1;
			  $prevpage = "rep/$alpha/$login/gser$title$biscuit$pageno.html";
		       }
		       $pageno = $page_num + 1;
		       if ($page_num eq 1) {
			  $nextpage = "rep/$alpha/$login/gser$title$biscuit$pageno.html";
		       } else {
			  $nextpage = "rep/$alpha/$login/gser$title$biscuit$pageno.html";
		       }

		       $prml = "";
		       $prml = strapp $prml, "entrynfield=entryn$page_entries";
		       $prml = strapp $prml, "entryno=$onekey";

		       $prml = strapp $prml, "grouptypefield=grouptype$page_entries";
		       $prml = strapp $prml, "grouptype=$grouptype";

		       $prml = strapp $prml, "checkboxfield=checkbox$page_entries";

		       $prml = strapp $prml, "groupname=$onekey";
		       #$prml = strapp $prml, "groupnamefield=groupname$page_entries";

		       $prml = strapp $prml, "grouptitle=$grouptitle";
		       #$prml = strapp $prml, "grouptitlefield=grouptitle$page_entries";

		       #$prml = strapp $prml, "groupfounder=$groupfounder";
		       #$prml = strapp $prml, "groupfounderfield=groupfounder$page_entries";

		       $prml = strapp $prml, "groupdesc=$groupdesc";
		       #$prml = strapp $prml, "groupdescfield=groupdesc$page_entries";

		       if ($grouptype eq "Personal") {
		       $prml = strapp $prml, "radiovalue=$onekey";
		       
		       $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgrouptblentry.html";
		       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpgrouptblentry.html";
		       } else {

		       $prml = strapp $prml, "template=$ENV{HDTMPL}/searchgrouptblentry.html";
		       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchgrouptblentry.html";
		       }
		       parseIt $prml, 1;
		       $prml = "";

		       if ($page_entries eq 1) {
			 # Generate Search Page Header
                  $prml = "";
                  
                  $prml = strapp $prml, "biscuit=$biscuit";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html"; 
		  $prml = strapp $prml, "pagenumber=Page: $page_num <BR>";
                  $prml = strapp $prml, "expiry=";
                  $prml = strapp $prml, "pagefield=page$dbentryno";

                  if ($grouptype eq "Personal") {
                     $urlcgi = buildurl("execgroupmanagedel.cgi");
                  } else {
                     $urlcgi = buildurl("execgroupjoinleavedel.cgi");
	          }
                  $prml = strapp $prml, "actioncgi=$urlcgi";
		  if ($groupname eq "") {
                    $prml = strapp $prml, "label=Group Search results for all entries";
		  } else {
                    $prml = strapp $prml, "label=Group Search results for \"$groupname\"";
                  }
                  parseIt $prml, 1;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html > $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
                  # Generate Standard Table Header
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html"; 
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
                  parseIt $prml, 1;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblhdr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
               }
               if ($grouptype eq "Personal") {
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpgrouptblentry.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
               } else {
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchgrouptblentry.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
               }

               if ($page_entries eq 10) {
# this is the last time we will use page_entries in this iteration, 
# so we can reset it now to 0
                  # Generate Standard Table Footer
                  $prml = strapp $prml, "numentries=$page_entries";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblftr.html";
                  $prml = strapp $prml, "nextpage=$nextpage";
                  $prml = strapp $prml, "prevpage=$prevpage";
                  parseIt $prml, 1;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";

                  # Generate Search Page Footer
                  if ($grouptype eq "Subscribed") {
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/sgroupsearchpgftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/sgroupsearchpgftr.html";
                  }
                  if ($grouptype eq "Unsubscribed") {
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/ugroupsearchpgftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/ugroupsearchpgftr.html";
                  }
                  if ($grouptype eq "Founded") {
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/fgroupsearchpgftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/fgroupsearchpgftr.html";
                  }
                  if ($grouptype eq "Personal") {
                     $prml = strapp $prml, "template=$ENV{HDTMPL}/pgroupsearchpgftr.html";
                     $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/pgroupsearchpgftr.html";
                  }
                  parseIt $prml, 1;
                  $prml = "";
                  if ($grouptype eq "Subscribed") {
                     system "/bin/cat $ENV{HDHREP}/$alpha/$login/sgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
                  }
                  if ($grouptype eq "Unsubscribed") {
                     system "/bin/cat $ENV{HDHREP}/$alpha/$login/ugroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
                  }
                  if ($grouptype eq "Founded") {
                     system "/bin/cat $ENV{HDHREP}/$alpha/$login/fgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
                  }
                  if ($grouptype eq "Personal") {
                     system "/bin/cat $ENV{HDHREP}/$alpha/$login/pgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
                  }
               }
               if ($page_entries eq 10) {
                  $page_entries = 0;
               }
            } # if nmmatch
         }  #if onekey
      }  #for
 

# deal with cases when the $found_counter are odd numbered
      $rem = $found_counter % 10;
      if ($rem != 0) {
         # Generate Standard Table Footer
         $prml = strapp $prml, "numentries=$page_entries";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblftr.html";
         $prml = strapp $prml, "nextpage=$nextpage";
         $prml = strapp $prml, "prevpage=$prevpage";
         parseIt $prml, 1;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";

         # Generate Search Page Footer
         if ($grouptype eq "Subscribed") {
            $prml = strapp $prml, "template=$ENV{HDTMPL}/sgroupsearchpgftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/sgroupsearchpgftr.html";
         }
         if ($grouptype eq "Unsubscribed") {
            $prml = strapp $prml, "template=$ENV{HDTMPL}/ugroupsearchpgftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/ugroupsearchpgftr.html";
         }
         if ($grouptype eq "Founded") { 
            $prml = strapp $prml, "template=$ENV{HDTMPL}/fgroupsearchpgftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/fgroupsearchpgftr.html";
         }
         if ($grouptype eq "Personal") {
            $prml = strapp $prml, "template=$ENV{HDTMPL}/pgroupsearchpgftr.html";
            $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/pgroupsearchpgftr.html";
         }
         parseIt $prml, 1;
         $prml = "";
         if ($grouptype eq "Subscribed") {
           system "/bin/cat $ENV{HDHREP}/$alpha/$login/sgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
         }
         if ($grouptype eq "Unsubscribed") {
           system "/bin/cat $ENV{HDHREP}/$alpha/$login/ugroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
         }
         if ($grouptype eq "Founded") {
            system "/bin/cat $ENV{HDHREP}/$alpha/$login/fgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
         }
         if ($grouptype eq "Personal") {
            system "/bin/cat $ENV{HDHREP}/$alpha/$login/pgroupsearchpgftr.html >> $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html";
         }
      }


# overwrite nextpage with lastpage
      $prml = strapp $prml, "expiry=";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/lastpage.html";
      $prml = strapp $prml, "prevpage=rep/$alpha/$login/gser$title$biscuit$page_num.html";
      $pageno = $page_num + 1; 
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha/$login/gser$title$biscuit$pageno.html";
      parseIt $prml, 1;
      $prml = "";
      system "cp $ENV{HDREP}/$alpha/$login/$biscuit.html $ENV{HDREP}/$alpha/$login/gser$title$biscuit$pageno.html";


      if ($found_counter eq 0) {
          if ($groupname eq "") {
		     status("$login: There are no $grouptype groups present that are applicable to you. <FONT COLOR=\"00ff00\"><p>Make sure you select the correct group type search option category before pressing the Search button.</FONT><p><FONT COLOR=\"0000ff\">Are you searching for a Personal group? If so, then you need to select the Group Type as Personal before pressing the Search button.</FONT><p><FONT COLOR=\"1299ff\">Are you searching for a group that someone created and you have not yet subscribed to? If so, then you need to select the Group Type as Unsubscribed before pressing the Search button.</FONT>");
          } else {
            if ((exists $lgrouptab{$groupname}) || (exists $plgrouptab{$groupname})) {
               if ($grouptype eq "Personal") {
                  $grpstr = "not a Personal group. <p><FONT COLOR=\"0000ff\">Please select the appropriate Group Type before pressing the search button.</FONT>";
               } else {
                  if ($grouptype eq "Founded") {
                     $grpstr = "not Founded by you. <p><FONT COLOR=\"0000ff\">Please select the appropriate Group Type before pressing the search button.</FONT>";
                  } else {
                      if ($grouptype eq "Subscribed") {
                         $grpstr = "not Subscribed by you. <p><FONT COLOR=\"0000ff\">Please select the appropriate Group Type before pressing the search button.</FONT>";
                      } else {
                          if ($grouptype eq "Unsubscribed") {
                             $grpstr = "either a public group that you have Founded or Subscribed or a Personal Group. <p><FONT COLOR=\"0000ff\">To search for your group, you must select the appropriate Group Type as either Founded, Subscribed or Personal and then press the Search button.</FONT>";
                          }
                      }
                  }
               }
               status("$login: Searched for $grouptype groups only. The group $groupname does exist, however it is $grpstr");
            } else {
               status("$login: Searched for $grouptype groups only. The group $groupname is available! You can create it now, by using the Add button and invite your friends to join the group.");
            }
          }
      } else {
            #system "/bin/cat $ENV{HDTMPL}/content.html\n\n"; 
            $page_num = "1";
            #system "/bin/cat $ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html"; 
            hdsystemcat "$ENV{HDREP}/$alpha/$login/gser$title$biscuit$page_num.html"; 
      }
   } #if

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   if ((($grouptype eq "Subscribed") || ($grouptype eq "Unsubscribed") || ($grouptype eq "Founded")) 
        && ($action eq "Add")) {
      tied(%lgrouptab)->sync();
      tied(%fgrouptab)->sync();
      tied(%usertab)->sync();
   } else {
      if (($grouptype eq "Personal") && ($action eq "Add")) {
         tied(%pgrouptab)->sync();
         tied(%plgrouptab)->sync();
      }
   }

   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

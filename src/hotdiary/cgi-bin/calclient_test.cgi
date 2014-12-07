#!/usr/bin/perl

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
# FileName: calclient.cgi
# Purpose: New HotDiary Calendar Client
# Creation Date: 06-14-99 
# Created by: Smitha Gudur
# 

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");    

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;
   #$sc = $input{$sc};
   if ($biscuit eq "") {
      $sc = "p";
   }
   $hs = $input{'hs'};
   $vdomain = trim $input{'vdomain'};
   $jp = trim $input{'jp'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $vdomain = "\L$vdomain";
   if ($jp ne "") {
      hddebug "JiveIt! Customer from $ENV{HTTP_REFERER}";
   }

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }


   $hs = $input{'hs'};
   #$rhost = qx{nslookup $ENV{'REMOTE_HOST'} | grep Name | awk '{print \$2}'};
   #$rhost =~ s/\n//g;
   $rhost = $ENV{'REMOTE_HOST'};
   hddebug "calclient.cgi: Invoked from $rhost";

   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['HDLIC', 'partner', 'IP'] };

   tie %parttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/parttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['logo', 'title', 'banner'] };


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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };

   # check if session record exists. 
   if ($sc ne "p") {
           if (!exists $sesstab{$biscuit}) {
             hddebug "biscuit = $biscuit";
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
              $login = $sesstab{$biscuit}{'login'};
              if ($login eq "") {
                 error("Login is an empty string. Possibly invalid session.\n");
                 exit;
              }
          }
   } else {
        $login = $input{'l'};
   }

  if (($biscuit ne "") && ($sc ne "p"))  {
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
   } 

   $g = $input{g};
   if (($login eq "") && ($g eq "")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode.");
      exit;
   }

   if ($g eq "NoGroup") {
      status("You have not subscribed to any groups so far. Press the Groups button to search specific groups by name, and use the Join feature to subscribe to your groups of interest. You can then use the <IMG SRC=\"/images/new2a.gif\" WIDTH=\"60\" HEIGHT=\"40\" BORDER=\"0\"> group Calendar service, by pressing the MemoCal button once again, selecting an appropriate group in the new Calendar section, and then pressing the Calendar button.");
      exit;
   }

   if (($sc eq "p") && ($g eq "") && ($logtab{$login}{'calpublish'} ne "CHECKED")) {
      status("$login has currently not published his/her calendar on HotDiary.");
      exit;
   }

   $a = $input{a};

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'readonly' ] };

   hddebug "Edit Decision: a = $a, sc = $sc, g = $g";
   if (($sc ne "p") && ($g ne "")) {
      if (exists $lgrouptab{$g}) {
         hddebug "founder = $lgrouptab{$g}{'groupfounder'}, login = $login";
         if ("\L$lgrouptab{$g}{'groupfounder'}" ne "\L$login") {
            hddebug "readonly = $lgrouptab{$g}{'readonly'}";
            if ($lgrouptab{$g}{'readonly'} eq "on") {
               if (($a eq "e") || ($a eq "a") || ($a eq "r")) {
                  status("You do not have permission to edit this calendar."); 
                  exit;
               }
            }
         }
      }
   }

# bind personal group table vars
   #if ($login ne "") {
   #   tie %pgrouptab, 'AsciiDB::TagFile',
   #   DIRECTORY => "$ENV{HDDATA}/groups/$login/personal/pgrouptab",
   #   SUFIX => '.rec', 
   #   SCHEMA => { 
   #        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
   #}

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that 
# the groupname is unique amoung all Listed as well as personal groups
   #tie %plgrouptab, 'AsciiDB::TagFile',
   #DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   #SUFIX => '.rec', 
   #SCHEMA => { 
   #     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

# bind subscribed group table vars
   #if ($login ne "") {
   #   tie %sgrouptab, 'AsciiDB::TagFile',
   #   DIRECTORY => "$ENV{HDDATA}/groups/$login/subscribed/sgrouptab",
   #   SUFIX => '.rec', 
   #   SCHEMA => { 
   #        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
   #}

# bind founded group table vars
   #if ($login ne "") {
      #tie %fgrouptab, 'AsciiDB::TagFile',
      #DIRECTORY => "$ENV{HDDATA}/groups/$login/founded/fgrouptab",
      #SUFIX => '.rec', 
      #SCHEMA => { 
      #     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
   #}

   $rand = getkeys();
   $dy = $input{dy};
   $mo = $input{mo};
   $yr = $input{yr};
   $vw = $input{vw};
   $f = $input{f};
   $h = $input{h};
   $m = $input{m};
   $en = $input{en};
   $jvw = $input{jvw};
   $rh = $input{rh};
   $ip = $input{HDLIC};
   $jp = $input{jp};
   hddebug  "ip = $ip";
   hddebug  "remoteaddr = $input{'ip'}";
   if ($rh ne "") {
      hddebug "enter rh = $rh";
      if (exists $jivetab{$jp}) {
            $logo = adjusturl $jivetab{$jp}{logo};
            hddebug "logo = $logo";
            $title = $jivetab{$jp}{title};
            hddebug "title = $title";
            $banner = adjusturl $jivetab{$jp}{banner};
            hddebug "banner = $banner";
      } else {

          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             hddebug "partner = $partner";
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                hddebug "logo = $logo";
                $title = $parttab{$partner}{title};
                hddebug "title = $title";
                $banner = adjusturl $parttab{$partner}{banner};
                hddebug "banner = $banner";
             }
          }
      }
   }

   #hddebug "rh = $rh";
   if ($tz eq "") {
      $tz = $logtab{$login}{'zone'};
      #$tz = "-8";
   }

   if (($a eq "r") && ($sc eq "p")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode.");
      exit;
   }
   
   #if (($vw eq "i") && ($sc eq "p")) {
   #   status("You do not have permission to perform this operation. You are viewing a published Calendar."); 
   #   exit;
   #}

   if (($vw eq "n") && ($sc eq "p")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode.");
      exit;
   }

   if ($f eq "j") {
      if (($login ne "mjoshi") && ($login ne "smitha")) {
         status("This service will be introduced shortly. If you need to create Memos, please click on the Home link and use the MemoCal button in the left frame.");
         exit;
      }
   }

   if ($f eq "h") {
      if ($sc eq "p") {
         status("You are currently not logged in. You only have view access to a published calendar.");
         exit;
      }
      #if ($g ne "") {
         #status("For group calendars you do not need to use this link. You can use the buttons in the left frame to navigate HotDiary.");
         #exit;
      #}
      $pr = "";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/d$biscuit.html";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/diarymenu.html";
      $pr = strapp $pr, "leftFrame=rep/$login/l$biscuit.html";
      $pr = strapp $pr, "rightFrame=rep/$login/$biscuit.html";
      #$label = "HotDiary Address Add/Search Menu.";
      #$label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      #$label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      #$logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      #$pr = strapp $pr, "login=$logi";
      #$pr = strapp $pr, "label=$label";
      #$pr = strapp $pr, "label1=$label1";
      #$pr = strapp $pr, "label2=$label2";
      $pr = strapp $pr, "biscuit=$biscuit";
      parseIt $pr;
      $expiry = localtime(time() + 5);
      $expiry = "\:$expiry";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/leftFrame.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/exechotmenu.cgi";
      #if (($login eq "smitha") || ($login eq "mjoshi")) {
         $calclient = adjusturl "<TR><TD WIDTH=\"100%\"><P><CENTER><a href=\"http://www.hotdiary.com/cgi-bin/execcalclient.cgi?biscuit=$biscuit\" target=_parent><IMAGE SRC=\"images/newcalclient.gif\" border=0></a></CENTER></TD></TR>";
      #} else {
      #   $calclient = "";
      #}
      $pr = strapp $pr, "calclient=$calclient";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$login/l$biscuit.html";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "expiry=$expiry";
      parseIt $pr;
      $pr = "";
      tie %hdtab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/hdtab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['title', 'logo', 'banner' ] };

      if (exists $hdtab{$login}) {
         $t2 = adjusturl $hdtab{$login}{title};
         $banner = adjusturl $hdtab{$login}{banner};
      } else {
         $t2 = "HotDiary";
      }
 
      $label = "$t2 Address Add/Search Menu.";
      $label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      $label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      $logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      $pr = strapp $pr, "login=$logi";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "label1=$label1";
      $pr = strapp $pr, "label2=$label2";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpghdr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/stdpghdr.html";
      $pr = strapp $pr, "expiry=";
      parseIt $pr;

      $pr = "";
      $label = "$t2 Address Add/Search Menu.";
      $label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      $label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      $pr = strapp $pr, "login=$login";
      $pr = strapp $pr, "label1=$label1";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "biscuit=$biscuit";
      $buddy = "rep/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/friend.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/friend.html";
      $buddy = "rep/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      parseIt $pr;
      system "/bin/cat $ENV{HDHREP}/$login/friend.html > $ENV{HDREP}/$login/friend$biscuit.html";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/addrmenutblhdr.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/execaddraddsearch.cgi";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/addrmenutblhdr.html";
      parseIt $pr;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/menuaddrtbl.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/menuaddrtbl.html";
      parseIt $pr;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdmenutblftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/stdmenutblftr.html";   
      parseIt $pr;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpgftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$login/stdpgftr.html";
      parseIt $pr;

      system "/bin/cat $ENV{HDHREP}/$login/stdpghdr.html $ENV{HDHREP}/$login/addrmenutblhdr.html $ENV{HDHREP}/$login/menuaddrtbl.html $ENV{HDHREP}/$login/stdmenutblftr.html $ENV{HDHREP}/$login/stdpgftr.html > $ENV{HDREP}/$login/$biscuit.html";

      system "/bin/cat $ENV{HDHREP}/$login/d$biscuit.html";
      exit;
   }
   system "cat \"$ENV{HDTMPL}/content.html\"";

   # if the function is event, and the action is add
   # When 8:00 (or 9:00, 10:00...) are pressed in daily view
   # in the event mode, a Add Event
   # HTML form is displayed. Enter the information for the event,
   # and press the Add button. When this add button is pressed the
   # following logic is executed.
   if ((($a eq "a") && ($f eq "e")) || (($a eq "e") && ($f eq "e"))) {
      $emonth = trim $input{'month'};
      $eday = trim $input{'day'};
      $eyear = trim $input{'year'};
      $ezone = trim $input{'zone'};
      $ehour = trim $input{'hour'};
      #status("ehour = $ehour");
      $emeridian = trim $input{'meridian'};
      $emin = trim $input{'min'};

      if ($emin eq "0") {
         $emin = '00';
      } 

      $event_hour = $ehour;
      $event_zone = adjustzone($ezone);

      if (($emeridian eq "PM") && ($ehour ne "12")) {
         $event_hour = $ehour + 12;
      }
      if (($emeridian eq "AM") && ($ehour eq "12")) {
         $event_hour = 0;
      }


      $etime = etimetosec("", $emin, $event_hour, $eday, $emonth, $eyear, "", "", "",$event_zone);

      $ctime = ctimetosec();

      $ediff = $etime - $ctime;

      if ($ediff < 1200) {
         #statuss("$login: You can only set reminders which are due in the future, atleast 20 minutes past current time.");
         #exit;
      }

      $erecurtype = trim $input{'recurtype'}; 
      $eatype = trim $input{'atype'}; 
      $econtact = trim $input{'contact'}; 
      $edtype = trim $input{'dtype'}; 
      $etitle = trim $input{'subject'}; 
      $edhour = trim $input{'dhour'};
      $edmin = trim $input{'dmin'};
      $efree = trim $input{'free'};
      $eshare = trim $input{'share'};
      $edesc = $input{'desc'}; 
      #status ("desc = $edesc");

# Accessing hidden fields in form (hdcalviewtop.html)
      $rurl = $input{rurl};
      #status("rurl = $rurl");
      
      #status("ehour = $ehour");
      if ($a eq "a") {
         addEvent $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $g, $econtact;
      }
      if ($a eq "e") {
         $en = $input{'en'}; 
         updateEvent $en, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $g, $econtact;
      }
      system "cat $rurl";
   }

   # for todo 
   if ((($a eq "a") && ($f eq "t")) || (($a eq "e") && ($f eq "t"))) {
      $emonth = trim $input{'month'};
      $eday = trim $input{'day'};
      $eyear = trim $input{'year'};
      $ehour = trim $input{'hour'};
      #status("ehour = $ehour");
      $emeridian = trim $input{'meridian'};
      $etitle = trim $input{'subject'};
      $eshare = trim $input{'share'};
      $edesc = $input{'desc'};
      $epriority = trim $input{'priority'};
      $estatus = trim $input{'status'};
      #status ("desc = $edesc");

# Accessing hidden fields in form (hdcalviewtop.html)
      $rurl = $input{rurl};
      #status("rurl = $rurl");

      if ($a eq "a") {
         addTodo $etitle, $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $login, $g;
      }
      if ($a eq "e") {
         $en = $input{'en'};
         updateTodo $en, $etitle, $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $login, $g;
      }
      system "cat $rurl";

   }

   #if ($login eq "smitha") {
      if ($f eq "r") {
         hddebug "report cal invoking";
         system "echo '#!/bin/ksh' > /var/tmp/reportcal$$-$login";
         $repparms = "biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&g=$g&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip";
         $cgis = "$ENV{HDEXECCGI}/execreportcal.cgi";
         system "echo \"$cgis\" \"$repparms\" >> /var/tmp/reportcal$$-$login";
         #$cgis = "$ENV{HDEXECCGI}/execreportcal.cgi?biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&g=$g&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip";
         # reset the timer.
         if (-f "/var/tmp/reportcal$$-$login") {
    	    system "chmod 777 /var/tmp/reportcal$$-$login";
            $sesstab{$biscuit}{'time'} = time();
            system "\"/var/tmp/reportcal$$-$login\"";
         } else {
	    status("No Events to report.");
         } 
         exit;
      }
   #}


   if (($a ne "a") && ($a ne "e")) {
      if ($g eq "") {
         $repdir = $login;
      } else {
         $repdir = "groups";
      }
      tie %hdtab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/hdtab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['title', 'logo', 'banner' ] };

      if (exists $hdtab{$login}) {
         $title = adjusturl $hdtab{$login}{title};
         $banner = adjusturl $hdtab{$login}{banner};
         $logo = adjusturl $hdtab{$login}{logo};
      }
 
      createCalendar $dy, $mo, $yr, "$ENV{HDHREP}/$repdir/cal$rand$biscuit.html", $login, $biscuit, $vw, $f, $a, $h, $m, $tz, $en, $sc, $jvw, $g, $logtab{$login}{'calpublish'}, "$rh", "$logo", "$title", "$banner", "$vdomain", "$hs", "$jp";
      system "cat \"$ENV{HDHREP}/$repdir/cal$rand$biscuit.html\"";
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

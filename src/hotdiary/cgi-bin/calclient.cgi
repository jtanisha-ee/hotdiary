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
use calfuncs::bizfuncs;
use MIME::Base64;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   #hddebug "calclient.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   hddebug "cookie login = $login";

   $addresses = $input{people};
   $biscuit = $input{'biscuit'};

   #$sc = $input{$sc};

   # bind leditgrouptab table vars
   tie %leditgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/leditgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'jiveit', 'publicedit' ] };

   $g = $input{g};
   
   $jp = trim $input{'jp'};
   if ($jp eq "") {
      if (exists($leditgrouptab{$g})) {
         $jp = $leditgrouptab{$g}{jiveit};
      }
   }
   hddebug "jp = $jp";
   $publicedit = 0;
   if ($biscuit eq "") {
      if ( ($g ne "") && (exists $leditgrouptab{$g}) && ($leditgrouptab{$g}{publicedit} eq "CHECKED") ) {
         $publicedit = 1;      
      } else {
         $sc = "p";
      }
   }
   #hddebug "sc = $sc";
   $hs = $input{'hs'};
   $vdomain = trim $input{'vdomain'};

   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   }
   $vdomain = "\L$vdomain";

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }


   $hs = $input{'hs'};
   #$rhost = qx{nslookup $ENV{'REMOTE_HOST'} | grep Name | awk '{print \$2}'};
   #$rhost =~ s/\n//g;
   $rhost = $ENV{'REMOTE_HOST'};
   if ($ENV{REMOTE_ADDR} eq "63.168.86.93") {
      status "You are denied access.";
      exit;
   }

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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish',
        'referer'] };      

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };

   # check if session record exists. 
   if ($publicedit == 0) {
   if ($sc ne "p") {
           if (!exists $sesstab{$biscuit}) {
             if ($hs eq "") {
	         if ($jp ne "") {
	            if ($jp ne "buddie") {
                       status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
	               exit;
                    }
                 }
                status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
             } else {
                status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
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
   } else {
        $login = $input{'l'};
        if ($jp eq "") {
	   if (exists($logtab{$login})) {
  	     $jp = $logtab{$login}{referer};
	   }
        }
   }
   }

      $alpha = substr $login, 0, 1;
      $alpha = $alpha . '-index';

  if ($publicedit == 0) {
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
   }

   if (($login eq "") && ($g eq "")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode. Please close this browser window and go back to the main browser.");
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


   if ( ($g ne "") && (!exists $lgrouptab{$g}) ) {
      status("The calendar $g is not available. Either it has been deleted or it was never created.");
      exit;
   }

   $pw = $input{pw};
   $pwenc = $pw;
   $pw =~ s/aaaa/=/g;
   $pw = decode_base64 $pw;
   #hddebug "pw = $pw";
   #hddebug "g = $g";
   #hddebug "password = $lgrouptab{$g}{password}";
   if ( ($sc eq "p") && ($g ne "") && ("\L$pw" ne "\L$lgrouptab{$g}{password}") ) {
      $prmm = "";
      $prmm = strapp $prmm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prmm = strapp $prmm, "templateout=$ENV{HDHOME}/tmp/pubgroup-redirect_url-$$.html";
      $prmm = strapp $prmm, "redirecturl=http://$vdomain/$hs/groups/$g";
      parseIt $prmm;
      hdsystemcat "$ENV{HDHOME}/tmp/pubgroup-redirect_url-$$.html";
      exit;
   }

   if (($sc ne "p") && ($g ne "")) {
      if (exists $lgrouptab{$g}) {
         if ("\L$lgrouptab{$g}{'groupfounder'}" ne "\L$login") {
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
   $os = $input{os};
   #if ($rh ne "") {
      if (exists $jivetab{$jp}) {
            $logo = adjusturl $jivetab{$jp}{logo};
            $title = $jivetab{$jp}{title};
            $banner = adjusturl $jivetab{$jp}{banner};
      } else {

          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
             }
          }
      }
   #}
   #hddebug "logo = $logo, jp = $jp";

   if ($banner eq "") {
      $banner = adjusturl "<a href=$hddomain/cgi-bin/adbanner/execshowsite?member=hotdiary&page=27><IMG SRC=$hddomain/cgi-bin/adbanner/execshowbanner?member=hotdiary&page=101 BORDER=0></a>";
      #hddebug "banner = $banner";
   }

   if (($a eq "u") && ($sc ne "p") && ($g ne "")) {
      addGroupEventToMyCal($en, $login, $g);
      #hddebug "addgroupevent en = $en, login = $login, g= $g";
      #status("$login: Group Event has been added to your personal calendar."); 
      $a = "d";
      #exit;
   }

   $tz = $input{zone};
   if ($tz eq "") {
      if (exists $logtab{$login}) {
         $tz = $logtab{$login}{'zone'};
      } else {
        $tz = "-8";
      }
   }

   if (($a eq "r") && ($sc eq "p")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode. Please close this browser window and go back to the main browser.");
      exit;
   }
   
   #if (($vw eq "i") && ($sc eq "p")) {
   #   status("You do not have permission to perform this operation. You are viewing a published Calendar."); 
   #   exit;
   #}

   if (($vw eq "n") && ($sc eq "p")) {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode. Please close this browser window and go back to the main browser.");
      exit;
   }

   #if ($f eq "j") {
      #if (($login ne "mjoshi") && ($login ne "smitha")) {
         #status("This service will be introduced shortly. If you need to create Memos, please click on the Home link and use the MemoCal button in the left frame.");
         #exit;
      #}
   #}

   if ($f eq "h") {
      if ($sc eq "p") {
         status("You are currently not logged in. You only have view access to a published calendar.");
         exit;
      }
      #if ($g ne "") {
         #status("For group calendars you do not need to use this link. You can use the buttons in the left frame to navigate HotDiary.");
         #exit;
      #}

      system "mkdir -p $ENV{HDREP}/$alpha/$login";
      system "mkdir -p $ENV{HDHREP}/$alpha/$login";
      $pr = "";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/d$biscuit.html";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/diarymenu.html";
      $pr = strapp $pr, "leftFrame=rep/$alpha/$login/l$biscuit.html";
      $pr = strapp $pr, "rightFrame=rep/$alpha/$login/$biscuit.html";
      #$label = "HotDiary Address Add/Search Menu.";
      #$label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      #$label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      #$logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      #$pr = strapp $pr, "login=$logi";
      #$pr = strapp $pr, "label=$label";
      #$pr = strapp $pr, "label1=$label1";
      #$pr = strapp $pr, "label2=$label2";
      $pr = strapp $pr, "biscuit=$biscuit";
      parseIt $pr, 1;
      $expiry = localtime(time() + 5);
      $expiry = "\:$expiry";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/leftFrame.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/exechotmenu.cgi";
      #if (($login eq "smitha") || ($login eq "mjoshi")) {
         $calclient = adjusturl "<TR><TD WIDTH=\"100%\"><P><CENTER><a href=\"$hddomain/cgi-bin/execcalclient.cgi?biscuit=$biscuit\" target=_parent><IMAGE SRC=\"images/newcalclient.gif\" border=0></a></CENTER></TD></TR>";
      #} else {
      #   $calclient = "";
      #}
      $pr = strapp $pr, "calclient=$calclient";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$alpha/$login/l$biscuit.html";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "expiry=$expiry";
      parseIt $pr, 1;
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
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/stdpghdr.html";
      $pr = strapp $pr, "expiry=";
      parseIt $pr, 1;

      $pr = "";
      $label = "$t2 Address Add/Search Menu.";
      $label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      $label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      $pr = strapp $pr, "login=$login";
      $pr = strapp $pr, "label1=$label1";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "biscuit=$biscuit";
      system "mkdir -p $ENV{HDREP}/$alpha/$login";
      system "mkdir -p $ENV{HDHREP}/$alpha/$login";
      $buddy = "rep/$alpha/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/friend.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/friend.html";
      $buddy = "rep/$alpha/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      parseIt $pr, 1;
      system "/bin/cat $ENV{HDHREP}/$alpha/$login/friend.html > $ENV{HDREP}/$alpha/$login/friend$biscuit.html";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/addrmenutblhdr.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/execaddraddsearch.cgi";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/addrmenutblhdr.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/menuaddrtbl.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/menuaddrtbl.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdmenutblftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/stdmenutblftr.html";   
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpgftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alpha/$login/stdpgftr.html";
      parseIt $pr, 1;

      system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/addrmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menuaddrtbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";

      #system "/bin/cat $ENV{HDHREP}/$alpha/$login/d$biscuit.html";
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/d$biscuit.html";
      exit;
   }
   #system "cat \"$ENV{HDTMPL}/content.html\"";

   $evtbanner = $input{evtbanner};
      $eday = trim $input{'day'};


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
      $evenue = $input{'evenue'}; 
      #status ("desc = $edesc");

# Accessing hidden fields in form (hdcalviewtop.html)
      $rurl = $input{rurl};
      $rurl = adjusturl $rurl;
      
      #status("ehour = $ehour");
      #hddebug "Manoj";


      if ($a eq "a") {
         depositmoney $login;
         #hddebug "addEvent";
         addEvent $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $g, $econtact, $evtbanner, $evenue;

	 #if ($addresses ne "") {
         #   $name = "$logtab{$login}{fname} $logtab{$login}{lname} (HotDiary Login - $login)";
            #sendEventInvitations($name, $g, $etitle, $edtype, $edesc, $ehour, $emin, $emeridian, $erecurtype, $ezone, $eshare, $efree, $evtbanner, $evenue, $addresses, $edhour, $edmin, $logtab{$login}{email});
	 #}
      }
      #hddebug "after addEvent";
      if ($a eq "e") {
         $en = $input{'en'}; 
	 $type = $input{type};
	 #hddebug "type = $type";
         if ($type eq "meeting") {
            $people = $input{people};
            $peoplevals = $input{peoplevals};
            $businesses = $input{businesses};
            $bizteamvals = $input{bizteamvals};
            $bizteams = $input{bizteams};
            $bizmemvals = $input{bizmemvals};
            $bizmem = $input{bizmem};
            $bizresourcevals = $input{bizresourcevals};
            $bizresource = $input{bizresource};
            $bizpeoplevals = $input{bizpeoplevals};
            $bizpeople = $input{bizpeople};
            $groups = $input{groups};
            $groupvals = $input{groupvals};
	    #hddebug "groups = $groups, groupvals = $groupvals";
            #hddebug "$emonth = $ehour, $eday, $min";
	    calfuncs::bizfuncs::updateMeetingEvent($people, $peoplevals, $bizteamvals, $bizteams, $bizmemvals, $bizmem, $bizresourcevals, $bizresource, $bizpeoplevals, $bizpeople, $groups, $groupvals, $en, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $g, $econtact, "1", $businesses);
         } else {
            updateEvent $en, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $login, $g, $econtact, $evtbanner, $evenue;

	 #if ($addresses ne "") {
            $name = "$logtab{$login}{fname} $logtab{$login}{lname} (HotDiary Login - $login)";
            #sendEventInvitations($name, $g, $etitle, $edtype, $edesc, $ehour, $emin, $emeridian, $erecurtype, $ezone, $eshare, $efree, $evtbanner, $evenue, $addresses, $edhour, $edmin, $logtab{$login}{email});
	 #}
         }
      }

      hddebug "rurl = $rurl";

      $prm = "";
      $prm = strapp $prm, "rh=$rh";
      $prm = strapp $prm, "label=$label";
      $prm = strapp $prm, "banner=$banner";
      if ($logo ne "") {
         $logo = adjusturl $logo;
      }
      $prm = strapp $prm, "logo=$logo";
      $prm = strapp $prm, "redirecturl=$rurl";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
      parseIt $prm;
      hdsystemcat "$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";

      #if ($login ne "mjoshi") {
      #   hdsystemcat "$rurl";
      #} else {
	 ## these below lines were commented out becos print is not working
	 ## after upgrading the tomcat/apache web server.
         ##if (!($rurl =~ /http/)) {
         ##   print "Location: http://$vdomain/$rurl\n\n"
         ##} else {
         ##   print "Location: $rurl\n\n"
         ##}
      #}
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
      $rurl = adjusturl $rurl;
      #status("rurl = $rurl");

      if ($a eq "a") {
         depositmoney $login;
         addTodo $etitle, $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $login, $g, $evtbanner;
      }
      if ($a eq "e") {
         $en = $input{'en'};
         updateTodo $en, $etitle, $edesc, $emonth, $eday, $eyear, $ehour, $emeridian, $eshare, $epriority, $estatus, $login, $g, $evtbanner;
      }


      hddebug "$rurl";

      $prm = "";
      $prm = strapp $prm, "rh=$rh";
      $prm = strapp $prm, "label=$label";
      $prm = strapp $prm, "banner=$banner";
      if ($logo ne "") {
         $logo = adjusturl $logo;
      }
      $prm = strapp $prm, "logo=$logo";
      $prm = strapp $prm, "redirecturl=$rurl";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
      parseIt $prm;
      hdsystemcat "$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";

      #if ($login ne "mjoshi") {
      #   hdsystemcat "$rurl";
      #} else {
	 ## print is not working after upgrading the websever.
         ##print "Location: $rurl\n\n";
      #} 

   }

   if ($f eq "r") {
      system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/reportcal$$-$login";
      $repparms = "biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&g=$g&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip&othermember=";
      $cgis = "$ENV{HDEXECCGI}/execreportcal.cgi";
      system "echo \"$cgis\" \"$repparms\" >> $ENV{HDHOME}/tmp/reportcal$$-$login";
      #$cgis = "$ENV{HDEXECCGI}/execreportcal.cgi?biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&g=$g&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip";
         # reset the timer.
      if (-f "$ENV{HDHOME}/tmp/reportcal$$-$login") {
	 system "chmod 777 $ENV{HDHOME}/tmp/reportcal$$-$login";
         $sesstab{$biscuit}{'time'} = time();
         system "cat $ENV{HDTMPL}/content.html"; 
         system "\"$ENV{HDHOME}/tmp/reportcal$$-$login\"";
      } else {
         status("No Events to report.");
      } 
      exit;
   }

    



   if (($a ne "a") && ($a ne "e")) {
      if ($g eq "") {
         $repdir = "$alpha/$login";
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
         hddebug "banner1 = $banner";
         $logo = adjusturl $hdtab{$login}{logo};
      }
 
      if ($g ne "") {
         $publish = $lgrouptab{$g}{cpublish};
      } else {
         $publish = $logtab{$login}{calpublish};
      }

      #hddebug "sc = $sc";
      hddebug "Calling createCalendar jp = $jp, vdomain = $vdomain, g = $g, rh = $rh";
      createCalendar $dy, $mo, $yr, "$ENV{HDHREP}/$repdir/cal$rand$biscuit.html", $login, $biscuit, $vw, $f, $a, $h, $m, $tz, $en, $sc, $jvw, $g, $publish, "$rh", "$logo", "$title", "$banner", "$vdomain", "$hs", "$jp", "$os", "$pwenc";
      if (!(-f "$ENV{HDHREP}/$repdir/cal$rand$biscuit.html")) {
         status "$login: We could not create the document that you requested. Please use the browser <b>Back</b> button, and re-try. If this re-occurs, please contact HotDiary support at support\@$diary.";
         hddebug "Serious ERROR! File $ENV{HDHREP}/$repdir/cal$rand$biscuit.html was not created.";
      } else {
         #system "cat \"$ENV{HDHREP}/$repdir/cal$rand$biscuit.html\"";
         hdsystemcat "$ENV{HDHREP}/$repdir/cal$rand$biscuit.html";
      }
   }

# reset the timer.
   if ($biscuit ne "") {
      $sesstab{$biscuit}{'time'} = time(); 
      tied(%sesstab)->sync(); 
      tied(%logsess)->sync(); 
   }
}

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
# FileName: mgcalclient.cgi
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
use mgcalutil::mgcalutil;
use calfuncs::mgcalfuncs;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   hddebug "mgcalclient.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   $g = $input{g};
   #hddebug "g = $g";

   
   if ($biscuit eq "") {
      $sc = "p";
   }
   if (($sc eq "p") && ($g ne "")) {
      system "mkdir -p $ENV{HDHREP}/$g";
      system "chmod 755 $ENV{HDHREP}/$g";
   }

   $hs = $input{'hs'};
   $vdomain = trim $input{'vdomain'};
   $jp = trim $input{'jp'};


   if ($jp ne "") {
      #hddebug "JiveIt! Customer Forwarded $ENV{HTTP_FORWARDED}";
   }

   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
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
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };      

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };

   # check if session record exists. 
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

# bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'readonly' ] };

   if ( ($g ne "") && (!exists $lmergetab{$g}) ) {
      status("The calendar $g is not available. Either it has been deleted or it was never created.");
      exit;
   }

   if (($sc ne "p") && ($g ne "")) {
      if (exists $lmergetab{$g}) {
         if ("\L$lmergetab{$g}{'groupfounder'}" ne "\L$login") {
            if ($lmergetab{$g}{'readonly'} eq "on") {
               if (($a eq "e") || ($a eq "a") || ($a eq "r")) {
                  status("You do not have permission to edit this calendar."); 
                  exit;
               }
            }
         }
      }
   }


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

   if ($f eq "j") {
      if (($login ne "mjoshi") && ($login ne "smitha")) {
         status("This service will be introduced shortly. If you need to create Memos, please click on the Home link and use the MemoCal button in the left frame.");
         exit;
      }
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

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
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/d$biscuit.html";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/diarymenu.html";
      $pr = strapp $pr, "leftFrame=rep/$alphaindex/$login/l$biscuit.html";
      $pr = strapp $pr, "rightFrame=rep/$alphaindex/$login/$biscuit.html";
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
      $pr = strapp $pr, "calclient=";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$alphaindex/$login/mg$biscuit.html";
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
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdpghdr.html";
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
      $buddy = "rep/$alphaindex/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/friend.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/friend.html";
      $buddy = "rep/$alphaindex/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      parseIt $pr, 1;
      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/friend.html > $ENV{HDREP}/$alphaindex/$login/friend$biscuit.html";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/addrmenutblhdr.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/execaddraddsearch.cgi";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/addrmenutblhdr.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/menuaddrtbl.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/menuaddrtbl.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdmenutblftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdmenutblftr.html";   
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpgftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdpgftr.html";
      parseIt $pr, 1;

      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdpghdr.html $ENV{HDHREP}/$alphaindex/$login/addrmenutblhdr.html $ENV{HDHREP}/$alphaindex/$login/menuaddrtbl.html $ENV{HDHREP}/$alphaindex/$login/stdmenutblftr.html $ENV{HDHREP}/$alphaindex/$login/stdpgftr.html > $ENV{HDREP}/$alphaindex/$login/$biscuit.html";

      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/d$biscuit.html";
      exit;
   }
   system "cat \"$ENV{HDTMPL}/content.html\"";


   # if the function is event, and the action is add
   # When 8:00 (or 9:00, 10:00...) are pressed in daily view
   # in the event mode, a Add Event
   # HTML form is displayed. Enter the information for the event,
   # and press the Add button. When this add button is pressed the
   # following logic is executed.


# Accessing hidden fields in form (hdcalviewtop.html)
   $rurl = $input{rurl};
    
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
         system "\"$ENV{HDHOME}/tmp/reportcal$$-$login\"";
      } else {
         status("No Events to report.");
      } 
      exit;
   }
    
   if (($a ne "a") && ($a ne "e")) {
      if ($g eq "") {
         $repdir = "$alphaindex/$login";
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
 
      if ($g ne "") {
         $publish = $lmergetab{$g}{cpublish};
      }

      #hddebug "createCalendar";
      createCalendar $dy, $mo, $yr, "$ENV{HDHREP}/$repdir/mgcal$rand$biscuit.html", $login, $biscuit, $vw, $f, $a, $h, $m, $tz, $en, $sc, $jvw, $g, $publish, "$rh", "$logo", "$title", "$banner", "$vdomain", "$hs", "$jp", "$os";
      system "cat \"$ENV{HDHREP}/$repdir/mgcal$rand$biscuit.html\"";
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

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
# FileName: mergedcalclient.cgi
# Purpose: New HotDiary Calendar Client
# Creation Date: 06-14-99 
# Created by: Smitha Gudur
# 

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use businesscalutil::teammergedcalutil;
use AsciiDB::TagFile;
use utils::utils;
use calfuncs::businesscalfuncs;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("mergedcalclient.cgi");    

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   $rh = $input{rh};
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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

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

   $business = $input{business};
   $teamname = $input{teamname};
   $teamname = "\L$teamname";

   if ($login eq "") {
      status("You are currently viewing a published Calendar. If you would like to make changes to this Calendar, you must be in edit mode. Please close this browser window and go back to the main browser.");
      exit;
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

   if ((!exists $businesstab{$business}) || ($business eq "")) {
      if ($os ne "nt") {
         $execbusiness = encurl "execbusiness.cgi";
         $execcreatebusiness = encurl "execcreatebusiness.cgi";
      } else {
         $execbusiness = "execbusiness.cgi";
         $execcreatebusiness = "execcreatebusiness.cgi";
      }

      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;
   }

   $a = $input{a};

   if (!-d ( "$ENV{HDDATA}/business/business/$business/teams/teamtab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/teamtab";
      system "chown nobody:nobody $ENV{HDDATA}/business/business/$business/teams/teamtab";
      status("The calendar $teamname is not available. Either it has been deleted or it was never created.");
   }


   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode', 
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] };

   if ( ($teamname ne "") && (!exists $teamtab{$teamname}) ) {
      status("The calendar $teamname is not available. Either it has been deleted or it was never created.");
      exit;
   }

   $en = $input{en};

   # add business event to my personal calendar 
   if (($sc ne "p") && ($a eq "u")) {
      addBusEventToMyCal($en, $login, $business, $teamname);
      $a = "d";
   }

   # create an entry in the peopletab
   tie %peopletab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$business/peopletab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['login', 'business']};

   $permit = 0;
   if ($login ne $businesstab{$business}{businessmaster}) {
      tie %mgraccesstab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother',
		 'invite',
                'approve', 'delete', 'edit', 'manage', 'contact', 'teams']};

      tie %managertab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login']};

     if (!exists($managertab{$login})) {
         $permit = 1;    
     } else {
       if (exists($managertab{$login})) {
          if ($mgraccesstab{access}{teams} ne "CHECKED") {
            $permit = 1;
         }
       }
     }
   }


   if (($sc ne "p") && ($teamname ne "")) {
      if (exists $teamtab{$teamname}) {
         if (($a eq "e") || ($a eq "a") || ($a eq "r")) {
            if ($permit != 0) {
               status("You do not have permission to add, edit or remove an event in this calendar."); 
               exit;
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
   $jvw = $input{jvw};
   $rh = $input{rh};
   $ip = $input{HDLIC};
   $jp = $input{jp};
   $os = $input{os};
   if ($rh ne "") {
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
   $alphaindex = $alphaindex . -'index';

   if ($f eq "h") {
      if ($sc eq "p") {
         status("You are currently not logged in. You only have view access to a published calendar.");
         exit;
      }
      #if ($teamname ne "") {
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
      #if (($login eq "smitha") || ($login eq "mjoshi")) {
         $calclient = adjusturl "<TR><TD WIDTH=\"100%\"><P><CENTER><a href=\"http://www.hotdiary.com/cgi-bin/execcalclient.cgi?biscuit=$biscuit\" target=_parent><IMAGE SRC=\"images/newcalclient.gif\" border=0></a></CENTER></TD></TR>";
      #} else {
      #   $calclient = "";
      #}
      $pr = strapp $pr, "calclient=$calclient";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$alphaindex/$login/l$biscuit.html";
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

      #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/d$biscuit.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/d$biscuit.html";
      exit;
   }
   
   #if (($a eq "de") || ($a eq "da") ) {
   #    status("$login: You are viewing team Group Calendars that displays all the events & todos of members belonging to $teamname.");
   #    exit;
   #}
   #system "cat \"$ENV{HDTMPL}/content.html\"";

   # if the function is event, and the action is add
   # When 8:00 (or 9:00, 10:00...) are pressed in daily view
   # in the event mode, a Add Event
   # HTML form is displayed. Enter the information for the event,
   # and press the Add button. When this add button is pressed the
   # following logic is executed.
   if ((($a eq "a") && ($f eq "e")) || (($a eq "e") && ($f eq "e")) ||
      (($a eq "a") && ($f eq "m")) || (($a eq "e") && ($f eq "m")) ) {
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

# Accessing hidden fields in form (hdcalviewtop.html)
      $rurl = $input{rurl};
      #status("rurl = $rurl");
      
      #status("ehour = $ehour");

      if ($f eq "e") {
	 status("$login: You are viewing team group calendars that displays all the events of members belonging to $teamname.");
         exit;
      }
   }

   # for todo 
   if ((($a eq "a") && ($f eq "t")) || (($a eq "e") && ($f eq "t"))) {
      #system "cat $rurl";
      hdsystemcat "$rurl";
   }

   #if ($login eq "smitha") {
      if ($f eq "r") {
         system "echo '#!/bin/ksh' > $ENV{HDHOME}/tmp/reportcal$$-$login";
         $repparms = "biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&teamname=$teamname&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip";
         $cgis = "$ENV{HDEXECCGI}/execreportcal.cgi";
         system "echo \"$cgis\" \"$repparms\" >> $ENV{HDHOME}/tmp/reportcal$$-$login";
         #$cgis = "$ENV{HDEXECCGI}/execreportcal.cgi?biscuit=$biscuit&jp=$jp&vdomain=$vdomain&hs=$hs&teamname=$teamname&mo=$mo&yr=$yr&rh=$rh&HDLIC=$ip&business=$business";
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
   #}


   if (($a ne "a") && ($a ne "e")) {
      $repdir = $login;
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

      if ($teamname ne "") {
         $publish = $teamtab{$teamname}{cpublish};
      }

      businesscalutil::teammergedcalutil::createCalendar($dy, $mo, $yr, "$ENV{HDHREP}/$repdir/businessmergedview$rand$biscuit.html", $login, $biscuit, $vw, $f, $a, $h, $m, $tz, $en, $sc, $jvw, $teamname, $publish, "$rh", "$logo", "$title", "$banner", "$vdomain", "$hs", "$jp", "$os", "$business");
      #system "cat \"$ENV{HDHREP}/$repdir/businessmergedview$rand$biscuit.html\"";
      hdsystemcat "$ENV{HDHREP}/$repdir/businessmergedview$rand$biscuit.html";
   }


   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

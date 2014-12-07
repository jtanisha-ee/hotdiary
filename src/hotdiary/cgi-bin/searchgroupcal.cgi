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
# FileName: searchgroupcal.cgi
# Purpose: New HotDiary Search Groups
# Creation Date: 07-16-99
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

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug("searchgroupcal.cgi");


   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

   $hs = $input{'hs'}; 
   $jp = $input{'jp'}; 
   $os = $input{'os'}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }
 

   $biscuit = $input{'biscuit'};
   if ($biscuit eq "") {
      if ($hs eq "") {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   }

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
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
        status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
        status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed'] };

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
   }
   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
   }
   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   $calkey = $input{'calkey'};
   hddebug "search key = $calkey";
   $calkey = "\L$calkey";
   if ( (length $calkey) < 2) {
      status "You must specify a keyword of atleast 2 characters when searching for groups or calendars.";
      exit;
   }
   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   $msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Group Id</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Group Title</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Group Master</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Organization Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Group Type</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Group Description</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Published Calendar</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;
   $cntr = 0;
   foreach $cal (sort keys %lgrouptab) {
       if ((($lgrouptab{$cal}{'listed'} ne "on") && ($lgrouptab{$cal}{'groupfounder'} ne $login)) || ($lgrouptab{$cal}{'groupfounder'} eq $login)) {
         if ( ((index "\L$lgrouptab{$cal}{'groupname'}", "\L$calkey") != -1) ||
            ((index "\L$lgrouptab{$cal}{'grouptitle'}", "\L$calkey") != -1) ||
            ((index "\L$lgrouptab{$cal}{'ctype'}", "\L$calkey") != -1) ||
            ((index "\L$lgrouptab{$cal}{'groupdesc'}", "\L$calkey") != -1) ) {
              $cntr = $cntr + 1;
              if ($cntr == 400) {
		 #last is like a break statement in loop
                 last;
              }
              $msg = "<TR>";
              $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=RADIO NAME=radio1 VALUE=\"$cal\"></FONT></TD>";
              $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$cal &nbsp;</FONT></TD>";
              $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$lgrouptab{$cal}{'grouptitle'} &nbsp;</FONT></TD>";
              $groupfounder = $lgrouptab{$cal}{'groupfounder'};
              if (exists $logtab{$groupfounder}) {
                 if ($logtab{$groupfounder}{'checkid'} ne "CHECKED") {
                    $groupfounder = "BLOCKED";
                 }
              } else {
                $groupfounder = "BLOCKED";
              }
              $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$groupfounder &nbsp;</FONT></TD>";
              $msg .= "<TD> &nbsp;</TD>";
              $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$lgrouptab{$cal}{'ctype'} &nbsp;</FONT></TD>";
             $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"1\">$lgrouptab{$cal}{'groupdesc'} &nbsp;</FONT></TD>";
             if ($lgrouptab{$cal}{'cpublish'} eq "on") {
                $cpub = "Yes";
             }
             $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$cpub &nbsp;</FONT></TD>";
             $msg .= "</TR>";
             if ((exists $sgrouptab{$cal}) || (exists $fgrouptab{$cal})) {
                $smsg .= $msg;
             } else {
                $umsg .= $msg;
             }
         }
      }
   }
   $smsg .= "</TABLE>";
   $umsg .= "</TABLE>";

   $rh = $input{'rh'};

   tie %hdtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/hdtab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $label = adjusturl $hdtab{$login}{title};
   } else {
      $label = "HotDiary";
   }

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $label = adjusturl($hdtab{$login}{title});
   } else {
      $label = "HotDiary";
   }
                           

   if ($rh ne "") {
      $ip = $input{HDLIC};

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
    
       tie %jivetab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/jivetab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };

       $logo = "";
       if (exists $jivetab{$jp}) {
          $logo = $jivetab{$jp}{logo};
          $title = $jivetab{$jp}{title};
          $banner = $jivetab{$jp}{banner};
          $label = $title;
       } else {
          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             if (exists $parttab{$partner}) {
                $logo = $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
       }
   }
 
    
   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }  
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
   } else {
      $prml = strapp $prml, "formenc=";
   }

   $alphj = substr $jp, 0, 1;
   $alphj = $alphj . '-index';

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphj/$jp/templates/hddisplaygroupcal.html") ) {
      $tmpl = "$ENV{HDDATA}/$alphj/$jp/templates/hddisplaygroupcal.html";
   } else {
      $tmpl = "$ENV{HDTMPL}/hddisplaygroupcal.html";
   }
   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/dgc-$biscuit-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   if ($rh eq "") {
      $cgis = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
   }

   $prml = strapp $prml, "searchcal=$cgis";
   $createcal = adjusturl "$cgis&f=cpc";
   $prml = strapp $prml, "createcal=$createcal";
   $managecal = adjusturl "$cgis&f=mc";
   $prml = strapp $prml, "managecal=$managecal";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "login=$login";
   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {

      if ($rh eq "") {
         $cgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp&os=$os";
      } else {
         $cgi = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp&os=$os";
      }
   }

   $prml = strapp $prml, "percal=$cgi";
   $home = adjusturl "$cgi&f=h";
   $prml = strapp $prml, "home=$home";
   $smsg = adjusturl $smsg;
   $prml = strapp $prml, "scalendars=$smsg";
   $umsg = adjusturl $umsg;
   $prml = strapp $prml, "ucalendars=$umsg";
   $prml = strapp $prml, "numentries1=$cntr1";
   $prml = strapp $prml, "numentries2=$cntr2";
   if (($cntr == 400) || ($calkey eq "")) {
      $stat = adjusturl "<FONT COLOR=ff0000 FACE=\"Verdana\" SIZE=\"2\">Too many matches were found. The results have been truncated. We display only the most recently accessed groups or calendars. You can narrow down the search by entering a specific keyword.</FONT><BR><BR>";
   } else {
      $stat = "";
   }
   $prml = strapp $prml, "status=$stat";
   parseIt $prml;
   #system "/bin/cat $ENV{HDTMPL}/content.html";
   #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/dgc-$biscuit-$$.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/dgc-$biscuit-$$.html";
   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

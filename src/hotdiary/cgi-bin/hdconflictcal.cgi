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
# FileName: hdconflictcal.cgi
# Purpose: New HotDiary conflict Resolutions
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

   #print &PrintHeader;
   #print &HtmlTop ("hdconflictcal.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

   $hs = $input{'hs'}; 
   $jp = $input{'jp'}; 
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

   $group = $input{'g'};

   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   $msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; Month &nbsp;</CENTER> </FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; Day &nbsp;</CENTER> </FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; Time &nbsp;</CENTER></FONT></TD>";
   #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Min</FONT></TD>";
   #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Meridian</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; Event &nbsp;</CENTER> </FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; Event Details &nbsp; </CENTER></FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;

   $mo = trim $input{mo};
   $yr = trim $input{yr};

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if ($group eq "") {
      # bind personal appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alpha/$login/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
            'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id',
            'type'] };

      (-e "$ENV{HDDATA}/$alpha/$login/appttab" and -d "$ENV{HDDATA}/$alpha/$login/appttab") or return $prml;                      
      $lflag = 1;
   } else {
      system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject'] };

      -d "$ENV{HDDATA}/listed/groups/$group/appttab or return $prml";          
      $lflag = "";
    }
    # place these in an ascii file with blank seperator
    # month, day, hour (add 12 hours to pm time), min, entryno
    # sort this file by month, day, hour, min
    if ($lflag == 1) {
       $name = $login;
    } else {
       $name = $group;
    }
    (@entrynohsh) = sortrep($lflag, $name);
    foreach $entryno (@entrynohsh) {
       $mo = trim $input{mo};
       $yr = trim $input{yr};
       $month = trim $appttab{$entryno}{'month'};
       $year = trim $appttab{$entryno}{'year'};
       if ($mo ne $month) {
	  next;
       }
       if ($yr ne $year) {
	  next;
       }
       $monstr = getmonthstr($month);
       $wday = getWeekDayIndex($aptttab{$entryno}{day}, $month, $year);
       $daystr = getdaystr($wday);
       $msg = "<TR>";
       $msg .= "<TD></TD>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; $monstr $appttab{$entryno}{day}&nbsp;</CENTER></FONT></TD>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; $daystr &nbsp; </CENTER></FONT></TD>";
       if (($appttab{$entryno}{hour} < 10) && ($appttab{$entryno}{meridian} eq "AM")) {
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; &nbsp;$appttab{$entryno}{hour}:$appttab{$entryno}{min} $appttab{$entryno}{meridian} &nbsp; </CENTER></FONT></TD>";
       } else {
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; $appttab{$entryno}{hour}:$appttab{$entryno}{min} $appttab{$entryno}{meridian} &nbsp; </CENTER></FONT></TD>";
       }
       #$msg .= "<TD> &nbsp;</TD>";
       #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$appttab{$entryno}{min} &nbsp;</FONT></TD>";
       #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"1\">$appttab{$entryno}{meridian} &nbsp;</FONT></TD>";
       if (($appttab{$entryno}{subject}) eq "") {
          $subject = $appttab{$entryno}{dtype};
       } else {
          $subject = $appttab{$entryno}{subject};
       }
           $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; $subject &nbsp;</CENTER></FONT></TD>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>&nbsp; $appttab{$entryno}{desc} &nbsp;</CENTER></FONT></TD>";
       $msg .= "</TR>";
       $smsg .= $msg;
       $umsg .= $msg;
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
       ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };

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
   $prml = strapp $prml, "template=$ENV{HDTMPL}/hddisplayreportcal.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/rcal-$biscuit-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   if ($rh eq "") {
      $cgis = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   }

   $prml = strapp $prml, "reportcal=$cgis";
   $createcal = adjusturl "$cgis&f=cpc";
   $prml = strapp $prml, "createcal=$createcal";
   $managecal = adjusturl "$cgis&f=mc";
   $prml = strapp $prml, "managecal=$managecal";
   $searchcal = adjusturl "$cgis&f=sgc";
   $prml = strapp $prml, "searchcal=$searchcal";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "login=$login";
   if ($rh eq "") {
      $cgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgi = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   }

   $prml = strapp $prml, "percal=$cgi";
   $home = adjusturl "$cgi&f=h";
   $prml = strapp $prml, "home=$home";
   $smsg = adjusturl $smsg;
   $prml = strapp $prml, "scalendars=$smsg";
   $umsg = adjusturl $umsg;
   #$prml = strapp $prml, "ucalendars=$umsg";
   $prml = strapp $prml, "g=$group";
   $prml = strapp $prml, "calrepnm=$name";
   $monstr = getmonthstr($mo);
   $prml = strapp $prml, "mo=$monstr";
   $prml = strapp $prml, "yr=$yr";

   parseIt $prml;
   #system "/bin/cat $ENV{HDTMPL}/content.html";
   #system "/bin/cat $ENV{HDHREP}/$alpha/$login/rcal-$biscuit-$$.html";
   hdsystemcat "$ENV{HDHREP}/$alpha/$login/rcal-$biscuit-$$.html";
   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

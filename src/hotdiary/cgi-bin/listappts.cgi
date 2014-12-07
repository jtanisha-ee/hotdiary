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
# FileName: listappts.cgi
# Purpose: New HotDiary listing all reminders for a group/personal/othermember
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
   $SESSION_TIMEOUT = 3600;

   hddebug "listappts.cgi()";
   $remove = $input{remove};
   hddebug "remove = $remove";

   $rh = $input{'rh'};
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
 

   $sc = $input{sc};
   $biscuit = $input{'biscuit'};
   if ( ($biscuit eq "") && ($sc ne "p") ) {
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
   if ($sc ne "p") {
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
   }

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if ($sc ne "p") {
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
   }

   $group = $input{'g'};

   $msg = "<TABLE BORDER=1 CELLPADDING=5 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR HEIGHT=\"10%\" BGCOLOR=1199ff>";
   $msg .= "<TD></TD>";
   $msg .= "<TD VALIGN=CENTER ALIGN=CENTER HEIGHT=\"10%\" WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>Month</CENTER> </FONT></TD>";
   #$msg .= "<TD VALIGN=CENTER ALIGN=CENTER WIDTH=\"10%\"><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>Day</CENTER> </FONT></TD>";
   $msg .= "<TD VALIGN=CENTER ALIGN=CENTER WIDTH=\"15%\"><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>Time</CENTER></FONT></TD>";
   #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Min</FONT></TD>";
   #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Meridian</FONT></TD>";
   $msg .= "<TD VALIGN=CENTER ALIGN=CENTER WIDTH=\"33%\"><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>Event</CENTER> </FONT></TD>";
   $msg .= "<TD VALIGN=CENTER ALIGN=CENTER WIDTH=\"33%\"><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>Event Details</CENTER></FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;


   $othermember = $input{othermember};

   hddebug "login = $login";

   if ($group eq "") {
      if ($othermember eq "") {
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
        $alphao = substr $othermember, 0, 1;
        $alphao = $alphao . '-index';
       # bind personal appt table vars
        tie %appttab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/$alphao/$othermember/appttab",
        SUFIX => '.rec',
        SCHEMA => {
           ORDER => ['entryno', 'login', 'month', 'day', 'year',
              'hour', 'min', 'meridian', 'dhour', 'dmin',
              'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
             'subject'] };
        (-e "$ENV{HDDATA}/$alpha/$othermember/appttab" and -d "$ENV{HDDATA}/$alpha/$othermember/appttab") or return $prml;                      
        $lflag = 1;
      }
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
       if ($othermember eq "") {
          $name = $login;
       } else {
          $name = $othermember;
       }
    } else {
       $name = $group;
    }
    hddebug "name = $name, lflag = $lflag";
    (@entrynohsh) = sortrep($lflag, $name);


    $remove = $input{remove};
    hddebug "remove = $remove";
    $remove = $input{remove};

    $numbegin = $input{numbegin};
    $numend = $input{numend};

    if ($remove ne "") {
      $k = 0;
      for ($i = $numbegin; $i <= $numend; $i= $i + 1) {
          $appt = $input{"box$k"};
          $checkboxval = $input{$appt};
          if ($checkboxval eq "on") {
             if (exists($appttab{$appt})) {
                delete $appttab{$appt};
             }
          }
          $k = $k + 1;
      }
      $listall = adjusturl "/cgi-bin/execlistappts.cgi?biscuit=$biscuit&jp=$jp";
      status("$login: You have successfully deleted the selected reminders. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execlistappts.cgi?biscuit=$biscuit&jp=$jp\">here</a> to list all reminders.");

      tied(%sesstab)->sync();
      tied(%logsess)->sync();
      tied(%appttab)->sync();
      exit;
   }              
  
  
    $cdir = ""; 
    foreach $entryno (@entrynohsh) {
       #hddebug ("hash number = $entryno");
       if ($entryno eq "") {
	  next;
       } 
       if (!exists($appttab{$entryno})) {
	  next;
       }

       $month = trim $appttab{$entryno}{'month'};
       $year = trim $appttab{$entryno}{'year'};

       $monstr = getmonthstr($month);
       $wday = getWeekDayIndex($aptttab{$entryno}{day}, $month, $year);
       $daystr = getdaystr($wday);
       $msg = "<TR>";
       $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$entryno> </FONT></TD>";
       $cdir .= $entryno;
       $cdir .= " ";
       $msg .= "<TD ALIGN=CENTER><FONT FACE=\"Verdana\" SIZE=\"2\">$monstr $appttab{$entryno}{day} $appttab{$entryno}{year}</FONT></TD>";
       #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><CENTER>$daystr</CENTER></FONT></TD>";
       $min100 = trim $appttab{$entryno}{min};
       if (($appttab{$entryno}{hour} < 10) && ($appttab{$entryno}{meridian} eq "AM")) {
          $msg .= "<TD ALIGN=CENTER><FONT FACE=\"Verdana\" SIZE=\"2\">$appttab{$entryno}{hour}:$min100 $appttab{$entryno}{meridian}</FONT></TD>";
       } else {
          $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$appttab{$entryno}{hour}:$min100 $appttab{$entryno}{meridian}</FONT></TD>";
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
   $smsg .= "<BR><BR><FONT FACE=\"Verdana\" SIZE=3><INPUT TYPE=submit NAME=remove VALUE=\"Remove\"></FONT>";
   $umsg .= "</TABLE>";


   tie %hdtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/hdtab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['title', 'logo' ] };


   if ($sc ne "p") {
      if (exists $hdtab{$login}) {
         $label = adjusturl $hdtab{$login}{title};
      } else {
         $label = "HotDiary Portal Services";
      }
   
      tie %hdtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/hdtab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['title', 'logo' ] };
   
   
      if (exists $hdtab{$login}) {
         $label = adjusturl($hdtab{$login}{title});
      } else {
         $label = "HotDiary Portal Services";
      }
   } else {
      $label = "HotDiary Portal Services"; 
   }
                           

   #if ($rh ne "") {
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
          hddebug "title = $title";
          $logo = $jivetab{$jp}{logo};
          #hddebug "logo = $logo";
          $title = $jivetab{$jp}{title};
          $banner = $jivetab{$jp}{banner};
          #hddebug "banner = $banner";
          $label = $title;
       } else {
          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             #hddebug "partner = $partner";
             if (exists $parttab{$partner}) {
                $logo = $parttab{$partner}{logo};
                #hddebug "logo = $logo";
                $title = $parttab{$partner}{title};
                #hddebug "title = $title";
                $banner = adjusturl $parttab{$partner}{banner};
                #hddebug "banner = $banner";
                $label = $title;
             }
          }
       }
   #}
 
   hddebug "jp = $jp, title=$title"; 
   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }  
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/hddisplayallcal.html";
   if ($sc eq "p") {
       $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/rcal-$biscuit-$$.html";
   } else {
       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/rcal-$biscuit-$$.html";
   }
   $prml = strapp $prml, "biscuit=$biscuit";
   if ($rh eq "") {
      $cgis = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   }

   hddebug "vdomain = $vdomain";

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
   if (-f "$ENV{HDREP}/$alpha/$login/topcal.html") {
      $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      if ($rh eq "") {
         $cgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
      } else {
         $cgi = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
      }
   }

   if ($rh eq "") {
      $percal = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $percal = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   }
  
         #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 1;
      $numend = $mcntr;
      $numbegin = $mcntr;

      $hiddenvars = "";
      (@hshcdir) = split " ", $cdir;
      # this tells from where the parameter for selection starts
      foreach $cn (@hshcdir) {
         $cn = trim $cn;
         $numend = $numend + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $k = $k + 1;
      }
      $numend = $numend - 1; 

   $prml = strapp $prml, "percal=$percal";
   $home = adjusturl "$cgi&f=h";
   $prml = strapp $prml, "home=$home";
   $smsg = adjusturl $smsg;
   $prml = strapp $prml, "scalendars=$smsg";
   $umsg = adjusturl $umsg;
   #$prml = strapp $prml, "ucalendars=$umsg";
   $prml = strapp $prml, "g=$group";
   $prml = strapp $prml, "calrepnm=$name";
   $prml = strapp $prml, "numbegin=$numbegin";
   $prml = strapp $prml, "numend=$numend";
   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";

   #$monstr = getmonthstr($mo);
   #hddebug "monstr = $monstr";
   #hddebug "yr = $yr";
   #$prml = strapp $prml, "mo=$monstr";
   #$prml = strapp $prml, "yr=$yr";

   $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
   $prml = strapp $prml, "formenc=$formenc";

   parseIt $prml;
   system "/bin/cat $ENV{HDTMPL}/content.html";
   if ($sc eq "p") {
      system "/bin/cat $ENV{HDHOME}/tmp/rcal-$biscuit-$$.html";
   } else {
      system "/bin/cat $ENV{HDHREP}/$alpha/$login/rcal-$biscuit-$$.html";
   }
   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

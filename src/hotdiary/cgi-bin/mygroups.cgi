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
# FileName: mygroups.cgi
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

   hddebug("mygroups.cgi");
   $hdcookie = $ENV{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

   $hs = $input{'hs'}; 
   $jp = $input{'jp'}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

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

   
   # bind subscribed group table vars
   system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
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
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   $g = $input{g};

   if ( ($g ne "") && (!exists $sgrouptab{$g}) && (!exists $fgrouptab{$g}) ) {
      status "You are neither the founder nor the subscriber of the group $g. Please check the group name and try again. Click $memoprog to return to Memo Manager.";
      exit;
   }


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
                           

      $HDLIC = $input{HDLIC};

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

      if (exists $jivetab{$jp}) {
          $logo = $jivetab{$jp}{logo};
          $title = $jivetab{$jp}{title};
          $banner = $jivetab{$jp}{banner};
          $label = $title;
       } else {
          if (exists $lictab{$HDLIC}) {
             $partner = $lictab{$HDLIC}{partner};
             if (exists $parttab{$partner}) {
                $logo = $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
       }

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }  

   $prml = "";
   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist < 0) && ($#glist1 < 0) ) {
      $lab100 = adjusturl "<FONT FACE=Verdana SIZE=1>Groups Not Created Or Subscribed</FONT>";
      $prml = strapp $prml, "memotype=$lab100";
   } else {
      $memotype = "<BR><CENTER><B>Groups Created or Subscribed</B><BR><BR><TABLE CELLPADDING=5 CELLSPACING=0 WIDTH=\"20%\" BORDER=0>";
      $memotype .= "<TR ALIGN=CENTER><TD>";
      $memotype .= "<FONT FACE=Verdana SIZE=2><SELECT NAME=selgroup SIZE=8>";
      $cnt = 0;
      foreach $grp (keys %fgrouptab) {
         if ($cnt == 0) {
           $memotype .= "<OPTION SELECTED>$grp";
         } else {
           $memotype .= "<OPTION>$grp";
         }
         $cnt = $cnt + 1;
      }

      foreach $grp (keys %sgrouptab) {
         if ($cnt == 0) {
            $memotype .= "<OPTION SELECTED>$grp";
         } else {
            $memotype .= "<OPTION>$grp";
         }
         $cnt = $cnt + 1;
      }

      $memotype .= "</SELECT></FONT>";
      $memotype .= "</TD>";
      $memotype .= "<TD>";
      $memotype .= "</TD></TR></TABLE></CENTER>";
      $memotype = adjusturl $memotype;
      $prml = strapp $prml, "memotype=$memotype";
   }
    

   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execgroupmemocal = encurl "execgroupmemocal.cgi";
      $execgroupcal = encurl "execgroupcal.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execgroupmemocal =  "execgroupmemocal.cgi";
      $execgroupcal = "execgroupcal.cgi";
   }

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/mygroups.html") ) {
       $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/mygroups.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/mygroups.html";
   }

   $groupcal = "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execgroupcal&p1=biscuit&p2=f&p3=jp&pnum=4&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/mygroups-$biscuit-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";

   ##if ($rh eq "") {
   ##   $cgis = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os&$hidden_enums";
   ##} else {
   ##   $cgis = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os&$hidden_enums";
   ##}

   $searchcal = adjusturl $groupcal;
   $prml = strapp $prml, "searchcal=$searchcal";

   $createcal = adjusturl "$groupcal&f=cpc";
   $prml = strapp $prml, "createcal=$createcal";

   $managecal = adjusturl "$groupcal&f=mc";
   $prml = strapp $prml, "managecal=$managecal";

   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "login=$login";
   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";
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
   $prml = strapp $prml, "status=$stat";

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
   }

  
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   #$prml = strapp $prml, "ip=$HDLIC";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   #$prml = strapp $prml, "title=$label";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execgroupmemocal\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=memo>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=calendar>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=groupcontact>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=diaryboard>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=notes>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=contactwebsite>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=calendarwebsite>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=selgroup>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=11>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   parseIt $prml;
   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/mygroups-$biscuit-$$.html";
   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

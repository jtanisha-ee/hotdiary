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
# FileName: managemgcal.cgi
# Purpose: New HotDiary Group Calendar Client
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
use calfuncs::businesscalfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug("managemgcal.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $rh = $input{'rh'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{'os'};
   $hs = $input{'hs'};
   $jp = $input{'jp'};
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

   # bind mgrouptab table vars
   tie %mgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/mgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                 'listed', 'readonly' ] };

   $g = $input{'pgroups'};
   if ($g eq "") {
      status("$login: Please select a calendar.");
      exit;
   }
   if (!exists($mgrouptab{$g}) ) {
      status("$login: This calendar has already been deleted.");
      exit;
   }
   $cname = $mgrouptab{$g}{'groupfounder'};
   $ctype = $mgrouptab{$g}{'ctype'};
   $corg = $mgrouptab{$g}{'corg'};
   $calname = $mgrouptab{$g}{'groupname'};
   $caltitle = $mgrouptab{$g}{'grouptitle'};
   $calpassword = $mgrouptab{$g}{'password'};
   $calrpassword = $mgrouptab{$g}{'password'};
   $cdesc = $mgrouptab{$g}{'groupdesc'};
   $cpublish = $mgrouptab{$g}{'cpublish'};
   $listed = $mgrouptab{$g}{'listed'};
   $readonly = $mgrouptab{$g}{'readonly'};
   if ($cpublish eq "on") {
      $cpublish = "CHECKED";
   }
   if ($listed eq "on") {
      $listed = "CHECKED";
   }
   if ($readonly eq "on") {
      $readonly = "CHECKED";
   }


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';


   if ($input{'delete'} ne "") {
      if ($calname eq "") {
         exit;
      }

      if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab")) {
         system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
         system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
      }
      # bind founded group table vars
      tie %fgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'calpublish', 'corg' ] };

         if ("\L$fgrouptab{$calname}{'groupfounder'}" eq "\L$login") {
         if (exists $fgrouptab{$calname}) {
            tie %usertab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/listed/groups/$calname/usertab",
            SUFIX => '.rec',
            SCHEMA => {
            ORDER => ['login'] };
            #$status = "<DL>";
            foreach $username (keys %usertab) {
               # bind subscribed group table vars
               if (!(-d "$ENV{HDDATA}/groups/$username/subscribed/sgrouptab")) {
                  system "mkdir -p $ENV{HDDATA}/groups/$username/subscribed/sgrouptab";
                  system "chmod 755 $ENV{HDDATA}/groups/$username/subscribed/sgrouptab";
               }
               tie %dsgrouptab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/groups/$username/subscribed/sgrouptab",
               SUFIX => '.rec',
               SCHEMA => {
               ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish' ] };
               delete $dsgrouptab{$calname};
               tied(%dsgrouptab)->sync();
               #$status .= "<LI>$username</LI>";
            }
            #$status .= "</DL>";
            delete $fgrouptab{$calname};
            tied(%fgrouptab)->sync();
            $calname = trim $calname;
            if ($calname ne "") {
               if (-d "$ENV{HTTPHOME}/html/hd/merged/$calname") { 
                   system "rm -f  $ENV{HTTPHOME}/html/hd/merged/$calname/mergedindex.cgi";
                   system "rm -f  $ENV{HTTPHOME}/html/hd/merged/$calname/mergedwebpage.cgi";
                   system "rmdir $ENV{HTTPHOME}/html/hd/merged/$calname";
               }
            }
            delete $mgrouptab{$calname};
            tied(%mgrouptab)->sync();
# safety check!! just in case any other directory is deleted
            if (-d "$ENV{HDDATA}/listed/groups/$calname") {
               $calname = trim $calname;
               if (($calname ne "") && ($ENV{HDDATA} ne "")) {
                  system "/bin/rm -rf $ENV{HDDATA}/listed/groups/$calname";
               }
            }
	    status("$login: You have successfully deleted $calname. Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=mc&jp=$jp\">here</a> to Manage your calendars. <p> Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search.");
	    exit;
         } else {
	    status("$login: You cannot delete this $calname, since you are not it's founder.");
	    exit;
         }
         } else {
              status("$login: The calendar master for $calname does not match your member login $login.");
         }
   }


   $rh  = $input{'rh'};
   $label = "HotDiary";
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
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title; 
            }
          }
       }
   }

   
   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      $cgis = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      if ($rh eq "") {
        $cgis = adjusturl "/cgi-bin/execmgcalclient.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
      } else {
        $cgis = adjusturl "/cgi-bin/$rh/execmgcalclient.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
      }
   }

   

   $prt = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }     
   $prt = strapp $prt, "rh=$rh";
   $prt = strapp $prt, "logo=$logo";
   $prt = strapp $prt, "label=$label";
   $prt = strapp $prt, "contact=$contact";
   $prt = strapp $prt, "template=$ENV{HDTMPL}/hdmgcal.html";
   $mctemp = "$ENV{HDREP}/$alphaindex/$login/mgc-$biscuit-$$.html";
   $prt = strapp $prt, "templateout=$mctemp";
   $prt = strapp $prt, "biscuit=$biscuit";
   $searchcal = adjusturl "$cgi&f=sgc";
   $prt = strapp $prt, "searchcal=$searchcal";
   $createcal = adjusturl "$cgi&f=cpc";
   $prt = strapp $prt, "createcal=$createcal";
   $prt = strapp $prt, "welcome=Welcome";
   $prt = strapp $prt, "vdomain=$vdomain";
   $prt = strapp $prt, "hs=$hs";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prt = strapp $prt, "formenc=$formenc";
   } else {
      $prt = strapp $prt, "formenc=";
   }

   $prt = strapp $prt, "percal=$cgis";
   $prt = strapp $prt, "login=$login";
   $home = adjusturl "$cgis&f=h";
   $prt = strapp $prt, "home=$home";
   $prt = strapp $prt, "rh=$rh";
   $prt = strapp $prt, "jp=$jp";
   if ($ctype eq "") {
      $ctype = "Intranet";
   }
   $prt = strapp $prt, "ctype=$ctype";
   $prt = strapp $prt, "cname=$cname";
   $prt = strapp $prt, "corg=$corg";
   $prt = strapp $prt, "calname=$calname";
   $prt = strapp $prt, "caltitle=$caltitle";
   $prt = strapp $prt, "calpassword=$calpassword";
   $prt = strapp $prt, "calrpassword=$calrpassword";
   $prt = strapp $prt, "cdesc=$cdesc";
   $prt = strapp $prt, "cpublish=$cpublish";
   $prt = strapp $prt, "listed=$listed";
   $prt = strapp $prt, "readonly=$readonly";
   $status = "<p><b>Group Members:</b><BR><BR><DL>";
   # bind subscribed group table vars
   tie %usertab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/listed/groups/$calname/usertab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login' ] };
   foreach $username (sort keys %usertab) {
      $status .= "<LI>$username</LI>";
   }
   $status .= "</DL>";
   $prt = strapp $prt, "status=$status";

   if ($os ne "nt") {
     $execupdatemgcal = encurl "execupdatemgcal.cgi";
   } else {
     $execupdatemgcal = "execupdatemgcal.cgi";
   }

   $loginlist = getmembers($lg);
   $grouplist = adjusturl $grouplist;
   $loginlist = adjusturl $loginlist;

   $prt = strapp $prt, "grouplist=$grouplist";
   $prt = strapp $prt, "loginlist=$loginlist";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execupdatemgcal\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=grouplist>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr5 VALUE=multsel>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=loginlist>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr6 VALUE=loginmultsel>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=cname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=corg>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=calname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=caltitle>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=calpassword>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=calrpassword>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=contact>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=cdesc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=cpublish>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=listed>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=userlogins>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=logins>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=groups>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=20>";

   $hiddenvars = adjusturl $hiddenvars;
   $prt = strapp $prt, "hiddenvars=$hiddenvars";
   parseIt $prt; 

   #system "cat \"$ENV{HDTMPL}/content.html\"";
   #system "/bin/cat $mctemp";
   hdsystemcat "$mctemp";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

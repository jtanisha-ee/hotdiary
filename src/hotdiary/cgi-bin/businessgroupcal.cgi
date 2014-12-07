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
# FileName: businessgroupcal.cgi
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
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
            error("Login is an empty string. This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
            exit;
         }
      }
   }

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

   # bind teamtab table vars
   tie %teamtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['teamname', 'teamtitle', 'teamdesc', 'projcode', 
                'supervisor', 'loccode', 'email', 'pager', 'fax' ] }; 


   $f = $input{f};
   if ($f eq "") {
      $f = "sgc";
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
                           
   $logo = "";
   $partnerlogo = "";

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
                $partnerlogo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
       }
   }




   $pr = "";
   # This is done to prevent an empty title, as it can happen when
   # $ip is not known.
   if ($rh eq "") {
      $cgi = adjusturl "/cgi-bin/execbusinessgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgi = adjusturl "/cgi-bin/$rh/execbusinessgroupcal.cgi?biscuit=$biscuit&jp=$jp";
   }

   $pr = strapp $pr, "label=$label";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   } 
   $pr = strapp $pr, "logo=$logo";
   $pr = strapp $pr, "banner=$banner";
   $pr = strapp $pr, "template=$ENV{HDTMPL}/hdsearchbusinessgroupcal.html";
   $sgctemp = "$ENV{HDREP}/$login/sgc-$biscuit-$$.html";
   $pr = strapp $pr, "templateout=$sgctemp";
   $pr = strapp $pr, "biscuit=$biscuit";
   $createcal = adjusturl "$cgi&f=cpc";
   $pr = strapp $pr, "createcal=$createcal";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $pr = strapp $pr, "formenc=$formenc";
   } else {
      $pr = strapp $pr, "formenc=";
   }
   $pr = strapp $pr, "vdomain=$vdomain";
   $pr = strapp $pr, "hs=$hs";
   $managecal = adjusturl "$cgi&f=mc";
   $pr = strapp $pr, "managecal=$managecal";
   $pr = strapp $pr, "welcome=Welcome";
   $pr = strapp $pr, "login=$login";
   $pr = strapp $pr, "jp=$jp";
   if ($rh eq "") {
       $cgis = adjusturl "/cgi-bin/execbusinesscalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
       $cgis = adjusturl "/cgi-bin/$rh/execbusinesscalclient.cgi?biscuit=$biscuit&jp=$jp";
   }
   $pr = strapp $pr, "percal=$cgis";
   $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   $pr = strapp $pr, "home=$fref";
   if ( ("\L$vdomain" eq "$hotdiary") || ("\L$vdomain" eq "$diary") ) {
      $pr = strapp $pr, "homestr=Home";
   } else {
      $pr = strapp $pr, "homestr=Logout";
   }
   $pr = strapp $pr, "rh=$rh";
   $pr = strapp $pr, "jp=$jp";
   parseIt $pr;

   $prs = "";
    
   if ($partnerlogo ne "") {
      $logo = $partnerlogo;
      $logo = adjusturl "<IMG SRC=\"$logo\">";
   }
   $prs = strapp $prs, "logo=$logo";
   $prs = strapp $prs, "banner=$banner";
   $prs = strapp $prs, "label=$label";
   if ( ($jp ne "") && 
        (-f "$ENV{HDDATA}/$jp/templates/hdcreateprivatecal.html") ) {
       $tmpl = "$ENV{HDDATA}/$jp/templates/hdcreateprivatecal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdcreateprivatecal.html";
   }   
   $prs = strapp $prs, "template=$tmpl";
   $cpctemp = "$ENV{HDREP}/$login/cpc-$biscuit-$$.html";
   $prs = strapp $prs, "templateout=$cpctemp";
   $prs = strapp $prs, "biscuit=$biscuit";
   $searchcal = adjusturl "$cgi&f=sgc";
   $prs = strapp $prs, "searchcal=$searchcal";
   $managecal = adjusturl "$cgi&f=mc";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prs = strapp $prs, "formenc=$formenc";
   } else {
      $prs = strapp $prs, "formenc=";
   }
   $prs = strapp $prs, "managecal=$managecal";
   $prs = strapp $prs, "welcome=Welcome";
   $prs = strapp $prs, "percal=$cgis";
   $prs = strapp $prs, "vdomain=$vdomain";
   $prs = strapp $prs, "hs=$hs";
   $prs = strapp $prs, "login=$login";
   $prs = strapp $prs, "home=$fref";
   if ( ("\L$vdomain" eq "$hotdiary") || ("\L$vdomain" eq "$diary") ) {
      $prs = strapp $prs, "homestr=Home";
   } else {
      $prs = strapp $prs, "homestr=Logout";
   }
   $prs = strapp $prs, "rh=$rh";
   $prs = strapp $prs, "jp=$jp";
   parseIt $prs;
 
   $prt = "";
   $prt = strapp $prt, "label=$label";
   if ($partnerlogo ne "") {
       $logo = $partnerlogo;
       #$logo = adjusturl "<IMG SRC=\"$logo\" WIDTH=\"60\" HEIGHT=\"60\">";
       $logo = adjusturl "<IMG SRC=\"$logo\">";
   }
   $prt = strapp $prt, "logo=$logo";
   $prt = strapp $prt, "banner=$banner";
   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$jp/templates/hdmanagegroupcal.html") ) {
       $tmpl = "$ENV{HDDATA}/$jp/templates/hdmanagegroupcal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdmanagegroupcal.html";
   }   
   $prt = strapp $prt, "template=$tmpl";
   $mctemp = "$ENV{HDREP}/$login/mc-$biscuit-$$.html";
   $prt = strapp $prt, "templateout=$mctemp";
   $prt = strapp $prt, "biscuit=$biscuit";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prt = strapp $prt, "formenc=$formenc";
   } else {
      $prt = strapp $prt, "formenc=";
   }
   $createcal = adjusturl "$cgi&f=cpc";
   $prt = strapp $prt, "createcal=$createcal";
   $searchcal = adjusturl "$cgi";
   $prt = strapp $prt, "searchcal=$searchcal";
   $prt = strapp $prt, "welcome=Welcome";
   $prt = strapp $prt, "percal=$cgis";
   $prt = strapp $prt, "vdomain=$vdomain";
   $prt = strapp $prt, "hs=$hs";
   $prt = strapp $prt, "login=$login";
   $prt = strapp $prt, "home=$fref";
   if ( ("\L$vdomain" eq "$hotdiary") || ("\L$vdomain" eq "$diary") ) {
      $prt = strapp $prt, "homestr=Home";
   } else {
      $prt = strapp $prt, "homestr=Logout";
   }
   $prt = strapp $prt, "status=$input{'status'}";
   $prt = strapp $prt, "rh=$rh";
   $prt = strapp $prt, "jp=$jp";

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';
   if (!(-d "$ENV{HDDATA}/groups/$alph/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alph/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alph/$login/founded/fgrouptab";
   }
   tie %fgrouptab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/groups/$alph/$login/founded/fgrouptab",
       SUFIX => '.rec',
       SCHEMA => {
          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   (@group) =  sort keys %fgrouptab;
   if (($f eq "mc") && ($#group == -1)) {
      status("$login: You have not created any calendars or groups. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=cpc&jp=$jp&os=$os\">here</a> to create a calendar. <p>When you create a calendar, you automatically become the calendar master for that calendar. As a calendar master you can then manage that calendar. <p> Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp\">here</a> to Search.");
      exit;
   } 
   foreach $group (sort keys %fgrouptab) {
      $sel = $sel . "\<OPTION\>$fgrouptab{$group}{'groupname'}\<\/OPTION\>";
   }
   $prt = strapp $prt, "pgroups=$sel";
   parseIt $prt; 


   system "cat \"$ENV{HDTMPL}/content.html\"";
   if ($f eq "sgc") {
      system "/bin/cat $sgctemp";
   }
   if ($f eq "cpc") {
      system "/bin/cat $cpctemp";
   }
   if ($f eq "mc") {
      system "/bin/cat $mctemp";
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

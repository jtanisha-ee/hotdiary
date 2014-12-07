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
# FileName: groupcal.cgi
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
   $SESSION_TIMEOUT = 3600;

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");
   hddebug "entered groupcal.cgi";

   $vdomain = trim $input{'vdomain'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
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

   $alpha = substr $jp, 0, 1;
   $alpha = $alpha . '-index';
   


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

   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'readonly' ] };

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

   $HDLIC = $input{'HDLIC'};
   $ip = $HDLIC;


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
                $logo = $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
       }

   hddebug "jp = $jp";
   hddebug "HDLIC = $HDLIC";

   if ($os ne "nt") {
      $execmygroups = encurl "execmygroups.cgi";
      $execmergedgroups = encurl "execmergedgroups.cgi";
      $execgroupcal = encurl "execgroupcal.cgi";
   } else {
      $execmygroups = "execmygroups.cgi";
      $execmergedgroups = "execmergedgroups.cgi";
      $execgroupcal = "execgroupcal.cgi";
   }

   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;
   
   $mygroups = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmygroups&p1=biscuit&p2=jp&pnum=3&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   $mergedgroups = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&pnum=3&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   $groupcal = "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execgroupcal&p1=biscuit&p2=f&p3=jp&pnum=4&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";


   if ($logo ne "") {
      $logo = adjusturl $logo;
   } 

   $pr = "";
   # This is done to prevent an empty title, as it can happen when

   ##if ($rh eq "") {
    ##  $cgi = adjusturl "http://$vdomain/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&vdomain=$vdomain&HDLIC=$ip";
   ##} else {
    ##  $cgi = adjusturl "http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&vdomain=$vdomain&HDLIC=$ip";
   ##}

   $pr = strapp $pr, "label=$label";
   $pr = strapp $pr, "logo=$logo";
   $pr = strapp $pr, "banner=$banner";

   if ( ($jp ne "") && 
        (-f "$ENV{HDDATA}/$alpha/$jp/templates/hdsearchgroupcal.html")){
       $tmpl = "$ENV{HDDATA}/$alpha/$jp/templates/hdsearchgroupcal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdsearchgroupcal.html";
   }

   $lalpha = substr $login, 0, 1;
   $lalpha = $lalpha . '-index';
 
   $pr = strapp $pr, "template=$tmpl";
   $sgctemp = "$ENV{HDREP}/$lalpha/$login/sgc-$biscuit-$$.html";
   $pr = strapp $pr, "templateout=$sgctemp";
   $pr = strapp $pr, "biscuit=$biscuit";

   $createcal = adjusturl "$groupcal&f=cpc";
   $pr = strapp $pr, "createcal=$createcal";

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $pr = strapp $pr, "formenc=$formenc";
   } else {
      $pr = strapp $pr, "formenc=";
   }
   $pr = strapp $pr, "vdomain=$vdomain";
   $pr = strapp $pr, "hs=$hs";

   $managecal = adjusturl "$groupcal&f=mc";
   $pr = strapp $pr, "managecal=$managecal";

   $pr = strapp $pr, "welcome=Welcome";
   $pr = strapp $pr, "login=$login";
   $pr = strapp $pr, "jp=$jp";
   $pr = strapp $pr, "HDLIC=$HDLIC";

   if ($rh eq "") {
       $cgis = adjusturl "http://$vdomain/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
       $cgis = adjusturl "http://$vdomain/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   }

   $pr = strapp $pr, "percal=$cgis";
   if (-f "$ENV{HDREP}/$lalpha/$login/topcal.html") {
      $fref = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }
   $pr = strapp $pr, "home=$fref";
   $pr = strapp $pr, "homestr=Home";
   $pr = strapp $pr, "rh=$rh";
   $pr = strapp $pr, "jp=$jp";

   #if (($login eq "smitha") || ($login eq "mjoshi") ) {
      $pr = strapp $pr, "mergedgroups=$mergedgroups";
      $pr = strapp $pr, "mergedgroupstxt=Merged Calendars";
   #} else {
   #   $pr = strapp $pr, "mergedgroups=";
   #   $pr = strapp $pr, "mergedgroupstxt=";
   #}

   if ( ("1800calendar.com" eq "\L$vdomain") ||  ("www.1800calendar.com" eq "\L$vdomain") || (validvdomain($vdomain) eq "1") ) {
      $pr = strapp $pr, "mygroups=$mygroups";
      $pr = strapp $pr, "mygrouptxt=My Groups";
   } else {
      $pr = strapp $pr, "mygroups=";
      $pr = strapp $pr, "mygrouptxt=";
   }
   $pr = strapp $pr, "hiddenvars=$hiddenvars";
   parseIt $pr;

   $prs = "";
   $prs = strapp $prs, "logo=$logo";
   $prs = strapp $prs, "banner=$banner";
   $prs = strapp $prs, "label=$label";
   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alpha/$jp/templates/hdcreateprivatecal.html")){
       $tmpl = "$ENV{HDDATA}/$alpha/$jp/templates/hdcreateprivatecal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdcreateprivatecal.html";
   }   
   $prs = strapp $prs, "template=$tmpl";
   $cpctemp = "$ENV{HDREP}/$lalpha/$login/cpc-$biscuit-$$.html";
   $prs = strapp $prs, "templateout=$cpctemp";
   $prs = strapp $prs, "biscuit=$biscuit";

   $searchcal = adjusturl "$groupcal&f=sgc";
   $prs = strapp $prs, "searchcal=$searchcal";

   $managecal =  adjusturl "$groupcal&f=mc";
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
   $prs = strapp $prs, "homestr=Home";
   $prs = strapp $prs, "rh=$rh";
   $prs = strapp $prs, "jp=$jp";


   if ( ("1800calendar.com" eq "\L$vdomain") ||  ("www.1800calendar.com" eq "\L$vdomain") || (validvdomain($vdomain) eq "1") ) {
      $prs = strapp $prs, "mygroups=$mygroups";
      $prs = strapp $prs, "mygrouptxt=My Groups";
   } else {
      $prs = strapp $prs, "mygroups=";
      $prs = strapp $prs, "mygrouptxt=";
   }

   $prs = strapp $prs, "mergedgroups=$mergedgroups";
   $prs = strapp $prs, "mergedgroupstxt=Merged Calendars";
   $prs = strapp $prs, "hiddenvars=$hiddenvars";
   parseIt $prs;
 
   $prt = "";
   $prt = strapp $prt, "label=$label";
   $prt = strapp $prt, "logo=$logo";
   $prt = strapp $prt, "banner=$banner";

   if ( ($jp ne "") && 
        (-f "$ENV{HDDATA}/$alpha/$jp/templates/hdmanagegroupcal.html") ) {
       $tmpl = "$ENV{HDDATA}/$alpha/$jp/templates/hdmanagegroupcal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdmanagegroupcal.html";
   }   

   $prt = strapp $prt, "template=$tmpl";
   $mctemp = "$ENV{HDREP}/$lalpha/$login/mc-$biscuit-$$.html";
   $prt = strapp $prt, "templateout=$mctemp";
   $prt = strapp $prt, "biscuit=$biscuit";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prt = strapp $prt, "formenc=$formenc";
   } else {
      $prt = strapp $prt, "formenc=";
   }
   $createcal = adjusturl "$groupcal&f=cpc";
   $prt = strapp $prt, "createcal=$createcal";

   $searchcal = adjusturl $groupcal;
   $prt = strapp $prt, "searchcal=$searchcal";

   $prt = strapp $prt, "welcome=Welcome";
   $prt = strapp $prt, "percal=$cgis";
   $prt = strapp $prt, "vdomain=$vdomain";
   $prt = strapp $prt, "hs=$hs";
   $prt = strapp $prt, "login=$login";
   $prt = strapp $prt, "home=$fref";
   $prt = strapp $prt, "homestr=Home";
   $prt = strapp $prt, "status=$input{'status'}";
   $prt = strapp $prt, "rh=$rh";
   $prt = strapp $prt, "jp=$jp";
   $prt = strapp $prt, "biscuit=$biscuit";
   $prt = strapp $prt, "HDLIC=$HDLIC";
   $prt = strapp $prt, "hiddenvars=$hiddenvars";

   if (! -d "$ENV{HDDATA}/groups/$lalpha/$login/founded/fgrouptab") {
      system "mkdir -p $ENV{HDDATA}/groups/$lalpha/$login/founded/fgrouptab";
      system "chmod -R 775 $ENV{HDDATA}/groups/$lalpha/$login/founded";
   }
   tie %fgrouptab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/groups/$lalpha/$login/founded/fgrouptab",
       SUFIX => '.rec',
       SCHEMA => {
          ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   (@group) =  sort keys %fgrouptab;
   if (($f eq "mc") && ($#group == -1)) {
      status("$login: You have not created any groups. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=cpc&jp=$jp&os=$os\">here</a> to create a group. <p>When you create a group, you automatically become the group master for that group. As a group master you can then manage that group. <p> Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp\">here</a> to Search.");
      exit;
   } 
   foreach $group (sort keys %fgrouptab) {
      $sel = $sel . "\<OPTION\>$fgrouptab{$group}{'groupname'}\<\/OPTION\>";
   }
   $prt = strapp $prt, "pgroups=$sel";

   if ( ("1800calendar.com" eq "\L$vdomain") ||  ("www.1800calendar.com" eq "\L$vdomain") || (validvdomain($vdomain) eq "1" ) ) {
      $prt = strapp $prt, "mygroups=$mygroups";
      $prt = strapp $prt, "mygrouptxt=My Groups";
   } else {
     $prt = strapp $prt, "mygroups=";
     $prt = strapp $prt, "mygrouptxt=";
   }

   $prt = strapp $prt, "mergedgroups=$mergedgroups";
   $prt = strapp $prt, "mergedgroupstxt=Merged Calendars";
   $prt = strapp $prt, "HDLIC=$HDLIC";
   $prt = strapp $prt, "hiddenvars=$hiddenvars";
   parseIt $prt; 


   #system "cat \"$ENV{HDTMPL}/content.html\"";
   if ($f eq "sgc") {
      #system "/bin/cat $sgctemp";
      hdsystemcat "$sgctemp";
   }
   if ($f eq "cpc") {
      #system "/bin/cat $cpctemp";
      hdsystemcat "$cpctemp";
   }
   if ($f eq "mc") {
      #system "/bin/cat $mctemp";
      hdsystemcat "$mctemp";
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

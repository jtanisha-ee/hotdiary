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
# FileName: mergedgroups.cgi
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
#use calfuncs::calfuncs;   
use calfuncs::businesscalfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "mergedgroups.cgi";

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   $hdcookie = $ENV{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   hddebug "jp = $jp";
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

   $f = $input{f};
   hddebug "f = $f";
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

       if (exists $jivetab{$jp}) {
          $logo = adjusturl $jivetab{$jp}{logo};
          $title = $jivetab{$jp}{title};
          $banner = $jivetab{$jp}{banner};
          $label = $title;
       } else {
          if (exists $lictab{$HDLIC}) {
             $partner = $lictab{$HDLIC}{partner};
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
       }

   if ($logo ne "") {
     $logo = adjusturl $logo;
   }

   if ($os ne "nt") {
      $execmygroups = encurl "execmygroups.cgi";
      $execmergedgroups = encurl "execmergedgroups.cgi";
      $execsearchmergedcal = encurl "execsearchmergedcal.cgi";
      $execcreatemergedcal = encurl "execcreatemergedcal.cgi";
      $execmanagemergedcal = encurl "execmanagemergedcal.cgi";
   } else {
      $execmygroups = "execmygroups.cgi";
      $execmergedgroups = "execmergedgroups.cgi";
      $execsearchmergedcal = "execsearchmergedcal.cgi";
      $execcreatemergedcal = "execcreatemergedcal.cgi";
      $execmanagemergedcal = "execmanagemergedcal.cgi";
   }


   $mygroups = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execmygroups&p1=biscuit&p2=jp&pnum=3&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";

   $mergedgroups = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";


   $cgi = $mergedgroups;

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
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   
   $memotype = "";
   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist < 0) && ($#glist1 < 0) ) {
      $grouplabel = adjusturl "<FONT FACE=Verdana SIZE=1>Groups Not Created Or Subscribed</FONT>";
   } else {
      $grouplabel = adjusturl "<B>Groups Created or Subscribed</B><BR>";
      foreach $grp (keys %fgrouptab) {
         $memotype .= "<OPTION>$grp";
      }
      foreach $grp (keys %sgrouptab) {
         $memotype .= "<OPTION>$grp";
      }
      $memotype = adjusturl $memotype;
   }

   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $fref = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";
   } else {
      $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }

   $loginlist = adjusturl getmembers($login);

   if ($f eq "sgc") {

      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execsearchmergedcal>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=calkey>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=f>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>"; 
      $hiddenvars = gethiddenvars($hiddenvars);
      $hiddenvars = adjusturl $hiddenvars;

      # This is done to prevent an empty title, as it can happen when
      #list of variables 

      $pr = "";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "logo=$logo";
      $pr = strapp $pr, "banner=$banner";
      if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdsearchmergedcal.html") ) {
         $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdsearchmergedcal.html";
      } else {
         $tmpl = "$ENV{HDTMPL}/hdsearchmergedcal.html";
      }

      $pr = strapp $pr, "template=$tmpl";
      $sgctemp = "$ENV{HDHREP}/$alphaindex/$login/sgc-$biscuit-$$.html";
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
          $cgis = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
      } else {
          $cgis = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
      }
      $pr = strapp $pr, "percal=$cgis";
      $pr = strapp $pr, "home=$fref";
      $pr = strapp $pr, "homestr=Home";
      $pr = strapp $pr, "rh=$rh";
      $pr = strapp $pr, "jp=$jp";

      if (($login eq "smitha") || ($login eq "mjoshi") ) {
         $pr = strapp $pr, "mergedgroups=$mergedgroups";
         $pr = strapp $pr, "mergedgroupstxt=Merged Calendars";
      } else {
         $pr = strapp $pr, "mergedgroups=";
         $pr = strapp $pr, "mergedgroupstxt=";
      }

      if ( ("1800calendar.com" eq "\L$vdomain") ||  ("www.1800calendar.com" eq "\L$vdomain") || (validvdomain($vdomain) eq "1") ) {
        $pr = strapp $pr, "mygroups=$mygroups";
        $pr = strapp $pr, "mygrouptxt=My Groups";
      } else {
        $pr = strapp $pr, "mygroups=";
        $pr = strapp $pr, "mygrouptxt=";
      }

      $pr = strapp $pr, "hiddenvars=$hiddenvars";
      $pr = strapp $pr, "label2=";
      parseIt $pr;
   }

   if ($f eq "cpc") {
      $hiddenvars = "";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=17>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execcreatemergedcal>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=userlogins>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=listed>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=grouplist>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr5 VALUE=multsel>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=loginlist>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr6 VALUE=multsel>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=cname>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=corg>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=calname>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=caltitle>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=calpassword>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=calrpassword>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=contact>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=cdesc>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=cpublish>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=f>"; 
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
      $hiddenvars = gethiddenvars($hiddenvars);
      $hiddenvars = adjusturl $hiddenvars;

      $prs = "";
      $prs = strapp $prs, "hiddenvars=$hiddenvars";
      $prs = strapp $prs, "logo=$logo";
      $prs = strapp $prs, "banner=$banner";
      $prs = strapp $prs, "label=$label";

      if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdcreatemergedcal.html") ) {
          $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdcreatemergedcal.html";
      } else {
          $tmpl = "$ENV{HDTMPL}/hdcreatemergedcal.html";
      }

      $prs = strapp $prs, "template=$tmpl";
      $cpctemp = "$ENV{HDHREP}/$alphaindex/$login/cpc-$biscuit-$$.html";
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
      $prs = strapp $prs, "homestr=Home";
      $prs = strapp $prs, "rh=$rh";
      $prs = strapp $prs, "jp=$jp";
      $prs = strapp $prs, "mygroups=$mygroups";
      $prs = strapp $prs, "mygrouptxt=My Groups";
      $prs = strapp $prs, "mergedgroups=";
      $prs = strapp $prs, "mergedgroupstxt=";
      $prs = strapp $prs, "grouplabel=$grouplabel";
      $prs = strapp $prs, "grouplist=$memotype";
      $prs = strapp $prs, "label2=";
      parseIt $prs;
   }

   if ($f eq "mc") {
     $hiddenvars = "";
     $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=7>"; 
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execmanagemergedcal>"; 
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=grouplist>";
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr3 VALUE=multsel>";
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=f>"; 
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=manage>"; 
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=delete>"; 
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
     $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";

     $hiddenvars = gethiddenvars($hiddenvars);
     $hiddenvars = adjusturl $hiddenvars;

     $prt = "";
     $prt = strapp $prt, "label=$label";
     $prt = strapp $prt, "hiddenvars=$hiddenvars";
     $prt = strapp $prt, "logo=$logo";
     $prt = strapp $prt, "banner=$banner";

     if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/managemergedcal.html") ) {
         $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/managemergedcal.html";
     } else {
         $tmpl = "$ENV{HDTMPL}/managemergedcal.html";
     }

     $prt = strapp $prt, "template=$tmpl";
     $mctemp = "$ENV{HDHREP}/$alphaindex/$login/mc-$biscuit-$$.html";
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
     $searchcal = adjusturl "$cgi&f=sgc";
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
     $prt = strapp $prt, "mygroups=$mygroups";
     $prt = strapp $prt, "mygrouptxt=My Groups";
     $prt = strapp $prt, "mergedgroups=";
     $prt = strapp $prt, "mergedgroupstxt=";
  
     system "mkdir -p $ENV{HDDATA}/merged/$login/subscribed/smergetab"; 
     system "chmod 755 $ENV{HDDATA}/merged/$login/subscribed/smergetab"; 

     system "mkdir -p $ENV{HDDATA}/merged/$login/founded/fmergetab"; 
     system "chmod 755 $ENV{HDDATA}/merged/$login/founded/fmergetab"; 


     # bind smergetab table vars
     tie %smergetab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/merged/$login/subscribed/smergetab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
            'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };

     # bind founded group table vars
     tie %fmergetab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/merged/$login/founded/fmergetab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
               'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };  

     $memotype = "";
     (@glist) = keys %fmergetab;
     (@glist1) = keys %smergetab;
     if ( ($#glist < 0) && ($#glist1 < 0) ) {
        $grouplabel = adjusturl "<FONT FACE=Verdana SIZE=1>Merged Calendars Not Created Or Subscribed</FONT>";
     } else {
        $grouplabel = adjusturl "<B>Merged Calendars Created or Subscribed</B><BR>";
        foreach $grp (keys %fmergetab) {
           $memotype .= "<OPTION>$grp";
        }
        foreach $grp (keys %smergetab) {
           $memotype .= "<OPTION>$grp";
        }
        $memotype = adjusturl $memotype;
     }
 
     $prt = strapp $prt, "grouplist=$memotype";
     $prt = strapp $prt, "grouplabel=$grouplabel";
     $prt = strapp $prt, "label2=";
     parseIt $prt; 
   }

   #hddebug "f = $f";
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

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
# FileName: calpublish.cgi
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
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   hddebug("calpublish.cgi");

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   }

   $hs = $input{'hs'}; 
   $jp = $input{'jp'}; 
   $os = $input{'os'}; 
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
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

   if (!(-d "$ENV{HDDATA}/groups/$login/subscribed/sgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
   }

   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   if (!(-d "$ENV{HDDATA}/groups/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$login/founded/fgrouptab";
   }
   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


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


   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist > 0) || ($#glist1 > 0) ) {

      $glist = "<BR><B>Group Calendars Published Options</B><BR><TABLE CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\" BORDER=1>";
      $glist .= "<TR><TD ALIGN=CENTER><FONT FACE=\"Verdana\" SIZE=\"2\"><B>Group Publishing Option</B></FONT></TD><TD><FONT FACE=\"Verdana\" SIZE=\"2\"><B>Publish</B></FONT></TD><TD ALIGN=CENTER><FONT FACE=\"Verdana\" SIZE=\"2\"><B>Group Website</B></FONT></TD></TR>";
      $glist .= "<TR><TD WIDTH=\"100%\" ALIGN=CENTER><B>Founded Groups</B></TD></TR>";
      foreach $grp (keys %fgrouptab) {
         $glist .= "<TR><TD>$grp Publish</TD>";
	 $checked = "";
         if (exists $sgrouptab{$grp}) {
	    if ($fgrouptab{$grp}{cpublish} eq "on") {
	       $checked = "CHECKED";
	    }
	 }
         $glist .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$grp $checked></FONT></TD>";
	 if ($rh ne "") {
	    $website = "http://$vdomain/$rh/groups/$grp";
         }  else {
	    $website = "http://$vdomain/$rh/groups/$grp";
         }
         $glist .= "<TD>$website</TD></TR>";
         $cdir .= "$grp ";
      }

      $glist .= "<BR><BR><TR><TD WIDTH=\"100%\" ALIGN=CENTER><B>Subscribed Groups</B></TD><TD>&nbsp;</TD><TD>&nbsp;</TD></TR>";
      foreach $grp (keys %sgrouptab) {
         $glist .= "<TR><TD>$grp</TD>";
	 if ($rh ne "") {
	    $website = "http://$vdomain/$rh/groups/$grp";
         }  else {
	    $website = "http://$vdomain/$rh/groups/$grp";
         }
	 $checked = "";

         if (exists $sgrouptab{$grp}) {
	    if ($sgrouptab{$grp}{cpublish} eq "on") {
	       $checked = "CHECKED";
	    }
	 }
         $glist .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$grp $checked></FONT></TD>";
         $glist .= "<TD>$website</TD></TR>";
         $cdir .= "$grp ";
      }
      $glist .= "</TABLE>";
      $glist = adjusturl $glist;
   }
    
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   (@hshcdir) = split " ", $cdir;
       

   $prml = "";
   $prml = strapp $prml, "glist=$glist";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execsavecalpublish = encurl "execsavecalpublish.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execsavecalpublish =  "execsavecalpublish.cgi";
   }

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$jp/templates/calpublish.html") ) {
       $tmpl = "$ENV{HDDATA}/$jp/templates/calpublish.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/calpublish.html";
   }

   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/calpublish-$biscuit-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "home=$home";
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
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "title=$label";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavecalpublish\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";

   #values of checkboxes as each parameter
   $k = 0;
   $mcntr = 3;
   $numend = $mcntr;
   $numbegin = $mcntr;

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

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";

   $hiddenvars = adjusturl $hiddenvars;
   $prml = strapp $prml, "hiddenvars=$hiddenvars";
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html";
   #system "/bin/cat $ENV{HDHREP}/$login/calpublish-$biscuit-$$.html";
   hdsystemcat "$ENV{HDHREP}/$login/calpublish-$biscuit-$$.html";
   
   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

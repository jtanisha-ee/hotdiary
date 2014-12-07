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
# FileName: notes.cgi
# Purpose: Top screen for notes
# Creation Date: 03-04-2000
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

   hddebug ("notes.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
   $rh = $input{rh};
   $g = $input{g};
   $show = $input{show};
   if ($os ne "nt") {
      $execnotes = encurl "execnotes.cgi";
   } else {
      $execnotes = "execnotes.cgi";
   }

   $sortby = $input{sortby};

   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                 'listed' ] };

   $notesprog = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execnotes&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\">here</FONT></a>";
   if ( ( $g ne "") && (!exists $lgrouptab{$g}) ) {
      status "Group name ($g) does not exist. Please select a valid group name.
Click $notesprog to return to Diary Pad.";
      exit;
   }


   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
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
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
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

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();

   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }


   tie %parttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/partners/parttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['logo', 'title', 'banner'] };

 
   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $fchar = substr $login, 0, 1;
   $alphaindex = $fchar . '-index';

   if (! -d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab") {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
   }

   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
        'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   if (! -d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab") {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
   }

  # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
        'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   if ( ($g ne "") && (!exists $sgrouptab{$g}) && (!exists $fgrouptab{$g}) ) {
      status "You are neither the founder nor the subscriber of the group $g. Please check the group name and try again. Click $memoprog to return to Memo Manager.";
      exit;
   }



   $prml = "";
   if ($logo ne "") {
      $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "logo=$logo";
   $sc = $input{sc};

   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execeditnotes =  encurl "execeditnotes.cgi";
      $execaddnotes =  encurl "execaddnotes.cgi";
      $execdeletenotes =  encurl "execdeletenotes.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execeditnotes =  "execeditnotes.cgi";
      $execaddnotes =  "execaddnotes.cgi";
      $execdeletenotes =  "execdeletenotes.cgi";
   }

   if ($g eq "") {
      if (! -d "$ENV{HDDATA}/$alphaindex/$login/notestab") {
         system "mkdir -p $ENV{HDDATA}/$alphaindex/$login/notestab";
         system "chmod 755 $ENV{HDDATA}/$alphaindex/$login/notestab";
      }
      # bind todo table vars
         tie %notestab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/notestab",
         SUFIX => '.rec',
         SCHEMA => {
              ORDER => ['entryno', 'login', 'subject', 'desc'] };
   } else {
      if (! -d "$ENV{HDDATA}/listed/groups/$g/notestab") {
         system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$g/notestab";
      }
      # bind group appt table vars
      tie %notestab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/notestab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };
   }

   $jpchar = substr $jp, 0, 1;
   $jpalphaindex = $jpchar . "-index";
 
   if (($jp ne "") && (-f "$ENV{HDDATA}/$jpalphaindex/$jp/templates/notes.html") ) {
      $tmpl = "$ENV{HDDATA}/$jpalphaindex/$jp/templates/notes.html";
   } else {
      $tmpl = "$ENV{HDTMPL}/notes.html";
   }   

   $prml = strapp $prml, "template=$tmpl";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/notes-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execaddnotes=$execaddnotes";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "label1=Diary Pad";
   $prml = strapp $prml, "title=$label";
   $prml = strapp $prml, "g=$g";

   #if ($login eq "mjoshi") {
   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist < 0) && ($#glist1 < 0) ) {
      $lab100 = adjusturl "<BR>Group Pad<BR><FONT FACE=Verdana SIZE=1>Groups Not Created Or Subscribed</FONT>";
      $prml = strapp $prml, "notetype=$lab100";
   } else {
         $notetype = "<BR><CENTER>Group Pad <TABLE CELLPADDING=0 CELLSPACING=0 WIDTH=\"20%\" BORDER=0>";
         $notetype .= "<TR ALIGN=CENTER><TD>";
         $notetype .= "<FONT FACE=Verdana SIZE=2><SELECT NAME=selgroup SIZE=3>";
         foreach $grp (keys %fgrouptab) {
            $notetype .= "<OPTION>$grp";
         }
         foreach $grp (keys %sgrouptab) {
            $notetype .= "<OPTION>$grp";
         }
         $notetype .= "</SELECT></FONT>";
         $notetype .= "</TD>";
         $notetype .= "<TD>";
         $notetype .= "<INPUT TYPE=SUBMIT NAME=Go VALUE=Go>";
         $notetype .= "</TD></TR></TABLE></CENTER>";
         $notetype = adjusturl $notetype;
         $prml = strapp $prml, "notetype=$notetype";
   }
   #}
   

   $noteslist = "";
   if ($g eq "") {
         $notestitle = "<h3>Diary Pad Blog Tool</h3>";
   } else {
         $notestitle = "<h3>Group Pad ($g) Blog Tool </h3>";
   }

   $noteslist .= "<CENTER>$notestitle</CENTER> <TABLE WIDTH=\"100%\" BORDERCOLOR=ee00ee CELLPADDING=5 CELLSPACING=0 BORDER=1>";

   if (-d "$ENV{HDDATA}/$alphaindex/$login/notestab") {
      hddebug "exists";
      $noteslist .= "<TR BGCOLOR=1f1f7f WIDTH=\"100%\">";
      $noteslist .= "<TD WIDTH=\"5%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Sel</FONT></TD>";
      $noteslist .= "<TD WIDTH=\"20%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=ffffff SIZE=2>Title</FONT></TD>";
      $noteslist .= "<TD WIDTH=\"50%\" ALIGN=CENTER><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\"  COLOR=ffffff SIZE=2>Description</FONT></TD>";
      $noteslist .= "</TR>";

      $cdir = "";
      foreach $item (sort keys %notestab) {
         #$noteslist .= "<TR BACKGROUND=\"http://www.hotdiary.com/images/pad.gif\" WIDTH=\"100%\">";
         $noteslist .= "<TR WIDTH=\"100%\">";
         $entry = $notestab{$item}{entryno};
         hddebug "entry = $entry";
         $noteslist .= "<TD WIDTH=\"5%\" ALIGN=CENTER VALIGN=TOP><INPUT TYPE=CHECKBOX NAME=$entry></TD>";
         $cdir .= $entry;
         $cdir .= " ";
         
         $subject = $notestab{$item}{subject};
         #hddebug "subject = $subject";
         $subjecturl = adjusturl "execdogeneric.cgi?pnum=5&p0=$execeditnotes&p1=biscuit&p2=entry&p3=jp&p4=g&g=$g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&entry=$entry&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&jp=$jp";
         $noteslist .= "<TD WIDTH=\"20%\" ALIGN=CENTER VALIGN=TOP><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" COLOR=1029ff SIZE=2><a href=\"http://$vdomain/cgi-bin/$rh/$subjecturl\">$subject</a>&nbsp;</FONT></TD>";
         $desc = $notestab{$item}{desc};
         #hddebug "desc = $desc";
         $noteslist .= "<TD WIDTH=\"60%\" VALIGN=TOP><FONT FACE=\"Tahoma, Arial, Helvetica, sans-serif\" SIZE=2>$desc &nbsp;</FONT></TD>";
      }
      $noteslist .= "</TABLE>";
      $noteslist = adjusturl $noteslist;
   }

   (@hshcdir) = split " ", $cdir;
   $noteslist =~ s/\n/<BR>/g;
   $prml = strapp $prml, "noteslist=$noteslist";
   if ($g ne "") {
      $pnotes = adjusturl "&nbsp;&nbsp;<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execnotes&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">Go To Personal Memo</a>";
      $prml = strapp $prml, "pnotes=$pnotes";
   } else {
      $prml = strapp $prml, "pnotes=";
   }
   #if ($login ne "mjoshi") {
   #   $prml = strapp $prml, "pnotes=";
   #   $prml = strapp $prml, "notetype=";
   #}


   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execdeletenotes\">";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=Delete>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=Go>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=selgroup>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=group>";

   #values of checkboxes as each parameter
   $k = 0;
   $mcntr = 9;
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
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=group VALUE=$g>";
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

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/notes.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/notes-$$.html";

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

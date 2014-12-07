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
# FileName: groupmemocal.cgi
# Purpose:  Display group bullentinboard, contacts, diarychat, memo, calendar  
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

   hddebug ("groupmemocal.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
 
   $jp = $input{jp}; 
   hddebug "jp = $jp";
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   $rh = $input{rh};
   $os = $input{os}; 
   $hs = $input{'hs'};
   $grp = $input{selgroup};
   hddebug "group = $grp";
   $biscuit = $input{'biscuit'};

   if ($os ne "nt") {
      $execmygroups = encurl "execmygroups.cgi";
      $execgroupcal = encurl "execgroupcal.cgi";
   } else {
      $execmygroups =  "execmygroups.cgi";
      $execgroupcal = "execgroupcal.cgi";
   }

   $mygroups = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmygroups&p1=biscuit&p2=jp&pnum=3&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a>";

   if ($grp eq "" ) {
       status("Please select a group. Click $mygroups to select a group.");
       exit;
   }
   
   $calendar = $input{calendar};
   $memo = $input{memo};
   $groupcontact = $input{groupcontact};
   $diaryboard = $input{diaryboard};
   $notes = $input{notes};
   $calendarwebsite = $input{calendarwebsite};
   $contactwebsite = $input{contactwebsite};

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };


   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed' ] };

   if ( ($contactwebsite ne "" ) || ($calendarwebsite ne "") ) {
      if ($lgrouptab{$grp}{'cpublish'} ne "on") {
         if ($lgrouptab{$grp}{'groupfounder'} eq $login) {
             $managegroups = adjusturl "<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execgroupcal&p1=biscuit&p2=f&p3=jp&p4=g&pnum=5&biscuit=$biscuit&g=$grp&jp=$jp&f=mc&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">Manage</a>";
             status("Your \"$grp\" website is not published. You have to enable Publish Calendar/Contacts to create a group website. Click $managegroups to publish $grp website. Click $mygroups to select a group.");
             exit;
         } else {
             status("This \"$grp\" website is not published. Your groupfounder has not published this group's calendar or croup contacts. Click $mygroups to select a group.");
             exit;
         }
       }
   }

   if ($calendarwebsite ne "") {
      $groupwebsite = adjusturl "http://$vdomain/groups/$grp";
   } else {
      if ($contactwebsite ne "") {
         if (!(-d "$ENV{HTTPHOME}/html/hd/contacts/$grp"))  {
           system "mkdir -p $ENV{HTTPHOME}/html/hd/contacts/$grp";
        }
        if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$grp/index.cgi")) {
            system "ln -s $ENV{HDCGI}/contacts/index.cgi $ENV{HTTPHOME}/html/hd/contacts/$grp";
        }
        if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$grp/webpage.cgi")) {
            system "ln -s $ENV{HDCGI}/contacts/webpage.cgi $ENV{HTTPHOME}/html/hd/contacts/$grp";
        }
        $groupwebsite= adjusturl "http://$vdomain/contacts/$grp";
      }
   }

   if ( ($contactwebsite ne "" ) || ($calendarwebsite ne "") ) {
      if ($groupwebsite ne "") {
         hddebug "groupwebsite = $groupwebsite";
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/groupwebsite-redirect_url.html";
         $prml = strapp $prml, "redirecturl=$groupwebsite";
         parseIt $prml;
         hdsystemcat "$ENV{HDHREP}/$alpha/$login/groupwebsite-redirect_url.html"; 
         exit;
      } else {
         status("Click $mygroups to select a group.");
         exit;
      }
   }
                                                                              
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

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $sc = $input{sc};

   if ($os ne "nt") {
      $execmemo =  encurl "execmemo.cgi";
      $execgroupcontact =  encurl "execgroupcontact.cgi";
      $execdiaryboard = encurl "execdiaryboard.cgi";
      $execnotes = encurl "execnotes.cgi";
   } else {
      $execmemo =  "execmemo.cgi";
      $execgroupcontact =  "execgroupcontact.cgi";
      $execnotes = "execnotes.cgi";
   }


   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;

   if ($memo ne "") {
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/memo-redirect_url.html";
      $memoprog = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$grp&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      #$memoprog = "http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&p3=show&p4=sortby&p5=g&pnum=6&g=$grp&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&show=all&sortby=$sortby&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      $prml = strapp $prml, "redirecturl=$memoprog";
      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "logo=$logo";
      parseIt $prml;
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/memo-redirect_url.html";
      #print "Location: $memoprog\n\n";
      exit;
   }

   if ($groupcontact ne "") {
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/groupcontact-redirect_url.html";
      $contactprg = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execgroupcontact&p1=biscuit&p2=jp&p3=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&g=$grp&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      $prml = strapp $prml, "redirecturl=$contactprg";
      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "logo=$logo";
      parseIt $prml;
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/groupcontact-redirect_url.html";
      exit;
   }

   if ($diaryboard ne "") {
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/g-diaryboard-redirect_url.html";
      $diaryboardprg = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execdiaryboard&p1=biscuit&p2=jp&p3=selgroup&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&selgroup=$grp&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      $prml = strapp $prml, "redirecturl=$diaryboardprg";
      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "logo=$logo";
      parseIt $prml;
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/g-diaryboard-redirect_url.html";
      exit;
  }

   if ($notes ne "") {
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/gnotes-redirect_url.html";
      $notesprg = adjusturl "http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execnotes&p1=biscuit&p2=jp&p3=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&g=$grp&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
      $prml = strapp $prml, "redirecturl=$notesprg";
      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "logo=$logo";
      parseIt $prml;
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/gnotes-redirect_url.html";
      exit;
  }

   if ($input{'calendar'} ne "") {
      if ($biscuit eq "") {
         if ($hs eq "") {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         } else {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         }
         exit;
      }
   }

   if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
   }
  
   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
   }
# bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   ##if ($grp eq "") {
   ##  status("No group has been selected. Please select a group. If there are no groups to select, it probably means that you have not yet subscribed to any groups or created any group. Use the create link to create a group, or press the subscribe button to subscribe to a group. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to search for groups.");
   ##  exit;
   ##} 

   if ($input{calendar} ne "") {
      if ( (!(exists $sgrouptab{$grp})) && (!(exists $fgrouptab{$grp})) ) {
         status("$login: You are currently not subscribed to this calendar. It is likely that you may have recently unsubscribed from this calendar or selected a calendar from the unsubscribed calendar list. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for calendars.");
         exit;
      } 

      if ($lgrouptab{$grp}{'password'} ne "") {
         $prml = "";

         if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdeditprivatecal.html") ) {
           $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdeditprivatecal.html";
         } else {
           $tmpl = "$ENV{HDTMPL}/hdeditprivatecal.html";
         }

         if ($os ne "nt") {
            $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
            $prml = strapp $prml, "formenc=$formenc";
         } else {
            $prml = strapp $prml, "formenc=";
         }

         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "label=$label";
         $prml = strapp $prml, "logo=$logo";
         $prml = strapp $prml, "template=$tmpl";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/esg-$$.html";
         $prml = strapp $prml, "biscuit=$biscuit";
         $prml = strapp $prml, "g=$grp";
         $prml = strapp $prml, "jp=$jp";
         $prml = strapp $prml, "hiddenvars=$hiddenvars";
         parseIt $prml;

	 #hddebug "prml = $prml";
         #system "/bin/cat $ENV{HDTMPL}/content.html";
         #system "/bin/cat $ENV{HDHREP}/$alpha/$login/esg-$$.html";
         hdsystemcat "$ENV{HDHREP}/$alpha/$login/esg-$$.html";

      } else {

           $prml = "";
           if ($rh eq "") {
              $pcgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
              #$pcgi = "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
           } else {
              $pcgi = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
              #$pcgi = "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
           }
           $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
           $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           $prml = strapp $prml, "redirecturl=$pcgi";
           $prml = strapp $prml, "logo=$logo";
           $prml = strapp $prml, "hiddenvars=$hiddenvars";
           parseIt $prml;
           hdsystemcat "$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           #print "Location: $pcgi\n\n";
      }
   }


   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

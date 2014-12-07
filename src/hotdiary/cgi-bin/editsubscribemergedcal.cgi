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
# FileName: editsubscribemergedcal.cgi
# Purpose: New HotDiary Edit Subscribe Group Calendar
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

   hddebug "enter editsubscribemergedcal.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $jp = $input{jp};
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   $os = $input{'os'};
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ($input{'view'} ne "") {
      if ($biscuit eq "") {
         if ($hs eq "") {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         } else {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         }
         exit;
      }
      $action = "View";
   } else {
      if ($input{'unsubscribe'} ne "") {
         $action = "Unsubscribe";
      } else {
         $action = "Subscribe";
      }
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

   $rh = $input{'rh'};
   $label = "HotDiary";
   $logo = "";

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

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

                           
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

       if (exists $jivetab{$jp}) {
          $logo = adjusturl $jivetab{$jp}{logo};
          $title = adjusturl $jivetab{$jp}{title};
          $label = $title;
       }  else {
          if (exists $lictab{$ip}) {
             $partner = $lictab{$ip}{partner};
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
	        $label = $title;
             }
          }
       }

   # bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'groups', 'logins' ] };

 
   system "mkdir -p $ENV{HDDATA}/merged/$login/subscribed/smergetab"; 
   system "chmod 755 $ENV{HDDATA}/merged/$login/subscribed/smergetab"; 

   system "mkdir -p $ENV{HDDATA}/merged/$login/founded/fmergetab"; 
   system "chmod 755 $ENV{HDDATA}/merged/$login/founded/fmergetab"; 
    
   # bind subscribed group table vars
   tie %smergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/merged/$login/subscribed/smergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
         'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

# bind founded group table vars
   tie %fmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/merged/$login/founded/fmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
      'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };

   $grp = $input{'radio1'};
   hddebug "grp = $grp";

   if ($os ne "nt") {
      $execmgcalclient = encurl "execmgcalclient.cgi";
      $execmergedgroups =  encurl "execmergedgroups.cgi";
      $execeditmergedcal =  encurl "execeditmergedcal.cgi";
      $execsubscribemergedcal =  encurl "execsubscribemergedcal.cgi";
   } else {
      $execmgcalclient = "execmgcalclient.cgi";
      $execmergedgroups =  "execmergedgroups.cgi";
      $execeditmergedcal =  "execeditmergedcal.cgi";
      $execsubscribemergedcal =  "execsubscribemergedcal.cgi";
   }

   if ($rh ne "") {
      $cgis = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   }  

   if (-f "$ENV{HDREP}/$alpha/$login/topcal.html") {
      $fref = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   } else {
      $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }

   $mcalmsg = adjusturl "Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&p4=grouplist&pnum=5&biscuit=$biscuit&f=mc&grouplist=$grp&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to search for merged calendars.";

   if ($grp eq "") {
      status("No group has been selected. Please select a group. If there are no group to select, it probably means that you have not yet subscribed to any merged group or created any merged group. Use the create link to create a merged group, or press the subscribe button to subscribe to a merged group. <p> $mcalmsg");
   } else {
   if ($action eq "View") {
      if ( (!(exists $smergetab{$grp})) && (!(exists $fmergetab{$grp})) ) {
         status("$login: You are currently not subscribed to this merged group calendar. It is likely that you may have recently unsubscribed from this merged group or selected a merged group calendar from the unsubscribed merged group calendar list. <p> $mcalmsg");
         exit;
      } 

      $logo = adjusturl $logo;

      if ($lmergetab{$grp}{'password'} ne "") {
         $prml = "";
         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "label=$label";
         $prml= strapp $prml, "logo=$logo";

         if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdviewmergedcal.html") ) {
            $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdviewmergedcal.html";
         } else {
            $tmpl = "$ENV{HDTMPL}/hdviewmergedcal.html";
         }

         $prml = strapp $prml, "template=$tmpl";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/esg-$$.html";
         $prml = strapp $prml, "biscuit=$biscuit";
         $prml = strapp $prml, "g=$grp";
         $prml = strapp $prml, "jp=$jp";
         $prml = strapp $prml, "welcome=Welcome";
         $prml = strapp $prml, "label2=";
         $prml = strapp $prml, "login=$login";
         $prml = strapp $prml, "percal=$cgis";
         $prml = strapp $prml, "home=$fref";             
         if ($os ne "nt") {
            $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
            $prml = strapp $prml, "formenc=$formenc";
         } else {
            $prml = strapp $prml, "formenc=";
         }

         $hiddenvars = "";
         $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execeditmergedcal>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=g>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=password>";

         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=g VALUE=$grp>";

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
	 hddebug "came here";
         #system "/bin/cat $ENV{HDTMPL}/content.html";
         #system "/bin/cat $ENV{HDHREP}/$alpha/$login/esg-$$.html";
         hdsystemcat "$ENV{HDHREP}/$alpha/$login/esg-$$.html";

      } else {
           $prml = "";
           #$prml = strapp $prml, "rh=$rh";
           #$prml = strapp $prml, "label=$label";
	   #$logo = adjusturl "<IMG SRC=\"$logo\" WIDTH=\"60\" HEIGHT=\"60\">";
           #$prml = strapp $prml, "logo=$logo";
           $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
           $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           $prml = strapp $prml, "welcome=Welcome";
           $prml = strapp $prml, "label2=";
           $prml = strapp $prml, "login=$login";
           if ($rh eq "") {
              $pcgi = adjusturl "/cgi-bin/execmgcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
           } else {
              $pcgi = adjusturl "/cgi-bin/$rh/execmgcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os";
           }
           $prml = strapp $prml, "redirecturl=$pcgi";
           parseIt $prml;
           #system "/bin/cat $ENV{HDTMPL}/content.html";
           #system "/bin/cat $ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           hdsystemcat "$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
      }
      exit;
   }


   if ($action eq "Unsubscribe") {
      if (exists $fmergetab{$grp}) {
         status("$login: You cannot unsubscribe from the merged calendar \"$grp\" because you are the calendar master for this merged calendar. Perhaps the Manage feature would be what you are looking for. <p>$mcalmsg");
	 exit;
      }
      if (!(exists $smergetab{$grp})) {
         status("$login: You are currently not subscribed to the merged calendar $grp. It is likely that you may have recently unsubscribed from this merged calendar or selected a merged calendar from the unsubscribed merged calendar list. <p>$mcalmsg");
         exit;
      }

      system "mkdir -p $ENV{HDDATA}/listed/merged/$grp/usertab";
      system "chmod 755 $ENV{HDDATA}/listed/merged/$grp/usertab";

      tie %usertab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/merged/$grp/usertab",
      SUFIX => '.rec',
      SCHEMA => {
            ORDER => ['login'] };

      delete $usertab{$login};
      tied(%usertab)->sync();
      delete $smergetab{$grp};
      tied(%smergetab)->sync();
      status("$login: You have successfully unsubscribed from $grp. Click <a href=\"http://$vdomain/cgi-bin/$rh/execmergedgroups.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for merged calendars.");
      exit;
   }

   if ($action eq "Subscribe") {
      if (exists $smergetab{$grp}) {
        
         status("$login: You are already subscribed to the merged calendar $grp. Click <a href=\"http://$vdomain/cgi-bin/$rh/execmergedgroups.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for merged calendars.");
      } else {
          if (exists $fmergetab{$grp}) {
             status("$login: You are already the merged calendar master for $grp. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execmergedgroups.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for merged calendars.");
          } else {
               if ($lmergetab{$grp}{'password'} ne "") {
                  $prml = "";
                
                  $prml = strapp $prml, "rh=$rh";
                  $prml = strapp $prml, "label=$label";
                  $prml = strapp $prml, "logo=$logo";

                  $prml = strapp $prml, "template=$ENV{HDTMPL}/hdsubscribemergedcal.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/esg-$$.html";
                  $prml = strapp $prml, "biscuit=$biscuit";
                  $prml = strapp $prml, "g=$grp";
                  $prml = strapp $prml, "jp=$jp";
                  $prml = strapp $prml, "os=$os";
                  $prml = strapp $prml, "welcome=Welcome";
                  $prml = strapp $prml, "label2=";
                  $prml = strapp $prml, "percal=$cgis";
                  $prml = strapp $prml, "home=$fref";             
                  $prml = strapp $prml, "homestr=Home";             
                  $prml = strapp $prml, "login=$login";             
                  if ($os ne "nt") {
                     $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
                     $prml = strapp $prml, "formenc=$formenc";
                  } else {
                     $prml = strapp $prml, "formenc=";
                  }
                  $hiddenvars = "";
                  $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execsubscribemergedcal>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=g>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=password>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
                  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=g VALUE=$grp>";

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
                  #system "/bin/cat $ENV{HDHREP}/$alpha/$login/esg-$$.html";
                  hdsystemcat "$ENV{HDHREP}/$alpha/$login/esg-$$.html";
               } else {
                    tie %smergetab, 'AsciiDB::TagFile',
                       DIRECTORY => "$ENV{HDDATA}/merged/$alpha/$login/subscribed/smergetab",
                       SUFIX => '.rec',
                       SCHEMA => {
                       ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
                    if (!(exists $smergetab{$grp})) {
                       $smergetab{$grp}{'groupname'} = $grp;
                       $smergetab{$grp}{'groupfounder'} = $lmergetab{$grp}{'groupfounder'};
                       $smergetab{$grp}{'grouptype'} = $lmergetab{$grp}{'grouptype'};
                       $smergetab{$grp}{'grouptitle'} = $lmergetab{$grp}{'grouptitle'};
                       $smergetab{$grp}{'groupdesc'} = $lmergetab{$grp}{'groupdesc'};
                       $smergetab{$grp}{'password'} = $lmergetab{$grp}{'password'};
                       $smergetab{$grp}{'ctype'} = $lmergetab{$grp}{'ctype'};
                       $smergetab{$grp}{'cpublish'} = $lmergetab{$grp}{'cpublish'};
                       tied(%smergetab)->sync();
                    } else {
                         status("$login: You are already subscribed to this merged calendar \"$grp\" Click <a href=\"http://$vdomain/cgi-bin/$rh/execmergedgroups.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for merged calendars. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execcalclientcal.cgi?biscuit=$biscuit&g=$grp&jp=$jp&os=$os\">here</a> to View merged calendar $grp.");
                         exit;
                    }

                    tie %usertab, 'AsciiDB::TagFile',
                        DIRECTORY => "$ENV{HDDATA}/listed/merged/$grp/usertab",
                        SUFIX => '.rec',
                        SCHEMA => {
                        ORDER => ['login'] };
                    $usertab{$login}{'login'} = $login;
                    tied(%usertab)->sync();
                    status("$login: You have successfully subscribed to the merged calendar $grp. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=f&p3=jp&pnum=4&biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for merged calendars. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execmgcalclient.cgi?biscuit=$biscuit&g=$grp&jp=$jp&os=$os\">here</a> to View merged calendar $grp.");
               }
          }
      }
   }
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   hddebug "leave editsubscribemergedcal.cgi";

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
# FileName: editsubscribegroupcal.cgi
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

   #print &PrintHeader;
   #print &HtmlTop ("editsubscribegroupcal.cgi example");
   hddebug "enter editsubscribegroupcal.cgi";

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $jp = $input{jp};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   $os = $input{'os'};
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ($input{'edit'} ne "") {
      if ($biscuit eq "") {
         if ($hs eq "") {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         } else {
            status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
         }
         exit;
      }
      $action = "Edit";
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

   $alphaindex = substr $login, 0, 1;
   $alpha = $alphaindex . '-index';

                           
   $HDLIC = $input{HDLIC};

   if ($rh ne "") {
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
          if (exists $lictab{$HDLIC}) {
             $partner = $lictab{$HDLIC}{partner};
             if (exists $parttab{$partner}) {
                $logo = adjusturl $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
	        $label = $title;
             }
          }
       }
   } 


   if ($logo ne "") {
      $logo = adjusturl $logo;
   }



   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed' ] };

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

   $grp = $input{'radio1'};

   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;

   if ($grp eq "") {
      status("No group has been selected. Please select a group or calendar. If there are no group or calendars to select, it probably means that you have not yet subscribed to any group or calendars or created any group or calendars. Use the create link to create a group or calendar, or press the subscribe button to subscribe to a group or calendar. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
   } else {
   if ($action eq "Edit") {
      if ( (!(exists $sgrouptab{$grp})) && (!(exists $fgrouptab{$grp})) ) {
         status("$login: You are currently not subscribed to this group or calendar. It is likely that you may have recently unsubscribed from this group or calendar or selected a group or calendar from the unsubscribed group or calendar list. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
         exit;
      } 
      if ($lgrouptab{$grp}{'password'} ne "") {
         $prml = "";
         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "label=$label";
         $prml = strapp $prml, "logo=$logo";

         $alphjp = substr $jp, 0, 1;
         $alphjp = $alphjp . '-index';

         if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdeditprivatecal.html") ) {
            $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdeditprivatecal.html";
         } else {
            $tmpl = "$ENV{HDTMPL}/hdeditprivatecal.html";
         }
         $prml = strapp $prml, "template=$tmpl";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/esg-$$.html";
         $prml = strapp $prml, "biscuit=$biscuit";
         $prml = strapp $prml, "g=$grp";
         $prml = strapp $prml, "jp=$jp";
         if ($os ne "nt") {
            $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
            $prml = strapp $prml, "formenc=$formenc";
         } else {
            $prml = strapp $prml, "formenc=";
         }
         $prml = strapp $prml, "hiddenvars=$hiddenvars";
         parseIt $prml;
         #system "/bin/cat $ENV{HDTMPL}/content.html";
         #system "/bin/cat $ENV{HDHREP}/$alpha/$login/esg-$$.html";
         hdsystemcat "$ENV{HDHREP}/$alpha/$login/esg-$$.html";

      } else {
           $prml = "";
           $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
           $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           
           if ($rh eq "") {
              $pcgi = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os&vdomain=$vdomain";
              #$pcgi = "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os&vdomain=$vdomain";
           } else {
              $pcgi = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os&vdomain=$vdomain";
              #$pcgi = "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&l=$login&g=$grp&jp=$jp&os=$os&vdomain=$vdomain";
           }
           $prml = strapp $prml, "redirecturl=$pcgi";
           $prml = strapp $prml, "logo=$logo";
           $prml = strapp $prml, "hiddenvars=$hiddenvars";
           parseIt $prml;
           hdsystemcat "$ENV{HDHREP}/$alpha/$login/red-$biscuit-$$.html";
           #print "Location: http://$vdomain/$pcgi\n\n";
      }
      exit;
   }


   if ($action eq "Unsubscribe") {
      if (exists $fgrouptab{$grp}) {
         status("$login: You cannot unsubscribe from the group or calendar \"$grp\" because you are the group or calendar master for this group or calendar. Perhaps the Manage feature would be what you are looking for. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
	 exit;
      }
      if (!(exists $sgrouptab{$grp})) {
         status("$login: You are currently not subscribed to the group or calendar $grp. It is likely that you may have recently unsubscribed from this group or calendar or selected a group or calendar from the unsubscribed group or calendar list. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
         exit;
      }

      tie %usertab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$grp/usertab",
      SUFIX => '.rec',
      SCHEMA => {
            ORDER => ['login'] };

      delete $usertab{$login};
      tied(%usertab)->sync();
      delete $sgrouptab{$grp};
      tied(%sgrouptab)->sync();
      status("$login: You have successfully unsubscribed from $grp. Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
      exit;
   }

   if ($action eq "Subscribe") {
      if (exists $sgrouptab{$grp}) {
        
         status("$login: You are already subscribed to the group or calendar $grp. Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
      } else {
          if (exists $fgrouptab{$grp}) {
             status("$login: You are already the group or calendar master for $grp. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars.");
          } else {
               if ($lgrouptab{$grp}{'password'} ne "") {
                  $prml = "";
                
                  $prml = strapp $prml, "rh=$rh";
                  $prml = strapp $prml, "label=$label";
                  $prml = strapp $prml, "logo=$logo";

                  #$logo = adjusturl "<IMG SRC=\"$logo\" WIDTH=\"60\" HEIGHT=\"60\">";	          
                  ##$logo = adjusturl "<IMG SRC=\"$logo\">";	          

                  $alphjp = substr $jp, 0, 1;
                  $alphjp = $alphjp . '-index';

                  if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdsubscribeprivatecal.html") ) {
                     $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdsubscribeprivatecal.html";
                 } else {
                     $tmpl = "$ENV{HDTMPL}/hdsubscribeprivatecal.html";
                 }
                  $prml = strapp $prml, "template=$tmpl";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/esg-$$.html";
                  $prml = strapp $prml, "biscuit=$biscuit";
                  $prml = strapp $prml, "g=$grp";
                  $prml = strapp $prml, "jp=$jp";
                  $prml = strapp $prml, "os=$os";
                  if ($os ne "nt") {
                     $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
                     $prml = strapp $prml, "formenc=$formenc";
                  } else {
                     $prml = strapp $prml, "formenc=";
                  }

                  $prml = strapp $prml, "hiddenvars=$hiddenvars";
                  parseIt $prml;
                  #system "/bin/cat $ENV{HDTMPL}/content.html";
                  #system "/bin/cat $ENV{HDHREP}/$alpha/$login/esg-$$.html";
                  hdsystemcat "$ENV{HDHREP}/$alpha/$login/esg-$$.html";
               } else {
                    tie %sgrouptab, 'AsciiDB::TagFile',
                       DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
                       SUFIX => '.rec',
                       SCHEMA => {
                       ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
                    if (!(exists $sgrouptab{$grp})) {
                       $sgrouptab{$grp}{'groupname'} = $grp;
                       $sgrouptab{$grp}{'groupfounder'} = $lgrouptab{$grp}{'groupfounder'};
                       $sgrouptab{$grp}{'grouptype'} = $lgrouptab{$grp}{'grouptype'};
                       $sgrouptab{$grp}{'grouptitle'} = $lgrouptab{$grp}{'grouptitle'};
                       $sgrouptab{$grp}{'groupdesc'} = $lgrouptab{$grp}{'groupdesc'};
                       $sgrouptab{$grp}{'password'} = $lgrouptab{$grp}{'password'};
                       $sgrouptab{$grp}{'ctype'} = $lgrouptab{$grp}{'ctype'};
                       $sgrouptab{$grp}{'cpublish'} = $lgrouptab{$grp}{'cpublish'};
                       tied(%sgrouptab)->sync();
                    } else {
                         status("$login: You are already subscribed to this group or calendar \"$grp\" Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to Search for group or calendars. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execcalclientcal.cgi?biscuit=$biscuit&g=$grp&jp=$jp&os=$os\">here</a> to View or Edit group or calendar $grp.");
                         exit;
                    }

                    tie %usertab, 'AsciiDB::TagFile',
                        DIRECTORY => "$ENV{HDDATA}/listed/groups/$grp/usertab",
                        SUFIX => '.rec',
                        SCHEMA => {
                        ORDER => ['login'] };
                    $usertab{$login}{'login'} = $login;
                    tied(%usertab)->sync();
                    status("$login: You have successfully subscribed to the group or calendar $grp. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=sgc&jp=$jp&os=$os\">here</a> to search for group or calendars. <p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&g=$grp&jp=$jp&os=$os\">here</a> to View or Edit calendar $grp.");
               }
          }
      }
   }
   }

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   #hddebug "leave editsubscribegroupcal.cgi";

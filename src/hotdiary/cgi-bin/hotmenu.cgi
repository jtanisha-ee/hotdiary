#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: hotmenu.cgi
# Purpose: it displays the appropriate user menus at the top level.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use tp::tp;
use ParseTem::ParseTem;
use utils::utils;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;

$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   #print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration"); 

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['login', 'password', 'fname', 'lname', 'street',
	'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['biscuit', 'login', 'time'] };

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
	'installation', 'domains', 'domain', 'orgrole', 'organization', 'orgsize', 'budget', 'timeframe', 'platform', 'priority', 'editcal', 'calpeople'] };
 
# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['login', 'biscuit'] };

# bind memo table vars
   tie %memotab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/memotab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'memolist'] };

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = trim $input{'biscuit'};
   #$title = time();

   #print "biscuit = ", $biscuit, "\n";
   if (!exists $sesstab{$biscuit}) {
      status("Not logged in. Please login before you can access HotDiary. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login. \n");
      exit;
   }

   if ($login eq "") {
      $login = $sesstab{$biscuit}{'login'};
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      if (exists $sesstab{$biscuit}) {
         delete $sesstab{$biscuit};
      }
      if (exists $logsess{$login}) {
         delete $logsess{$login};
       }
      status("You have been logged out automatically. Please relogin. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");

      exit;
   } else {
      $sesstab{$biscuit}{'time'} = time();
   }

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $title = $hdtab{$login}{title};
      $title = adjusturl($title); 
   } else {
      $title = "HotDiary";
   }  
                         
   if ($input{'addresses.x'} ne "") {
      $action = "Addresses";
   } else {
       if ($input{'reminders.x'} ne "") {
          $action = "Appointments";
       }  else {
          if ($input{'collabrum.x'} ne "") {
             $action = "Collabrum";
          } else {
              if ($input{'logout.x'} ne "") {
                $action = "Logout";
	      } else  {
	         if ($input{'profile.x'} ne "") {
                    $action = "Profile";
	         } else {
	            if ($input{'faq.x'} ne "") {
                       $action = "Faq";
	            } else {
			if ($input{'memocal.x'} ne "") {
                           $action = "MemoCal";
			} else {
                           if ($input{'importf.x'} ne "") {
                              $action = "Import";
                           } else {
                              if ($input{'exportf.x'} ne "") {
                                 $action = "Export";
                              } else {
                                 if ($input{'groups.x'} ne "") {
                                    $action = "Groups";
                                 } else {
                                    if ($input{'calclient.x'} ne "") {
                                       #$action = "Calendar"; 
                                    }
                                 }
                              }
                           }
                        }
	            }
		 }
	      } 
	  }
	
       }
   }   
   hddebug "hotmenu action = $action";

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if ($action eq "Logout") {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html $ENV{HDREP}/$alpha/$login/index.html1";
      system "/bin/rm -f $ENV{HDREP}/$alpha/$login/*.html";
      system "/bin/rm -f $ENV{HDHREP}/$alpha/$login/*.html";
      system "/bin/mv $ENV{HDREP}/$alpha/$login/index.html1 $ENV{HDREP}/$alpha/$login/index.html";
      status("$login: You have been logged out. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.");
      exit;	
   }   

   if ($action eq "Calendar") {
      # Init the base CGI url

      $cgiscript = "execcalclient.cgi?biscuit=$biscuit";
      $cgis = "http://www.hotdiary.com/cgi-bin/$cgiscript";

      $rurl = adjusturl "$cgis";
      $prm = "";
      $prm = strapp $prm, "redirecturl=$rurl";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect.html";
      $prm = strapp $prm, "templateout=$ENV{HDHREP}/$alpha/$login/$biscuit-$$-redirect.html";
      parseIt $prm, 1;
      #system "/bin/cat $ENV{HDTMPL}/content.html";
      #system "/bin/cat $ENV{HDHREP}/$alpha/$login/$biscuit-$$-redirect.html";
   }


   if ($action eq "Addresses") {
        $buddy = "rep/$alpha/$login/friend$biscuit.html";
         
   	$label = "$title Address Add/Search Menu";
	$label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
        $label1 = "To search entries, use the first few letters of First or Last Name.";
        $prml = "";
        $prml = strapp $prml, "buddy=$buddy";
        $prml = strapp $prml, "template=$ENV{HDTMPL}/menuaddrtbl.html";
        $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/menuaddrtbl.html";
        parseIt $prml, 1;

   } else {
	if ($action eq "Appointments") {
   	  $label = "$title Reminder Add/Search Menu";
          $label1 = "Voice, and Fax are supported only for premium members. Reminders are sent a minimum of 20 minutes in advance of due time.";
          $label2 = "To search entries, use Month as key.";
          $prml = "";
          ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
	  
	  $monthstr = getmonthstr($mon+1);
	  $newmonth = $mon + 1;
          $zone = $logtab{$login}{'zone'};
	  if ($zone eq "") {
	     $zone = -8;
          }
          $zonestr = getzonestr($zone);
          $prml = strapp $prml, "monthnum=$newmonth";
          $prml = strapp $prml, "month=$monthstr";
          $prml = strapp $prml, "day=$mday";
          $prml = strapp $prml, "zone=$zone";
          $prml = strapp $prml, "zonestr=$zonestr";
          #$prml = strapp $prml, "year=19$year";
   
          $prml = strapp $prml, "template=$ENV{HDTMPL}/menuappttbl.html";
          $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/menuappttbl.html";     
          parseIt $prml, 1;

	} else  {
	   if ($action eq "Collabrum") {
   	      $label = "$title Multi-Group Reminder Add/Search Menu";
              $label1 = "Voice, and Fax are supported only for premium members. Reminders are sent a minimum of 20 minutes in advance of due time.";
	      $label2 = "To search entries, use Entry Number as key.";
              $prml = "";
              ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());

              $monthstr = getmonthstr($mon+1);
              $newmonth = $mon + 1;
              $zone = $logtab{$login}{'zone'};
	      if ($zone eq "") {
	         $zone = -8;
              }
              $zonestr = getzonestr($zone);
              $prml = strapp $prml, "monthnum=$newmonth";
              $prml = strapp $prml, "month=$monthstr";
              $prml = strapp $prml, "day=$mday";
              $prml = strapp $prml, "zone=$zone";
              $prml = strapp $prml, "zonestr=$zonestr";
              #$prml = strapp $prml, "year=19$year;
              $prml = strapp $prml, "template=$ENV{HDTMPL}/menucolltbl.html";
              $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/menucolltbl.html";
              tie %pgrouptab, 'AsciiDB::TagFile',
                DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab",
                SUFIX => '.rec',
                SCHEMA => {
                     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };
              if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
                  system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
                  system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
              }
              tie %sgrouptab, 'AsciiDB::TagFile',
                DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
                SUFIX => '.rec',
                SCHEMA => {
                     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };
              (@records) = sort keys %pgrouptab;
              if ($#records >= 0) {
                 for ($l = 0; $l <= $#records; $l++) {
                     $records[$l] = "\L$records[$l]";
                     $multsel = $multsel . "\<OPTION\>$records[$l]\<\/OPTION\>";
                 }
              }
              (@records1) = sort keys %sgrouptab;
              if ($#records1 >= 0) {
                 for ($l = 0; $l <= $#records1; $l++) {
                     $records[$l] = "\L$records[$l]";
                     $multsel = $multsel . "\<OPTION\>$records1[$l]\<\/OPTION\>";
                 }
              }
              if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
                  system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
                  system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
              }
              tie %fgrouptab, 'AsciiDB::TagFile',
                DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
                SUFIX => '.rec',
                SCHEMA => {
                     ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };
              (@records2) = sort keys %fgrouptab;
              if ($#records2 >= 0) {
                 for ($l = 0; $l <= $#records2; $l++) {
                     $multsel = $multsel . "\<OPTION\>$records2[$l]\<\/OPTION\>";
                 }
              }
              if (($#records < 0) && ($#records1 < 0) && ($#records2 < 0)) {
                 $multsel = "<OPTION>No Group</OPTION>";
              }
              $prml = strapp $prml, "distopt=$multsel";
              parseIt $prml, 1;

	   } else {
	      if ($action eq "MemoCal") {
		 if (!exists $memotab{$login}) {
		    system "/bin/touch $ENV{HDDATA}/memotab/$login";
                    system "/bin/chmod 700 $ENV{HDDATA}/memotab/$login";
                    #print "MemoCal record does not exist.\n";
		 } else {
                #($outfield = $memotab{$login}{'memolist'}) =~ s/\n/\n<BR>/g;
                    $outfield = $memotab{$login}{'memolist'};
                    $prml = strapp $prml, "memolist=$outfield";
		    #print "outfield = ", $outfield, "\n"; 
		 }
                 #if ($login eq "demo") {
                 #   $ENV{'PERL5LIB'} = "/usr/local/hotdiary/perllibs";
                 #   $ENV{'biscuit'} = $biscuit;
                 #   system "/home/httpd/cgi-bin/calendar.pl";
                 #   exit;
                 #}
   	         #$label = "$title Memo";
		 #$label1 = $label2 = "";
                 #$prml = strapp $prml, "memolist=$memolist";
                 $prml = strapp $prml, "template=$ENV{HDTMPL}/memocal.html";
                 $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/memocal.html";
                 $purlcgi = adjusturl("<a href=\"http://www.hotdiary.com/cgi-bin/execcalclient.cgi?biscuit=$biscuit\" target=_parent>View</a> My TelTalk Calendar");
                 $prml = strapp $prml, "pcalendarprog=$purlcgi";

                 $prml = strapp $prml, "template=$ENV{HDTMPL}/memocal.html";
                 $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/memocal.html";
                 $urlcgi = adjusturl("cgi-bin/execcalendar.cgi?biscuit=$biscuit&memolist=$memolist");
                 $prml = strapp $prml, "calendarprog=$urlcgi";
                 if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab")) {
                    system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
                    system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
                 }
                 tie %sgrouptab, 'AsciiDB::TagFile',
                 DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab",
                  SUFIX => '.rec',
                  SCHEMA => {
                  ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };
                 (@records1) = sort keys %sgrouptab;
                 $cntr = 0; 
                 if ($#records1 >= 0) {
                    for ($l = 0; $l <= $#records1; $l++) {
                       if ($sgrouptab{$records1[$l]}{'password'} eq "") {
                          $cntr = $cntr + 1;
                          $singsel = $singsel . "\<OPTION\>$records1[$l]\<\/OPTION\>";
                       }
                    }
                 }
                 if (!(-d "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab")) {
                     system "mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
                     system "chmod 755 $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
                 }
                 tie %fgrouptab, 'AsciiDB::TagFile',
                 DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab",
                  SUFIX => '.rec',
                  SCHEMA => {
                  ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg'] };
                 (@records) = sort keys %fgrouptab;
                 if ($#records >= 0) {
                    for ($l = 0; $l <= $#records; $l++) {
                       if ($fgrouptab{$records[$l]}{'password'} eq "") {
                          $cntr = $cntr + 1;
                          $singsel = $singsel . "\<OPTION\>$records[$l]\<\/OPTION\>";
                       }
                    }
                 }
                 #if ( ($#records1 < 0) && ($#records < 0) ) {
                 if ($cntr == 0) {
                    $singsel = "<OPTION>NoGroup</OPTION>";
                 }
                 $prml = strapp $prml, "pgroups=$singsel";
                 $prml = strapp $prml, "ppgroups=$singsel";


                 parseIt $prml, 1;
                 $prml = "";
              }	else  {
	      if ($action eq "Faq") {
   	         $label = "$title Frequently asked questions.";
		 $label1 = $label2 = "";
              }	else  {
	      if ($action eq "Profile") {
		 #print "action is profile \n\n";
		 if (!exists $logtab{$login}) {
                     #print "Profile record does not exist.\n";
                     status("$login: Profile does not exist.\n");
                     exit;
                 } else {
                    $prml = "";
                    $prml = strapp $prml, "biscuit=$biscuit";
                    #print "Profile record exists login =", $login, "\n\n";
                    #($outfield = $logtab{$login}{'login'}) =~ s/\n/\n<BR>/g;
                    $outfield = $logtab{$login}{'login'};
                    #print "Login = ", $login, "\n";
                    $prml = strapp $prml, "login=$outfield";

                    ($outfield = $logtab{$login}{'password'}) =~ s/\n/\n<BR>/g;
                    #print "Password = ", $outfield, "\n";
                    $prml = strapp $prml, "password=$outfield";

                    ($outfield = $logtab{$login}{'password'}) =~ s/\n/\n<BR>/g;
                    #print "Repeat Password = ", $outfield, "\n";
                    $prml = strapp $prml, "rpassword=$outfield";
                    #$prml = strapp $prml, "password=outfield";

                    ($outfield = $logtab{$login}{'fname'}) =~ s/\n/\n<BR>/g;
                    #print "First Name = ", $outfield, "\n";
                    $prml = strapp $prml, "fname=$outfield";

                    ($outfield = $logtab{$login}{'lname'}) =~ s/\n/\n<BR>/g;
                    #print "Last Name = ", $outfield, "\n";
                    $prml = strapp $prml, "lname=$outfield";

                    ($outfield = $logtab{$login}{'street'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "street=$outfield";
                    #print "Street = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'city'}) =~ s/\n/\n<BR>/g;
                    #print "City = ", $outfield, "\n";
                    $prml = strapp $prml, "city=$outfield";
 
                    ($outfield = $logtab{$login}{'state'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "state=$outfield";
                    #print "State = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'zipcode'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "zipcode=$outfield";
                    #print "ZipCode = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'country'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "country=$outfield";
                    #print "Country = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'phone'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "phone=$outfield";
                    #print "Phone = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'pager'}) =~ s/\n/\n<BR>/g;
                    $outfield = adjusturl $outfield;
                    $prml = strapp $prml, "pager=$outfield";
                    #print "Pager = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'pagertype'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "pagertype=$outfield";
 
                    ($outfield = $logtab{$login}{'fax'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "fax=$outfield";
                    #print "Fax = ", $outfield, "\n";
 
                    ($outfield = $logtab{$login}{'cphone'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "cellp=$outfield";
                    #print "cell phone = ", $outfield, "\n";
 
                    ($outfield = $logtab{$login}{'bphone'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "busp=$outfield";
                    #print "BusinessPhone = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'email'}) =~ s/\n/\n<BR>/g;
                    $outfield = adjusturl $outfield;
                    $prml = strapp $prml, "email=$outfield";
                    #print "Email = ", $outfield, "\n";
 
                    ($outfield = $logtab{$login}{'url'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "url=$outfield";
                    #print "URL = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'zone'}) =~ s/\n/\n<BR>/g;
                    if ($outfield eq "") {
			$outfield = -8;
                    }               
                    $prml = strapp $prml, "zone=$outfield";

                    ($outfield = $logtab{$login}{'zone'}) =~ s/\n/\n<BR>/g;
                    if ($outfield eq "") {
			$outfield = -8;
                    }               
	            $zonestr = getzonestr($outfield);
                    $prml = strapp $prml, "zonestr=$zonestr";

                    ($outfield = $logtab{$login}{'checkid'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "checkid=$outfield";
                    #print "checkid = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'calpublish'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "calpublish=$outfield";

                    if (exists $surveytab{$login}) {
                    ($outfield = $surveytab{$login}{'calinvite'}) =~ s/\n/\n<BR>/g;
	            } else {
	             $outfield = "";
                    }
                    $prml = strapp $prml, "calinvite=$outfield";
                    #print "checkid = ", $outfield, "\n";

                    ($outfield = $logtab{$login}{'informme'}) =~ s/\n/\n<BR>/g;
                    $prml = strapp $prml, "checkboxfield=$outfield";

                    #$urlcgi = buildurl("execprofupdate.cgi");
                    $urlcgi = "execprofupdate.cgi";
                    $prml = strapp $prml, "actioncgi=$urlcgi";

   	            $label = "Personal Profile";
                    $prml = strapp $prml, "label=$label";
                    $formenc = adjusturl ("ENCTYPE=\"$ENV{HDENCODE}\"");
                    $prml = strapp $prml, "formenc=$formenc";
                    $prml = strapp $prml, "template=$ENV{HDTMPL}/profile.html";
                    $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/profile.html";
                    parseIt $prml, 1;
                    $prml = "";
                    }
                  } else {
                    if ($action eq "Import") {
   	               $label = "$title Import Utility";
	               $label1 = "";
                       $label2 = "Import comma-separated values (.csv) file.";
                       $prml = "";
                       $prml = strapp $prml, "template=$ENV{HDTMPL}/importmenu.html";
                       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/importmenu.html";
                       parseIt $prml, 1;
                    } else {
                       if ($action eq "Export") {
   	                  $label = "$title Export Utility";
	                  $label1 = "";
                          $label2 = "";
                          $prml = "";
                          $prml = strapp $prml, "template=$ENV{HDTMPL}/exportmenu.html";
                          $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/exportmenu.html";
                          parseIt $prml, 1;

                       } else {

   if ($action eq "Groups") {
      #if (($login ne "mjoshi") && ($login ne "smitha") && ($login ne "buddie") && ($login ne "user1") &&
      #    ($login ne "user2") && ($login ne "user3") && ($login ne "user4") && ($login ne "user5") &&
      #    ($login ne "user6") && ($login ne "user7") && ($login ne "user8") && ($login ne "user9") &&
      #    ($login ne "user10") && ($login ne "user11") && ($login ne "user12") ) {
      #   status("This service is coming soon!");
      #   exit;
      #}
      $label = "$title Groups Wizard";
      $label1 = "To use secure calendar groups, press Calendar button.";
      $label2 = "Secure groups are not displayed here.";
      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/menugrouptbl.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/menugrouptbl.html";
      # bind personal group table vars
      tie %pgrouptab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };

      (@records) = sort keys %pgrouptab;
      #print "Num records = $#records<BR>";
      if ($#records < 0) {
         $prml = strapp $prml, 'pgroups=<OPTION>No Group</OPTION>';
      } else {
         $pgroups = "";
         for ($l = 0; $l <= $#records; $l++) {
             $pgroups = $pgroups . "\<OPTION\>$records[$l]\<\/OPTION\>"; 
         }
         $prml = strapp $prml, "pgroups=$pgroups";
      }
      parseIt $prml, 1;
   }
                       }
                    }
                  }
  	        }
	     }
          }
      }
   }


   $prml = "";
   #$prml = strapp $prml, "rightFrame=$ENV{HDREP}/$alpha/$login/rightInitialFrame.html";
   $prml = strapp $prml, "label=$label";
   $logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
   $prml = strapp $prml, "login=$logi";
   $prml = strapp $prml, "label1=$label1";
   $prml = strapp $prml, "label2=$label2";
   $prml = strapp $prml, "biscuit=$biscuit";
   
   #$expiry = localtime(time() + 300);
   #$expiry = "\:$expiry";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/stdpghdr.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdpghdr.html";
   #$prml = strapp $prml, "expiry=$expiry";
   $prml = strapp $prml, "expiry=";
   parseIt $prml, 1;


   $prml = "";

   if ($action eq "Addresses") {
       $buddy = "rep/$alpha/$login/friend$biscuit.html"; 
       $prml = strapp $prml, "buddy=$buddy";

       $prml = strapp $prml, "template=$ENV{HDTMPL}/addrmenutblhdr.html";
       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/addrmenutblhdr.html";   

        $urlcgi = buildurl("execaddraddsearch.cgi");
        $prml = strapp $prml, "actioncgi=$urlcgi"; 
        
   }  else {
        if ($action eq "Appointments") {
           $prml = strapp $prml, "template=$ENV{HDTMPL}/stdmenutblhdr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html";   
           $urlcgi = buildurl("execapptaddsearch.cgi");
           $prml = strapp $prml, "actioncgi=$urlcgi";
	}
	else {
	  if ($action eq "Collabrum") {
            $prml = strapp $prml, "template=$ENV{HDTMPL}/stdmenutblhdr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html";   
	    $urlcgi = buildurl("execcolladdsearch.cgi");
            $prml = strapp $prml, "actioncgi=$urlcgi"
	   } else {
	     if ($action eq "Faq") {
	     } else {
	        if ($action eq "Profile") {
                  #$label = "Personal Profile";
                  #$prml = strapp $prml, "label=$label";
                  #$prml = strapp $prml, "template=$ENV{HDTMPL}/profile.html";
                  #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/profile.html";   
                  #$urlcgi = buildurl("execprofupdate.cgi");
                  #$prml = strapp $prml, "actioncgi=$urlcgi";
	        } else {
	            if ($action eq "MemoCal") {
                       $prml = strapp $prml, "template=$ENV{HDTMPL}/stdmenutblhdr.html";
                       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html";   
                       $urlcgi = buildurl("execmemocalupdate.cgi");
                       $prml = strapp $prml, "actioncgi=$urlcgi";
		    } else {
                       if ($action eq "Import") {
                          $prml = strapp $prml, "template=$ENV{HDTMPL}/importmenu.html";
                          $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/importmenu.html";   
                          $urlcgi = buildurl("execsyncaddr.cgi");
                          $prml = strapp $prml, "actioncgi=$urlcgi";
                       } else {
                          if ($action eq "Export") {
                             $prml = strapp $prml, "template=$ENV{HDTMPL}/exportmenu.html";
                             $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/exportmenu.html";   
                             $urlcgi = buildurl("execexport.cgi");
                             $prml = strapp $prml, "actioncgi=$urlcgi";
                          } else {
     if ($action eq "Groups") {
       $prml = strapp $prml, "template=$ENV{HDTMPL}/menugrouptbl.html";
       $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/menugrouptbl.html";
       $urlcgi = buildurl("execgroupaddsearch.cgi");
       $prml = strapp $prml, "actioncgi=$urlcgi";
     }
                          }
                       }
                    }

	         }
	      }
	   }
       }
   }
   
   parseIt $prml, 1;    
 
   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/stdmenutblftr.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdmenutblftr.html";
   parseIt $prml, 1;

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/stdpgftr.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdpgftr.html";
   parseIt $prml, 1;
   $prml = "";

   if ($action eq "MemoCal") {
      $prml = "";
      $label = "$title Calendar Blogging";
      $label1 = "Home of all Calendars";
      $label2 = "For reminders, use TelTalk and new Group Calendars";
      $prml = strapp $prml, "label=$label";
      $logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      $prml = strapp $prml, "login=$logi";
      $prml = strapp $prml, "label1=$label1";
      $prml = strapp $prml, "label2=$label2";
      $prml = strapp $prml, "biscuit=$biscuit";
      #$prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/memocalpghdr.html";
      #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/memocalpghdr.html";
      parseIt $prml, 1;
      $prml = "";

      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
      parseIt $prml, 1;
      $prml = "";

      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/memocalpgftr.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/memocalpgftr.html";
      parseIt $prml, 1;
      $prml = "";
   } 
      


   if ($action eq "Profile") {
      #$prml = "";
      #$label = "Personal Profile";
      #$prml = strapp $prml, "label=$label";
      #$prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
      #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html";
      #parseIt $prml;
      #$prml = "";
#
      #$prml = "";
      #$prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html";
      #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
      #parseIt $prml;
      #$prml = "";
#
      #$prml = "";
      #$prml = strapp $prml, "template=$ENV{HDTMPL}/profilepgftr.html";
      #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/profilepgftr.html";
      #parseIt $prml;
      #$prml = "";
      
   }
   
   if ($action eq "Addresses") {
      #system "/bin/cat $ENV{HDTMPL}/content.html $ENV{HDREP}/$alpha/$login/stdpghdr.html $ENV{HDREP}/$alpha/$login/addrmenutblhdr.html $ENV{HDREP}/$alpha/$login/menuaddrtbl.html $ENV{HDREP}/$alpha/$login/stdmenutblftr.html $ENV{HDREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
      system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/addrmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menuaddrtbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
   } else {
	if ($action eq "Appointments") {
           #system "/bin/cat $ENV{HDTMPL}/content.html $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menuappttbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html >$ENV{HDREP}/$alpha/$login/$biscuit.html";
           system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menuappttbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html >$ENV{HDREP}/$alpha/$login/$biscuit.html";
	} else {
	  if ($action eq "Collabrum") {
            #system "/bin/cat $ENV{HDTMPL}/content.html $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menucolltbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html >$ENV{HDREP}/$alpha/$login/$biscuit.html";
            system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/stdmenutblhdr.html $ENV{HDHREP}/$alpha/$login/menucolltbl.html $ENV{HDHREP}/$alpha/$login/stdmenutblftr.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html >$ENV{HDREP}/$alpha/$login/$biscuit.html";
	  } else {
	     if ($action eq "Profile") {
            #system "/bin/cat $ENV{HDTMPL}/content.html $ENV{HDREP}/$alpha/$login/searchpghdr.html $ENV{HDREP}/$alpha/$login/stdtblhdr.html $ENV{HDREP}/$alpha/$login/profile.html $ENV{HDREP}/$alpha/$login/profilepgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
            #system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html $ENV{HDHREP}/$alpha/$login/stdtblhdr.html $ENV{HDHREP}/$alpha/$login/profile.html $ENV{HDHREP}/$alpha/$login/profilepgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
            system "/bin/cat $ENV{HDHREP}/$alpha/$login/profile.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
	     } else {
	           if ($action eq "MemoCal") {
                      #system "/bin/cat $ENV{HDTMPL}/content.html $ENV{HDREP}/$alpha/$login/searchpghdr.html $ENV{HDREP}/$alpha/$login/stdtblhdr.html $ENV{HDREP}/$alpha/$login/memocal.html $ENV{HDREP}/$alpha/$login/memocalpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
                      #system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html $ENV{HDHREP}/$alpha/$login/stdtblhdr.html $ENV{HDHREP}/$alpha/$login/memocal.html $ENV{HDHREP}/$alpha/$login/memocalpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
                      system "/bin/cat $ENV{HDHREP}/$alpha/$login/memocalpghdr.html $ENV{HDHREP}/$alpha/$login/stdtblhdr.html $ENV{HDHREP}/$alpha/$login/memocal.html $ENV{HDHREP}/$alpha/$login/memocalpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
	           } else {
                     if ($action eq "Import") {
                      system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/importmenu.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
                     } else {
                          if ($action eq "Export") {
                             system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/exportmenu.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
                          } else {
                             if ($action eq "Groups") {
                               system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdpghdr.html $ENV{HDHREP}/$alpha/$login/menugrouptbl.html $ENV{HDHREP}/$alpha/$login/stdpgftr.html > $ENV{HDREP}/$alpha/$login/$biscuit.html";
                             }
                          }
                     }
                   }
	        }
	    } 
        }
    }

   if ($action eq "Faq") {
      #system "/bin/cat $ENV{HDTMPL}/content.html";
      hdsystemcat "$ENV{HTTPHOME}/html/hd/faq.html";
   } else { 
      #system "/bin/cat $ENV{HDTMPL}/content.html";
      #print "Cookie = \"$ENV{'HTTP_COOKIE'}\"<BR>";
      #system "/bin/cat $ENV{HDREP}/$alpha/$login/$biscuit.html";
      hdsystemcat "$ENV{HDREP}/$alpha/$login/$biscuit.html";
   } 

# save the info in db
   tied(%sesstab)->sync();
   #tied(%logtab)->sync();
   tied(%memotab)->sync();
   tied(%logsess)->sync();
}

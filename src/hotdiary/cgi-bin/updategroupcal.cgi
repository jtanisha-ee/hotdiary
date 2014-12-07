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
# FileName: updategroupcal.cgi
# Purpose: New HotDiary Update Group Calendar
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
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
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
      status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
      status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      exit;
   }



   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };

                tie %activetab, 'AsciiDB::TagFile',
                DIRECTORY => "$ENV{HDDATA}/aux/activetab",
                SUFIX => '.rec',
                SCHEMA => {
                     ORDER => ['login', 'acode', 'verified' ] };

   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }
                           
   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 
                 'listed', 'readonly' ] };

   # bind leditgrouptab table vars
   tie %leditgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/leditgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'jiveit', 'publicedit' ] };


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
          $logo = $jivetab{$jp}{logo};
          $title = $jivetab{$jp}{title};
          $banner = $jivetab{$jp}{banner};
          $label = $title;
   } else {
          if (exists $lictab{$HDLIC}) {
             $partner = $lictab{$HDLIC}{partner};
             if (exists $parttab{$partner}) {
                $logo = $parttab{$partner}{logo};
                $title = $parttab{$partner}{title};
                $banner = adjusturl $parttab{$partner}{banner};
                $label = $title;
             }
          }
   }

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }

   $ctype = $input{'ctype'};
   $calname = $input{'calname'};
   $caltitle = trim $input{'caltitle'};
   $corg = trim $input{'corg'};
   $listed = trim $input{'listed'};
   hddebug "listed = $listed";
   $readonly = $input{'readonly'};
   if ($caltitle eq "") {
      status("$login: Group title is empty. Please specify a group title.");
      exit;
   }
   if (notDesc $caltitle) {
      status("$login: Invalid characters in group title.");
      exit;
   }

   #if ($corg eq "") {
   #   status("$login: Organization/Company Name of Calendar is empty. Please specify a Organization/Company Name");
   #   exit;
   #}

   if (notDesc $corg) {
      status("$login: Invalid characters in Organization/Company Name of Calendar.");
      exit;
   }


   $calpassword = trim $input{'calpassword'};
   $calpassword = "\L$calpassword";
   if (notDesc $calpassword) {
      status("$login: Invalid characters in group password.");
      exit;
   }

   $calrpassword = trim $input{'calrpassword'};
   $calrpassword = "\L$calrpassword";
   if (notDesc $calrpassword) {
      status("$login: Invalid characters in group repeat password.");
      exit;
   }

   if ($calpassword ne $calrpassword) {
      status("$login: Calendar password field and the repeat password field do not match. Please use the Back button and enter identical passwords.");
      exit;
   }
 
   #$invitemsg = "";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };      
 
   $contact = $input{'contact'};
   hddebug "contact = $contact";
   if ($contact ne "") {
      $eventdetails .= "Calendar Master Name:  $logtab{$login}{fname} $logtab{$login}{lname}\n"; 
      $eventdetails .= "Calendar Id: $calname \n";
      $eventdetails .= "Calendar Title: $caltitle \n";
      $eventdetails .= "Calendar Type: $ctype \n";
      $eventdetails .= "Organization Company/Name: $corg \n"; 
      $eventdetails .= "Calendar Password:  $calpassword \n"; 
   }

   $mname = $login;
   (@hshemail) = split ",", $contact;
   $cntr = 0;
   hddebug "email = $#hshemail";

   # bind surveytab table vars
   tie %surveytab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/surveytab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
		'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority', 
		'editcal', 'calpeople'] };

   $acode = "";
   foreach $cn (@hshemail) {
       $cntr = $cntr + 1;
       $cn = "\L$cn";
       $cn = trim $cn;
       hddebug "cn = $cn";
       hddebug "mname = $mname";
       if ("\L$logtab{$mname}{email}" eq $cn) {
          next;
       }

       if ($cn eq "") {
          next;
       }

       if (exists ($logtab{$cn} ) ) {
          if ($surveytab{$cn}{calinvite} ne "CHECKED") {
             #$invitemsg .= "<BR><FONT COLOR=ff0000>$cn specified in your invitation list prefers not to receive invitations from others.</FONT>";
             #hddebug "invitemsg = $invitemsg";
             next;
          }
          $login_db = $cn;
          $cn = $logtab{$cn}{email};
          $eemail = 1;
          $oldlogin = $login_db;
          hddebug "oldlogin = $login_db";
       } else {
          ($login_db, $domain) = split '@', $cn;
          $login_db = trim $login_db;
          $eemail = 0;
       }

       hddebug "login_db = $login_db"; 
       if ($login_db =~ /\&/) {
          next;
       }
       #if ( (!(notLogin $login_db)) || (exists ($logtab{$login_db} )) ) {
       if ( (notLogin $login_db) || (exists ($logtab{$login_db} )) ) {
          if ($eemail ne "1") {
             $oldlogin = $login_db;
             if (exists($logtab{$login_db} )) {
                $login_db = "l$login_db$$-$cntr";
             }
             hddebug "login = $login_db";
          }
       }
       #if (!exists ($logtab{$login_db} )) {
       hddebug "login does notexist = $login_db eemail =$eemail"; 
          if ($eemail ne "1") {
             $logtab{$login_db}{'login'} = $login_db;
             $logtab{$login_db}{'fname'} = $login_db;
             $logtab{$login_db}{'password'} = $login_db;
             $logtab{$login_db}{'email'} = $cn;
             $surveytab{$login_db}{'login'} = $login_db;
             $surveytab{$login_db}{'hearaboutus'} = "Friend";
             $surveytab{$login_db}{'browser'} = $ENV{'HTTP_USER_AGENT'};
             tied(%surveytab)->sync();
             if ($jp eq "") {
                $pidd = $$;
                $acode = rand $pidd;
                $acode = $acode % $pidd;
      
                $activetab{$login_db}{login} = $login_db;
                $activetab{$login_db}{acode} = $acode;
                $activetab{$login_db}{verified} = "false";

             } 
          }


       hddebug "oldlogin = $oldlogin";
       if (!exists $logtab{$oldlogin}) {
          next;
       }
       $emsg = "Dear $logtab{$oldlogin}{fname}, \n \n";
       $uname = $logtab{$mname}{'fname'} . " " . $logtab{$mname}{'lname'};
       $emsg .= "You have been invited by $uname to join group.\n\n";
       $emsg .= "Calendar Details: \n";
       $emsg .=  $eventdetails;
       $emsg .=  "\n\n";
       $emsg .= "If you would like to contact $uname directly, please send an email to $uname at $logtab{$mname}{'email'}. $uname's member login ID on HotDiary is \"$mname\".\n";

       if ($eemail ne "1") {
          $emsg .= "\nName: $logtab{$login_db}{'fname'} $logtab{$login_db}{'lname'}\n";
          $emsg .= "Login: $login_db \n";
          $emsg .= "Password: $logtab{$login_db}{'password'}\n\n";
          if ($jp eq "") {
             $emsg .= "Activation Code: $acode\n\n";
          }
          $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
       }

       $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
       $emsg .= "HotDiary ($hddomain80) - New Generation Calendaring Products and Services\n";

       qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
       $logtab{$login_db}{email} = trim $logtab{$login_db}{email};
       if ($logtab{$login_db}{email} =~ /\s/) {
          status "Found spaces in email addresses ($logtab{$login_db}{email}). Please separate email addresses with a comma.";
          exit;
       }
       if (notEmailAddress $logtab{$login_db}{email}) {
          status "Invalid format in email address ($logtab{$login_db}{email}). Please specify correct email address.";
          exit;
       }
       #qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login_db}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};
       qx{metasend -b -S 800000 -m \"text/plain\" -f $ENV{HDHOME}/tmp/reginviteletter$$ -s \"Invitation From $uname\" -e \"\" -t \"$logtab{$login_db}{email}\" -F \"$uname <$logtab{$mname}{'email'}>\"};


       $alphaindex = substr $login_db, 0, 1;
       $alphaindex = $alphaindex . '-index';

       if ($eemail ne "1") {
           system "/bin/mkdir -p $ENV{HDREP}/$alphaindex/$login_db";
           system "/bin/chmod 755 $ENV{HDREP}/$alphaindex/$login_db";
           system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphaindex/$login_db";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login_db";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login_db";
           system "/bin/touch $ENV{HDDATA}/$alphaindex/$login_db/addrentrytab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login_db/addrentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login_db/addrtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login_db/addrtab";
           system "/bin/touch $ENV{HDDATA}/$alphaindex/$login_db/apptentrytab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login_db/apptentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login_db/appttab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login_db/appttab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login_db/personal/pgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login_db/subscribed/sgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login_db/founded/fgrouptab";
           system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$login_db";
           system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login_db/index.html";
           system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$login_db";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login_db/calendar_events.txt";

           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login_db/faxtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login_db/faxtab";

           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login_db/faxdeptab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login_db/faxdeptab";
        }
        if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login_db/subscribed/sgrouptab")) {
           system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login_db/subscribed/sgrouptab";
           system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login_db/subscribed/sgrouptab";
        }
        tie %sgrouptab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login_db/subscribed/sgrouptab",
        SUFIX => '.rec',
        SCHEMA => {
           ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
        if (!(exists $sgrouptab{$calname})) {
     hddebug "calname $calname does not exist in $login_db subscribed";
           $sgrouptab{$calname}{'groupname'} = $calname;
           $sgrouptab{$calname}{'groupfounder'} = $lgrouptab{$calname}{'groupfounder'};
           $sgrouptab{$calname}{'grouptype'} = $lgrouptab{$calname}{'grouptype'};
           $sgrouptab{$calname}{'grouptitle'} = $lgrouptab{$calname}{'grouptitle'};
           $sgrouptab{$calname}{'groupdesc'} = $lgrouptab{$calname}{'groupdesc'};
           $sgrouptab{$calname}{'password'} = $lgrouptab{$calname}{'password'};
           $sgrouptab{$calname}{'ctype'} = $lgrouptab{$calname}{'ctype'};
           $sgrouptab{$calname}{'cpublish'} = $lgrouptab{$calname}{'cpublish'};
           tied(%sgrouptab)->sync();

           system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$calname/usertab";
           system "/bin/chmod 755 $ENV{HDDATA}/listed/groups/$calname/usertab";
           tie %usertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/listed/groups/$calname/usertab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['login'] };
           $usertab{$login_db}{'login'} = $login_db;
           tied(%usertab)->sync();
        }
    }



   $cdesc = $input{'cdesc'};
   if (notDesc $cdesc eq "") {
      status("$login: Invalid characters in group description.");
      exit;
   }

   $alpha1 = substr $login, 0, 1;
   $alpha1 = $alpha1 . '-index';

   if (!(-d "$ENV{HDDATA}/groups/$alpha1/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alpha1/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alpha1/$login/founded/fgrouptab";
   }
   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alpha1/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


   $lgrouptab{$calname}{'grouptitle'} = $caltitle;
   $lgrouptab{$calname}{'groupdesc'} = $cdesc;
   $lgrouptab{$calname}{'password'} = $calpassword;
   $lgrouptab{$calname}{'ctype'} = $ctype;
   $lgrouptab{$calname}{'corg'} = $corg;
   $lgrouptab{$calname}{'listed'} = $listed;
   $lgrouptab{$calname}{'readonly'} = $readonly;

   $fgrouptab{$calname}{'grouptitle'} = $caltitle;
   $fgrouptab{$calname}{'groupdesc'} = $cdesc;
   $fgrouptab{$calname}{'password'} = $calpassword;
   $fgrouptab{$calname}{'ctype'} = $ctype;
   $fgrouptab{$calname}{'corg'} = $corg;

   $publicedit = $input{publicedit};
   $leditgrouptab{$calname}{groupname} = $calname;
   $jiveit = $input{jiveit};
   if ($jiveit eq "") {
      $jiveit = $jp;
   } 
   $leditgrouptab{$calname}{jiveit} = $jiveit;
   if ($publicedit eq "on") {
      $publicedit = "CHECKED";
   }
   $leditgrouptab{$calname}{publicedit} = $publicedit;
   tied(%leditgrouptab)->sync();

   if ($publicedit eq "CHECKED") {
      if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$calname")) {
	 system "mkdir -p $ENV{HTTPHOME}/html/hd/contacts/$calname";
	 system "chmod 755 $ENV{HTTPHOME}/html/hd/contacts/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/contacts/index.cgi $ENV{HTTPHOME}/html/hd/contacts/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDCGI}/contacts/webpage.cgi $ENV{HTTPHOME}/html/hd/contacts/$calname";
      }

      if (!(-d "$ENV{HTTPHOME}/html/hd/addressbook/$calname")) {
          system "ln -s $ENV{HTTPHOME}/html/hd/contacts/$calname $ENV{HTTPHOME}/html/hd/addressbook";
      }
   } else {
      if (-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/index.cgi") {
         system "rm -f $ENV{HTTPHOME}/html/hd/contacts/$calname/index.cgi";
      }
      if (-f "$ENV{HTTPHOME}/html/hd/contacts/$calname/webpage.cgi") {
         system "rm -f $ENV{HTTPHOME}/html/hd/contacts/$calname/webpage.cgi";
      }
      if (-d "$ENV{HTTPHOME}/html/hd/addressbook/$calname") {
         system "rm -f $ENV{HTTPHOME}/html/hd/addressbook/$calname";
      }
   }

   $cpublish = $input{'cpublish'};
   $lgrouptab{$calname}{'cpublish'} = $cpublish;
   tied(%lgrouptab)->sync();
   if ($cpublish eq "on") {
      $logtab{$login}{referer} = $jp; 
      tied(%logtab)->sync();
      if (!(-d "$ENV{HTTPHOME}/html/hd/groups/$calname"))  {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/groups/$calname";
         if ($hs eq "") {
             $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/groups/$calname\">http://$vdomain/groups/$calname</a>.";
         } else {
             $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/$hs/groups/$calname\">http://$vdomain/$hs/groups/$calname</a>.";
         }
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/groups/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/groups/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/groups/$calname/webpage.cgi")) {
         system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/groups/$calname";
      }
   } else {
      if (-d "$ENV{HTTPHOME}/html/hd/groups/$calname")  {
         if ($calname ne "") {
            if (-f "$ENV{HTTPHOME}/html/hd/groups/$calname/index.cgi") {
                system "rm -f $ENV{HTTPHOME}/html/hd/groups/$calname/index.cgi";
            }
         }
         if ($calname ne "") {
           if (-f "$ENV{HTTPHOME}/html/hd/groups/$calname/webpage.cgi") {
              system "rm -f $ENV{HTTPHOME}/html/hd/groups/$calname/webpage.cgi";
           }
         }
         if ($calname ne "") {
            if (-d "$ENV{HTTPHOME}/html/hd/groups/$calname")  {
               system "rmdir $ENV{HTTPHOME}/html/hd/groups/$calname";
               $cmsg = "<p>$p2 has removed your  website for you.";
            }
         } 
      }
   }

   $rh = $input{'rh'};
   $msg = "$login: $calname updated. Password is $calpassword"; 
   $msg = replacewithplus($msg);

if ($rh eq "") {
      $pcgi = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&os=$os";
   } else {
      $pcgi = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&rh=$rh&os=$os";
   }


      $prml = "";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha1/$login/ugc-$biscuit-$$.html";
      $prml = strapp $prml, "login=$login";
#
      if ($rh eq "") {
         $cgi = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
      } else {
         $cgi = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
      }

      $searchcal = adjusturl "$cgi&f=sgc";
      $prml = strapp $prml, "logo=";
      $prml = strapp $prml, "searchcal=$searchcal"; 
      $createcal = adjusturl "$cgi&f=cpc";
      $prml = strapp $prml, "createcal=$createcal";  
      $prml = strapp $prml, "welcome=Welcome";
      if ($rh eq "") {
         $cgis = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
      } else {
         $cgis = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
      }

      $prml = strapp $prml, "home=$cgis"; 
      $pgroups = $input{'pgroups'};

      $prml = strapp $prml, "redirecturl=$pcgi";

      $hiddenvars = gethiddenvars($hiddenvars);
      $hiddenvars = adjusturl $hiddenvars;
      $prml = strapp $prml, "hiddenvars=$hiddenvars"; 
      $prml = strapp $prml, "logo=$logo"; 
      parseIt $prml;
      hddebug "$ENV{HDREP}/$alpha1/$login/ugc-$biscuit-$$.html";
      hdsystemcat "$ENV{HDREP}/$alpha1/$login/ugc-$biscuit-$$.html";
      

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   #tied(%logtab)->sync();
   tied(%activetab)->sync();


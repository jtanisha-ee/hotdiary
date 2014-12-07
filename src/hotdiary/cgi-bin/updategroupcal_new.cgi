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

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
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
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("Invalid session or session does not exists. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
      $login = $sesstab{$biscuit}{'login'};
      if ($login eq "") {
         error("Login is an empty string. Possibly invalid session.\n");
         exit;
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      exit;
   }


   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };

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


   $ctype = $input{'ctype'};
   $calname = $input{'calname'};
   $caltitle = trim $input{'caltitle'};
   $corg = trim $input{'corg'};
   $listed = trim $input{'listed'};
   $readonly = $input{'readonly'};
   if ($caltitle eq "") {
      status("$login: Calendar title is empty. Please specify a calendar title.");
      exit;
   }
   if (notDesc $caltitle) {
      status("$login: Invalid characters in calendar title.");
      exit;
   }

   if ($corg eq "") {
      status("$login: Organization/Company Name of Calendar is empty. Please specify a Organization/Company Name");
      exit;
   }

   if (notDesc $corg) {
      status("$login: Invalid characters in Organization/Company Name of Calendar.");
      exit;
   }


   $calpassword = trim $input{'calpassword'};
   $calpassword = "\L$calpassword";
   if (notDesc $calpassword) {
      status("$login: Invalid characters in calendar password.");
      exit;
   }

   $calrpassword = trim $input{'calrpassword'};
   $calrpassword = "\L$calrpassword";
   if (notDesc $calrpassword) {
      status("$login: Invalid characters in calendar repeat password.");
      exit;
   }

   if ($calpassword ne $calrpassword) {
      status("$login: Calendar password field and the repeat password field do not match. Please use the Back button and enter identical passwords.");
      exit;
   }
 
   if (($calpassword ne "") && ((length $calpassword) < 6)) {
      status ("$login: If you wish to password-protect your calendar, you must specify a password of minimum 6 letters. This is to ensure the security of your calendar. Password protection is only an option. If you do not specify a password, everyone will be able to subscribe to it as long as they know the name of your calendar. However, you can restrict all other than yourself from editing it, by using an option at the bottom of this page.");
      exit;
   }

   #$contact = $input{'contact'};
   #if ($contact ne "") {
   #   $eventdetails .= "Calendar Name: $etitle \n";
   #   $eventdetails .= "Calendar Title: $edtype \n";
   #   $eventdetails .= "Calendar Type: $edtype \n";
   #   $eventdetails .= "Organization Company/Name:  \n"; 
   #   $eventdetails .= "Calendar Master Name:  \n"; 
   #}

   $mname = $login;
   #(@hshemail) = split ",", $contacts;
   $cntr = 0;
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
          $login = $cn;
          $cn = $logtab{$cn}{email};
          $eemail = 1;
          $oldlogin = $login;
       } else {
          ($login, $domain) = split '@', $cn;
          $login = trim $login;
          $eemail = 0;
       }

       if ($login =~ /\&/) {
          next;
       }
       if ( (!(notLogin $login)) || (exists ($logtab{$login} )) ) {
          if ($eemail ne "1") {
             $oldlogin = $login;
             if (exists($logtab{$login} )) {
                $login = "l$login$$-$cntr";
             }
             hddebug "login = $login";
          }
       }
       #if (!exists ($logtab{$login} )) {
          if ($eemail ne "1") {
             $logtab{$login}{'login'} = $login;
             $logtab{$login}{'fname'} = $login;
             $logtab{$login}{'password'} = $login;
             $logtab{$login}{'email'} = $cn;
             # bind surveytab table vars
             tie %surveytab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/surveytab",
               SUFIX => '.rec',
               SCHEMA => {
               ORDER => ['login', 'hearaboutus', 'browser', 'rhost'] };
             $surveytab{$login}{'login'} = $login;
             $surveytab{$login}{'hearaboutus'} = "Friend";
             $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
             tied(%surveytab)->sync();
          }


          $emsg = "Dear $logtab{$oldlogin}{fname}, \n \n";
          $uname = $logtab{$mname}{'fname'} . " " . $logtab{$mname}{'lname'};
          $emsg .= "You have been invited by $uname to an event. \n \n";
          $emsg .= "Event Details: \n";
          $emsg .=  $eventdetails;
          $emsg .=  "\n\n";
          $emsg .= "If you would like to contact $uname directly, please send an email to $uname at $logtab{$mname}{'email'}. $uname's member login ID on HotDiary is \"$mname\".\n";

          if ($eemail ne "1") {
             $emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
             $emsg .= "Login: $login \n";
             $emsg .= "Password: $logtab{$login}{'password'}\n\n";
             $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
          }

          $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
          $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Internet Products and Services\n";

          qx{echo \"$emsg\" > /var/tmp/reginviteletter$$};
          qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login}{email} < /var/tmp/reginviteletter$$};

          if ($eemail ne "1") {
             system "/bin/mkdir -p $ENV{HDREP}/$login";
             system "/bin/chmod 755 $ENV{HDREP}/$login";
             system "/bin/mkdir -p $ENV{HDHOME}/rep/$login";
             system "/bin/mkdir -p $ENV{HDDATA}/$login";
             system "/bin/chmod 755 $ENV{HDDATA}/$login";
             system "/bin/touch $ENV{HDDATA}/$login/addrentrytab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/addrentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$login/addrtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/addrtab";
             system "/bin/touch $ENV{HDDATA}/$login/apptentrytab";
             system "/bin/chmod 660 $ENV{HDDATA}/$login/apptentrytab";
             system "/bin/mkdir -p $ENV{HDDATA}/$login/appttab";
             system "/bin/chmod 770 $ENV{HDDATA}/$login/appttab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/personal/pgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/subscribed/sgrouptab";
             system "/bin/mkdir -p $ENV{HDDATA}/groups/$login/founded/fgrouptab";
             system "/bin/chmod -R 770 $ENV{HDDATA}/groups/$login";
             system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";
             system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$login";
             system "/bin/chmod 775 $ENV{HDDATA}/$login/calendar_events.txt";

             system "/bin/mkdir -p $ENV{HDDATA}/$login/faxtab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/faxtab";

             system "/bin/mkdir -p $ENV{HDDATA}/$login/faxdeptab";
             system "/bin/chmod 755 $ENV{HDDATA}/$login/faxdeptab";
          }
    }

   $cdesc = $input{'cdesc'};
   if (notDesc $cdesc eq "") {
      status("$login: Invalid characters in calendar description.");
      exit;
   }

   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$login/founded/fgrouptab",
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

   $cpublish = $input{'cpublish'};
   $lgrouptab{$calname}{'cpublish'} = $cpublish;
   if ($cpublish eq "on") {
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

   $prml = "";
   $msg = "$login: $calname updated. Password is $calpassword"; 
   $msg = replacewithplus($msg);
   $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$login/ugc-$biscuit-$$.html";
   $prml = strapp $prml, "login=$login";

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
   if ($rh eq "") {
      $pcgi = adjusturl "/cgi-bin/execgroupcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&os=$os";
   } else {
      $pcgi = adjusturl "/cgi-bin/$rh/execgroupcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&rh=$rh&os=$os";
   }

   $prml = strapp $prml, "redirecturl=$pcgi";
   parseIt $prml;
   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDREP}/$login/ugc-$biscuit-$$.html";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   #tied(%logtab)->sync();


#!usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: topcal.cgi
# Purpose: top html for cal mgmt tools
# This program is invoked by newindex.html file
# Creation Date: 09-10-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use AsciiDB::TagFile;
use utils::utils;
use calutil::calutil;
use tparser::tparser;

&ReadParse(*input); 

$jp = $input{jp};
$vdomain = $input{'vdomain'};
$vdomain = "\L$vdomain";
if ($vdomain =~ /www/) {
   $vdomain =~ s/www\.//g;
}


$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

# bind login table vars

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };

   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 
	'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 
	'calpublish', 'referer'] };


# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };


$login = trim $input{login};
$login = "\L$login";

$fchar = substr $login, 0, 1; 
$alphaindex = $fchar . '-index';
#hddebug "$alphaindex";

if ($login eq "") {
   status("Please specify a non-empty login name.");
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

# bind logsess table vars
   tie %accounttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab/accounttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login'] };


if ( (!(-f "$ENV{HDDATA}/logtab/$login.rec")) &&
       (-f "$ENV{HDDATA}/yplogtab/$login.rec") ) {
   system "mv $ENV{HDDATA}/yplogtab/$login.rec $ENV{HDDATA}/logtab";
}

if ( (!(-f "$ENV{HDDATA}/surveytab/$login.rec")) &&
       (-f "$ENV{HDDATA}/ypsurveytab/$login.rec") ) {
   system "mv $ENV{HDDATA}/ypsurveytab/$login.rec $ENV{HDDATA}/surveytab";
}

if (!(exists $logtab{$login})) {
   hddebug "login = $login";
   if (! notEmailAddress $login) {
      $msg100 = "$login resembles an email address. Please enter your member login. When you registered, the member login should have been mailed to your email address.";
   }
   if ($login =~ /\s/) {
      $sp100 = "You seem to have spaces in your login. Spaces are not allowed in the login name. Please check your login name and try again.";
   }
   status("Member login $login does not exist. $sp100 $msg100 Click <a href=\"http://$vdomain/\">here</a> to go back to top page.");
   exit;
}

# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };


$password = trim $input{password};
$password = "\L$password";
if ("\L$password" ne "\L$logtab{$login}{password}") {
   if ( (exists $activetab{$login}) && ($password eq $activetab{$login}{acode}) ) {
      hddebug "Customer entered activation code instead of password";
   } else {
      if ( ("\L$vdomain" eq "\L$hotdiary") ||
            ("\L$vdomain" eq "\L$diary") ) {
          $m100 = "Click on <a href=\"$hddomain/forgotpasswd.html\">Forgot Password</a> to have your password and other account information emailed to you.";
      }
      status("The password you have specified for $login ($password) is invalid or the account $login does not exist. Your password should have been emailed to you to the email address you specified at the time of registration. $m100 For additional help, please access <a href=\"/accounthelp.html\">account help information</a>."); 
      exit;
   }
}

$remoteaddr = $input{ip};
$sessionid = getkeys();

# bake a biscuit
$biscuit = "$sessionid-$login-$remoteaddr";
$title = time();

# check if user has already logged in

if (!exists $logsess{$login}) {
   $sesstab{$biscuit}{'login'} = $login;
   $sesstab{$biscuit}{'biscuit'} = $biscuit;
   $sesstab{$biscuit}{'time'} = time();
   $logsess{$login}{'login'} = $login;
   $logsess{$login}{'biscuit'} = $biscuit;
} else {

    if (!exists $sesstab{$logsess{$login}{'biscuit'}}) {
       delete $logsess{$login};
       error("$login: Either your session has timed out or there is inconsistency in your session information. Please try to login again. If this problem persists, send us an email.");
       exit;
    }
# if session has not expired then, check if remote addr of current user
# is same as remote addr in sesstab table for this user
    if ((time() - $sesstab{$logsess{$login}{'biscuit'}}{'time'})
                < $SESSION_TIMEOUT) {
       ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         #if ($raddr eq $remoteaddr) {
            delete $sesstab{$logsess{$login}{'biscuit'}};
            delete $logsess{$login};
            $sesstab{$biscuit}{'biscuit'} = $biscuit;
            $sesstab{$biscuit}{'login'} = $login;
            $sesstab{$biscuit}{'time'} = time();
            $logsess{$login}{'login'} = $login;
            $logsess{$login}{'biscuit'} = $biscuit;
         #}
         #else {
            #error("$login: Intrusion detected. Access denied.\n");
            #exit;
         #}
# if session has expired then do not check for intrusion problem, since
# the user may have logged into one location, then travelled to another
# location and logged in from there with same login, but not within
# 3600 seconds.
   } else {
         ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
         delete $sesstab{$logsess{$login}{'biscuit'}};
         delete $logsess{$login};
         $sesstab{$biscuit}{'biscuit'} = $biscuit;
         $sesstab{$biscuit}{'login'} = $login;
         $sesstab{$biscuit}{'time'} = time();
         $logsess{$login}{'login'} = $login;
         $logsess{$login}{'biscuit'} = $biscuit;
   }
}

$msg500 = "For help on your account <a href=$hddomain/accounthelp.html>click here.</a>";

if ( (!exists $activetab{$login}) ||  ($jp ne "") || ( ($vdomain ne "$hotdiary") && ($vdomain ne "$diary") && ($vdomain ne "") ) ) {
   hddebug "arrived here $vdomain";
   $activetab{$login}{login} = $login;
   $activetab{$login}{acode} = $$;
   $activetab{$login}{verified} = "true";
} else {
   if ($activetab{$login}{verified} eq "false") {
      #if ($login eq "user601") {
      if ($password eq $logtab{$login}{password}) {
         if ($logtab{$login}{email} eq "") {
            $msg400 = "The password you have entered is correct. However, you haven't yet activated your account. For downloading certain products you will not need to activate your account. Your records indicate that we do not have your email address. So it will not be possible to mail you the activation code. Please <a href=\"contact_us.html\">contact us</a> and tell us your login and email address, and we will be happy to respond to you with your activation code. $msg500";
         } else {
            $msg400 = "The password you have entered is correct. However, you haven't yet activated your account. For downloading certain products you will not need to activate your account. $msg500";
         }
      } else {
         $msg400 = "You haven't yet activated your account. For downloading certain products you will not need to activate your account. $msg500";
      }
      status "$login: $msg400 Please click <a href=\"$hddomain/activateacc.shtml\">here</a> to activate your account. If you have registered recently, you should have received an email that contains your account activation code. (If we do not have your email address, you may not have received this email. In such a case you need to <a href=\"contact_us.html\">contact us</a> with your login and email address, so we can mail you your activation code.) You will need this activation code to activate your account. Once you have successfully activated your account, you will be able to sign-in to HotDiary.<p>If you have lost your activation code but remember the email address you used to register, please click <a href=\"/forgotpasswd.html\">here</a>. If you have lost both your activation code and your email address,
you may either <a href=\"$hddomain/quikregister.html\">register</a> again or contact us and we can fix the problem for you immediately.";
      exit;
      #}
   }
}


$rh = $input{rh};
$os = $input{os};
$HDLIC = $input{'HDLIC'};
hddebug "HDLIC = $HDLIC";
$jp = $input{'jp'};
hddebug "jp = $jp";
$hs = $input{'hs'};

# bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   hddebug "vdomain = $vdomain";

if (!(exists $lictab{$HDLIC})) {
   status("You do not have a valid license to use the application.");
   exit;
} else {
   if ($lictab{$HDLIC}{'vdomain'} eq "") {
      $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
      $ip = $input{'ip'};
      $lictab{$HDLIC}{'ip'} = "\L$ip";
   } else {
        if (!("\L$lictab{$HDLIC}{'vdomain'}" =~ "\L$vdomain")) {
           status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
           exit;
        }
   }
}

$mytime = time() + $ENV{HDCOOKIE_TIMEOUT};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime($mytime);
$wdaystr = getdaystr($wday);
$monstr = getmonthstr($mon+1);
$year += 1900;

$expirytime = "$wdaystr, $mday-$monstr-$year $hour:$min:$sec GMT";
hddebug "time = $expirytime";

if ($vdomain eq "") {
   $vdomain = "$hotdiary";
}

#if (("\L$vdomain" eq "$hotdiary") || 
#   ("\L$vdomain" eq "$diary")) {
   $hdbuttontools= "Diary Toolbox";
   $hdbuttontext= "Collabrum";
#}
   $profile= "My Profile"; 
   # $profiletxt= "Account, Setup..."; 
   $profiletxt= ""; 
#}

if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
   $icgi = "index.cgi?jp=$jp";
} else {
   $icgi = adjusturl "index.html";
}

if ($login eq "") {
   if ($hs eq "") {
      if ($jp ne "") {
         if ($jp ne "buddie") {
            status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.");
            exit;
         }
      }
      status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.");
   } else {
      status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.");
   }
   exit;
}

tie %parttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/partners/parttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['logo', 'title', 'banner'] };

$HDLIC = $input{HDLIC};

$logo = "";
if (exists $jivetab{$jp}) {
   $logo = $jivetab{$jp}{logo};
   $label = $jivetab{$jp}{title};
   $label = adjusturl $label;
} else {
   if (exists $lictab{$HDLIC}) {
      $partner = $lictab{$HDLIC}{partner};
      if (exists $parttab{$partner}) {
         $logo = $parttab{$partner}{logo};
         $label = $parttab{$partner}{title};
         $label = adjusturl $label;
       }
   }
}

if ( 
     (validvdomain($vdomain) eq "1")
   ) {
   $logo = "";
   $label = "";
}


$prml = "";
if ($logo ne "") {
   $logo = adjusturl "$logo";
} 

$prml = strapp $prml, "rh=$rh";
$prml = strapp $prml, "logo=$logo";
$prml = strapp $prml, "label=$label";
system "mkdir -p $ENV{HDREP}/$alphaindex/$login";
system "mkdir -p $ENV{HDHREP}/$alphaindex/$login";

      if (exists $accounttab{$login}) {
         system "/bin/mkdir -p $ENV{HDREP}/$alphaindex/$login";
         system "/bin/chmod 755 $ENV{HDREP}/$alphaindex/$login";
         system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphaindex/$login";
         system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login";
         system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login";
         system "/bin/touch $ENV{HDDATA}/$alphaindex/$login/addrentrytab";
         system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/addrentrytab";
         system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/addrtab";
         system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/addrtab";
         system "/bin/touch $ENV{HDDATA}/$alphaindex/$login/apptentrytab";
         system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/apptentrytab";
         system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/appttab";
         system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/appttab";
         system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/personal/pgrouptab";
         #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
         #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
         system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$login";
         system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login/index.html";
         system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$login";
         system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$login/calendar_events.txt";

         system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxtab";
         system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxtab";

         system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$login/faxdeptab";
         system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$login/faxdeptab";

         system "/bin/mkdir -p $ENV{HDHREP}/$alphaindex/$login";
         system "/bin/chmod 755 $ENV{HDHREP}/$alphaindex/$login";
      }

# if we reached here, the login was successful, display the choice screen

system "/bin/rm -f $ENV{HDREP}/$alphaindex/$login/*.html";
system "/bin/rm -f $ENV{HDHREP}/$alphaindex/$login/*.html";
system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$login/index.html";

$sc = $input{sc};
if ($os ne "nt") {
   $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
   $prml = strapp $prml, "formenc=$formenc";
   $execproxylogout = encurl "/proxy/execproxylogout.cgi";
   $execdeploypage =  encurl "execdeploypage.cgi";              
   $execcalclient =  encurl "execcalclient.jsp";              
   $execbusiness =  encurl "execbusiness.cgi";              
   $execgroupcal =  encurl "execgroupcal.cgi";              
   $execshowprofile = encurl "execshowprofile.cgi";              
   $execrewards = encurl "execrewards.cgi";              
   $execfilebrowser = encurl "execfilebrowser.cgi";              
   $execothermemberui = encurl "execothermemberui.cgi";              
   $execpartyplanner = encurl "execpartyplanner.cgi";              
   $execpersonaldir = encurl "execpersonaldir.cgi";
   $execcalpreferences = encurl "execcalpreferences.cgi";
   $execdiarychat = encurl "execdiarychat.cgi";
   $execbboard = encurl "execbboard.cgi";
   $execmemo = encurl "execmemo.cgi";
   $execnotes = encurl "execnotes.cgi";
   $execshowcommerceportal = encurl "execshowcommerceportal.cgi";
   $execcalpublish = encurl "execcalpublish.cgi";
} else {
   $prml = strapp $prml, "formenc=";
   $execproxylogout = "/proxy/execproxylogout.cgi";
   $execdeploypage =  "execdeploypage.cgi";              
   $execcalclient =  "execcalclient.jsp";              
   $execbusiness =  "execbusiness.cgi";              
   $execgroupcal =  "execgroupcal.cgi";              
   $execshowprofile =  "execshowprofile.cgi";              
   $execrewards = "execrewards.cgi";              
   $execfilebrowser = "execfilebrowser.cgi";              
   $execothermemberui = "execothermemberui.cgi";              
   $execpartyplanner = "execpartyplanner.cgi";              
   $execpersonaldir = "execpersonaldir.cgi";
   $execcalpreferences = "execcalpreferences.cgi";
   $execdiarychat = "execdiarychat.cgi";
   $execbboard = "execbboard.cgi";
   $execmemo = "execmemo.cgi";
   $execnotes = "execnotes.cgi";
   $execshowcommerceportal = "execshowcommerceportal.cgi";
   $execcalpublish = "execcalpublish.cgi";
}


$alphjp = substr $jp, 0, 1;
$alphjp = $alphjp . '-index';

if ($jp ne "") {
   if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/topcal.html") {
      $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/topcal.html";
   } else {
      $tmpl = "$ENV{HDTMPL}/topcal.html";
   }
} else {
   $tmpl = "$ENV{HDTMPL}/topcal.html";
}

$sessionheader = qx{cat $ENV{'HTTPJAVAHOME'}/sessionheader.html};
$sessionheader = adjusturl $sessionheader;
$sessionfooter = qx{cat $ENV{'HTTPJAVAHOME'}/sessionfooter.html};
$sessionfooter = adjusturl $sessionfooter;
$css = qx{cat $ENV{HTTPJAVAHOME}/css.html};
$css = adjusturl $css;


$hdcookie = adjusturl "hdlogin=$login";
# $expirytime = adjusturl "expires=$expirytime; domain=hotdiary.com; path=/;";
$expirytime = adjusturl "expires=$expirytime; domain=$vdomain; path=/;";
hddebug "hdcookie = $hdcookie";
$prml = strapp $prml, "template=$tmpl";
#$prml = strapp $prml, "template=$ENV{HDTMPL}/topcal.html";
$prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/topcal.html";
$prml = strapp $prml, "cracker=$hdcookie";
$prml = strapp $prml, "expirytime=$expirytime";
$prml = strapp $prml, "HTTP_COOKIE=$login";
$prml = strapp $prml, "biscuit=$biscuit";
$prml = strapp $prml, "jp=$jp";
$prml = strapp $prml, "hdbuttontools=$hdbuttontools";
$prml = strapp $prml, "hdbuttontext=$hdbuttontext";
$prml = strapp $prml, "indexlogin=$alphaindex";
$prml = strapp $prml, "profile=$profile";
$prml = strapp $prml, "profiletxt=$profiletxt";
$prml = strapp $prml, "execshowprofile=$execshowprofile";
$prml = strapp $prml, "execgroupcal=$execgroupcal";
$prml = strapp $prml, "execbusiness=$execbusiness";
$prml = strapp $prml, "execcalclient=$execcalclient";
$prml = strapp $prml, "execdeploypage=$execdeploypage";
$prml = strapp $prml, "execproxylogout=$execproxylogout";
$prml = strapp $prml, "execrewards=$execrewards";
$prml = strapp $prml, "rewards=My Rewards";
$prml = strapp $prml, "rewardstxt=Cash To Go...";
$prml = strapp $prml, "carryon=";
$prml = strapp $prml, "carryontxt=";
$prml = strapp $prml, "sessionheader=$sessionheader";
$prml = strapp $prml, "sessionfooter=$sessionfooter";
$prml = strapp $prml, "css=$css";

$theader = getTheader($jp);
$tmiddle = getTmiddle($jp);
$tfooter = getTfooter($jp);
$prml = strapp $prml, "theader=$theader";
$prml = strapp $prml, "tmiddle=$tmiddle";
$prml = strapp $prml, "tfooter=$tfooter";

$allusers = rand 250;
$allusers = 150 + $allusers % 250;

# Commented out - Need to be taken out
# $usermsg = "Registered Users: 1.6 m+ &nbsp;&nbsp;&nbsp;&nbsp;
# Users Currently Logged In: $allusers";

## currently commented out
#$usermsg = "&nbsp;&nbsp;&nbsp;&nbsp;Users Currently Logged In: $allusers";
#$prml = strapp $prml, "usermsg=$usermsg";

$prml = strapp $prml, "usermsg=";

if ($jp eq "") {
   $prml = strapp $prml, "maintarget=";
} else {
   $maintarget = adjusturl "target=_main";
   $prml = strapp $prml, "maintarget=$maintarget";
}
$diarychat = adjusturl "<a href=\"http://$vdomain/jsp/$rh/execdogeneric.jsp?p0=$execdiarychat&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\"><b>Diary Chat</b></a><BR><FONT SIZE=2>Java Chat</FONT>";

$bboard = adjusturl "<a href=\"http://$vdomain/jsp/$rh/execdogeneric.jsp?p0=$execbboard&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\"><b>Diary Board</b></a><BR><FONT SIZE=2>Bulletin Board</FONT>";

if ($jp eq "") {
   $prml = strapp $prml, "diarychat=$diarychat";
   #if ($login eq "mjoshi") {
      $prml = strapp $prml, "bboard=$bboard";
   #} else {
   #   $prml = strapp $prml, "bboard=";
   #}
} else {
   $diarychat = adjusturl "<font size=2 color=white><b>Diary Chat</b><br>Java Chat</font>";
   $prml = strapp $prml, "diarychat=$diarychat";
   $bboard = adjusturl "<font size=2 color=white><b>Diary Board</b><br>Bulletin Board</font>";
   $prml = strapp $prml, "bboard=$bboard";
}
if ( ($login eq "jjenner") || ($login eq "smitha") || ($login eq "buddie") || ($login eq "agudur") ) {
$prml = strapp $prml, "grouppublishtxt=Publish";
$grouppublish = adjusturl "<a href=\"http://$vdomain/jsp/$rh/execdogeneric.jsp?p0=$execcalpublish&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\"><b>Publish</b></a><BR><FONT SIZE=2>My Group Calendar Publishing...</FONT>";
$prml = strapp $prml, "grouppublish=$grouppublish";
} else {
#$prml = strapp $prml, "diarychat=";
$prml = strapp $prml, "grouppublish=";
$prml = strapp $prml, "grouppublishtxt=";
}

$prml = strapp $prml, "execshowcommerceportal=$execshowcommerceportal";
$prml = strapp $prml, "comportal=Premium Channel";
$prml = strapp $prml, "comportaltxt=Buy Products";

$prml = strapp $prml, "notes=Diary Pad";
$prml = strapp $prml, "notestxt=Notes, Scribe...";
$prml = strapp $prml, "execnotes=$execnotes";
$prml = strapp $prml, "callink=$callink";

$memo = adjusturl "<a href=\"http://$vdomain/jsp/$rh/execdogeneric.jsp?p0=$execmemo&p1=biscuit&p2=jp&pnum=3&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\"><b>Memo Manager</b></a>";

$memotxt = adjusturl "<BR>Memos/To-Do";

#if ( ( $login eq "mjoshi") || ($login eq "jjenner") || ($login eq "manoj") || ($login eq "smitha") || ($login eq "buddie") || ($login eq "agudur") ) {

   $prml = strapp $prml, "memo=$memo";
   $prml = strapp $prml, "memotxt=$memotxt";

#} else {
#   $prml = strapp $prml, "memo=";
#}
if ( ($vdomain eq "$hotdiary") || ($vdomain eq "$diary")) {
   $prml = strapp $prml, "flg=";
} else {
   $prml = strapp $prml, "flg=1";
}
$prml = strapp $prml, "framedomain=$vdomain";
$prml = strapp $prml, "partyplanner=";
$prml = strapp $prml, "partyplannertxt=";
$prml = strapp $prml, "execpartyplanner=";
$prml = strapp $prml, "address=Contact Manager";
$prml = strapp $prml, "addresstxt=My Address Book";
$prml = strapp $prml, "execpersonaldir=$execpersonaldir";
$prml = strapp $prml, "execcalpreferences=$execcalpreferences";

$prml = strapp $prml, "execothermemberui=$execothermemberui";
$prml = strapp $prml, "othercalendar=Share Calendar";
$prml = strapp $prml, "othercalendartxt=Others Calendar";

    $prml = strapp $prml, "execfilebrowser=$execfilebrowser";
    $prml = strapp $prml, "carryontxt=File Storage";
    $prml = strapp $prml, "carryon=My Carry-On";

  $balloon = adjusturl "<IMG SRC=\"$hddomain/images/balloon4.gif\" WIDTH=30 HEIGHT=50 BORDER=0>";
  
  #$prml = strapp $prml, "partyplanner=Party Invite<BR>$balloon";
  $prml = strapp $prml, "partyplanner=Party Invitation";
  $prml = strapp $prml, "partyplannertxt=Manage Parties";
  $prml = strapp $prml, "execpartyplanner=$execpartyplanner";

if ($sc eq "p") {
   $welcome = "Calendar Of";
} else {
   $welcome = "Welcome";
}
$prml = strapp $prml, "welcome=$welcome";
$prml = strapp $prml, "login=$login";
$prml = strapp $prml, "HDLIC=$HDLIC";
$prml = strapp $prml, "ip=$ip";
$prml = strapp $prml, "rh=$rh";
$prml = strapp $prml, "hs=$hs";
$prml = strapp $prml, "vdomain=$vdomain";
parseIt $prml, 1;



$pr = "";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$alphaindex/$login/d$biscuit.html";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/hotbutton.html";
      $pr = strapp $pr, "leftFrame=rep/$alphaindex/$login/l$biscuit.html";
      $pr = strapp $pr, "rightFrame=rep/$alphaindex/$login/$biscuit.html";
      #$label = "HotDiary Address Add/Search Menu.";
      #$label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      #$label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      #$logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      #$pr = strapp $pr, "login=$logi";
      #$pr = strapp $pr, "label=$label";
      #$pr = strapp $pr, "label1=$label1";
      #$pr = strapp $pr, "label2=$label2";
      $pr = strapp $pr, "biscuit=$biscuit";
      parseIt $pr, 1;
      $expiry = localtime(time() + 5);
      $expiry = "\:$expiry";
      $pr = "";
      $pr = strapp $pr, "alphaindex=$alphaindex";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/lhotbutton.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/exechotmenu.cgi";
      $pr = strapp $pr, "login=$login";
      $pr = strapp $pr, "calclient=$calclient";
      $pr = strapp $pr, "templateout=$ENV{HDREP}/$alphaindex/$login/l$biscuit.html";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "expiry=$expiry";
      parseIt $pr, 1;
      $pr = "";
      tie %hdtab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/hdtab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['title', 'logo', 'banner' ] };

if (exists $hdtab{$login}) {
         $t2 = adjusturl $hdtab{$login}{title};
         $banner = adjusturl $hdtab{$login}{banner};
      } else {
         $t2 = "HotDiary";
      }

      $label = "$t2 Address Add/Search Menu.";
      $label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      $label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      $logi = $login . "<BR><BR></i><b>" . localtime() . "</b>";
      $pr = strapp $pr, "login=$logi";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "label1=$label1";
      $pr = strapp $pr, "label2=$label2";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpghdr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdpghdr.html";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "expiry=";
      parseIt $pr, 1;

      $pr = "";
      $label = "$t2 Address Add/Search Menu.";
      $label2 = "To page someone in your diary, first Search, and then click on the pager icon. If you modify the pager number, press Update button, and re-search again from Add/Search menu before paging again.";
      $label1 = "To search entries, use the first few letters of Name(Person/Business) as key.";
      $pr = strapp $pr, "login=$login";
      $pr = strapp $pr, "label1=$label1";
      $pr = strapp $pr, "label=$label";
      $pr = strapp $pr, "biscuit=$biscuit";
      $buddy = "rep/$alphaindex/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/friend.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/friend.html";
      $buddy = "rep/$alphaindex/$login/friend$biscuit.html";
      $pr = strapp $pr, "buddy=$buddy";
      parseIt $pr, 1;
      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/friend.html > $ENV{HDREP}/$alphaindex/$login/friend$biscuit.html";
      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/addrmenutblhdr.html";
      $pr = strapp $pr, "actioncgi=cgi-bin/execaddraddsearch.cgi";
      $pr = strapp $pr, "biscuit=$biscuit";
      $pr = strapp $pr, "buddy=$buddy";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/addrmenutblhdr.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/menuaddrtbl.html";
$pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/menuaddrtbl.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdmenutblftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdmenutblftr.html";
      parseIt $pr, 1;

      $pr = "";
      $pr = strapp $pr, "template=$ENV{HDTMPL}/stdpgftr.html";
      $pr = strapp $pr, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdpgftr.html";
      parseIt $pr, 1;

      system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdpghdr.html $ENV{HDHREP}/$alphaindex/$login/addrmenutblhdr.html $ENV{HDHREP}/$alphaindex/$login/menuaddrtbl.html $ENV{HDHREP}/$alphaindex/$login/stdmenutblftr.html $ENV{HDHREP}/$alphaindex/$login/stdpgftr.html > $ENV{HDREP}/$alphaindex/$login/$biscuit.html";

      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execshowtopcalprog = adjusturl "/jsp/$rh/execdogeneric.jsp?p0=$execshowtopcal&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5";

      if (exists $accounttab{$login}) {
         status "$login: Congratulations for choosing to use HotDiary as your life-time organizer. Your temporary qualifier ID will be granted a permanent status to access HotDiary, if you so wish. Click <a href=\"$execshowtopcalprog\">here</a> to confirm your interest in registering for HotDiary's life-time free organizer.";
         delete $accounttab{$login};
         $logtab{$login}{informme} = "CHECKED";
         exit;
      }


#if ($login eq "mjoshi") {
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/topcal.html";
#} else {
#   system "cat $ENV{HDTMPL}/content.html";
#   system "cat $ENV{HDREP}/$alphaindex/$login/topcal.html";
#}
tied(%activetab)->sync();

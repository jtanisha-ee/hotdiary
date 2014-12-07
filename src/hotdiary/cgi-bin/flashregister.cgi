#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: flashregister.cgi
# Purpose: it quickly register users in hotdiary.
# Creation Date: 10-05-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
#use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Registration"); 

# bind active table vars
   tie %activetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/activetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'acode', 'verified' ] };


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

# bind flashtab table vars
   tie %flashtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/flashtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'email'] };

                       
  $email = trim $input{'email'};
##### CASE BEGIN
  $email = "\L$email";
  hddebug "Changed to lower case $email";
##### CASE END

  if ($email eq "") {
     status "Please enter a non-empty email address.";
     exit;
  }
  if (notEmailAddress $email) {
     status "Email address must have the correct format. Please enter a valid email address.<BR>(For example joe\@foo.com is a valid address.).";
     exit;
  }
  ($login, $host) = split '@', $email;
  $login = "\L$login";
  $alpha = substr $login, 0, 1;
  $alpha = $alpha . '-index';

  if ( (-f "$ENV{HDDATA}/yplogtab/$login.rec") &&
       (!(-f "$ENV{HDDATA}/logtab/$login.rec")) ) {
       system "mv $ENV{HDDATA}/yplogtab/$login.rec $ENV{HDDATA}/logtab/$login.rec";
  }

  if ( (exists $logtab{$login}) || (notLogin $login) ) {
     $login = $login . $$; 
  }
  if ( (exists $logtab{$login}) || (notLogin $login) ) {
     $key1 = substr (getkeys(), 0, 5);
     $login = $login . $key1;
  }
  hddebug "QuikRegister: Trying Member Login $login";
  if ( (exists $logtab{$login}) || (notLogin $login) ) {
     status "Could not find a unique and valid member login for your email address. Please use the <a href=\"register.html\">regular registration</a> process to register with HotDiary.";
     hddebug "Could not find a unique and valid member login for your email address. Please use the <a href=\"register.html\">regular registration</a> process to register with HotDiary.";
     exit;
  }
  (@words) = qx{cat $ENV{HDTMPL}/words.db};
  $rand = rand $#words;
  $rand = $rand % $#words;
  hddebug "rand = $rand";
  $password = $words[$rand];
  $password =~ s/\n//g;
  $password = "\L$password";

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
       ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
		 'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority', 
		'editcal', 'calpeople' ] };

# bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed' ] };

# bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'groups', 'logins' ] };

# bind personal list group table vars
# This table is useful when we are doing a Add group, and we want to make sure that
# the groupname is unique amoung all Listed as well as personal groups
   tie %plgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/personal/plgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' ] };


   $input{acceptit} = "on";
# check if login  record exists.
   if (exists $logtab{$login}) {
      status("Member login \"$login\" already exists. Please use another login. For example, $login$$.");
      exit;
   }

	  if ((exists $lgrouptab{$login}) || (exists $lmergetab{$login}) ||
              (exists $plgrouptab{$login})) {
            $login = "$login" . $$;
            if ((exists $lgrouptab{$login}) || (exists $lmergetab{$login}) ||
		(exists $plgrouptab{$login})) {
               status("Could not create a unique member login. Group with the same name as $login already exists. Names must be unique among group names and member login names. Try using another name, like $login$$.");
               exit;
            }
          }

          $input{fname} = $login;
          $logtab{$login}{'login'} = $login;
          $logtab{$login}{'password'} = $password;
          $logtab{$login}{'email'} = $email;
          $logtab{$login}{'checkid'} =  "CHECKED";
          $logtab{$login}{'calpublish'} =  "CHECKED";
          $logtab{$login}{'zone'} =  "-8";
          system "mkdir -p $ENV{HTTPHOME}/html/hd/members/$alpha/$login";
          if ($login ne "") {
             system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/members/$alpha/$login";
             system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/members/$alpha/$login";
          }
          $logtab{$login}{'informme'} = "CHECKED";
          $logtab{$login}{'pagertype'} = "Other Pager";
          $logtab{$login}{'fname'} = $input{fname};
          $logtab{$login}{'remoteaddr'} = $ENV{'REMOTE_ADDR'};
          $surveytab{$login}{'login'} = $login;
          $surveytab{$login}{'hearaboutus'} = "Windows Magazine/CMP Media";
          $surveytab{$login}{'browser'} = $ENV{'HTTP_USER_AGENT'};
          tied(%surveytab)->sync();
          $flashtab{$login}{login} = $login;
          $flashtab{$login}{email} = $email;
          tied(%flashtab)->sync();

          $msg = "<h3>Please Take A Print-Out Of This Page</h3>$login: Congratulations! You have been instantaneously registered for receiving news about flash templates from ShockTheWave.Com and HotDiary.Com. <p>HotDiary has automatically assigned you a unique member login ($login), password ($password). Please keep this information in a safe place. This information has also been mailed to the email address $email that you specified. <p>Note that you can also use this member ID to <a href=\"http://www.hotdiary.com/signin.shtml\">signin</a> to HotDiary."; 
             $msg .= "<b><p>An activation code has been mailed to your email address. Please activate your account before you login to HotDiary. Activation code is not necessary for JazzIt! and JiveIt! members. <p>Click <a href=\"http://www.hotdiary.com/activateacc.shtml\">here to activate your account</a>.</b>";

          $pidd = $$;
          $acode = rand $pidd;
          $acode = $acode % $pidd;
          
          $activetab{$login}{login} = $login;
          $activetab{$login}{acode} = $acode;
          $activetab{$login}{verified} = "false";

          #if ($email eq "redbasin\@hotdiary.com") {
             $prml = "";
             $prml = strapp $prml, "template=$ENV{HDTMPL}/regletter.html";
             $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/regletter-$login.html";
             $prml = strapp $prml, "login=$login";
             $prml = strapp $prml, "email=$email";
             $prml = strapp $prml, "password=$password";
             $prml = strapp $prml, "acode=$acode";
             $logo = adjusturl "http://www.hotdiary.com/images/newhdlogo.gif";
             $prml = strapp $prml, "logo=$logo";
             $prml = strapp $prml, "vdomain=www.hotdiary.com";
             $banner = adjusturl "<a href=\"http://www.hotdiary.com\" target=_main><IMG SRC=\"http://www.hotdiary.com/images/dotcombanner.gif\" BORDER=0></a>";
             $prml = strapp $prml, "banner=$banner";
             $prml = strapp $prml, "func=quikreg";
             $title = "HotDiary";
             $prml = strapp $prml, "title=$title";
             $activationmsg = '<p>Thank you for registering interest in ShockTheWave.Com flash templates. A representative from ShockTheWave.Com will contact you soon to process your query.<p>Your account activation code is ' . $acode . '. If you are reading this email in a web-enabled browser and are able to click on the link, please click <a href="http://www.hotdiary.com/cgi-bin/execverifyacc.cgi?login=' . $login . '&acode=' . $acode . '">here to activate your account.</a>' . "\n\n" . 'If you do not have a web-enabled browser, please visit http://www.hotdiary.com/activateacc.shtml to activate your account.';
             $activationmsg = adjusturl $activationmsg;
             $prml = strapp $prml, "activationmsg=$activationmsg";
             parseIt $prml;
             $esubject = "$title Registration Greeting";
             # send notification to pcontact@yahoo.com
             #system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/regletter-$login.html -s \"$esubject\" -e \"\" -t \"$email pcontact\@yahoo.com\" -F rhsup\@hotdiary.com";
             system "/usr/bin/metasend -b -S 800000 -m \"text/html\" -f $ENV{HDHOME}/tmp/regletter-$login.html -s \"$esubject\" -e \"\" -t \"$email\" -F rhsup\@hotdiary.com";
          #}
          #$emsg = "Dear $logtab{$login}{'fname'},\n";
          #$emsg .= qx{cat $ENV{'HDHOME'}/letters/regwelcome};
          #$emsg .= "\nName: $logtab{$login}{'fname'} $logtab{$login}{'lname'}\n";
          #$emsg .= "Login: $logtab{$login}{'login'}\n";
          #$emsg .= "Password: $logtab{$login}{'password'}\n\n";
          #if ($login eq "user600") {
             #$emsg .= 'Your account activation code is ' . $acode . '. If you are reading this email in a web-enabled browser and are able to click on the link, please click http://www.hotdiary.com/cgi-bin/execverifyacc.cgi?login=' . $login . '&acode=' . $acode . ' to activate your account.' . "\n\n" . 'If you do not have a web-enabled browser, please visit http://www.hotdiary.com/activateacc.shtml to activate your account.';
          #}

          #$emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
          #$emsg .= "HotDiary (http://www.hotdiary.com) - Innovative Internet Calendaring Products and Services\n";

          #qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/regletter$$};
          #qx{/bin/mail -s \"HotDiary Registration Confirmation\" $logtab{$login}{'email'} < $ENV{HDHOME}/tmp/regletter$$};

          system "/bin/mkdir -p $ENV{HDREP}/$alpha/$login";
	  system "/bin/chmod 755 $ENV{HDREP}/$alpha/$login";
          system "/bin/mkdir -p $ENV{HDHREP}/$alpha/$login";
	  system "/bin/chmod 755 $ENV{HDHREP}/$alpha/$login";
          system "/bin/mkdir -p $ENV{HDHOME}/rep/$alpha/$login";
          system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login";
          system "/bin/touch $ENV{HDDATA}/$alpha/$login/addrentrytab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/addrentrytab";
          system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/addrtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/addrtab";
          system "/bin/touch $ENV{HDDATA}/$alpha/$login/apptentrytab";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alpha/$login/apptentrytab";
          system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/appttab";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alpha/$login/appttab";
          system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/personal/pgrouptab";
          #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/subscribed/sgrouptab";
          #system "/bin/mkdir -p $ENV{HDDATA}/groups/$alpha/$login/founded/fgrouptab";
	  system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alpha/$login";
          system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alpha/$login/index.html";
          system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alpha/$login";
	  system "/bin/chmod 775 $ENV{HDDATA}/$alpha/$login/calendar_events.txt";

          system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/faxtab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/faxtab";

          system "/bin/mkdir -p $ENV{HDDATA}/$alpha/$login/faxdeptab";
	  system "/bin/chmod 755 $ENV{HDDATA}/$alpha/$login/faxdeptab";

          status($msg);
          #system "java COM.hotdiary.main.SendPage \"1412165\" \"fRegistration\" \"$login\"";
   #}


#synch the database
   tied(%logtab)->sync();
   tied(%activetab)->sync();
}

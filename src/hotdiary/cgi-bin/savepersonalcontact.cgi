#!/usr/local/bin/perl5
#
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
# FileName: savepersonalcontact.cgi 
# Purpose: add a personal contact to the folders
# Creation Date: 12-01-98
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("savepersonalcontact.cgi ");

   $vdomain = trim $input{'vdomain'};
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $jp = $input{jp}; 
   hddebug "jp = $jp";
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
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
              status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
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
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $sesstab{$biscuit}{'time'} = time();
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

   $rh = $input{rh};

   $street =  $input{street}; 
   if (notAddress($input{street})) {
       status("Invalid characters in Street Address ($input{'street'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{fname})) {
       status("Invalid characters in First Name ($input{'fname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{lname})) {
       status("Invalid characters in Last Name ($input{'lname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{busname})) {
       status("Invalid characters in Business Name ($input{'busname'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }


   if (notAddress($input{aptno})) {
       status("Invalid characters in Last Name ($input{'aptno'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{city})) {
       status("Invalid characters in City ($input{'city'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{state})) {
       status("Invalid characters in State ($input{'state'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notName($input{country})) {
       status("Invalid characters in Country ($input{'country'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notNumber($input{zipcode})) {
       status("Invalid characters in Zipcode ($input{'zipcode'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{hphone})) {
       status("Invalid characters in Home Phone ($input{'hphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{bphone})) {
       status("Invalid characters in Business Phone ($input{'bphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{cphone})) {
       status("Invalid characters in Cell Phone ($input{'cphone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{fax})) {
       status("Invalid characters in Fax ($input{'fax'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notPhone($input{pager})) {
       status("Invalid characters in Pager ($input{'pager'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notEmail($input{email})) {
       status("Invalid characters in Email ($input{'email'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }

   if (notUrl($input{url})) {
       status("Invalid characters in URL ($input{'url'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notDesc($input{other})) {
       status("Invalid characters in Other ($input{'other'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }
   if (notName($input{title})) {
       status("Invalid characters in Title ($input{'title'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
       exit;
   }


   $fname = trim $input{fname};
   $lname = trim $input{lname};
   $aptno = trim $input{aptno};
   $street = trim $input{street};
   $city = trim $input{city};
   $state = trim $input{state};
   $zipcode = trim $input{zipcode};
   $country = trim $input{country};
   $hphone = trim $input{hphone};
   $bphone = trim $input{bphone};
   $cphone = trim $input{cphone};
   $pager = trim $input{pager};
   $fax = trim $input{fax};
   $email = trim $input{email};
   $url = trim $input{url};
   $other = $input{other};
   $other = adjusturl $other;
   $title = trim $input{title};
   $bday = trim $input{bday};
   $bmonth = trim $input{bmonth};
   $byear = trim $input{byear};
   $pagertype = trim $input{pagertype};
   $busname = trim $input{busname};

   # indicates a new entry
   if ($input{newentry} == 0) {
     $entkey = getkeys();
   } else {
     $entkey = $input{entryno};
   }

   hddebug "newentry = $input{newentry}, $entkey";

   $fchar = substr $login, 0, 1;
   $alphaindex = $fchar . '-index';
   # bind address table vars
      tie %addrtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/addrtab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

      $addrtab{$entkey}{entryno} = $entkey;
      $addrtab{$entkey}{login} = $login;
      $addrtab{$entkey}{fname} = $fname;
      $addrtab{$entkey}{lname} = $lname;
      $addrtab{$entkey}{street} = $street;
      $addrtab{$entkey}{city} = $city;
      $addrtab{$entkey}{state} = $state;
      $addrtab{$entkey}{zipcode} = $zipcode;
      $addrtab{$entkey}{country} = $country;
      $addrtab{$entkey}{phone} = $hphone;
      $addrtab{$entkey}{pager} = $pager;
      $addrtab{$entkey}{pagertype} = $pagertype;
      $addrtab{$entkey}{fax} = $fax;
      $addrtab{$entkey}{cphone} = $cphone;
      $addrtab{$entkey}{bphone} = $bphone;
      $addrtab{$entkey}{email} = $email;
      $addrtab{$entkey}{url} = $url;
      $addrtab{$entkey}{id} = $id;
      $addrtab{$entkey}{other} = $other;
      $addrtab{$entkey}{aptno} = $aptno;
      $addrtab{$entkey}{busname} = $busname;
      $addrtab{$entkey}{bday} = $bday;
      $addrtab{$entkey}{bmonth} = $bmonth;
      $addrtab{$entkey}{byear} = $byear;
      $addrtab{$entkey}{title} = $title;
      $addrtab{$entkey}{busname} = $busname;
      tied(%addrtab)->sync();

   $checkid = $logtab{$login}{'checkid'};
   $autoinvite = $input{'autoinvite'};
   if (($autoinvite eq "on") && ($id eq "") && ($checkid eq "CHECKED")) {
        # bind surveytab table vars
        tie %surveytab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/surveytab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
'installation', 'domains', 'domain', 'orgrole', 'organization', 'orgsize', 
'budget', 'timeframe', 'platform', 'priority', 'editcal', 'calpeople' ] };

        $em = trim $input{'email'};
        $em = "\L$em";
        $em1 = $logtab{$login}{'email'};
        $em1 = "\L$em1";
        if ("\L$em" ne "\L$em1") {
        if (($em  ne "") && (!(notEmailAddress $em))) {
           $fn = trim $input{'fname'};
           $fn = "\L$fn";
           $fn =~ s/\s//g;
           $ln = trim $input{'lname'};
           $ln = "\L$ln";
           $ln =~ s/\s//g;
           if (!(exists $logtab{$fn})) {
              $logi = $fn;
           } else {
              $temp = "$fn-$ln";
              if (($ln ne "") && (!(exists $logtab{$temp}))) {
                 $logi = $temp;
              } else {
                   $temp = "$fn_$ln";
                   if  (($ln ne "") && (!(exists $logtab{$temp}))) {
                      $logi = $temp;
                   } else {
                      $temp = "$fn-$$";
                      if (!(exists $logtab{$temp})) {
                         $logi = $temp;
                      } else {
                           hderror "Autoinvite option was selected by $login. However, could not find a unique member login for the invitee. Invitee's first name was $fn, Invitee's last name was $ln, and Invitee's email was $em";
                      }
                   }
              }
           }
           if (($logi ne "")  && (!(notLogin $logi))) {
           $logtab{$logi}{'login'} = $logi;
           $logtab{$logi}{'fname'} = $fn;
           $logtab{$logi}{'lname'} = $ln;
           $logtab{$logi}{'email'} = $em;
           $logtab{$logi}{'password'} = $$;
           $surveytab{$logi}{'login'} = $logi;
           $surveytab{$logi}{'hearaboutus'} = "HotDiary Member";
           $emsg = "Dear $logtab{$logi}{'fname'},\n";
           $mname = $logtab{$login}{'fname'} . " " . $logtab{$login}{'lname'};
           $emsg .= "You have been invited by $mname to join http://www.hotdiary.com! If you would like to contact $mname directly, please send an email to $mname at $logtab{$login}{'email'}.\n";

           $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
           $emsg .= "\nName: $logtab{$logi}{'fname'} $logtab{$logi}{'lname'}\n";
           $emsg .= "Login: $logtab{$logi}{'login'}\n";
           $emsg .= "Password: $logtab{$logi}{'password'}\n\n";
           $emsg .= "Regards,\nHotDiary Inc.\n\n";
           $emsg .= "HotDiary (http://www.hotdiary.com) - New Generation Collaborative Internet Organizer\n";
 
           qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
           qx{/bin/mail -s \"Invitation From $mname\" $logtab{$logi}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};
           system "/bin/mkdir -p $ENV{HDREP}/$alphaindex/$logi";
           system "/bin/chmod 755 $ENV{HDREP}/$alphaindex/$logi";
           system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphaindex/$logi";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$logi";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$logi";
           system "/bin/touch $ENV{HDDATA}/$alphaindex/$logi/addrentrytab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$logi/addrentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$logi/addrtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$logi/addrtab";
           system "/bin/touch $ENV{HDDATA}/$alphaindex/$logi/apptentrytab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$logi/apptentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$logi/appttab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$logi/appttab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$logi/personal/pgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$logi/subscribed/sgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphaindex/$logi/founded/fgrouptab";
           system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphaindex/$logi";
           system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphaindex/$logi/index.html";
           system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphaindex/$logi";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphaindex/$logi/calendar_events.txt";
 
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$logi/faxtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$logi/faxtab";
 
           system "/bin/mkdir -p $ENV{HDDATA}/$alphaindex/$logi/faxdeptab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphaindex/$logi/faxdeptab";
           } else {
                hddebug "User $logi was not created or invited, because either it was a null user, or because it was not a validated login string.";
           }
        }
        }
     }


   if ($os ne "nt") {
      $execpersonaldir = encurl "execpersonaldir.cgi";
   } else {
      $execpersonaldir = "execpersonaldir.cgi";
   }

   $letter = substr $fname, 0, 1;

   $pcgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?pnum=5&p0=$execpersonaldir&p1=biscuit&p2=letter&p3=all&p4=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&letter=$letter&all=&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   $alpha1 = substr $login, 0, 1;
   $alpha1 = $alpha1 . '-index';

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha1/$login/spc-$biscuit-$$.html";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "logo=";
   $prml = strapp $prml, "welcome=Welcome";
   $prml = strapp $prml, "redirecturl=$pcgi";
   parseIt $prml;

   #hddebug "$pcgi";
   hdsystemcat "$ENV{HDREP}/$alpha1/$login/spc-$biscuit-$$.html";

   #status("$login: Your contact information has been added to addressbook. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=5&p0=$execpersonaldir&p1=biscuit&p2=letter&p3=all&p4=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&letter=$letter&all=&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to contact manager.");

   depositmoney $login;

   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   
}

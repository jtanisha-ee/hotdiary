#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: login.cgi
# Purpose: This program uses dataplates like other programs and checks for
# 	   user login and displays appropriate menus and error messages.
# 
# Creation Date: 10-09-97
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
#use UNIVERSAL qw(isa);
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = 3600;


# parse the command line
   &ReadParse(*input); 

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Profupdate"); 


   hddebug "Entered HotDiary proxyprofupdateGot login= $input{'login'}";
   hddebug "Entered HotDiary proxyprofupdate Got password = $input{'password'}";
   hddebug "Entered HotDiary proxyprofupdateGot biscuit = $input{'biscuit'}";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite'] };

 
   $login = trim $input{'login'};
   
   $vdomain = trim $input{'vdomain'};
   $os = $input{'os'};
   $hs = $input{'hs'};
   $jp = $input{'jp'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

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

##### CASE BEGIN
   $login = "\L$login";
   hddebug "Lower case login = $login";
##### CASE END

   $biscuit = trim $input{'biscuit'};

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

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
         if ($jp ne "") {
            if ($jp ne "buddie") {
               status("$sesstab{$biscuit}{'login'}: You have been logged out automatically. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    }
         }
         status("$sesstab{$biscuit}{'login'}: You have been logged out automatically. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("$sesstab{$biscuit}{'login'}: You have been logged out automatically. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   } else {
        hddebug "login = $login";
        $login = $sesstab{$biscuit}{'login'};
        hddebug "login = $login";
        hddebug "biscuit = $biscuit";
        if ($login eq "") {
          error("Login is an empty string.\n");
          exit;
        }

#### BEGIN CASE
        $login = "\L$login";
#### END CASE

   }


   $remoteaddr = $ENV{'REMOTE_ADDR'};
   $sessionid = getkeys();


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      if (exists $sesstab{$biscuit}) {
        delete $sesstab{$biscuit};
      }
      if (exists $logsess{$login}) {
        delete $logsess{$login};
      }

      if ($hs eq "") {
         if ($jp ne "") {
           if ($jp ne "buddie") {
               status("$login: Your session has timed out.  Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.");
	      exit;
           }
         }
         status("$login: Your session has timed out.  Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      } else {
         status("$login: Your session has timed out.  Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.");
      }
     exit;
   }

   $sesstab{$biscuit}{'time'} = time();

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

  #print "Profile before checking login.\n";

# check if login  record exists.
   if (!exists $logtab{$login}) {
       #print "Profile record does not exist.\n";
       error("$login: Profile does not exist.\n");
       exit;
   } else {
       #if ($action eq "Update") {
          #print "Profile update called.\n";
##### BEGIN CASE
          $pass1 = "\L$input{'password'}";
          $pass2 = "\L$input{'rpassword'}";
          if ($pass1 ne $pass2) {
##### END CASE

          #if ($input{'password'} ne $input {'rpassword'}) {
             status("$login: Passwords do not match. Please enter passwords again.");
             exit;
          }

##### BEGIN CASE
          $logtab{$login}{'password'} = trim $pass1;
##### END CASE

          #$logtab{$login}{'password'} = trim $input{'password'};

          if (!(notName(trim $input{'fname'}))) {
             $logtab{$login}{'fname'} = trim $input{'fname'};
          } else {
             if ($hs eq "") {
                status("$login: Invalid characters in first name.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in first name.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notName(trim $input{'lname'}))) {
             $logtab{$login}{'lname'} = trim $input{'lname'};
          } else {
             if ($hs eq "") {
                status("$login: Invalid characters in last name.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in last name.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notAddress(trim $input{'street'}))) {
             $logtab{$login}{'street'} = trim $input{'street'};
          } else {
             if ($hs eq "") {
                status("$login: Invalid characters in street address.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in street address.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notName(trim $input{'city'}))) {
              $logtab{$login}{'city'} = trim $input{'city'};
          } else {
             if ($hs eq "") {
                status("$login: Invalid characters in city.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in city.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notName(trim $input{'state'}))) {
             $logtab{$login}{'state'} = trim $input{'state'};
          } else {
             if ($hs eq "") {
                status("$login: Invalid characters in state.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in state.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notNumber(trim $input{'zipcode'}))) {
             $logtab{$login}{'zipcode'} = trim $input{'zipcode'};
          } else {
	     if ($hs eq "") {
                status("$login: Invalid characters in zipcode.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
             } else {
                status("$login: Invalid characters in zipcode.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notName(trim $input{'country'}))) {
              $logtab{$login}{'country'} = trim $input{'country'};
          } else {
	     if ($hs eq "") {
                status("$login: Invalid characters in country.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	     } else {
                status("$login: Invalid characters in country.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
	     }
             exit;
          }

          if (!(notPhone(trim $input{'phone'}))) {
             $logtab{$login}{'phone'} = trim $input{'phone'};
          } else {
	     if ($hs eq "") {
                status("$login: Invalid characters in phone.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	     } else { 
                status("$login: Invalid characters in phone.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
	     }
             exit;
          }


          #if (notPhone(trim $input{'pager'})) {
	  #   if ($hs eq "") {
          #      status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	  #   } else {
          #      status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
	  #   }
          #   exit;
          #}
          #hddebug "Pager = $input{'pager'}";

          $pgtype = $input{'pagertype'};
          #if ( ("\U$pgtype" eq "\USkyTel Pager") && (notSkyTelPin (trim $input{'pager'})) ) {
          #    status("$login: You have specified the SkyTel Pager, but the pager number must be a PIN (7 numeric digits) For instance 1234567 is a valid field where PIN in this case is 1234567.If you have a 1800 SkyTel number, and the last 7 digits are the PIN code, please enter only the last 7 digits. <p>You must have an alphanumeric SkyTel Pager which is capable of receiving internet pager messages in order to use this feature. Check with a SkyTel representative if you are not familiar with alphanumeric service.");
          #    exit;
          #}

          if ( ("\U$pgtype" eq "\UMetrocall Pager") && (notAlphaNumeric (trim $input{'pager'})) ) {
             #status("$login: You can specify alphanumeric characters (a-z A-Z 0-9) in your Metrocall Pager message");
             #exit;
          }

          if (!(notPhone(trim $input{'fax'}))) {
             $logtab{$login}{'fax'} = trim $input{'fax'};
          } else {
	     if ($hs eq "") {
               status("$login: Invalid characters in fax.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	     } else {
               status("$login: Invalid characters in fax.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
	     }
             exit;
          }

          if (!(notPhone(trim $input{'cellp'}))) {
             $logtab{$login}{'cphone'} = trim $input{'cellp'};
             #print "entered and updated cphone", $input{'cellp'}, "\n";
          } else {
	     if ($hs eq "") {
                status("$login: Invalid characters in cellphone.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	     } else { 
                status("$login: Invalid characters in cellphone.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          if (!(notPhone(trim $input{'busp'}))) {
             $logtab{$login}{'bphone'} = trim $input{'busp'};
          } else {
	     if ($hs eq "") {
                status("$login: Invalid characters in business phone.  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
	     } else {
                status("$login: Invalid characters in business phone.  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
             }
             exit;
          }

          $pgtype = $input{'pagertype'};
          if ("\L$pgtype" eq "\LOther Pager") {
             if (notEmail(trim $input{'pager'})) {
                if ($hs eq "") {
                    status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
                } else {
                    status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
                }   
                exit;
             }
          } else {
             if (notPhone(trim $input{'pager'})) {
                if ($hs eq "") {
                   status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/validation.html\"> here</a> for valid input.");
                } else {
                   status("$login: Invalid characters in pager ($input{'pager'}).  Click <a href=\"http://$vdomain/$hs/validation.html\"> here</a> for valid input.");
                }
                exit;
             }
          }

          
          #if ("\U$pgtype" ne "\UOther Pager") {
             #if (!(notEmailAddress(trim $input{'pager'}))) {
             #   status("You have selected pager type as $pgtype but entered an email address in the pager field. Please enter the pager PIN number or pager number instead of email address. A pager PIN or pager number is usually assigned to $pgtype pagers only if you explicitly subscribe for Internet paging service on your $pgtype. Please talk to your $pgtype representative for more details on how to enable the Internet paging option on your pager.<p>If you would still like to enter an email address for your pager, you need to select the pager type to be \"Other Pager\" even if you have a $pgtype.\n");
             #   exit;
             #}
          #} else {
          #   if (trim $input{'pager'} ne "") {
          #      if (notEmailAddress(trim $input{'pager'})) {
          #         status("You have selected pager type as $pgtype but not entered an email address in the pager field. Please enter a valid email address of the form user\@domain.com.\n");
          #         exit;
          #      }
          #   }
          #}

# NO VALIDATION AFTER THIS LINE OF CODE
##### BEGIN CASE
          $em = trim $input{'email'};
          $logtab{$login}{'email'} = "\L$em";
##### END CASE
          $logtab{$login}{'pager'} = trim $input{'pager'};

          #$logtab{$login}{'email'} = trim $input{'email'};
          $logtab{$login}{'pagertype'} = $input{'pagertype'};
          $logtab{$login}{'zone'} = $input{'zone'};
          $logtab{$login}{'url'} = trim $input{'url'};
          if ($input{'checkid'} eq "on") {
             $logtab{$login}{'checkid'} = "CHECKED";
          }  else {
             $logtab{$login}{'checkid'} = $input{'checkid'};
          }
          if ($input{'calinvite'} eq "on") {
             $surveytab{$login}{'calinvite'} = "CHECKED";
          }  else {
             $surveytab{$login}{'calinvite'} = $input{'calinvite'};
          }
          if ($input{'calpublish'} eq "on") {
             if (!(-d "$ENV{HTTPHOME}/html/hd/members/$login")) {
                $logtab{$login}{'calpublish'} = "CHECKED";
                system "mkdir -p $ENV{HTTPHOME}/html/hd/members/$login";
                if ($login ne "") {
                   system "rm -f $ENV{HTTPHOME}/html/hd/members/$login/*.cgi";
                   system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/members/$login";
                   system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/members/$login";
                   $cmsg = "<p>You have chosen to publish your calendar on the web. HotDiary has created a website for you. Your website is \"http://$vdomain/members/$login\". Please note down this website for your future reference."

   # Please click <a href=\"http://www.hotdiary.com/members/$login\">here</a> to view your calendar!";

                } else {
                   error("Invalid member login. No operation performed.");
                   exit;
                }
             }
          }  else {
             $logtab{$login}{'calpublish'} = $input{'calpublish'};
             if ($login ne "") {
                if (-d "$ENV{HTTPHOME}/html/hd/members/$login") {
                   system "rm -rf $ENV{HTTPHOME}/html/hd/members/$login";
                   $cmsg = "<p>You have chosen not to publish your calendar on the web. HotDiary has removed your website for you.";
                }
             } else {
                error("Invalid member login. No operation performed.");
                exit;
             }
          }


          if ($input{'informme'} eq "on") {
             $logtab{$login}{'informme'} = "CHECKED";
          }  else {
             $logtab{$login}{'informme'} = $input{'checkboxfield'};
          }
          #$msg = "$login: Profile has been updated. $cmsg\n";
          #print "login profile has been updated";
       #}
   }
   #status("$msg");

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();


   #system "/bin/rm -f $ENV{HDREP}/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$login/*.html";
   #system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";

   $prml = "";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/redprof-$biscuit-$$.html";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/proxy/redirect.html";
   $rh = $input{'rh'};
   $url = adjusturl "/cgi-bin/$rh/execdocalclient.cgi?biscuit=$biscuit&os=$os";
   $prml = strapp $prml, "redirecturl=$url";
   parseIt $prml;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$login/redprof-$biscuit-$$.html";

# save the info in db
   tied(%logtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

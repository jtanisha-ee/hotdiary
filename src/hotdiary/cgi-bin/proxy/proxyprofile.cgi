#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: profile.cgi
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

   #"mkdir -p $ENV{HDDATA}/partners/lictab";

# bind lictab table vars
   tie %lictab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/lictab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $HDLIC = $input{'HDLIC'};
   $vdomain = $input{'vdomain'};
   $hs = $input{'hs'};
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
            status("You have a valid license, however this product was installed on a system with a domain that is different from $vdomain. Please contact HotDiary.Com, and they will be happy to help you with the license.");
            exit;
         }

      }
   }


# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Profile"); 

  hddebug "action = $input{'action'} \n";

   if ($input{'action'} ne "") {
      $action = $input{'action'};
   }


   hddebug "Entered HotDiary proxyprofile Got login= $input{'login'}";
   hddebug "Entered HotDiary proxyprofile Got password = $input{'password'}";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      
 
   $login = trim $input{'login'};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 

   $os = $input{'os'};
   $jp = $input{'jp'};
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

   $sessionid = getkeys();
   $remoteaddr = $ENV{'REMOTE_ADDR'};

# bake a biscuit
   $biscuit = "$sessionid-$login-$remoteaddr";
   $title = time();

#### BEGIN CASE
        $login = "\L$login";
#### END CASE



   if (exists $logsess{$login}) {
       delete $logsess{$login};
   }

   $sesstab{$biscuit}{'time'} = time();
   $sesstab{$biscuit}{'login'} = $login;
   $sesstab{$biscuit}{'biscuit'} = $biscuit;

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

  hddebug "action = $action \n";

       if ($action eq "Profile") {
##### BEGIN CASE
##### END CASE
          if (!exists $logtab{$login}) {
             #print "Profile record does not exist.\n";
             status("$login: Profile does not exist.\n");
             exit;
          } else {
             hddebug "login = $login \n";
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

              # bind surveytab table vars
              tie %surveytab, 'AsciiDB::TagFile',
               DIRECTORY => "$ENV{HDDATA}/surveytab",
               SUFIX => '.rec',
               SCHEMA => {
                    ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite'] };
              ($outfield = $surveytab{$login}{'calinvite'}) =~ s/\n/\n<BR>/g;
              $prml = strapp $prml, "calinvite=$outfield";

              ($outfield = $logtab{$login}{'informme'}) =~ s/\n/\n<BR>/g;
              $prml = strapp $prml, "checkboxfield=$outfield";

              $rh = $input{'rh'};
              $urlcgi = adjusturl "/cgi-bin/$rh/execdoprofupdate.cgi?biscuit=$biscuit&os=$os";
              #$urlcgi = buildurl("execprofupdate.cgi");
              $prml = strapp $prml, "actioncgi=$urlcgi";

              $label = "Personal Profile";
              $prml = strapp $prml, "label=$label";
              hddebug "reached template \n";
              $prml = strapp $prml, "pagenumber=";
              $prml = strapp $prml, "template=$ENV{HDTMPL}/profile.html";
              if ($os eq "nt") {
                  $prml = strapp $prml, "formenc=";
              } else {
                  $formenc = adjusturl("ENCTYPE=\"$ENV{HDENCODE}\"");
                  $prml = strapp $prml, "formenc=$formenc";
              }
              $prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/profile.html";
              parseIt $prml;
              $prml = "";
           }
       } 

  hddebug "after parsing the template";
  # if ($action eq "Profile") {
  #    system "/bin/cat $ENV{HDHREP}/$login/profile.html > $ENV{HDREP}/$login/$biscuit.html";
  # }
 



# reset the timer.
   $sesstab{$biscuit}{'time'} = time();


   #system "/bin/rm -f $ENV{HDREP}/$login/*.html";
   #system "/bin/rm -f $ENV{HDHREP}/$login/*.html";
   #system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$login/index.html";

   #$prml = "";
   #$prml = strapp $prml, "template=$ENV{HDTMPL}/proxy/redirect.html";
   #$prml = strapp $prml, "templateout=$ENV{HDHREP}/$login/profile.html";
   #$rh = $input{'rh'};
   ##$url = adjusturl "/cgi-bin/$rh/execprofile.cgi?biscuit=$biscuit";
   #$prml = strapp $prml, "redirecturl=$url";
   #parseIt $prml;

   hddebug "reached content and catting \n";
   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$login/profile.html";

# save the info in db
   tied(%logtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

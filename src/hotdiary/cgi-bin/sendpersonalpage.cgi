#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#


#
# FileName: sendpersonalpage.cgi
# Purpose: it sends appropriate pager messages from the address book.
# Creation Date: 07-01-98
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
   hddebug "sendpersonalpage.cgi";

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXMESSAGE = 1024;

   $biscuit = $input{'biscuit'};

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
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
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
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
   $to = $input{'to'};
   $pagertype = $input{'pagertype'};
   #print "to = ", $to, "\n";
   #print "pagertype = ", $pagertype;
   $message = trim $input{'message'};
   if (notDesc($message)) {
      status("Invalid characters in message. Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
      exit;
   }

   #is this particular only to skytel ???
   if ("\U$pagertype" eq "\USkyTel Pager") {
      $message = replaceblanks($message);
   }
   if (length($message) > $MAXMESSAGE) {
	status("Limit the length of pager/fax message to $MAXMESSAGE.");
	exit;
   }

   $successpage = $input{'thispage'};
   #print "successpage = ", $successpage, "\n";

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
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        $login = $sesstab{$biscuit}{'login'};
        if ($login eq "") {
           error("Login is an empty string. Possibly invalid biscuit.\n");
           exit;
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already timed out. However, all your personal information is completely intact.");
    exit;
   }

   $sesstab{$biscuit}{'time'} = time();
   $from = $logtab{$login}{'fname'};

   $dirtype = $input{dirtype};

   if ($dirtype eq "personaldir") {
     $execfile = "execpersonaldir.cgi";
   } 
   if ($os ne "nt") {
      $execfile = encurl "$execfile";
   }

   $successpage = "http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execfile&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";

   $successpage = goodwebstr($successpage);

   qx{echo \"$message\" > /var/tmp/$login$$};
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   #if ($action = "Send") { 
       if ("\U$pagertype" eq "\USkyTel Pager") {
          $prml = "";
          $redirecturl = adjusturl("http://www.skytel.com/cgi-bin/page.pl\?to=$to&message=$message&success_url=$successpage&from=$from");
          #$redirecturl = adjusturl("http://www.skytel.com/cgi-bin/page.pl\?to=$to&message=$message&from=$from");
       
          $prml = strapp $prml, "redirecturl=$redirecturl";
          $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
          $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/redirect_url.html";
          $prml = strapp $prml, "redirecturl=$redirecturl";
          parseIt $prml;         
          system "cat $ENV{HDTMPL}/content.html"; 
          system "cat $ENV{HDREP}/$alphaindex/$login/redirect_url.html"; 
          exit;
       } else  {
	  if ("\U$pagertype" eq "\UAirTouch Pager") {
	       $email = "$to\@airtouch.net";
               system "/bin/mail -s \"$from\" $email < /var/tmp/$login$$";	
               #system "cat $ENV{HDTMPL}/content.html"; 
               #$successpage = qx{basename $successpage};
               #system "cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
	  } else  {
	     if ("\U$pagertype" eq "\UNextel Pager") {
	         $email = "$to\@page.nextel.com";
                 system "mail -s \"$from\" $email < /var/tmp/$login$$";	
                 #system "cat $ENV{HDTMPL}/content.html"; 
                 #$successpage = qx{basename $successpage};
                 #system "cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
             } else {
	         if ("\U$pagertype" eq "\UPageMart Pager") {
	            $email = "$to\@pagemart.net";
                    system "mail -s \"$from\" $email < /var/tmp/$login$$";	
                    #system "cat $ENV{HDTMPL}/content.html"; 
                    #$successpage = qx{basename $successpage};
                    #system "cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                 } else {
	             if ("\U$pagertype" eq "\UMetrocall Pager") {
                        $message =~ s/\s/\+/g;
                        $url = "http://www.metrocall.com/cgi-bin/rbox/default.cgi?TO=$to&Message=\"$message\"";
                        system "java COM.hotdiary.main.ExecCGIURL \"$url\"";
                        #system "cat $ENV{HDTMPL}/content.html"; 
                        #$successpage = qx{basename $successpage};
                        #system "cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                     } else {
                          ($user, $domain) = split "\@", $to;
                          if ((trim($user) eq "") || (trim($domain) eq "")) {
                             status("For Other Pager type, your pager field must contain a valid email address. Could not deliver message to pager.");
                             exit; 
                          }
                          system "mail -s \"$from\" $to < /var/tmp/$login$$";	
                          #system "cat $ENV{HDTMPL}/content.html"; 
                          #$successpage = qx{basename $successpage};
                          #system "cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                          #status("$login: You have selected \"Other Pager\", which is not supported for communication from HotDiary.");
                          #exit;
                     }
                 }
             }
          }
       }
   #}


# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHREP}/$alphaindex/$login/$dirtype.html";

}

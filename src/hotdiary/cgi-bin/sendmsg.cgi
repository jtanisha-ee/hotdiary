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
# FileName: sendmsg.cgi
# Purpose: it sends appropriate pager messages from the address book.
# Creation Date: 07-01-98
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXMESSAGE = 1024;

   #print &PrintHeader;
   #print &HtmlTop ("sendmsg.cgi example");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'send.x'} ne "") {
      $action = "Send";
   } 

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.\n");
              exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already timed out. However, all your personal information is completely intact.");
    exit;
   }

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $sesstab{$biscuit}{'time'} = time();
   $from = $logtab{$login}{'fname'};
   qx{echo \"$message\" > /var/tmp/$login$$};
   if ($action = "Send") { 
       if ("\U$pagertype" eq "\USkyTel Pager") {
          $prml = "";
          $redirecturl = adjusturl("http://www.skytel.com/cgi-bin/page.pl\?to=$to&message=$message&success_url=$successpage&from=$from");
       
          $prml = strapp $prml, "redirecturl=$redirecturl";
          $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
          $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/redirect_url.html";
          #$prml = strapp $prml, "redirecturl=$redirecturl";
          parseIt $prml;         
          system "/bin/cat $ENV{HDTMPL}/content.html"; 
          system "/bin/cat $ENV{HDREP}/$alphaindex/$login/redirect_url.html"; 
       } else  {
	  if ("\U$pagertype" eq "\UAirTouch Pager") {
	       $email = "$to\@airtouch.net";
               system "/bin/mail -s \"$from\" $email < /var/tmp/$login$$";	
               system "/bin/cat $ENV{HDTMPL}/content.html"; 
               $successpage = qx{basename $successpage};
               system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
	  } else  {
	     if ("\U$pagertype" eq "\UNextel Pager") {
	         $email = "$to\@page.nextel.com";
                 system "/bin/mail -s \"$from\" $email < /var/tmp/$login$$";	
                 system "/bin/cat $ENV{HDTMPL}/content.html"; 
                 $successpage = qx{basename $successpage};
                 system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
             } else {
	         if ("\U$pagertype" eq "\UPageMart Pager") {
	            $email = "$to\@pagemart.net";
                    system "/bin/mail -s \"$from\" $email < /var/tmp/$login$$";	
                    system "/bin/cat $ENV{HDTMPL}/content.html"; 
                    $successpage = qx{basename $successpage};
                    system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                 } else {
	             if ("\U$pagertype" eq "\UMetrocall Pager") {
                        $message =~ s/\s/\+/g;
                        $url = "http://www.metrocall.com/cgi-bin/rbox/default.cgi?TO=$to&Message=\"$message\"";
                        system "java COM.hotdiary.main.ExecCGIURL \"$url\"";
                        system "/bin/cat $ENV{HDTMPL}/content.html"; 
                        $successpage = qx{basename $successpage};
                        system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                     } else {
                          ($user, $domain) = split "\@", $to;
                          if ((trim($user) eq "") || (trim($domain) eq "")) {
                             status("For Other Pager type, your pager field must contain a valid email address. Could not deliver message to pager.");
                             exit; 
                          }
                          system "/bin/mail -s \"$from\" $to < /var/tmp/$login$$";	
                          system "/bin/cat $ENV{HDTMPL}/content.html"; 
                          $successpage = qx{basename $successpage};
                          system "/bin/cat $ENV{HDREP}/$alphaindex/$login/$successpage"; 
                          #status("$login: You have selected \"Other Pager\", which is not supported for communication from HotDiary.");
                          exit;
                     }
                 }
             }
          }
       }
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   
# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

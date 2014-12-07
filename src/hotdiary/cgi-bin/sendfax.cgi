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
# FileName: sendfax.cgi 
# Purpose: it sends a fax message.
# Creation Date: 12-01-98
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

   #print &PrintHeader;
   #print &HtmlTop ("sendfax.cgi example");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   $to = $input{'to'};
   #print "to = ", $to, "\n";
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $thispage = $input{'thispage'};
   #print "thispage = ", $thispage, "\n";

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

   $sesstab{$biscuit}{'time'} = time();


   $prml = "";
   $prml = strapp $prml, "label=HotDiary Send Fax Premium Service";
   $prml = strapp $prml, "biscuit=$biscuit";

   # these lines are uncommented for testing.
   $prml = strapp $prml, "to=$to";
   $prml = strapp $prml, "thispage=$thispage";
   $urlcgi = buildurl("execsendmsg.cgi");
   $prml = strapp $prml, "actioncgi=cgi-bin/execsendfaxmsg.cgi";

   #send email to faxsav at number@faxsav.com
   #system "/bin/mail -s \"fax\" $email < $mfile";

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = strapp $prml, "template=$ENV{HDTMPL}/sendfax.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/sendfax-$$.html";
   parseIt $prml;

   #system "/bin/cat $ENV{HDTMPL}/content.html"; 
   #system "/bin/cat $ENV{HDREP}/$alphaindex/$login/sendfax.html"; 
   hdsystemcat "$ENV{HDREP}/$alphaindex/$login/sendfax-$$.html"; 


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

# need to add counter to keep track of faxes sent and also the fax numbers
# used for each customer.

   
# save the info in db
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

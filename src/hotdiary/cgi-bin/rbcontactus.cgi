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
# FileName: search.cgi
# Purpose: it searches info. in hotdiary.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
require "flush.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 

   #status("This service is coming soon!");
   #print "Set-Cookie: hotdiary\n\n";

   hddebug "search action = $input{'Send Question'}";

   if ($input{'Send Question'} eq "Send Question") {
      $action = "Send Question";
   }

   $bookie = $ENV{HTTP_COOKIE};
   #hddebug "Cookie = $ENV{HTTP_COOKIE}";
   hddebug "Cookie = $bookie";

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   hddebug "action = $action";
   if ($action eq "Search") {
      hddebug "Came here";
      $search = trim $input{'search'};
      if ($search eq "") {
         local ($oldbar) = $|;
         $cfh = select (STDOUT);
         $| = 1;
         status("Please enter a non-empty search criteria. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         $| = $oldbar;
         select ($cfh);
         exit;
      }
      if ($search =~ /\\/) {
         local ($oldbar) = $|;
         $cfh = select (STDOUT);
         $| = 1;
         status("Invalid characters found in search expression. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         $| = $oldbar;
         select ($cfh);
         exit;
      }
      ($firstname, $lastname) = split(" ", $search);
      $firstname = trim $firstname;
      $lastname = trim $lastname;
      if (($firstname eq "") && ($lastname eq "")) {
         local ($oldbar) = $|;
         $cfh = select (STDOUT);
         $| = 1;
         status("Please enter \"firstname, lastname\" in search criteria. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         $| = $oldbar;
         select ($cfh);
         exit;
      }
      $tooshort = "";
      if (((length $firstname) <= 3) && ((length $lastname) <= 3)) {
         $msg .= "The specified search names are too short. A lot of matches were found. HotDiary will not display results, for protecting user and system security. Will perform an exact name match search to shorten output.<BR>";
         $tooshort = "true";
         $msg .= "<p>\"$firstname\", \"$lastname\" <b>exactly</b> matches the following people in HotDiary's directory: <BR><DL>";
      } else {
         $msg .= "<p>\"$firstname\", \"$lastname\" matches the following people in HotDiary's directory (Demo calendars displayed only): <BR><DL>";
      }
      $cntr = 0;
      foreach $account (sort keys %logtab) {
         $checkid = $logtab{$account}{'checkid'};
         if ($checkid eq "CHECKED") {
            if ((($tooshort eq "") && (nmmatch $logtab{$account}{'fname'}, $firstname) && (nmmatch $logtab{$account}{'lname'}, $lastname)) || 
               (($tooshort eq "true") && ("\U$logtab{$account}{'fname'}" eq "\U$firstname") && ("\U($logtab{$account}{'lname'}" eq "\U$lastname"))) {
               $cntr++;
               $msg .= "<LI>";
               $msg .= $logtab{$account}{'fname'} . " " . $logtab{$account}{'lname'} . "<BR>";
               #$msg .= "Member Login: $account <BR>";
               #$msg .= "Member Email: $logtab{$account}{'email'} <BR>";
               if ($logtab{$account}{'calpublish'} eq "CHECKED") {
                  $urlref = "<a href=\"$ENV{HDHTML}/members/$account\">Example Website Demo</a>";
                  $msg .= "$urlref<BR>";
               }
               $msg .= "</LI><BR>";
            }
         }
      }
      $msg .= "</DL>";
      if ($cntr eq "0") {
         $msg .= "<p>Did not find any matches based on your search criteria.<BR>";
         if (($firstname eq "FirstName") || ($lastname eq "LastName")) {
            $msg .= "<p>Please replace \"FirstName\" with the actual first name, and \"LastName\" with the actual last name, that you are looking for.<BR>";
         } else {
            if ($tooshort eq "") {
               #$msg .= "<p>It is likely that the person you are looking for has decided not to make his/her ID public. So even if he/she exists on HotDiary as a valid member, you will not be able to find him/her.<BR>";
            }
         }
      } else {
         $msg .= "<BR>Found a total of $cntr matches.<BR>";
      }
      local ($oldbar) = $|;
      $cfh = select (STDOUT);
      $| = 1;
      system "/bin/cat $ENV{HDTMPL}/content.html";
      $| = $oldbar;
      select ($cfh);
      statuss($msg);
      exit;
   }

   if ($action eq "Send Question") {
      hddebug "Came into Send Question";
      #$name = $input{'name'};
      $org = $input{'Subject'};
      $email = $input{'EMail'};
      #$phone = $input{'phone'};
      #$domain1 = $input{'domain1'};
      #$cal100 = $input{'cal100'};
      $message = $input{'question'};

      hddebug "message is $message";

# Block the spammers!
      if ( 
           ($name =~ /shoe-apparel/) ||
           ($name =~ /Wesley/) ||
           ($name =~ /Lam/) ||
           ($name =~ /Chen/) ||
           ($org =~ /China/) ||
           ($org =~ /Keyi/) ||
           ($org =~ /bizdiscovery/) ||
           ($email =~ /ymdisplay/) ||
           ($email =~ /YMDISPLAY/) ||
           ($email =~ /163/) ||
           ($email =~ /effort/) ||
           ($email =~ /bizdiscovery/) ||
           ($email =~ /cn/) ||
           ($email =~ /126/) ||
           ($email =~ /hzcnc/) ||
           ($email =~ /hk/) ||
           ($message =~ /bio/) ||
           ($message =~ /China/) ||
           ($message =~ /china/) ||
           ($email =~ /orient/) ||
           ($org =~ /orient/) ||
           ($org =~ /SHENZHEN/) ||
           ($org =~ /hunan/) ||
           ($org =~ /Zhejiang/) ||
           ($email =~ /lc_oisq_com/)
         ) {
         status "Thank you for contacting HotDiary! Your message has been sent. We will get back to you as soon as possible. Please <a href=http://hotdiary.com>click here</a> to return to HotDiary.";
         hddebug "The message was not sent. $name $org $email $phone $domain1 $message";
         exit;
      }

      if ($email eq "") {
         status "Please enter a valid email address.";
         exit;
      }

      hddebug "Before email message";

      $mfile = "$ENV{HDHOME}/tmp/contact_us$$";
      open mhandle, ">$mfile";
      printf mhandle "Name: $name\n\n";
      printf mhandle "Domain: $ENV{'REMOTE_ADDR'}\n\n";
      printf mhandle "Subject: $org\n\n";
      printf mhandle "Email: $email\n\n";
      printf mhandle "Phone: $phone\n\n";
      printf mhandle "Message: $message\n\n";
      &flush(mhandle);
      system "/bin/mail -s \"Customer Query\" smitha\@redbasin.com manoj\@redbasin.com < $ENV{HDHOME}/tmp/contact_us$$";
      hddebug "After email $mfile";
      #system "$ENV{HDEXECCGI}/execcleanproducts $mfile 300";
      hddebug "After cleanproducts";
      #$len = length $message;
      #if ($len > 20) {
      #   $len = 20;
      #}
      #$msg = substr $message, 0, $len;

      hddebug "back to redbasin";


      #$cgis = adjusturl "http://192.168.0.10";
      $cgis = adjusturl "http://redbasin.com";
      $prm = strapp $prm, "redirecturl=$cgis";
      $prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
      $prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
      parseIt $prm;
      hdsystemcat "$ENV{HDHOME}/tmp/apc-$$-redirect_url.html";
      #print "Location: http://192.168.0.10\n\n";
   }

   exit;
}

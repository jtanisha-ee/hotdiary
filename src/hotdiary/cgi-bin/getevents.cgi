#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: getevents.cgi
# Purpose: it searches events 
# Creation Date: 10-09-99
# Created by: Smitha Gudur
#

#!/usr/local/bin/perl5

require "cgi-lib.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

#max length in the description
   $MAXDESC = 4096;

# parse the command line
   &ReadParse(*input);

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

   $biscuit = trim $input{'biscuit'};

   if ($input{'add.x'} ne "") {
      $action = "Add";
   } else {
      if ($input{'search.x'} ne "") {
        $action = "Search";
      }
   }


   hddebug "action = $action";

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
               error("Login  is an empty string.\n");
               exit;
	   }
        }
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
     if (exists $sesstab{$biscuit}) {
        delete $sesstab{$biscuit};
     }
     if (exists $logsess{$login}) {
        delete $logsess{$login};
     }
     status("$login: Your session has timed out. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.");
     exit;
  }

  $sesstab{$biscuit}{'time'} = time();

  $alpha = substr $login, 0, 1;
  $alpha = $alpha . '-index';


# bind personal appointment table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alpha/$login/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'phone', 'city', 'url', 'imgfn', 'venue'] };

   (@records) =sort keys %appttab;

   if ($#records < 0) { 
      hddebug("no events found");
   }

   for ($i = 0; $i <= $#records; $i = $i + 1) {
      if (exists $appttab{$records[$i]}) {

         $prml = strapp $prml, "year=$appttab{$records[$i]}{'year'}";
         $prml = strapp $prml, "meridian=$appttab{$records[$i]}{'meridian'}";

         ($monthstr = getmonthstr($appttab{$records[$i]}{'month'})) =~ s/\n/\n<BR>/g;
         $prml = strapp $prml, "month=$monthstr";
         $prml = strapp $prml, "monthnum=$appttab{$records[$i]}{'month'}";
         $prml = strapp $prml, "day=$appttab{$records[$i]}{'day'}";

         $prml = strapp $prml, "hour=$appttab{$records[$i]}{'hour'}";
         if ($appttab{$records[$i]}{'min'} eq "00") {
            $min = 0;
         } else {
            $min = $appttab{$records[$i]}{'min'};
         }

         $prml = strapp $prml, "min=$min";
         $prml = strapp $prml, "sec=$appttab{$records[$i]}{'sec'}";

         $prml = strapp $prml, "zone=$appttab{$records[$i]}{'zone'}";
         $zone = getzonestr($appttab{$records[$i]}{'zone'});
         $prml = strapp $prml, "zonestr=$zone";

         $subject = adjusturl($appttab{$records[$i]}{'subject'});
         $prml = strapp $prml, "subject=$subject";

         $desc = adjusturl($appttab{$records[$i]}{'desc'});
         $prml = strapp $prml, "desc=$desc";

         $prml = strapp $prml, "phone=$appttab{$records[$i]}{'phone'}";
         $prml = strapp $prml, "city=$appttab{$records[$i]}{'city'}";
         $prml = strapp $prml, "url=$appttab{$records[$i]}{'url'}";
         $prml = strapp $prml, "imgfn=$appttab{$records[$i]}{'imgfn'}";
         $prml = strapp $prml, "venue=$appttab{$records[$i]}{'venue'}";
      }
   }
}

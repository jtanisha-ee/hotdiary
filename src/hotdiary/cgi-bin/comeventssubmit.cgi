#!/usr/bin/perl

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
# FileName: comeventssubmit.cgi 
# Purpose: submit a Community Event
# Creation Date: 09-18-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


$login = trim $input{login};
if ($login eq "") {
   status "Please enter a non-empty member login. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}
$login = "\L$login";

if (!exists $logtab{$login}) {
   status "Member login $login does not exist. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

$password = "\L$input{password}";
if ($password ne "\L$logtab{$login}{password}") {
   status "Password $password for login $login is incorrect. Please enter a valid password. If you haven't yet registered with HotDiary, please click <a href=\"/index.html\">here.</a>";
   exit;
}

$category = $input{category};
$desc = $input{desc};
$subject = $input{subject};
if ( ($subject eq "") && ($desc eq "") ) {
   status "Please enter atleast one of Event Title or Event Details. We encourage you to specify more details about the event, so people will find your entry useful and interesting and also show-up for your event!";
   exit;
}
if ($subject eq "") {
   $subject = $category;
}
$month = $input{month};
$day = $input{day};
$year = $input{year};
$hour = $input{hour};
$min = $input{min};
hddebug "min = $min";
$meridian = $input{meridian};
$zone = $input{zone};
$venue = trim $input{venue};
$street = trim $input{street};
$city = trim $input{city};
$zipcode = trim $input{zipcode};
$state = trim $input{state};
$country = trim $input{country};
$person = trim $input{person};
$phone = trim $input{phone};
$banner = $input{banner};

   if ($category eq "Arts and Entertainment") {
      $group = "comarts";
   }
   if ($category eq "Science and Technology") {
      $group = "comscience";
   }
   if ($category eq "News and Media") {
      $group = "comnews";
   }
   if ($category eq "Education") {
      $group = "comeducation";
   }
   if ($category eq "Sports and Recreation") {
      $group = "comsports";
   }
   if ($category eq "Business and Economy") {
      $group = "combusiness";
   }
   if ($category eq "Travel and Leisure") {
      $group = "comtravel";
   }
   if ($category eq "Government") {
      $group = "comgovt";
   }
   if ($category eq "Health and Fitness") {
      $group = "comhealth";
   }
   if ($category eq "Other") {
      $group = "comother";
   }

   system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
   system "chmod 755 $ENV{HDDATA}/listed/groups/$group/appttab";
   system "chown nobody:nobody $ENV{HDDATA}/listed/groups/$group/appttab";
   
# bind group appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

   $en = $login . "." . getkeys();

   $appttab{$en}{entryno} = $en;
   $appttab{$en}{login} = $login;
   $appttab{$en}{month} = $month;
   $appttab{$en}{day} = $day;
   $appttab{$en}{year} = $year;
   $appttab{$en}{hour} = $hour;
   if ($min == 0) {
      $min = "00";
   }
   $appttab{$en}{min} = $min;
   $appttab{$en}{meridian} = $meridian;
   $appttab{$en}{atype} = "Email";
   $appttab{$en}{desc} = adjusturl $desc;
   $appttab{$en}{zone} = $zone;
   $appttab{$en}{recurtype} = "Once";
   $appttab{$en}{subject} = $subject;
   $appttab{$en}{street} = $street;
   $appttab{$en}{city} = $city;
   $appttab{$en}{state} = $state;
   $appttab{$en}{zipcode} = $zipcode;
   $appttab{$en}{country} = $country;
   $appttab{$en}{venue} = $venue;
   $appttab{$en}{person} = $person;
   $appttab{$en}{phone} = $phone;
   $appttab{$en}{banner} = adjusturl $banner;

   $msg = "Congratulations! Your event has been added to the group $group. If you would like to check out the calendar for $group, click <a href=\"http://www.hotdiary.com/groups/$group\">here</a>. <p>Click <a href=\"/cgi-bin/execdeploypage.cgi?page=comeventshelp.html\">here</a> to view the benefits of public community business promotional services offered by HotDiary. <p><FONT COLOR=ff0000>If you have made an error in adding the event, use the key $en and group $group as a reference when you contact us with the details of your request. In such an event, please allow a maximum of 24 hours for processing your request. Typically, we complete processing within 2 hours, however cannot give you an assurance that the processsing will be completed in 2 hours.</FONT>";

   system "echo \"$msg\" >> $ENV{HDHOME}/tmp/comevent-$login-$en";

   system "/bin/mail -s \"ComEvent From $login\" rhsup\@hotdiary.com < $ENV{HDHOME}/tmp/comevent-$login-$en";

   status($msg);

   tied(%appttab)->sync();




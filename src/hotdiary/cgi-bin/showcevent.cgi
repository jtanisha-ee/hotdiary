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
# FileName: groupcal.cgi
# Purpose: New HotDiary Group Calendar Client
# Creation Date: 06-14-99
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

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};


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

   $login = $input{login}; 


   # bind lgrouptab table vars
   tie %lgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                  'listed', 'readonly' ] };

   $group = $input{group};
   $en = $input{en};
   
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

   
   $subject = $appttab{$en}{subject};
   $desc = adjusturl $appttab{$en}{desc};
   $street = $appttab{$en}{street};
   $city = $appttab{$en}{city};
   $state = $appttab{$en}{state};
   $zipcode = $appttab{$en}{zipcode};
   $country = $appttab{$en}{country};
   $venue = $appttab{$en}{venue};
   $person = $appttab{$en}{person};
   $phone = $appttab{$en}{phone};
   $category = $appttab{$en}{category};
   $banner = adjusturl $appttab{$en}{banner};
   $zonestr = getzonestr($appttab{$en}{zone}); 

   $date = "$appttab{$en}{day} $appttab{$en}{month} $appttab{$en}{year}, $appttab{$en}{hour}:$appttab{$en}{min} $appttab{$en}{meridian} $zonestr";


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
 
   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/showcevent.html"; 
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/showcevent-$$.html"; 
   $prml = strapp $prml, "subject=$subject";
   $prml = strapp $prml, "category=$category";
   $prml = strapp $prml, "desc=$desc";
   $prml = strapp $prml, "street=$street";
   $prml = strapp $prml, "city=$city";
   $prml = strapp $prml, "state=$state";
   $prml = strapp $prml, "zipcode=$zipcode";
   $prml = strapp $prml, "country=$country";
   $prml = strapp $prml, "venue=$venue";
   $prml = strapp $prml, "person=$person";
   $prml = strapp $prml, "phone=$phone";
   $prml = strapp $prml, "banner=$banner";
   $prml = strapp $prml, "date=$date";

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";   
   #system "cat $ENV{HDHREP}/$alphaindex/$login/showcevent.html";   
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showcevent-$$.html";   

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();


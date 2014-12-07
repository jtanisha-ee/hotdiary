#!/usr/bin/perl


# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: setremindtab.cgi
# Purpose: Updates reminder dispatch indexing tables, Invoked from cron
# from cron.      
# Creation Date: 02-04-98 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
#require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;
#use calutil::calutil;
require "flush.pl";

MAIN:
{


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

    # get the login name of each hotdiary user.
    # open the user's login apptentrytab. 
    # check in their apptentrytab if there are any entry numbers
    # search for each entry in the appointment entry tab
    # look for the entry numbers that are current or relevant   

    #print "this is appt cron cgi file \n";
    #print "$ENV{HDDATA}/logtab \n"; 
    #%dirlistt = dirlist "$ENV{HDDATA}/logtab";
      
    #foreach $fl (%dirlistt) {
    $mycnt = 0;
    #system "echo \"*******************************\" >> $ENV{HDHOME}/tmp/crontest";
    #system "echo \"*******************************\" >> $ENV{HDHOME}/tmp/crontest";
    #system "echo \"Invoked cron reminder, PID = $$\" >> $ENV{HDHOME}/tmp/crontest";
    $lult = localtime(time());
    #system "echo \"Current Time = $lult\" >> $ENV{HDHOME}/tmp/crontest";

    foreach $fl (keys %logtab) {
      $mycnt += 1;
      #print "entered for each loop fl = $fl\n";
      #($lg, $sf) = split(/\./, $fl);
      #$lg = substr $fl, 0, (length($fl)-4);
      $lg = $fl;
      #print "Processing member login $lg\n";
      $alp = substr $lg, 0, 1;
      $alp = $alp . '-index';
      (-e "$ENV{HDDATA}/$alp/$lg/appttab" and -d "$ENV{HDDATA}/$alp/$lg/appttab") or next;
      
      # bind personal appointment table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alp/$lg/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'sec', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype',
        'share', 'free', 'subject', 'street', 'city', 'state',
        'zipcode', 'country', 'venue', 'person', 'phone',
        'banner', 'confirm', 'id', 'type'] };

      # bind remind index table vars
      tie %remindtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/aux/remindtab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['login'] };
      (@aptsno) = keys %appttab;
      $rmail = trim $logtab{$lg}{email};
      if ( ($#aptsno >= 0) && ($rmail ne "") ) {
         $remindtab{$lg}{login} = $lg; 
         tied(%remindtab)->sync(); 
         system "chmod 777 $ENV{HDDATA}/aux/remindtab/$lg.rec";
      } else {
         #if ($rmail eq "") {
         #   print "Member login $lg has no email address\n";
         #}
         if (exists $remindtab{$lg}) {
            delete $remindtab{$lg};
            tied(%remindtab)->sync();
         }
      }
      #foreach $onekey (sort keys %appttab) {
      #   if ($onekey ne "")  {
      #      #system  "echo \"	Appt = $onekey\" >> /tmp/junk10000";
#	 }
      #}
   }
}	    

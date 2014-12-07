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
# FileName: mergedwebpage.cgi
# Purpose: It creates a member webpage dynamically.
# Creation Date: 05-30-99 
# 

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

&ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme'] };

  $alphaindex = substr $login, 0, 1;
  $alphaindex = $alphaindex . '-index';


system "/bin/cat $ENV{HDTMPL}/content.html";

$login = qx{basename `pwd`};
$login =~ s/\n//g;
$entity = qx{basename `cd ..; pwd`};
$entity =~ s/\n//g;

#if ($entity eq "groups") {
#   $g = $login;
#   $login = "";
#}

#$login = "\L$login";
$g = $login;
$g = "\L$g";

hddebug "g = $g";

if ($g ne "") {
   # bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish' ] };

   #hddebug "lmergetab password = $lmergetab{$g}{'password'}";
   if (exists $lmergetab{$g}) {
      if (($lmergetab{$g}{'cpublish'} ne "on") && ($lmergetab{$g}{'password'} ne "")) {
         statuss("The calendar master for this secure calendar, \"$g\",  has decided not to publish this calendar.");
         exit;
      }
      #hddebug "lmergetab password = $lmergetab{$g}{'password'}";
      if ($lmergetab{$g}{'password'} ne "") {
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/hdaccessmergedcal.html";
         $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/wp-$$.html";
         $rh = $input{'rh'};
         $prml = strapp $prml, "rh=$rh";
         $prml = strapp $prml, "g=$g";
         $prml = strapp $prml, "label=HotDiary";
         parseIt $prml;
         #system "/bin/cat $ENV{HDTMPL}/content.html";
         system "/bin/cat $ENV{HDHOME}/tmp/wp-$$.html";
         exit;
      }
   } else {
        statuss("The webpage for group ($g) does not exist.");
        exit;
   }
}

# this is redirect url, will be invoked when Add button is pressed
$cgis = adjusturl "/cgi-bin/execmgcalclient.cgi?sc=p&l=$login&g=$g";
$prm = "";
$prm = strapp $prm, "redirecturl=$cgis";
$prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
$prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/wp-$$-redirect_url.html";
parseIt $prm;
system "/bin/cat $ENV{HDHOME}/tmp/wp-$$-redirect_url.html";

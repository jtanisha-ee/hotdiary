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
# FileName: index.cgi
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

    
 # bind leditgrouptab table vars
   tie %leditgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/leditgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'jiveit', 'publicedit' ] };        

system "/bin/cat $ENV{HDTMPL}/content.html";
$login = qx{basename `pwd`};
$login =~ s/\n//g;
$entity = qx{basename `cd ..; pwd`};
$entity =~ s/\n//g;
if ($entity eq "groups") {
   $g = $login;
   $login = "";
}

$login = "\L$login";
$g = trim $login;
hddebug "g = $g, login =$login";

      # bind lgrouptab table vars
      tie %lgrouptab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/lgrouptab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                     'groupdesc', 'password', 'ctype', 'cpublish', 'corg',
                     'listed', 'readonly' ] };


if ($g ne "") {
    

   if (exists $lgrouptab{$g}) {

      ## add extra parameter
      # if (exists $leditgrouptab{$g}) {
      #hddebug "leditgrouptab password = $leditgrouptab{$g}{'password'}";
      #if (($leditgrouptab{$g}{'publicedit'} ne "CHECKED") && ($lgrouptab{$g}{'password'} ne "")) {
      #   statuss("The group master for this secure group, \"$g\",  has decided not to publish this addressbook or contacts.");
      #   exit;
      #}

      #hddebug "lgrouptab password = $lgrouptab{$g}{'password'}";

      if ($lgrouptab{$g}{'password'} ne "") {
         $prml = "";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/hdaccessgroupcontacts.html";
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
$cgis = adjusturl "/cgi-bin/execgroupcontact.cgi?sc=p&g=$g";
$prm = "";
$prm = strapp $prm, "redirecturl=$cgis";
$prm = strapp $prm, "template=$ENV{HDTMPL}/redirect_url.html";
$prm = strapp $prm, "templateout=$ENV{HDHOME}/tmp/wp-$$-redirect_url.html";
parseIt $prm;
system "/bin/cat $ENV{HDHOME}/tmp/wp-$$-redirect_url.html";

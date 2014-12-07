#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: addraddsearch.cgi
# Purpose: it adds and searches the addresses.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


use calfuncs::calfuncs;
require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{
  #print &PrintHeader;
  #print &HtmlTop ("caltest.cgi example");

  
  # $vw, $f, $a, $mo, $dy, $yr, $meridian, $login, $url, $eventnum
  $vw = "m";
  $f = "e";
  $mo = 4;
  $dy = 23;
  $yr = 1999;
  $meridian = "PM";
  $login = "smitha";
  $url = "biscuit=93017374328645-smitha-206.184.134.99&mo=$mo&yr=$yr&dy=$dy&vw=m";
  $eno = 12;
   $h = 0;
   $a = "d";
  $prml = dispatch($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $meridian, $login, $url, $eno);
  print "prml = $prml \n";

  $a = "e";
  $m = 1;
  $dy = 3;
  $eno= 92040137622736;
  $prml = dispatch($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $meridian, $login, $url, $eno);

  $a = "r";
  $prml = dispatch($prml, $vw, $f, $a, $mo, $dy, $yr, $h, $meridian, $login, $url, $eno);
}

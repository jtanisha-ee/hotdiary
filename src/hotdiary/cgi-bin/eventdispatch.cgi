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
# FileName: addraddsearch.cgi
# Purpose: it adds and searches the addresses.
# Creation Date: 10-09-97
# Created by: Smitha Gudur
#


#!/usr/local/bin/perl5

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;                 
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{ 

# bind session table vars
   tie %todo, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/todotab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['subject', 'desc', 'month', 'day', 'year', 
        'priority', 'status', 'share' ] };       
  
 
} 

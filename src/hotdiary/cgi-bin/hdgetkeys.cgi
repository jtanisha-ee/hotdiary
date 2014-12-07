#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: hdgetkeys.cgi
# Purpose: it returns a key used to create a record for tag file.
# Creation Date: 05-27-99 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{
   print &PrintHeader;
   $entryno = getkeys();
   print "$entryno";
}

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
# FileName: vcardsync.cgi
# Purpose: it allows users to upload a file which is vcard compatible and saves the vcards
# as address records in the appropriate login files
# we support both vCard 2.1 and vCard 3.0 versions
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

 
   system "java COM.hotdiary.main.jvcard \"/usr/local/hotdiary/java/COM/hotdiary/vcardio/vcard2\" \"/usr/local/hotdiary/java/COM/hotdiary/main/test/execperlvcard.cgi\" $biscuit";
}

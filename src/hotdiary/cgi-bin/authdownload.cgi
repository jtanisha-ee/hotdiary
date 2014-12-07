#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


&ReadParse(*input);

$password = $input{password};

   tie %passtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/passtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['password'] };

if (!exists($passtab{$password})) {
   status("You do not have the permission."); 
   exit;
}

if ($password eq $passtab{$password}{password} ) {

   system "mkdir -p $ENV{HTTPHOME}/html/hd/downloads/key-$$";
   system "ln -s $ENV{HDHOME}/JazzIt3.0.tar.gz $ENV{HTTPHOME}/html/hd/downloads/key-$$";
   system "ln -s $ENV{HDHOME}/JazzItx86.zip $ENV{HTTPHOME}/html/hd/downloads/key-$$";
   
} else {
   status("You do not have the permission."); 
   exit;
}   

status("Your distribution for JazzIt! is ready. Please click <a href=\"http://www.hotdiary.com/downloads/key-$$\">here</a> to proceed to the download area.");   





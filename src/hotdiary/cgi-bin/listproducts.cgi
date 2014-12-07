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

$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/productpurchase.html";
$prml = strapp $prml, "templateout=$ENV{HDHREP}/common/productpurchase-$$.html";
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDHREP}/common/productpurchase-$$.html";

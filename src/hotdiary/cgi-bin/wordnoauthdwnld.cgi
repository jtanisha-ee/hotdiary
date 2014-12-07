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

system "mkdir -p $ENV{HTTPHOME}/html/hd/words/key-$$";
system "ln -s $ENV{HDHOME}/yp/WordIt10.zip $ENV{HTTPHOME}/html/hd/words/key-$$";
system "ln -s $ENV{HDHOME}/yp/WordIt10.txt $ENV{HTTPHOME}/html/hd/words/key-$$";

$msg = "<p>Click <a href=$ENV{HDDOMAIN}/cgi-bin/execprocwordit.cgi>here to purchase and download</a> the complete WordIt! English Diary that contains a <B>quarter million words</B>, only for " . 'US $5.99.';

system "$ENV{HDEXECCGI}/execcleanwordit $ENV{HTTPHOME}/html/hd/words/key-$$/WordIt10.zip";
system "$ENV{HDEXECCGI}/execcleanwordit $ENV{HTTPHOME}/html/hd/words/key-$$/WordIt10.txt";

status("Congratulations! HotDiary's WordIt! English Diary is ready. Please click <a href=\"$ENV{HDDOMAIN}/words/key-$$/WordIt10.zip\">here to download diary</a> in WinZip format. The diary contains 105850 words. If your browser does not support the WinZip format, click <a href=\"$ENV{HDDOMAIN}/words/key-$$/WordIt10.txt\">here to download the plain text version</a> of the file. Depending upon the MIME application configuration in your browser, in some cases you may need to explicitly use the SHIFT+LEFTMOUSE combination to invoke the File Save dialog box. You have 15 minutes to download the diary. It will not be available for download at the end of 15 minutes. $msg");   

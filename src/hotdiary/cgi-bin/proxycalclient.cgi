#!/usr/bin/perl

require "cgi-lib.pl";
use AsciiDB::TagFile;

system "cat $ENV{HDTMPL}/content.html";
$sc = $input{sc};
$l = $input{l};
$g = $input{g};
system "java COM.hotdiary.main.ExecURLPrint \"http://www.hotdiary.com/cgi-bin/execcalclient.cgi?sc=$sc&l=$l&g=$g\"";

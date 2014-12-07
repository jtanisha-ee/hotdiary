#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: jiveithelp.cgi
# Purpose: Help On JiveIt
# 
# Creation Date: 08-17-99
# Created by: Smitha Gudur & Manoj Joshi
#


require "cgi-lib.pl";

&ReadParse(*input);

system "cat $ENV{HDTMPL}/content.html";
system "cat $ENV{HDTMPL}/jiveithelp.html";

#!/usr/bin/perl


# Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: lwpupload.cgi
# Purpose: File upload
# Creation Date: 01-09-01
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;
use utils::utils;
use HTTP::Request::Common qw(POST);
use LWP::UserAgent;
use HTML::TreeBuilder;
use URI::URL;
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Request::Common;
use HTTP::Request::Form;


# parse the command line
   &ReadParse(*input);
   hddebug("lwpupload.cgi");

   my $ua = LWP::UserAgent->new;
   my $url = url 'file:lwpuploadform.html';
   my $res = $ua->request(GET $url);
   my $tb = HTML::TreeBuilder->new;
   $tb->parse($res->content);
   my @forms = @{$tb->extract_links(qw(FORM))};
   my $f = HTTP::Request::Form->new($forms[0][1], $url);
   $f->field("uploadfile", "/tmp/colladd24110.txt");
   my $response = $ua->request($f->press("upload"));
   print $response->content if ($response->is_success);

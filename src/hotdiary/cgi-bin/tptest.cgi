
#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: tptest.cgi
# Purpose: it tests all the parser suites.
# Creation Date: 06-10-98
# Created by: Manoj Joshi 
#


use tp::tp;

# Template Parser regresssion test suite

{

# Build the param list for parseIt function

   $prml = "fname=manoj";
   $prml = strapp $prml, "lname=joshi";
   $prml = strapp $prml, "street=317 edgewater drive";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/searchaddrtblentry.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/tptestout.html";
   

# call parseIt

   parseIt $prml;
}

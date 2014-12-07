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
# FileName: utiltest.cgi 
# Purpose: it tests all the util suites.
# Creation Date: 06-10-98
# Created by: Manoj Joshi
#


use utils::utils;
use tp::tp;
use Time::Local;

{
   $str = "This	9is a test string";
   #if ( ($str =~ /\d+/) ||
   #if ($str =~ /[^a-zA-Z ]+/)  {
   #if ($str =~ /[^a-zA-Z\s]+/)  {

   $str = "Manoj Kumar";
   if (!(notName($str)))  {
      print "TEST PASS: $str: Valid string\n";
   } else {
      print "TEST FAIL:  notName() .\n";
   }

   $str = "Manoj 9Kumar";
   if (notName($str))  {
      print "TEST PASS: $str: Invalid string\n";
   } else {
      print "TEST FAIL:  notName() .\n";
   }

   $str = "(408)956-8550";
   if (!(notPhone($str))) {
      print "TEST PASS: $str: Valid Phone\n";
   } else {
      print "TEST FAIL:  notPhone() .\n";
   }

   $str = "(408)9_56-8550";
   if (notPhone($str)) {
      print "TEST PASS: $str: Invalid Phone\n";
   } else {
      print "TEST FAIL:  notPhone() .\n";
   }

   $str = " 	Manoj Kumar 		Pant ";
   $tstr = trim($str);
   #$tstr = "Manoj Kumar Pant";
   if ("$tstr" eq "Manoj Kumar Pant") {
      print "TEST PASS: trim '$str': '$tstr'\n";
   } else {
      print "TEST FAIL:  trim() .\n";
   }

   $str = 'uucpmail!m-josh_i@intrasail.com';
   if (!(notEmail($str))) {
      print "TEST PASS: $str: Valid Email\n";
   } else {
      print "TEST FAIL:  notEmail() .\n";
   }

   #$str = "isail";
   #$str1 = '@';
   #$str2 = "shell5.ba.best.com";
   #$str3 = "$str$str1$str2";
   #system "mail -s test1 mjoshi@intrasail.com < ~/.profile";

   $str = 'uucp!mjos=@intrasail.com';
   if (notEmail($str)) {
      print "TEST PASS: $str: invalid Email\n";
   } else {
      print "TEST FAIL:  notEmail() .\n";
   }

   $str = 'http://www.intrasail.com/cgi-bin?email=a@junk.com?name1=val1';
   if (!(notUrl($str))) {
      print "TEST PASS: $str: valid Url\n";
   } else {
      print "TEST FAIL:  notUrl() .\n";
   }

   $str = 'http://www.intras%ail.com';
   if (notUrl($str)) {
      print "TEST PASS: $str: invalid Url\n";
   } else {
      print "TEST FAIL: notUrl().\n";
   }

   $da = '29';
   $mo = '2';
   $yr = '2000';
   if (!(notDate($da, $mo, $yr))) {
      print "TEST PASS: $da $mo $yr: valid date\n";
   } else {
      print "TEST FAIL:  notDate() .\n";
   }

   $da = '29';
   $mo = '2';
   $yr = '2001';
   if (notDate($da, $mo, $yr)) {
      print "TEST PASS: $da $mo $yr: invalid date\n";
   } else {
      print "TEST FAIL:  notDate() .\n";
   }

   $da = '31';
   $mo = '3';
   $yr = '2037';
   if (!(notDate($da, $mo, $yr))) {
      print "TEST PASS: $da $mo $yr: valid date\n";
   } else {
      print "TEST FAIL:  notDate() .\n";
   }

   $da = '30';
   $mo = '4';
   $yr = '20 07';
   if (notDate($da, $mo, $yr)) {
      print "TEST PASS: $da $mo $yr: invalid date\n";
   } else {
      print "TEST FAIL:  notDate() .\n";
   }

   $da = '12';
   $mo = '31';
   $yr = '1998';
   if (notDate($da, $mo, $yr)) {
      print "TEST PASS: $da $mo $yr: invalid date\n";
   } else {
      print "TEST FAIL:  notDate() .\n";
   }

   $me = 'Am';
   if (!(notMeridian($me))) {
      print "TEST PASS: $me: valid meridian\n";
   } else {
      print "TEST FAIL:  notMeridian() .\n";
   }

   $me = 'Post Meridian';
   if (notMeridian($me)) {
      print "TEST PASS: $me: invalid meridian\n";
   } else {
      print "TEST FAIL:  notMeridian() .\n";
   }

   $hr = '11';
   if (!(notHour($hr))) {
      print "TEST PASS: $hr: valid hour\n";
   } else {
      print "TEST FAIL:  notHour() .\n";
   }

   $hr = '21';
   if (notHour($hr)) {
      print "TEST PASS: $hr: invalid hour\n";
   } else {
      print "TEST FAIL:  notHour() .\n";
   }

   $ms = '35';
   if (!(notMinSec($ms))) {
      print "TEST PASS: $ms: valid minsec\n";
   } else {
      print "TEST FAIL:  notMinSec() .\n";
   }

   $ms = '60';
   if (notMinSec($ms)) {
      print "TEST PASS: $ms: invalid minsec\n";
   } else {
      print "TEST FAIL:  notMinSec() .\n";
   }

   $msg = "This         is a test.";
   $msg = replaceblanks($msg);
   if ($msg eq "This%20is%20a%20test.") {
      print "TEST PASS: replaced string = $msg\n";
   } else {
      print "TEST FAIL: replaced string = $msg\n";
   }

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/neptune/redirect_url.html";
   $redirecturl = adjusturl("http://www.skytel.com/cgi-bin/page.pl?name=value&name1=value1");
   $prml = strapp $prml, "redirecturl=$redirecturl";
   parseIt $prml;
}

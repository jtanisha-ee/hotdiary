#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: informcustomers.cgi
# Purpose: This script is used to mail newsletters to members
# Creation Date: 04-03-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use AsciiDB::TagFile;

# bind master table vars
   tie %mastertab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['email', 'login', 'password', 'busname', 'suite', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'fax',
        'bphone', 'url', 'contacted', 'category0', 'category1',
        'category2', 'category3', 'category4', 'yearsinbusiness',
        'numemp', 'annualrev', 'held', 'symbol', 'description',
        'companycontact', 'email2', 'areacodes', 'numareacodes' ]};

# bind master table vars
   tie %accounttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/mastertab/accounttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login' ]};

foreach $email (keys %mastertab) {
   $login = $mastertab{$email}{login};
   $accounttab{$login}{login} = $login;
}

tied(%accounttab)->sync();

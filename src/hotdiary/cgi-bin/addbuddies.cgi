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
# FileName: addbuddies.cgi
# Purpose: it add buddies info. in hotdiary.
# Creation Date: 04-04-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

# parse the command line
   &ReadParse(*input); 
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");

   #status("This service is coming soon!");

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   #check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      #return;
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid session.\n");
              #return;
              exit;
           }
        }
   }

  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired.\n");
    #return;
    exit;
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }
                           
   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

# bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alph/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id',
	'other', 'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };



   $numentries = trim $input{'numentries'};
#form the array of entry numbers that are to be updated/deleted.
   for ($i = 0; $i <= $numentries; $i = $i + 1) {
        #how do we define an array
        $entry_array[$i] = "entryn$num";
        $num = $num + 1;
   }

   $checknum = 0;

   #$entryno in this case is $account or login name in logtab

   for ($l = 0; $l <= $numentries; $l = $l + 1) {
        $one_entryno = $entry_array[$l];
        $entryno = trim $input{$one_entryno};
        #print "entryno", $entryno;

        # check if checkbox is on.
        $checkbox_e = "checkbox$entryno";
        $checkbox = trim $input{$checkbox_e};

        $logaccount_e = "logaccoun$entryno";
        $id = trim $input{$logaccount_e};
        #print "id = ", $id;
        #print "checkbox = ", $checkbox;

        if ($checkbox eq "on") {

           $checknum = $checknum + 1;

           if (exists $logtab{$id}) { 

              $idfile = "$ENV{HDDATA}/$alph/$login/addrentrytab";
              open idhandle, "+<$idfile";
              while (<idhandle>) {
                 chop;
                 $mykey = $_;
                 if ($mykey ne "") {
                    #print "id in addrtab =", $addrtab{$mykey}{'id'}, "\n";
                    #print if address  record exists with firstname.
                    if (exists $addrtab{$mykey}) {
                      #print "exists id in addrtab =", $addrtab{$mykey}{'id'}, "\n";
                       if ($addrtab{$mykey}{'id'} ne "") {
                          #print "ne id in addrtab =", $addrtab{$mykey}{'id'}, "\n";
                          if ($addrtab{$mykey}{'id'} eq $id) {
                             status("$login: $p2 user with ID $id already exists in your diary.");
                             #return;
                             exit;
                          }
                       }
                    }
                 }
              }

               $addrentryno = getkeys();
	       #print "addrentryno ", $addrentryno;
	       $addrtab{$addrentryno}{'id'} = $id;
               #print "addrtab{id} = ", $addrtab{$addrentryno}{'id'};
               $addrtab{$addrentryno}{'entryno'} = $addrentryno;
               #print "addrtab{id} = ", $addrtab{$addrentryno}{'entryno'};

               # add the entry in the addrentrytab/$login.
               $tfile = "$ENV{HDDATA}/$alph/$login/addrentrytab";
               open thandle, ">>$tfile";
               printf thandle "%s\n", $addrentryno;
               close thandle;
               status ("$login: Address entries have been added.\n");
           }
        }
    }

    if ($checkbox ne "on") {
       status ("$login: You must atleast check one checkbox before you can add this entry\n");
       exit;
    }


# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

# save the info in db
   

   tied(%addrtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

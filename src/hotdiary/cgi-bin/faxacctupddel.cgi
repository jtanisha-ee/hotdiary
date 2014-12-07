#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: faxacctupddel.cgi
# Purpose: fax account balance updates and deletes.                  
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


#!/usr/local/bin/perl5

require "cgi-lib.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use utils::utils;
$cgi_lib'maxdata = 500000;

MAIN:
{


# parse the command line
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   $MAXDESC = 4096;

# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Update/Delete Fax Account Balance ");
  # print "testing";


   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
   $biscuit = $input{'biscuit'};
   #print "biscuit =", $biscuit;

   $numentries = $input{'numentries'};
   #print "numentries =", $numentries;
 
   if ($input{'update.x'} ne "") {     
      $action = "Update";
   } else {
   if ($input{'delete.x'} ne "") {
      $action = "Delete";
   }}

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

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      error("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
             error("Login  is an empty string.\n");
             exit;
           }
        }
   }

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
       #error("Intrusion detected. Access denied.\n");
       #exit;
   #}


   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      error("$login: Your session has already expired.\n");
      exit;
   }

   $sesstab{$biscuit}{'time'} = time();

# bind faxaccttab table vars to maintain the account balance.
   tie %faxaccttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/faxaccttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'faxid', 'balance'] };


# initialize the counter
   $num = 1;

   # from the array of entry numbers that are to be deleted.
   for ($i = 0; $i < $numentries; $i = $i + 1) {

        #how do we define an array
        $entry_array[$i] = "entryn$num";
        #print "entry_array =", $entry_array[$i];
        #print "\n";
        $num = $num + 1;
   }

   #initialize the counter
   $found_counter = 0;
   $checknum = 0; 

   for ($l = 0; $l < $numentries; $l = $l + 1) {
       $one_entryno = $entry_array[$l];
       $entryno = $input{$one_entryno};
       #print "entryno = ", $entryno;
       #print "one_entryno = ", $one_entryno;

       # check if checkbox is on.
       $checkbox_e = "checkbox$entryno";
       $checkbox = $input{$checkbox_e};
       #print "cbeckbox = ", $checkbox;

       if ($checkbox eq "on") {
          #print "checkbox is on";
          $checknum = $checknum + 1;

          # check if fax account balance record exists.
          if (!exists $faxaccttab{$entryno}) {
	     $msg = "Fax Deposit Blance record does not exist.";
          } else {
              if ($action eq "Update") {
                 #increment the counter
                 $found_counter = $found_counter + 1;
                 #print "entered the update ";

                 #modify/edit an existing fax account balances
                 $faxid_e = "faxi$entryno";
                 $faxi = trim $input{$faxid_e};
                 $balance_e = "balanc$entryno";
                 $balanc = trim $input{$balance_e};

                 $faxaccttab{$entryno}{'faxid'} = $faxi; 
                 $faxaccttab{$entryno}{'balance'} = $balanc;

                 $msg = "$login: Fax Account Balance entries have been updated.";
	      }

              if ($action eq "Delete")
              {
                 # remove it.
                 $msg = "$login: Fax Account Balanace record cannot be deleted.";
	      }
           }
        }
   }

   if ($checknum == 0) {
      error("$login: Please select or click atleast one checkbox.");
      exit;
   }

   status("$msg");

   #reset the timer.
   $sesstab{$biscuit}{'time'} = time();
   

# save the info in db
   tied(%faxaccttab)->sync();
   tied(%sesstab)->sync();

}

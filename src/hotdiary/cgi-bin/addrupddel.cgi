#!/usr/local/bin/perl5

#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,           
# in whole or in part.

#
# FileName: addrupddel.cgi
# Purpose: it updates and deletes the addresses.                  
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;
use calutil::calutil;

MAIN:
{


# parse the command line
   &ReadParse(*input); 

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);
 
   $biscuit = trim $input{'biscuit'};
   #print "biscuit =", $biscuit;

   $numentries = trim $input{'numentries'};

   if ($input{'update.x'} ne "") {
      $action = "Update";
   } else {
   if ($input{'delete.x'} ne "") {
      $action = "Delete";
   }}
   hddebug "action = $action";


# print HTML headers
   #print &PrintHeader;
   #print &HtmlTop ("HotDiary Update Address"); 

# bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['biscuit', 'login', 'time'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };      

# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec', 
   SCHEMA => { 
	ORDER => ['login', 'biscuit'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
             status("Login  is an empty string.\n");
             exit;
           }
	}
   }


  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
     delete $sesstab{$biscuit};
     delete $logsess{$login};
     status("$login: Your session has already expired.\n");
     exit;
  }

   # check for intruder access. deny the permission and exit error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
   #    error("Intrusion detected. Access denied.\n");
   #    exit;
   #}

   $sesstab{$biscuit}{'time'} = time(); 

   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';

# bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alph/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title']};


# we get entryno and num etries to be deleted from the form.
# calculate the numcheckbox from the checkbox tickmarks.


   #initailize the counters
   $num = 1;
   $found_counter =0;

#form the array of entry numbers that are to be updated/deleted.
   for ($i = 0; $i < $numentries; $i = $i + 1) {
        #how do we define an array
        $entry_array[$i] = "entryn$num";
        #print "entry_array =", $entry_array[$i];
        #print "\n";
        $num = $num + 1;

   }
  
   $checknum = 0;
 
   if ($action eq "Update") {
      $chmsg = "You must select atleast one checkbox before performing this operation. If you have already selected a checkbox, and you are still getting this message, it means that you are trying to update a self-updating contact in the address book. Self-updating contacts cannot be updated. They can either be viewed or deleted. Only the owner of a self-updating contact can update this entry.";
   } else {
      $chmsg = "You must select atleast one checkbox before performing this operation.";
   }
   for ($l = 0; $l < $numentries; $l = $l + 1) {

        $one_entryno = $entry_array[$l];
        $entryno = trim $input{$one_entryno};
        #print "entryno = ", $entryno;
        #print "one_entryno = ", $one_entryno;

        if (!exists $addrtab{$entryno}) {
            error("$login: Address record does not exist.\n");
	    exit;
        }
        $id = $addrtab{$entryno}{'id'};
       
        # check if checkbox is on.
        $checkbox_e = "checkbox$entryno";
        $checkbox = trim $input{$checkbox_e}; 

        #if ($checkbox eq "on") {
        #   $checknum = $checknum + 1;
	   #print "checkbox is on";	
           if (($id ne "") && ($action eq "Update")) {
              if ($shmsg eq "") {
                 $shmsg = "One or more self-updating address entries were selected for update, but will not be updated.";
              }
           } else {
                if (($checkbox eq "on") && ($action eq "Delete")) {
                   $chmsg = "";
                }
           }
 
           # check if address  record exists.
           if (!exists $addrtab{$entryno}) {
                #print "Address record does not exist.\n";
              error("$login: Address record does not exist.\n");
	      exit;
           } else {
              if (($action eq "Update") && ($id eq ""))
              {
                 $found_counter = $found_counter + 1;
                 $chmsg = "";
                 $fname_e = "fnam$entryno";
                 if (!(notName(trim $input{$fname_e}))) {
                    $addrtab{$entryno}{'fname'} = trim $input{$fname_e};
                 } else {
		    status("$login: Invalid characters in Name(s) ($input{$fname_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }


                 $lname_e = "lnam$entryno";
                 if (!(notName(trim $input{$lname_e}))) {
                    $addrtab{$entryno}{'lname'} = trim $input{$lname_e};
                 } else {
		    status("$login: Invalid characters in last name(s) ($input{$lname_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules.");
                   exit;
                 }

                 $busname_e = "busnam$entryno";
                 if (!(notName(trim $input{$busname_e}))) {
                    $addrtab{$entryno}{'busname'} = trim $input{$busname_e};
                 } else {
                    status("$login: Invalid characters in last name(s) ($input{$busname_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }                    
           
                  $aptno_e = "aptn$entryno";
                 if (!(notAddress(trim $input{$aptno_e}))) {
                    $addrtab{$entryno}{'aptno'} = trim $input{$aptno_e};
                 } else {
                    status("$login: Invalid characters in Aptno/Suiteno address ($input{$aptno_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules.");
                   exit;
                 }  

                 $bmonth_e = "bmont$entryno";
                 $addrtab{$entryno}{'bmonth'} = $input{$bmonth_e};

                 $bday_e = "bda$entryno";
                 $addrtab{$entryno}{'bday'} = $input{$bday_e};

		 $byear_e = "byea$entryno";
                 if (!(notNumber(trim $input{$byear_e}))) {
                    $addrtab{$entryno}{'byear'} = trim $input{$byear_e};
                 } else {
                    status("$login: Invalid characters in Year ($input{$byear_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }          

                 $street_e = "stree$entryno";
                 if (!(notAddress(trim $input{$street_e}))) {
                    $addrtab{$entryno}{'street'} = trim $input{$street_e};
                 } else {
		    status("$login: Invalid characters in street address ($input{$street_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }

                 $city_e = "cit$entryno";
                 if (!(notName(trim $input{$city_e}))) { 
                    $addrtab{$entryno}{'city'} = trim $input{$city_e};
		 } else {
		    status("$login: Invalid characters in city ($input{$city_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }
 
                 $state_e = "stat$entryno";
                 if (!(notName(trim $input{$state_e}))) { 
                    $addrtab{$entryno}{'state'} = trim $input{$state_e};
		 } else {
		    status("$login: Invalid characters in state ($input{$state_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }
 
                 $zipcode_e = "zipcod$entryno";
                 if (!(notNumber(trim $input{$zipcode_e}))) { 
                    $addrtab{$entryno}{'zipcode'} = trim $input{$zipcode_e};
		 } else {
		    status("$login: Invalid characters in zipcode ($input{$zipcode_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }
 
                 $country_e = "countr$entryno";
		 if (!(notName(trim $input{$country_e}))) {
                    $addrtab{$entryno}{'country'} = trim $input{$country_e};
		 } else {
		    status("$login: Invalid characters in country ($input{$country_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                    exit;
                 }

                 $phone_e = "phon$entryno";
		 if (!(notPhone(trim $input{$phone_e}))) {
                    $addrtab{$entryno}{'phone'} = trim $input{$phone_e};
		 } else {
		    status("$login: Invalid characters in phone ($input{$phone_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                    exit;
                 }
 
                 $pager_e = "page$entryno";
		 if (!(notPhone(trim $input{$pager_e}))) {
                    $addrtab{$entryno}{'pager'} = trim $input{$pager_e};
		 } else {
                     status("$login: Invalid characters in pager ($input{$pager_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
                 }
   
                 $fax_e = "fa$entryno";
		 if (!(notPhone(trim $input{$fax_e}))) {
                    $addrtab{$entryno}{'fax'} = trim $input{$fax_e};
		 } else {
		    status("$login: Invalid characters in fax ($input{$fax_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
		    exit;
                 } 
   
                 $cphone_e = "cphon$entryno";
		 if (!(notPhone(trim $input{$cphone_e}))) {
                    $addrtab{$entryno}{'cphone'} = trim $input{$cphone_e};
		 } else {
		    status("$login: Invalid characters in cell phone ($input{$cphone_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
	         }
   
   
                 $bphone_e = "bphon$entryno";
		 if (!(notPhone(trim $input{$bphone_e}))) {
                     $addrtab{$entryno}{'bphone'} = trim $input{$bphone_e};
		 } else {
		    status("$login: Invalid characters in business phone ($input{$bphone_e}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
                   exit;
	         }

		
                 $pagertype_e = "pagertyp$entryno";
                 $addrtab{$entryno}{'pagertype'} = trim $input{$pagertype_e};
   
                 $email_e = "emai$entryno";
                 $addrtab{$entryno}{'email'} = trim $input{$email_e};
   
                 $otherinfo_e = "otherinf$entryno";
                 $addrtab{$entryno}{'other'} = $input{$otherinfo_e};

                 $url_e = "ur$entryno";
                 $addrtab{$entryno}{'url'} = trim $input{$url_e};

		 $msg = "$login: Address entries have been updated.\n";
                 #print "address entries have been updated";
              }

              if (($action eq "Delete") && ($checkbox eq "on")) {
                 $checknum = $checknum + 1;
	         $found_counter = $found_counter + 1;

                 #$tfile = "$ENV{HDDATA}/$alph/$login/addrentrytab";
                 #open thandle, "+<$tfile";

                 #$i = 0;
 
                 #while (<thandle>) {
                 #   chop;
                 #   $onekey = $_; 
                 #   #print "entryno in the file ", $onekey;
                 #   if ($onekey ne $entryno) {
                 #      $num_array[$i] = $onekey;
                 #      #print "num_array =", $num_array[$i];
                 #      $i = $i + 1;
	         #   }
                 #}
                 #close thandle;

		 # intialize the file
                 #system "/bin/echo >$ENV{HDDATA}/$login/addrentrytab";

                 #$tfile = "$ENV{HDDATA}/$login/addrentrytab";
                 #open thandle, "+<$tfile";
              
		 #for ($k = 0; $k < $i; $k = $k + 1)  {
                 #   $get_entryno = $num_array[$k];
                 #   printf thandle "%s\n", $get_entryno;
	         #}
	         #close thandle;
               
                 delete $addrtab{$entryno};
                 withdrawmoney $login;

                 # delete entrynumber from the addrentrytab
                 # lookup the entrynumber in the addrentrytab and
	         # remove it.

		 $msg = "$login: Address entries have been deleted.\n";
	      }
	     
           } 
        #}
        #}
   }
  
   status("$chmsg $msg $shmsg $altmsg");

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

#synch the database
   tied(%addrtab)->sync();
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
}

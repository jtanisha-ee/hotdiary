#!/usr/local/bin/perl5

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


#
# FileName: syncaddr.cgi
# Purpose: it imports the addressbook
# Creation Date: 02-19-99
# Created by: Manoj Joshi
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tp::tp;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{

   # Read in all the variables set by the form
   &ReadParse(*input);

   #status("This service is coming soon!.");
   #exit;

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("syncaddsearch.cgi");

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   #if ($input{'syncaddr.x'} ne "") {
   #   $action = "Import";
   #}
   $action = "Import";


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
      status("You have been logged out automatically. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");
      exit;
   } else {
        if ($login eq "") {
           $login = $sesstab{$biscuit}{'login'};
           if ($login eq "") {
              error("Login is an empty string. Possibly invalid biscuit.\n");
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
    status("$login: Your session has already timed out. However, all your personal data is completely intact.");
    exit;
  }

  $sesstab{$biscuit}{'time'} = time();


# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };


  $fchar = substr $login, 0, 1;
  $alphaindex = $fchar . '-index';

# bind address table vars
   #tie %addrtab, 'AsciiDB::TagFile',
   #DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/addrtab",
   #SUFIX => '.rec',
   #SCHEMA => {
   #     ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
   #     'city', 'state', 'zipcode', 'country', 'phone', 'pager',
        #'fax', 'cphone', 'bphone','email', 'url', 'id'] };

# bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$login/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
	'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };



  #if (notDesc($input{'syncfile'})) {
     #error("File contents is invalid.");
     #exit;
  #}

  hddebug "fmttype = $input{'fmttype'}";

  if (($input{'fmttype'} ne "Palm Pilot") && 
	($input{'fmttype'} ne "Microsoft Outlook")) {
	status("$login: Support for $input{'fmttype'} is coming soon!.");
	exit;
  }

  if (trim $input{'syncfile'} eq "") {
     status("$login: No input or empty input file specified. Please specify a valid comma-separated file. No action performed.");
     exit;
  }

  $contents = $input{'syncfile'};
  $contents =~ s/\r//g;
  open thandle, ">$ENV{HDDATA}/$alphaindex/$login/addrtab/syncfile$$";
  printf thandle "%s", $contents;
  close thandle;

  $msg = "<DL>";
  $reccntr = 0;
  (@records) = ();

  ### auto invite #####

  
  $autoinvite = $input{'autoinvite'};
  hddebug "autoinvite = $autoinvite \n";
   
  
  if ($input{'fmttype'} eq "Palm Pilot") {
     #print $input{'syncfile'};
     (@records) = split("\n", $input{'syncfile'});
     for ($i = 0; $i <= $#records; $i++) {
        #print $records[$i];
        $records[$i] =~ s/\"//g;
        $records[$i] =~ s/\r//g;
        (@fields) = split(",", $records[$i]);
        #print "fields = ", @fields;
        $lname = trim $fields[0];
        $fname = trim $fields[1];
        $bphone = trim $fields[4];
        $phone = trim $fields[5];
        $fax = trim $fields[6];
        $email = trim $fields[8];
        $street = trim $fields[9];
        $city = trim $fields[10];
        $state = trim $fields[11];
        $country = trim $fields[12];
        $zipcode = trim $fields[13];
# Make sure the First Name or record is not null
        if ($fname eq "") {
           if (($lname eq "") && ($fname eq "") && ($bphone eq "") && ($phone eq "")
               && ($fax eq "") && ($email eq "") && ($street eq "") && ($city eq "")
               && ($state eq "") && ($country eq "") && ($zipcode eq "")) {
               $msg .= "<LI>Found empty record. Skipping record.</LI>";
               next;
           } else {
               $msg .= "<LI>Found empty first name.</LI>";
           }
        }
        if (notName($fname)) {
           $msg .= "<LI>Invalid characters in Name $fname. Resetting it to \"None\".</LI>";
           $fname = "None";
        }
        if (notName($lname)) {
           $msg .= "<LI>Invalid characters in Name $lname.</LI>";
        }
        if (notAddress($street)) {
           $msg .= "<LI>Invalid characters in Street $street</LI>";
        }
        if (notName($city)) {
           $msg .= "<LI>Invalid characters in City $city</LI>";
        }
        if (notName($state)) {
           $msg .= "<LI>Invalid characters in State $state</LI>";
        }
        if (notNumber($zipcode)) {
           $msg .= "<LI>Invalid characters in Zipcode $zipcode</LI>";
        }
        if (notName($country)) {
           $msg .= "<LI>Invalid characters in Country $country</LI>";
        }
        if (notPhone($phone)) {
           $msg .= "<LI>Invalid characters in Phone $phone</LI>";
        }
        if (notPhone($pager)) {
           $msg .= "<LI>Invalid characters in Pager $pager</LI>";
        }
        if (notPhone($fax)) {
           $msg .= "<LI>Invalid characters in Fax $fax</LI>";
        }
        if (notPhone($cellp)) {
           $msg .= "<LI>Invalid characters in CellPhone $cellp</LI>";
        }
        if (notPhone($busp)) {
           $msg .= "<LI>Invalid characters in Business Phone $busp</LI>";
        }
        if (notEmail($email)) {
           $msg .= "<LI>Invalid characters in Email $email</LI>";
        }
        if (notUrl($url)) {
           $msg .= "Invalid characters in URL $url</LI>";
        }

        $reccntr = $reccntr + 1;
        $entryno = getkeys() + $i;
        #$msg .= "<LI>Entry No = $entryno</LI>";
        $addrtab{$entryno}{'login'} = $login;
        #print "$addrtab{$entryno}{'login'}";
        #next if (trim($fname) eq "");
        $addrtab{$entryno}{'fname'} = $fname;
        $addrtab{$entryno}{'lname'} = $lname;
        $addrtab{$entryno}{'street'} = $street;
        $addrtab{$entryno}{'city'} = $city;
        $addrtab{$entryno}{'state'} = $state;
        $addrtab{$entryno}{'zipcode'} = $zipcode;
        $addrtab{$entryno}{'country'} = $country;
        $addrtab{$entryno}{'phone'} = $phone;
        $addrtab{$entryno}{'fax'} = $fax;
        $addrtab{$entryno}{'bphone'} = $bphone;
        $addrtab{$entryno}{'email'} = $email;
        $addrtab{$entryno}{'entryno'} = $entryno;
        # add the entry in the addrentrytab/$login.
        #$tfile = "$ENV{HDDATA}/$alphaindex/$login/addrentrytab";
        #open thandle, ">>$tfile";
        #printf thandle "%s\n", $entryno;
        #close thandle;


        $checkid = $logtab{$login}{'checkid'}; 
        hddebug "checkid = $checkid";
        ### auto invite this entry ###
        if (($autoinvite eq "on") && ($checkid eq "CHECKED")) {

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite', 
		'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority', 
		'editcal', 'calpeople'] };

           $em = trim $email;
           $em = "\L$em";
           $em1 = $logtab{$login}{'email'};
           $em1 = "\L$em1";
	   hddebug "email = $em";
           hddebug "em1 = $em1";
           if ("\L$em" ne "\L$em1") {
              if (($em  ne "") && (!(notEmailAddress $em))) {
                 $fn = trim $fname;
                 $fn = "\L$fn";
                 $fn =~ s/\s//g;
                 $ln = trim $lname;
                 $ln = "\L$ln";
                 $ln =~ s/\s//g;
                 hddebug "new fname = $fn";
                 if (!(exists $logtab{$fn})) {
                    $logi = $fn;
                 } else {
                    $temp = "$fn-$ln";
                    if (($ln ne "") && (!(exists $logtab{$temp}))) {
                       $logi = $temp;
                    } else {
                      $temp = "$fn_$ln";
                      if  (($ln ne "") && (!(exists $logtab{$temp}))) {
                         $logi = $temp;
                      } else {
                         $temp = "$fn-$$";
                         if (!(exists $logtab{$temp})) {
                            $logi = $temp;
                         } else {
                              hderror "Autoinvite option was selected by $login. However, could not find a unique member login for the invitee. Invitee's first name was $fn, Invitee's last name was $ln, and Invitee's email was $em";
                         }
                      }
                  }
               }
               hddebug "completed the checks";
               if (($logi ne "")  && (!(notLogin $logi))) {
                  $logtab{$logi}{'login'} = $logi;
                  $logtab{$logi}{'fname'} = $fn;
                  $logtab{$logi}{'lname'} = $ln;
                  $logtab{$logi}{'email'} = $em;
                  $logtab{$logi}{'password'} = $$;
                  hddebug "new login = $logi";
                  $alp = substr $logi, 0, 1;
                  $alp = $alp . '-index';
                  system "/bin/mkdir -p $ENV{HDREP}/$alp/$logi";
                  system "/bin/chmod 755 $ENV{HDREP}/$alp/$logi";
                  system "/bin/mkdir -p $ENV{HDHOME}/rep/$alp/$logi";
                  system "/bin/mkdir -p $ENV{HDDATA}/$alp/$logi";
                  system "/bin/chmod 755 $ENV{HDDATA}/$alp/$logi";
                  system "/bin/touch $ENV{HDDATA}/$alp/$logi/addrentrytab";
                  system "/bin/chmod 755 $ENV{HDDATA}/$alp/$logi/addrentrytab";
                  system "/bin/mkdir -p $ENV{HDDATA}/$alp/$logi/addrtab";
                  system "/bin/chmod 755 $ENV{HDDATA}/$alp/$logi/addrtab";
                  system "/bin/touch $ENV{HDDATA}/$alp/$logi/apptentrytab";
                  system "/bin/chmod 775 $ENV{HDDATA}/$alp/$logi/apptentrytab";
                  system "/bin/mkdir -p $ENV{HDDATA}/$alp/$logi/appttab";
                  system "/bin/chmod 775 $ENV{HDDATA}/$alp/$logi/appttab";
                  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alp/$logi/personal/pgrouptab";
                  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alp/$logi/subscribed/sgrouptab";
                  system "/bin/mkdir -p $ENV{HDDATA}/groups/$alp/$logi/founded/fgrouptab";
                  system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alp/$logi";
                  system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alp/$logi/index.html";
                  system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alp/$logi";
                  system "/bin/chmod 775 $ENV{HDDATA}/$alp/$logi/calendar_events.txt";

                  system "/bin/mkdir -p $ENV{HDDATA}/$alp/$logi/faxtab";
                  system "/bin/chmod 755 $ENV{HDDATA}/$alp/$logi/faxtab";

                  system "/bin/mkdir -p $ENV{HDDATA}/$alp/$logi/faxdeptab";
                  system "/bin/chmod 755 $ENV{HDDATA}/$alp/$logi/faxdeptab";
                  $surveytab{$logi}{'login'} = $logi;
                  $surveytab{$logi}{'hearaboutus'} = "HotDiary Member";
                  tied(%surveytab)->sync();
                  tied(%logtab)->sync();

		  # send email to the new user
		  hddebug "sending email";
	          hddebug "login = $login";
	          hddebug "email = $logtab{$login}{'email'}";
                  
	          system "$ENV{HDEXECCGI}/exechdsendmail \"$logi\" \"$login\"";
		  

               } else {
                  hddebug "User $logi was not created or invited, because either it was a null user, or because it was not a validated login string.";
               }
             }
          }
       }
     }
  } else {
#########################################################################
# Documenting MS Outlook Column List. This could be stored in any
# order in the CSV file, but he names of the columns should not
# change very often.

# MSOutLook Field - HotDiary Field
# Title
# First Name   --
#                ----------->  fname
# Middle Name  --
# Last Name - lname
# Suffix
# Company
# Department
# Job Title
# Business Street ----------> street
# Business Street 2 --------> street
# Business Street 3 --------> street
# Business City ------------> city
# Business State -----------> state
# Business Postal Code -----> zipcode
# Business Country ---------> country
# Home Street --------------> street
# Home Street 2 ------------> street
# Home Street 3 ------------> street
# Home City ----------------> city
# Home State ---------------> state
# Home Postal Code ---------> zipcode
# Home Country -------------> country
# Other Street
# Other Street 2
# Other Street 3
# Other City
# Other State
# Other Postal Code
# Other Country
# Assistant's Phone
# Business Fax -------------> fax
# Business Phone -----------> bphone
# Business Phone 2
# Callback
# Car Phone
# Company Main Phone
# Home Fax
# Home Phone ---------------> phone
# Home Phone 2
# ISDN
# Mobile Phone -------------> cphone
# Other Fax
# Other Phone
# Pager --------------------> pager
# Primary Phone
# Radio Phone
# TTY/TDD Phone
# Telex
# Account
# Anniversary
# Assistant's Name
# Billing Information
# Birthday
# Categories
# Children
# E-mail Address ------------> email
# E-mail Display Name
# E-mail 2 Address
# E-mail 2 Display Name
# E-mail 3 Address
# E-mail 3 Display Name
# Gender
# Government ID Number
# Hobby
# Initials
# Keywords
# Language
# Location
# Mileage
# Notes
# Office Location
# Organizational ID Number
# PO Box
# Private
# Profession
# Referred By
# Spouse
# User 1
# User 2
# User 3
# User 4
# Web Page -------------------> url

#########################################################################

     if ($input{'fmttype'} eq "Microsoft Outlook") {
        #print $input{'syncfile'};
        (@records) = split("\n", $input{'syncfile'});
# Read the first record to learn about the fields
        $records[0] =~ s/\r//g;
        $records[0] =~ s/\"//g;
        (@fields) = split(",", $records[0]);
        if ($#records < 0) {
           status("No records found in file. Please enter a valid file name.");
           exit;
        } 
        if ($#fields < 0) {
           status("Valid column definitions not found as the first row in the file. Please enter a valid file name.");
           exit;
        }
        $ind = 0;
        (@fieldtags) = ();
        foreach $field (@fields) {
           @fieldtags{$field} = $ind;
           $ind += 1; 
        } 
        #if (!(exists $fieldtags{"First Name"})) {
        #   status("Invalid input file. The first name is a mandatory field. Please create a valid input file, and retry import."); 
        #   exit;
        #}
        if ($#records > 1999) {
           $#records = 1999;
           $msg .= "<LI>You can import only 2000 records at a time. Truncating the size of the import file to 2000 records.</LI>";
        }
        for ($i = 1; $i <= $#records; $i++) {
           #print $records[$i];
# If the line is empty, skip it
           if ((trim $records[$i]) eq "") {
              next;
           }
           $other = "";
           $records[$i] =~ s/\"//g;
           $records[$i] =~ s/\r//g;
# Skip row that contains some MS messages
           if (($records[$i] =~ /Use Contacts to keep your contact/) ||
               ($records[$i] =~ /To create a contact/) ||
               ($records[$i] =~ /For more information about working with contacts/)) {
              next;
           }
           (@fields) = split(",", $records[$i]);
           #print "fields = ", @fields;
           $fname = trim $fields[$fieldtags{"First Name"}];
           if (exists $fieldtags{"Middle Name"}) {
              $fname .= " " . trim $fields[$fieldtags{"Middle Name"}];
           }
           if (exists $fieldtags{"Last Name"}) {
              $lname = trim $fields[$fieldtags{"Last Name"}];
           }
# We will check if there is a empty business street, if there is
# then we will check if the home street is empty. If both are empty
# then we store "" in $street. If Home street is not empty, then
# we store the home street in $street. 
# If both are non-empty, then we store the Business street in street
# and store the Home street in Other
# Same logic for city, state,
# zipcode, country, state
           if (exists $fieldtags{"Business Street"}) {
              $street = trim $fields[$fieldtags{"Business Street"}];
           }
           if ($street eq "") {
              if (exists $fieldtags{"Home Street"}) {
                 $street = trim $fields[$fieldtags{"Home Street"}];
              }
              if (exists $fieldtags{"Home Street 2"}) {
                 $street .= " " . trim $fields[$fieldtags{"Home Street 2"}];
              }
              if (exists $fieldtags{"Home Street 3"}) {
                 $street .= " " . trim $fields[$fieldtags{"Home Street 3"}];
              }
           } else {
              if (exists $fieldtags{"Business Street 2"}) {
                 $street .= " " . trim $fields[$fieldtags{"Business Street 2"}];
              }
              if (exists $fieldtags{"Business Street 3"}) {
                 $street .= " " . trim $fields[$fieldtags{"Business Street 3"}];
              }
              if (exists $fieldtags{"Home Street"}) {
                 $hstreet = trim $fields[$fieldtags{"Home Street"}];
              }
              if ($hstreet ne "") {
                 $other .= "Home Street = " . "$hstreet";
                 if (exists $fieldtags{"Home Street 2"}) {
                    $other .= trim $fields[$fieldtags{"Home Street 2"}];
                 }
                 if (exists $fieldtags{"Home Street 3"}) {
                    $other .= trim $fields[$fieldtags{"Home Street 3"}] . "\n";
                 }
              }
           } 

           if (exists $fieldtags{"Business City"}) {
              $city = trim $fields[$fieldtags{"Business City"}];
           }
           if ($city eq "") {
              if (exists $fieldtags{"Home City"}) {
                 $city = trim $fields[$fieldtags{"Home City"}];
              }
           } else {
              if (exists $fieldtags{"Home City"}) {
                 $hcity = trim $fields[$fieldtags{"Home City"}];
              }
              if ($hcity ne "") {
                 $other .= "Home City = " . "$hcity" . "\n";
              }
           }

           if (exists $fieldtags{"Business State"}) {
              $state = trim $fields[$fieldtags{"Business State"}];
           }
           if ($state eq "") {
              if (exists $fieldtags{"Home State"}) {
                 $state = trim $fields[$fieldtags{"Home State"}];
              }
           } else {
              if (exists $fieldtags{"Home State"}) {
                 $hstate = trim $fields[$fieldtags{"Home State"}];
              }
              if ($hstate ne "") {
                 $other .= "Home State = " . "$hstate" . " ";
              }
           }
           if (exists $fieldtags{"Business Postal Code"}) {
              $zipcode = trim $fields[$fieldtags{"Business Postal Code"}];
           }
           if ($zipcode eq "") {
              if (exists $fieldtags{"Home Postal Code"}) {
                 $zipcode = trim $fields[$fieldtags{"Home Postal Code"}];
              }
           } else {
              if (exists $fieldtags{"Home Postal Code"}) {
                 $hzipcode = trim $fields[$fieldtags{"Home Postal Code"}];
              }
              if ($hzipcode ne "") {
                 $other .= "Home Postal Code = " . "$hzipcode" . " ";
              }
           }
           if (exists $fieldtags{"Business Country"}) {
              $country = trim $fields[$fieldtags{"Business Country"}];
           }
           if ($country eq "") {
              if (exists $fieldtags{"Home Country"}) {
                 $country = trim $fields[$fieldtags{"Home Country"}];
              }
           } else {
              if (exists $fieldtags{"Home Country"}) {
                 $hcountry = trim $fields[$fieldtags{"Home Country"}];
              }
              if ($hcountry ne "") {
                 $other .= "Home Postal Code = " . "$hzipcode" . " ";
              }
           }
           if (exists $fieldtags{"Business Phone"}) {
              $bphone = trim $fields[$fieldtags{"Business Phone"}];
           }
           if (exists $fieldtags{"Business Fax"}) {
              $fax = trim $fields[$fieldtags{"Business Fax"}];
           }
           if ($fax eq "") {
              if (exists $fieldtags{"Home Fax"}) {
                 $fax = trim $fields[$fieldtags{"Home Fax"}];
              }
           } else {
              if (exists $fieldtags{"Home Fax"}) {
                 $hfax = trim $fields[$fieldtags{"Home Fax"}];
              }
              if ($hfax ne "") {
                 $other .= "Home Fax = " . "$hfax" . " ";
              }
           }
           if (exists $fieldtags{"Home Phone"}) {
              $phone = trim $fields[$fieldtags{"Home Phone"}];
           }
           if (exists $fieldtags{"E-mail Address"}) {
              $email = trim $fields[$fieldtags{"E-mail Address"}];
           }
           if (exists $fieldtags{"Web Page"}) {
              $url = trim $fields[$fieldtags{"Web Page"}];
           }
# Title
           if (exists $fieldtags{"Title"}) {
              $of = trim $fields[$fieldtags{"Title"}];
           }
           if ($of ne "") {
              $other .= "Title -$of- ";
           }
# Suffix
           if (exists $fieldtags{"Suffix"}) {
              $of = trim $fields[$fieldtags{"Suffix"}];
           }
           if ($of ne "") {
              $other .= "Suffix -$of- ";
           }
# Company
           if (exists $fieldtags{"Company"}) {
              #$of = trim $fields[$fieldtags{"Company"}];
              $busname = trim $fields[$fieldtags{"Company"}];
           }
           #if ($of ne "") {
           #   $other .= "Company -$of- ";
           #}
# Department
           if (exists $fieldtags{"Department"}) {
              $of = trim $fields[$fieldtags{"Department"}];
           }
           if ($of ne "") {
              $other .= "Department -$of- ";
           }
# Job Title
           if (exists $fieldtags{"Job Title"}) {
              $of = trim $fields[$fieldtags{"Job Title"}];
           }
           if ($of ne "") {
              $other .= "Job Title -$of- ";
           }
# Other Street
           if (exists $fieldtags{"Other Street"}) {
              $of = trim $fields[$fieldtags{"Other Street"}];
           }
           if ($of ne "") {
              $other .= "Other Street -$of- ";
           }
# Other Street 2
           if (exists $fieldtags{"Other Street 2"}) {
              $of = trim $fields[$fieldtags{"Other Street 2"}];
           }
           if ($of ne "") {
              $other .= "Other Street 2 -$of- ";
           }
# Other Street 3
           if (exists $fieldtags{"Other Street 3"}) {
              $of = trim $fields[$fieldtags{"Other Street 3"}];
           }
           if ($of ne "") {
              $other .= "Other Street 3 -$of- ";
           }
# Other City
           if (exists $fieldtags{"Other City"}) {
              $of = trim $fields[$fieldtags{"Other City"}];
           }
           if ($of ne "") {
              $other .= "Other City -$of- ";
           }
# Other State
           if (exists $fieldtags{"Other State"}) {
              $of = trim $fields[$fieldtags{"Other State"}];
           }
           if ($of ne "") {
              $other .= "Other State -$of- ";
           }
# Other Postal Code
           if (exists $fieldtags{"Other Postal Code"}) {
              $of = trim $fields[$fieldtags{"Other Postal Code"}];
           }
           if ($of ne "") {
              $other .= "Other Postal Code -$of- ";
           }
# Other Country
           if (exists $fieldtags{"Other Country"}) {
              $of = trim $fields[$fieldtags{"Other Country"}];
           }
           if ($of ne "") {
              $other .= "Other Country -$of- ";
           }
# Assistant's Phone
           if (exists $fieldtags{"Assistant's Phone"}) {
              $of = trim $fields[$fieldtags{"Assistant's Phone"}];
           }
           if ($of ne "") {
              $other .= "Assistant's Phone -$of- ";
           }
# Business Phone 2
           if (exists $fieldtags{"Business Phone 2"}) {
              $of = trim $fields[$fieldtags{"Business Phone 2"}];
           }
           if ($of ne "") {
              $other .= "Business Phone 2 -$of- ";
           }
# Callback
           if (exists $fieldtags{"Callback"}) {
              $of = trim $fields[$fieldtags{"Callback"}];
           }
           if ($of ne "") {
              $other .= "Callback -$of- ";
           }
# Car Phone
           if (exists $fieldtags{"Car Phone"}) {
              $of = trim $fields[$fieldtags{"Car Phone"}];
           }
           if ($of ne "") {
              $other .= "Car Phone -$of- ";
           }
# Company Main Phone
           if (exists $fieldtags{"Company Main Phone"}) {
              $of = trim $fields[$fieldtags{"Company Main Phone"}];
           }
           if ($of ne "") {
              $other .= "Company Main Phone -$of- ";
           }
# Home Fax
           if (exists $fieldtags{"Home Fax"}) {
              $of = trim $fields[$fieldtags{"Home Fax"}];
           }
           if ($of ne "") {
              $other .= "Home Fax -$of- ";
           }
# Home Phone 2
           if (exists $fieldtags{"Home Phone 2"}) {
              $of = trim $fields[$fieldtags{"Home Phone 2"}];
           }
           if ($of ne "") {
              $other .= "Home Phone 2 -$of- ";
           }
# ISDN
           if (exists $fieldtags{"ISDN"}) {
              $of = trim $fields[$fieldtags{"ISDN"}];
           }
           if ($of ne "") {
              $other .= "ISDN -$of- ";
           }
# Other Fax
           if (exists $fieldtags{"Other Fax"}) {
              $of = trim $fields[$fieldtags{"Other Fax"}];
           }
           if ($of ne "") {
              $other .= "Other Fax -$of- ";
           }
# Other Phone
           if (exists $fieldtags{"Other Phone"}) {
              $of = trim $fields[$fieldtags{"Other Phone"}];
           }
           if ($of ne "") {
              $other .= "Other Phone -$of- ";
           }
# Primary Phone
           if (exists $fieldtags{"Other Phone"}) {
              $of = trim $fields[$fieldtags{"Primary Phone"}];
           }
           if ($of ne "") {
              $other .= "Primary Phone -$of- ";
           }
# Radio Phone
           if (exists $fieldtags{"Radio Phone"}) {
              $of = trim $fields[$fieldtags{"Radio Phone"}];
           }
           if ($of ne "") {
              $other .= "Radio Phone -$of- ";
           }
# TTY/TDD Phone
           if (exists $fieldtags{"TTY/TDD Phone"}) {
              $of = trim $fields[$fieldtags{"TTY/TDD Phone"}];
           }
           if ($of ne "") {
              $other .= "TTY/TDD Phone -$of- ";
           }
# Telex
           if (exists $fieldtags{"Telex"}) {
              $of = trim $fields[$fieldtags{"Telex"}];
           }
           if ($of ne "") {
              $other .= "Telex -$of- ";
           }
# Account
           if (exists $fieldtags{"Account"}) {
              $of = trim $fields[$fieldtags{"Account"}];
           }
           if ($of ne "") {
              $other .= "Account -$of- ";
           }
# Anniversary
           if (exists $fieldtags{"Account"}) {
              $of = trim $fields[$fieldtags{"Anniversary"}];
           }
           if ($of ne "") {
              $other .= "Anniversary -$of- ";
           }
# Assistant's Name
           if (exists $fieldtags{"Assistant's Name"}) {
              $of = trim $fields[$fieldtags{"Assistant's Name"}];
           }
           if ($of ne "") {
              $other .= "Assistant's Name -$of- ";
           }
# Billing Information
           if (exists $fieldtags{"Billing Information"}) {
              $of = trim $fields[$fieldtags{"Billing Information"}];
           }
           if ($of ne "") {
              $other .= "Billing Information -$of- ";
           }
# Birthday
           if (exists $fieldtags{"Birthday"}) {
              $of = trim $fields[$fieldtags{"Birthday"}];
              $of =~ s/\-/ /g;
              $of = trim $of;
              ($bmonth, $bday, $byear) = split ' ', $of;
           }
           if ($of ne "") {
              $other .= "Birthday -$of- ";
           }
# Categories
           if (exists $fieldtags{"Categories"}) {
              $of = trim $fields[$fieldtags{"Categories"}];
           }
           if ($of ne "") {
              $other .= "Categories -$of- ";
           }
# Children
           if (exists $fieldtags{"Children"}) {
              $of = trim $fields[$fieldtags{"Children"}];
           }
           if ($of ne "") {
              $other .= "Children -$of- ";
           }
# E-mail Display Name
           if (exists $fieldtags{"Children"}) {
              $of = trim $fields[$fieldtags{"E-mail Display Name"}];
           }
           if ($of ne "") {
              $other .= "E-mail Display Name -$of- ";
           }
# E-mail 2 Address
           if (exists $fieldtags{"E-mail 2 Address"}) {
              $of = trim $fields[$fieldtags{"E-mail 2 Address"}];
           }
           if ($of ne "") {
              $other .= "E-mail 2 Address -$of- ";
           }
# E-mail 2 Display Name
           if (exists $fieldtags{"E-mail 2 Display Name"}) {
              $of = trim $fields[$fieldtags{"E-mail 2 Display Name"}];
           }
           if ($of ne "") {
              $other .= "E-mail 2 Display Name -$of- ";
           }
# E-mail 3 Address
           if (exists $fieldtags{"E-mail 3 Address"}) {
              $of = trim $fields[$fieldtags{"E-mail 3 Address"}];
           }
           if ($of ne "") {
              $other .= "E-mail 3 Address -$of- ";
           }
# E-mail 3 Display Name
           if (exists $fieldtags{"E-mail 3 Display Name"}) {
              $of = trim $fields[$fieldtags{"E-mail 3 Display Name"}];
           }
           if ($of ne "") {
              $other .= "E-mail 3 Display Name -$of- ";
           }
# Gender
           if (exists $fieldtags{"Gender"}) {
              $of = trim $fields[$fieldtags{"Gender"}];
           }
           if ($of ne "") {
              $other .= "Gender -$of- ";
           }
# Government ID Number
           if (exists $fieldtags{"Government ID Number"}) {
              $of = trim $fields[$fieldtags{"Government ID Number"}];
           }
           if ($of ne "") {
              $other .= "Government ID Number -$of- ";
           }
# Hobby
           if (exists $fieldtags{"Hobby"}) {
              $of = trim $fields[$fieldtags{"Hobby"}];
           }
           if ($of ne "") {
              $other .= "Hobby -$of- ";
           }
# Initials
           if (exists $fieldtags{"Initials"}) {
              $of = trim $fields[$fieldtags{"Initials"}];
           }
           if ($of ne "") {
              $other .= "Initials -$of- ";
           }
# Keywords
           if (exists $fieldtags{"Keywords"}) {
              $of = trim $fields[$fieldtags{"Keywords"}];
           }
           if ($of ne "") {
              $other .= "Keywords -$of- ";
           }
# Language
           if (exists $fieldtags{"Language"}) {
              $of = trim $fields[$fieldtags{"Language"}];
           }
           if ($of ne "") {
              $other .= "Language -$of- ";
           }
# Location
           if (exists $fieldtags{"Location"}) {
              $of = trim $fields[$fieldtags{"Location"}];
           }
           if ($of ne "") {
              $other .= "Location -$of- ";
           }
# Mileage
           if (exists $fieldtags{"Mileage"}) {
              $of = trim $fields[$fieldtags{"Mileage"}];
           }
           if ($of ne "") {
              $other .= "Mileage -$of- ";
           }
# Notes
           if (exists $fieldtags{"Notes"}) {
              $of = trim $fields[$fieldtags{"Notes"}];
           }
           if ($of ne "") {
              $other .= "Notes -$of- ";
           }
# Office Location
           if (exists $fieldtags{"Office Location"}) {
              $of = trim $fields[$fieldtags{"Office Location"}];
           }
           if ($of ne "") {
              $other .= "Office Location -$of- ";
           }
# Organizational ID Number
           if (exists $fieldtags{"Organizational ID Number"}) {
              $of = trim $fields[$fieldtags{"Organizational ID Number"}];
           }
           if ($of ne "") {
              $other .= "Organizational ID Number -$of- ";
           }
# PO Box
           if (exists $fieldtags{"PO Box"}) {
              $of = trim $fields[$fieldtags{"PO Box"}];
           }
           if ($of ne "") {
              $other .= "PO Box -$of- ";
           }
# Private
           if (exists $fieldtags{"Private"}) {
              $of = trim $fields[$fieldtags{"Private"}];
           }
           if ($of ne "") {
              $other .= "Private -$of- ";
           }
# Profession
           if (exists $fieldtags{"Profession"}) {
              $of = trim $fields[$fieldtags{"Profession"}];
           }
           if ($of ne "") {
              $other .= "Profession -$of- ";
           }
# Referred By
           if (exists $fieldtags{"Referred By"}) {
              $of = trim $fields[$fieldtags{"Referred By"}];
           }
           if ($of ne "") {
              $other .= "Referred By -$of- ";
           }
# Spouse
           if (exists $fieldtags{"Spouse"}) {
              $of = trim $fields[$fieldtags{"Spouse"}];
           }
           if ($of ne "") {
              $other .= "Spouse -$of- ";
           }
# User 1
           if (exists $fieldtags{"User 1"}) {
              $of = trim $fields[$fieldtags{"User 1"}];
           }
           if ($of ne "") {
              $other .= "User 1 -$of- ";
           }
# User 2
           if (exists $fieldtags{"User 2"}) {
              $of = trim $fields[$fieldtags{"User 2"}];
           }
           if ($of ne "") {
              $other .= "User 2 -$of- ";
           }
# User 3
           if (exists $fieldtags{"User 3"}) {
              $of = trim $fields[$fieldtags{"User 3"}];
           }
           if ($of ne "") {
              $other .= "User 3 -$of- ";
           }
# User 4
           if (exists $fieldtags{"User 4"}) {
              $of = trim $fields[$fieldtags{"User 4"}];
           }
           if ($of ne "") {
              $other .= "User 4 -$of- ";
           }

   # Make sure the First Name or record is not null
           if ($fname eq "") {
              if (($lname eq "") && ($bphone eq "") && ($phone eq "")
                  && ($fax eq "") && ($email eq "") && ($street eq "") 
		  && ($city eq "") && ($state eq "") && ($country eq "") 
		  && ($zipcode eq "") && ($url eq "") && ($other eq "")) {
                  $msg .= "<LI>Found empty record. Skipping record.</LI>";
                  next;
              } else {
                  $msg .= "<LI>Found empty first name.</LI>";
              }
           }
           
           if (notName($fname)) {
              $msg .= "<LI>Invalid characters in Name $fname</LI>";
           }
           if (notName($lname)) {
              $msg .= "<LI>Invalid characters in Name $lname</LI>";
           }
           if (notAddress($street)) {
              $msg .= "<LI>Invalid characters in Street $street</LI>";
           }
           if (notName($city)) {
              $msg .= "<LI>Invalid characters in City $city</LI>";
           }
           if (notName($state)) {
              $msg .= "<LI>Invalid characters in State $state</LI>";
           }
           if (notNumber($zipcode)) {
              $msg .= "<LI>Invalid characters in Zipcode $zipcode</LI>";
           }
           if (notName($country)) {
              $msg .= "<LI>Invalid characters in Country $country</LI>";
           }
           if (notPhone($phone)) {
              $msg .= "<LI>Invalid characters in Phone $phone</LI>";
           }
           if (notPhone($pager)) {
              $msg .= "<LI>Invalid characters in Pager $pager</LI>";
           }
           if (notPhone($fax)) {
              $msg .= "<LI>Invalid characters in Fax $fax</LI>";
           }
           if (notPhone($cellp)) {
              $msg .= "<LI>Invalid characters in CellPhone $cellp</LI>";
           }
           if (notPhone($busp)) {
              $msg .= "<LI>Invalid characters in Business Phone $busp</LI>";
           }
           if (notEmail($email)) {
              $msg .= "<LI>Invalid characters in Email $email</LI>";
           }

           if (notUrl($url)) {
              $msg .= "Invalid characters in URL $url/LI>";
           }

           $reccntr = $reccntr + 1;
           $entryno = getkeys() + $i;
           #print "$addrtab{$entryno}{'login'}";
           next if (trim($fname) eq "");
           $addrtab{$entryno}{'login'} = $login;
           $addrtab{$entryno}{'fname'} = $fname;
           $addrtab{$entryno}{'lname'} = $lname;
           $addrtab{$entryno}{'street'} = $street;
           $addrtab{$entryno}{'city'} = $city;
           $addrtab{$entryno}{'state'} = $state;
           $addrtab{$entryno}{'zipcode'} = $zipcode;
           $addrtab{$entryno}{'country'} = $country;
           $addrtab{$entryno}{'phone'} = $phone;
           $addrtab{$entryno}{'busname'} = $busname;
           $addrtab{$entryno}{'bmonth'} = $bmonth;
           $addrtab{$entryno}{'bday'} = $bday;
           $addrtab{$entryno}{'byear'} = $byear;
           $addrtab{$entryno}{'fax'} = $fax;
           $addrtab{$entryno}{'bphone'} = $bphone;
           $addrtab{$entryno}{'email'} = $email;
           $addrtab{$entryno}{'other'} = $other;
           $addrtab{$entryno}{'entryno'} = $entryno;
           # add the entry in the addrentrytab/$login.
           #$tfile = "$ENV{HDDATA}/$alphaindex/$login/addrentrytab";
           #open thandle, ">>$tfile";
           #printf thandle "%s\n", $entryno;
           #close thandle;

           ### auto invite this entry ###
           $checkid = $logtab{$login}{'checkid'};
           hddebug "checkid = $checkid";
           #if (($autoinvite eq "on") && ($id eq "") && ($checkid eq "CHECKED")) {
           if (($autoinvite eq "on") && ($checkid eq "CHECKED")) {

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus'] };


              $em = trim $email;
              $em = "\L$em";
              $em1 = $logtab{$login}{'email'};
              $em1 = "\L$em1";
              if ("\L$em" ne "\L$em1") {
                 if (($em  ne "") && (!(notEmailAddress $em))) {
                    $fn = trim $fname;
                    $fn = "\L$fn";
                    $fn =~ s/\s//g;
                    $ln = trim $lname;
                    $ln = "\L$ln";
                    $ln =~ s/\s//g;
                    if (!(exists $logtab{$fn})) {
                       $logi = $fn;
                    } else {
                       $temp = "$fn-$ln";
                       if (($ln ne "") && (!(exists $logtab{$temp}))) {
                          $logi = $temp;
                       } else {
                         $temp = "$fn_$ln";
                         if  (($ln ne "") && (!(exists $logtab{$temp}))) {
                            $logi = $temp;
                         } else {
                            $temp = "$fn-$$";
                            if (!(exists $logtab{$temp})) {
                               $logi = $temp;
                            } else {
                                 hderror "Autoinvite option was selected by $login. However, could not find a unique member login for the invitee. Invitee's first name was $fn, Invitee's last name was $ln, and Invitee's email was $em";
                            }
                         }
                     }
                  }
                  if (($logi ne "")  && (!(notLogin $logi))) {
                     $logtab{$logi}{'login'} = $logi;
                     $logtab{$logi}{'fname'} = $fn;
                     $logtab{$logi}{'lname'} = $ln;
                     $logtab{$logi}{'email'} = $em;
                     $logtab{$logi}{'password'} = $$;

                     $lalphaindex = substr $logi, 0, 1;
                     $lalphaindex = $lalphaindex . '-index';
                     system "/bin/mkdir -p $ENV{HDREP}/$lalphaindex/$logi";
                     system "/bin/chmod 755 $ENV{HDREP}/$lalphaindex/$logi";
                     system "/bin/mkdir -p $ENV{HDHOME}/rep/$lalphaindex/$logi";
                     system "/bin/mkdir -p $ENV{HDDATA}/$lalphaindex/$logi";
                     system "/bin/chmod 755 $ENV{HDDATA}/$lalphaindex/$logi";
                     system "/bin/touch $ENV{HDDATA}/$lalphaindex/$logi/addrentrytab";
                     system "/bin/chmod 755 $ENV{HDDATA}/$lalphaindex/$logi/addrentrytab";
                     system "/bin/mkdir -p $ENV{HDDATA}/$lalphaindex/$logi/addrtab";
                     system "/bin/chmod 755 $ENV{HDDATA}/$lalphaindex/$logi/addrtab";
                     system "/bin/touch $ENV{HDDATA}/$lalphaindex/$logi/apptentrytab";
                     system "/bin/chmod 775 $ENV{HDDATA}/$lalphaindex/$logi/apptentrytab";
                     system "/bin/mkdir -p $ENV{HDDATA}/$lalphaindex/$logi/appttab";
                     system "/bin/chmod 775 $ENV{HDDATA}/$lalphaindex/$logi/appttab";
                     system "/bin/mkdir -p $ENV{HDDATA}/groups/$lalphaindex/$logi/personal/pgrouptab";
                     system "/bin/mkdir -p $ENV{HDDATA}/groups/$lalphaindex/$logi/subscribed/sgrouptab";
                     system "/bin/mkdir -p $ENV{HDDATA}/groups/$lalphaindex/$logi/founded/fgrouptab";
                     system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$lalphaindex/$logi";
                     system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$lalphaindex/$logi/index.html";
                     system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$lalphaindex/$logi";
                     system "/bin/chmod 775 $ENV{HDDATA}/$lalphaindex/$logi/calendar_events.txt";

                     system "/bin/mkdir -p $ENV{HDDATA}/$lalphaindex/$logi/faxtab";
                     system "/bin/chmod 755 $ENV{HDDATA}/$lalphaindex/$logi/faxtab";

                     system "/bin/mkdir -p $ENV{HDDATA}/$lalphaindex/$logi/faxdeptab";
                     system "/bin/chmod 755 $ENV{HDDATA}/$lalphaindex/$logi/faxdeptab";
                     $surveytab{$logi}{'login'} = $logi;
                     $surveytab{$logi}{'hearaboutus'} = "Friend";
                     tied(%surveytab)->sync();
                     tied(%logtab)->sync();

                     # send email to the new user.
	             system "$ENV{HDEXECCGI}/exechdsendmail \"$logi\" \"$login\"";

                  } else {
                     hddebug "User $logi was not created or invited, because either it was a null user, or because it was not a validated login string.";
                  }
                }
             }
          }
       } #for
# **********************
     } else {
         status("$login: This synchronization service is coming soon!");
         exit;
     }
  }

  if ($action = "Import") {
     if ($reccntr eq "0") {
        status("$login: Found no records. No action performed.");
     } else {
        status("$login: Found $reccntr records. File has been imported successfully.<BR>$msg</DL>");
     }
  }


# reset the timer.
  $sesstab{$biscuit}{'time'} = time();

# save the info in db
  tied(%addrtab)->sync();
  tied(%sesstab)->sync();
  tied(%logsess)->sync();
}

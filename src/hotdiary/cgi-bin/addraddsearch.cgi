
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors. 
# Licensee shall not modify, decompile, disassemble, decrypt, extract, 
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: addraddsearch.cgi
# Purpose: it adds and searches the addresses.                  
# Creation Date: 10-09-97 
# Created by: Smitha Gudur
# 


#!/usr/local/bin/perl5

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

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};


   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");    

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

   if ($input{'add.x'} ne "") {
      $action = "Add"; 
   } else {
   if ($input{'search.x'} ne "") { 
      $action = "Search";
   }}
   hddebug "action = $action";

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

# bind cntrtab table vars
   tie %cntrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/cntrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['counter'] };

  # if ($biscuit eq "") {
  #    $somefile = "$$.html";
  #    error("Biscuit is empty.");     
  #    return;
  # }

   #print "biscuit= ", $biscuit;


   # check if session record exists. 
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

   # check for intruder access. deny the permission and return error.
   $remoteaddr = $ENV{'REMOTE_ADDR'};
   ($a, $b, $raddr) = split("-", $logsess{$login}{'biscuit'});
   #if ($raddr ne $remoteaddr) {
   #    error("$login: Intrusion detected. Access denied.\n");
       #return;
   #    exit;
   #}
        
  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    if (exists $sesstab{$biscuit}) {
       delete $sesstab{$biscuit};
    }
    if (exists $logsess{$login}) {
       delete $logsess{$login};
    }
    status("$login: Your session has timed out. Please relogin.  Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login."); 
    exit;
   }

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

# bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alpha/$login/addrtab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street', 
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };


   #$entryno = getkeys("addrnotab", "entryno");
   $entryno = getkeys();
   #print "entryno= ", $entryno;

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

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

#  add a new address, 
   if ($action eq "Add")
   { 
     $id = trim $input{'id'};
##### BEGIN CASE
     $id = "\L$id";
##### END CASE
     #print "id = ", $id, "\n";
     if ($id ne "") {
        if (!exists $logtab{$id}) {
           status("$login: The login id, $id, does not exist.");
           #return;
           exit;
        } else {
           if ($logtab{$id}{'login'} eq $login) {
              status("$login: You cannot add your own member login to your diary. To access your member information, click on the Profile button in the left frame.");
              exit;
           }
           if (($logtab{$id}{'checkid'} ne "CHECKED") && ($logtab{$id}{'login'} ne $login)) {
	      status("$login: $p2 user with ID $id is not willing to share his/her entry with anybody. Please consult him/her."); 
              exit;
           }

           #$idfile = "$ENV{HDDATA}/$alpha/$login/addrentrytab";
           #open idhandle, "+<$idfile";
           #while (<idhandle>) {
           #   chop;
           #   $mykey = $_;

	   (@hshaddrs) = (sort keys %addrtab);
	   foreach $mykey (@hshaddrs) {
              if ($mykey ne "") {
		 #hddebug "mykey = $mykey";

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
           $addrtab{$entryno}{'id'} = $id;
        }
     } else {
  
        if (notName($input{'fname'})) {
           status("$login: Invalid characters in Name(s) ($input{'fname'}). Click <a href=\"validation.html\"> here</a> to learn validation rules. \n");
           #return;
           exit;
        }


        if (notName($input{'lname'})) {
           status("$login: Invalid characters in Other(s) ($input{'lname'}).  Click <a href=\"validation.html\"> here</a> to learn validation .\n");
           #return;
           exit;
        }

        if (notName($input{'busname'})) {
           status("$login: Invalid characters in Business ($input{'busname'}).  Click <a href=\"validation.html\"> here</a> to learn validation .\n");
           #return;
           exit;
        }          

        if (notNumber($input{'byear'})) {
           status("$login: Invalid characters in Birthday Year ($input{'byear'}).  Click <a href=\"validation.html\"> here</a> to learn validation .\n");
           #return;
           exit;
        }             

        if (notAddress($input{'aptno'})) {
           status("Invalid characters in Aptno/Suiteno($input{'aptno'}).  Cli
ck <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }     
             
        if (notAddress($input{'street'})) {
           status("Invalid characters in Street Address ($input{'street'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notName($input{'city'})) {
           status("Invalid characters in City ($input{'city'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notName($input{'state'})) {
           status("Invalid characters in State ($input{'state'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
        
        if (notNumber(trim $input{'zipcode'})) {
           status("Invalid characters in Zipcode ($input{'zipcode'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
             
        if (notName($input{'country'})) {
           status("Invalid characters in Country ($input{'country'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notPhone($input{'phone'})) {
           status("Invalid characters in Phone ($input{'phone'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notPhone($input{'pager'})) {
           status("Invalid characters in Pager ($input{'pager'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }

        if (notPhone($input{'fax'})) {
           status("Invalid characters in Fax ($input{'fax'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notPhone($input{'cellp'})) {
           status("Invalid characters in Cell Phone ($input{'cellp'}). Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }

        if (notPhone($input{'busp'})) {
           status("Invalid characters in Business Phone ($input{'busp'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
        if (notEmail($input{'email'})) {
           status("Invalid characters in Email ($input{'email'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }

        if (notDesc($input{'other'})) {
           status("Invalid characters in Other Field ($input{'other'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
   
        if (notUrl($input{'url'})) {
           status("Invalid characters in URL ($input{'url'}).  Click <a href=\"validation.html\"> here</a> for valid input.\n");
           #return;
           exit;
        }
   
# if all the fields were found correct, then we update the table
 
        #if ($login eq "smitha") {
         #status("$login: bday = $input{bday}");
         #status("$login: bmonth = $input{bmonth}");
         #status("$login: byear = $input{byear}");
         #status("$login: busname = $input{busname}");
         #status("$login: aptno = $input{aptno}");
        #}

      
        depositmoney $login;
        $addrtab{$entryno}{'login'} = $login;
        $addrtab{$entryno}{'fname'} = $input{'fname'};
        $fname = trim $fname;
        $addrtab{$entryno}{'lname'} = $input{'lname'};
        $lname = trim $lname;
        $addrtab{$entryno}{'busname'} = $input{'busname'};
        $busname = trim $busname;
        $addrtab{$entryno}{'bday'} = $input{'bday'};
        $bday= trim $bday;
        $addrtab{$entryno}{'bmonth'} = $input{'bmonth'};
        $bmonth= trim $bmonth;
        $addrtab{$entryno}{'byear'} = $input{'byear'};
        $byear= trim $byear;
        $addrtab{$entryno}{'aptno'} = $input{'aptno'};
        $aptno= trim $aptno;
        $addrtab{$entryno}{'street'} = $input{'street'};
        $street = trim $street;
        $addrtab{$entryno}{'city'} = $input{'city'};
        $city = trim $city;    
        $addrtab{$entryno}{'state'} = $input{'state'};
        $state = trim $state;    
        $addrtab{$entryno}{'zipcode'} = $input{'zipcode'};
        $zipcode = trim $zipcode;
        $addrtab{$entryno}{'country'} = $input{'country'};
        $country = trim $country;
        $addrtab{$entryno}{'phone'} = $input{'phone'};
        $phone = trim $phone;
        $addrtab{$entryno}{'pager'} = $input{'pager'};
        $pager = trim $pager;
        $addrtab{$entryno}{'pagertype'} = $input{'pagertype'};
        $pagertype = trim $pagertype;
        $addrtab{$entryno}{'fax'} = $input{'fax'};
        $fax = trim $fax;
        $addrtab{$entryno}{'cphone'} = $input{'cellp'};
        $cellp = trim $cellp;
        $addrtab{$entryno}{'bphone'} = $input{'busp'};
        $busp = trim $busp;
        $addrtab{$entryno}{'email'} = $input{'email'};
        $email = trim $email;
        $addrtab{$entryno}{'other'} = $input{'other'};
        $addrtab{$entryno}{'url'} = $input{'url'};
        $url = trim $url;
     } 
     $addrtab{$entryno}{'entryno'} = $entryno;
    
     ## this is not required anymore. 
     ## add the entry in the addrentrytab/$login.
     #$tfile = "$ENV{HDDATA}/$alpha/$login/addrentrytab"; 
     #open thandle, ">>$tfile";
     #printf thandle "%s\n", $entryno;
     #close thandle;

     $checkid = $logtab{$login}{'checkid'};
     $autoinvite = $input{'autoinvite'};
     if (($autoinvite eq "on") && ($id eq "") && ($checkid eq "CHECKED")) {
        # bind surveytab table vars
        tie %surveytab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/surveytab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
'installation', 'domains', 'domain', 'orgrole', 'organization', 'orgsize', 'budget', 'timeframe', 'platform', 'priority', 'editcal', 'calpeople' ] };

        $em = trim $input{'email'};
        $em = "\L$em";
        $em1 = $logtab{$login}{'email'};
        $em1 = "\L$em1";
        if ("\L$em" ne "\L$em1") {
        if (($em  ne "") && (!(notEmailAddress $em))) {
           $fn = trim $input{'fname'};
           $fn = "\L$fn";
           $fn =~ s/\s//g;
           $ln = trim $input{'lname'};
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
           $surveytab{$logi}{'login'} = $logi;
           $surveytab{$logi}{'hearaboutus'} = "HotDiary Member";
           $emsg = "Dear $logtab{$logi}{'fname'},\n";
           $mname = $logtab{$login}{'fname'} . " " . $logtab{$login}{'lname'};
           $emsg .= "You have been invited by $mname to join $hddomain80! If you would like to contact $mname directly, please send an email to $mname at $logtab{$login}{'email'}.\n";

           $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
           $emsg .= "\nName: $logtab{$logi}{'fname'} $logtab{$logi}{'lname'}\n";
           $emsg .= "Login: $logtab{$logi}{'login'}\n";
           $emsg .= "Password: $logtab{$logi}{'password'}\n\n";
           $emsg .= "Regards,\nHotDiary Inc.\n\n";
           $emsg .= "HotDiary ($hddomain80) - New Generation Collaborative Internet Organizer\n";
 
           qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
           qx{/bin/mail -s \"Invitation From $mname\" $logtab{$logi}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};
           $alphnew = substr $logi, 0, 1;
           $alphnew = $alphnew . '-index';
           system "/bin/mkdir -p $ENV{HDREP}/$alphnew/$logi";
           system "/bin/chmod 755 $ENV{HDREP}/$alphnew/$logi";
           system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphnew/$logi";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphnew/$logi";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphnew/$logi";
           system "/bin/touch $ENV{HDDATA}/$alphnew/$logi/addrentrytab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphnew/$logi/addrentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphnew/$logi/addrtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphnew/$logi/addrtab";
           system "/bin/touch $ENV{HDDATA}/$alphnew/$logi/apptentrytab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphnew/$logi/apptentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphnew/$logi/appttab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphnew/$logi/appttab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphnew/$logi/personal/pgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphnew/$logi/subscribed/sgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphnew/$logi/founded/fgrouptab";
           system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphnew/$logi";
           system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphnew/$logi/index.html";
           system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphnew/$logi";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphnew/$logi/calendar_events.txt";
 
           system "/bin/mkdir -p $ENV{HDDATA}/$alphnew/$logi/faxtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphnew/$logi/faxtab";
 
           system "/bin/mkdir -p $ENV{HDDATA}/$alphnew/$logi/faxdeptab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphnew/$logi/faxdeptab";
           } else {
                hddebug "User $logi was not created or invited, because either it was a null user, or because it was not a validated login string.";
           }

        }
        }
     }
     if ($cntrtab{'entrycounter'}{'counter'} != 0) {
        $counter = $cntrtab{'entrycounter'}{'counter'} + 1;
        if (($counter % $ENV{'USE_ADDR_WINNER_FREQ'}) == 0) {
           status("$login: Address entry has been added.<BR>Congratulations! You are the potential lucky user of HotDiary, and may qualify to win a free Skytel pager. Contact us giving details about your member name, email, and postal address and your entry number ($entryno) and we will send you a free SkyTel pager after verification of your account!");
           $logtab{$login}{'winner'} = "Yes - Lucky User ($entryno)";
        } else {
           status("$login: Address entry has been added.");
        }
        $cntrtab{'entrycounter'}{'counter'} = $counter;
     }
     # if we reached here, the add was successful
     tied(%cntrtab)->sync();
   }

   if ($action eq "Search") { 
      system "/bin/rm -f $ENV{HDREP}/$alpha/$login/ser*.html";      
      $title = time();
      $fname = trim $input{'fname'};
      if ($fname eq "") {
         $fname = trim $input{'lname'};
      }

      #hddebug "name = $fname";
      $found_counter = 0;
      $page_entries = 0;
      $page_num = 0;
      $prevpage = "";
      $nextpage = "";
      #$buddy = "";

      #unlink glob("$ENV{HDREP}/$alpha/$login/searchpage*.html"), "lastpage.html";

      #go through each entry in the address table.
      # @allkeys = keys %addrtab;

      #system "/bin/rm $ENV{HDREP}/$alpha/$login/searchaddrtblent*.html";
      #$tfile = "$ENV{HDDATA}/$alpha/$login/addrentrytab"; 
      #open thandle, "+<$tfile";
      #while (<thandle>) {

      (@hshentries) = (sort keys %addrtab);
      foreach $onekey (@hshentries) {
         #chop;
         #$onekey = $_;
         #if ($login eq "smitha") {
         #   status("found onekey = $onekey");
         #}

         $nomatch = "true";
         if ($onekey ne "")  {
   	    #hddebug "onekey = $onekey";
            #print if address  record exists with firstname.
            if (exists $addrtab{$onekey}) {
               if ($addrtab{$onekey}{'id'} ne "") {
                  $noshare = "false";
                  $id = $addrtab{$onekey}{'id'};
                  if ($id ne "") {
                     if (!(exists $logtab{$id})) {
                        next;
                     } else {
                        if ($logtab{$id}{'checkid'} ne "CHECKED") {
                           next;
                        }
                     }
                  }
                     

                  #if (exists $logtab{$id}) {
                     #if ($logtab{$id}{'checkid'} ne "CHECKED") {
                      #if ($dmsg eq "") { 
                        # $dmsg = "$login: One or more shared address entries were not displayed, since the owner(s) of those entries has disabled sharing of their ID."; 
	              #}
                      #last;
                  #   }
                  #}
                  #if ("\U$logtab{$id}{'fname'}" eq "\U$fname") {

               #if ($login eq "smitha") {
               #   status("fname = $logtab{$id}{'fname'}");
               #}
                  #if ((nmmatch $logtab{$id}{'fname'}, $fname) ||
    		  #    (nmmatch $logtab{$id}{'lname'}, $fname) ) {
                  if ( ((index "\L$logtab{$id}{'fname'}", "\L$fname") != -1) ||
                    ((index "\L$logtab{$id}{'lname'}", "\L$fname") != -1)) {
                  #if ($logtab{$id}{'fname'} =~ /$fname[\w]+/) {
	             #hddebug "$fname came here1";
                     $nomatch = "false";
                     ($dbentryno = $onekey) =~ s/\n/\n<BR>/g;
                     ($dbfname = $logtab{$id}{'fname'}) =~ s/\n/\n<BR>/g;
                     ($dblname = $logtab{$id}{'lname'}) =~ s/\n/\n<BR>/g;
                     ($dbstreet = $logtab{$id}{'street'}) =~ s/\n/\n<BR>/g;
                     ($dbcity = $logtab{$id}{'city'}) =~ s/\n/\n<BR>/g;
                     ($dbstate = $logtab{$id}{'state'}) =~ s/\n/\n<BR>/g;
                     ($dbzipcode = $logtab{$id}{'zipcode'}) =~ s/\n/\n<BR>/g;
                     ($dbcountry = $logtab{$id}{'country'}) =~ s/\n/\n<BR>/g;
                     ($dbphone = $logtab{$id}{'phone'}) =~ s/\n/\n<BR>/g;
                     ($dbpager = $logtab{$id}{'pager'}) =~ s/\n/\n<BR>/g;
                     ($dbpagertype = $logtab{$id}{'pagertype'}) =~ s/\n/\n<BR>/g;
                     if ($dbpagertype eq "") {
                        $dbpagertype = "SkyTel Pager";
                     }
                     ($dbfax = $logtab{$id}{'fax'}) =~ s/\n/\n<BR>/g;
                     ($dbcphone = $logtab{$id}{'cphone'}) =~ s/\n/\n<BR>/g;
                     ($dbbphone = $logtab{$id}{'bphone'}) =~ s/\n/\n<BR>/g;
                     ($dbemail = $logtab{$id}{'email'}) =~ s/\n/\n<BR>/g;
                     #($dbotherinfo = $logtab{$id}{'other'}) =~ s/\n/\n<BR>/g;
                     $dbotherinfo = "";
                     ($dburl = $logtab{$id}{'url'}) =~ s/\n/\n<BR>/g;
                  }
               } else {
                    $noshare = "true";
               }
            } else {
                 $noshare = "true";
            }
            if ($noshare eq "true") {
               if (exists $addrtab{$onekey}) {
               #if ("\U$addrtab{$onekey}{'fname'}" eq "\U$fname") {
               #if ($login eq "smitha") {
               #   status("fname = $addrtab{$onekey}{'fname'}");
               #}
               #if ((nmmatch $addrtab{$onekey}{'fname'}, $fname) ||
               #    (nmmatch $addrtab{$onekey}{'lname'}, $fname) ) {
               #hddebug "fname = $fname";
               #$alname = "\L$addrtab{$onekey}{'lname'}";
               #hddebug "lname = $alname";
               if ( ((index "\L$addrtab{$onekey}{'fname'}", "\L$fname") != -1) ||
                    ((index "\L$addrtab{$onekey}{'lname'}", "\L$fname") != -1))  {
                    #hddebug "Matching $fname";
               #if ($addrtab{$onekey}{'fname'} =~ /$fname[\w]+/) {
	             #hddebug "$fname came here2";
                  $nomatch = "false";
                  ($dbentryno = $addrtab{$onekey}{'entryno'}) =~ s/\n/\n<BR>/g;
                  ($dbfname = $addrtab{$onekey}{'fname'}) =~ s/\n/\n<BR>/g;
                  ($dblname = $addrtab{$onekey}{'lname'}) =~ s/\n/\n<BR>/g;
                  ($dbstreet = $addrtab{$onekey}{'street'}) =~ s/\n/\n<BR>/g;
                  ($dbaptno = $addrtab{$onekey}{'aptno'}) =~ s/\n/\n<BR>/g;
                  ($dbbday = $addrtab{$onekey}{'bday'}) =~ s/\n/\n<BR>/g;
                  ($dbbmonth = $addrtab{$onekey}{'bmonth'}) =~ s/\n/\n<BR>/g;
                  $dbbmonth = getmonthstr $dbbmonth;
                  ($dbbyear = $addrtab{$onekey}{'byear'}) =~ s/\n/\n<BR>/g;
                  ($dbbusname = $addrtab{$onekey}{'busname'}) =~ s/\n/\n<BR>/g;
                  ($dbcity = $addrtab{$onekey}{'city'}) =~ s/\n/\n<BR>/g;
                  ($dbstate = $addrtab{$onekey}{'state'}) =~ s/\n/\n<BR>/g;
                  ($dbzipcode = $addrtab{$onekey}{'zipcode'}) =~ s/\n/\n<BR>/g;
                  ($dbcountry = $addrtab{$onekey}{'country'}) =~ s/\n/\n<BR>/g;
                  ($dbphone = $addrtab{$onekey}{'phone'}) =~ s/\n/\n<BR>/g;
                  ($dbpager = $addrtab{$onekey}{'pager'}) =~ s/\n/\n<BR>/g;
                  ($dbpagertype = $addrtab{$onekey}{'pagertype'}) =~ s/\n/\n<BR>/g;
                  if ($dbpagertype eq "") {
                     $dbpagertype = "SkyTel Pager";
                  }
                  ($dbfax = $addrtab{$onekey}{'fax'}) =~ s/\n/\n<BR>/g;
                  ($dbcphone = $addrtab{$onekey}{'cphone'}) =~ s/\n/\n<BR>/g;
                  ($dbbphone = $addrtab{$onekey}{'bphone'}) =~ s/\n/\n<BR>/g;
                  ($dbemail = $addrtab{$onekey}{'email'}) =~ s/\n/\n<BR>/g;
                  $dbotherinfo = $addrtab{$onekey}{'other'};
                  ($dburl = $addrtab{$onekey}{'url'}) =~ s/\n/\n<BR>/g;
               }
               } else {
                    next;
               }
            }
            if ($nomatch eq "false") {
            #if ("\U$dbfname" eq "\U$fname") {
            #if ((nmmatch $dbfname, $fname) ||
            #    (nmmatch $dblname, $fname) ) {
            if ( ((index "\L$dbfname", "\L$fname") != -1) ||
               ((index "\L$dblname", "\L$fname") != -1))  {
                #hddebug "came here";
	             #hddebug "$fname came here3";
            #if ($dbfname =~ /$fname[\w]+/) {
               $found_counter= $found_counter + 1;
               $page_entries = $page_entries + 1;
               if ($page_entries eq 1) {
                  $page_num = $page_num + 1;
               }
               #print "page_num = ", $page_num, "\n";
               if ($page_num eq 1) {
                  $prevpage = "rep/$alpha/$login/ser$title$biscuit$page_num.html";
               } else {
                  $pageno = $page_num - 1;
                  $prevpage = "rep/$alpha/$login/ser$title$biscuit$pageno.html";
               }
               $pageno = $page_num + 1;
               if ($page_num eq 1) {
                  $nextpage = "rep/$alpha/$login/ser$title$biscuit$pageno.html";
               } else {
                  $nextpage = "rep/$alpha/$login/ser$title$biscuit$pageno.html";
	       }

               #$buddy = "rep/$alpha/$login/ser$title$biscuit$friend.html";

               #print "nextpage = ", $nextpage, "\n";
               #print "prevpage = ", $prevpage, "\n";

               #($entryno = $addrtab{$onekey}{'entryno'}) =~ s/\n/\n<BR>/g;
               #print "Entryno = ", $entryno, "\n";
               $prml = "";
               $prml = strapp $prml, "entrynfield=entryn$page_entries";
               $prml = strapp $prml, "entryno=$dbentryno";

               #$ENV{'checkboxfield'} = "checkbox$dbentryno";
               $prml = strapp $prml, "checkboxfield=checkbox$dbentryno";

               #($outfield = $addrtab{$onekey}{'fname'}) =~ s/\n/\n<BR>/g;
               #print "First Name = ", $outfield, "\n"; 
               $prml = strapp $prml, "fname=$dbfname";
               $prml = strapp $prml, "fnamfield=fnam$dbentryno";

               #($outfield = $addrtab{$onekey}{'lname'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "lname=$dblname";
               $prml = strapp $prml, "lnamfield=lnam$dbentryno";
               #print "Last Name = ", $outfield, "\n";

#if ($login eq "smitha") {
         #status("$login: bday = $dbbday");
         #status("$login: bmonth = $dbbmonth");
         #status("$login: byear = $dbbyear");
         #status("$login: busname = $dbbusname");
         #status("$login: aptno = $dbaptno");
#}
               $prml = strapp $prml, "busname=$dbbusname";
               $prml = strapp $prml, "busnamfield=busnam$dbentryno";

               $prml = strapp $prml, "bday=$dbbday";
               $prml = strapp $prml, "bdafield=bda$dbentryno";

               $prml = strapp $prml, "bmonth=$dbbmonth";
               $prml = strapp $prml, "bmontfield=bmont$dbentryno";

               $prml = strapp $prml, "byear=$dbbyear";
               $prml = strapp $prml, "byeafield=byea$dbentryno";

               $prml = strapp $prml, "aptno=$dbaptno";
               $prml = strapp $prml, "aptnfield=aptn$dbentryno";

               #($outfield = $addrtab{$onekey}{'street'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "street=$dbstreet";
               $prml = strapp $prml, "streefield=stree$dbentryno";
               #print "Street = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'city'}) =~ s/\n/\n<BR>/g;
               #print "City = ", $outfield, "\n";
               $prml = strapp $prml, "city=$dbcity";
               $prml = strapp $prml, "citfield=cit$dbentryno";

               #($outfield = $addrtab{$onekey}{'state'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "state=$dbstate";
               $prml = strapp $prml, "statfield=stat$dbentryno";
               #print "State = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'zipcode'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "zipcode=$dbzipcode";
               $prml = strapp $prml, "zipcodfield=zipcod$dbentryno";
               #print "ZipCode = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'country'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "country=$dbcountry";
               $prml = strapp $prml, "countrfield=countr$dbentryno";
               #print "Country = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'phone'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "phone=$dbphone";
               $prml = strapp $prml, "phonfield=phon$dbentryno";
               #print "Phone = ", $outfield, "\n";

               $prml = strapp $prml, "pagertype=$dbpagertype";
               $prml = strapp $prml, "pagertypfield=pagertyp$dbentryno";

               #($outfield = $addrtab{$onekey}{'pager'}) =~ s/\n/\n<BR>/g;
               $dbpager = adjusturl $dbpager;
               $dbpager = getPhoneDigits $dbpager;
               $prml = strapp $prml, "pager=$dbpager";
               $prml = strapp $prml, "pagefield=page$dbentryno";
               #print "Pager = ", $outfield, "\n";
               $dbpagertype =~ s/ /+/g;
	       $pageurl = adjusturl("cgi-bin/execsendpage.cgi?thispage=$ENV{'HDDOMAIN'}/rep/$alpha/$login/ser$title$biscuit$page_num.html&to=$dbpager&biscuit=$biscuit&pt=$dbpagertype");
	       $prml = strapp $prml, "pageurl=$pageurl"; 

               #($outfield = $addrtab{$onekey}{'fax'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "fax=$dbfax";
               $prml = strapp $prml, "fafield=fa$dbentryno";
               #print "Fax = ", $outfield, "\n";
               $dbfax = getPhoneDigits $dbfax;
	       $faxurl = adjusturl("cgi-bin/execsendfax.cgi?thispage=ser$title$biscuit$page_num.html&to=$dbfax&biscuit=$biscuit");
	       $prml = strapp $prml, "faxurl=$faxurl"; 

               #($outfield = $addrtab{$onekey}{'cphone'}) =~ s/\n/\n<BR>/g;
               #$prml = strapp $prml, "cphone=$dbcphone";
               $prml = strapp $prml, "cellp=$dbcphone";
               $prml = strapp $prml, "cphonfield=cphon$dbentryno";
               #print "Fax = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'bphone'}) =~ s/\n/\n<BR>/g;
               #$prml = strapp $prml, "bphone=$dbbphone";
# Found a bug where the busp and cellp were always blank when searched
               $prml = strapp $prml, "busp=$dbbphone";
               $prml = strapp $prml, "bphonfield=bphon$dbentryno";
               #print "BusinessPhone = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'email'}) =~ s/\n/\n<BR>/g;
               $dbemail = adjusturl $dbemail;
               $prml = strapp $prml, "email=$dbemail";
               $prml = strapp $prml, "emaifield=emai$dbentryno";
               #print "Email = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'url'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "url=$dburl";
               $prml = strapp $prml, "urfield=ur$dbentryno";
               #print "URL = ", $outfield, "\n";

               $prml = strapp $prml, "otherinfo=$dbotherinfo";
               $prml = strapp $prml, "otherinffield=otherinf$dbentryno";

	       $jumpurl = $dburl;  
	       $prml = strapp $prml, "jumpurl=$jumpurl"; 
               $prml = strapp $prml, "template=$ENV{HDTMPL}/searchaddrtblentry.html";
               $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchaddrtblentry.html";

               $fromstreet = $logtab{$login}{'street'};
               $fromstreet =~ s/ /+/g;
               $fromcity = $logtab{$login}{'city'};
               $fromcity =~ s/ /+/g;
               $fromstate = $logtab{$login}{'state'};
               $fromstate =~ s/ /+/g;

               $tostreet = $dbstreet;
               $tostreet =~ s/ /+/g;
               $tocity = $dbcity;
               $tocity =~ s/ /+/g;
               $tostate = $dbstate;
               $tostate =~ s/ /+/g;
               #$directions = adjusturl "http://www.zip2.com/scripts/map.dll?mad1=317+Edgewater+Drive&mct1=Milpitas&mst1=CA&mad2=2149+Fordham+Drive&mct2=Santa+Clara&mst2=CA&type=gis&mwt=350&mht=280&mwt1=350&mht1=280&mwt2=350&mht2=280&mwt3=350&mht3=280&method=d2d&ck=21439101&userid=55724010&userpw=xtv0J_txAwt8tE_FD0C&version=663922&sType=street&adrVer=918629102&ver=d3.0&GetDir.x=Get+Directions";
               $directions = adjusturl "http://www.zip2.com/scripts/map.dll?mad1=$fromstreet&mct1=$fromcity&mst1=$fromstate&mad2=$tostreet&mct2=$tocity&mst2=$tostate&type=gis&mwt=350&mht=280&mwt1=350&mht1=280&mwt2=350&mht2=280&mwt3=350&mht3=280&method=d2d&ck=21439101&userid=55724010&userpw=xtv0J_txAwt8tE_FD0C&version=663922&sType=street&adrVer=918629102&ver=d3.0&GetDir.x=Get+Directions";
               $prml = strapp $prml, "directions=$directions";

               parseIt $prml;
               $prml = "";

               if ($page_entries eq 1) {
                  #if ($page_num eq 1 ) {
                     #system "/bin/cat ../templates/content.html > $ENV{HDREP}/$alpha/$login/$biscuit$page_num.html";
                  #}
                 # Generate Search Page Header
                  $prml = "";
                  
                  $prml = strapp $prml, "biscuit=$biscuit";
                  #$expiry = localtime(time() + 5);
                  #$expiry = "\:$expiry";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpghdr.html"; 
		  $prml = strapp $prml, "pagenumber=Page: $page_num <BR>";
                  #$prml = strapp $prml, "expiry=$expiry";
                  $prml = strapp $prml, "expiry=";
                  $prml = strapp $prml, "pager=$dbpager";
                  $prml = strapp $prml, "pagefield=page$dbentryno";

		  #$pageurl = "$ENV{HDREP}/$alpha/$login/sendpage.html?thispage=<ser$title$biscuit$page_num.html>&to=<$pagefield>";
		  #$pageurl = "$ENV{HDREP}/$alpha/$login/sendpage.html";
	          #$prml = strapp $prml, "pageurl=testpageurl"; 

                  $urlcgi = buildurl("execaddrupddel.cgi");
                  $prml = strapp $prml, "actioncgi=$urlcgi";
		  if ($fname eq "") {
                    $prml = strapp $prml, "label=$p2 Search results for all entries";
		  } else {
                    $prml = strapp $prml, "label=$p2 Search results for \"$fname\"";
                  }
                  $prml = strapp $prml, "label1=Click on Email, Pager and Fax Icons to activate TelTalk";
                  parseIt $prml;
                  $prml = "";
                  #if ($page_num eq 1) {
                    #system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";
                  #} else {
                    system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpghdr.html > $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";
                  #}


                  # Generate Standard Table Header
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html"; 
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblhdr.html";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblhdr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";
               }

               system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchaddrtblentry.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";

               if ($page_entries eq 2) {
# this is the last time we will use page_entries in this iteration, 
# so we can reset it now to 0
                  # Generate Standard Table Footer
                  $prml = strapp $prml, "numentries=$page_entries";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblftr.html";
                  $prml = strapp $prml, "nextpage=$nextpage";
                  $prml = strapp $prml, "prevpage=$prevpage";
                  #$prml = strapp $prml, "buddy=$buddy";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblftr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";

                  # Generate Search Page Footer
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpgftr.html";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpgftr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";
               }
               if ($page_entries eq 2) {
                  $page_entries = 0;
               }
            }
            }
         }
      }
 
      close thandle;

# deal with cases when the $found_counter are odd numbered
      $rem = $found_counter % 2;
      if ($rem != 0) {
         # Generate Standard Table Footer
         $prml = strapp $prml, "numentries=$page_entries";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/stdtblftr.html";
         $prml = strapp $prml, "nextpage=$nextpage";
         $prml = strapp $prml, "prevpage=$prevpage";
         #$prml = strapp $prml, "buddy=$buddy";
         parseIt $prml;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/stdtblftr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";

         # Generate Search Page Footer
         $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpgftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/searchpgftr.html";
         parseIt $prml;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alpha/$login/searchpgftr.html >> $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html";
      }


# overwrite nextpage with lastpage
      #$expiry = localtime(time() + 5);
      #$expiry = "\:$expiry";
      #$prml = strapp $prml, "expiry=$expiry";
      $prml = strapp $prml, "expiry=";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/lastpage.html";
      $prml = strapp $prml, 
      			"prevpage=rep/$alpha/$login/ser$title$biscuit$page_num.html";
      $pageno = $page_num + 1; 
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alpha/$login/ser$title$biscuit$pageno.html";
      parseIt $prml;
      $prml = "";
      system "cp $ENV{HDREP}/$alpha/$login/$biscuit.html $ENV{HDREP}/$alpha/$login/ser$title$biscuit$pageno.html";

      if ($found_counter eq 0) {
          if ($fname eq "") {
             status("$login: Your address book is empty.");
          } else {
             status("$login: $fname not found in addresses. If you enter fewer characters in the First Name or Last Name field, you are more likely to find the contact you are looking for. <p>Note that we do not search by Business Name or any other field, except for the contact's First Name or Last Name.<p>To view all the contacts, simply press the Search button without entering anything in the First or Last Name.");
          }
      }
      else {
            #system "/bin/cat $ENV{HDTMPL}/content.html\n\n"; 
            $page_num = "1";
            #system "/bin/cat $ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html"; 
            hdsystemcat "$ENV{HDREP}/$alpha/$login/ser$title$biscuit$page_num.html"; 
        }
    }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   #tied(%addrnotab)->sync();
   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
   if ($action eq "Add") {
      tied(%cntrtab)->sync();
      tied(%addrtab)->sync();
   }
}

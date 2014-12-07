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
   $SESSION_TIMEOUT = 120;

   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");    

   $biscuit = $input{'biscuit'};
   #print "biscuit = ", $biscuit;

#   if ($input{'add.x'} ne "") {
#      $action = "Add"; 
#   } else {
#   if ($input{'search.x'} ne "") { 
#      $action = "Search";
#   }}
 

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
        'city', 'state', 'zipcode', 'country', 'phone', 'pager',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid'] };      

  # if ($biscuit eq "") {
  #    $somefile = "$$.html";
  #    error("Biscuit is empty.");     
  #    return;
  # }

   #print "biscuit= ", $biscuit;

   # check if session record exists. 
 #  if (!exists $sesstab{$biscuit}) {
 #     error("Biscuit does not exist.\n");
 #     return;
 #  } else {
 #       $login = $sesstab{$biscuit}{'login'};
 #       if ($login eq "") {
 #          error("Login is an empty string. Possibly invalid biscuit.\n");
 #          return;
 #       }
 #  }

        
 # if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
 #   delete $sesstab{$biscuit};
 #   delete $logsess{$login};
 #   error("$login: Your session has already expired.\n");
 #   return;
 #  }

# bind address table vars
   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/addrtab",
   SUFIX => '.rec', 
   SCHEMA => { 
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street', 
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 
        'fax', 'cphone', 'bphone','email', 'url', 'id'] };


   #$entryno = getkeys("addrnotab", "entryno");
   $entryno = getkeys();
   #print "entryno= ", $entryno;

# reset the timer.
 #  $sesstab{$biscuit}{'time'} = time(); 

#  add a new address, 
   if ($action eq "Add")
   { 
     $id = trim $input{'id'};
     #print "id = ", $id, "\n";
     if ($id ne "") {
        if (!exists $logtab{$id}) {
           error("The login id, $id, does not exist.");
           return;
        } else {
           if ($logtab{$id}{'checkid'} ne "CHECKED") {
	      error("$login: HotDiary user with ID $id is not willing to share his/her entry with anybody. Please consult him/her."); 
              return;
           }

           $idfile = "$ENV{HDDATA}/$login/addrentrytab";
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
		          status("$login: HotDiary user with ID $id already exists in your diary.");
		          return;
	               }	
                    }
                 }
              }
           }
           $addrtab{$entryno}{'id'} = $id;
        }
     } else {
  
        if (notName($input{'fname'})) {
           error("Please enter only alphabets in the first name.\n");
           return;
        }


        if (notName($input{'lname'})) {
           error("Please enter only alphabets in the last name.");
           return;
        }
             
        if (notAddress($input{'street'})) {
           error("Please donot enter binary characters in the street address.");
           return;
        }
   
        if (notName($input{'city'})) {
           error("Please enter only alphabets in the city.");
           return;
        }
   
        if (notName($input{'state'})) {
           error("Please enter only alphabets in the state.");
           return;
        }
        
        if (notNumber($input{'zipcode'})) {
           error("Please enter only numbers in the zipcode.");
           return;
        }
             
        if (notName($input{'country'})) {
           error("Please enter only alphabets in the country.");
           return;
        }
   
        if (notPhone($input{'phone'})) {
           error("Please enter alphabets or numericals in the phone.");
           return;
        }
   
        if (notPhone($input{'pager'})) {
           error("Please enter alphabets or numericals in the pager.");
           return;
        }
   
        if (notPhone($input{'fax'})) {
           error("Please enter alphabets or numericals in the fax.");
           return;
        }
   
        if (notPhone($input{'cellp'})) {
           error("Please enter alphabets or numericals in the cell phone.");
           return;
        }

        if (notPhone($input{'busp'})) {
           error("Please enter alphabets or numericals in the business phone.");
           return;
        }
   
        if (notEmail($input{'email'})) {
           error("Please enter proper email address.");
           return;
        }
   
        if (notUrl($input{'url'})) {
           error("Please enter proper URL.");
           return;
        }
   
# if all the fields were found correct, then we update the table
        $addrtab{$entryno}{'login'} = $login;
        $addrtab{$entryno}{'fname'} = $input{'fname'};
        $fname = trim $fname;
        $addrtab{$entryno}{'lname'} = $input{'lname'};
        $lname = trim $lname;
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
        $addrtab{$entryno}{'fax'} = $input{'fax'};
        $fax = trim $fax;
        $addrtab{$entryno}{'cphone'} = $input{'cellp'};
        $cellp = trim $cellp;
        $addrtab{$entryno}{'bphone'} = $input{'busp'};
        $busp = trim $busp;
        $addrtab{$entryno}{'email'} = $input{'email'};
        $email = trim $email;
        $addrtab{$entryno}{'url'} = $input{'url'};
        $url = trim $url;
     }  

     $addrtab{$entryno}{'entryno'} = $entryno;
     
     # add the entry in the addrentrytab/$login.
     $tfile = "$ENV{HDDATA}/$login/addrentrytab"; 
     open thandle, ">>$tfile";
     printf thandle "%s\n", $entryno;

     close thandle;
     status("$login: Address entry has been added\n");
     # if we reached here, the add was successful
   }

   if ($action eq "Search") { 

      $fname = $input{'fname'};
      $found_counter = 0;
      $page_entries = 0;
      $page_num = 0;
      $prevpage = "";
      $nextpage = "";

      #unlink glob("$ENV{HDREP}/$login/searchpage*.html"), "lastpage.html";

      #go through each entry in the address table.
      # @allkeys = keys %addrtab;

      #system "/bin/rm $ENV{HDREP}/$login/searchaddrtblent*.html";
      $tfile = "$ENV{HDDATA}/$login/addrentrytab"; 
      open thandle, "+<$tfile";
      while (<thandle>) {
         chop;
         $onekey = $_;

         $nomatch = "true";
         if ($onekey ne "")  {
          
            #print if address  record exists with firstname.
            if (exists $addrtab{$onekey}) {
               if ($addrtab{$onekey}{'id'} ne "") {
                  $noshare = "false";
                  $id = $addrtab{$onekey}{'id'};

                  if ($logtab{$id}{'checkid'} ne "CHECKED") {
                      #if ($dmsg eq "") { 
                        # $dmsg = "$login: One or more shared address entries were not displayed, since the owner(s) of those entries has disabled sharing of their ID."; 
	              #}
                      last;
                  }
                  if ($logtab{$id}{'fname'} eq $fname) {
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
                     ($dbfax = $logtab{$id}{'fax'}) =~ s/\n/\n<BR>/g;
                     ($dbcphone = $logtab{$id}{'cphone'}) =~ s/\n/\n<BR>/g;
                     ($dbbphone = $logtab{$id}{'bphone'}) =~ s/\n/\n<BR>/g;
                     ($dbemail = $logtab{$id}{'email'}) =~ s/\n/\n<BR>/g;
                     ($dburl = $logtab{$id}{'url'}) =~ s/\n/\n<BR>/g;
                  }
               } else {
                    $noshare = "true";
               }
            } else {
                 $noshare = "true";
            }
            if ($noshare eq "true") {
               if ($addrtab{$onekey}{'fname'} eq $fname) {
                  $nomatch = "false";
                  ($dbentryno = $addrtab{$onekey}{'entryno'}) =~ s/\n/\n<BR>/g;
                  ($dbfname = $addrtab{$onekey}{'fname'}) =~ s/\n/\n<BR>/g;
                  ($dblname = $addrtab{$onekey}{'lname'}) =~ s/\n/\n<BR>/g;
                  ($dbstreet = $addrtab{$onekey}{'street'}) =~ s/\n/\n<BR>/g;
                  ($dbcity = $addrtab{$onekey}{'city'}) =~ s/\n/\n<BR>/g;
                  ($dbstate = $addrtab{$onekey}{'state'}) =~ s/\n/\n<BR>/g;
                  ($dbzipcode = $addrtab{$onekey}{'zipcode'}) =~ s/\n/\n<BR>/g;
                  ($dbcountry = $addrtab{$onekey}{'country'}) =~ s/\n/\n<BR>/g;
                  ($dbphone = $addrtab{$onekey}{'phone'}) =~ s/\n/\n<BR>/g;
                  ($dbpager = $addrtab{$onekey}{'pager'}) =~ s/\n/\n<BR>/g;
                  ($dbfax = $addrtab{$onekey}{'fax'}) =~ s/\n/\n<BR>/g;
                  ($dbcphone = $addrtab{$onekey}{'cphone'}) =~ s/\n/\n<BR>/g;
                  ($dbbphone = $addrtab{$onekey}{'bphone'}) =~ s/\n/\n<BR>/g;
                  ($dbemail = $addrtab{$onekey}{'email'}) =~ s/\n/\n<BR>/g;
                  ($dburl = $addrtab{$onekey}{'url'}) =~ s/\n/\n<BR>/g;
               }
            }
            if ($nomatch eq "false") {
            if ($dbfname eq $fname) {
               $found_counter= $found_counter + 1;
               $page_entries = $page_entries + 1;
               if ($page_entries eq 1) {
                  $page_num = $page_num + 1;
               }
               #print "page_num = ", $page_num, "\n";
               if ($page_num eq 1) {
                  $prevpage = "$ENV{HDREP}/$login/searchpage$page_num.html";
               } else {
                  $pageno = $page_num - 1;
                  $prevpage = "$ENV{HDREP}rep/$login/searchpage$pageno.html";
               }
               $pageno = $page_num + 1;
               if ($page_num eq 1) {
                  $nextpage = "$ENV{HDREP}rep/$login/searchpage$pageno.html";
               } else {
                  $nextpage = "$ENV{HDREP}rep/$login/searchpage$pageno.html";
	       }
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

               #($outfield = $addrtab{$onekey}{'pager'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "pager=$dbpager";
               $prml = strapp $prml, "pagefield=page$dbentryno";
               #print "Pager = ", $outfield, "\n";
	       $pageurl = adjusturl("cgi-bin/execsendpage.cgi?thispage=http://www.portalserver.net/rep/$login/searchpage$page_num.html&to=$dbpager&biscuit=$biscuit");
	       $prml = strapp $prml, "pageurl=$pageurl"; 

               #($outfield = $addrtab{$onekey}{'fax'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "fax=$dbfax";
               $prml = strapp $prml, "fafield=fa$dbentryno";
               #print "Fax = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'cphone'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "cphone=$dbcphone";
               $prml = strapp $prml, "cphonfield=cphon$dbentryno";
               #print "Fax = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'bphone'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "bphone=$dbbphone";
               $prml = strapp $prml, "bphonfield=bphon$dbentryno";
               #print "BusinessPhone = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'email'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "email=$dbemail";
               $prml = strapp $prml, "emaifield=emai$dbentryno";
               #print "Email = ", $outfield, "\n";

               #($outfield = $addrtab{$onekey}{'url'}) =~ s/\n/\n<BR>/g;
               $prml = strapp $prml, "url=$dburl";
               $prml = strapp $prml, "urfield=ur$dbentryno";
               #print "URL = ", $outfield, "\n";

	       $jumpurl = $dburl;  
	       $prml = strapp $prml, "jumpurl=$jumpurl"; 
               $prml = strapp $prml, "template=../templates/searchaddrtblentry.html";
               $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/searchaddrtblentry.html";
               parseIt $prml;
               $prml = "";

               if ($page_entries eq 1) {
                  #if ($page_num eq 1 ) {
                     #system "/bin/cat ../templates/content.html > ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
                  #}
                 # Generate Search Page Header
                  $prml = "";
                  
                  $prml = strapp $prml, "biscuit=$biscuit";
                  $expiry = localtime(time() + 300);
                  $expiry = "\:$expiry";
                  $prml = strapp $prml, "template=../templates/searchpghdr.html";
                  $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/searchpghdr.html"; 
                  $prml = strapp $prml, "expiry=$expiry";
                  $prml = strapp $prml, "pager=$dbpager";
                  $prml = strapp $prml, "pagefield=page$dbentryno";

		  #$pageurl = "../$ENV{HDREP}rep/$login/sendpage.html?thispage=<searchpage$page_num.html>&to=<$pagefield>";
		  #$pageurl = "../$ENV{HDREP}rep/$login/sendpage.html";
	          #$prml = strapp $prml, "pageurl=testpageurl"; 

                  $urlcgi = buildurl("execaddrupddel.cgi");
                  $prml = strapp $prml, "actioncgi=$urlcgi";
                  $prml = strapp $prml, "label=HotDiary Search results for $fname";
                  parseIt $prml;
                  $prml = "";
                  #if ($page_num eq 1) {
                    #system "/bin/cat ../$ENV{HDREP}rep/$login/searchpghdr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
                  #} else {
                    system "/bin/cat ../$ENV{HDREP}rep/$login/searchpghdr.html > ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
                  #}


                  # Generate Standard Table Header
                  $prml = strapp $prml, "template=../templates/stdtblhdr.html"; 
                  $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/stdtblhdr.html";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat ../$ENV{HDREP}rep/$login/stdtblhdr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
               }

               system "/bin/cat ../$ENV{HDREP}rep/$login/searchaddrtblentry.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";

               if ($page_entries eq 2) {
# this is the last time we will use page_entries in this iteration, 
# so we can reset it now to 0
                  # Generate Standard Table Footer
                  $prml = strapp $prml, "numentries=$page_entries";
                  $prml = strapp $prml, "template=../templates/stdtblftr.html";
                  $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/stdtblftr.html";
                  $prml = strapp $prml, "nextpage=$nextpage";
                  $prml = strapp $prml, "prevpage=$prevpage";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat ../$ENV{HDREP}rep/$login/stdtblftr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";

                  # Generate Search Page Footer
                  $prml = strapp $prml, "template=../templates/searchpgftr.html";
                  $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/searchpgftr.html";
                  parseIt $prml;
                  $prml = "";
                  system "/bin/cat ../$ENV{HDREP}rep/$login/searchpgftr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
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
         $prml = strapp $prml, "template=../templates/stdtblftr.html";
         $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/stdtblftr.html";
         $prml = strapp $prml, "nextpage=$nextpage";
         $prml = strapp $prml, "prevpage=$prevpage";
         parseIt $prml;
         $prml = "";
         system "/bin/cat ../$ENV{HDREP}rep/$login/stdtblftr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";

         # Generate Search Page Footer
         $prml = strapp $prml, "template=../templates/searchpgftr.html";
         $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/searchpgftr.html";
         parseIt $prml;
         $prml = "";
         system "/bin/cat ../$ENV{HDREP}rep/$login/searchpgftr.html >> ../$ENV{HDREP}rep/$login/searchpage$page_num.html";
      }


# overwrite nextpage with lastpage
      $prml = strapp $prml, "template=../templates/lastpage.html";
      $prml = strapp $prml, 
      			"prevpage=$ENV{HDREP}rep/$login/searchpage$page_num.html";
      $pageno = $page_num + 1; 
      $prml = strapp $prml, "templateout=../$ENV{HDREP}rep/$login/searchpage$pageno.html";
      parseIt $prml;
      $prml = "";

      if ($found_counter eq 0) {
          status("$fname not found in addresses.\n");
      }
      else {
            system "/bin/cat ../templates/content.html\n\n"; 
            system "/bin/cat ../$ENV{HDREP}rep/$login/searchpage1.html"; 
        }
    }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time(); 

# save the info in db
   tied(%addrtab)->sync();
   #tied(%addrnotab)->sync();
   tied(%sesstab)->sync(); 
   tied(%logsess)->sync(); 
}

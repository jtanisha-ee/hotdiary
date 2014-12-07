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
# FileName: searchbuddies.cgi
# Purpose: it searches buddies info. in hotdiary.
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
$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
# parse the command line
   &ReadParse(*input); 

   #print &PrintHeader;
   #print &HtmlTop ("addraddsearch.cgi example");

     

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

  if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
    delete $sesstab{$biscuit};
    delete $logsess{$login};
    status("$login: Your session has already expired.\n");
    #return;
    exit;
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   if ($input{"Submit"} eq "Search") {
   #   status("Search Buddies service is coming soon!.");
      $action = "Search";
   #   exit;
   }

   $title = time();

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   if ($action eq "Search") {
      system "/bin/rm -f $ENV{HDREP}/$alphaindex/$login/bser*.html";
      $found_counter = 0;
      $page_entries = 0;
      $page_num = 0;
      $prevpage = "";
      $nextpage = "";

      $search = trim $input{'search'};
      if ($search eq "") {
         status("Please enter name to Search. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         exit;
      }

      ($firstname, $lastname) = split(" ", $search);
      $firstname = trim $firstname;
      $lastname = trim $lastname;

      if (($firstname eq "") && ($lastname eq "")) {
         status("Please enter \"firstname, lastname\" in search criteria. Click <a href=\"validation.html\"> here</a> to learn validation rules.");
         exit;
      }

      $tooshort = "";
      if (((length $firstname) <= 3) && ((length $lastname) <= 3)) {
         $msg .= "The specified search names are too short. A lot of matches were found. HotDiary will not display members, for protecting user and system security. Will perform an exact name match search to shorten output.<BR><BR>";
         $tooshort = "true";
      }

      foreach $account (sort keys %logtab) {
         $checkid = $logtab{$account}{'checkid'};
         if ($checkid eq "CHECKED") {
            if ((($tooshort eq "") && (nmmatch $logtab{$account}{'fname'}, $firstname) && (nmmatch $logtab{$account}{'lname'}, $lastname)) || 
               (($tooshort eq "true") && (("\U$logtab{$account}{'fname'}" eq "\U$firstname") || ("\U($logtab{$account}{'lname'}" eq "\U$lastname")))) {

               $found_counter= $found_counter + 1;
               $page_entries = $page_entries + 1;

               $log_fname = $logtab{$account}{'fname'};
               $log_lname = $logtab{$account}{'lname'};
               $log_account = $account;

               if ($page_entries eq 1) {
                  $page_num = $page_num + 1;
               }

               if ($page_num eq 1) {
                  $prevpage = "rep/$alphaindex/$login/bser$title$biscuit$page_num.html";
               } else {
                  $pageno = $page_num - 1;
                  $prevpage = "rep/$alphaindex/$login/bser$title$biscuit$pageno.html";
               }

               $pageno = $page_num + 1;
               if ($page_num eq 1) {
                  $nextpage = "rep/$alphaindex/$login/bser$title$biscuit$pageno.html";
               } else {
                  $nextpage = "rep/$alphaindex/$login/bser$title$biscuit$pageno.html";
               }


               $prml = "";
               $prml = strapp $prml, "entrynfield=entryn$page_entries";
               $prml = strapp $prml, "entryno=$account";

               $prml = strapp $prml, "checkboxfield=checkbox$account";

               $prml = strapp $prml, "fname=$log_fname";
               $prml = strapp $prml, "fnamfield=fnam$page_entries";

               $prml = strapp $prml, "lname=$log_lname";
               $prml = strapp $prml, "lnamfield=lnam$page_entries";

               $prml = strapp $prml, "logaccount=$log_account";
               $prml = strapp $prml, "logaccounfield=logaccoun$account";

          
               $prml = strapp $prml, "template=$ENV{HDTMPL}/searchbuddytblentry.html";
               $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/searchbuddytblentry.html";

               parseIt $prml, 1;
               $prml = "";

               if ($page_entries eq 1) {
                 # Generate Search Page Header
                  $prml = "";

                  $prml = strapp $prml, "biscuit=$biscuit";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/searchpghdr.html";

                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/searchpghdr.html";
                  $prml = strapp $prml, "pagenumber=Page: $page_num <BR>";
                  $prml = strapp $prml, "expiry=";
                  $prml = strapp $prml, "pagefield=page$dbentryno";

                  $urlcgi = buildurl("execaddbuddies.cgi");
                  $prml = strapp $prml, "actioncgi=$urlcgi";

                  $prml = strapp $prml, "label= Search results for \"$log_fname, $log_lname \"";
                  #}

                  parseIt $prml, 1;
                  $prml = "";

                  system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/searchpghdr.html > $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
                  # Generate Standard Table Header
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblhdr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdtblhdr.html";
                  parseIt $prml, 1;
                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdtblhdr.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
               }
               #print "Just before appending<BR>";
               system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/searchbuddytblentry.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";

               if ($page_entries eq 10) {
# this is the last time we will use page_entries in this iteration,
# so we can reset it now to 0
               #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/searchbuddytblentry.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
                  # Generate Standard Table Footer
                  $prml = strapp $prml, "numentries=$page_entries";
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdtblftr.html";
                  $prml = strapp $prml, "nextpage=$nextpage";
                  $prml = strapp $prml, "prevpage=$prevpage";
                  parseIt $prml, 1;

                  $prml = "";
                  system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdtblftr.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";

                  # Generate Search Page Footer
                  $prml = strapp $prml, "template=$ENV{HDTMPL}/buddysearchpgftr.html";
                  $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/buddysearchpgftr.html";

                  parseIt $prml, 1;
                  $prml = "";

                  system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/buddysearchpgftr.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
               }

               if ($page_entries eq 10) {
                  $page_entries = 0;
               }
            }
         } 
      }

# deal with cases when the $found_counter are odd numbered
      $rem = $found_counter % 10;
      if ($rem != 0) {
      #system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/searchbuddytblentry.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
         # Generate Standard Table Footer
         $prml = strapp $prml, "numentries=$page_entries";
         $prml = strapp $prml, "template=$ENV{HDTMPL}/stdtblftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/stdtblftr.html";
         $prml = strapp $prml, "nextpage=$nextpage";
         $prml = strapp $prml, "prevpage=$prevpage";
         parseIt $prml, 1;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/stdtblftr.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";

         # Generate Search Page Footer
         $prml = strapp $prml, "template=$ENV{HDTMPL}/buddysearchpgftr.html";
         $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/buddysearchpgftr.html";

         parseIt $prml, 1;
         $prml = "";
         system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/buddysearchpgftr.html >> $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
      }


# overwrite nextpage with lastpage
      $prml = strapp $prml, "expiry=";
      $prml = strapp $prml, "template=$ENV{HDTMPL}/lastpage.html";
      $prml = strapp $prml, "prevpage=rep/$alphaindex/$login/bser$title$biscuit$page_num.html";

      $pageno = $page_num + 1;
      $prml = strapp $prml, "templateout=$ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$pageno.html";
      parseIt $prml, 1;
      $prml = "";
      system "cp $ENV{HDREP}/$alphaindex/$login/$biscuit.html $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$pageno.html";

      if ($found_counter eq 0) {
          #if ($login eq "user1000") {
             $label = "Invite Someone to HotDiary";
             $label1 = "Choose a login and enter invitee's email address.";
             $prml = "";
             $prml = strapp $prml, "login=$login";
             $prml = strapp $prml, "label1=$label1";
             $prml = strapp $prml, "label=$label";
             $prml = strapp $prml, "biscuit=$biscuit";
             $mname = $logtab{$login}{'login'};
             $prml = strapp $prml, "mname=$mname";
             $prml = strapp $prml, "template=$ENV{HDTMPL}/invitefriend.html";
             $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/invitefriend.html";
             parseIt $prml, 1;
             system "/bin/cat $ENV{HDHREP}/$alphaindex/$login/invitefriend.html > $ENV{HDREP}/$alphaindex/$login/invitefriend$biscuit.html";
             $emsg = "<p>Click <a href=\"rep/$alphaindex/$login/invitefriend$biscuit.html\">here to invite $firstname $lastname to HotDiary</a>.";
          #}
          status("$login: $msg Could not find a match for $firstname, $lastname. $emsg");
      } else {
            system "/bin/cat $ENV{HDTMPL}/content.html\n\n";
            $page_num = "1";
            system "/bin/cat $ENV{HDREP}/$alphaindex/$login/bser$title$biscuit$page_num.html";
      }
   }

# reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

}

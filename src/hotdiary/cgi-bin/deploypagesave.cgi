#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: deploypage.cgi
# Purpose: Deploy Page From Template System With Embedded Session Management
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              #status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      #exit;
	    } 
	 }
         #status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         #status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      #exit;
   }

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
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   hddebug "hs = $hs";
   # check if session record exists.
   
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               #status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               #exit;
	    } 
         }
         #status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         #status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      #exit;
   } else {
      $login = $sesstab{$biscuit}{'login'};
      if ($login eq "") {
         #error("Login is an empty string. Possibly invalid session.\n");
         #exit;
      }
   }

   if (exists($sesstab{$biscuit})) {
   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               #status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       #exit;
            }
         } 
         #status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         #status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      #exit;
   }
   }

   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

# bind login table vars
   tie %pagetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/pagetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['page' ] };

   $page = $input{page};
   hddebug "page = $page";
   if (!exists $pagetab{$page}) {
      status("$login: Security violation. The page you have requested ($page) has been blocked. This message has been sent to hotdiary.com");
      exit;
   }

   if (($page eq "jwhatsnew.html") || ($page eq "jfeatures.html")) {
      if ($login eq "") {
	 status("Cannot access this document from published or community events calendar.");
	 exit;
      }
   }

   if (($page eq "jintranetfeatures.html") || ($page eq "jintranetwhatsnew.html")) {
      tie %businesstab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/businesstab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };

      if ($os ne "nt") {
	 $execbusiness = encurl "execbusiness.cgi";
	 $execsetupdowntown = encurl "execsetupdowntown.cgi";
	 $execdowntownmem = encurl "execdowntownmem.cgi";
      } else {
	 $execbusiness = "execbusiness.cgi";
	 $execsetupdowntown = "execsetupdowntown.cgi";
	 $execdowntownmem = "execdowntownmem.cgi";
      }
  
      foreach $business_idx (sort keys %businesstab) {
        tie %peopletab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business_idx/peopletab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['login', 'business']};

        if (($businesstab{$business_idx}{businessmaster} eq $login) ||
          (exists($peopletab{$login})) ){
          ###
          ### There have to be atleast 10 mem in the business to go for manage
          ###
          (@hshnumpeople) = sort keys %peopletab;
	  if ( ($login ne "smitha") || ($login ne "mjoshi")) {
             tie %downtowntab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/aux/downtowntab",
             SUFIX => '.rec',
             SCHEMA => {
                ORDER => ['login', 'fname', 'lname', 'company',
                    'street', 'city', 'state', 'zipcode',
                    'country', 'email', 'prodtype', 'amount', 'invoicenum',
                    'business'] };           
	      if (!exists($downtowntab{$login})) {
	         if (-d "$ENV{HDDATA}/aux/business/$business_idx/headtab") {
                    tie %headtab, 'AsciiDB::TagFile',
                    DIRECTORY => "$ENV{HDDATA}/aux/business/$business_idx/headtab",
                    SUFIX => '.rec',
                    SCHEMA => {
                    ORDER => ['login', 'business', 'datejoined', 'clearance']};
 
  	            if (!exists ($headtab{$login} ) ) {
                       status("$login: Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execdowntownmem&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&re4=os&le4=os&enum=5\">here</a> to add your membership to $business_idx.");
		       exit;
		    } else {
		       ## if it exists but the membership is not yet cleared.
		       if ($headtab{$login}{clearance} ne "true") {
                          status("$login: Your membership in $business_idx is not yet effective. It may take approximately 72 hours to process your request to. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&re4=os&le4=os&enum=5\">here</a> to return to business home.");
			  exit;
		       }
		    }
	         } else {
                    status("$login: Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execsetupdowntown&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&re4=os&le4=os&enum=5\">here</a> to setup My Downtown - B2B Planner to access the features and services of business.");
	            exit;
		 }
	      }
           } 
        }
     }
   }

 
   $rh = $input{rh};
   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }


   if ($logo ne "") {
         $logo = adjusturl $logo;
   }


   $prml = "";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "label=$label";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
   }

   $prml = strapp $prml, "template=$ENV{HDTMPL}/$page";
   if ($login eq "") {
      $prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/$$-$page";
   } else {
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/$$-$page";
   }
 
   $prml = strapp $prml, "biscuit=$biscuit";
   $welcome = "Welcome";
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "biscuit=$biscuit";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execaddpersonalcontact=$execaddpersonalcontact";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
   $prml = strapp $prml, "jp=$jp";

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   if ($login eq "") {
      #system "cat $ENV{HDHOME}/tmp/$$-$page";
      hdsystemcat "$ENV{HDHOME}/tmp/$$-$page";
   } else {
      #system "cat $ENV{HDHREP}/$alpha/$login/$$-$page";
      hdsystemcat "$ENV{HDHREP}/$alpha/$login/$$-$page";
   }

   if (exists($sesstab{$biscuit})) {
     # reset the timer.
     $sesstab{$biscuit}{'time'} = time();
     tied(%sesstab)->sync();
   }

   tied(%logsess)->sync();

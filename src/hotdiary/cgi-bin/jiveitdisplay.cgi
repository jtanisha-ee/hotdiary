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
# FileName: jiveitadmin.cgi
# Purpose: it admin users for jiveit.
# Creation Date: 08-14-99
# Created by: Smitha Gudur
#


require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;

MAIN:
{


# parse the command line
   &ReadParse(*input);

   $adminp = trim $input{'password'};
   $login = trim $input{'jp'};
   $login = "\L$login";
   $adminp = "\L$adminp";

   if (notLogin($login)) { 
      status("Invalid characters in login ($login). Make sure there are no spaces in the login name.");
     exit;                                    
   }

   if ($login eq "") {
      status("Your login is empty");
      exit;
   }
         
   # bind jivetab table vars

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };         

   if (!exists($logtab{$login})) { 
      status("Your login=$login is invalid. Please register before you can use JiveIt!"); 
       exit; 
   }

   ## we need to check the password if it is not coming from jiveitupload.
   $file = $input{file};
   #if (file eq "") {
      if ($adminp ne $logtab{$login}{'password'}) {
         status("Please enter the correct password. Your password ($adminp) is invalid");
         exit; 
      } 
   #}
   
   # bind jivetab table vars
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account', 
	     'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright'] };

   $alp = substr $login, 0, 1;
   $alp = $alp . '-index';

   $pr = "";    
   $url=$jivetab{$login}{'url'};
   $url= adjusturl($url);
   $pr = strapp $pr, "url=$url";
   $logo= adjusturl "$jivetab{$login}{'logo'}";
   $pr = strapp $pr, "logo=$logo";
   $title= adjusturl "$jivetab{$login}{'title'}";
   $pr = strapp $pr, "title=$title";
   $pr = strapp $pr, "login=$login";
   $pr = strapp $pr, "welcome=Welcome";

   $banner= $jivetab{$login}{'banner'};
   $banner= adjusturl ($banner);
   $banner =~ s/\"/\&quot;/g;
   hddebug "banner = $banner";
   $pr = strapp $pr, "banner=$banner";
   #$bannertxt = "$banner";
   $pr = strapp $pr, "bannertxt=$banner"; 

   
   $topleft= adjusturl $jivetab{$login}{'topleft'};
   $pr = strapp $pr, "topleft=$topleft"; 

   $topright= adjusturl $jivetab{$login}{'topright'};
   $pr = strapp $pr, "topright=$topright"; 

   $middleright= adjusturl $jivetab{$login}{'middleright'};
   $pr = strapp $pr, "middleright=$middleright"; 

   $bottomleft= adjusturl $jivetab{$login}{'bottomleft'};
   $pr = strapp $pr, "bottomleft=$bottomleft"; 

   $bottomright= adjusturl $jivetab{$login}{'bottomright'};
   $pr = strapp $pr, "bottomright=$bottomright"; 

   $account=$jivetab{$login}{'account'};
   if ($account ne "") {
      $damount = $account / 100;
      $str = 'US $' . "$damount";
   }
   
   $pr = strapp $pr, "account=$str";
   $pr = strapp $pr, "regusers=$jivetab{$login}{'regusers'}";
   $pr = strapp $pr, "jp=$login";
   $jiveitlogo = adjusturl $jivetab{$login}{'logo'};
   $pr = strapp $pr, "jiveitlogo=$jiveitlogo";
   $pr = strapp $pr, "jiveittitle=$jivetab{$login}{'title'}";
   $banner = $jivetab{$login}{'banner'};
   $banner =~ s/\n/<BR>/g;
   $pr = strapp $pr, "jiveitbanner=$banner";  

   $vdomain = $input{vdomain};
   $os = $input{os};
   $HDLIC = $input{HDLIC};
   $rh = $input{rh};
  
      if ($os ne "nt") {
	 $execjiveitfile = encurl "execjiveitfile.cgi";
	 $execdownloadmytemplates = encurl "execdownloadmytemplates.cgi";
      } else {
	 $execjiveitfile = "execjiveitfile.cgi";
	 $execdownloadmytemplates = "execdownloadmytemplates.cgi";
      }

      $upload = adjusturl "<a href=\"http://www.hotdiary.com/cgi-bin/execdogeneric.cgi?p0=$execjiveitfile&p1=login&p2=password&pnum=3&login=$login&password=$adminp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&le3=HDLIC&HDLIC=$HDLIC&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\">Upload My Templates</a>";
      $pr = strapp $pr, "upload=$upload";  

   #if (($login eq "user8000") || ($login eq "smitha") || 
   #    ($login eq "mjoshi")) {
      $downloadmytmp = adjusturl "<a href=\"http://www.hotdiary.com/cgi-bin/execdogeneric.cgi?p0=$execdownloadmytemplates&p1=login&pnum=2&login=$login&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&pnum=4&le3=HDLIC&HDLIC=$HDLIC&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&enum=5\" target=_main>Download My Templates</a>";

      $members = adjusturl "<a href=\"http://www.hotdiary.com/jsp/execjivemembers.jsp?jp=$login&password=$adminp\" target=_main>My Members (Summary Report)</a>";
      $membersdetail = adjusturl "<a href=\"http://www.hotdiary.com/jsp/execjivemembers.jsp?jp=$login&password=$adminp&report=detail\" target=_main>My Members (Detail Report)</a>";
   #}

   $download = "";
   if ($login ne "bradn1") {
     $download = adjusturl "<a href=\"http://www.hotdiary.com/downloadtemplates.html\" target=_main>Download HotDiary Templates</a>";
   }

   $jp = $login;
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';

   if ($jp ne "") {
      if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitaccount.html") {
         $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/jiveitaccount.html";
      } else {
         $tmpl = "$ENV{HDTMPL}/jiveitaccount.html";
      }
   } else {
      $tmpl = "$ENV{HDTMPL}/jiveitaccount.html";
   }

   $pr = strapp $pr, "downloadmytmp=$downloadmytmp";  
   $pr = strapp $pr, "download=$download";  
   $pr = strapp $pr, "members=$members";  
   $pr = strapp $pr, "membersdetail=$membersdetail";  
   #$pr = strapp $pr, "template=$ENV{HDTMPL}/jiveitaccount.html";  
   $pr = strapp $pr, "template=$tmpl";
   $pr = strapp $pr, "templateout=$ENV{HDREP}/$alp/$login/jiveitaccount-$$.html"; 

   parseIt $pr; 
   #system "cat \"$ENV{HDTMPL}/content.html\"";   
   #system "cat \"$ENV{HDREP}/$alp/$login/jiveitaccount.html\""; 
   hdsystemcat "$ENV{HDREP}/$alp/$login/jiveitaccount-$$.html"; 
}

                                   
                         

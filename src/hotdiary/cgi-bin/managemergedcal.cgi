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
# FileName: managemergedcal.cgi
# Purpose: New HotDiary Group Calendar Client
# Creation Date: 06-14-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
#use calfuncs::calfuncs;   
use calfuncs::businesscalfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug "managemergedcal.cgi";

   $hdcookie = $ENV{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   $jp = $input{jp}; 
   $alphjp = substr $jp, 0, 1;
   $alphjp = $alphjp . '-index';
   hddebug "jp = $jp";
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account'] };
                                                                              
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
              status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
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

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
               exit;
	    } 
         }
         status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
      } else {
         status("This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. This could be either an older session or you are viewing a published (read-only) page. <p>If this is an older session, please relogin. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.<p>If this is a published (read-only) page, click <a href=\"http://$vdomain\">here.</a>");
            exit;
         }
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   
   $rh = $input{'rh'};
   tie %hdtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/hdtab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['title', 'logo' ] };
   if (exists $hdtab{$login}) {
      $label = adjusturl $hdtab{$login}{title};
   } else {
      $label = "HotDiary";
   }

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };


   if (exists $hdtab{$login}) {
      $label = adjusturl($hdtab{$login}{title});
   } else {
      $label = "HotDiary";
   }
                           

   tie %parttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/partners/parttab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['logo', 'title', 'banner'] };

   $HDLIC = $input{HDLIC};
   hddebug "HDLIC = $HDLIC";

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

   if ($os ne "nt") {
      $execmygroups = encurl "execmygroups.cgi";
      $execmergedgroups = encurl "execmergedgroups.cgi";
      $execmergedsearchcal = encurl "execmergedsearchcal.cgi";
      $execcreatemergedcal = encurl "execcreatemergedcal.cgi";
      $execmanagemergedcal = encurl "execmanagemergedcal.cgi";
   } else {
      $execmygroups = "execmygroups.cgi";
      $execmergedgroups = "execmergedgroups.cgi";
      $execmergedsearchcal = "execmergedsearchcal.cgi";
      $execcreatemergedcal = "execcreatemergedcal.cgi";
      $execmanagemergedcal = "execmanagemergedcal.cgi";
   }


   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';


   if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab";
   }
   # bind subscribed group table vars
   tie %sgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/subscribed/sgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   # bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
            'groupdesc' , 'password', 'ctype', 'cpublish', 'corg',
            'listed', 'readonly', 'groups', 'logins'] };           

   $g = trim $input{grouplist};
   $createcal = adjusturl "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&f=cpc&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6\">here</a> to create merged calendar.";     

   $mcalmsg = adjusturl "<p>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&f=mc&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6\">here</a> to manage merged calendar."; 

   if ($g eq "") {
      status("$login: You have not selected any merged calendar to manage or delete. $createcal $mcalmsg");
      exit;
   }

   $delete = $input{delete};
   
   # bind founded group table vars
   tie %fmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/merged/$login/founded/fmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   if ($delete ne "") {
      if (exists $fmergetab{$g}) {
         if ("\L$fmergetab{$g}{'groupfounder'}" eq "\L$login") {
            delete $fmergetab{$g};
            tied(%fmergetab)->sync();

	    tie %usertab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/listed/merged/$g/usertab",
            SUFIX => '.rec',
            SCHEMA => {
               ORDER => ['login'] };
	    (@hshuserdir) = (sort keys %usertab);
	    foreach $user (@hshuserdir) {
		if (-d "$ENV{HDDATA}/merged/$user/subscribed/smergetab") {
		   # bind subscribed group table vars
                   tie %smergetab, 'AsciiDB::TagFile',
                   DIRECTORY => "$ENV{HDDATA}/merged/$user/subscribed/smergetab",
                   SUFIX => '.rec',
                   SCHEMA => {
                        ORDER => ['groupname', 'groupfounder', 'grouptype', 
			'grouptitle', 'groupdesc', 'password', 'ctype', 
			'cpublish', 'corg' ] };
	           if (exists($smergetab{$g})) {
                      delete $smergetab{$g};
                      tied(%smergetab)->sync();
		   }
	        }
            }
            if ($g ne "") {
               if (-d "$ENV{HTTPHOME}/html/hd/merged/$g") {
                   system "rm -f  $ENV{HTTPHOME}/html/hd/merged/$g/index.cgi";
                   system "rm -f  $ENV{HTTPHOME}/html/hd/merged/$g/mergedwebpage.cgi";
                   system "rmdir $ENV{HTTPHOME}/html/hd/merged/$g";
               }
            }

# safety check!! just in case any other directory is deleted
            if (-d "$ENV{HDDATA}/listed/merged/$g") {
               $g = trim $g;
               if (($g ne "") && ($ENV{HDDATA} ne "")) {
                  system "/bin/rm -rf $ENV{HDDATA}/listed/merged/$g";
               }
            }
            if (exists($lmergetab{$g})) {
               delete($lmergetab{$g});
               tied(%lmergetab)->sync();
            }
	    $msg = "Merged calendar $g has been removed. <BR>All the resources allocated for $g have been removed. <p>$createcal";
	 } else {
           status("$login: The calendar master for $calname does not match your member login $login. $mcalmsg");
	    exit;
         } 
      } else {
	 $msg = "You cannot delete merged calendar <B>$g</B>, since you are not its' founder."; 
      }
      status("$login: $msg $mcalmsg");
      exit;
   }

   if (!exists ($lmergetab{$g})) {
      status("$login: $g merged calendar does not exist. $createcal $mcalmsg");
      exit;
   }

   $mygroups = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execmygroups&p1=biscuit&p2=jp&pnum=3&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";
   
   $mergedgroups = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";

   if (!(-d "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab")) {
      system "mkdir -p $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
      system "chmod 755 $ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab";
   }
   # bind founded group table vars
   tie %fgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/groups/$alphaindex/$login/founded/fgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 
                 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };

   $memotype = "";
   $cntr = 0;
   (@glist) = keys %fgrouptab;
   (@glist1) = keys %sgrouptab;
   if ( ($#glist < 0) && ($#glist1 < 0) ) {
      $grouplabel = adjusturl "<FONT FACE=Verdana SIZE=1>Groups Not Created Or Subscribed</FONT>";
   } else {
      $grouplabel = adjusturl "<B>Groups Created or Subscribed</B><BR>";
      foreach $grp (keys %fgrouptab) {
	 $cntr = $cntr + 1;
         $memotype .= "<OPTION>$grp";
      }
      foreach $grp (keys %sgrouptab) {
	 $cntr = $cntr + 1;
         $memotype .= "<OPTION>$grp";
      }
      $memotype = adjusturl $memotype;
   }

   if ($cntr == 0) {
       $status = "You have not created any merged calendars or subscribed to any merged calendars.";  
   }

   $inclist = "";
   $loginlist = adjusturl getmembers($login);
   $groups = adjusturl $lmergetab{$g}{groups};

   $calname = adjusturl $lmergetab{$g}{groupname};

   (@hshcdir) = split(" ", $groups);

   if ($groups ne "") {
      $inclist .= "<TR><TD COLSPAN=2><FONT FACE=Verdana SIZE=2><B>Groups included in merged calendar</B></FONT></TD></TR>"; 
   }

   foreach $grpname (@hshcdir) {
      #hddebug "grpname = $grpname";
      $cdir .= "$grpname ";
      $inclist .= "<TR><TD>&nbsp;</TD><TD><FONT FACE=Verdana SIZE=2><INPUT TYPE=CHECKBOX NAME=$grpname CHECKED>$grpname</FONT></TD></TR>"; 
   }
   $inclist = adjusturl $inclist;
   (@hshcdir) = split(" ", $cdir);
   
   $hiddenvars = "";
   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execcreatemergedcal>"; 
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=userlogins>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=listed>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=grouplist>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr5 VALUE=multsel>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=loginlist>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pattr6 VALUE=multsel>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=cname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=corg>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=calname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=caltitle>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=calpassword>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=calrpassword>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=contact>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=cdesc>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=cpublish>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=f>"; 
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=numbegin>"; 
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=numend>"; 
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=edit>"; 

   #values of checkboxes as each parameter
   $k = 0;
   $mcntr = 20;
   $numend = $mcntr;
   $numbegin = $mcntr;

   # this tells from where the parameter for selection starts
   foreach $cn (@hshcdir) {
      $cn = trim $cn;
      $numend = $numend + 1;
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
      $mcntr = $mcntr + 1;
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
      $mcntr = $mcntr + 1;
      $k = $k + 1;
   }
   $numend = $numend - 1;            

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=edit VALUE=edit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=calname VALUE=$calname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars = gethiddenvars($hiddenvars);
   $hiddenvars = adjusturl $hiddenvars;

   $caltitle = adjusturl $lmergetab{$g}{groupname};
   $cpublish = adjusturl $lmergetab{$g}{cpublish};
   $calpassword = adjusturl $lmergetab{$g}{password};
   $contact = adjusturl $lmergetab{$g}{contact};
   $cdesc = adjusturl $lmergetab{$g}{groupdesc};
   $corg = adjusturl $lmergetab{$g}{corg};
   $userlogins = adjusturl $lmergetab{$g}{logins};
   $cname = adjusturl $lmergetab{$g}{groupfounder};
   $listed = adjusturl $lmergetab{$g}{listed};

   $userlogins = trim $userlogins;
   if ($cpublish eq "on") {
      $cpublish = "CHECKED";
      $website = "Merged Calendar Website: http://$vdomain/merged/$caltitle";
   }
   if ($listed eq "on") {
      $listed = "CHECKED";
   }


   $prs = "";
   $prs = strapp $prs, "hiddenvars=$hiddenvars";
   $prs = strapp $prs, "logo=$logo";
   $prs = strapp $prs, "caltitle=$caltitle";
   $prs = strapp $prs, "calrpassword=$calpassword";
   $prs = strapp $prs, "calpassword=$calpassword";
   $prs = strapp $prs, "contact=$contact";
   $prs = strapp $prs, "cpublish=$cpublish";
   $prs = strapp $prs, "cdesc=$cdesc";
   $prs = strapp $prs, "cname=$cname";
   $prs = strapp $prs, "calname=$calname";
   $prs = strapp $prs, "corg=$corg";
   $prs = strapp $prs, "userlogins=$userlogins";
   $prs = strapp $prs, "grouplist=$groups";
   $prs = strapp $prs, "label2=";
   $prs = strapp $prs, "listed=$listed";

   $cgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=$execmergedgroups&p1=biscuit&p2=jp&p3=f&pnum=4&biscuit=$biscuit&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6"; 

   if ($rh eq "") {
      $cgis = adjusturl "/cgi-bin/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execcalclient.cgi?biscuit=$biscuit&jp=$jp";
   }

   if ($jp ne "") {
      $prs = strapp $prs, "label2=Powered By HotDiary";
   }

  

   $prs = strapp $prs, "banner=$banner";
   $prs = strapp $prs, "label=$label";

   if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphjp/$jp/templates/hdmanagemergedcal.html") ) {
       $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/hdmanagemergedcal.html";
   } else {
       $tmpl = "$ENV{HDTMPL}/hdmanagemergedcal.html";
   }

   $prs = strapp $prs, "template=$tmpl";
   $mergetemp = "$ENV{HDHREP}/$alphaindex/$login/merge-$biscuit-$$.html";
   $prs = strapp $prs, "templateout=$mergetemp";
   $prs = strapp $prs, "biscuit=$biscuit";
   $searchcal = adjusturl "$cgi&f=sgc";
   $prs = strapp $prs, "searchcal=$searchcal";
   $managecal = adjusturl "$cgi&f=mc";
   $createcal = adjusturl "$cgi&f=cpc";
   $prs = strapp $prs, "createcal=$createcal";
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prs = strapp $prs, "formenc=$formenc";
   } else {
      $prs = strapp $prs, "formenc=";
   }
   $prs = strapp $prs, "managecal=$managecal";
   $prs = strapp $prs, "welcome=Welcome";
   $prs = strapp $prs, "percal=$cgis";
   $prs = strapp $prs, "vdomain=$vdomain";
   $prs = strapp $prs, "hs=$hs";
   $prs = strapp $prs, "login=$login";
   if (-f "$ENV{HDREP}/$alphaindex/$login/topcal.html") {
      $fref = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&le5=HTTP_COOKIE&re5=HTTP_COOKIE&enum=6";
   } else {
       $fref = adjusturl "$cgis&mo=$mo&dy=$dy&yr=$yr&vw=$vew&f=h&a=d";
   }
   $prs = strapp $prs, "home=$fref";
   $prs = strapp $prs, "homestr=Home";
   $prs = strapp $prs, "rh=$rh";
   $prs = strapp $prs, "jp=$jp";

   if ( ("1800calendar.com" eq "\L$vdomain") ||  ("www.1800calendar.com" eq "\L$vdomain") || (validvdomain($vdomain) eq "1" ) ) {
     $prs = strapp $prs, "mygroups=$mygroups";
     $prs = strapp $prs, "mygrouptxt=My Groups";
   } else {
     $prs = strapp $prs, "mygroups=";
     $prs = strapp $prs, "mygrouptxt=";
   }

   $prs = strapp $prs, "mergedgroups=";
   $prs = strapp $prs, "mergedgroupstxt=";
   $prs = strapp $prs, "grouplabel=$grouplabel";
   $prs = strapp $prs, "grouplist=$memotype";
   $prs = strapp $prs, "loginlist=$loginlist";
   $prs = strapp $prs, "inclist=$inclist";
   $prs = strapp $prs, "status=$status";
   $prs = strapp $prs, "website=$website";
   parseIt $prs;

   #system "cat \"$ENV{HDTMPL}/content.html\"";
   #system "/bin/cat $mergetemp";
   hdsystemcat "$mergetemp";
  

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

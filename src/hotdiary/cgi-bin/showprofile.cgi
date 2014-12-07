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
# FileName: showprofile.cgi
# Purpose: it adds and displays appropriate user profile. 
# Creation Date: 9-09-99
# Created by: Smitha Gudur


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
#$login  = $input{login};
$SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

$biscuit = $input{biscuit};
$vdomain = trim $input{vdomain};

hddebug "showprofile.cgi()";

#hddebug "rh = $input{rh}";
#hddebug "hs = $input{hs}";
#hddebug "vdomain = $input{vdomain}";
#hddebug "fcomp = $fcomp";

$hdcookie = $input{HTTP_COOKIE};
$login = getlogin($hdcookie);



# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

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

if (! -d "$ENV{HDDATA}/surveytab") {
   system "mkdir $ENV{HDDATA}/surveytab";
   system "chmod 755 $ENV{HDDATA}/surveytab";
}

# bind surveytab table vars
  tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
		'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority', 
		'editcal', 'calpeople'] };  

   #biscuit=93703459617477-smitha-209.133.53.216
   if (exists $sesstab{$biscuit}) {
   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      if (exists $sesstab{$biscuit}) {
         delete $sesstab{$biscuit};
      }
      if (exists $logsess{$login}) {
         delete $logsess{$login};
       }
      status("You have been logged out automatically. Please relogin. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.\n");

      exit;
   } else {
      $sesstab{$biscuit}{'time'} = time();
   }
   } else {
      status "You have been logged out. Please relogin. Click <a href=\"index.html\" TARGET=\"_parent\"> here</a> to login.";
      exit;
   }

   if ($login eq "") {
      $login = $sesstab{$biscuit}{'login'};
   }
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }

   $hs = $input{'hs'};
   $os = $input{'os'};
   $jp = $input{'jp'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   if ($login eq "") {
      if ($hs eq "") {
         if ($jp ne "") {
           if ($jp ne "buddie") {
              status("Please enter a non-empty login string. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.");
           }
         }
       }
   }


#
# new changes here 
#
   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };

   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };

    tie %parttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/partners/parttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['logo', 'title', 'banner'] };

    $HDLIC = $input{HDLIC};

    $logo = "";

    hddebug "jp = $jp, vdomain =$vdomain";

    if (exists $jivetab{$jp}) {
       $logo = $jivetab{$jp}{logo};
       $label = $jivetab{$jp}{title};
       $label = adjusturl $label;
    } else {
       if (exists $lictab{$HDLIC}) {
          hddebug "came here";
          $partner = $lictab{$HDLIC}{partner};
          if (exists $parttab{$partner}) {
             $logo = $parttab{$partner}{logo};
             $label = $parttab{$partner}{title};
             $label = adjusturl $label;
           }
       }
    }

    if ( validvdomain($vdomain) eq "1" ) {
       $logo = "";
       $label = "";
    }

    if ($logo ne "") {
       $logo = adjusturl "$logo";
    } 
    $sc = $input{sc};
    if ($sc eq "p") {
       $welcome = "Calendar Of";
    } else {
       $welcome = "Welcome";
    }
#
# new changes end
#
   if (!exists $logtab{$login}) {
      status("$login: Profile does not exist.\n");
      exit;
   } else {
     $alphaindex = substr $login, 0, 1;
     $alphaindex = $alphaindex . '-index';

      $prml = 0;
      $prml = strapp $prml, "login=$login";

## new changes
      $prml = strapp $prml, "logo=$logo";
      $prml = strapp $prml, "vdomain=$vdomain";
      $prml = strapp $prml, "welcome=$welcome";
      $prml = strapp $prml, "label=$label";
## end new changes

      $password=$logtab{$login}{'password'}; 
      $prml = strapp $prml, "password=$password"; 
      $prml = strapp $prml, "rpassword=$password"; 
      if (exists $surveytab{$login}) {
         $calpeople = $surveytab{$login}{calpeople};
         $editcal = $surveytab{$login}{editcal};
         $calinvite = $surveytab{$login}{'calinvite'};
      } else {
         $surveytab{$login}{login} = $login;
         tied(%surveytab)->sync();        
      }
      $prml = strapp $prml, "calpeople=$calpeople"; 
      $prml = strapp $prml, "editcal=$editcal"; 

      $fname=$logtab{$login}{'fname'};
      $prml = strapp $prml, "fname=$fname";

      $lname = $logtab{$login}{'lname'};
      $prml = strapp $prml, "lname=$lname";

      $street = $logtab{$login}{'street'};
      $prml = strapp $prml, "street=$street";

      $city = $logtab{$login}{'city'};
      $prml = strapp $prml, "city=$city";

      $state = $logtab{$login}{'state'};
      $prml = strapp $prml, "state=$state";

      $zipcode = $logtab{$login}{'zipcode'};
      $prml = strapp $prml, "zipcode=$zipcode";

      $country = $logtab{$login}{'country'};
      $prml = strapp $prml, "country=$country";

      $phone = $logtab{$login}{'phone'};
      $prml = strapp $prml, "phone=$phone";

      $pager = $logtab{$login}{'pager'};
      $prml = strapp $prml, "pager=$pager";

      $pagertype = $logtab{$login}{'pagertype'};
      $prml = strapp $prml, "pagertype=$pagertype";

      $fax = $logtab{$login}{'fax'};
      $prml = strapp $prml, "fax=$fax";

      $bphone = $logtab{$login}{'bphone'};
      $prml = strapp $prml, "busp=$bphone";

      $cphone = $logtab{$login}{'cphone'};
      $prml = strapp $prml, "cellp=$cphone";

      $url = $logtab{$login}{'url'};
      $prml = strapp $prml, "url=$url";

      $zone = $logtab{$login}{'zone'};
      $prml = strapp $prml, "zone=$zone";

      $zonestr = getzonestr($logtab{$login}{'zone'});
      $prml = strapp $prml, "zonestr=$zonestr";

      $checkid = $logtab{$login}{'checkid'};
      $prml = strapp $prml, "checkid=$checkid";

      $calpublish = $logtab{$login}{'calpublish'};
      $prml = strapp $prml, "calpublish=$calpublish";

      $email = $logtab{$login}{'email'};
      $prml = strapp $prml, "email=$email";

      ## $label = "HotDiary Portal Services";
      $prml = strapp $prml, "label=$label";

      $informme = $logtab{$login}{'informme'};
      $prml = strapp $prml, "informme=$informme";
      $prml = strapp $prml, "calinvite=$calinvite";

      $alphjp = substr $jp, 0, 1;
      $alphjp = $alphjp . '-index';

      if ($jp ne "") {
         if (-f "$ENV{HDDATA}/$alphjp/$jp/templates/profile.html") {
            $tmpl = "$ENV{HDDATA}/$alphjp/$jp/templates/profile.html";
         } else {
            $tmpl = "$ENV{HDTMPL}/showprofile.html";
         }
      } else {
         $tmpl = "$ENV{HDTMPL}/showprofile.html";
      }

      $prml = strapp $prml, "template=$tmpl";

      #$prml = strapp $prml, "template=$ENV{HDTMPL}/showprofile.html";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/showprofile-$$.html";

      if ($os ne "nt") {
        $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
        $prml = strapp $prml, "formenc=$formenc";
        $execproxylogout = encurl "/proxy/execproxylogout.cgi";
        $execdeploypage =  encurl "execdeploypage.cgi";
        $execsaveprofile = encurl "execsaveprofile.cgi";
        $execproxylogout = encurl "/proxy/execproxylogout.cgi";
        $execdeploypage =  encurl "execdeploypage.cgi";
        $execshowtopcal =  encurl "execshowtopcal.cgi";
      } else {
        $prml = strapp $prml, "formenc=";
        $execproxylogout = "/proxy/execproxylogout.cgi";
        $execdeploypage =  "execdeploypage.cgi";
        $execsaveprofile = "execsaveprofile.cgi";
	$execproxylogout =  "/proxy/execproxylogout.cgi";
        $execdeploypage =  "execdeploypage.cgi";
        $execshowtopcal =  "execshowtopcal.cgi";
      }

      $rh = $input{rh};
      $prml = strapp $prml, "rh=$rh";

      $prml = strapp $prml, "execdeploypage=$execdeploypage";
      $prml = strapp $prml, "execproxylogout=$execproxylogout";


      $execshowtopcal = encurl "execshowtopcal.cgi";
      $execshowtopcalprog = adjusturl "/jsp/$rh/execdogeneric.jsp?p0=$execshowtopcal&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";


      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=26>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsaveprofile\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=\"$biscuit\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=password>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=fname>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=lname>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=street>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=city>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=state>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=zipcode>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=country>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=phone>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=pager>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=pagertype>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p13 VALUE=fax>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p14 VALUE=busp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p15 VALUE=cellp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p16 VALUE=url>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p17 VALUE=zone>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p18 VALUE=checkid>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p19 VALUE=calpublish>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p20 VALUE=email>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p21 VALUE=rpassword>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p22 VALUE=informme>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p23 VALUE=calinvite>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p24 VALUE=editcal>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p25 VALUE=calpeople>";
      $hiddenvars = gethiddenvars($hiddenvars);
      $hiddenvars = adjusturl $hiddenvars;

      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "vdomain=$vdomain";
      $prml = strapp $prml, "hs=$hs";
      $prml = strapp $prml, "biscuit=$biscuit";
      $prml = strapp $prml, "jp=$jp";
      $prml = strapp $prml, "HDLIC=$HDLIC";
      $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
      $prml = strapp $prml, "execproxylogout=$execproxylogout";
      $prml = strapp $prml, "execdeploypage=$execdeploypage";
      $prml = strapp $prml, "execshowtopcal=$execshowtopcal";

      $sessionheader = getsessionheader($jp);
      $sessionfooter = getsessionfooter($jp);
      $css = getcss($jp);

      $prml = strapp $prml, "css=$css";
      $prml = strapp $prml, "sessionheader=$sessionheader";
      $prml = strapp $prml, "sessionfooter=$sessionfooter";

      $theader = getTheader($jp);
      $tmiddle = getTmiddle($jp);
      $tfooter = getTfooter($jp);
      $prml = strapp $prml, "theader=$theader";
      $prml = strapp $prml, "tmiddle=$tmiddle";
      $prml = strapp $prml, "tfooter=$tfooter";
      parseIt $prml;

      system "cat $ENV{HDTMPL}/content.html";  
      system "cat $ENV{HDHREP}/$alphaindex/$login/showprofile-$$.html";
   }
}

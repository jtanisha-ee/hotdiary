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
# FileName: savecalpreferences.cgi
# Purpose: Top screen for calendar preferences
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug ("savecalpreferences.cgi");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

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
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.\n");
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

   $HDLIC = $input{'HDLIC'};
   $sesstab{$biscuit}{'time'} = time();

   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';
 

   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }

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


   # bind surveytab table vars
   tie %surveytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/surveytab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
                'installation', 'domains', 'domain', 'orgrole', 'organization',
                'orgsize', 'budget', 'timeframe', 'platform', 'priority',
                'editcal', 'calpeople' ] };

   $rh = $input{rh};

   $logtab{$login}{'zone'} = $input{'zone'};
   if ($input{'calinvite'} eq "on") {
      $surveytab{$login}{'calinvite'} = "CHECKED";
   }  else {
       $surveytab{$login}{'calinvite'} = $input{'calinvite'};
   }

   if ($input{'editcal'} eq "on") {
      $surveytab{$login}{'editcal'} = "CHECKED";
   } else {
      $surveytab{$login}{'editcal'} = $input{'editcal'};
   }

   $surveytab{$login}{'calpeople'} = $input{'calpeople'};

   
   if ($input{'calpublish'} eq "on") {
# if old system is in effect, delete the directory, and migrate
# the customer to the new system
      if ($login ne "") {
         system "rm -rf $ENV{HTTPHOME}/html/hd/members/$login";
      }
      if (!(-d "$ENV{HTTPHOME}/html/hd/members/$alphaindex/$login")) {
         $logtab{$login}{'calpublish'} = "CHECKED";
         system "mkdir -p $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
         if ($login ne "") {
            system "rm -f $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login/*.cgi";
            system "ln -s $ENV{HDCGI}/calpublish/index.cgi $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
            system "ln -s $ENV{HDCGI}/calpublish/webpage.cgi $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
            $cmsg = "<p>You have chosen to publish your calendar on the web. A wbesite has been created for you. Your website is \"http://$vdomain/members/$alphaindex/$login\". Please note down this website for your future reference."
 
           # Please click <a href=\"http://www.hotdiary.com/members/$alphaindex/$login\">here</a> to view your calendar!";
 
         } else {
            error("Invalid member login. No operation performed.");
            exit;
        }
     }
  }  else {
     $logtab{$login}{'calpublish'} = $input{'calpublish'};
      if ($login ne "") {
         if (-d "$ENV{HTTPHOME}/html/hd/members/$alphaindex/$login") {
             system "rm -rf $ENV{HTTPHOME}/html/hd/members/$alphaindex/$login";
             $cmsg = "<p>You have chosen not to publish your calendar on the web. HotDiary has removed your website for you.";
         }
         if (-d "$ENV{HTTPHOME}/html/hd/members/$login") {
             system "rm -rf $ENV{HTTPHOME}/html/hd/members/$login";
             $cmsg = "<p>You have chosen not to publish your calendar on the web. HotDiary has removed your website for you.";
         }
      } else {
         error("Invalid member login. No operation performed.");
         exit;
      }
   } 

   $reset = $input{reset};
   if ($reset eq "on") {
      $cmsg .= "All your calendar reminders events and todos have been deleted as you chose to reset your calendar.";
      deleteAllCal($login);
   }

   $editcal = $input{editcal};
   $reset = $input{reset};
   $calpeople = $input{calpeople};
   $calinvite = $input{calinvite};
   $calpublish = $input{calpublish};
   

   $cmsg .= "Your calendar preferences have been saved.";

   if ($os ne "nt") {
     $execshowtopcal = encurl "execshowtopcal.cgi";
   } else {
     $execshowtopcal = "execshowtopcal.cgi";
   } 

   if ($login eq "user8000") {
      $cmsg .= "$calpublish";
   }

   # bind portaltab table vars
   tie %portaltab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/portaltab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['login', 'calcolor', 'photo', 'title', 'logo',
                'tbanner', 'bbanner', 'but1', 'but2', 'but3', 'but4',
                'audio'] };                      

      $portaltab{$login}{photo} = adjusturl $input{photo};
      $portaltab{$login}{login} = $login;
      $portaltab{$login}{title} = adjusturl $input{title};
      $portaltab{$login}{logo} = adjusturl $input{callogo};
      $portaltab{$login}{tbanner} = adjusturl $input{tbanner};
      $portaltab{$login}{bbanner} = adjusturl $input{bbanner};
      $portaltab{$login}{but1} = adjusturl $input{but1};
      $portaltab{$login}{but2} = adjusturl $input{but2};
      $portaltab{$login}{but3} = adjusturl $input{but3};
      $portaltab{$login}{but4} = adjusturl $input{but4};
      $portaltab{$login}{audio} = adjusturl $input{audio};
      tied(%portaltab)->sync();
   $calcolor = $portaltab{$login}{calcolor};
   $val1 = "";
   $val2 = "";
   $val3 = "";
   $val4 = "";
   $val5 = "";
   $val6 = "";
   $val7 = "";
   $val8 = "";
   $val9 = "";
   $val10 = "";
   $val11 = "";
   $val12 = "";
   $val13 = "";

   if ($calcolor eq "") {
       $calcolor = "ffffff";
       $val1 = "CHECKED";
   } else {
      if ($calcolor eq "ffffff") {
          $val1 = "CHECKED";
      } else {
	  if ($calcolor eq "eec591") {
              $val2 = "CHECKED";
	  }  else {
	     if ($calcolor eq "cd5b45") {
                 $val3 = "CHECKED";
	     } else {
	        if ($calcolor eq "8ee5ee") {
                    $val5 = "CHECKED";
	        }  else {
	           if ($calcolor eq "8ee5ee") {
                       $val15 = "CHECKED";
	           } else {
	               if ($calcolor eq "bf3eff") {
                           $val6 = "CHECKED";
	               } else {
	                   if ($calcolor eq "7fffd4") {
                               $val8 = "CHECKED";
	                   } else {
	                       if ($calcolor eq "cd1076") {
                                   $val9 = "CHECKED";
		               } else {
	                           if ($calcolor eq "eeca50") {
                                      $val10 = "CHECKED";
			   	   } else {
	                              if ($calcolor eq "8fbc8f") {
                                         $val11 = "CHECKED";
				      } else {
	                                  if ($calcolor eq "7ac5cd") {
                                             $val12 = "CHECKED";
				          } else {
	                                     if ($calcolor eq "cdad00") {
                                                $val13 = "CHECKED";
					     }
				          }
			              }
				   }
			       }
		           }
		       }
		   }
	        }    
	     }
          } 
       }
    }
   

   if ($input{savecolor} ne "") {
      $prml = "";
      if ($logo ne "") {
         $logo = adjusturl $logo;
      }
      $rh = $input{rh};
      $prml = strapp $prml, "rh=$rh";
      $prml = strapp $prml, "logo=$logo";
      $prml = strapp $prml, "label=$label";
      $sc = $input{sc};
      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prml = strapp $prml, "formenc=$formenc";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execshowtopcal = encurl "execshowtopcal.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execcalclient = encurl "execcalclient.cgi";
         $execfilebrowser = encurl "execfilebrowser.cgi";
         $execsavepubcal = encurl "execsavepubcal.cgi";
      } else {
         $prml = strapp $prml, "formenc=";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execcalclient = "execcalclient.cgi";
         $execfilebrowser = "execfilebrowser.cgi";
         $execsavepubcal = "execsavepubcal.cgi";
      }

      $alphj = substr $jp, 0, 1;
      $alphj = $alphj .  '-index';

      if ( ($jp ne "") && (-f "$ENV{HDDATA}/$alphj/$jp/templates/hdshowbizbg.html") ) {
         $tmpl = "$ENV{HDDATA}/$alphj/$jp/templates/hdshowbizbg.html";
      } else {
           $tmpl = "$ENV{HDTMPL}/hdshowbizbg.html";
      }   

      $prml = strapp $prml, "template=$tmpl";
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/hdshowbizbg-$$.html";
      $prml = strapp $prml, "biscuit=$biscuit";
      $prml = strapp $prml, "execproxylogout=$execproxylogout";
      $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
      $prml = strapp $prml, "execdeploypage=$execdeploypage";
      $prml = strapp $prml, "execcalclient=$execcalclient";
      $prml = strapp $prml, "execfilebrowser=$execfilebrowser";

      $welcome = "Welcome";
      $prml = strapp $prml, "welcome=$welcome";
      $prml = strapp $prml, "login=$login";
      $prml = strapp $prml, "HDLIC=$HDLIC";
      $prml = strapp $prml, "ip=$ip";
      $prml = strapp $prml, "rh=$rh";
      $prml = strapp $prml, "hs=$hs";
      $prml = strapp $prml, "vdomain=$vdomain";
      $prml = strapp $prml, "jp=$jp";
      $prml = strapp $prml, "pubcolor=$calcolor";
      $prml = strapp $prml, "val1=$val1";
      $prml = strapp $prml, "val2=$val2";
      $prml = strapp $prml, "val3=$val3";
      $prml = strapp $prml, "val4=$val4";
      $prml = strapp $prml, "val5=$val5";
      $prml = strapp $prml, "val6=$val6";
      $prml = strapp $prml, "val7=$val7";
      $prml = strapp $prml, "val8=$val8";
      $prml = strapp $prml, "val9=$val9";
      $prml = strapp $prml, "val10=$val10";
      $prml = strapp $prml, "val11=$val11";
      $prml = strapp $prml, "val12=$val12";
      $prml = strapp $prml, "val13=$val13";

      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=3>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execsavepubcal\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=pubcolor>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";    

      $hiddenvars = adjusturl $hiddenvars;
      $prml = strapp $prml, "hiddenvars=$hiddenvars";  

      parseIt $prml;

      system "cat $ENV{HDTMPL}/content.html";
      system "cat $ENV{HDHREP}/$alphaindex/$login/hdshowbizbg-$$.html";
      exit;
   } 

# - Title On The Top (eg. Events For City Of Bern)
#        - Logo On Top Left
#        - Bottom Banner
#        - Top Banner
#        - One picture on left
#        - 4 button banners
#        - Color or Tile background
#        - Background Audio Clip              

   $cmsg .= " Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execshowtopcal&p1=biscuit&p2=jp&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&jp=$jp&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return home.";

   $logtab{$login}{referer} = $jp;

   status ("$login: $cmsg");
   tied(%sesstab)->sync();
   tied(%logsess)->sync();
   tied(%logtab)->sync();
   tied(%surveytab)->sync();



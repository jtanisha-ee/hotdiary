#!/usr/bin/perl

# Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: filebrowser.cgi
# Purpose: Top screen for hotdiary carryon 
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;
use utils::utils;


# parse the command line
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};
   hddebug "filebrowser.cgi";

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $rh = trim $input{'rh'};
   $jp = $input{jp};
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   }
   $os = $input{os};
   $flg = $input{flg};
   hddebug "flg = $flg";
   $framedomain = $input{framedomain};

   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 'account',
    'topleft', 'topright', 'middleright', 'bottomleft', 'bottomright', 'meta'] };

   $hs = $input{'hs'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   $fp = $input{$fp};

   ## fp indicates whether it is public and the users login is selected
   ## lookup the calendars error messages
   if (($fp eq "") || ($login eq "")) {
	status("You do not have the permission to access this directory. Please
enter the members carry on website.");
	exit;
   }
 

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
	 status("No such user name." );
	 exit;
     }


   $alpha = substr $login, 0, 1;
   $alpha = $alpha . '-index';

   if (!-d("$ENV{HDCARRYON}/aux/carryon/$login/")) { 
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/";
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/MyFolder";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/MyFolder";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/MyFolder";
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/MyPhotoAlbum";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/MyPhotoAlbum";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/MyPhotoAlbum";
      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/permittab";
   }

   if (!-e ("$ENV{HDCARRYON}/aux/carryon/$login/permittab")) {

      system "mkdir -p $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chmod 755 $ENV{HDCARRYON}/aux/carryon/$login/permittab";
      system "chown nobody:nobody $ENV{HDCARRYON}/aux/carryon/$login/permittab"; 
   }

   $startdir = "$ENV{HDCARRYON}/aux/carryon/$login";

   # bind permittab table vars
   tie %permittab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDCARRYON}/aux/carryon/$login/permittab",
   SUFIX => '.rec',
   SCHEMA => {
         ORDER => ['entryno', 'fn', 'permit', 'list', 'publish'] };


   if (! -d $startdir) {
      mkdir $startdir, 755; 
      system "chmod 755 $startdir";
   }

   $jumpdir = "";

   if (($framedomain ne "www.hotdiary.com") && ($framedomain ne "hotdiary.com")) {
      $newflg = 2;
   } else {
      $newflg = "";
   }

   ## we need to set the currdir and base dir to the top level 
   $currdir = $input{'currdir'};
   $basedir = $input{'basedir'};

   #if ($currdir eq "")
   #   $currdir = $ENV{HDCARRYON}/aux/carryon/$login;

   #if ($basedir eq "")
   #   $basedir = $ENV{HDCARRYON}/aux/carryon/$login;

   if ( ($currdir =~ /\.\./) || ($currdir =~ /\~/) ) {
     status("$login: Invalid directory specification. HotDiary Security Alert.");
      exit;
   }
   if ( ($basedir =~ /\.\./) || ($basedir =~ /\~/) ) {
      status("$login: Invalid directory specification. HotDiary Security Alert.");
      exit;
      
   }

   $msg = "Click <a href=\"http://www.hotdiary.com/cgi-bin/execfilebrowser_publish.cgi?flg=$newflg&framedomain=$framedomain&jp=$jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&login=$login&f=mc&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\"><b>here</a></b> to go back to file Carry-On'.";

   if (notCarryOnFile($currdir)) {
      status("login: You can have only alphabets(a-z)(A-Z), numerals(0-9), forwards slash(/), and a dot(.) in your directory path. $msg");
      exit;
   }
   if (notCarryOnFile($basedir)) {
      status("login: You can have only alphabets(a-z)(A-Z), numerals(0-9), forwards slash(/), and a dot(.) in your directory path. $msg");
      exit;
   }

   $images = "$ENV{HDHTML}/images";

   $list .= "<TABLE BORDER=\"3\" BORDERCOLOR=dd0402 CELLSPACING=\"0\" CELLPADDING=\"0\" WIDTH=\"75%\">";
   $list .= "<TR BGCOLOR=dddddd>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Name</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Type</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Size</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Permissions</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Change</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Date Accessed</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Delete</FONT></TD>";
   $list .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Email</FONT></TD>";
   $list .= "</TR>";
   $list .= "<TR>";

   if ($currdir eq "") {
      $jumpdir = ".";
   } else {
      if ($basedir eq "") {
         $jumpdir = "$currdir";
      } else {
        $jumpdir = "$basedir/$currdir";
      }
   }

      if ($input{'gocmd'} eq "up") {
         $jumpdir = qx{dirname $jumpdir};
         $jumpdir =~ s/\n//g;
         #$jumpdir = "$jumpdir/..";
         system "cd $startdir; ls $jumpdir > $ENV{HDHOME}/tmp/carryon-$login$$ 2>> $ENV{HDHOME}/tmp/carryon-$login$$";
      } else {
        system "cd $startdir; ls $jumpdir > $ENV{HDHOME}/tmp/carryon-$login$$ 2>> $ENV{HDHOME}/tmp/carryon-$login$$";
      }
   hddebug "startdir = $startdir, lsdir = $jumpdir, jumpdir=$jumpdir, currdir= $currdir, basedir=$basedir";

   if (($startdir ne "$ENV{HDCARRYON}/aux/carryon/$login") && ($jumpdir ne "$ENV{HDCARRYON}/aux/carryon/$login") ) {
       status("$login: You donot have the permission to access the files. Email has been sent to customer representative for violating the security of HotDiary Inc.");
       exit;
   }

   
   $home_flg = 0;
   open infiile, "<$ENV{HDHOME}/tmp/carryon-$login$$";
   while (<infiile>) {
         $_ =~ s/\n//g;

	 if ("\L$_" eq "\Lpermittab") {
	    next;	
	 }
	 $permission = "personal";
	 $en = "";
	 foreach $entryno (sort keys %permittab) {
	    if ($permittab{$entryno}{fn} eq "$_") {
	       $permission = $permittab{$entryno}{permission};
	       $en = $entryno;
	    }
	 }
         if ($fp eq "p") {
	    ## Not the owner of these files
	    ## Is permission private, if private, is this user a listed member
	    ## in the permittab list. If he is not listed, donot display the 
	    ## this file.
	    $fuser = $input{fuser};
	    $owner = $input{owner};
            if ($permission ne "public") {
   	       if ($owner ne $fuser) {
	          if ($permission eq "private") {
	 	     if ((index "\L$permittab{$entryno}{list}", "\L$fuser") != -1) {
		        next; 
		     }
	          }
	          if ($permission eq "personal") {
		     next;
	          }    
               } 
	    }
         }
         if ($permission eq "") {
	    $permission = "personal";
         }
	 ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat "$startdir/$jumpdir/$_";
	 ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($mtime);
         $year = $year + 1900;
         $mon = $mon + 1;
	 $dirpath = "$jumpdir";
         if (-d "$startdir/$jumpdir/$_") {
            $msize = qx{du -s $startdir/$jumpdir/$_};
            $msize =~ s/\n//g;
	    ($ksize, $rem) = split(" ", $msize);
	    hddebug "ksize = $ksize";
            $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execfilebrowser.cgi?flg=$newflg&framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&basedir=$jumpdir&currdir=$_\"><IMG SRC=\"$images/folder.gif\" WIDTH=20 HEIGHT=20 BORDER=0>$_</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>";
            $list .= "<TD>Directory</TD>";
	    $list .= "<TD>$ksize Kb &nbsp;</TD>";
	    $list .= "<TD>$permission &nbsp;</TD>";
	    if (("\L$_" eq "\LMyFolder") || ("\L$_" eq "\LMyPhotoAlbum")) {
	       $list .= "<TD>N/A</TD>";
	       $list .= "<TD>$mon/$mday/$year &nbsp;</TD>";
	       $list .= "<TD>N/A</TD>";
	       $list .= "<TD>N/A</TD></TR>";
	       $home_flg = 1;
	    } else {
	       $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execeditfile.cgi?jp=$jp&framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&login=$login&en=$en&filename=$_&basedir=$jumpdir\">Change</TD>";
	       $list .= "<TD>$mon/$mday/$year &nbsp;</TD>";
	       $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execdelfile.cgi?framedomain=$framedomain&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&dir=dir&dirpath=$dirpath&l=$login&dirname=$_\"><IMG SRC=\"$images/delevt.gif\" WIDTH=20 HEIGHT=20 BORDER=0></a></TD>";
	       $list .= "<TD>N/A &nbsp;</TD></TR>";
	    }
         } else {
            if (-f "$startdir/$jumpdir/$_") {
	     $fn = $_; 
	     $up = $currdir;
	     ($fn, $ext) = split (/\./, $fn);
	     $fnimg = "filetxt.gif";
	     $app = $_;
	     if (($ext eq "zip") || ($ext eq "tar") || 
	  	($ext eq "gz")) {
	        $fnimg = "filezip.gif";
	     }
	     if ($ext eq "rm") {
	        $fnimg = "fileavi.gif";
	     }
	     if ($ext eq "avi") {
	        $fnimg = "fileavi.gif";
	     }
	     if ($ext eq "java") {
	        $fnimg = "filejava.gif";
	     }
	     if ($ext eq "pdf") {
	        $fnimg = "filepdf.gif";
	        $app = "xpdf::$_:";
	    }
	    if ($ext eq "exe") {
	       $fnimg = "fileexe.gif";
	    }
	    if ($ext eq "wav") {
	       $fnimg = "filewav.gif";
	    }
	    if ($ext eq "gif") {
	       $fnimg = "filegif.gif";
	    }
	    if ($ext eq "doc") {
	       $fnimg = "filedoc.gif";
	    }
	    if ($ext eq "xls") {
	       $fnimg = "filexls.gif";
	    }
	    if ($ext eq "xls") {
	       $fnimg = "filexls.gif";
	    }

	    ## this is a working code 
            #system "ls -l $startdir/$jumpdir/$_ > $ENV{HDHOME}/tmp/filesize";
            #$size = qx{cat $ENV{HDHOME}/tmp/filesize | awk '{print \$5}'};
            #hddebug "size = $size";

            #$date = qx{cat $ENV{HDHOME}/tmp/filesize | awk '{print \$6}'};
            #hddebug "date = $date";
            #$date .= qx{cat $ENV{HDHOME}/tmp/filesize | awk '{print \$7}'};
            #$year = qx{cat $ENV{HDHOME}/tmp/filesize| awk '{print \$8}'};
	    #if ((index "\L$year", "\L:") != -1) {
		#$date .= "1999";
	    #} else {
		#$date .= $year;
	    #}

	    $list .= "<TR>";
	    ## syntax for file opening with appropriateextension
            ## file:/tmp/test.html
            $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execfire.cgi?framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&login=$login&ftype=$ext&dfile=$jumpdir&catfile=$_\"><IMG SRC=\"$images/$fnimg\" WIDTH=20 HEIGHT=20 BORDER=0>$_</a>&nbsp;&nbsp;&nbsp;&nbsp&nbsp;</TD>";
	    $list .= "<TD>File</TD>";
	    $list .= "<TD>$size &nbsp;</TD>";
	    $list .= "<TD>$permission &nbsp;</TD>";
	    $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execeditfile.cgi?framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&login=$login&en=$en&filename=$_&basedir=$jumpdir\">Change</TD>";
	    $list .= "<TD>$mon/$mday/$year &nbsp;</TD>";
	    $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execdelfile.cgi?framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&dir=file&dirpath=$dirpath&l=$login&filename=$_\"><IMG SRC=\"$images/delevt.gif\" WIDTH=20 HEIGHT=20 BORDER=0></a></TD>";
	    $list .= "<TD><a href=\"http://www.hotdiary.com/cgi-bin/execcarryonmail.cgi?framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC&basedir=$jumpdir&l=$login&filename=$_\">Email&nbsp;</a></TD></TR>";
         }   
	}
      }
	
      close infiile;
   #}

   $status = "";
   $list .= "</TABLE>";
   $list = adjusturl $list;
   $myfolder =  "<a href=\"http://www.hotdiary.com/cgi-bin/execfilebrowser.cgi?flg=$newflg&framedomain=$framedomain&rh=$rh&hs=$hs&vdomain=$vdomain&jp=$jp&HDLIC=$HDLIC\">My Carry-On</a>";
   $myfolder = adjusturl($myfolder);


   $prml = "";
   $pra = "";
   $prb = "";
   $prc = "";

   $hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=13>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=$execuploadfile>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=list>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=uploadfile>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=uploadname>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=jumpdir>";
   #$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=startdir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=CreateDirectory>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=upload>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=currdir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p10 VALUE=basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p11 VALUE=framedomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p12 VALUE=jp>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jumpdir VALUE=$jumpdir>";
   #$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=startdir VALUE=$startdir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=currdir VALUE=$currdir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=basedir VALUE=$basedir>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=framedomain VALUE=$framedomain>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";

   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";
   $hiddenvars = adjusturl $hiddenvars;

   if ($logo ne "") {
         $logo = adjusturl $logo;
   }

   hddebug "label = $label, vdomain = $vdomain";
   #$prml = strapp $prml, "rh=$rh";

   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   if ($os ne "nt") {
      #$formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $formenc = adjusturl "ENCTYPE=\"multipart/form-data\"";
      $prml = strapp $prml, "formenc=$formenc";
      $pra = strapp $pra, "formenc=$formenc";
      $prb = strapp $prb, "formenc=$formenc";
      $prc = strapp $prc, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execuploadfile =  encurl "execuploadfile.cgi";
      $execcalclient =  encurl "execcalclient.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $pra = strapp $pra, "formenc=";
      $prb = strapp $prb, "formenc=";
      $prc = strapp $prc, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execuploadfile =  "execuploadfile.cgi";
      $execcalclient =   "execcalclient.cgi";
   }

   $welcome = "Welcome";
   hddebug "flg = $flg";

   if ($flg eq "") {
      if ($home_flg eq "1") { 
         $prml = strapp $prml, "template=$ENV{HDTMPL}/homebrowser.html";
	 $status = "Click on MyFolder or MyPhotoAlbum link to upload and email files, photos, Images, MP3 to family, friends, and co-workers.";
      } else {
         $prml = strapp $prml, "template=$ENV{HDTMPL}/filebrowser.html";
      }
      $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alpha/$login/filebrowser-$login$$.html";
   } else {
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";
      if ($home_flg eq "1")  {
        $prb = strapp $prb, "template=$ENV{HDTMPL}/jzhomebrowser.html";
        $status = "Click on MyFolder or MyPhotoAlbum link to upload and email files, photos, Images, MP3 to family, friends, and co-workers.";
      } else {
         $prb = strapp $prb, "template=$ENV{HDTMPL}/jzfilebrowser.html";
      }
      $prb = strapp $prb, "templateout=$ENV{HDREP}/$alpha/$login/jzfilebrowser-$$.html";

      $prb = strapp $prb, "biscuit=$biscuit";
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $prb = strapp $prb, "jp=$jp";
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "status=$status";
      $prb = strapp $prb, "list=$list";
      $prb = strapp $prb, "myfolder=$myfolder";
      $prb = strapp $prb, "execcalclient=$execcalclient";
      if ($currdir ne "") {
         $prb = strapp $prb, "curdir=<B>Current Directory: $currdir</B>";
      } else {
         $prb = strapp $prb, "curdir=";
      }
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
      parseIt $prb;

      if ($flg == 1) {
        $pra = strapp $pra, "logo=$logo";
        $pra = strapp $pra, "label=$label";
        $pra = strapp $pra, "template=$ENV{HDTMPL}/jztopfilebrowser.html";
        $pra = strapp $pra, "templateout=$ENV{HDREP}/$alpha/$login/jztopfilebrowser-$$.html";
        $pra = strapp $pra, "biscuit=$biscuit";
        $pra = strapp $pra, "business=$business";
        $pra = strapp $pra, "welcome=$welcome";
        $pra = strapp $pra, "login=$login";
        $pra = strapp $pra, "HDLIC=$HDLIC";
        $pra = strapp $pra, "ip=$ip";
        $pra = strapp $pra, "rh=$rh";
        $pra = strapp $pra, "hs=$hs";
        $pra = strapp $pra, "vdomain=$vdomain";
        $pra = strapp $pra, "hiddenvars=$hiddenvars";
        $pra = strapp $pra, "status=$status";
        $pra = strapp $pra, "list=$list";
        $pra = strapp $pra, "myfolder=$myfolder";
        $pra = strapp $pra, "jp=$jp";
        $pra = strapp $pra, "execcalclient=$execcalclient";
        if ($currdir ne "") {
           $pra = strapp $pra, "curdir=<B>Current Directory: $currdir</B>";
        } else {
           $pra = strapp $pra, "curdir=";
        }
        $pra = strapp $pra, "execproxylogout=$execproxylogout";
        $pra = strapp $pra, "execdeploypage=$execdeploypage";
        $pra = strapp $pra, "execshowtopcal=$execshowtopcal";
        parseIt $pra;
      }
      if ($flg eq "1") {
        $prc = strapp $prc, "template=$ENV{HDTMPL}/jzcarryonmenu.html";
        $prc = strapp $prc, "templateout=$ENV{HDREP}/$alpha/$login/jzcarryonmenu-$login$$.html";
        $prc = strapp $prc, "topFrame=/rep/$alpha/$login/jztopfilebrowser-$$.html";
        $prc = strapp $prc, "bottomFrame=/rep/$alpha/$login/jzfilebrowser-$$.html";
        parseIt $prc;
      } 
   }

   if ($flg eq "") {
      $prml = strapp $prml, "biscuit=$biscuit";
      $prml = strapp $prml, "business=$business";
      $prml = strapp $prml, "welcome=$welcome";
      $prml = strapp $prml, "login=$login";
      $prml = strapp $prml, "HDLIC=$HDLIC";
      $prml = strapp $prml, "ip=$ip";
      $prml = strapp $prml, "rh=$rh";
      $prml = strapp $prml, "hs=$hs";
      $prml = strapp $prml, "vdomain=$vdomain";
      $prml = strapp $prml, "hiddenvars=$hiddenvars";
      $prml = strapp $prml, "status=$status";
      $prml = strapp $prml, "list=$list";
      $prml = strapp $prml, "myfolder=$myfolder";
      $prml = strapp $prml, "jp=$jp";
      $prml = strapp $prml, "execcalclient=$execcalclient";
      if ($currdir ne "") {
         $prml = strapp $prml, "curdir=<B>Current Directory: $currdir</B>";
      } else {
         $prml = strapp $prml, "curdir=";
      }
  
      $prml = strapp $prml, "execproxylogout=$execproxylogout";
      $prml = strapp $prml, "execdeploypage=$execdeploypage";
      $prml = strapp $prml, "execshowtopcal=$execshowtopcal";
      parseIt $prml;
      system "cat $ENV{HDTMPL}/content.html";
      system "cat $ENV{HDHREP}/$alpha/$login/filebrowser-$login$$.html";
   } else {
      if ($flg == 1) {
         system "cat $ENV{HDREP}/$alpha/$login/jzcarryonmenu-$login$$.html";
      } else {
         system "cat $ENV{HDTMPL}/content.html";
         system "cat $ENV{HDREP}/$alpha/$login/jzfilebrowser-$$.html";
      }
   }

   # reset the timer.
   tied(%sesstab)->sync();
   tied(%logsess)->sync();

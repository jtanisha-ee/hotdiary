package utils::utils;
require Exporter;
use Time::Local;
use tparser::tparser;
use AsciiDB::TagFile;
use MIME::Base64;

@ISA = qw(Exporter);
@EXPORT = qw(notName notPhone notEmail notUrl notAddress notNumber notDesc notDate notHour notMinSec notMeridian trim replaceblanks adjusturl error status hddebug hddebugtraffic hidebugtraffic hderror buildurl getkeys dirlist isaptcurrent etimetosec ctimetosec getzonestr adjustzone nmmatch getmonthstr notLogin nmmatchcs multselkeys multsel getPhoneDigits getAreaCode getPhoneMiddleDigits getPhoneEndDigits getFaxSavUSPhoneDigits getMoYrDy getGmValues getdailyEtime notNumeric notSkyTelPin notAirTouchPin notPageMartPin notNextelPin notEmailAddress notAlphaNumeric notCarryOnFile notCarryOnName isHiddenFile errors statuss replacewithplus normalizeurlparmvalue isstd sortrep sortmemo sortmemodate sortgroupmemo sortgroupmemodate sortcontacts goodwebstr normalizeurlparmvalue quikstatus encurl getuserstime depositmoney withdrawmoney hdsystem hdsystemcat statuscat wrapstr getlogin getbiscuit gethdvisitor validvdomain gethiddenvars getsessionheader getsessionfooter getcss getTheader getTfooter getTmiddle);

sub notName {
   my($nm) = @_;
   return ($nm =~ /[^a-zA-Z\d\s\.\&\',+;\-\(\)\[\]{}\@|\!\%\?*\<\>\_\:]+/);
}

sub notPhone {
   my($nm) = @_;
   return ($nm =~ /[^a-zA-Z\d\\(\\)\-\s,@.=+]+/);
}

sub notEmail {
   my($em) = @_;
   return ($em =~ /[^a-zA-Z\d\!\.\\@\_\-\s]+/);
}

sub notUrl {
   my($ur) = @_;
   return ($ur =~ /[^a-zA-Z\d\:\=\+\?\/\@\!\.\_\-\~\s\&]+/);
}

sub notAlphaNumeric {
   my($ur) = @_;
   return ($ur =~ /[^a-zA-Z\d\s]+/);
}

sub notCarryOnFile {
   my($ur) = @_;
   $fchar = substr $ur, 0, 1;
   return ( ($ur =~ /[^a-zA-Z\_\-\d\/\.]+/) || ($fchar eq '/') );
}

sub notCarryOnName {
   my($ur) = @_;
   $fchar = substr $ur, 0, 1;
   return ( ($ur =~ /[^a-zA-Z\-\_\d\.]+/) || ($fchar eq '/') );
}

sub isHiddenFile {
   my($ur) = @_;
   $fchar = substr $ur, 0, 1;
   return ($fchar eq '.');
}

sub notAddress {
   my($ad) = @_;
   return ($ad =~ /[^a-zA-Z\d\s\/\-,;+\:\.\&\'\#\(\)\'\<\>\_\[\]{}*\?\%\@\=\$\!|]+/);
}


sub notNumber {
   my($nu) = @_;
   return ($nu =~ /[^a-zA-Z\d\-\\(\\)\s]+/);
}

sub notDesc {
   my($nu) = @_;
   #return ($nu =~ /[^\w\s]+/); 
   return ($nu =~ /[^a-zA-Z\d\-\,\;+\:\?\(\)\&\_\%\@\=\$\!\#\<\>\s\.\'\/\[\]{}*|\~]+/);
}

sub notDate {
   my($da, $mo, $yr) = @_;
  
   $yl = '1970';
   $yu = '2038';
   $ml = '1';
   $mu = '12';
   $dl = '1';
  
   if ((notNumber $da) || (notNumber $mo) || (notNumber $yr)) {
      return 1;
   }

   if (($mo eq 1) || ($mo eq 3) || ($mo eq 5) || ($mo eq 7) ||
       ($mo eq 8) || ($mo eq 10) || ($mo eq 12)) {
      $du = 31;
   } else {
      if ($mo ne 2) {
         $du = 30;
      } else {
         if (($yr % 4) eq 0) {
            $du = 29;
         } else {
            $du = 28;
         }
      }
   }
 
   return (($da < $dl) || ($da > $du) || ($mo < $ml) || ($mo > $mu) ||
           ($yr < $yl) || ($yr > $yu));
}

sub notHour {
   my($hr) = @_;
   return (notNumber $hr) || ($hr < 1) || ($hr > 12);
}

sub notMinSec {
   my($ms) = @_;
   return (notNumber $ms) || ($ms < 0) || ($ms > 59);
}

sub notMeridian {
   my($mr) = @_;
   return ((notName $mr) || (("\U$mr" ne "AM") && ("\U$mr" ne "PM")));
}

sub trim {
   my($ts) = @_;
   $ts =~ s/[\s]+/ /g;
   @hsh = split(" ", $ts);
   #print $#hsh;
   #print @hsh[0];
   $ts = "";
   #@hsh[0] = "\b@hsh[0]";
   foreach $i (@hsh) {
      if ($ts eq "") {
        $ts = "$i";
      } else {
        $ts = "$ts $i";
      }
   }
   return $ts;
}

sub replaceblanks {
   my($msg) = @_;
   $msg = trim $msg;
   $msg =~ s/\s/%20/g;
   return $msg;
}

sub adjusturl {
   my($ur) = @_;
   $ur =~ s/\=/\-\-\-/g;
   return $ur;
}

#  reservered characters in url string:
#  =  |  ;  |  /  |  #  | ? |  : | space
sub normalizeurlparmvalue {
   my($ur) = @_;
   $ur =~ s/\&/%26/g;
   $ur =~ s/\|/%7c/g;
   $ur =~ s/\'/%27/g;
   $ur =~ s/\=/%3d/g;
   $ur =~ s/\?/%3f/g;
   $ur =~ s/\;/%3b/g;
   $ur =~ s/\#/%23/g;
   $ur =~ s/\:/%3a/g;
   $ur =~ s/\//%2f/g;
# replacing space damages CRLF (\r\n). Hence we first
# replace those with %0d%0a below
   $ur =~ s/\r\n/%0d%0a/g;
# extra stuff
   $ur =~ s/\)/%29/g;
   $ur =~ s/\(/%28/g;
   $ur =~ s/\#/%2a/g;
   $ur =~ s/\+/%2b/g;
   $ur =~ s/\,/%2c/g;
   $ur =~ s/\-/%2d/g;
   $ur =~ s/\./%2e/g;
   $ur =~ s/\>/%3e/g;
   $ur =~ s/\</%3c/g;
   $ur =~ s/\"/%22/g;
   $ur =~ s/\!/%21/g;
   $ur =~ s/\~/%7e/g;
   $ur =~ s/\{/%7b/g;
   $ur =~ s/\}/%7d/g;
   $ur =~ s/\[/%5b/g;
   $ur =~ s/\\/%5c/g;
   $ur =~ s/\]/%5d/g;
   $ur =~ s/\_/%5f/g;
   $ur =~ s/\^/%5e/g;
   return $ur;
}

sub replacewithplus {
   my($msg) = @_;
   $msg = trim $msg;
   $msg =~ s/\s/+/g;
   return $msg;
}

#sub error {
   #my($msg) = @_;
   #$somefile = "$$.html";
   #$ENV{template} = "$ENV{HDTMPL}/errorTemplate.html";
   #$ENV{templateout} = "$ENV{HDREP}/common/$somefile";
   #$ENV{label} = $msg;
   #$ret = ParseTem::ParseTem::parseIt;
   #system "/bin/cat $ENV{HDREP}/common/$somefile";
   #system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   #$msg =~ s/\"/\\"/g;
   #$msg =~ s/\n//g;
   #$msg = localtime(time()) . " $msg";
   #system "echo \"$msg\" >> $ENV{HDHOME}/logs/hderror.log";
   #return;
#}

sub error {
   my($msg) = @_;

   $somefile = "$$.html";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/errorTemplate.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/$somefile";
   $msg = adjusturl $msg;
   $prml = strapp $prml, "label=$msg";
   parseIt $prml;

   system "/bin/cat $ENV{HDREP}/common/$somefile";
   system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hderror.log";
   return;
}


#sub errors {
   #my($msg) = @_;
   #$somefile = "$$.html";
   #$ENV{template} = "$ENV{HDTMPL}/error.html";
   #$ENV{templateout} = "$ENV{HDREP}/common/$somefile";
   #$ENV{label} = $msg;
   #$ret = ParseTem::ParseTem::parseIt;
   #system "/bin/cat $ENV{HDREP}/common/$somefile";
   #system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   #$msg =~ s/\"/\\"/g;
   #$msg =~ s/\n//g;
   #$msg = localtime(time()) . " $msg";
   #system "echo \"$msg\" >> $ENV{HDHOME}/logs/hderror.log";
   #return;
#}
#

sub errors {
   my($msg) = @_;

   $somefile = "$$.html";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/error.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/$somefile";
   $msg = adjusturl $msg;
   $prml = strapp $prml, "label=$msg";
   parseIt $prml;

   system "/bin/cat $ENV{HDREP}/common/$somefile";
   system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hderror.log";
   return;
}


sub hddebug {
   my($msg) = @_;
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hddebug.log";
   return;
}

sub hddebugtraffic {
   my($msg) = @_;
   $msg =~ s/\"/\\"/g;
   #$msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/traffic.log";
   return;
}

sub hidebugtraffic {
   my($msg) = @_;
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hitraffic.log";
   return;
}


#sub status {
   #my($msg) = @_;
   #$somefile = "$$.html";
   #$ENV{template} = "$ENV{HDTMPL}/statusTemplate.html";
   #$ENV{templateout} = "$ENV{HDREP}/common/$somefile";
   #$ENV{label} = $msg;
   #$ret = ParseTem::ParseTem::parseIt;
   #system "/bin/cat $ENV{HDREP}/common/$somefile";
   #system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   #$msg =~ s/\"/\\"/g;
   #$msg =~ s/\n//g;
   #$msg = localtime(time()) . " $msg";
   #system "echo \"$msg\" >> $ENV{HDHOME}/logs/hdstatus.log";
   #return;
#}

sub status {
   my($msg) = @_;

   #$msg = "<HR><CENTER><H1>HotDiary.com site is being upgraded.</H1>We are experiencing a lot of traffic, and we are upgrading our infrastucture to support millions of additional users. We should be ready on Monday Aug 7, 2000, by 6 AM PST. We apologize for the inconvenience this has caused you.<P><HR>";
   $somefile = "$$.html";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/statusTemplate.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/$somefile";
   $msg = adjusturl $msg;
   $prml = strapp $prml, "label=$msg";
   parseIt $prml;

   system "/bin/cat $ENV{HDREP}/common/$somefile";
   system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hdstatus.log";
   return;
}

sub quikstatus {
   my($msg) = @_;

   system "cat $ENV{HDTMPL}/content.html";
   print "<HTML><BODY>|$msg|</BODY></HTML>"; 
}

sub statuss {
   my($msg) = @_;
   #$msg = "<HR><CENTER><H1>HotDiary.com site is being upgraded.</H1>We are experiencing a lot of traffic, and we are upgrading our infrastucture to support millions of additional users. We should be ready on Monday Aug 7, 2000, by 6 AM PST. We apologize for the inconvenience this has caused you.<P><HR>";

   $somefile = "$$.html";

   $prml = "";
   $prml = strapp $prml, "template=$ENV{HDTMPL}/status.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/common/$somefile";
   $msg = adjusturl $msg;
   $prml = strapp $prml, "label=$msg";
   parseIt $prml;

   system "/bin/cat $ENV{HDREP}/common/$somefile";
   system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hdstatus.log";
   return;
}

#sub statuss {
   #my($msg) = @_;
   #$somefile = "$$.html";
   #$ENV{template} = "$ENV{HDTMPL}/status.html";
   #$ENV{templateout} = "$ENV{HDREP}/common/$somefile";
   #$ENV{label} = $msg;
   #$ret = ParseTem::ParseTem::parseIt;
   #system "/bin/cat $ENV{HDREP}/common/$somefile";
   #system "/bin/rm -f $ENV{HDREP}/common/$somefile";
   #$msg =~ s/\"/\\"/g;
   #$msg =~ s/\n//g;
   #$msg = localtime(time()) . " $msg";
   #system "echo \"$msg\" >> $ENV{HDHOME}/logs/hdstatus.log";
   #return;
#}

sub hderror {
   my($msg) = @_;
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> $ENV{HDHOME}/logs/hderror.log";
   return;
}


sub buildurl {
   my($url) = @_;
   $myurl = "cgi-bin/$url";
   return $myurl;
}

# bind sequence table vars
#   tie %seqtab, 'AsciiDB::TagFile',
#   DIRECTORY => '../data/seqtab',
#   SUFIX => '.rec',
#   SCHEMA => {
#
#        ORDER => ['sessionid'] };
#
#
# bind address entry table vars
#   tie %addrnotab, 'AsciiDB::TagFile',
#   DIRECTORY => '../data/addrnotab',
#   SUFIX => '.rec',
#   SCHEMA => {  
#        ORDER => ['entryno'] };

#constructs a sessionid from time since epoch and process id

sub getkeys {
   $tt = time();
   $sessionid = "$tt$$";
   return $sessionid;
}



# commented this out, since if run thru web on best, the lock
# does not work. in plain terminal it works fine. so keep this
# code for future use.
# getkeys uses two arguments tablename and fieldname.
# fieldname  is substitued for eg: 'sessionid' or 'entryno'.
# tablename is substitued for eg:  seqtab, addrnotab etc.
# needs to be tested for locking.

#sub getkeys { 
#
#   my($tablename) = $_[0];
#   my($fieldname) = $_[1];
#
#   opendir THISDIR, "../../hd/data/$tablename";
#
#   @allfiles = grep !/^\.\.?$/, readdir THISDIR;
#   foreach $fiile (@allfiles) {
#     ($fiiile, $sufffix) = split(/\./, $fiile);
#      open infiile, "$fiile";
#      $ret = flock(infiile, 2);
#      print "flock ret = ", $ret;
#      $oldkeyid = $$tablename{$fiiile}{$fieldname};
#      $mykey = $oldkeyid + 1;
#      $ret = flock(infiile, 8);
#      print "flock unlock ret = ", $ret;
#      delete $$tablename{$oldkeyid};
#      $$tablename{$mykey}{$fieldname} = $mykey;
#    #  print "new sessionid = ", $mykey;
#    }
#
#    return $mykey;
#}

sub dirlist {
   ($sdir) = @_;
   opendir THISDIR, $sdir;
   %dirlist2 = grep !/^\./, readdir THISDIR;
   print "dirlist2=", %dirlist2;
   %dirlist3 = grep !/^\./, readdir THISDIR;
   print "dirlist3 =", %dirlist3;
   %dirlist4= join %dirlist2, %dirlist3;
   closedir THISDIR;
   return %dirlist4;
  
}

#
# This function takes as input the current time and expected time both
# in GM format. 
#
sub isaptcurrent {
   ($ctm, $etm) = @_;

   # the event time is already passed. it is an old event.
   if (($etm - $ctm) < 0) {
      #print "event is already passed \n";
      return 0;
   } 

   # this event will happen ,after 10 min. but before and incl. 20 min.
   if ((($etm - $ctm) > 600) && (($etm - $ctm) <= 1200)) {
      #print "An event is due \n";
      return 1;
   }
   #print "event is somewhere in the future \n";
   return 0;
}

# 
# this function takes time as input in the users time zone specified 
# in appointment/collabrum table.
# It then converts this into seconds after epoch. 
# It then converts this seconds into appropriate gm time in seconds.
#  
sub etimetosec {
   ($sec, $min, $hour, $day, $month, $year, $wday, $yday, $isdst, $tz) = @_;
   $etime = 0;
   if ($month > 0) {
      $etime = timegm($sec, $min, $hour, $day, ($month - 1), ($year - 1900));
      $etime = $etime - ($tz * 3600);
   }
   return($etime); 
}

#
# this function returns current local time in seconds in GMT.
# we add 8 hours in seconds to local time in seconds after epoch.
# 
sub ctimetosec {
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time()); 
   $ctm = timegm($sec, $min, $hour, $mday, $mon, $year);
   $ctm = $ctm + ( 8 * 3600);
   return($ctm); 
}

sub getmonthstr {

   ($month) = @_;

   if ($month == 12) {
       return "Dec";
   }
   if ($month == 11) {
       return "Nov";
   }
   if ($month == 10) {
       return "Oct";
   }
   if ($month == 9) {
       return "Sep";
   }
   if ($month == 8) {
       return "Aug";
   }
   if ($month == 7) {
       return "Jul";
   }
   if ($month == 6) {
       return "Jun";
   }
   if ($month == 5) {
       return "May";
   }
   if ($month == 4) {
       return "Apr";
   }
   if ($month == 3) {
       return "Mar";
   }
   if ($month == 2) {
       return "Feb";
   }
   if ($month == 1) {
       return "Jan";
   }
}

sub getzonestr {
   ($zone) = @_;

   if ($zone == -12) {
       return "DateLine";
   }
   # STD
   if ($zone == -11) {
	return "Samoa";
   }

   # STD
   if ($zone == -10) {
        return "Hawaiian";
   }
   # DST
   if ($zone == -9) {
        return "Alaskan";
   }
   # DST
   if ($zone == -8) {
        return "Pacific"; 
   }
   # DST
   if ($zone == -7) {
        return "Mountain"; 
   }
   # DST
   if ($zone == -6) {
        return "Central"; 
   }
   # DST
   if ($zone == -5) {
        return "Eastern"; 
   }

   # STD
   if ($zone == -4) {
        return "Atlantic"; 
   }

   # don't know assume STD 
   if ($zone == -3.5) {
        return "Newfoundland"; 
   }

   # STD
   if ($zone eq "-3B") {
        return "Brazil"; 
   }

   # STD
   if ($zone eq "-3A") {
        return "Argentina"; 
   }

   # don't know assume DST
   if ($zone == -2) {
        return "Mid-Atlantic"; 
   }

   # DST
   if ($zone == -1) {
        return "Azores"; 
   }

   # DST
   if ($zone == -0) {
        return "GMT"; 
   }

   # STD namibia, nigeria, congo, cameroon, chad, tunisia, gabon, equ guninea GMT +1
   # STD Ethiopia, tanzania, Kenya, uganda, somalia GMT + 3
   # DST Egypt GMT + 3
   # STD Zambia, s.africa, sudan, botswana, rwanda, burundi, zimbabwe + 2
   # STD gambia, ghana, liberia, morrocco +0
  
   # DST 
   if ($zone == 1) {
        return "W.Europe"; 
   }

   # DST
   if ($zone == 2) {
        return "E.Europe"; 
   }

   #  DST
   if ($zone eq "3R") {
        return "Russia"; 
   }

   # STD
   if ($zone eq "3S") {
        return "Saudi Arabia"; 
   }

   # DST
   if ($zone == 3.5) {
        return "Iran"; 
   }

   # STD
   if ($zone == 4) {
        return "Arabian"; 
   }

   #  DST
   if ($zone == 5) {
        return "W.Asia"; 
   }

   #  STD
   if ($zone == 5.5) {
        return "India"; 
   }

   # STD
   if ($zone == 6) {
        return "C.Asia";
   }

   # STD
   if ($zone eq "7T") {
        return "Thailand";
   }

   # STD 
   if ($zone eq "7V") {
        return "Vietnam";
   }

   # STD
   if ($zone eq "7I") {
        return "Indonesia";
   }
   # STD
   if ($zone eq "8C") {
        return "China";
   }
   # STD
   if ($zone eq "8S") {
        return "Singapore";
   }

   # STD
   if ($zone eq "8T") {
        return "Taiwan";
   }

   # STD
   if ($zone eq "9J") {
        return "Japan";
   }

   # STD
   if ($zone eq "9K") {
        return "Korea";
   }

   #  STD
   if ($zone == 9.5) {
        return "C.Australia";
   }

   # STD
   if ($zone == 10) {
        return "E.Australia";
   }
   # STD
   if ($zone eq "12F") {
        return "Fiji";
   }
   # STD
   if ($zone eq "12N") {
        return "New Zealand";
   }
}


sub adjustzone {

   ($zone) = @_;

   if ($zone eq "-3B") {
      return '-3';
   }  
   if ($zone eq "-3A") {
     return '-3';
   }
   if ($zone eq "3R") {
     return '3';
   }
   if ($zone eq "3S") {
       return '3';
   } 
   if ($zone eq "7T") {
      return '7';
   }
   if ($zone eq "7V") {
       return '7';
   } 
   if ($zone eq "7I") {
      return '7';
   } 
   if ($zone eq "8C") {
      return '8';
   } 
   if ($zone eq "8S") {
      return '8';
   } 
   if ($zone eq "8T") {
      return '8';
   } 
   if ($zone eq "9J") {
     return '9';
   } 
   if ($zone eq "9K") {
      return'9';
   } 
   if ($zone eq "12F") {
      return '12';
   } 
   if ($zone eq "12N") {
      return '12';
   } 
   return $zone;
}

sub nmmatch {
   ($nm, $match) = @_;
   $cnm = "\U$nm";
   $cmatch = "\U$match";
   return((index $cnm, $cmatch) == 0);
   #return (($cnm =~ /$cmatch/) || ($cnm =~ /$cmatch[\w]+/));
}

sub nmmatchcs {
   ($nm, $match) = @_;
   $cnm = "$nm";
   $cmatch = "$match";
   return((index $cnm, $cmatch) == 0);
   #return (($cnm =~ /$cmatch/) || ($cnm =~ /$cmatch[\w]+/));
}

sub notLogin {
   my($nm) = @_;
   # return ($nm =~ /[^a-zA-Z\d\_\-\.]+/);
   return ( ($nm =~ /[^a-zA-Z\d\_\-\.]+/) || (($c = substr($nm, 0, 1)) eq '.') || ($c eq '-') || (index($nm, '..') != -1) );
}

# Pass a user entered that has already been validated by using notPhone
# and trimmed using trim function. This function strips '(', ')', '-'
# and space characters like tab, blank etc. For instance following strings
# are passed as input and the respective output is shown
# Input                     Output
# "(408)736-5407"           4087365407
# "(408-736-5407"           4087365407
# "408-736-5407"            4087365407
# "1-408-736-5407"          14087365407
# "408 - 736 - 5407"        4087365407
sub getPhoneDigits {
   my($pd) = @_;
   $pd =~ s/\(//g;
   $pd =~ s/\)//g;
   $pd =~ s/\s//g;
   $pd =~ s/\-//g; 
   return $pd;
}

sub notNumeric {
  my($num) = @_;

  return ($num =~ /[^\d]+/);
}

sub notSkyTelPin {
   my($pin) = @_;

   #($pin, $suffix) = split ",", $pin;
   $digits = getPhoneDigits $pin;
   return ((notNumeric $digits) || ((length $digits) != 7));
}

sub notAirTouchPin {
   my($pin) = @_;
   $digits = getPhoneDigits $pin;
   return 1 if (notNumeric $digits);
   return 1 if ((length $digits) ne 11);
   $fd = substr $digits, 0, 1;
   return 1 if ($fd ne "1");
   return 0;
}

sub notPageMartPin {
   my($pin) = @_;
   $digits = getPhoneDigits $pin;
   return 1 if (notNumeric $digits);
   return 1 if (((length $digits) ne 10) && ((length $digits) ne 7));
   return 0;
}

sub notNextelPin {
   my($pin) = @_;
   $digits = getPhoneDigits $pin;
   return 1 if (notNumeric $digits);
   return 1 if ((length $digits) ne 10);
   return 0;
}

sub notEmailAddress {
   my($email) = @_;

   if ($email =~ /\s/) {
      return 1;
   }
   ($user, $domain) = split '@', $email;
   if (((trim $user) eq "") || ((trim $domain) eq "")) {
      return 1;
   }
   ($sub, $dom) = split '\.', $domain;
   if (((trim $sub) eq "") || ((trim $dom) eq "")) {
      return 1;
   }
   return ((index $email, '@') == -1);
   return 0;
}


# This function returns the area code given the number. This function 
# assumes that the phone number is already validated, trimmed, and 
# a getPhoneDigits is already called on it.
# Input                     Output
# "14087365407"             408
# "4087365407"              408
sub getAreaCode {
   my($pd) = @_;
   $fd = substr $pd, 0, 1;
   if ($fd eq "1") { 
      return substr $pd, 1, 3;
   }
   return substr $pd, 0, 3;
}

# This function returns the middle three digits given the number. This function 
# assumes that the phone number is already validated, trimmed, and 
# a getPhoneDigits is already called on it.
# Input                     Output
# "14087365407"             736
# "4087365407"              736
sub getPhoneMiddleDigits {
   my($pd) = @_;
   $fd = substr $pd, 0, 1; 
   if ($fd eq "1") {
      return substr $pd, 4, 3;
   }
   return substr $pd, 3, 3;
}

# This function returns the final four digits given the number. This function
# assumes that the phone number is already validated, trimmed, and 
# a getPhoneDigits is already called on it.
# Input                     Output
# "14087365407"             5407
# "4087365407"              5407
sub getPhoneEndDigits {
   my($pd) = @_;
   $fd = substr $pd, 0, 1;
   if ($fd eq "1") {
      return substr $pd, 7, 4;
   }
   return substr $pd, 6, 4;
}

# This function returns the fax number in FaxSav format. This function
# assumes that the phone number is already validated, trimmed, and 
# a getPhoneDigits is already called on it.
# Input                     Output
# "14087365407"             1-408-736-5407
# "4087365407"              1-408-736-5407
sub getFaxSavUSPhoneDigits {
   my($pd) = @_;
   $ad = getAreaCode $pd;
   $md = getPhoneMiddleDigits $pd;
   $ld = getPhoneEndDigits $pd;
   $pd = '1-' . $ad . '-' . $md . '-' . $ld;
}

sub multselkeys {
   my($input, $argmatch) = @_;
   $option = "";
   (@pairs) = split '&', $input;
   foreach $pair (@pairs) {
     ($name, $value) = split '=', $pair;
     if ($name eq $argmatch) {
        $option .= ' ' . $value;
     }
   }
   return $option;
}

sub multsel {
   my(%arginput, $argmatch) = @_;
   hddebug "argmatch = $argmatch";
   hddebug "arginput = $arginput";
   foreach $key (sort keys(%arginput)) {
      hddebug "Comparing $key with $argmatch";
      if ((index $key, $argmatch) == 0) {
        foreach (split("\0", $arginput{$key})) {
          ($out = $_) =~ s/\n//g;
          $output .=  " $out";
        }
      }
   }
   return $output;

 #$output =  "\n<dl compact>\n";
   #foreach $key (sort keys(%input)) {
   #  if ((index $key, "pgroups") == 0) {
   #     foreach (split("\0", $input{$key})) {
   #       ($out = $_) =~ s/\n/<br>\n/g;
   #       $output .=  "<dt><b>$key</b>\n <dd>:<i>$out</i>:<br>\n";
   #     }
   #  }
   #}
#   $output .=  "</dl>\n";
#   print $output;
}


# this function takes seconds 
# returns mon, year, day in gmtime. 

sub getMoYrDy {
   my($sec) = @_;
   #print "getMoYrDy seconds = $sec \n";
   ($s, $m, $h, $day, $mon, $year, $wday, $yday, $isdst) = gmtime($sec);
   $mon = $mon + 1; 
   #hddebug "day = $day";
   (@values) = ($mon, $year, $day, $wday);
   #hddebug "h = $h";
   #hddebug "m = $m";
   #print "month =  $mon\n";
   #print "year =  $year\n";
   #print "day = $day\n";
   #print "wk =  $wday\n";

   ($gmapt_mon, $gmapt_year, $gmapt_day, $gmapt_wk) = (@values);
   #hddebug "gmapt_day = $gmapt_day";
   return @values;
}

sub getGmValues {
   my($sec) = @_;
   ($s, $m, $h, $day, $mon, $year, $wday, $yday, $isdst) = gmtime($sec);
   $mon = $mon + 1; 
   (@values) = ($mon, $year, $day, $wday, $h, $m);

   ($gmapt_mon, $gmapt_year, $gmapt_day, $gmapt_wk, $gmapt_h, $gmapt_m) = (@values);
   return @values;
}

# this takes input as apptsec, apptmin, appthour, appttimezone
# takes current month, current day, current year, current wday, current yday
sub getdailyEtime {
   ($apptsec, $apptmin, $appthour, $appttz) = @_;
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time()); 
   #print "Start getDailyETime\n";
   #print "apptsec = $apptsec\n";
   #print "apptmin = $apptmin\n";
   #print "appthour = $appthour\n";
   #hddebug  "mday = $mday\n";
   $year += 1900;
   $mon += 1;
   #hddebug "mon = $mon\n";
   #hddebug "year = $year\n";
   #print "wday = $wday\n";
   #print "yday = $yday\n";
   #print "isdst = $isdst\n";
   #print "appttz = $appttz\n";
   #print "End getDailyETime\n";

   $etime = etimetosec($apptsec, $apptmin, $appthour, $mday, $mon, $year, "", "", "", $appttz);
   return $etime;
}

# this function takes seconds
# returns Min, Hours in gmtime.

sub getMinHour {

   my($tzone) = @_;
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
   $ctm = timegm($sec, $min, $hour, $mday, $mon, $year);
   $utm = $ctm + (tzone * 3600);

   ($s, $m, $h, $day, $mon, $year, $wday, $yday, $isdst) = gmtime($utm);

   if (($m > 0) && ($m <= 9)) {
	$m = 10;
   }

   if (($m >= 11) && ($m <= 19)) {
	$m = 20;
   }

   if (($m >= 21) && ($m <= 29)) {
	$m = 30;
   }

   if (($m >= 31) && ($m <= 39)) {
	$m = 40;
   }

   if (($m >= 41) && ($m <= 49)) {
	$m = 50;
   }

   if (($m >= 51) && ($m <= 59)) {
	$m = 0;
	$h = $h + 1;
   }

   (@values) = ($m, $h);
   #print "minutes =  $m\n";
   #print "hour =  $hour\n";

   ($gmapt_min, $gmapt_hour) = (@values);
   return @values;
}

sub sortrep {
  my($lflag, $name) = @_;
  $alph = substr $name, 0, 1;
  $alph = $alph . '-index';
  if ($lflag ne "") {
     tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alph/$name/appttab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
           'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
  } else {
     tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$name/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

  }
  foreach $entryno (sort keys %appttab) {
    #hddebug "entryno = $entryno";
    if ((trim $entryno) eq "") {
       next;
    }
    #hddebug "entryno = $entryno";
    if (!exists $appttab{$entryno}) {
       next;
    }
    if ($appttab{$entryno}{meridian} eq "PM") {
       $hour = $appttab{$entryno}{hour} + 12;
    } else {
       $hour = $appttab{$entryno}{hour};
    }
    #hddebug "month = $appttab{$entryno}{month}";
    #hddebug "day = $appttab{$entryno}{day}";
    #hddebug "min = $appttab{$entryno}{min}";
    system "echo \"$appttab{$entryno}{month} $appttab{$entryno}{day} $hour $appttab{$entryno}{min} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 +3.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$5}'};
     system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);  
}

sub sortmemo {
  my($name) = @_;

  hddebug "name = $name";
  $alph = substr $name, 0, 1;
  $alph = $alph . '-index';
  hddebug "alph = $alph";
  system "mkdir  -p $ENV{HDDATA}/$alph/$name/todotab";
  tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alph/$name/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };

  foreach $entryno (sort keys %todotab) {
    if ((trim $entryno) eq "") {
       next;
    }
    if (!exists $todotab{$entryno}) {
       next;
    }
    #system "echo \"$todotab{$entryno}{month} $todotab{$entryno}{day} $todotab{$entryno}{year} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
    system "echo \"$todotab{$entryno}{priority} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     #system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$2}'};
     system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);
}

sub sortgroupmemo {
  my($name) = @_;

  if (! -d "$ENV{HDDATA}/listed/groups/$name/todotab") {
     system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$name/todotab";
  }

  # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$name/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };

  foreach $entryno (sort keys %todotab) {
    if ((trim $entryno) eq "") {
       next;
    }
    if (!exists $todotab{$entryno}) {
       next;
    }
    #system "echo \"$todotab{$entryno}{month} $todotab{$entryno}{day} $todotab{$entryno}{year} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
    system "echo \"$todotab{$entryno}{priority} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     #system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$2}'};
     system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  #system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);
}


sub sortmemodate {
  my($name) = @_;

  $alph = substr $name, 0, 1;
  $alph = $alph . '-index';
  tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/$alph/$name/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };

  foreach $entryno (sort keys %todotab) {
    if ((trim $entryno) eq "") {
       next;
    }
    if (!exists $todotab{$entryno}) {
       next;
    }
    system "echo \"$todotab{$entryno}{month} $todotab{$entryno}{day} $todotab{$entryno}{year} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
    #system "echo \"$todotab{$entryno}{priority} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     #system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$4}'};
     system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);
}

sub sortgroupmemodate {
  my($name) = @_;

  if (! -d "$ENV{HDDATA}/listed/groups/$name/todotab") {
     system "/bin/mkdir -p $ENV{HDDATA}/listed/groups/$name/todotab";
  }
  # bind group appt table vars
      tie %todotab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$name/todotab",
      SUFIX => '.rec',
      SCHEMA => {
           ORDER => ['entryno', 'login', 'subject', 'desc', 'month',
           'day', 'year', 'meridian', 'priority', 'status', 'share',
           'hour', 'banner'] };

  foreach $entryno (sort keys %todotab) {
    if ((trim $entryno) eq "") {
       next;
    }
    if (!exists $todotab{$entryno}) {
       next;
    }
    system "echo \"$todotab{$entryno}{month} $todotab{$entryno}{day} $todotab{$entryno}{year} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
    #system "echo \"$todotab{$entryno}{priority} $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     #system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$4}'};
     system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  #system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);
}

sub sortcontacts {
  my($name, $g) = @_;

  $alph = substr $name, 0, 1;
  $alph = $alph . '-index';
  if ($g eq "") {
     # bind address table vars
     tie %addrtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/$alph/$name/addrtab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };
  } else {
     # bind address table vars
     tie %addrtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/addrtab",
     SUFIX => '.rec',
     SCHEMA => {
        ORDER => ['entryno', 'login', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

     $name = $g;
  }

  foreach $entryno (sort keys %addrtab) {
    if ((trim $entryno) eq "") {
       next;
    }
    if (!exists $addrtab{$entryno}) {
       next;
    }
    $fname = $addrtab{$entryno}{fname};
    if ($fname eq "") {
       $fname = "a";
    }
    $fname =~ s/\s//g;
    $lname = $addrtab{$entryno}{lname};
    if ($lname eq "") {
       $lname = "a";
    }
    $lname =~ s/\s//g;
    $busname = $addrtab{$entryno}{busname};
    if ($busname eq "") {
        $busname = "a";
    }
    $busname =~ s/\s//g;
    system "echo \"$fname $lname $busname $entryno\" >> $ENV{HDHOME}/tmp/sort$$-$name";
  }
  $outfile = "$ENV{HDHOME}/tmp/sortout$$-$name";
  if (-f "$ENV{HDHOME}/tmp/sort$$-$name") {
     #system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     system "cat $ENV{HDHOME}/tmp/sort$$-$name | sort -n +0.0 +1.0 +2.0 > $outfile";
     $replist = qx{cat $outfile | awk '{print \$4}'};
     #system "rm -f $outfile";
     (@replist1) = split '\n', $replist;
  }
  #system "rm -f $ENV{HDHOME}/tmp/sort$$-$name";
  return (@replist1);
}

sub isstd {

   my($zone) = @_;

   if ($zone == -1) {
      return 1;
   }

   # STD
   if ($zone == 2) {
      return 1;
   }

   if ($zone == 3) {
      return 1;
   }

   # STD
   if ($zone == -11) {
      return 1;
   }

   # STD
   if ($zone == -10) {
      return 1;
   }

   # STD
   if ($zone == -4) {
        return 1;
   }

   # don't know assume STD
   if ($zone == -3.5) {
        return 1;
   }

   # STD
   if ($zone eq "-3B") {
        return 1;
   }

   # STD
   if ($zone eq "-3A") {
        return 1;
   }

   # STD
   if ($zone eq "3S") {
        return 1;
   }

   # STD
   if ($zone == 4) {
        return 1;
   }

   #  STD
   if ($zone == 5.5) {
        return 1;
   }

   # STD
   if ($zone == 6) {
        return 1;
   }

   # STD
   if ($zone eq "7T") {
        return 1;
   }

   # STD
   if ($zone eq "7V") {
        return 1;
   }

   # STD
   if ($zone eq "7I") {
        return 1;
   }

   # STD
   if ($zone eq "8C") {
        return 1;
   }
   # STD
   if ($zone eq "8S") {
        return 1;
   }

   # STD
   if ($zone eq "8T") {
        return 1;
   }

   # STD
   if ($zone eq "9J") {
        return 1;
   }

   # STD
   if ($zone eq "9K") {
        return 1;
   }

   #  STD
   if ($zone == 9.5) {
        return 1;
   }

   # STD
   if ($zone == 10) {
        return 1;
   }
   # STD
   if ($zone eq "12F") {
        return 1;
   }
   # STD
   if ($zone eq "12N") {
        return 1;
   }

   return 0;
}

sub goodwebstr {
   my($str) = @_;

   $str = normalizeurlparmvalue($str);
# replacing space below also damages CRLF (\r\n). Hence we first
# replace those with %0d%0a in upper function.
   $str =~ s/ /%20/g;
   return $str;
}

sub normalizeurlparmvalue {
   my($ur) = @_;
   $ur =~ s/\&/%26/g;
   $ur =~ s/\|/%7c/g;
   $ur =~ s/\'/%27/g;
   $ur =~ s/\=/%3d/g;
   $ur =~ s/\?/%3f/g;
   $ur =~ s/\;/%3b/g;
   $ur =~ s/\#/%23/g;
   $ur =~ s/\:/%3a/g;
   $ur =~ s/\//%2f/g;
   $ur =~ s/\r\n/%0d%0a/g;
# extra stuff
   $ur =~ s/\)/%29/g;
   $ur =~ s/\(/%28/g;
   $ur =~ s/\#/%2a/g;
   $ur =~ s/\+/%2b/g;
   $ur =~ s/\,/%2c/g;
   $ur =~ s/\-/%2d/g;
   $ur =~ s/\./%2e/g;
   $ur =~ s/\>/%3e/g;
   $ur =~ s/\</%3c/g;
   $ur =~ s/\"/%22/g;
   $ur =~ s/\!/%21/g;
   $ur =~ s/\~/%7e/g;
   $ur =~ s/\{/%7b/g;
   $ur =~ s/\}/%7d/g;
   $ur =~ s/\[/%5b/g;
   $ur =~ s/\\/%5c/g;
   $ur =~ s/\]/%5d/g;
   $ur =~ s/\_/%5f/g;
   $ur =~ s/\^/%5e/g;
   return $ur;
}

sub encurl {
   my($ur) = @_;
   $ur = encode_base64 $ur, "";
   $ur =~ s/=/aaaa/g; 
   return $ur;
}

sub depositmoney {
   my($login) = @_;

   tie %moneytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/moneytab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'account', 'comment', 'approved'] };

   if (!exists $moneytab{$login}) {
      $moneytab{$login}{login} = $login;
   }
   $moneytab{$login}{account} = $moneytab{$login}{account} + $ENV{HDREWARD};
   tied(%moneytab)->sync();
}

sub withdrawmoney {
   my($login) = @_;

   tie %moneytab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/moneytab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'account', 'comment', 'approved'] };

   if (!exists $moneytab{$login}) {
      $moneytab{$login}{login} = $login;
   }
   #$moneytab{$login}{account} = $moneytab{$login}{account} - $ENV{HDREWARD};
   $moneytab{$login}{account} = $moneytab{$login}{account} - 1;
   if ($moneytab{$login}{account} < 0) {
      $moneytab{$login}{account} = 0;
   }
   tied(%moneytab)->sync();
}

sub statuscat {
   my($doc) =@_;

   statuss "The document you requested, could not be created. Please use the <b>Back</b> button of your browser, and try again. If the problem recurs, please contact hotdiary.com";
}

sub wrapstr {
   my($str, $len) = @_;
   $str =~ s/<BR>//g;
   $str =~ s/<br>//g;
   $str =~ s/\r//g;
   $str =~ s/\n//g;
   $totlen = length($str);
   $intr = $totlen / $len;
   my $tostr = "";
   for ($i = 0; $i < $intr; $i++) {
      $tostr .= ((substr $str, ($i * $len), $len) . "<BR>");
   }
   return $tostr;
   
}

sub hdsystem {
   my($cmd) = @_;

   $! = "";
   hddebug "Executing cmd = $cmd";
   system $cmd;
   $retcode = $?;
   if ($retcode != 0) {
      hddebug "ERROR in hdsystem ($retcode): $cmd";
   }
   return $retcode;
}

sub hdsystemcat {
   my($cmd) = @_;

   system "cat $ENV{HDTMPL}/content.html";
   $! = "";
   hddebug "catting file $cmd";
   system "cat $cmd";
   $retcode = $?;
   hddebug "retcode = $retcode";
   if ($retcode != 0) {
      hddebug "ERROR in hdsystemcat ($retcode): $cmd";
      statuscat $cmd;
      exit;
   }
   return $retcode;
}


sub getlogin {
   
   my($hdcookie) = @_;
   ($hdfirststr, $hdsecondstr, $hdthirdstr) = split ";", $hdcookie;

   if ($hdfirststr =~ /hdlogin/) {
      ($hdname, $login) = split "=", $hdfirststr;
   } else {
      if ($hdsecondstr =~ /hdlogin/) {
          ($hdname, $login) = split "=", $hdsecondstr;
      } else {
          ($hdname, $login) = split "=", $hdthirdstr;
      }
   }
   return $login;
}

sub getbiscuit {

   my($hdcookie) = @_;
   ($hdfirststr, $hdsecondstr, $hdthirdstr) = split ";", $hdcookie;

   if ($hdfirststr =~ /biscuit/) {
      ($biscuitlabel, $biscuit) = split "=", $hdfirststr;
   } else {
      if ($hdsecondstr =~ /biscuit/) {
         ($biscuitlabel, $biscuit) = split "=", $hdsecondstr;
      } else {
         ($biscuitlabel, $biscuit) = split "=", $hdthirdstr;
      }
   }
   return $biscuit;

}

sub gethdvisitor {

   my($hdcookie) = @_;
   ($hdfirststr, $hdsecondstr, $hdthirdstr) = split ";", $hdcookie;

   if ($hdfirststr =~ /hdvisitor/) {
      ($biscuitlabel, $visitor) = split "=", $hdfirststr;
   } else {
      if ($hdsecondstr =~ /visitor/) {
         ($biscuitlabel, $visitor) = split "=", $hdsecondstr;
      } else {
         ($biscuitlabel, $visitor) = split "=", $hdthirdstr;
      }
   }
   return $visitor;

}

sub validvdomain {
   my($vdomain) = @_;
   if (
         ("hotdiary.com" eq "\L$vdomain") ||
         ("hotdiary.org" eq "\L$vdomain") ||
         ("hotdiary.net" eq "\L$vdomain") ||
         ("mydowntown.net" eq "\L$vdomain") ||
         ("portalserver.net" eq "\L$vdomain") ||
         ("www.hotdiary.com" eq "\L$vdomain") ||
         ("www.hotdiary.org" eq "\L$vdomain") ||
         ("www.mydowntown.net" eq "\L$vdomain") ||
         ("www.portalserver.net" eq "\L$vdomain") ||
         ("www.hotdiary.net" eq "\L$vdomain")
      ) {
      return "1";
   }
   return "0";
}


# takes input gmtime and timezone of the user
# converts gmtime to users time in its timezone
sub getuserstime {
   ($etime, $tz) = @_;
   $ctm = $etime + ( tz * 3600);
   return($ctm);
}

sub gethiddenvars {

   ($hiddenvars) = @_;
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
   return ($hiddenvars);
}

sub getsessionheader {

  ($jp) = @_;
  $sessionheader = "";

  if ($jp eq "") {
     $sessionheader = qx{cat $ENV{'HTTPJAVAHOME'}/sessionheader.html};
     $sessionheader = adjusturl $sessionheader;
  }
  return $sessionheader;
}

sub getsessionfooter {

  ($jp) = @_;
  $sessionfooter = "";
  if ($jp eq "") {
     $sessionfooter = qx{cat $ENV{'HTTPJAVAHOME'}/sessionfooter.html};
     $sessionfooter = adjusturl $sessionfooter;
  }
  return $sessionfooter;
}

sub getcss {

  ($jp) = @_;
  $css = "";
  if ($jp eq "") {
     $css = qx{cat $ENV{HTTPJAVAHOME}/css.html};
     $css = adjusturl $css;
  }
  return $css;
}

##
## these three methods are used for jiveit logo and title and to disable hotdiary's label and logo.
##

sub getTheader {
   ($jp) = @_;
   if ($jp ne "") {
      return adjusturl "<CENTER><TABLE VALIGN=TOP WIDTH=100%><TR VALIGN=TOP><TD ALIGN=LEFT WIDTH=15%>";
   } else {
      return "";
   }
}

sub getTmiddle {
   ($jp) = @_;
   if ($jp ne "") {
      return adjusturl "</TD><TD ALIGN=CENTER WIDTH=85%> <FONT color=black SIZE=2><b>";
   } else {
      return "";
   }
}

sub getTfooter {
   ($jp) = @_;
   if ($jp ne "") {
      return adjusturl "</b></FONT></TD></TR></TABLE></CENTER>";
   } else {
      return "";
   }
}


1;

__END__

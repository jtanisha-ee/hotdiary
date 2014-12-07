package calfuncs::calfuncs;
require Exporter;
require "flush.pl";
#require "cgi-lib.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use calutil::calutil;
use calfuncs::bizfuncs;


@ISA = qw(Exporter);
@EXPORT = qw(publishEventNew);

sub publishEventNew {

   my($prml, $vwtype, $f, $a, $cmonth, $cday, $cyear, $h, $m, $lg, $url, $en, $sc, $group) = @_;

    $alphaindex = substr $lg, 0, 1;
    $alphaindex = $alphaindex . '-index';

   # bind personal appt table vars
   tie %appttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/$alphaindex/$lg/appttab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free', 
	'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };

    $lflag = 1;
    $name = $lg;

    if ($group ne "") {
       $lflag = "";
       $name = $group;
    }

    (@entrynohsh) = sortrep($lflag, $name);

    foreach $entryno (@entrynohsh) {
       #hddebug ("hash number = $entryno");
       if ($entryno eq "") {
          next;
       }
       if (!exists($appttab{$entryno})) {
          next;
       }

       $month = trim $appttab{$entryno}{'month'};
       $year = trim $appttab{$entryno}{'year'};
       if ($cmonth ne $month) {
          next;
       }
       if ($cyear ne $year) {
          next;
       }                                        

       $monstr = getmonthstr($month);
       $wday = getWeekDayIndex($aptttab{$entryno}{day}, $month, $year);
       $daystr = getdaystr($wday);

       $msg = "<TR>";
       $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$monstr $appttab{$entryno}{day}</FONT>";
       $min100 = trim $appttab{$entryno}{min};
       if (($appttab{$entryno}{hour} < 10) && ($appttab{$entryno}{meridian} eq "AM")) {
          $msg .= "<FONT FACE=\"Verdana\" SIZE=\"2\">$appttab{$entryno}{hour}:$min100 $appttab{$entryno}{meridian}</FONT>";   
      } else {
          $msg .= "<FONT FACE=\"Verdana\" SIZE=\"2\">$appttab{$entryno}{hour}:$min100 $appttab{$entryno}{meridian}</FONT>";   
      } 
       if (($appttab{$entryno}{subject}) eq "") {
          $subject = $appttab{$entryno}{dtype};
       } else {
          $subject = $appttab{$entryno}{subject};
       }               

       $desc = $appttab{$entryno}{desc};

       $burlhref1 = "<CENTER><a href=\"/cgi-bin/execshowcevent.cgi?group=$group&en=$entryno&login=$login\">$subject</a> <BR>$desc <BR>$hour $min $meridian <BR> $imgurl$addeventtop </CENTER>";         

       #$slink = createSubjectLink($appttab{$entryno}{dtype}, $entryno, $url, $hour, $min100, $appttab{$entryno}{meridian}, $appttab{$entryno}{day}, $month, $year,$f, $vwtype, $free, $subject, $jvw, $group, $lg, $desc, "p");

       $msg .= "<FONT FACE=\"Verdana\" SIZE=\"2\">$slink</FONT>";
       $msg .= "<FONT FACE=\"Verdana\" SIZE=\"2\">&nbsp;$desc</FONT></TD></TR>";
    }
    $msg = adjusturl ($msg);
    $prml = strapp $prml, "matter=$msg";
    return $prml;
}

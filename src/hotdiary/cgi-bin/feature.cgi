#!/usr/bin/perl

require "cgi-lib.pl";
use tparser::tparser;
use utils::utils;

&ReadParse(*input);
system "cat \"$ENV{HDTMPL}/content.html\"";
$fcomp = $input{fcomp};
#hddebug "fcomp = $fcomp";
$biscuit = $input{biscuit};
#hddebug "biscuit = $biscuit";
#hddebug "rh = $input{rh}";
#hddebug "hs = $input{hs}";
#hddebug "vdomain = $input{vdomain}";

$prml = 0;
$prml = strapp $prml, "template=$ENV{HDTMPL}/feature.html";
$prml = strapp $prml, "templateout=$ENV{HDHREP}/manoj/feature.html";
$rh = $input{rh};
$prml = strapp $prml, "rh=$rh";
$prml = strapp $prml, "fcomp=$fcomp";
$prml = strapp $prml, "login=$login";
$hiddenvars = "<INPUT TYPE=HIDDEN NAME=pnum VALUE=5>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"execfeature.cgi\">";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=fcomp>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=submit>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=login>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=3>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
$hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
$hiddenvars = adjusturl $hiddenvars;
$prml = strapp $prml, "hiddenvars=$hiddenvars";
parseIt $prml;

system "cat \"$ENV{HDHREP}/manoj/feature.html\"";

#!/usr/bin/perl

use tparser::tparser;
use utils::utils;

$biscuit = "biscuit-12345-test";
# get this as input
$rh = "calendar";
# the function name
# the parameter names
# the parameter values
# the pnum 

$hidden = "<input type=hidden name=p0 size=\"-1\" value=\"/cgi-bin/execshowbg.cgi\">";
$hidden .= "<input type=hidden name=p1 size=\"-1\" value=\"biscuit\">";
$hidden = adjusturl $hidden;
$prml = "";
$prml = strapp  $prml, "biscuit=$biscuit";
$prml = strapp  $prml, "pnum=2";
$prml = strapp  $prml, "rh=$rh";
$prml = strapp $prml, "hidden=$hidden";
$prml = strapp $prml, "template=$ENV{HDTMPL}/hdshowbizbg.html";
$prml = strapp $prml, "templateout=/tmp/genericout";
parseIt $prml;

#print $prml;
 

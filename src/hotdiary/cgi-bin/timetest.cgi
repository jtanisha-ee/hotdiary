#!/usr/bin/perl

use Time::Local;

$timesec = timegm 0, 0, 10, 14, 5, 1999, "", "", "";
#$wday = (qw(Thu Fri Sat Sun Mon Tue Wed))[(gmtime $timesec)[6]];
$wday = (gmtime $timesec)[6];
print "wday = $wday\n";

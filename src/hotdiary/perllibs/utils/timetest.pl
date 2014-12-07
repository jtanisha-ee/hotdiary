#!/usr/local/bin/perl

use Time::Local;

$msg = localtime(time());
print "localtime = ", $msg, "\n";

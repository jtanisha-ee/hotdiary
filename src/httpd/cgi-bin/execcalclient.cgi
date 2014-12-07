#!/bin/ksh

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


. /usr/local/hotdiary/config/hd.env
##export PATH=$PATH:/usr/local/bin:/usr/gnu/bin
export PERL5LIB=$HDHOME/perllibs
if [ $REMOTE_ADDR = "63.168.86.93" ]; then
   sleep 3000
   exit
fi
perl $HDCGI/calclient.cgi

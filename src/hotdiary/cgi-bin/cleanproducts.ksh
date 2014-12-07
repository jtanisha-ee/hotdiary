#!/bin/ksh

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: cleanproducts.ksh
# Purpose: it cleans products file so it cannot be downloaded twice
# Creation Date: 02-16-2000
# Created by: Smitha Gudur
#

wfile=$1
sleeptime=$2
if [ "$sleeptime" == "" ]; then
   sleeptime=30
fi

echo "`date`: Sleeping $sleeptime seconds before removing $wfile" >> $HDHOME/logs/hddebug.log
sleep $sleeptime
sz=`cat $wfile | wc -c | tr -d " "`
rm -f $wfile
echo "`date`: Removed ($sz bytes) $wfile" >> $HDHOME/logs/hddebug.log

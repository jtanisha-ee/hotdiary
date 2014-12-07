#!/bin/ksh

# (C) Copyright 1998-1999 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


# FileName: execdoeditprivatecal.cgi
# Purpose: it invokes doeditprivatecal.cgi

#. /usr/local/hotdiary/franchise/franchise.env
ENVFILE=/usr/local/hotdiary/jazzit_env/$SERVER_NAME.env
if [ -f $ENVFILE ]; then
. $ENVFILE
else
   echo "Content-type: text/html"
   echo
   echo
   echo "<HTML><BODY BGCOLOR=ffffff><FONT FACE="Verdana" SIZE=5 COLOR=ff0000>Did not find the file $ENVFILE. Please check the installation and INSTALL.README.</FONT></BODY></HTML>"
fi

$HDHOME/doeditprivatecal.cgi

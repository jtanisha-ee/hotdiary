#!/bin/ksh

if [ $# -ne 1 ]; then
   echo "Usage: $0 <file-name>"
   exit 1
fi

if [ -z $TDATALOG ]; then
   echo "Environment variable TDATALOG (directory where the ftp log file resides) has not been set. Please check the installation, or set the variable on the command line, if you are executing this program from command line."
   exit 1
fi

FTPHISTLOG=$TDATA_LOGFILE
FTPLOG=$TDATATMP/mibftp$$.log

tfile=$1

echo > $FTPLOG
echo "***** Begin Transfer Of File $tfile *****" >> $FTPLOG
date >> $FTPLOG
ftp -inv mibsfp01 1>>$FTPLOG 2>&1 << eof
user mibftp devftp999
bin
cd /dbload/ftp/easevt
put $tfile
quit
eof

#use this for testing
#echo > $FTPLOG
#echo "***** Begin Transfer Of File $tfile *****" >> $FTPLOG
#date >> $FTPLOG
#ftp -inv ibomllow15 1>>$FTPLOG 2>&1 << eof
#user mjoshi xxxxxx
#put $tfile
#quit
#eof

egrep -e "Transfer complete" $FTPLOG 2>&1 >/dev/null

status=0

if [ $? = 0 ]; then
   echo "File $tfile has been successfully transferred."
   echo "**********************************************"
   status=0
else
   echo "Error occurred while transferring file $tfile. Here's the log:"
   cat $FTPLOG
   echo "**************************************************************"
   status=1
fi

cat $FTPLOG >> $FTPHISTLOG
if [ $? != 0 ]; then
   echo "Failed to concatenate temporary log file $FTPLOG to $FTPHISTLOG. Saving copy of $FTPLOG for emergency use."
   exit $status
fi
rm -f $FTPLOG
if [ $? != 0 ]; then
   echo "Failed to remove temporary log file $FTPLOG."
fi
exit $status


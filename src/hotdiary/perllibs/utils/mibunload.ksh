#!/bin/ksh
#  Instance:            1
#  %version:            4 %
#  Description:
#  %created_by:         mjoshi %
#  %date_created:       Fri Dec 22 14:24:36 2000 %

# File: mibunload.ksh
# Depends On: INFORMIXDIR, INFORMIXSERVER
# Initial Version: mjoshi
#
# Execution: Must be executed with fully qualified path name from
# a cron script.
#
# Directory structure:
# 
#     $APPLROOT/$APPLICATION/rt_$RUNTIME/mib/
# Need to install atleast the scripts in the bin directory
#                                             bin/
#                                                mibunload.ksh
#                                                eventunload.pl
#                                                tdatautils.pm
#                                                mibftp.ksh
#
# The sql directory and stored procedure needs to be installed
# using the dbinit procedure. We store it here for reference.
#                                             sql/
#                                                insertchangeaidbatch.sp.sql
#                                                inserteventbatch.sp.sql
#                                                insertcustacctsbatch.sp.sql
#                                                insertonlineidbatch.sp.sql
#                                                insertcustprofilebatch.sp.sql
# The following directories will be automatically created
#                                             log
#                                             tmp
#                                             unload
#                                             archive
#
# Description: 
#
# This is the master script and will be executed by cron typically
# once a month beginning on the first day of the month. All design
# details are described in the design document at:
#    http://ibomllow7.bankamerica.com:8000/teradata.html
# 
# Here are a few implementation details:
# 1. The "log" directory contains the log file mibunload.log. It
#    contains the history of all the extraction, conversion, and
#    file transfer activity.
# 2. The "tmp" directory is a work area for all scripts. Typically
#    all files are cleaned after the scripts finish.
# 3. The "unload" directory is used to store a freshly generated
#    mib unload (*.unl) file. This file will be archived and deleted
#    if the file transfer succeeds. If the transfer fails, this file
#    can be examined for manual diagnostics. 
# 4. The "archive" directory is used to stored the archived (tar+gz)
#    files whose uncompressed versions were successfully transferred.
#
# Issues:
#
# 1. Need to insert the date into the naming scheme of generated
#    mib unload files.
# 2. Need to pass the correct start and end dates as arguments to
#    the stored procedure.
# 3. Need to examine the return code of dbaccess call to execute
#    stored procedure. Currently we are only checking for "0" row output.
# 4. Need the password for the login account SFBAT1. Apparently the
#    the current password is not correct as per Patricia Thomas's email.
# 5. Need confirmation on date format from Patricia.


[[ "$PATH" = "" ]] && export PATH=/usr/bin:/bin:/usr/local/bin:.
export PATH=`cd $(dirname $0); /usr/bin/pwd`:.:$PATH

# Commenting out below since, env.sh is not available on prod db system
#fatal()
#{
#    echo $*; exit 1
#}
#APPLICATION=${APPLICATION:-jrun}
#ENVFILE=${ENVFILE:-env.sh}
#. /apps/runtime/bin/env.sh "$@" || {
#    echo "Error:  env.sh failed.  Possible cause env.sh is not in \$PATH"
#    exit 1
#}

#if [[ ! -d $CDIR ]] ; then
#    fatal "Directory $CDIR not found"
#fi

if [ $# != 1 ]; then
   echo "Usage: $0 <event|changeaid|custaccts|custprofile|onlineid>"
   exit 1
fi

export UNLOAD_TYPE=$1

if [ $UNLOAD_TYPE == "event" ]; then
   SCRIPTNAME=eventunload.pl
else if [ $UNLOAD_TYPE == "changeaid" ]; then
   SCRIPTNAME=changeaidunload.pl
else if [ $UNLOAD_TYPE == "custaccts" ]; then
   SCRIPTNAME=custacctsunload.pl
else if [ $UNLOAD_TYPE == "custprofile" ]; then
   SCRIPTNAME=custprofileunload.pl
else if [ $UNLOAD_TYPE == "onlineid" ]; then
   SCRIPTNAME=onlineidunload.pl
else   
   echo "Usage: $0 <event|changeaid|custaccts|custprofile|onlineid>"
   exit 1
fi
fi
fi
fi
fi

export RUNTIME=${RUNTIME:-`/usr/ucb/whoami`}

# informix variables
export INFORMIXDIR=${INFORMIXDIR:-/informix/current}
export PATH=${INFORMIXDIR}/bin:$PATH
export INFORMIXSERVER=${INFORMIXSERVER:-eas_dev_tcp};

# informix db
#export DBNAME=${DBNAME:-db_${RUNTIME}_eas@${INFORMIXSERVER}}
export DBNAME=$DB_NAME@$DB_TCP_SERVICE

# EAS start directories
export STARTDIR=${APPLROOT}/${APPLICATION}/rt_${RUNTIME}

# Mib Unload Home
export TDATAHOME=${STARTDIR}/mib

if [ ! -d ${TDATAHOME} ]; then
   mkdir -p ${TDATAHOME} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${TDATAHOME}"
      exit $? 
   fi 
fi

# The following need not be changed, as long as the TDATAHOME
# is set correctly.

export UNLOADDIR=${TDATAHOME}/unload
if [ ! -d ${UNLOADDIR} ]; then
   mkdir -p ${UNLOADDIR} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${UNLOADDIR}"
      exit $? 
   fi 
fi


export ARCDIR=${TDATAHOME}/archive
if [ ! -d ${ARCDIR} ]; then
   mkdir -p ${ARCDIR} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${ARCDIR}"
      exit $? 
   fi 
fi

export BINDIR=${TDATAHOME}
if [ ! -d ${BINDIR} ]; then
   mkdir -p ${BINDIR} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${BINDIR}"
      exit $? 
   fi 
fi

export TDATATMP=${TDATAHOME}/tmp
if [ ! -d ${TDATATMP} ]; then
   mkdir -p ${TDATATMP} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${TDATATMP}"
      exit $? 
   fi 
fi

export TDATALOG=${TDATAHOME}/log
if [ ! -d ${TDATALOG} ]; then
   mkdir -p ${TDATALOG} 1>/dev/null 2>&1
   if [ $? != 0 ]; then
      echo "FATAL: Could not make directory ${TDATALOG}"
      exit $? 
   fi 
fi

export TDATA_LOGFILE=$TDATAHOME/log/${UNLOAD_TYPE}.log

# Make sure the perl module can be found
export PERL5LIB=$BINDIR:$PERL5LIB

# Log header to log file
echo >> $TDATA_LOGFILE
echo "===================================================" >> $TDATA_LOGFILE
echo "MIB Unload Cron Process: `date`" >> $TDATA_LOGFILE
echo "===================================================" >> $TDATA_LOGFILE

# Call the extraction program. This program extracts or unloads the
# data for the previous month from the database.
if [ -f $BINDIR/$SCRIPTNAME ]; then
   $BINDIR/$SCRIPTNAME 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
   if [ $? != 0 ]; then
	  echo "FATAL: Extraction program failed." >> $TDATA_LOGFILE
	  exit $?
   fi
else
   echo "FATAL: Could not find program $BINDIR/$SCRIPTNAME. Please check installation." >> $TDATA_LOGFILE
   exit 1
fi

# Move output file to unload directory
outlist=`ls -1t $TDATATMP/*${UNLOAD_TYPE}*.unl 2>/dev/null`
if [ $? != 0 ]; then
   echo "No extracted files found in $TDATATMP. Check extraction program." >> $TDATA_LOGFILE
   exit $?
fi
totfile=`echo $outlist | wc -l`
firstfile=`echo $outlist | awk '{print $1}'`
if [ $totfile -gt 1 ]; then
   echo "Found more than one file ($totfile files) in directory $TDATATMP. Picking the most recent file ($firstfile)." >> $TDATA_LOGFILE
else 
   if [ $totfile -lt 1 ]; then
	  echo "No file found in source directory $TDATATMP." >> $TDATA_LOGFILE
	  exit 0
   fi
fi
integer cntfile=0
if [ -f $UNLOADDIR/$firstfile ]; then
   echo "WARNING: Source file name $TDATATMP/$firstfile conflicts with destination file name $UNLOADDIR/$firstfile. Skipping this file for now." >> $TDATA_LOGFILE
   c1sum=`sum $TDATATMP/$firstfile`
   c2sum=`sum $UNLOADDIR/$firstfile`
   if [ $c1sum -ne $c2sum ]; then
	  echo "WARNING: Source file $TDATATMP/$firstfile differs from destination file $UNLOADDIR/$firstfile. Skipping this file anyway." >> $TDATA_LOGFILE
   fi
fi
cntfile=$cntfile+1
mv $firstfile $UNLOADDIR 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE

echo "Moved $cntfile files successfully to $UNLOADDIR" >> $TDATA_LOGFILE

if [ $? != 0 ]; then
   echo "Extraction program failed. File transfer will not be invoked." >> $TDATA_LOGFILE
   exit $?
fi

# Call the file transfer program. This program transfers the converted
# file using ftp to the mib dest. system.

genfile=`basename $firstfile`
if [ ! -f $UNLOADDIR/$genfile ]; then
   echo "No file found in source directory $TDATATMP." >> $TDATA_LOGFILE
   exit 1
fi
if [ -f $BINDIR/mibftp.ksh ]; then
   cd $UNLOADDIR 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
   $BINDIR/mibftp.ksh $genfile 1>> $TDATA_LOGFILE 2>>$TDATA_LOGFILE
else 
   echo "FATAL: Could not find program $BINDIR/mibftp.ksh. Please check installation." >> $TDATA_LOGFILE
   exit 1
fi

if [ $? != 0 ]; then
   echo "File Transfer program failed. Could not transfer file $UNLOADDIR/$genfile to destination host." >> $TDATA_LOGFILE
   exit $?
fi

# Archive the generated and transferred file

cd $UNLOADDIR
tar -cvf $genfile.tar $genfile 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
if [ $? != 0 ]; then
   echo "Error occurred while generating tar file $genfile.tar" >> $TDATA_LOGFILE
   exit $?
fi

compress $genfile.tar 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
if [ $? -ne 0 ]; then
   echo "Error occurred while generating file $genfile.tar.Z" >> $TDATA_LOGFILE
   exit $?
fi

mv $genfile.tar.Z $ARCDIR 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
if [ $? != 0 ]; then
   echo "Error occurred while moving $genfile.tar.Z to $ARCDIR" >> $TDATA_LOGFILE
   exit $?
else
   echo "Successfully generated archive file $ARCDIR/$genfile.tar.Z" >> $TDATA_LOGFILE
fi

# Presently commented out for debugging
rm $genfile 1>>$TDATA_LOGFILE 2>>$TDATA_LOGFILE
if [ $? != 0 ]; then
   echo "Error occurred while removing file $UNLOADDIR/$genfile" >> $TDATA_LOGFILE
   exit $?
fi


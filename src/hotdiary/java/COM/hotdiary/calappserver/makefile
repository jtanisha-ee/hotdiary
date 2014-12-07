# $Id: makefile,v 1.1 1999/05/04 22:38:20 mjoshi Exp $
#
# Copyright (c) 1999 HotDiary Inc.
#
# This makefile has targets to checkout java files and jar files
# from the database, build them, and generate appropriate sami.jar
# file. This file can be committed back into CVS. The error output
# of cvs is appended to make.log in current directory.
#
# USAGE:
# To perform a fresh make of the latest stuff in CVS:
# 	make new
# To build what's already in your directory:
#	make

all : build

new : update build commit

sami.jar : build

update :
	cvs update .

build : intersolv SendPage.class AlarmDbLogger.class
	jar cvf sami.jar SendPage.class AlarmDbLogger.class intersolv 2>> make.log

commit :
	cvs commit -m "Rebuilding new sami.jar from makefile" sami.jar

SendPage.class : SendPage.java
	javac SendPage.java

AlarmDbLogger.class : AlarmDbLogger.java
	javac AlarmDbLogger.java

intersolv:
	jar xvf intersolv.jar 2>> make.log

clean:
	rm -f *.class sami.jar make.log

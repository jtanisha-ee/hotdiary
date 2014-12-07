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

all : $(HDHOME)/java/efisps.jar

$(HDHOME)/java/efisps.jar : $(HDHOME)/java/efi.jar ISPFeedServerImpl.class ISPFeedServerImpl_Skel.class
	cd $(HDHOME)/java && jar cvf $(HDHOME)/java/efisps.jar COM/hotdiary/eventfeed/isp/server/ISPFeedServerImpl.class COM/hotdiary/eventfeed/isp/server/ISPFeedServerImpl_Skel.class

ISPFeedServer.class : ISPFeedServer.java
	javac ISPFeedServer.java

ISPFeedServerImpl.class : ISPFeedServerImpl.java
	javac ISPFeedServerImpl.java

ISPFeedServerImpl_Skel.class: ISPFeedServerImpl.class
	rmic COM.hotdiary.eventfeed.isp.server.ISPFeedServerImpl

clean:
	rm -f ISPFeedServerImpl.class ISPFeedServerImpl_Skel.class $(HDHOME)/java/efisps.jar

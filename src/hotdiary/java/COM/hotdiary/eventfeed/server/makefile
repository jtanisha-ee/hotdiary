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

all : $(HDHOME)/java/efs.jar

$(HDHOME)/java/efs.jar : $(HDHOME)/java/efi.jar EFServerImpl.class EFServerImpl_Skel.class
	cd $(HDHOME)/java && jar cvf $(HDHOME)/java/efs.jar COM/hotdiary/eventfeed/server/EFServerImpl.class COM/hotdiary/eventfeed/server/EFServerImpl_Skel.class

EFServer.class : EFServer.java
	javac EFServer.java

EFServerImpl.class : EFServerImpl.java
	javac EFServerImpl.java

EFServerImpl_Skel.class: EFServerImpl.class
	rmic COM.hotdiary.eventfeed.server.EFServerImpl

clean:
	rm -f EFServerImpl.class EFServerImpl_Skel.class $(HDHOME)/java/efs.jar

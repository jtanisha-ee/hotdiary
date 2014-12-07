# $Id: makefile,v 1.1 1999/05/04 22:38:20 mjoshi Exp $
#
# Copyright (c) 1999 HotDiary Inc.
#
# This makefile has targets to checkout java files and jar files
# from the database, build them, and generate appropriate efi.jar
# file. This file can be committed back into CVS. The error output
# of cvs is appended to make.log in current directory.
#
# USAGE:
# To perform a fresh make of the latest stuff in CVS:
# 	make new
# To build what's already in your directory:
#	make

all : $(HDHOME)/java/efi.jar

$(HDHOME)/java/efi.jar : EFServer.class HDEvent.class HDLogin.class
	cd $(HDHOME)/java && jar cvf $(HDHOME)/java/efi.jar COM/hotdiary/eventfeed/hdif/EFServer.class COM/hotdiary/eventfeed/hdif/HDEvent.class COM/hotdiary/eventfeed/hdif/HDLogin.class

EFServer.class : EFServer.java
	javac EFServer.java

HDLogin.class : HDLogin.java
	javac HDLogin.java

HDEvent.class: HDEvent.java
	javac HDEvent.java

clean:
	rm -f EFServer.class HDLogin.class HDEvent.class $(HDHOME)/java/efi.jar

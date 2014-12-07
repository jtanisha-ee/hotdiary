# $Id: makefile,v 1.1 1999/05/04 22:38:20 mjoshi Exp $
#
# Copyright (c) 1999 HotDiary Inc.
#
# USAGE:
# To perform a fresh make of the latest stuff in CVS:
# 	make new
# To build what's already in your directory:
#	make

all : $(HDHOME)/java/efc.jar

$(HDHOME)/java/efc.jar : $(HDHOME)/java/efi.jar EFClient.class
	cd $(HDHOME)/java && jar cvf $(HDHOME)/java/efc.jar COM/hotdiary/eventfeed/client/EFClient.class COM/hotdiary/eventfeed/server/EFServerImpl_Stub.class

EFClient.class : EFClient.java
	javac EFClient.java

clean:
	rm -f EFClient.class $(HDHOME)/java/efc.jar

# $Id: makefile,v 1.1 1999/05/04 22:38:20 mjoshi Exp $
#
# Copyright (c) 1999 HotDiary Inc.
#
# USAGE:
# To perform a fresh make of the latest stuff in CVS:
# 	make new
# To build what's already in your directory:
#	make

all : $(HDHOME)/java/efispc.jar

$(HDHOME)/java/efispc.jar : $(HDHOME)/java/efi.jar ISPFeedClient.class
	cd $(HDHOME)/java && jar cvf $(HDHOME)/java/efispc.jar COM/hotdiary/eventfeed/isp/client/ISPFeedClient.class COM/hotdiary/eventfeed/isp/server/ISPFeedServerImpl_Stub.class

ISPFeedClient.class : ISPFeedClient.java
	javac ISPFeedClient.java

clean:
	rm -f ISPFeedClient.class $(HDHOME)/java/efispc.jar

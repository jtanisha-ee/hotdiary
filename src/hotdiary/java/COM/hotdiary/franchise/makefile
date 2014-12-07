# $Id: makefile,v 1.1 1999/05/04 22:38:20 sgudur Exp $
#
# Copyright (c) 1999 HotDiary Inc.
#
# USAGE:
# To perform a fresh make of the latest stuff
# 	make new
# To build what's already in your directory:
#	make

all : $(HDHOME)/franchise/hotdiaryjazzit.jar

$(HDHOME)/franchise/hotdiaryjazzit.jar : SUR.class FetchCal.class
	cd $(HDHOME)/java && jar cvf hotdiaryjazzit.jar COM/hotdiary/franchise/SUR.class COM/hotdiary/franchise/FetchCal.class COM/hotdiary/calmgmtserver/CalAppClient.class COM/hotdiary/calmgmtserver/RequestHandler.class COM/hotdiary/calmgmtserver/CalAppServer.class JP UK muffin sdsu && rm -f $(HDHOME)/java/COM/hotdiary/franchise/*.class && mv hotdiaryjazzit.jar $(HDHOME)/franchise

SUR.class : SUR.java
	javac SUR.java

FetchCal.class : FetchCal.java
	javac FetchCal.java

clean:
	mv $(HDHOME)/franchise/hotdiaryjazzit.jar $(HDHOME)/franchise/hotdiaryjazzit.jar.save

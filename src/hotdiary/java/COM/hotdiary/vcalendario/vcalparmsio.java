package COM.hotdiary.vcalendario;
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;

public class vcalparmsio {

   int parms_cnt = 10;
   vcalendario vcalendario;
   vcalparmsfmt vcalparmsfmt;

   String s = vcalendario.s;

   void getcomment(int k, String comment[]) {

      int comlen = vcalparmsfmt.comment.length();

      if (s.regionMatches(vcalendario.ignoreCase, k, vcalparmsfmt.comment, 
		0, comlen)) {

         int tlen = vcalendario.getValueSepIndex(k+comlen);
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);

         if (tindex == -1) {
            return;
         }

         for (int i = 0; i < parms_cnt; i++) {
            if (comment[i] == null) {
               comment[i] = s.substring(tlen, tindex);
	       break;
            }
         }
      }
   }


   /*
      This applies to rdate, dtstart, dtend, dtstamp, freebusy whichever is in
      date format of vcalendar.
      This deals with the following formats:
	  1. DTSTART:19971015T050000Z
          2. FREEBUSY:19980314T233000Z/19980315T003000Z
          3. DTSTART:19971026T020000
          4. DTSTART;TZID=US-Eastern:19970902T090000
	  5. FREEBUSY;VALUE=PERIOD:19971015T050000Z/PT8H30M,
              19971015T160000Z/PT5H30M,19971015T223000Z/PT6H30M

	This returns year, month, day, hour,min,sec given a date in the
        following formats:
		19971026T020000
                19971015T050000Z 
                19971015T050000Z/PT8H30M 
   */
   void getTime(String vcaldate ) {
      String meridian;
      String year = vcaldate.substring(0, 4);
      String month = vcaldate.substring(4,6);
      String day = vcaldate.substring(6,8);

      if (vcaldate.regionMatches(vcalendario.ignoreCase, 9, "T", 0, 1)) {
         String shour = vcaldate.substring(10,12);
         String min =  vcaldate.substring(12,14);
         String sec =  vcaldate.substring(14,16);
         int hour = (new Integer(shour)).intValue();
         if (hour  > 11) {
            meridian = "PM";
         } else
            meridian = "AM";
      }
      String slash = "z";

      int bindex = vcaldate.indexOf(slash, 15);
      if (bindex != -1) {
         int ptindx = vcaldate.indexOf("PT", bindex+1);
         if (ptindx != -1) {
            int pt_hourinx = vcaldate.indexOf("H", ptindx+1);
            String pt_hour = vcaldate.substring(ptindx+1, ptindx+3);
            String pt_min = vcaldate.substring(pt_hourinx+1, pt_hourinx+3);
         }
      }
   }



   void getURL(int k, String url) {

      if (s.regionMatches(vcalendario.ignoreCase, k,vcalparmsfmt.url, 0,
		 vcalparmsfmt.url.length())) {
         int tlen = vcalendario.getValueSepIndex(k+vcalparmsfmt.url.length());
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);

         if (tindex == -1) {
            return;
         }

         if (url == null) {
            url = s.substring(tlen, tindex);
         }
      }
   }

   /*
         ATTENDEE;RSVP=TRUE;ROLE=REQ-PARTICIPANT:MAILTO:
	 ATTENDEE;CUTYPE=GROUP:MAILTO:ietf-calsch@imc.org
         ATTENDEE;DELEGATED-FROM="MAILTO:jsmith@host.com":MAILTO:
         	jdoe@host.com
	  ATTENDEE;DELEGATED-TO="MAILTO:jdoe@host.com","MAILTO:jqpublic@
          host.com":MAILTO:jsmith@host.com
          ATTENDEE;MEMBER="MAILTO:ietf-calsch@imc.org":MAILTO:jsmith@host.com
	  ATTENDEE;MEMBER="MAILTO:projectA@host.com","MAILTO:projectB@host.
           com":MAILTO:janedoe@host.com
	  ATTENDEE;PARTSTAT=DECLINED:MAILTO:jsmith@host.com 
	  ATTENDEE;ROLE=CHAIR:MAILTO:mrbig@host.com
	  ATTENDEE;RSVP=TRUE:MAILTO:jsmith@host.com
          ATTENDEE:MAILTO:jane_doe@host.com
          ATTENDEE;MEMBER="MAILTO:DEV-GROUP@host2.com":
		MAILTO:joecool@host2.com
          ATTENDEE;DELEGATED-FROM="MAILTO:immud@host3.com":
      		MAILTO:ildoit@host1.com
          ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=TENTATIVE;DELEGATED-FROM=
             "MAILTO:iamboss@host2.com";CN=Henry Cabot:MAILTO:hcabot@host2.com
          ATTENDEE;ROLE=NON-PARTICIPANT;PARTSTAT=DELEGATED;DELEGATED-TO=
       	"MAILTO:hcabot@host2.com";CN=The Big Cheese:MAILTO:iamboss@host2.com
          ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;CN=Jane Doe
      		:MAILTO:jdoe@host1.com
          ATTENDEE;SENT-BY=MAILTO:jan_doe@host1.com;CN=John Smith:MAILTO:
      		jsmith@host1.com
	  ATTENDEE;RSVP=TRUE;ROLE=REQ-PARTICIPANT;CUTYPE=GROUP:
              MAILTO:employee-A@host.com
    */
   
   void getattendee(int k, String attendee[]) {

      if (s.regionMatches(vcalendario.ignoreCase, k,vcalparmsfmt.attendee, 0,
		 vcalparmsfmt.attendee.length())) {

         int tlen = vcalendario.getValueSepIndex(k+vcalparmsfmt.attendee.length());
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);
         if (tindex == -1) {
            return;
         }

         int sepindex = tlen;
         for (int i = sepindex; i <= tindex; i= sepindex +1) {
	    if (s.regionMatches(vcalendario.ignoreCase, i,  
		vcalparmsfmt.mailto, 0, vcalparmsfmt.mailto.length())) {
	       sepindex = vcalendario.getValueSepIndex(i+vcalparmsfmt.mailto.length());
	    }

            if ((sepindex == -1)  || (sepindex == tlen))
	       sepindex = tindex;

            for (int j = 0; j < parms_cnt; j++) {
               if (attendee[j] == null) {
                  attendee[j] = s.substring(i, sepindex);
	          break;
               }
            }
         }
	 return;
      }
   }

   /*
	ORGANIZER:MAILTO:jsmith@host.com
        ORGANIZER;CN="John Smith":MAILTO:jsmith@host.com
        ORGANIZER;DIR="ldap://host.com:6666/o=eDABC%20Industries,c=3DUS??
      (cn=3DBJim%20Dolittle)":MAILTO:jimdo@host1.com
	ORGANIZER;SENT-BY:"MAILTO:sray@host.com":MAILTO:jsmith@host.com
    */

   void getorganizer(int k, String organizer[]) {

      if (s.regionMatches(vcalendario.ignoreCase, k,vcalparmsfmt.organizer, 0,
                 vcalparmsfmt.organizer.length())) {

         int tlen = vcalendario.getValueSepIndex(k+vcalparmsfmt.organizer.length());
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);
         if (tindex == -1) {
            return;
         }

         int sepindex = tlen;
         for (int i = sepindex; i <= tindex; i= sepindex +1) {
            if (s.regionMatches(vcalendario.ignoreCase, i,  
		vcalparmsfmt.mailto, 0, vcalparmsfmt.mailto.length())) {
               sepindex = vcalendario.getValueSepIndex(i+vcalparmsfmt.mailto.length());
            }

            if ((sepindex == -1)  || (sepindex == tlen))
               sepindex = tindex;

            for (int j = 0; j < parms_cnt; j++) {
               if (organizer[j] == null) {
                  organizer[j] = s.substring(i, sepindex);
                  break;
               }
            }
         }
      }
   }


}


package COM.hotdiary.vcalendario;
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;

/* 
public class vfreebusyin {

   int fbcnt;
   String freebusy[];
   class vcalparams vparms;
}
*/

public class vfreebusyio {

   /* this needs to be set in vcalendario.java */
   vcalparmsfmt vcalparms;
   vcalendario vcalendario;
   int rec = vcalendario.rec;
   String s = vcalendario.s;
   int fbcnt = vcalendario.fbcnt;
   vfreebusyin[] vfreebusyin = new vfreebusyin[fbcnt];
   vfreebusyfmt vfreebusyfmt;
   String cgistr, jstr;
   int fbrec;

   void initializefreebusy() {
    
      for (int i = 0; i < fbcnt; i++) {
         vfreebusyin[i] = new vfreebusyin();
         vfreebusyin[i].freebusy[i] = new String();
         vfreebusyin[i].vparms.dtstart = null;
         vfreebusyin[i].vparms.dtend = null;
         vfreebusyin[i].vparms.organizer = null;
         vfreebusyin[i].vparms.url = null;
         vfreebusyin[i].vparms.duration = null;
         vfreebusyin[i].vparms.organizer = null;
         vfreebusyin[i].vparms.attendee[i]= null;
         vfreebusyin[i].vparms.dtstamp = null;
         vfreebusyin[i].vparms.uid = null;
         vfreebusyin[i].vparms.comment[i] = null;
         vfreebusyin[i].vparms.rstatus[i] = null;
      }
   }

   void getfreebusy(int k) {

      int fblen = vfreebusyfmt.freebusy.length();

      if (s.regionMatches(vcalendario.ignoreCase, k, vfreebusyfmt.freebusy,0,
           fblen)) {
         int tlen = vcalendario.getValueSepIndex(k+fblen);
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);

         if (tindex == -1) {
            return;
         }
      
         int mutvals; 
	 int j;
         for (int i = tlen; i < tindex; i = mutvals+1) { 
            mutvals = s.indexOf(",", tlen);
            if (mutvals != -1 ) {
               if ((j = getfbrec()) != -1) { 
                  vfreebusyin[fbrec].freebusy[j] = s.substring(tlen, mutvals);
	       }
	    } else {
	       if (i == tlen) {
                  if ((j = getfbrec()) != -1) { 
                     vfreebusyin[fbrec].freebusy[j] = s.substring(tlen, tindex);
		  }
	       }
	       break;
            }
         }  
      }         
   }


   int getfbrec() {
      for (int i = 0; i < fbcnt; i++) {
         if (vfreebusyin[fbrec].freebusy[i] == null) {
	    return i;
         }
      }
      return -1;
   }


   void getcomment(int k) {

      int comlen = vcalparms.comment.length();

      if (s.regionMatches(vcalendario.ignoreCase, k, vcalparms.comment, 0, comlen)) {
         int tlen = vcalendario.getValueSepIndex(k+comlen);
         if (tlen == -1)
            return;

         int tindex = vcalendario.getTerminatorIndex(tlen);

         if (tindex == -1) {
            return;
         }

         for (int i = 0; i < fbcnt; i++) {
           if (vfreebusyin[fbrec].vparms.comment[i] == null) {
               vfreebusyin[fbrec].vparms.comment[i] = s.substring(tlen, tindex);
	       break;
           }
         }
      }
   }


   void checkFBTYPE(int k) {

      /** TEL:+1-919-555-7878 */
      int fblen = vfreebusyfmt.fbtype.length();

      if (s.regionMatches(vcalendario.ignoreCase, k,  vfreebusyfmt.fbtype, 0, fblen)) {
         int tlen = vcalendario.getValueSepIndex(k+fblen);
         int telindex = vcalendario.getTerminatorIndex(tlen);

         if (telindex == -1)
            return;

         jstr = s.substring(tlen+1, telindex );
         cgistr = vcalendario.getCGIString(jstr);
      }
   }

   void checkVFREEBUSY(int k) {
      int beglen = vfreebusyfmt.begin.length();
      int endlen = vfreebusyfmt.end.length();

      if (s.regionMatches(vcalendario.ignoreCase, k,  vfreebusyfmt.begin, 0, beglen)) {
         for (int j = k+beglen; j < vcalendario.bytesRead; j++) {
            if (s.regionMatches(vcalendario.ignoreCase, j, vfreebusyfmt.end, 0,
                         endlen)) {
	       vcalendario.fbrec++;
	       fbrec = vcalendario.fbrec;
               break;
            }
            processVFreebusy(k);
         }
      }
   }


  void getdatestart(int k) {
     int dlen = vcalparms.dtstart.length();

     if (s.regionMatches(vcalendario.ignoreCase, k,  vcalparms.dtstart,
	 0, dlen)) {
        int tlen = vcalendario.getValueSepIndex(k+dlen);
        int telindex = vcalendario.getTerminatorIndex(tlen);

        if (telindex == -1)
           return;

        jstr = s.substring(tlen+1, telindex );
        cgistr = vcalendario.getCGIString(jstr);
     }
  }



   void processVFreebusy(int k) {
      getfreebusy(k);
      getcomment(k);
      getdatestart(k); 
      get 
   }

}

/*

   int getEndCnt(String pattern, String inbuf) {

      int cnt = 0;
      int j = 0;

      for (int i = 0; i < (int)size; i = j+1) {
         j = inbuf.indexOf(pattern, i);
         if (j != -1) {
            cnt++;
         } else
            break;
       }
       System.out.println("endcnt" + cnt);
       return cnt;
   }


   int getBeginCnt(String pattern, String inbuf) {
      int cnt = 0;
      int j = 0;
      for (int i = 0; i < (int)size; i = j+1) {
         j = inbuf.indexOf(pattern, i);
         System.out.println("j =" + j);
         System.out.println("i ="  + i);
         if (j != -1) {
            cnt++;
         } else
            break;
      }
      System.out.println("begincnt" + cnt);
      return cnt;
   }


   int checkValidityOfFile() {
      int begincnt = getBeginCnt();
      int endcnt = getEndCnt();

      if (begincnt != endcnt) {
         msg = "This file has mismatched BEGIN" + begincnt + "and END" + endcnt;
         msg = getCGIString(msg);
         return 0;
      }

      if (begincnt <= 0) {
         msg = "This file is missing BEGINs";
         msg = getCGIString(msg);
         return 0;
      }

      if (endcnt <= 0) {
         msg = "This file is missing ENDs and is not a valid VCARD format";
         msg = getCGIString(msg);
         return 0;
      }

      numrec = begincnt;
      return 1;

  }
*/




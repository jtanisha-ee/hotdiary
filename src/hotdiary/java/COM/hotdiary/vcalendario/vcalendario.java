package COM.hotdiary.vcalendario; 
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;


/**
 *  : colon seperates between name=value i.e name:value
 *  The content types are seperated by a CRLF i.e ASCII (decimal 13)
 *  and ascii (decimal 10).
 *  if CRLF is followed by white space then the content type is being
 *  continued.
 *  if a parameter values contain : colon it should be in quoted string
 *  ie. ":" 
 *  as there could be more than one vlaue associated with the name
 *  we should for colon's until we reach CRLF 
 * 
*/

public class vcalendario {
    String s, cgistr, jstr; 
    int bytesRead, rec = 0;
    int numrec= 10;
    int fbrec = 0;
    vcalendarin[] vcalendarin = new vcalendarin[10];
    vfreebusyio vfreebusy;
    int fbcnt = 10;
    byte[] inb;
    vcalendarfmt vcalendarfmt= new vcalendarfmt();
    vcalparmsfmt vcalparmsfmt;
    String terminator = "CRLF";
    String quote = "'";
     
    int termlen = terminator.length();
    boolean ignoreCase = true; 
    String valuesep = ":";
    int valueseplen = valuesep.length();
    int size;
    String msg;

    /**
     * All comparisons are case insensitive.
     */
    public void parseVcalendar(String pprog) {

        byte[] vcalendar = new byte[size];
        int k, endindex, j = 0; 
        s = new String(inb);
	InitializeFields(); 
        int beglen = vcalendarfmt.vcalbegin.length(); 
        int endlen = vcalendarfmt.vcalend.length(); 
           
        for (int i = 0; i < bytesRead; i++) {
           if ((s.regionMatches(ignoreCase, i, vcalendarfmt.vcalbegin, 0, beglen))) {
              /** then we have more than one vcalendar listed in this file */
              for (k = i+beglen; k < bytesRead; k++) {
                 if (s.regionMatches(ignoreCase, k, vcalendarfmt.vcalend, 0, endlen)) {
       		     printVcalendar();  
		     sendVcalendar(pprog);
		     rec++;
	             break;
                 }
	         checkVcalendarFields(k);	
              }
           }
        }
    }

    public void vcalendar_read(String infile, String pprog) {
       FileInputStream fis = null;

       /** 
        * we should get the vcalendar format first. 
        * then read the format of each vcalendar record.
        * and write it into a .rec file
        * .rec file has an entrynumber associated with it.
        * chunksize is the vcalendar record size.
        *
        */
       File file = new File(infile);
       long size1 = file.length();
       size = (int)size1;
       inb = new byte[size+1];
       bytesRead = 0;
       for (int i = 0; i < size; i++) {
	 inb[i] = 0;
       }

       try {
           fis = new FileInputStream(file);
           bytesRead = fis.read(inb);

       } catch (IOException e) {
           System.out.println(e.getMessage());
       }
       inb[bytesRead] = '\0';
       String str = new String(inb);
       s = str.toUpperCase();
      // dump(); 
       parseVcalendar(pprog);
       /** sendVcalendar(pprog); */
    }

    void dump() {
	System.out.println("contents" + inb);
    }

    int getTerminatorIndex(int tlen) {
       return(s.indexOf(terminator, tlen));
    }

    int getValueSepIndex(int i) {
       int indlen;
       /** get the value seperator index */
       indlen = s.indexOf(valuesep, i);
       return(indlen);
    }

   
    void checkVcalendarFields( int k) {
       vfreebusy.checkVFREEBUSY(k);

       /* checkVEVENT(k); 
        checkVTODO(k); 
        checkVJOURNAL(k); 
        checkVTIMEZONE(k);  */
    } 

    void processParms(int k, String component ) {
       checkDTSTART(k, component);
/*
       checkDTEND(k, component);
       checkURL(k, component);
       checkDTSTART(k, component);
       checkDTEND(k, component);
       checkDURATION(k, component);
       checkDTSTAMP(k, component);
       checkUID(k, component);
       checkATTENDEE(k, component);
       checkORGANIZER(k, component);
*/
    }

    String getTZID(int starttz, int tlen ) {
       int tzindex = s.indexOf("TZID=", starttz);
       if (tzindex == -1) {
          return null;
       }
       return(s.substring(tzindex+1, tlen-1));
    }



    void checkDTSTART(int k, String dtstart) {
	/**   DTSTART;TZID=US-Eastern:19980119T020000 
	      DTSTART:19980118T230000   - local time with out  UTC  or TZ
              DTSTART:19980119T070000Z 
              DTSTART;TZID=US-Eastern:19970105T083000 
         */
       int dtstartlen = vcalparmsfmt.dtstart.length();
       if (s.regionMatches(ignoreCase, k, vcalparmsfmt.dtstart, 0, dtstartlen)) {
  	  int tlen = getValueSepIndex(k+dtstartlen+1);
	  if (tlen == -1) {
	      return;
          }

          int telindex = getTerminatorIndex(tlen);
          if (telindex == -1) 
             return;
          dtstart = s.substring(tlen+1, telindex);
	  String tzone = getTZID(k+dtstartlen, tlen); 
       }
    }
  
/* 
   void checkVEVENT(int k ) {
      
      int beglen = vevent.begin.length();
    
      if (s.regionMatches(ignoreCase, k,  vevent.begin, 0, beglen)) {
         for (int j = k+vevent.beglen; j < bytesRead; j++) {
            if (s.regionMatches(ignoreCase, j, vevent.end, 0,
                         vevent.endlen)) {
               break;
            }
            processVevent(k);
         }
      }
   }            
*/

   void processVevent(int k) {
       return;
       /* getvevent(k); */
   }
   
   void InitializeFields() {
      for (int i = 0; i < numrec; i++) {
         vcalendarin[i] = new vcalendarin();
      }
   }

   void printVcalendar() {
         System.out.println("entered printVcalendar");
   }

  void sendVcalendar(String pprog) {
     if (pprog != null)  {
        try {
           System.out.println("calling perl program" + pprog);
           /** this one works */
           Process p = Runtime.getRuntime().exec(pprog); 
           InputStream is = p.getInputStream();
           byte b[] = new byte[256];
           int len;
           try {
               while ((len = is.read(b)) != -1) {
                  System.out.print(new String(b, 0, len));
               }
           } catch (NullPointerException e) {
           }
        } catch (Exception e) {
               e.printStackTrace();
        }
        System.out.println("done perl program");
     }
  }

  // s = getCGIString("Manoj Joshi");
  String getCGIString(String s) {
      StringTokenizer st = new StringTokenizer(s);
      String msg = null;
      if (st.hasMoreTokens()) {
         msg = st.nextToken();
      } 
    /** else {
           System.out.println("Empty Message String");
      } */
      while (st.hasMoreTokens()) {
         msg += "+" + st.nextToken();
      }
      return msg;
  }

}

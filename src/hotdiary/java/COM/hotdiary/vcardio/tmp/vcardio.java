package COM.hotdiary.vcardio; 
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;


/**
 * when reading semicolon(ASCII decimal 59) be seperated with (ASCII decimal 92)
 * 
*/

public class vcardio {
     String s, cgistr, jstr; 
     int bytesRead, rec = 0;
     int numrec= 10;
     vcardin[] vcardin = new vcardin[10];
     byte[] inb;
     vcardfmt vcard = new vcardfmt();
     String terminator = "\n";
     int termlen = terminator.length();
     boolean ignoreCase = true; 
     String valuesep = ":";
     int valueseplen = valuesep.length();
     int pager, work,home, cell,fax; 

    /**
     * All comparisons are case insensitive.
     */
    public void parseVcard(String pprog) {

        byte[] vcardrec = new byte[4096];
        int k, endindex, j = 0; 
        s = new String(inb);
	InitializeFields(); 
        
           
        for (int i = 0; i < bytesRead; i++) {
           if ((s.regionMatches(ignoreCase, i, vcard.begin, 0, vcard.beglen))) {
              /**
               * this is a vcard as it matches "BEGIN:VCARD, so we go ahead and put 
               * this in a record in addrtab. we need to generate vcardrec.
               * should we present this a vcard for later use. need to use another
               * function to do that.
               * ignore backspace (\n)
               */
	      endindex =  s.indexOf("END:vCard", i);

              /** then we have more than one vcard listed in this file */
              for (k = i+vcard.beglen; k < bytesRead; k++) {
                 if (s.regionMatches(ignoreCase, k, vcard.end, 0, vcard.endlen)) {
       		     printVcard();  
		     sendVcard(pprog);
		     rec++;
	             break;
                 }
	         checkVcardFields(k);	
              }
          }
      }
   }

    public void vcard_read(String infile, String pprog) {
       FileInputStream fis = null;

       /** 
        * we should get the vcard format first. 
        * then read the format of each vcard record.
        * and write it into a .rec file
        * .rec file has an entrynumber associated with it.
        * chunksize is the vcard record size.
        *
        */
       inb = new byte[4096];
       bytesRead = 0;
       for (int i = 0; i < 4096; i++) {
	 inb[i] = 0;
       }

       try {
           fis = new FileInputStream(new File(infile));
           bytesRead = fis.read(inb);

       } catch (IOException e) {
           System.out.println(e.getMessage());
       }
       inb[bytesRead] = '\0';
       parseVcard(pprog);
       /** sendVcard(pprog); */
    }

    int getValueSepIndex(int i) {
      int indlen;
      /** get the value seperator index */
      indlen = s.indexOf(valuesep, i);
      return(indlen);
    }

   
    void checkVcardFields( int k) {
        checkVER(k); 
        checkFN(k); 
        checkNickName(k);
        /** checkN(k); */
        checkADR(k);
        checkBDAY(k);
        checkTEL(k);
        checkORG(k);
        checkEMAIL(k);
        checkURL(k);
        checkUID(k);
    } 

    void checkFN(int k ) {

       /** FN:Mr. John Q. Public\, Esq. */
       /** find out what the FN ends with */
       int fnlen = vcard.fn.length();
    
       if (s.regionMatches(ignoreCase, k,  vcard.fn, 0, fnlen)) {

          /** get the value seperator index */
          int tlen = getValueSepIndex(k+fnlen); 

	  int telindex = getTerminatorIndex(tlen);
          if (telindex == -1) 
	     return;
          jstr = s.substring(tlen+1, telindex);
	  cgistr = getCGIString(jstr);
          if (vcardin[rec].fn == null)  {
             vcardin[rec].fn = cgistr;
          } else 
	     vcardin[rec].other.concat(cgistr);
       }
    }
  
   void checkNickName(int k ) {
       /** NICKNAME:Jim, Jimmie */
       /** find out what the NICKNAME ends with */
       int nicklen = vcard.nickname.length();
     
       if (s.regionMatches(ignoreCase, k,  vcard.nickname, 0, nicklen)) {

          int tlen = getValueSepIndex(k+nicklen); 
          int telindex = getTerminatorIndex(tlen); 
          if (telindex == -1) 
	     return;
          jstr = s.substring(tlen+1, telindex); 
	  cgistr = getCGIString(jstr);
          if (vcardin[rec].nickname == null) {
             vcardin[rec].nickname = cgistr;
          } else {
	     vcardin[rec].other.concat(cgistr);
          }
       }
   }

   void checkN(int k) {
       /** N:Stevenson;John;Quinlan;Mr.;Esq. */
       /** find out what the NICKNAME ends with */
       int nlen = vcard.n.length();
     
       if (s.regionMatches(ignoreCase, k,  vcard.n, 0, nlen)) {
          int tlen = getValueSepIndex(k+nlen); 
          int telindex = getTerminatorIndex(tlen); 
          if (telindex == -1) 
	     return;
          jstr = s.substring(tlen+1, telindex );
	  cgistr = getCGIString(jstr);
          if (vcardin[rec].n == null) {
             vcardin[rec].n = cgistr; 
          } else 
	     vcardin[rec].other.concat(cgistr);
       }
   }

   void checkBDAY(int k) {
       /** BDAY:1996-04-15 */
       /** find out what the NICKNAME ends with */
       int bdaylen = vcard.bday.length();
     
       if (s.regionMatches(ignoreCase, k,  vcard.bday, 0, bdaylen)) {
          int tlen = getValueSepIndex(k+bdaylen); 
          int telindex = getTerminatorIndex(tlen); 
          if (telindex == -1) 
	     return;
          jstr = s.substring(tlen+1, telindex );
          cgistr = getCGIString(jstr);
          vcardin[rec].bday = cgistr;
       }
   }

   void checkTEL(int k) {
       /** TEL:+1-919-555-7878 */
       int tellen = vcard.tel.length();
       String telValue = null;

       getTelDigits(k, vcard.tel, tellen, pager, work, home, cell, fax);
   }
   
   void checkUID(int k) {
       int uidlen = vcard.uid.length();

       if (s.regionMatches(ignoreCase, k,  vcard.uid, 0, uidlen)) {
          int tlen = getValueSepIndex(k+uidlen);
          int telindex = getTerminatorIndex(tlen);
          if (telindex == -1)
             return;
          jstr = s.substring(tlen+1, telindex );
          cgistr = getCGIString(jstr);
          if (vcardin[rec].uid == null) {
             vcardin[rec].uid = cgistr;
          } else
             vcardin[rec].other.concat(cgistr);
       }
   }               
   }

   void checkVER(int k) {

       /** TEL:+1-919-555-7878 */
       int verlen = vcard.ver.length();
        
       if (s.regionMatches(ignoreCase, k,  vcard.ver, 0, verlen)) {
          int tlen = getValueSepIndex(k+verlen); 
          int telindex = getTerminatorIndex(tlen); 
          if (telindex == -1) 
	     return;
	  jstr = s.substring(tlen+1, telindex );
          cgistr = getCGIString(jstr);
          if (vcardin[rec].ver == null) {
             vcardin[rec].ver = cgistr;
	  } else  
             vcardin[rec].other.concat(cgistr);
       }
   }

   void checkADR(int k) {

       /** ADR;TYPE=WORK:;;501 E. Middlefield Rd.;Mountain View;CA; 94043;U.S.A. 
         we ignore type in our field, and use the following:
         each value is seperated by a ; (SEMICOLON)
         address has:
               1. Po BOX
               2. extended address
	       3. Street Address
	       4. City
	       5. State
	       6. Zip or Postal Code
	       7. Country Name
       */
       String sep = ";";
       int seplen = sep.length();
       int addrlen = vcard.address.length();
       int indlen, max = 0;
       
       if (s.regionMatches(ignoreCase, k,  vcard.address, 0, addrlen)) {

          /** get the value seperator index */
          int tlen = getValueSepIndex(k+addrlen); 

	  int adrend = s.indexOf(terminator, tlen);
	  char[] vchar = new char[adrend-tlen +1];
	  s.getChars(tlen, adrend,  vchar,0);

          max = tlen;
          for (int i = 0; i < 3; i++) {
	    max = s.indexOf(sep, max); 
            max = max+1;
          } 

          /** copy this into street address */
          jstr = s.substring(tlen+1, max-1 );
	  cgistr = getCGIString(jstr); 
          vcardin[rec].street = cgistr;

          /** copy this into city */   
	  indlen = s.indexOf(sep, max); 
	  if (indlen != -1)  {
             jstr = s.substring(max, indlen);
	     cgistr = getCGIString(jstr); 
	     if (vcardin[rec].city == null) {
                 vcardin[rec].city = cgistr;
	     } else 
		 vcardin[rec].other  =cgistr;
	     max = indlen;
          }

          /** copy this into state */   
	  indlen = s.indexOf(sep, max+1); 
	  if (indlen != -1) {
             jstr = s.substring(max+1, indlen);
	     cgistr = getCGIString(jstr); 
             vcardin[rec].state = cgistr;
	     max = indlen;
          }

          /** copy this into zipcode */   
	  indlen = s.indexOf(sep, max+1); 
	  if (indlen != -1) {
             jstr = s.substring(max+1, indlen);
	     cgistr = getCGIString(jstr); 
             vcardin[rec].zipcode = cgistr; 
	     max = indlen;
          }
              
          /** copy country  */   
	  if (indlen != -1)  {
                jstr = s.substring(max+1, adrend - 1);
	        cgistr = getCGIString(jstr); 
             if (vcardin[rec].country == null)  
                vcardin[rec].country = cgistr;
	     else 
                vcardin[rec].other.concat(cgistr);
          }
	  
       }
   }

   void checkORG(int k) {

       /** ORG:HotDiary Inc. */
       int orglen = vcard.org.length();

       if (s.regionMatches(ignoreCase, k,  vcard.org, 0, orglen)) {

          int textlen = getValueSepIndex(k+orglen); 

	  int telindex = s.indexOf(terminator, textlen);
          if (telindex == -1) 
	     return;
          jstr = s.substring(textlen+1, telindex);
	  cgistr = getCGIString(jstr); 
          if (vcardin[rec].org == null)  
             vcardin[rec].org = cgistr; 
	  else
             vcardin[rec].other.concat(cgistr);
       }
   }


   void checkEMAIL(int k) {

       /**  */
       int emaillen = vcard.email.length();

       if (s.regionMatches(ignoreCase, k,  vcard.email, 0, emaillen)) {

          int textlen = getValueSepIndex(k+emaillen);
          int telindex = s.indexOf(terminator, textlen);
          if (telindex == -1)
             return;
          jstr = s.substring(textlen+1, telindex);
	  cgistr = getCGIString(jstr); 
	  if (vcardin[rec].email == null) 
             vcardin[rec].email = cgistr; 
	  else 
             vcardin[rec].other.concat( cgistr);
       }
   }

   void checkURL(int k) {

       int urllen = vcard.url.length();

       if (s.regionMatches(ignoreCase, k,  vcard.url, 0, urllen)) {

          int textlen = getValueSepIndex(k+urllen);

          int telindex = s.indexOf(terminator, textlen);
          if (telindex == -1)
             return;
          jstr = s.substring(textlen+1, telindex);
	  cgistr = getCGIString(jstr); 
	  if (vcardin[rec].url == null)
             vcardin[rec].url = cgistr;
	  else 
             vcardin[rec].other.concat(cgistr);
       }
   }

   void setCELL(String telvalue) {
       cgistr = getCGIString(telvalue); 
       if (vcardin[rec].cell == null)
          vcardin[rec].cell = cgistr; 
       else 
	  vcardin[rec].other.concat(cgistr);
   }

   void setHOME(String telvalue) {
       cgistr = getCGIString(telvalue); 
       if (vcardin[rec].home == null)
          vcardin[rec].home = cgistr; 
       else 
	 vcardin[rec].other.concat(cgistr);
   }

   void setWORK(String telvalue) {
       cgistr = getCGIString(telvalue);
       if (vcardin[rec].work == null)
          vcardin[rec].work = cgistr; 
       else 
	  vcardin[rec].other.concat(cgistr);
   }

   void setPAGER(String telvalue) {
       cgistr = getCGIString(telvalue);
       if (vcardin[rec].pager == null)
          vcardin[rec].pager = cgistr; 
       else 
	  vcardin[rec].other.concat(cgistr);
   }

   void setFAX(String telvalue) {
       cgistr = getCGIString(telvalue);
       if (vcardin[rec].fax == null)
          vcardin[rec].fax = cgistr; 
       else 
	  vcardin[rec].other.concat(cgistr);
   }

   void getTelDigits(int k, String telType, int telTypeLen, int pager, int work, int home, int cell, int fax) {

       if (s.regionMatches(ignoreCase, k, telType, 0, telTypeLen)) {
          int telindex = s.indexOf(terminator, k);
          if (telindex == -1) {
             return;
          }

          /** get the value seperator index */
          int sepindex = getValueSepIndex(k); 
	  int max = telindex - sepindex;
	  int j = 0;
          char[] telchar = new char[max+1];
          char[] vchar = new char[max +1];
          Character tchar = new Character('1');
          int telnum;

          s.getChars(sepindex, telindex, vchar, 0);

          /** check if pager,cell, work.home,fax are part of the same number */
	  String telstring = s.substring(k+telTypeLen - 1, telindex);
	  String upcaseString = telstring.toUpperCase();

          pager = upcaseString.indexOf(vcard.pager, 0);
          work = upcaseString.indexOf(vcard.work, 0);
          home = upcaseString.indexOf(vcard.home, 0);
          cell = upcaseString.indexOf(vcard.cell, 0);     
          fax = upcaseString.indexOf(vcard.fax, 0);

          for (int i = 0; i < max; i++) {
             telnum = tchar.getNumericValue(vchar[i]);
             if ((telnum >= 0 ) && (telnum <= 9)) {
                telchar[j] = vchar[i];
                j++;
             }
          }
	  if (j > 0) {
	     String tel = new String();
             String telValue = tel.copyValueOf(telchar, 0, j);
             if (pager > 0)
                setPAGER(telValue);
             if (work > 0)
                setWORK(telValue);
             if (home > 0)
                setHOME(telValue);
             if (cell > 0)
                setCELL(telValue);
             if (fax > 0)
                setFAX(telValue);
          }

       }
   }

   int getTerminatorIndex(int tlen) {
      return(s.indexOf(terminator, tlen));
   }

   void InitializeFields() {
     for (int i = 0; i < numrec; i++) {
       vcardin[i] = new Vcardin();
       vcardin[i].begin = null;
       vcardin[i].n = null;
       vcardin[i].title = null;
       vcardin[i].email = null;
       vcardin[i].pref = null;
       vcardin[i].internet = null;
       vcardin[i].ver = null;
       vcardin[i].end = null;
       vcardin[i].type = null;
       vcardin[i].fn = null;
       vcardin[i].nickname = null;
       vcardin[i].street = null;
       vcardin[i].city = null;
       vcardin[i].state = null;
       vcardin[i].zipcode = null;
       vcardin[i].country = null;
       vcardin[i].birthday = null;
       vcardin[i].url = null;
       vcardin[i].home = null;
       vcardin[i].fax = null;
       vcardin[i].work = null;
       vcardin[i].pager = null;
       vcardin[i].cell = null;
       vcardin[i].emailtype = null;
       vcardin[i].org = null;
       vcardin[i].bday = null;
       vcardin[i].other = new String();
       vcardin[i].Photo = null;
    }
   }

    
 
   void printVcard() {
         System.out.println("entered printVcard");
	 System.out.println("vcardin[rec].ver =" + vcardin[rec].ver);
	 System.out.println("vcardin[rec].fn =" + vcardin[rec].fn);
         System.out.println("vcardin[rec].fax =" + vcardin[rec].fax);
         System.out.println("vcardin[rec].work =" + vcardin[rec].work);
         System.out.println("vcardin[rec].home =" + vcardin[rec].home);
         System.out.println("vcardin[rec].street =" + vcardin[rec].street);
         System.out.println("vcardin[rec].city =" + vcardin[rec].city);
         System.out.println("vcardin[rec].state =" + vcardin[rec].state);
         System.out.println("vcardin[rec].zipcode =" + vcardin[rec].zipcode);
         System.out.println("vcardin[rec].country =" + vcardin[rec].country);
         System.out.println("vcardin[rec].nickname =" + vcardin[rec].nickname);
	 System.out.println("vcardin[rec].org =" + vcardin[rec].org);
         System.out.println("vcardin[rec].url =" + vcardin[rec].url);
         System.out.println("vcardin[rec].cell =" + vcardin[rec].cell);
         System.out.println("vcardin[rec].bday =" + vcardin[rec].bday);
	 System.out.println("vcardin[rec].n =" + vcardin[rec].n);
	 System.out.println("vcardin[rec].email=" + vcardin[rec].email);
	 System.out.println("vcardin[rec].url=" + vcardin[rec].url);
         System.out.println("vcardin[rec].pager =" + vcardin[rec].pager);
         System.out.println("vcardin[rec].uid =" + vcardin[rec].uid);
   }

  void sendVcard(String pprog) {
       String[] name = new String[2];
       name[0] = "name=";
       name[1] = "testing";
       if (pprog != null) 
            try {
               System.out.println("calling perl program" + pprog);
               /** this one works */
               Process p = Runtime.getRuntime().exec(pprog + " " +  
	          vcardin[rec].fn + " " +  
                  vcardin[rec].ver + " " + 
                  vcardin[rec].street + " " +
                  vcardin[rec].city + " "  + 
                  vcardin[rec].state + " " + 
                  vcardin[rec].zipcode + " " +
                  vcardin[rec].country + " " +
                  vcardin[rec].home + " " + 
                  vcardin[rec].pager + " " +
                  vcardin[rec].cell + " " + 
                  vcardin[rec].work + " " + 
                  vcardin[rec].email + " " +
                  vcardin[rec].url + " " + 
                  vcardin[rec].bday + " " +
                  vcardin[rec].org + " " + 
                  vcardin[rec].fax + " " + 
                  vcardin[rec].other  ); 
               /** Process p = Runtime.getRuntime().exec(pprog, name); */
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

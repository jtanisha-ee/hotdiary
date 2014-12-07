package COM.hotdiary.vcardio; 
import java.io.*;
import java.util.*;


/**
 * when reading semicolon(ASCII decimal 59) be seperated with (ASCII decimal 92)
 * 
*/

public class vcard {

   public String begin = "BEGIN:VCARD";   
   public String n = "N";
   public String title = "TITLE";  
   public String pref;
   public String internet;
   public String ver ="VERSION";
   public String end = "END:VCARD";
   public String terminator = "\n";
   public String type = "TYPE=";
   public String fn = "FN";
   public String nickname = "NICKNAME";
   public String address = "ADR;TYPE=";
   /** Telephone type is specified as :
      TEL;TYPE=work,voice,pref,msg:+1-213-555-1234
    */
   public String url = "URL";
   /** we don't care if the fields do not match in telephone. but they should not
       be overidden but should be saved in other fields 
   */ 
   public String tel = "TEL;TYPE=";
   public String cell = "CELL";
   public String fax = "FAX";
   public String pager = "PAGER";
   public String home = "HOME";
   public String email = "EMAIL;TYPE=";
   public String emailtype = "ET";
   public String org = "ORG";
   public String work = "WORK";
   public String bday = "BDAY";

   /** photo can be PHOTO;VALUE=uri or PHOTO;ENCODING=b;TYPE=JPEG:<binary> */
   public String Photo = "PHOTO";
   public int beglen = begin.length();
   public int endlen = end.length();
   public String uid = "UID";
}

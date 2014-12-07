package COM.hotdiary.vcardio; 
import java.io.*;
import java.util.*;


/**
 * when reading semicolon(ASCII decimal 59) be seperated with (ASCII decimal 92)
 * 
*/

public class vcardin implements Serializable {

   public String begin = null;
   public String n = null;
   public String title = null;  
   public String email = null; 
   public String pref = null;
   public String internet = null;
   public String ver = null; 
   public String end = null;
   public String type = null; 
   public String fn = null;
   public String nickname = null;
   public String street = null;
   public String city = null;
   public String state = null;
   public String zipcode = null;
   public String country = null;
   public String birthday = null;
   /** Telephone type is specified as :
      TEL;TYPE=work,voice,pref,msg:+1-213-555-1234
    */
   public String url = null;
   public String home = null;
   public String fax = null;
   public String work = null;
   public String pager = null;
   public String cell = null;
   public String emailtype = null;
   public String org = null;
   public String bday = null;
   public String other = null;
   public String uid = null;

   /** photo can be PHOTO;VALUE=uri or PHOTO;ENCODING=b;TYPE=JPEG:<binary> */
   public String Photo = null;
}

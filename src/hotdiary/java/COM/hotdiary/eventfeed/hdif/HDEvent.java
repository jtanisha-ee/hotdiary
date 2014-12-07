package COM.hotdiary.eventfeed.hdif;
import java.io.*;
import java.util.*;


/**
 * when reading semicolon(ASCII decimal 59) be seperated with (ASCII decimal 92)
 *
*/

public class HDEvent implements Serializable {

   public String entryno;
   public String biscuit;
   public String month;
   public String day;
   public String year;
   public String hour;
   public String min;
   public String meridian;
   public String zone; 
   public String desc; 
   public String subject; 
   public String phone; 
   public String city; 
   public String url; 
   public String imgfn; 
   public String venue; 

}

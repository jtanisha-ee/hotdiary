package COM.hotdiary.eventfeed.hdif;
import java.io.*;
import java.util.*;


/**
 * when reading semicolon(ASCII decimal 59) be seperated with (ASCII decimal 92)
 *
*/

public class HDLogin implements Serializable {

   public String login; 
   public String passwd; 
   public String biscuit; 

}

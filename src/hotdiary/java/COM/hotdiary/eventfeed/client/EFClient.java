package COM.hotdiary.eventfeed.client;
import java.awt.*;
import java.applet.*;
import java.rmi.*;
import COM.hotdiary.eventfeed.hdif.*;
import COM.hotdiary.eventfeed.server.*;
import COM.hotdiary.fileutil.*;

public class EFClient {

    public static void main(String args[]) {
	initRmi();
    }

    public static void initRmi() {
       while (true) {
       try {
/*           efserver = (COM.hotdiary.eventfeed.hdif.EFServer)Naming.lookup("rmi://www.hotdiary.com/EFServer"); 
*/

          efserver = (COM.hotdiary.eventfeed.hdif.EFServer)Naming.lookup("rmi://hotdiary.com/EFServer"); 
          break;
       }  catch(Exception e)  {
	   /*  e.printStackTrace();   */
       } 
     }

      try {
      
// Test one event, see if server prints the message
           efserver.feedEvent("Holiday", "Go to Alaska");

       HDLogin sess = new HDLogin();
       sess.login = "smitha";
       sess.passwd = "f16ab";
       sess.biscuit = efserver.authUser(sess);

       HDEvent event = new HDEvent();
       event.biscuit = sess.biscuit;
       event.month = "7";
       event.day = "13";
       event.year = "1999";
       event.min = "0";
       event.hour = "8";
       event.meridian = "PM";
       event.subject = "5k  walk";
       event.desc = "5k marathon walk is for the benefit of Cancer society. portion of the funds will also go to AIDS and get rich funds.";
       event.phone = "408-956-8550";
       event.venue = "Great Mall";
       event.city = "Milpitas";
       event.url = "url";
       event.imgfn = "imgfn";
       event.zone = "Pacific";
     
       efserver.setEvent(event);

       } catch (Exception e) {
           e.printStackTrace();
       }
    }

    public static EFServer efserver;
    
}

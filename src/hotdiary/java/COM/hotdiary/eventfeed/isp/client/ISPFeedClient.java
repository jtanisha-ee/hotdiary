package COM.hotdiary.eventfeed.isp.client;
import java.awt.*;
import java.applet.*;
import java.rmi.*;
import COM.hotdiary.eventfeed.hdif.*;
import COM.hotdiary.eventfeed.isp.server.*;
import COM.hotdiary.fileutil.*;

public class ISPFeedClient {

   public static String main(String[] argv) {
      return(initRmi(argv));
   }

   // argv includes ispdomain name, login, password for auth
   // other details for events 
   public static String initRmi(String[] argv) {
      if (argv.length < 2) return null;
      while (true) {
         try {
            ispfserver = (COM.hotdiary.eventfeed.hdif.EFServer)Naming.lookup("rmi://argv[0]/EFServer");
          break;
         }  catch(Exception e)  {
           /*  e.printStackTrace();   */
         }
      } 

      try {
         if (argv.length == 2) {
	    HDLogin sess = new HDLogin();
            sess.login = argv[1];
            sess.passwd = argv[2];
            // sess.biscuit = ispfserver.authUser(sess);
            return(sess.biscuit);
         } else {
	    HDEvent event = new HDEvent();
            event.biscuit = argv[1];
            event.month =  argv[2];
            event.day =  argv[3];
            event.year =  argv[4];
            event.min = argv[5];
            event.hour =  argv[6];
            event.meridian = argv[7];
            event.subject=  argv[8];
            event.desc =  argv[9];
            event.phone =  argv[10];
            event.venue = argv[11];
            event.city =  argv[12];
            event.url =  argv[13];
            event.imgfn =  argv[14];
            event.zone =  argv[15];
            ispfserver.setEvent(event);
	    return null;
	 }
      }  catch (Exception e) {
         e.printStackTrace();
      }
      return null;
   }
   public static ISPFeedServer ispfserver;
}

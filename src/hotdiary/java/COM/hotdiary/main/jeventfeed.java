package COM.hotdiary.main;

import java.util.Vector;
import COM.hotdiary.eventfeed.hdif.*;
import COM.hotdiary.eventfeed.isp.server.*;

public class jeventfeed {

   public static String main(String[] argv) {

      ISPFeedServer ispfserver = new ISPFeedServer();

      if (argv.length != 2) {
         // authenticate the user and also create event feed records for
	 // that calendar  
         // the print statements are for debug only
         System.out.println("Usage: <login> <password>");
         System.exit(1);
      }

      if (argv.length == 2) {
         return(ispfserver.authUser(argv[0], argv[1]));
      } else {
	 HDEvent event = new HDEvent();
         event.biscuit = argv[0];
         event.month = argv[1];
         event.day = argv[2];
         event.year = argv[3];
         event.min = argv[4];
         event.hour = argv[5];
         event.meridian = argv[6];
         event.subject = argv[7];
         event.desc = argv[8];
         event.phone = argv[9];
         event.venue = argv[10];
         event.city = argv[11];
         event.url = argv[12];
         event.imgfn = argv[13];
         event.zone = argv[14];
         ispfserver.setEvent(event); 
	 return null;
      }
   }
}

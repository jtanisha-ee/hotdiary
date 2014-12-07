package COM.hotdiary.main;

import COM.hotdiary.urlutil.*;
import COM.hotdiary.fileutil.*;

import java.util.*;

public class SendPage {

/**
 * Usage: java SendPage to-pager-no message from
 * This program sends an alphanumeric page to destination party addressed
 * by to-pager-no. The contents of message are in message. The from field
 * is the identification of the sender.
 * The blanks in the message have to be substituted with "%20" as required
 * by SkyTel protocol. 
 * This program exits if the message is empty. The to-pager-no is the PIN
 * number of pager followed by comma sign. 
 */

   public static void main(String args[]) {

      if (args.length != 3) {
         System.out.println("Usage: java SendPage <to-pager-no> <message> <from>");
         FileIO.error("Usage: java SendPage <to-pager-no> <message> <from>");
         System.exit(1);
      }

      StringTokenizer st = new StringTokenizer(args[1]);
      String msg = null;
      if (st.hasMoreTokens()) {
         msg = st.nextToken();
      } else {
           FileIO.error("SendPage " + args[0] + " " + args[2] + ": Empty Message String ");
           System.out.println("SendPage " + args[0] + " " + args[2] + ": Empty Message String ");
           System.exit(1);
      }
      while (st.hasMoreTokens()) {
         msg += "%20" + st.nextToken();
      }
      String pager = args[0] + ",1";
      String urls = "http://www.skytel.com/cgi-bin/page.pl?to=" + pager + "&message=" + "\"" + msg + "\"" + "&from=" + args[2];
      FileIO.status(urls);
      SimpleUrlPost sup = new SimpleUrlPost(urls);
   }
}

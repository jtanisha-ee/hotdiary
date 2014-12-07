package COM.hotdiary.main;

import COM.hotdiary.urlutil.*;
import COM.hotdiary.fileutil.*;

import java.util.*;

public class ExecCGIURL {

/**
 * Usage: java ExecCGIURL
 * This program executes a CGI URL.
 */

   public static void main(String args[]) {

      if (args.length != 1) {
         String message = "Usage: java ExecCGIURL <http-URL>";
         System.out.println(message);
         FileIO.error(message);
         System.exit(1);
      }

      FileIO.status(args[0]);
      SimpleUrlPost sup = new SimpleUrlPost(args[0]);
   }
}

package COM.hotdiary.urlutil;

import java.net.*;
import COM.hotdiary.fileutil.*;

public class SimpleUrlPost {

/**
 * The constructor opens a URL string, typically a CGI command and does not
 * return any response to the user. This is especially useful if
 * no response is required and no interactive communication is necessary
 * with the web server.
 */
   public SimpleUrlPost(String urls) {
      turls = urls;
      try {
         turl = new URL(turls); 
         turl.openStream();
      } catch (Exception e) {
         e.printStackTrace();
         FileIO.error(e.toString());
         FileIO.error(e.getMessage());
         FileIO.printStackTrace(e);
      }
      
   }

   String turls;
   URL turl;
}

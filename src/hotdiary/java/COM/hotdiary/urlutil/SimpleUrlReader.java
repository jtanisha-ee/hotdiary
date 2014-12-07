package COM.hotdiary.urlutil;

import java.net.*;
import java.io.*;

public class SimpleUrlReader {

/**
 * The constructor opens a URL string, typically a CGI command and does not
 * return any response to the user. This is especially useful if
 * no response is required and no interactive communication is necessary
 * with the web server.
 */
   public SimpleUrlReader(String urls) {
      turls = urls;
      try {
         turl = new URL(turls); 
      } catch (Exception e) {
         e.printStackTrace();
      }
   }

   public String getContent() {
      BufferedReader d = null;
      String data = "";
      String inputLine;

      try {
          d = new BufferedReader(new InputStreamReader(turl.openStream()));
    
          while ((inputLine = d.readLine()) != null) {
             //System.out.println(inputLine);
             data += "\n" + inputLine;
          }
    
          d.close(); 
      } catch (Exception e) {
          e.printStackTrace();
      }
      return data;
   }

   String turls;
   URL turl;
}

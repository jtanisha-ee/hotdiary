package COM.hotdiary.calmgmtserver;

import java.net.*;
import java.io.*;

public class CalAppServer {


   public CalAppServer(String[] arg) {
      if (arg.length != 1) {
         System.out.println("Usage: java CalAppServer <port>");
         return;
      }
      port = new Integer(arg[0]).intValue();
      try {
          serverSocket = new ServerSocket(port);
      } catch (Exception e) {
          e.printStackTrace();
          return;
      }
      run();
   }

   public void run() {
      while (true) {
         try {
            connection = serverSocket.accept();
         } catch (Exception e) {
            e.printStackTrace();
            return;
         }
         handleAsyncConnection(connection);
      }
   }

   public void handleAsyncConnection(Socket connection) {
      (new RequestHandler(connection)).start();
   }

   public static void main(String[] arg) {
      CalAppServer caserver = new CalAppServer(arg);      
   }

   ServerSocket serverSocket = null;   
   int port;
   Socket connection = null;
}

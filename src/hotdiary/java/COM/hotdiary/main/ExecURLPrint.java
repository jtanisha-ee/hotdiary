package COM.hotdiary.main;

import COM.hotdiary.urlutil.*;

public class ExecURLPrint {

   public ExecURLPrint(String url) {
      SimpleUrlReader sur = new SimpleUrlReader(url);
      System.out.println(sur.getContent());
   }

   public static void main(String args[]) {
 
      if (args.length != 1) {
         System.out.println("Usage: java COM.hotdiary.main.ExecURLPrint <url>");
         System.exit(1);
      }
  
      ExecURLPrint up = new ExecURLPrint(args[0]);
   }
}

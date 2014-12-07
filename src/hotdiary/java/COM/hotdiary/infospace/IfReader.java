package COM.hotdiary.infospace;

import COM.hotdiary.urlutil.*;

public class IfReader {

   public IfReader(String fname, String lname, String city, String state) {
      SimpleUrlReader sur = new SimpleUrlReader("http://kevdb.infospace.com/info/kevdb?OTMPL=%2Fres%2Fr1.html&QFM=N&QK=5&XNavigation=&QN=" + lname + "&QF=" + fname + "&QC=" + city + "&QS=" + state + "&QD=1&KCFG=us");
      System.out.println(sur.getContent());
   }

   public static void main(String args[]) {
 
      if (args.length != 4) {
         System.out.println("Usage: java COM.hotdiary.infospace.IfReader <fname> <lname> <city> <state>");
         System.exit(1);
      }
  
      IfReader ir = new IfReader(args[0], args[1], args[2], args[3]);
   }

}

package COM.hotdiary.fileutil;

import java.io.*;
import java.util.*;

/**
  * This is an example of an object that appends a string to
  * a file.
  */

public class FileIO {

   static String logdir = null;
   static String basedir = "/usr/local/hotdiary/logs/";
   static String statusfile = "hdstatus.log";
   static String errorfile = "hderror.log";

   public static void appendString(String file, String message) {
      FileWriter raf = null;
      try {
         message = (new Date()).toString() + " " + message;
         raf = new FileWriter(file, true);
         char[] c = new char[message.length()];
         message.getChars(0, message.length(), c, 0);
         raf.write(c);
         raf.write('\n');
         raf.close();
      } catch (Exception e) {
         printStackTrace(e);
      }
   }

   public static void status(String message) {
      appendString(basedir + statusfile, message);
   }

   public static void error(String message) {
      appendString(basedir + errorfile, message);
   }

   public static void printStackTrace(Exception e) {
      FileOutputStream err = null;
      try {
         err = new FileOutputStream(basedir + errorfile, true);
         PrintStream errPrintStream = new PrintStream(err);
         System.setErr(errPrintStream);
         e.printStackTrace(errPrintStream);
         err.close();
      } catch (Exception e1) {
         e1.printStackTrace();
      }
   }

/*
   public static void main(String argv[]) {
      try {
         FileWriter raf = new FileWriter("/tmp/test", true);
         String s = "This is a test";
         char[] c = new char[s.length()];
         s.getChars(0, s.length(), c, 0);
         raf.write(c);
         raf.write('\n');
         raf.close();
      } catch (Exception e) {
         e.printStackTrace();
      }
   }
*/

}

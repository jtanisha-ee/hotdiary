package COM.hotdiary.ntsetup;
import java.sql.*;
import java.io.*;
import java.awt.*;

/**
 * The DbGet is an application that fetches data from a database.
 * It is typically used for doing select, and returns a resultset.
 * The program takes as input an SQL statement, an output
 * file name, and the full-path name of a program.
 */

public class ntsetup {
 
   public void ntsetupdoc() {
      ntsetupui setuihtdoc = new ntsetupui();
      setuihtdoc.ntsetui("Enter the path of your HTML Documents",  "htdocs"); 
   }

   public static void main(String argv[])  {
      (new ntsetup()).ntsetupdoc();
   }
 

/*
   public ntLicense() {
   }

   public ntHtDocsPath() {
   }

   public ntCgiPath() {
   }

   public isntProxySetup() {
   }

   public ntProxyPortSetup() {
   }
   public ntProxydomainSetup() {
   }
*/
}

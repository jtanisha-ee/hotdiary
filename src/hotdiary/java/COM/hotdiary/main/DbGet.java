package COM.hotdiary.main;

import java.sql.*;
import java.io.*;

import COM.hotdiary.db.*;

/**
 * The DbGet is an application that fetches data from a database.
 * It is typically used for doing select, and returns a resultset.
 * The program takes as input an SQL statement, an output
 * file name, and the full-path name of a program.
 */

public class DbGet {

   /**
    * Create an instance of pgutil, and pass it the sql statement.
    */
   public DbGet(String sql, String ofile, String pprog) {
      pgutil = new PgUtil(sql); 
      outputfile = ofile;
      prog = pprog; 
      if (outputfile != null) {
         try {
            fw = new FileWriter(ofile);
         } catch (Exception e) {
            e.printStackTrace();
         }
      }
   }

   /**
    * Execute the current statement. Print the output to a file. Execute
    * a perl script, and pass the output file as a parameter to the script.
    * Connect the output of the script to the inputstream of this java
    * program. Read the data from the inputstream, and print it to stdout.
    */
   public void execute() {
      pgutil.executeGet();
      pgutil.printData(fw);
      if (fw == null) return;
      try {
         fw.close();
         if (prog != null) {
            Process p = Runtime.getRuntime().exec(prog + " " + "outputfile=" + outputfile);
            InputStream is = p.getInputStream();
            byte b[] = new byte[256];
            int len;
            try {
                while ((len = is.read(b)) != -1) {
                   System.out.print(new String(b, 0, len)); 
                }
            } catch (NullPointerException e) {
            }
         }
      } catch (Exception e) {
         e.printStackTrace();
      }
      
   }

   /**
    * This is the main. Validate the input args, create an instance of DbGet
    * and execute the statement.
    */
   public static void main(String args[]) {
      if ((args.length < 1) || (args.length > 3)) {
         System.out.println("Usage: java DbGet <sql-statement> <output-file> <program>"); 
         System.exit(1);
      }
      String ofile, prog;
      if (args.length >= 2) {
         ofile = args[1]; 
      } else {
         ofile = null;
      }
      if (args.length == 3) {
         prog = args[2];
      } else {
         prog = null;
      }
      dbget = new DbGet(args[0], ofile, prog);
      dbget.execute();
   }

   static DbGet dbget;
   private PgUtil pgutil;
   private String outputfile;
   private String prog;
   FileWriter fw;
}

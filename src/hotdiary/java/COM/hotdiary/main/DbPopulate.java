package COM.hotdiary.main;

import COM.hotdiary.db.*;

/**
 * The DbPopulate is an application that populates a table.
 * The program takes as input an ascii file of columns separated by
 * by a separator character. The separator is passed as an input to
 * to the program.
 */

public class DbPopulate {

   /**
    * Create an instance of pgutil, and pass it the sql statement.
    */
   public DbPopulate(String sql) {
      pgutil = new PgUtil(sql); 
   }

   /**
    * Execute the current statement.
    */
   public void execute() {
      pgutil.executeSet();
   }

   /**
    * This is the main. Validate the input args, create an instance of 
    * DbPopulate and execute the statement.
    */
   public static void main(String args[]) {
      if (args.length != 2) {
         System.out.println("Usage: java DbPopulate <sql-statement> <separator>"); 
         System.exit(1);
      }
      dbPopulate = new DbPopulate(args[0]);
      dbPopulate.execute();
   }

   static DbPopulate dbPopulate;
   private PgUtil pgutil;
}
